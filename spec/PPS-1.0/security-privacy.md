---
title: PPS v1.0 Security & Privacy (Threat Model)
status: draft
version: 1.0.0
---

# 1. 威胁模型
- 注入（prompt/URL/证据污染）
- 越权（未声明工具或外部通道）
- 合规风险（PII、未引用、跨辖区限制）

# 2. 保障机制（规范性关联）
- 接口白名单与能力沙箱：`how_to_do.tools ⊆ who.capabilities`（REQ-181）
- 非浏览约束：`no_external_browse` ⇒ 禁用 `web_browse` 与 URL 移除（REQ-052/183）
- 引用一致性：`citations_required` ⇒ `evidence` 非空（REQ-180）
- GDPR：`gdpr` ⇒ `no_pii`（REQ-182）
- 因果非干扰：未授权输入不改变授权输出分布（论文主文与规范对应）

# 3. 残余风险与边界
- 第三方模型/检索源不可控更新导致轻微漂移（由确定性解码与证据快照缓解）
- 人工标注或外部评分的主观性（以 KPI 与 schema 验证减轻）


