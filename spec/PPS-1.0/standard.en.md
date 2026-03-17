---
title: Prompt Protocol Specification (PPS) v1.0 — Normative Specification (English)
status: community-specification
version: 1.0.0
lang: en
---

## Table of Contents

| Section | Content |
|---------|---------|
| [§1](#1-scope) | Scope |
| [§2](#2-terms) | Terms |
| [§3](#3-data-model-normative-schema) | Data Model (8 Dimensions) |
| [§4](#4-header-required) | Header |
| [§5](#5-body-required) | Body |
| [§6](#6-integrity-required) | Integrity |
| [§7](#7-determinism--replay) | Determinism & Replay |
| [§8](#8-security--compliance) | Security & Compliance |
| [§9](#9-conformance) | Conformance |
| [§10](#10-versioning) | Versioning |
| [§11](#11-interoperability-profile) | Interoperability Profile |
| [§12](#12-reference-implementation-informative) | Reference Implementation |
| [Annex A](#annex-a-informative-controlled-constraint-vocabulary) | Constraint Vocabulary |
| [Annex B](#annex-b-informative-pps-content-profile--strictness-thresholds) | Conformance Thresholds |
| [Annex C](#annex-c-informative-minimal-interoperable-example) | Minimal Example |
| [Annex D](#annex-d-informative-validation-checklists) | Validation Checklists |
| [Annex E](#annex-e-informative-pps-qr-optional-binding-specification) | PPS-QR Binding |

---

# 1. Scope

This specification defines the minimum interoperable implementation of PPS (Prompt Protocol Specification), a human-AI interaction instruction protocol. Normative requirements are expressed using MUST / SHOULD / MAY (per RFC 2119) and carry REQ identifiers.

# 2. Terms

- **Envelope**: The protocol carrier for a single interaction, consisting of `header`, `body`, and `integrity`.
- **Canonicalization**: Deterministic ordering and serialization of JSON to produce a stable hash.
- **Deterministic Decoding**: Fixed decoding parameters enabling reproducible replay.

# 3. Data Model (Normative Schema)

Implementors MUST accept and produce Envelopes conforming to `schema/pps-1.0.schema.json` (REQ-001).

## 3.1 Eight Dimensions and JSON Paths (Normative Mapping)

- **REQ-100 (What)**: MUST provide `body.what.task`; if output is structured JSON, SHOULD provide `body.what.output_schema`.
  - JSON path: `/body/what/{task, input_schema?, output_schema?}`

- **REQ-110 (Why)**: SHOULD list `body.why.goals`; constraints SHOULD come from the controlled vocabulary (Annex A), e.g. `no_external_browse`, `citations_required`, `use_provided_evidence`.
  - JSON path: `/body/why/{goals?, constraints?}`

- **REQ-120 (Who)**: SHOULD specify `persona`; if tools will be used, MUST whitelist them in `who.capabilities`.
  - JSON path: `/body/who/{persona?, capabilities?, policy?}`

- **REQ-130 (When)**: MUST provide at least one of `timeframe` or `validity_window`.
  - JSON path: `/body/when/{timeframe?, validity_window?, staleness_policy?}`

- **REQ-140 (Where)**: If `citations_required=true`, MUST provide at least one `evidence` entry; evidence SHOULD include `digest` and `title`.
  - JSON path: `/body/where/{environment?, evidence[], jurisdiction?, citations_required?}`

- **REQ-150 (How-to-do)**: SHOULD specify `paradigm` and `steps`; any `tools` used MUST satisfy REQ-181 (capability constraint).
  - JSON path: `/body/how_to_do/{paradigm?, steps?, tools?}`

- **REQ-160 (How-much)**: SHOULD specify quantitative elements targeting the *generated content itself* (e.g. length, structure, detail density, quality guidance, cultural depth). Field names are an open set; domain-specific keys and units are permitted. These quantifications concern generated content, not system resources or call quotas.
  - JSON path: `/body/how_much/{content_length?, structure_elements?, detail_richness?, quality_guidance?, cultural_depth?}`

- **REQ-161 (How-much as unified quantification container)**: This specification does not distinguish between *how much* and *how many* as separate dimensions. All quantity- and resource-related quantifications are consolidated into `how_much`. Implementations MUST normalize synonym fields (e.g. `how_many`) by mapping them to `how_much`.

- **REQ-170 (How-feel)**: SHOULD specify `tone` and `style`; if targeting a specific audience, `audience_level` MUST be drawn from the enumeration.
  - JSON path: `/body/how_feel/{tone?, style?, audience_level?}`

- **REQ-175 (Interface / Governance)**: If the output interface is JSON, the schema MUST appear in at least one of `what.output_schema` or `how_interface.schema`. If it appears only in `what`, the implementor MAY copy it to `how_interface.schema` at runtime for validation.

## 3.2 Partial Specification and Auto-completion

- **REQ-340**: `what.task` is the minimum input a user MUST provide.
- **REQ-341**: The remaining seven dimensions MAY be omitted or partially omitted; implementations fill them using default policies, retrieval results, or inference.
- **REQ-342**: When auto-completion occurs, the system MUST record the completed or overwritten fields in `header.implementation.filled_fields` (as a JSON Pointer array), and MAY annotate the default configuration used in `header.implementation.defaults_profile`; key assumptions MAY be recorded in `header.implementation.assumptions`.
- **REQ-343**: Auto-completion MUST NOT violate governance constraints. For example, injecting a tool without a declared capability is an overreach (see REQ-181); a capability such as `function_call` MAY be added only when compliant and only to satisfy an existing `fn:*` tool call.

---

# 4. Header (Required)

- **REQ-010**: MUST include `pps_version` in the form `PPS-vMAJOR.MINOR.PATCH`.
- **REQ-011**: MUST specify `model.name`, `model.digest`, and `model.data_cutoff`.
- **REQ-012**: MUST specify `decode.seed`, `decode.temperature`, and `decode.top_p`; use `temperature=0` and `top_p=1` for deterministic replay.
- **REQ-013**: MUST specify `locale`; `header.created_at` SHOULD record the creation timestamp.

---

# 5. Body (Required)

- **REQ-020**: MUST contain all eight flat dimensions: `what`, `why`, `who`, `when`, `where`, `how_to_do`, `how_much`, `how_feel`.
- **REQ-021**: `how_to_do`, `how_much`, and `how_feel` are sibling fields; tools are available only when the corresponding capability is declared.
- **REQ-022**: If `where.citations_required=true`, MUST provide at least one `evidence` entry (URI + digest or title).

---

# 6. Integrity (Required)

- **REQ-030**: MUST populate `integrity.canonical_hash`; its value is computed by canonically serializing the Envelope, applying SHA-256, and prefixing with `sha256:`.

---

# 7. Determinism & Replay

- **REQ-040**: MUST fix `model.digest` and `decode` parameters from the Header when replaying.
- **REQ-041**: SHOULD specify `stop` to obtain stable truncation.

## 7.1 Reproducibility

- **REQ-300**: An Envelope MUST be canonicalizable; any change to `body`, `header`, or `integrity` changes the hash.
- **REQ-301**: Evidence reproducibility: when `where.evidence[].uri` points to a mutable resource, SHOULD also provide `digest` and `title` snapshot fields; replay SHOULD prefer locally cached content with a matching digest.
- **REQ-302**: Decode reproducibility: `decode.seed`, `temperature`, and `top_p` MUST be fixed (see REQ-012); `stop` and `top_k` / `beam_width` SHOULD also be recorded where applicable.
- **REQ-303**: Model reproducibility: `model.digest` MUST identify a specific version (model weights, parameters, toolchain).
- **REQ-304**: Implementors MUST document replay steps: canonicalize → validate → policy check → deterministic decode; replay output SHOULD match prior output at the token level, or within a defined tolerance.

## 7.2 Hash Stability

- **REQ-305**: Multiple canonicalizations of the same Envelope MUST produce the same `canonical_hash` (idempotency).
- **REQ-306**: When the canonicalization algorithm changes, `pps_version` MUST be bumped (MAJOR or MINOR).

## 7.3 Canonicalization Algorithm

To ensure cross-platform consistency, implementations SHOULD adopt a minimal implementation compatible with RFC 8785 (JCS — JSON Canonicalization Scheme):

- **Input**: Full Envelope. Temporarily remove `integrity.canonical_hash` before canonicalizing.
- **Strings**: UTF-8 encoding with standard JSON escaping.
- **Objects**: Keys sorted in lexicographic order.
- **Arrays**: Original order preserved.
- **Numbers**: Standard JSON representation (no trailing zeros).
- **Output**: SHA-256 of the canonicalized byte string, prefixed with `sha256:`.
- **Write-back**: Store the result in `integrity.canonical_hash`.

Reference implementation: `tests/pps-conformance/canonicalize.js`

## 7.4 Replay Artefacts

- **REQ-310**: Generating systems SHOULD emit a replay record (timestamp, host, implementation version) to `header.implementation` or an external audit log.

---

# 8. Security & Compliance

- **REQ-050**: If `gdpr` is present in `header.compliance`, MUST explicitly include `no_pii` in `who.policy`.
- **REQ-051**: If `why.constraints` prohibits external browsing, MUST NOT include `web_browse` or any other external network tool.
- **REQ-052**: If `why.constraints` prohibits external browsing and `what.task` contains an `http(s)://` URL, MUST replace or flag it (e.g. `[URL_REMOVED]`) and record the event as a policy violation or auto-fix.
- **REQ-053**: Every tool in `how_to_do.tools` MUST appear in `who.capabilities` (capability sandbox, preventing privilege escalation).

## 8.1 Cross-field Invariants

- **REQ-180**: `where.citations_required=true` ⇒ number of evidence entries ≥ 1.
- **REQ-181**: `how_to_do.tools ⊆ who.capabilities`.
- **REQ-182**: `gdpr ∈ header.compliance` ⇒ `no_pii ∈ who.policy`.
- **REQ-183**: `no_external_browse ∈ why.constraints` ⇒ `web_browse ∉ how_to_do.tools`.

## 8.2 Field Locks and Iterative Refinement

- **REQ-344**: Implementors MAY provide a list of JSON Pointers in `body.how_meta.governance.locks` marking paths as "write-protected"; when regenerating or switching models, the values at those paths MUST remain unchanged.
- **REQ-345**: Implementors SHOULD record the origin of key fields in `header.implementation.origins` (e.g. `user`, `ai:qwen`, `ai:deepseek`) for audit purposes; fields with origin `user` are treated as locked by default unless the user explicitly unlocks them.

## 8.3 AI Compliance Testing and Anchoring

- **REQ-346 (Anchor Priority)**: When user input is present (`origins` contains `user`) or explicit `locks` exist, AI regeneration MUST treat those paths as anchors and MUST NOT overwrite them; completion is permitted only when the value is absent.
- **REQ-347 (Lock Operational Semantics)**:
  - Lock granularity: any JSON Pointer (scalar, object, or array).
  - Priority: `locks` > `origins` > other enhancement policies.
  - Unlock mechanism: a path MAY be overwritten only when the user explicitly removes the pointer or passes `unlock=[...]` via the UI or API.
- **REQ-348 (Consistency Constraint)**: If `why.constraints` prohibits external browsing, `how_to_do.tools` MUST NOT contain `web_browse`; if `where.citations_required=true`, `evidence` MUST be non-empty (consistent with §8.1).
- **REQ-349 (Cross-turn Verification)**: Implementors SHOULD provide a before/after comparison tool verifying that values at `locks`-designated paths remain unchanged; the conformance suite is recommended to include this check.
- **REQ-350 (Failure Handling)**: When a `locks` or consistency constraint is violated, the system MUST roll back to the previous value and record the violation and remediation event (MAY be appended to `header.implementation`).

---

# 9. Conformance

Implementors MUST pass the following tests:
1. JSON Schema validation passes (REQ-001).
2. Policy checks pass (REQ-050/051 etc.).
3. Canonical hash consistency: the same Envelope always produces the same `canonical_hash`.
4. Reproducibility test: same input and decode strategy produces consistent output across platforms (or within defined tolerance).

## 9.1 Human-AI Alignment

- **REQ-320**: `body.what.kpi` SHOULD provide measurable metrics or acceptance criteria (e.g. accuracy ≥ threshold, coverage rate, JSON validation pass rate).
- **REQ-321**: `body.why.goals` and `body.what.kpi` SHOULD be mappable (goal → metric).
- **REQ-322**: If `how_much.quality_guidance` or other measurable criteria are specified, SHOULD also provide a computable `what.output_schema` or external evaluation script so that alignment is verifiable.
- **REQ-323**: `how_meta.governance.verification` SHOULD include `schema_validate` and `policy_check`, and MAY include `self_check` (independent model/rule-based self-verification).

---

# 10. Versioning

- **REQ-060**: `pps_version` follows semantic versioning; v1.0 is backward-compatible with new optional fields added in future v1.x releases.

---

# 11. Interoperability Profile

- **REQ-070**: The minimum subset comprises the required fields of Header + Body + Integrity described above; `how_meta` is optional.

---

# 12. Reference Implementation (Informative)

This specification package does not bundle any scripts. Implementors MAY use the separately published reference implementation and conformance suite for engineering-level validation and benchmarking, which includes examples, validation and canonicalization tools, and CI usage guidance. Refer to the release page for the authoritative link and version number.

---

# Annex A (Informative): Controlled Constraint Vocabulary

| Chinese | English key |
|---------|-------------|
| 禁止外部浏览 | `no_external_browse` |
| 仅使用提供的证据 | `use_provided_evidence` |
| 需要引用 | `citations_required` |
| 禁止个人身份信息 | `no_pii` |

---

# Annex B (Informative): PPS-Content Profile & Strictness Thresholds

This annex provides domain-agnostic thresholds for content creation and task execution, aimed at improving cross-model reproducibility. It does not modify the main specification; it is an optional interoperability profile.

## B.1 Profile Declaration

Declare in `header.compliance`:
- Profile: `pps-content` (or `pps-core`, `pps-analysis`, `pps-code`, `custom`)
- Strictness: `strict` | `balanced` (default) | `permissive`
- Example: `["pps-content", "balanced"]`

## B.2 Structural and Type Requirements (Under This Profile)

- `body.what.task` MUST be a non-empty string.
- `body.who.audience`, if present, MUST be an array.
- `body.how_to_do.steps`, if present, MUST be an array.
- `body.how_much` SHOULD adopt the five quantification elements (compatible with the main spec):
  - `content_length` — length / scale
  - `structure_elements` — structure / sections / modules
  - `detail_richness` — detail / element density
  - `quality_guidance` — quality standards
  - `cultural_depth` — cultural context / depth of engagement

> Note: These field names are recommended practice. Implementations may map equivalents via Schema, but validation must ensure that "quantification elements ≥ N fields are populated."

## B.3 Minimum Thresholds (by Strictness)

| Level | `why.goals` | `who.audience` | `how_to_do.steps` | `how_much` elements |
|-------|:-----------:|:--------------:|:-----------------:|:-------------------:|
| `strict` | ≥ 4 | ≥ 4 | ≥ 6 | 5 / 5 |
| `balanced` (default) | ≥ 3 | ≥ 3 | ≥ 5 | ≥ 3 / 5 |
| `permissive` | ≥ 2 | ≥ 2 | ≥ 4 | ≥ 2 / 5 |

Under `strict`, failure to meet thresholds SHOULD be reported as an error; under `balanced` / `permissive`, as a warning.

---

# Annex C (Informative): Minimal Interoperable Example (balanced)

The following example demonstrates structure and thresholds only; it is not bound to any specific genre or domain.

```json
{
  "header": {
    "pps_version": "PPS-v1.0.0",
    "model": {
      "name": "example-model",
      "digest": "sha256-model-xyz",
      "data_cutoff": "2025-01-01"
    },
    "decode": { "seed": 0, "temperature": 0, "top_p": 1 },
    "locale": "en-US",
    "compliance": ["pps-content", "balanced"],
    "created_at": "2025-10-01T12:00:00Z"
  },
  "body": {
    "what": { "task": "Write a structured introduction to the topic" },
    "why": {
      "goals": [
        "Convey the core concepts",
        "Provide actionable information",
        "Facilitate understanding and application"
      ]
    },
    "who": {
      "persona": "Professional assistant",
      "audience": ["Beginners", "Practitioners", "Decision-makers"]
    },
    "when": { "timeframe": "Current cycle, staged delivery" },
    "where": { "environment": "Online documentation and general work environment" },
    "how_to_do": {
      "paradigm": "CoT",
      "steps": [
        "Identify key points",
        "Organize structure",
        "Draft content",
        "Review and publish",
        "Collect feedback"
      ]
    },
    "how_much": {
      "content_length": "1000–1500 words",
      "structure_elements": "3–4 main sections with headings and summary",
      "detail_richness": "5–8 key points with examples and data where necessary",
      "quality_guidance": "Logical flow, consistent terminology, high readability",
      "cultural_depth": "Moderate references to authoritative or industry context"
    },
    "how_feel": {
      "tone": "Professional and approachable",
      "style": "Clear",
      "audience_level": "intermediate"
    }
  },
  "integrity": {
    "canonical_hash": "sha256:TO_BE_FILLED_AFTER_CANONICALIZATION"
  }
}
```

---

# Annex D (Informative): Validation Checklists

## D.1 Structure and Consistency

- [ ] JSON Schema validation passes (REQ-001)
- [ ] `body.what.task` is non-empty (REQ-100)
- [ ] `who.audience` is an array if present
- [ ] `how_to_do.steps` is an array if present
- [ ] `where.citations_required=true` ⇒ `evidence` ≥ 1 (REQ-180)
- [ ] `how_to_do.tools ⊆ who.capabilities` (REQ-181; semantic matching permitted)
- [ ] Constraint conflict: `no_external_browse` ⇒ `web_browse` not permitted (REQ-183)

## D.2 Quality Thresholds (by Strictness)

- **strict**:
  - [ ] `why.goals` ≥ 4
  - [ ] `who.audience` ≥ 4
  - [ ] `how_to_do.steps` ≥ 6
  - [ ] All five `how_much` elements populated (5/5)
- **balanced** (default): 3 / 3 / 5 / 3
- **permissive**: 2 / 2 / 4 / 2

## D.3 Reproducibility

- [ ] `decode.temperature=0` and `top_p=1` (deterministic, REQ-012)
- [ ] `integrity.canonical_hash` computed and stored (REQ-030 / REQ-300)
- [ ] Model and decode parameters recorded to ensure replay consistency (REQ-040 / REQ-302 / REQ-303)

## D.4 Optional Interface / Output Structure

- [ ] If `how_interface.schema` constrains output shape, its value is an object
- [ ] If schema is provided only in `what.output_schema`, runtime MAY copy it to `how_interface.schema` for validation (REQ-175)

---

# Annex E (Informative): PPS-QR Optional Binding Specification (Binding v1)

This annex defines an optional binding for carrying PPS instructions via QR code, enabling rapid offline or cross-device verification and reuse. It does not modify the main specification; it constrains only the text format and minimum fields of the QR payload to ensure interoperability across implementations.

## E.1 Objectives

- After scanning, a human-readable 5W3H instruction summary can be read directly, together with the information needed for integrity verification.
- No sensitive or private information is included; `integrity.canonical_hash` serves as the sole integrity anchor.

## E.2 Payload (UTF-8 Plain Text)

**MUST include:**
- `pps_version` (from `header.pps_version`)
- `created_at` (from `header.created_at`)
- `task` (from `body.what.task`)
- `canonical_hash` (full value `sha256:…`; if display space is limited, `id_short` MAY be shown but the full hash MUST be retained in the payload)
- `verification_hint` (e.g. "Compare hash to confirm instruction integrity")
- `instruction` (human-readable instruction text organized by 5W3H; show only non-empty dimensions)

**SHOULD include:**
- `id_short`: fixed-length truncation of `canonical_hash` (last 12–16 characters recommended)
- `provider_note`: human-readable note (e.g. "This structured instruction can be reused across AI models")

**MAY include:**
- `signature` / `public_key_id`: if the implementation uses signing
- `retrieval_uri`: optional URI for retrieving the JSON Envelope (verification does not depend on network access)

Recommended text layout:
```
PPS Instruction Certificate
Task: <task>
Created: <created_at>
Instruction ID: <id_short>
Verification: Compare hash to confirm instruction integrity
PPS Version: <pps_version>
Full Hash: <sha256:...>

=== Full Instruction ===

What:        ...
Why:         ...
Who:         ...
When:        ...
Where:       ...
How-to-do:   ...
How-much:    ...
How-feel:    ...

=== Instructions for Use ===
Please complete the task according to the content above.
```

## E.3 Encoding and Error Correction

- Character encoding: UTF-8 plain text.
- Error correction level: L or M; if content is too long, human-readable descriptions MAY be moderately compressed, but 5W3H heading keys MUST NOT be removed.

## E.4 Security and Privacy

- MUST NOT include personally identifiable information, keys, access tokens, or other sensitive data.
- `id_short` is a non-sensitive identifier; strict verification relies on recomputing and comparing `canonical_hash`.

## E.5 Verification Flow (Scanner Side)

1. Read `canonical_hash` and 5W3H instruction.
2. Reconstruct a minimal Envelope from the instruction (or retrieve the JSON Envelope via `retrieval_uri`).
3. Perform canonical serialization (remove `integrity`, sort object keys lexicographically, compact JSON).
4. Compute SHA-256 and compare with `canonical_hash`.
5. Match → verification passed.

## E.6 Versioning

- Binding version: `PPS-QR Binding v1`.
- Adding optional fields to the binding format is backward-compatible with existing implementations; MUST fields remain unchanged.
