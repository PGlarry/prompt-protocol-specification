# PPS v1.0 — Community Specification Status

This repository publishes PPS (Prompt Protocol Specification) as a community, patent‑free specification aiming for broad interoperability and adoption.

## Current phase
- Phase: Community Specification (v1.0.0)
- Goals (0–12 months):
  - 3+ production adoptions
  - Reference conformance suite stabilized (schema/policy/locks/hash)
  - Minor releases for clarifications (v1.0.x)

## Roadmap (indicative)
- 12–24 months (Industry adoption):
  - 10+ organizations adopt PPS
  - Reference SDKs (Python/JS) for envelope build/validate/hash
  - Whitepaper and public talks
- 24–36 months (Standards track, optional):
  - Explore W3C CG→WG, or IETF Internet‑Draft (with RF/RAND‑Z commitments as required)

## Governance
- Source of truth: this repository (tags/releases)
- Changes: PR + review; semver versioning; normative changes require a minor/major bump

## IP & Openness
- PPS and the 5W3H framework are fully open and patent-free (no patents filed or claimed) — like TCP/IP, anyone can freely implement and commercialize without any patent license
- Software copyright on the creative expression of this specification is held by Gang Peng (CC BY 4.0 / MIT); see `spec/PPS-1.0/IP_NOTICE.md`
- Code under MIT; docs under CC BY 4.0

## Conformance quick links
- Summary: `node tests/pps-conformance/summary.js`
- Locks compliance: `node tests/pps-conformance/locks_compliance.js before.json after.json`
- Canonical hash: `node tests/pps-conformance/canonicalize.js compute <file>`
