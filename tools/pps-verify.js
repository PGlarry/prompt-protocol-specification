#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

function readJson(p) {
  const abs = path.resolve(process.cwd(), p);
  return JSON.parse(fs.readFileSync(abs, 'utf8'));
}

function run(cmd, args) {
  const res = spawnSync(cmd, args, { stdio: 'pipe', encoding: 'utf8' });
  return { code: res.status ?? 0, out: (res.stdout || '').trim(), err: (res.stderr || '').trim() };
}

function main() {
  const target = process.argv[2];
  if (!target) {
    console.error('Usage: node tools/pps-verify.js <path-to-envelope.json>');
    process.exit(2);
  }
  const data = readJson(target);
  const declared = data?.integrity?.canonical_hash || '';
  if (!declared) {
    console.error('Missing integrity.canonical_hash in envelope');
    process.exit(1);
  }
  const r = run('node', ['tests/pps-conformance/canonicalize.js', 'compute', target]);
  if (r.code !== 0) {
    console.error('canonicalize failed:', r.err || r.out);
    process.exit(1);
  }
  const computed = r.out;
  const pass = declared === computed;
  console.log(JSON.stringify({ file: target, declared, computed, pass }, null, 2));
  process.exit(pass ? 0 : 1);
}

main();
