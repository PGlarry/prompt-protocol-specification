---
title: PPS v1.0 Conformance & Test Specification
status: draft
version: 1.0.0
---

# 1. 范围
定义 PPS v1.0 的最小合规测试：Schema 校验、策略检查、可复现性与哈希一致性。输出用于人工审阅与 CI。

# 2. 必须通过的校验项
1) JSON Schema（REQ-001）: `spec/pps-1.0.schema.json`
2) 策略检查（REQ-050/051/052/053, 180..183, 320..323）
3) 规范化哈希一致性（REQ-300）
4) 解码确定性（REQ-012/302）与跨平台重放（容差内）

# 3. 工具与命令
- 规范化/哈希: `node tests/pps-conformance/canonicalize.js <file> --write`
- Schema 校验: `node tests/pps-conformance/validate.js <file>`
- 策略检查: `node tests/pps-conformance/policy_checks.js <file> --json`
- 自动修复: `node tests/pps-conformance/auto_fix.js <file> --write`

# 4. 输出格式（建议）
策略检查 `--json`：
```json
{ "pass": true, "warnings": [], "issues": [{ "type": "tool_capability_missing", "message": "..." }] }
```

# 5. CI 集成（建议）
在 CI 中对 `spec/examples/*.json` 逐一执行：规范化→Schema→策略→（必要时）自动修复→汇总。失败即阻断。


