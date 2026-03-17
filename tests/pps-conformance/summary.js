const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

function run(cmd, args) {
  const res = spawnSync(cmd, args, { stdio: 'pipe', encoding: 'utf8' });
  return { code: res.status, out: res.stdout.trim(), err: res.stderr.trim() };
}

function main() {
  const examplesDir = path.resolve(process.cwd(), 'spec/examples');
  const files = fs.readdirSync(examplesDir).filter(f => f.endsWith('.json'));
  const rows = [];

  for (const f of files) {
    const full = path.join(examplesDir, f);
    const val = run('node', ['tests/pps-conformance/validate.js', full]);
    const pol = run('node', ['tests/pps-conformance/policy_checks.js', full, '--json']);
    let policy = { pass: false, warnings: [], issues: [] };
    try { policy = JSON.parse(pol.out || '{}'); } catch {}

    // Optional locks compliance: if <file>.after.json exists, compare
    const afterPath = path.join(examplesDir, f.replace(/\.json$/, '.after.json'));
    let locks = { pass: true };
    if (fs.existsSync(afterPath)) {
      const lres = run('node', ['tests/pps-conformance/locks_compliance.js', full, afterPath, '--json']);
      try { locks = JSON.parse(lres.out || '{}'); } catch { locks = { pass: false }; }
    }

    rows.push({
      file: f,
      schema: val.code === 0 ? 'VALID' : 'INVALID',
      policy: policy.pass ? 'PASS' : 'FAIL',
      warnings: (policy.warnings || []).length,
      issues: (policy.issues || []).length,
      locks: fs.existsSync(afterPath) ? (locks.pass ? 'PASS' : 'FAIL') : 'N/A'
    });
  }

  const header = ['File','Schema','Policy','Warnings','Issues','Locks'];
  const lines = [header.join('\t')];
  for (const r of rows) {
    lines.push([r.file, r.schema, r.policy, String(r.warnings), String(r.issues), r.locks].join('\t'));
  }
  console.log(lines.join('\n'));
}

main();


