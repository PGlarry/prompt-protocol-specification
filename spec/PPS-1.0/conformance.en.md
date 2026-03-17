---
title: PPS v1.0 Conformance & Test Specification
lang: en
status: draft
version: 1.0.0
---

# 1. Scope
Defines the minimum compliance tests for PPS v1.0: Schema validation, policy checks, reproducibility, and hash consistency. Output is intended for human review and CI.

# 2. Required Validations
1) JSON Schema (REQ-001): `spec/pps-1.0.schema.json`
2) Policy checks (REQ-050/051/052/053, 180..183, 320..323)
3) Canonical hash consistency (REQ-300)
4) Decode determinism (REQ-012/302) and cross-platform replay (within tolerance)

# 3. Tools & Commands
- Canonicalize / hash: `node tests/pps-conformance/canonicalize.js <file> --write`
- Schema validation: `node tests/pps-conformance/validate.js <file>`
- Policy checks: `node tests/pps-conformance/policy_checks.js <file> --json`
- Auto-fix: `node tests/pps-conformance/auto_fix.js <file> --write`

# 4. Output Format (Recommended)
Policy check `--json`:
```json
{ "pass": true, "warnings": [], "issues": [{ "type": "tool_capability_missing", "message": "..." }] }
```

# 5. CI Integration (Recommended)
In CI, for each file in `spec/examples/*.json`: canonicalize → Schema → policy → (if needed) auto-fix → summarize. Failure blocks the pipeline.
