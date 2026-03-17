# PPS Conformance Test Suite (Draft)

This suite validates 5W3H-PPS envelopes. It supports PPS v1.0 mode with schema, policy and reproducibility checks.

## Validate with Node (AJV)

1) Install dependencies (project root):
```
npm i -D ajv
```

2) Run validator (default schema):
```
node tests/pps-conformance/validate.js spec/examples/minimal.json | cat
node tests/pps-conformance/validate.js spec/examples/classification.json | cat
```

Expected: `VALID` for both examples.

## PPS v1.0 Mode

Schema:
```
node tests/pps-conformance/validate.js spec/examples/minimal.json --schema spec/pps-1.0.schema.json | cat
```

Policy (JSON output with typed violations):
```
node tests/pps-conformance/policy_checks.js spec/examples/mixed_adversarial.json --json | cat
```

Canonicalize and write hash:
```
node tests/pps-conformance/canonicalize.js spec/examples/minimal.json --write
```

## Notes
- The validator currently disables strict format validation to avoid extra deps. Production pipelines should enable `ajv-formats` and require date/datetime formats.
- `integrity.canonical_hash` is a placeholder; production should compute a canonicalized hash of the envelope.

## Conformance Summary (CSV)

Generate an overview CSV for all examples:
```
npm run pps:summary
```
Output: `tests/pps-conformance/summary.csv` (may be extended to include violation types and fixes in future).
