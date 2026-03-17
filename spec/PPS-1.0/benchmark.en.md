---
title: PPS v1.0 Benchmark & Metrics (Informative)
lang: en
status: draft
version: 1.0.0
---

# 1. Objective
Quantify protocol-layer capability: reproducibility, governance effectiveness, and resource explicitness.

# 2. Metrics
- Policy capture rate = FAIL count / total cases (by type: injection, overreach, citation, GDPR, budget)
- Auto-fix success rate = post-fix PASS count / cases that triggered auto-fix
- Replay consistency rate = proportion of multi-platform replays that are consistent (or within tolerance)
- Resource budget explicitness rate = proportion of cases containing a `how_much` budget field

## 2.1 Partial-Spec / Free-Combination Ablation
- Input setup: provide only `what.task`; for the remaining 7 dimensions randomly select subsets for the system to complete (following REQ-341..343).
- Evaluation items:
  - Compliance retention rate: proportion that still satisfies cross-field invariants (REQ-180..183) after completion
  - Alignment robustness: KPI pass rate vs. number of provided dimensions curve (0..7)
  - Budget deviation: distribution of deviation between completed resource budget and target configuration

# 3. Data Sources
- `issues[].type` from `tests/pps-conformance/policy_checks.js --json`
- `fixesApplied` from `auto_fix.js` (exported by subsequent script)
- `summary.js` aggregates and generates `summary.csv` and `benchmark.json`
