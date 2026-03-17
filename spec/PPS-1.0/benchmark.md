---
title: PPS v1.0 Benchmark & Metrics (Informative)
status: draft
version: 1.0.0
---

# 1. 目标
量化协议层能力：可复现性、治理有效性与资源显式度。

# 2. 指标
- Policy 捕获率 = FAIL 数 / 总用例数（按类型细分：注入、越权、引用、GDPR、预算）
- Auto-fix 成功率 = 修复后 PASS 数 / 触发 auto-fix 的用例数
- 重放一致率 = 多平台重放一致的比例（或容差内）
- 资源预算显式率 = 存在 `how_much` 预算字段的用例比例

## 2.1 部分规范/自由组合消融
- 输入设定：仅提供 `what.task`；对其余 7 维随机选择子集由系统补全（遵循 REQ-341..343）。
- 评测项：
  - 合规保持率：补全后仍满足交叉一致性（REQ-180..183）的比例
  - 对齐稳健度：KPI 达标率随提供维度数量的曲线（0..7）
  - 预算偏差：补全产生的资源预算与目标配置的偏差分布

# 3. 数据来源
- `tests/pps-conformance/policy_checks.js --json` 的 `issues[].type`
- `auto_fix.js` 的 `fixesApplied`（后续脚本导出）
- `summary.js` 聚合生成 `summary.csv` 与 `benchmark.json`


