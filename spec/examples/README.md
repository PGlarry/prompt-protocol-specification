# PPS Example Envelopes

This directory contains annotated example PPS envelopes demonstrating conformance testing scenarios.

| File | Scenario | Expected Result |
|------|----------|----------------|
| `minimal.json` | Minimum valid envelope (what only) | ✅ PASS |
| `minimal.after.json` | Minimal envelope after auto-completion | ✅ PASS |
| `classification.json` | Text classification with output schema | ✅ PASS |
| `citation_required.json` | Research task requiring evidence | ✅ PASS |
| `rag_citations_required.json` | RAG pipeline with citations | ✅ PASS |
| `budget_violation.json` | how_much budget constraint violation | ❌ FAIL (policy) |
| `min_budget_degradation.json` | Budget degradation below minimum | ❌ FAIL (policy) |
| `gdpr_missing_no_pii.json` | GDPR declared but no_pii missing | ❌ FAIL (REQ-182) |
| `json_interface_missing_schema.json` | JSON output declared without schema | ❌ FAIL (REQ-175) |
| `adversarial.json` | Prompt injection attempt | ❌ FAIL (security) |
| `mixed_adversarial.json` | Mixed adversarial input (before fix) | ❌ FAIL |
| `mixed_adversarial.after.json` | After auto-fix applied | ✅ PASS |
| `prompt_injection_url.json` | URL-based prompt injection | ❌ FAIL (REQ-052) |
| `tool_overreach.json` | Tool not in capabilities whitelist | ❌ FAIL (REQ-181) |

## Running Validation

```bash
# Validate a single file
node ../../tests/pps-conformance/validate.js minimal.json

# Run policy checks
node ../../tests/pps-conformance/policy_checks.js minimal.json --json

# Check locks compliance (before/after pair)
node ../../tests/pps-conformance/locks_compliance.js \
  mixed_adversarial.json mixed_adversarial.after.json

# Run all examples
node ../../tests/pps-conformance/summary.js
```

## Adding New Examples

1. Create a `.json` file following the PPS schema (`schema/pps-1.0.schema.json`).
2. Add a row to the table above with the expected result.
3. Run the full test suite to confirm behavior.
4. Submit a PR with both the example and updated README.
