// PPS canonical hash (JCS-like) utility
// Usage:
//  node tests/pps-conformance/canonicalize.js compute <path>
//  node tests/pps-conformance/canonicalize.js write <path>

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

function stringifyCanonical(value) {
  const t = typeof value;
  if (value === null) return 'null';
  if (t === 'number' || t === 'boolean') return JSON.stringify(value);
  if (t === 'string') return JSON.stringify(value);
  if (Array.isArray(value)) {
    return '[' + value.map(v => stringifyCanonical(v)).join(',') + ']';
    }
  if (t === 'object') {
    const keys = Object.keys(value).sort();
    const parts = [];
    for (const k of keys) {
      parts.push(JSON.stringify(k) + ':' + stringifyCanonical(value[k]));
    }
    return '{' + parts.join(',') + '}';
  }
  throw new Error('Unsupported type in canonicalizer: ' + t);
}

function sanitizeForHash(input) {
  // deep clone and drop integrity.canonical_hash for deterministic hashing
  const obj = JSON.parse(JSON.stringify(input));
  if (obj && obj.integrity && typeof obj.integrity === 'object') {
    if ('canonical_hash' in obj.integrity) delete obj.integrity.canonical_hash;
  }
  return obj;
}

function computeCanonicalHash(objInput) {
  const obj = sanitizeForHash(objInput);
  const canonical = stringifyCanonical(obj);
  const hash = crypto.createHash('sha256').update(Buffer.from(canonical, 'utf8')).digest();
  // base64url
  const b64 = hash.toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/g, '');
  return 'sha256:' + b64;
}

function loadJson(filePath) {
  const abs = path.resolve(process.cwd(), filePath);
  return { abs, data: JSON.parse(fs.readFileSync(abs, 'utf8')) };
}

function main() {
  const mode = process.argv[2];
  const target = process.argv[3];
  if (!mode || !target || !['compute', 'write'].includes(mode)) {
    console.error('Usage: canonicalize.js <compute|write> <path>');
    process.exit(2);
  }
  const { abs, data } = loadJson(target);
  const hash = computeCanonicalHash(data);
  if (mode === 'compute') {
    console.log(hash);
    return;
  }
  if (!data.integrity) data.integrity = {};
  data.integrity.canonical_hash = hash;
  fs.writeFileSync(abs, JSON.stringify(data, null, 2) + '\n', 'utf8');
  console.log('WROTE', hash, 'to', target);
}

main();


