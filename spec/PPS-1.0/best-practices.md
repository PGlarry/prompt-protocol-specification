---
title: Prompt Protocol Standard (PPS) v1.0 — Best Practices (Informative)
status: draft
version: 1.0.0
---

# 1. 设计指南
- What 作为主干：任务一句话 + 结构化 KPI。
- Why 约束枚举化：禁止外部浏览、需引用、隐私策略等可机读短语。
- Who 能力白名单：仅声明可用工具名，默认拒绝未声明能力。
- When 时效策略：提供 `timeframe` 或 `validity_window`，并声明 `staleness_policy`（如“过期拒绝/降级处理”）。
- Where 证据与环境：固定 `environment`；`citations_required=true` 时提供 `evidence`（uri、digest、title），优先受控素材；必要时标注 `jurisdiction`；外链内容需文本化或占位符处理以避免注入。
- How-to-do 透明：步骤式或范式标签（ReAct/CoT/ToT）。
- How-much 面向“内容本身”的量化：例如 `content_length`（篇幅）、`structure_elements`（结构/段落/模块）、`detail_richness`（细节密度）、`quality_guidance`（质量指引）、`cultural_depth`（文化/深度）。避免系统层面的 token/time/cost 语义。
- How-feel 风格：语域、受众层级。

提示：不使用 `how_many`，统一在 `how_much` 中表达所有量化维度。

## 1.1 最小 8 维模板（可拷贝）
```json
{
  "header": {
    "pps_version": "PPS-v1.0.0",
    "model": { "name": "<model>", "digest": "sha256-<digest>", "data_cutoff": "2024-01-01" },
    "decode": { "seed": 1, "temperature": 0, "top_p": 1 },
    "locale": "zh-CN",
    "implementation": { "vendor": "local", "version": "1.0.0", "filled_fields": [], "defaults_profile": "strict" }
  },
  "body": {
    "what": { "task": "<核心任务>", "output_schema": { } },
    "why": { "goals": ["<目标>"], "constraints": ["use_provided_evidence", "no_external_browse"] },
    "who": { "persona": "<角色>", "capabilities": ["json_output"] },
    "when": { "timeframe": "本周" },
    "where": { "environment": "prod", "citations_required": true, "evidence": [] },
    "how_to_do": { "paradigm": "ReAct", "steps": ["读取证据", "综合输出"], "tools": [] },
    "how_much": { "content_length": "800-1200字", "structure_elements": "3-4段", "detail_richness": "5-8要点" },
    "how_feel": { "tone": "正式", "style": "简洁", "audience_level": "mixed" },
    "how_interface": { "format": "json", "schema": {} }
  },
  "integrity": { "canonical_hash": "" }
}
```

# 2. 可复现性
- 固定 `seed/temperature/top_p/stop`，并将输入证据规范化；对外部检索应以 URI+摘要方式固定。

# 3. 安全与合规
- URL 注入：输出面向引用的内容，而非执行外链；对 `http(s)` 进行显式剥离或替换为占位符。
- 工具越权：能力与工具解耦，先声明后使用；CI 中加入越权用例。
- GDPR：在 `who.policy` 标注 `no_pii`，并在产出侧执行脱敏规则。

# 4. 自检与修复
- 自检器：在生成后运行 schema/policy/self-check；失败则进入 auto-fix（禁用冲突工具、补证据、注入 policy）。
  - 规则示例：`gdpr ⇒ no_pii`、`citations_required ⇒ evidence≥1`、`no_external_browse ⇒ url_removed + tools-\n{web_browse}`。

## 4.1 迭代增强与锁（实践）
- 在 `how_meta.governance.locks` 标注锁定路径（如 `/body/where`）；跨轮次/跨模型保持不变，仅对未锁字段做增强式改写。
- 在 `header.implementation.origins` 记录来源：`user` 优先级最高且默认锁定；`ai:*` 用于追溯模型贡献。

# 5. 组合与管道
- 多阶段时以 `P2 ∘ P1` 串联；每阶段保留各自 `canonical_hash` 与预算；在聚合物料前做去重与版本锁定。

# 6. 版本管理
- 采用 `PPS-vMAJOR.MINOR.PATCH`；仅在破坏性变更时提升 MAJOR；示例与 CI 应标注适配版本。



