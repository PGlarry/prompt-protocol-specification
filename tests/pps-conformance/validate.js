// Minimal JSON Schema validation for PPS envelopes
// Usage: node tests/pps-conformance/validate.js <path-to-envelope.json>

const fs = require('fs');
const path = require('path');
const Ajv = require('ajv/dist/2020');

function loadJson(filePath) {
  const abs = path.resolve(process.cwd(), filePath);
  return JSON.parse(fs.readFileSync(abs, 'utf8'));
}

function main() {
  const target = process.argv[2];
  if (!target) {
    console.error('Usage: validate.js <path-to-envelope.json>');
    process.exit(2);
  }

  const schema = loadJson('spec/pps.schema.json');
  const data = loadJson(target);

  const ajv = new Ajv({ allErrors: true, strict: false, validateFormats: false });
  const validate = ajv.compile(schema);
  const ok = validate(data);

  if (ok) {
    console.log('VALID');
  } else {
    console.log('INVALID');
    console.log(JSON.stringify(validate.errors, null, 2));
    process.exit(1);
  }
}

main();


