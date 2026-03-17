// Auto-fix common policy issues in PPS envelopes
// Usage: node tests/pps-conformance/auto_fix.js <path> [--write]

const fs = require('fs');
const path = require('path');

function load(filePath) {
  const abs = path.resolve(process.cwd(), filePath);
  return { abs, data: JSON.parse(fs.readFileSync(abs, 'utf8')) };
}

function save(abs, obj) {
  fs.writeFileSync(abs, JSON.stringify(obj, null, 2) + '\n', 'utf8');
}

function ensureArray(obj, key) {
  if (!obj[key]) obj[key] = [];
  if (!Array.isArray(obj[key])) obj[key] = [obj[key]];
}

function autoFix(env) {
  const b = env.body || {};
  // 1) If why forbids external browsing, drop 'web_browse' from tools (flat only)
  const constraints = (b.why && Array.isArray(b.why.constraints)) ? b.why.constraints : [];
  const forbidBrowse = constraints.some(x => /禁止外部浏览|不允许外部链接|仅使用提供的证据/.test(String(x)));
  if (forbidBrowse && b.how_to_do && Array.isArray(b.how_to_do.tools)) {
    b.how_to_do.tools = b.how_to_do.tools.filter(t => t !== 'web_browse');
  }

  // 1b) remove URLs from task if browsing is forbidden
  if (forbidBrowse && b.what && typeof b.what.task === 'string') {
    b.what.task = b.what.task.replace(/https?:\/\/\S+/ig, '[URL_REMOVED]');
  }

  // 2) If citations_required=true and evidence empty, inject placeholder evidence
  if (!b.where) b.where = {};
  if (Array.isArray(b.where)) {
    // if where was mistakenly converted to array, restore first element or empty object
    b.where = b.where[0] && typeof b.where[0] === 'object' ? b.where[0] : {};
  }
  if (b.where.citations_required === true) {
    if (!Array.isArray(b.where.evidence)) b.where.evidence = [];
    if (b.where.evidence.length === 0) {
      b.where.evidence.push({ uri: 'content://placeholder', digest: 'sha256-PLACEHOLDER', title: 'Placeholder Evidence' });
    }
  }

  // 3) If tools prefixed with fn: exist but capability missing, add 'function_call' (flat only)
  if (b.how_to_do && Array.isArray(b.how_to_do.tools) && b.who) {
    const hasFn = b.how_to_do.tools.some(t => String(t).startsWith('fn:'));
    if (hasFn) {
      if (!Array.isArray(b.who.capabilities)) b.who.capabilities = [];
      if (!b.who.capabilities.includes('function_call')) {
        b.who.capabilities.push('function_call');
      }
    }
  }

  // 4) If interface.json missing schema, copy from body.what.output_schema if present (flat only)
  if (b.how_interface && b.how_interface.format === 'json') {
    const iface = b.how_interface;
    if (typeof iface.schema !== 'object' || iface.schema === null) {
      if (b.what && typeof b.what.output_schema === 'object') {
        iface.schema = b.what.output_schema;
      }
    }
  }

  // 5) If header.compliance contains gdpr, inject no_pii policy if missing
  const headerCompliance = (env.header && Array.isArray(env.header.compliance)) ? env.header.compliance.map(x => String(x).toLowerCase()) : [];
  if (headerCompliance.includes('gdpr')) {
    if (!b.who) b.who = {};
    if (!Array.isArray(b.who.policy)) b.who.policy = [];
    if (!b.who.policy.some(x => /no[_-]?pii|不包含个人信息|禁止个人敏感信息/i.test(String(x)))) {
      b.who.policy.push('no_pii');
    }
  }

  env.body = b;
  return env;
}

function main() {
  const target = process.argv[2];
  const write = process.argv.includes('--write');
  if (!target) {
    console.error('Usage: auto_fix.js <path> [--write]');
    process.exit(2);
  }
  const { abs, data } = load(target);
  const fixed = autoFix(data);
  if (write) {
    save(abs, fixed);
    console.log('FIXED and wrote', target);
  } else {
    console.log(JSON.stringify(fixed, null, 2));
  }
}

main();


