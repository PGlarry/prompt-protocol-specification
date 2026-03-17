---
title: PPS v1.0 Controlled Vocabulary Registry
status: draft
version: 1.0.0
---

# 1. 约束（Constraints）
- `no_external_browse` | 禁止外部浏览
- `use_provided_evidence` | 仅使用提供的证据
- `citations_required` | 需要引用
- `no_pii` | 禁止个人身份信息

# 2. 能力（Capabilities）
- `web_browse` | 外部浏览
- `function_call` | 函数调用
- 其它工具名遵循“工具名即能力名”规则

# 3. 范式（Paradigms）
- `ReAct`, `CoT`, `ToT`, `Plan-Execute`, `None`

# 4. 术语规范化（Normalization）
- `how_many` ⇒ 规范化为 `how_much`

# PPS v1.0 词汇与术语建议（非强制）

本文件提供实现者在不同体裁/场景下可复用的“建议词汇”，不改变标准 Schema 的自由度与兼容性。实现可按需选用或自定义，建议与组织内部风格指南对齐。

## how_much（内容量化容器）推荐字段
- 通用类（文本/报告/文章）
  - content_length: 如 "800-1200字", "5-7万字"
  - structure_elements: 如 "3-4段", "10-12章"
  - detail_richness: 如 "每段3-5要点", "含数据与图表"
  - quality_guidance: 如 "术语统一、可复核、引文规范"
  - cultural_depth: 如 "领域背景/标准对照/本地化适配"
- 旅游/指南类
  - poi_count: "50+景点"
  - price_ranges: "门票0-150元", "住宿80-2000元/晚"
  - itinerary_days: "1-5日行程"
- 代码/开发类
  - module_count: "3-5模块"
  - api_count: "2-3个API端点"
  - test_coverage_hint: "示例用例+基本分支覆盖"
- 歌词/诗歌类
  - line_count: "16-24行"
  - stanza_count: "3-4节"
  - rhyme_scheme: "AABB/ABAB"
- 教程/清单类
  - steps_count: "5-8步"
  - checklist_items: "10-15项"

说明：以上仅为示例。how_much 可为字符串或对象；字段名/单位不强制，鼓励领域自定义。


