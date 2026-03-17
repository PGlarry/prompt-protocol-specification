---
title: PPS Versioning & Compatibility Policy
lang: en
status: draft
---

# 1. Semantic Versioning
- Uses `MAJOR.MINOR.PATCH`; protocol version is tagged as `PPS-vMAJOR.MINOR.PATCH` in `header.pps_version`.

# 2. Compatibility Policy
- 1.0.x series: new fields remain optional and are backwards-compatible.
- MAJOR is incremented only for breaking changes (field removal or semantic change).

# 3. Migration
- Upgrading from 1.0 to 1.x: tag examples and CI with the target version; if new policy clauses are added, they can be detected via `policy_checks` rule upgrades.
