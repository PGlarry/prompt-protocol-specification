---
title: PPS v1.0 Security & Privacy (Threat Model)
lang: en
status: draft
version: 1.0.0
---

# 1. Threat Model
- Injection (prompt / URL / evidence poisoning)
- Overreach (undeclared tools or external channels)
- Compliance risk (PII, missing citations, cross-jurisdiction restrictions)

# 2. Countermeasures (Normative References)
- Interface whitelist & capability sandbox: `how_to_do.tools ⊆ who.capabilities` (REQ-181)
- No-browse constraint: `no_external_browse` ⇒ disable `web_browse` and remove URLs (REQ-052/183)
- Citation consistency: `citations_required` ⇒ `evidence` non-empty (REQ-180)
- GDPR: `gdpr` ⇒ `no_pii` (REQ-182)
- Causal non-interference: unauthorized inputs must not alter the output distribution of authorized inputs (aligns with paper body and normative spec)

# 3. Residual Risks & Boundaries
- Minor drift from uncontrolled updates to third-party models or retrieval sources (mitigated by deterministic decoding and evidence snapshots)
- Subjectivity in manual annotation or external scoring (reduced by KPI thresholds and schema validation)
