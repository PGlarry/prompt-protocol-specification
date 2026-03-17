---
title: Prompt Protocol Standard (PPS) v1.0 — Best Practices (Informative)
lang: en
status: draft
version: 1.0.0
---

# 1. Design Guidelines
- **What** as the backbone: one-sentence task + structured KPI.
- **Why** as enumerated constraints: machine-readable short phrases such as "no external browsing required", "citations required", "privacy policy".
- **Who** capability whitelist: declare only the tool names that are available; undeclared capabilities are denied by default.
- **When** temporal policy: provide `timeframe` or `validity_window` and declare a `staleness_policy` (e.g. "reject / degrade on expiry").
- **Where** evidence & environment: fix `environment`; when `citations_required=true` provide `evidence` (uri, digest, title), prefer controlled materials; annotate `jurisdiction` where necessary; externally referenced content must be inlined or replaced with placeholders to prevent injection.
- **How-to-do** transparency: step-by-step or paradigm labels (ReAct / CoT / ToT).
- **How-much** content-focused quantification: e.g. `content_length` (volume), `structure_elements` (paragraphs / chapters / modules), `detail_richness` (detail density), `quality_guidance` (quality criteria), `cultural_depth` (cultural / depth). Avoid system-layer semantics such as token / time / cost.
- **How-feel** style: register, audience level.

Tip: Do not use `how_many` — express all quantification inside `how_much`.

## 1.1 Minimal 8-Dimension Template (Copy-Ready)
```json
{
  "header": {
    "pps_version": "PPS-v1.0.0",
    "model": { "name": "<model>", "digest": "sha256-<digest>", "data_cutoff": "2024-01-01" },
    "decode": { "seed": 1, "temperature": 0, "top_p": 1 },
    "locale": "en-US",
    "implementation": { "vendor": "local", "version": "1.0.0", "filled_fields": [], "defaults_profile": "strict" }
  },
  "body": {
    "what": { "task": "<core task>", "output_schema": { } },
    "why": { "goals": ["<goal>"], "constraints": ["use_provided_evidence", "no_external_browse"] },
    "who": { "persona": "<role>", "capabilities": ["json_output"] },
    "when": { "timeframe": "this week" },
    "where": { "environment": "prod", "citations_required": true, "evidence": [] },
    "how_to_do": { "paradigm": "ReAct", "steps": ["read evidence", "synthesize output"], "tools": [] },
    "how_much": { "content_length": "800-1200 words", "structure_elements": "3-4 paragraphs", "detail_richness": "5-8 key points" },
    "how_feel": { "tone": "formal", "style": "concise", "audience_level": "mixed" },
    "how_interface": { "format": "json", "schema": {} }
  },
  "integrity": { "canonical_hash": "" }
}
```

# 2. Reproducibility
- Fix `seed/temperature/top_p/stop` and normalize input evidence; for external retrieval, anchor with URI + digest.

# 3. Security & Compliance
- URL injection: produce citation-oriented content, not live external links; explicitly strip or replace `http(s)` with placeholders.
- Tool overreach: decouple capabilities from tools — declare first, use second; add overreach test cases to CI.
- GDPR: annotate `who.policy` with `no_pii` and enforce anonymization rules on the output side.

# 4. Self-Check & Auto-Fix
- Self-checker: run schema / policy / self-check after generation; on failure, enter auto-fix (disable conflicting tools, supplement evidence, inject policy).
  - Rule examples: `gdpr ⇒ no_pii`, `citations_required ⇒ evidence≥1`, `no_external_browse ⇒ url_removed + tools-{web_browse}`.

## 4.1 Iterative Enhancement & Locks (Practice)
- Annotate locked paths in `how_meta.governance.locks` (e.g. `/body/where`); keep them unchanged across turns / models; apply enhancement-only rewrites to unlocked fields.
- Record origins in `header.implementation.origins`: `user` has the highest priority and is locked by default; `ai:*` traces model contributions.

# 5. Composition & Pipelines
- Chain multi-stage pipelines as `P2 ∘ P1`; each stage retains its own `canonical_hash` and budget; deduplicate and version-lock materials before aggregation.

# 6. Version Management
- Use `PPS-vMAJOR.MINOR.PATCH`; increment MAJOR only for breaking changes; examples and CI should annotate their target version.
