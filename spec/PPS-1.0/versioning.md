---
title: PPS Versioning & Compatibility Policy
status: draft
---

# 1. 语义化版本
- 采用 `MAJOR.MINOR.PATCH`，协议版本以 `PPS-vMAJOR.MINOR.PATCH` 标记于 `header.pps_version`。

# 2. 兼容策略
- 1.0.x 系列：新增字段保持可选，后向兼容。
- MAJOR 升级仅在破坏性变更时发生（字段删除/语义改变）。

# 3. 迁移
- 从 1.0 升级至 1.x：示例与 CI 标注目标版本；若新增策略条款，可通过 `policy_checks` 升级规则检测。


