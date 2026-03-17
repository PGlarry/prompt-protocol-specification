// PPS Policy Checks (beyond schema): citations, capabilities, budgets, governance
// Usage: node tests/pps-conformance/policy_checks.js <path>

const fs = require('fs');
const path = require('path');

function loadJson(filePath) {
  const abs = path.resolve(process.cwd(), filePath);
  return { abs, data: JSON.parse(fs.readFileSync(abs, 'utf8')) };
}

function hasCap(capList, key) {
  if (!Array.isArray(capList)) return false;
  if (capList.includes(key)) return true;
  // simple CN synonyms
  if (key === 'web_browse') {
    return capList.some(x => /浏览|web/i.test(String(x)));
  }
  if (key === 'function_call') {
    return capList.some(x => /函数调用|function/i.test(String(x)));
  }
  return false;
}

function checkPolicy(env) {
  const issues = [];
  const warn = [];
  const violations = []; // { type, message }
  const b = env.body || {};
  const governance = (b.how_meta && b.how_meta.governance) ? b.how_meta.governance : {};
  const locks = Array.isArray(governance.locks) ? governance.locks : [];

  // 1) citations_required => evidence non-empty
  const citationsRequired = b.where && b.where.citations_required === true;
  const evidence = (b.where && Array.isArray(b.where.evidence)) ? b.where.evidence : [];
  if (citationsRequired && evidence.length === 0) {
    const msg = 'citations_required=true but evidence is empty';
    issues.push(msg);
    violations.push({ type: 'citations_missing_evidence', message: msg });
  }

  // 2) governance.citations => align with citations_required
  if (governance.citations === true && !citationsRequired) {
    warn.push('governance.citations=true but where.citations_required is false');
  }
  // 2c) locked paths should not be altered by regeneration (cannot verify without prior state)
  // We at least validate pointer format and existence
  for (const p of locks) {
    if (typeof p !== 'string' || !p.startsWith('/')) {
      const msg = 'invalid lock pointer (must start with /): ' + String(p);
      issues.push(msg);
      violations.push({ type: 'lock_pointer_invalid', message: msg });
    }
  }

  // 2b) interface json must provide schema
  const iface = b.how_interface || null;
  if (iface && iface.format === 'json' && (typeof iface.schema !== 'object' || iface.schema === null)) {
    const msg = 'json interface requires output schema (how_interface.schema)';
    issues.push(msg);
    violations.push({ type: 'interface_json_missing_schema', message: msg });
  }

  // 3) tools capability checks
  const tools = (b.how_to_do && Array.isArray(b.how_to_do.tools)) ? b.how_to_do.tools : [];
  const caps = (b.who && Array.isArray(b.who.capabilities)) ? b.who.capabilities : [];
  for (const t of tools) {
    if (t === 'web_browse' && !hasCap(caps, 'web_browse')) {
      const msg = 'tool web_browse requires capability web_browse';
      issues.push(msg);
      violations.push({ type: 'tool_capability_missing', message: msg });
    }
    if (String(t).startsWith('fn:') && !hasCap(caps, 'function_call')) {
      const msg = 'function-like tool requires capability function_call / 函数调用';
      issues.push(msg);
      violations.push({ type: 'tool_capability_missing', message: msg });
    }
  }

  // 3b) tool-policy contradiction (Why.constraints vs tools)
  const constraints = (b.why && Array.isArray(b.why.constraints)) ? b.why.constraints : [];
  const forbidBrowse = constraints.some(x => /禁止外部浏览|不允许外部链接|仅使用提供的证据/.test(String(x)));
  if (forbidBrowse && tools.includes('web_browse')) {
    const msg = 'policy forbids external browsing but tools include web_browse';
    issues.push(msg);
    violations.push({ type: 'policy_forbid_browse_tool_present', message: msg });
  }

  // 3c) external URL presence under forbidden browsing
  const taskStr = b.what && typeof b.what.task === 'string' ? b.what.task : '';
  const hasUrl = /(https?:\/\/|www\.)/i.test(taskStr);
  if (forbidBrowse && hasUrl) {
    const msg = 'policy forbids external browsing but task contains external URL';
    issues.push(msg);
    violations.push({ type: 'policy_forbid_browse_url_present', message: msg });
  }

  // 3d) generic capability check for non-fn tools
  for (const t of tools) {
    if (!String(t).startsWith('fn:') && t !== 'web_browse') {
      if (!caps.includes(t)) {
        const msg = `tool ${t} requires capability ${t}`;
        issues.push(msg);
        violations.push({ type: 'tool_capability_missing', message: msg });
      }
    }
  }

  // 4) content quantification sanity (content-facing, open fields)
  // how_much 为开放键名的量化容器：不做系统配额限制，仅做：
  // a) 数量门槛统计（非强制，由实现自定阈值，此处仅提示）；
  // b) 对所有键值做极端值启发式警告。
  const hm = (b.how_much && typeof b.how_much === 'object') ? b.how_much : {};
  const keys = Object.keys(hm || {});
  const nonEmptyCount = keys.filter(k => {
    const v = hm[k];
    if (v === null || v === undefined) return false;
    if (typeof v === 'string') return v.trim().length > 0;
    if (Array.isArray(v)) return v.length > 0;
    if (typeof v === 'object') return Object.keys(v).length > 0;
    if (typeof v === 'number') return true;
    if (typeof v === 'boolean') return true;
    return false;
  }).length;
  if (nonEmptyCount === 0) {
    warn.push('how_much has no quantification items (open set, consider adding 1+)');
  }
  for (const k of keys) {
    const v = hm[k];
    const s = typeof v === 'string' ? v : JSON.stringify(v);
    if (typeof s === 'string' && /\b(\d{6,}|10{5,})\b/.test(s)) {
      warn.push(`how_much.${k} seems extremely large: ${s}`);
    }
  }

  // 5) determinism hint
  const dec = env.header && env.header.decode ? env.header.decode : {};
  if (!(dec.temperature === 0 && dec.top_p === 1)) {
    warn.push('decode not strictly deterministic (temperature!=0 or top_p!=1)');
  }

  // 6) GDPR compliance requires no_pii policy
  const headerCompliance = env.header && Array.isArray(env.header.compliance) ? env.header.compliance : [];
  if (headerCompliance.map(x => String(x).toLowerCase()).includes('gdpr')) {
    const hasNoPII = b.who && Array.isArray(b.who.policy) && b.who.policy.some(x => /no[_-]?pii|不包含个人信息|禁止个人敏感信息/i.test(String(x)));
    if (!hasNoPII) {
      const msg = 'gdpr compliance requires an explicit no_pii policy in who.policy';
      issues.push(msg);
      violations.push({ type: 'gdpr_missing_no_pii', message: msg });
    }
  }

  return { issues, warn, violations };
}

function main() {
  const target = process.argv[2];
  const asJson = process.argv.includes('--json');
  if (!target) {
    console.error('Usage: policy_checks.js <path>');
    process.exit(2);
  }
  const { data } = loadJson(target);
  const { issues, warn, violations } = checkPolicy(data);

  if (asJson) {
    const payload = { pass: issues.length === 0, warnings: warn, issues: violations };
    console.log(JSON.stringify(payload, null, 2));
    process.exit(issues.length === 0 ? 0 : 1);
  } else {
    for (const w of warn) console.log('WARN:', w);
    if (issues.length === 0) {
      console.log('POLICY: PASS');
      return;
    }
    console.log('POLICY: FAIL');
    for (const e of issues) console.log(' -', e);
    process.exit(1);
  }
}

main();


