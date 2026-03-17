# PPS — Prompt Protocol Specification

<div align="center">

**[English](README.md) · [中文](README.zh.md) · [日本語](README.ja.md)**

[![License: MIT](https://img.shields.io/badge/Tools-MIT-blue.svg)](LICENSE)
[![Docs: CC BY 4.0](https://img.shields.io/badge/Docs-CC%20BY%204.0-green.svg)](spec/PPS-1.0/IP_NOTICE.md)
[![Version](https://img.shields.io/badge/PPS-v1.0.0-orange.svg)](spec/PPS-1.0/standard.md)
[![Status](https://img.shields.io/badge/Status-Community%20Specification-brightgreen.svg)](STATUS.md)

*An open 8-dimension structured instruction framework for Human-AI Interaction*

</div>

---

## What is PPS?

Natural language prompts suffer from **intent transmission loss** — the gap between what users actually need and what they communicate to AI systems. PPS (Prompt Protocol Specification) solves this by providing a structured, machine-verifiable envelope for AI instructions.

PPS is built on the **5W3H model**: *What, Why, Who, When, Where, How-to-do, How-much, How-feel* — eight dimensions that fully specify any AI task.

```json
{
  "pps_header": {
    "pps_version": "PPS-v1.0.0",
    "model": { "name": "gpt-4o", "digest": "sha256:abc123", "data_cutoff": "2025-01-01" },
    "decode": { "seed": 42, "temperature": 0.7, "top_p": 0.95 },
    "locale": "en-US"
  },
  "pps_body": {
    "what": { "task": "Write a competitive analysis of the EV market in China" },
    "why": { "goals": ["support strategic investment decision"], "constraints": ["no_pii"] },
    "who": { "persona": "senior industry analyst", "audience": ["C-suite executives"] },
    "when": { "timeframe": "2024 data, current market snapshot" },
    "where": { "environment": "board presentation", "jurisdiction": "CN" },
    "how_to_do": { "paradigm": "CoT", "steps": ["market sizing", "Porter's Five Forces", "top 5 players", "trend projection"] },
    "how_much": { "content_length": "2000 words", "structure_elements": "5 sections with tables", "detail_richness": "10+ data points" },
    "how_feel": { "tone": "professional", "style": "data-driven", "audience_level": "expert" }
  },
  "pps_integrity": {
    "canonical_hash": "sha256:TO_BE_FILLED_AFTER_CANONICALIZATION"
  }
}
```

---

## Why PPS?

Empirical results from a controlled experiment (60 topics × 3 LLMs × 3 conditions, 540 outputs):

| Metric | Simple Prompt (A) | PPS Rendered (C) | Improvement |
|--------|:-----------------:|:----------------:|:-----------:|
| **goal_alignment** | 4.34 | **4.61** | *p* = 0.006, *d* = 0.374 |
| Follow-up prompts needed | ~3.3 rounds | ~1.1 rounds | **−66%** |
| First-impression accuracy | — | **85%** accurate on first expansion | — |

> Full methodology and results: [Paper (arXiv)](https://arxiv.org/abs/PENDING) · [Experiment data](experiments/)

**Key insight**: Traditional LLM evaluation metrics show A > C due to *constraint scoring asymmetry* — prompts without constraints trivially score perfect. When evaluated on user-intent alignment (`goal_alignment`), structured PPS prompts significantly outperform simple prompts, especially in high-ambiguity domains (business: *d* = 0.895).

---

## Repository Structure

```
prompt-protocol-specification/
├── spec/
│   └── PPS-1.0/
│       ├── standard.md          # Normative specification (Chinese)
│       ├── standard.en.md       # Normative specification (English)  [coming]
│       ├── best-practices.md    # Implementation guidance
│       ├── conformance.md       # Conformance levels
│       ├── security-privacy.md  # Security & GDPR requirements
│       ├── versioning.md        # Version policy
│       ├── benchmark.md         # Benchmark methodology
│       ├── registry.md          # Controlled vocabulary
│       └── IP_NOTICE.md         # Patent & IP notice
├── schema/
│   ├── pps-1.0.schema.json      # JSON Schema (strict)
│   └── pps.schema.json          # JSON Schema (base)
├── spec/examples/               # Annotated example envelopes
├── tests/pps-conformance/       # Conformance test suite (Node.js)
├── tools/
│   └── pps-verify.js            # CLI verification tool
├── STATUS.md                    # Specification roadmap & governance
└── PUBLISHING.md                # Release & DOI guide
```

---

## Quick Start

**Validate an envelope:**
```bash
node tests/pps-conformance/validate.js spec/examples/minimal.json
```

**Run all conformance checks:**
```bash
node tests/pps-conformance/summary.js
```

**Compute canonical hash:**
```bash
node tools/pps-verify.js spec/examples/minimal.json
```

**Requirements:** Node.js ≥ 16

---

## Conformance Profiles

PPS defines three conformance levels declared in `header.compliance`:

| Profile | `why.goals` | `who.audience` | `how_to_do.steps` | `how_much` fields |
|---------|:-----------:|:--------------:|:-----------------:|:-----------------:|
| `strict` | ≥ 4 | ≥ 4 | ≥ 6 | ≥ 3 |
| `balanced` | ≥ 3 | ≥ 3 | ≥ 5 | ≥ 2 |
| `permissive` | ≥ 2 | ≥ 2 | ≥ 4 | ≥ 1 |

---

## Citation

If you use PPS in academic work, please cite:

```bibtex
@article{peng2026pps,
  title     = {PPS: Structured Intent Transmission — An Empirical Study of a
               5W3H-Based Prompt Protocol for Human-AI Interaction},
  author    = {Peng, Gang},
  year      = {2026},
  note      = {arXiv preprint, cs.HC},
  url       = {https://github.com/PGlarry/prompt-protocol-specification}
}
```

---

## Related

- **5W3H Platform**: [https://www.lateni.com](https://www.lateni.com) — live implementation
- **Book**: *Super Prompt: 5W3H* (Amazon KDP, April 2025) — practitioner guide

---

## License

- **Specification documents** (`spec/`): [CC BY 4.0](spec/PPS-1.0/IP_NOTICE.md) — free to use, share, adapt with attribution
- **Tools & tests** (`tools/`, `tests/`): [MIT](LICENSE)
- **Patent notice**: The PPS specification is patent-free. See [IP_NOTICE.md](spec/PPS-1.0/IP_NOTICE.md) for details.

---

<div align="center">
<sub>Created by <a href="https://www.lateni.com">Gang Peng</a> · Huizhou University · Huizhou Lateni AI Technology Co., Ltd.</sub>
</div>
