// PPS locks compliance checker
// Usage: node tests/pps-conformance/locks_compliance.js <before.json> <after.json> [--json]

const fs = require('fs');
const path = require('path');

function loadJson(p) {
  const abs = path.resolve(process.cwd(), p);
  return JSON.parse(fs.readFileSync(abs, 'utf8'));
}

function get(obj, pointer) {
  if (!pointer || pointer === '/') return obj;
  if (!pointer.startsWith('/')) return undefined;
  const parts = pointer.split('/').slice(1).map(s => s.replace(/~1/g, '/').replace(/~0/g, '~'));
  let cur = obj;
  for (const key of parts) {
    if (cur == null) return undefined;
    cur = cur[key];
  }
  return cur;
}

function main() {
  const beforePath = process.argv[2];
  const afterPath = process.argv[3];
  const asJson = process.argv.includes('--json');
  if (!beforePath || !afterPath) {
    console.error('Usage: locks_compliance.js <before.json> <after.json> [--json]');
    process.exit(2);
  }
  const before = loadJson(beforePath);
  const after = loadJson(afterPath);

  const locks = ((before.body && before.body.how_meta && before.body.how_meta.governance && Array.isArray(before.body.how_meta.governance.locks))
    ? before.body.how_meta.governance.locks : []);

  const diffs = [];
  for (const p of locks) {
    if (typeof p !== 'string' || !p.startsWith('/')) continue;
    const bv = get(before, p);
    const av = get(after, p);
    const same = JSON.stringify(bv) === JSON.stringify(av);
    if (!same) {
      diffs.push({ pointer: p, before: bv, after: av });
    }
  }

  const pass = diffs.length === 0;
  if (asJson) {
    console.log(JSON.stringify({ pass, diffs }, null, 2));
    process.exit(pass ? 0 : 1);
  }
  if (pass) {
    console.log('LOCKS: PASS');
  } else {
    console.log('LOCKS: FAIL');
    for (const d of diffs) {
      console.log('-', d.pointer);
    }
    process.exit(1);
  }
}

main();


