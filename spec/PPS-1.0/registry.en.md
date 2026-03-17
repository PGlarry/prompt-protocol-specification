---
title: PPS v1.0 Controlled Vocabulary Registry
lang: en
status: draft
version: 1.0.0
---

# 1. Constraints
- `no_external_browse` | Prohibit external browsing
- `use_provided_evidence` | Use only provided evidence
- `citations_required` | Citations required
- `no_pii` | Prohibit personally identifiable information

# 2. Capabilities
- `web_browse` | External browsing
- `function_call` | Function call
- Other tool names follow the "tool name = capability name" rule

# 3. Paradigms
- `ReAct`, `CoT`, `ToT`, `Plan-Execute`, `None`

# 4. Term Normalization
- `how_many` ⇒ normalize to `how_much`

# PPS v1.0 Recommended Vocabulary (Non-normative)

This document provides suggested vocabulary that implementers can reuse across different genres and scenarios. It does not change the freedom or compatibility of the standard Schema. Implementations may adopt or customize as needed; alignment with internal style guides is recommended.

## how_much (Content Quantification Container) — Recommended Fields
- General (text / reports / articles)
  - content_length: e.g. "800–1200 words", "50,000–70,000 words"
  - structure_elements: e.g. "3–4 paragraphs", "10–12 chapters"
  - detail_richness: e.g. "3–5 key points per paragraph", "include data and charts"
  - quality_guidance: e.g. "consistent terminology, verifiable, citation standards"
  - cultural_depth: e.g. "domain background / standards comparison / localization"
- Travel / Guide
  - poi_count: "50+ attractions"
  - price_ranges: "tickets ¥0–150", "accommodation ¥80–2000/night"
  - itinerary_days: "1–5 day itinerary"
- Code / Development
  - module_count: "3–5 modules"
  - api_count: "2–3 API endpoints"
  - test_coverage_hint: "sample test cases + basic branch coverage"
- Lyrics / Poetry
  - line_count: "16–24 lines"
  - stanza_count: "3–4 stanzas"
  - rhyme_scheme: "AABB / ABAB"
- Tutorial / Checklist
  - steps_count: "5–8 steps"
  - checklist_items: "10–15 items"

Note: The above are examples only. `how_much` may be a string or an object; field names and units are not mandated — domain-specific customization is encouraged.
