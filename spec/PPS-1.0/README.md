# PPS v1.0 规范包（Specification）· 快速导读

本目录提供对外公开的 PPS（Prompt Protocol Standard）v1.0 规范性材料，帮助实现者在最短时间内理解与落地。

## 1. 我们解决什么问题
- 复现性：固定模型指纹与解码策略、对输入证据做规范化与哈希，支持可重放与审计。
- 人机对齐：把目标、约束与可度量 KPI 显式化，提供可验证的质量阈值与自检挂钩。
- 治理与安全：能力沙箱、接口白名单与交叉一致性，抑制注入/越权/引用缺失等问题。
- 可组合与迭代：8 维结构化描述，支持部分规范（仅 What 必填）与跨模型的增强式再生成。

## 2. 最小实现（必须）
1) 使用 `spec/pps-1.0.schema.json` 序列化一次提示交互（Envelope）。
2) What 必填，其余 7 维可选；如自动补全，需记录来源（见 2.3）。
3) 在 Header 中固定：`model.digest`、`decode.seed/temperature/top_p`；生成 `integrity.canonical_hash`（规范化哈希）。
4) 满足交叉一致性（工具越权、GDPR、引用、禁外链）。

### 2.1 8 维到 JSON 路径映射
- What：`/body/what/{task,input_schema?,output_schema?,kpi?[]}`
- Why：`/body/why/{goals?[],constraints?[]}`
- Who：`/body/who/{persona?,audience?[],roles?[],capabilities?[],policy?[]}`
- When：`/body/when/{timeframe?,validity_window?,staleness_policy?}`
- Where：`/body/where/{environment?,evidence?[],jurisdiction?[],citations_required?}`
- How‑to‑do：`/body/how_to_do/{paradigm?,steps?[],tools?[]}`
- How‑much（量化表达容器，与其他维度平级）：`/body/how_much/{<开放键名>}`（字段名开放，示例见附录与 registry）
- How‑feel：`/body/how_feel/{tone?,style?,audience_level?}`

提示：本规范不区分 how much/how many，所有量化统一归入 `how_much`。

### 2.2 交叉一致性（片段）
- `how_to_do.tools ⊆ who.capabilities`
- `gdpr ∈ header.compliance ⇒ no_pii ∈ who.policy`
- `where.citations_required=true ⇒ evidence 非空`
- `no_external_browse ∈ why.constraints ⇒ web_browse 不得出现`

### 2.3 迭代增强（可选但建议）
- 锁：`/body/how_meta/governance/locks`（JSON Pointer 列表）指示“禁止改写”的路径（如 `/body/where`）。
- 来源：`/header/implementation/origins` 记录关键字段来源 `user|ai:<vendor>`；来源为 `user` 默认为锁定。

## 3. 合格判据（Conformance）
- Schema：通过 `spec/pps-1.0.schema.json` 校验。
- Policy：无阻断项（越权、GDPR、引用、禁外链等）。
- 哈希：规范化后 `integrity.canonical_hash` 重算一致。
- 重放：在固定模型与解码下，输出与先前一致或在约定容差内一致。

详情见 `conformance.md`（仅描述通过条件与输出格式，不含脚本）。

## 4. 文件清单（本标准包）
- `standard.md`：规范性要求（含 REQ 编号、8 维映射、锁与迭代、交叉一致性）
- `registry.md`：受控词汇（约束/能力/范式）与术语规范化
- `security-privacy.md`：威胁模型、保障机制作说明
- `versioning.md`：版本与兼容策略
- `conformance.md`：合格判据与输出格式
- `../pps.schema.json`：基础 Schema
- `../pps-1.0.schema.json`：v1.0 版本化 Schema（继承基础 Schema）

## 5. 最小示例（示意）
```json
{
  "header": {
    "pps_version": "PPS-v1.0.0",
    "model": { "name": "<model>", "digest": "sha256-<digest>", "data_cutoff": "2024-01-01" },
    "decode": { "seed": 1, "temperature": 0, "top_p": 1 },
    "locale": "zh-CN"
  },
  "body": {
    "what": { "task": "<核心任务>", "output_schema": {} },
    "how_to_do": { "paradigm": "ReAct" },
    "how_much": { "content_length": "800-1200字" },
    "how_feel": { "tone": "正式" }
  },
  "integrity": { "canonical_hash": "" }
}
```

> 完整用法请参考 `standard.md`；演示用例可放在独立的“参考实现/符合性套件”仓库中发布。

---
若需引用：请使用发布页面的版本号（如 v1.0.0）与仓库/DOI 链接。

## 6. 快速校验（一键命令）

在仓库根目录执行（需 Node 18+）：

```bash
# 汇总校验（Schema / Policy / Locks）
node tests/pps-conformance/summary.js

# 单例校验
node tests/pps-conformance/validate.js spec/examples/minimal.json
node tests/pps-conformance/policy_checks.js spec/examples/minimal.json --json
node tests/pps-conformance/canonicalize.js compute spec/examples/minimal.json
node tests/pps-conformance/locks_compliance.js \
  spec/examples/mixed_adversarial.json \
  spec/examples/mixed_adversarial.after.json --json
```

## 7. Expected‑Fail 用例（解释性）

- `mixed_adversarial.json`：禁外链但含 URL、能力与工具不匹配等 → Policy/Locks 预期 FAIL
- `prompt_injection_url.json`：禁外链但任务含 URL → Policy 预期 FAIL
- `tool_overreach.json`：工具越权（未在 `who.capabilities` 声明）→ Policy 预期 FAIL
- `json_interface_missing_schema.json`：`how_interface.format=json` 但缺 schema → Policy 预期 FAIL

上述用例用于验证策略与锁一致性，非实现错误。
