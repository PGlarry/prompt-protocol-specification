---
title: Prompt Protocol Specification (PPS) v1.0 — Normative Specification
status: community-specification
version: 1.0.0
lang: zh
---

**语言 / Language / 言語 / 언어 / Idioma**：[中文](standard.md) · [English](standard.en.md) · [日本語](standard.ja.md) · [한국어](standard.ko.md) · [Español](standard.es.md)

---

## 目录（Table of Contents）

| 章节 | 内容 |
|------|------|
| [§1](#1-范围scope) | 范围 |
| [§2](#2-术语terms) | 术语 |
| [§3](#3-数据模型normative-schema) | 数据模型（8维度） |
| [§4](#4-header必需) | Header |
| [§5](#5-body必需) | Body |
| [§6](#6-integrity必需) | Integrity |
| [§7](#7-解码与重放determinism) | 解码与重放 |
| [§8](#8-安全与合规security--compliance) | 安全与合规 |
| [§9](#9-符合性conformance) | 符合性 |
| [§10](#10-版本与兼容versioning) | 版本与兼容 |
| [§11](#11-互操作最小子集interoperability-profile) | 互操作最小子集 |
| [§12](#12-参考实现与符合性套件informative) | 参考实现 |
| [附录A](#附录-ainformative受控约束词汇) | 受控约束词汇 |
| [附录B](#附录-binformativepps-content-profile-与严格度门槛) | 符合性门槛 |
| [附录C](#附录-cinformative最小可互操作样例) | 最小示例 |
| [附录D](#附录-dinformative校验清单) | 校验清单 |
| [附录E](#附录-einformativepps-qr-可选绑定规范) | PPS-QR 绑定 |

---

# 1. 范围（Scope）
本规范定义人机交互提示协议 PPS 的最小可互操作实现。规范性条款以 MUST/SHOULD/MAY 表示，带有 REQ 编号。

# 2. 术语（Terms）
- Envelope：一次交互的协议载体。
- Canonicalization：对 JSON 进行确定化排序与序列化。
- Deterministic Decoding：解码参数固定使重放可复现。

# 3. 数据模型（Normative Schema）
实现者 MUST 接受并生成符合 `spec/pps-1.0.schema.json` 的 Envelope（REQ-001）。

# 3.1 8 维度与 JSON 路径（Normative Mapping）
- REQ-100 (What): MUST 提供 `body.what.task`；若输出为结构化 JSON，SHOULD 提供 `body.what.output_schema`。
  - JSON 路径：`/body/what/{task, input_schema?, output_schema?}`
- REQ-110 (Why): SHOULD 列出 `body.why.goals`；约束 SHOULD 来自受控词汇（附录 A），如 `no_external_browse`, `citations_required`, `use_provided_evidence`。
  - JSON 路径：`/body/why/{goals?, constraints?}`
- REQ-120 (Who): SHOULD 指定 `persona`；若将使用工具，MUST 在 `who.capabilities` 白名单中声明。
  - JSON 路径：`/body/who/{persona?, capabilities?, policy?}`
- REQ-130 (When): MUST 至少给出 `timeframe` 或 `validity_window` 之一。
  - JSON 路径：`/body/when/{timeframe?, validity_window?, staleness_policy?}`
- REQ-140 (Where): 若 `citations_required=true`，MUST 至少 1 条 `evidence`；证据 SHOULD 含 `digest` 与 `title`。
  - JSON 路径：`/body/where/{environment?, evidence[], jurisdiction?, citations_required?}`
- REQ-150 (How-to-do): SHOULD 指定 `paradigm` 与 `steps`；使用的 `tools` MUST 满足 REQ-181（能力约束）。
  - JSON 路径：`/body/how_to_do/{paradigm?, steps?, tools?}`
- REQ-160 (How-much): SHOULD 明确面向“内容本身”的量化要素（例如篇幅、结构、细节密度、质量指引、文化/深度等）。实现者可使用字段如 `content_length`、`structure_elements`、`detail_richness`、`quality_guidance`、`cultural_depth`，或自定义等价表述；这些量化均针对“生成内容”，与系统资源/调用配额无关。
  - JSON 路径：`/body/how_much/{content_length?, structure_elements?, detail_richness?, quality_guidance?, cultural_depth?}`
- REQ-161 (How-much 单一量化容器): 本规范不区分英语习惯的 how much/how many，所有数量与资源相关的量化维度均归入 `how_much`；如出现同义字段（如 `how_many`），实现者 MUST 将其规范化映射为 `how_much`。
- REQ-170 (How-feel): SHOULD 指定 `tone/style`；若面向特定人群，`audience_level` MUST 取自枚举。
  - JSON 路径：`/body/how_feel/{tone?, style?, audience_level?}`
- REQ-175 (Interface/Governance): 若输出接口为 JSON，MUST 在 `what.output_schema` 或 `how_interface.schema` 至少出现一处；若仅出现于 `what`，实现者 MAY 在运行时复制至 `how_interface.schema` 用于验证。

# 3.2 部分规范与自动补全（Partial Spec & Auto-completion）
- REQ-340: `what.task` 为用户必须提供的最小输入（MUST）。
- REQ-341: 其余 7 个维度 MAY 省略或部分省略，由实现根据默认策略/检索结果/推理进行补全。
- REQ-342: 一旦发生自动补全，系统 MUST 在 `header.implementation.filled_fields`（JSON Pointer 数组）记录被补全/改写的字段，并可在 `header.implementation.defaults_profile` 标注所用默认配置；可选 `header.implementation.assumptions` 记录关键假设。
- REQ-343: 自动补全不得违反治理约束：例如在未声明能力时补入工具属于越权（见 REQ-181）；仅允许在合规的前提下添加如 `function_call` 的能力以满足已存在的 `fn:*` 工具调用（与参考实现一致）。

# 4. Header（必需）
- REQ-010: MUST 包含 `pps_version`，形如 `PPS-vMAJOR.MINOR.PATCH`。
- REQ-011: MUST 指定 `model` 的 `name`、`digest`、`data_cutoff`。
- REQ-012: MUST 指定 `decode.seed/temperature/top_p`，其中 `temperature=0` 与 `top_p=1` 用于确定性重放。
- REQ-013: MUST 指定 `locale`。

# 5. Body（必需）
- REQ-020: MUST 包含 `what/why/who/when/where/how_to_do/how_much/how_feel` 八个域（扁平）。
- REQ-021: `how_to_do`/`how_much`/`how_feel` 为并列字段；工具仅在具备相应能力时可用。
- REQ-022: 若 `where.citations_required=true`，MUST 提供至少一条 `evidence`（URI + 摘要或标题）。

# 6. Integrity（必需）
- REQ-030: MUST 填充 `integrity.canonical_hash`，其值由规范化序列化后以 SHA-256 计算并以 `sha256:` 前缀表示。

# 7. 解码与重放（Determinism）
- REQ-040: MUST 在重放时固定 Header 中的 `model.digest` 与 `decode` 参数。
- REQ-041: SHOULD 指定 `stop` 以获得稳定截断。

# 7.1 可复现性（Reproducibility）
- REQ-300: Envelope MUST 可被规范化（canonicalization），并据此计算 `integrity.canonical_hash`；任何对 `body`/`header`/`integrity` 的更改都会改变哈希。
- REQ-301: 证据可复现：当 `where.evidence[].uri` 指向可变资源时，SHOULD 同时提供 `digest` 与 `title` 的快照字段；重放时优先使用带 `digest` 的本地/缓存内容。
- REQ-302: 解码可复现：`decode.seed/temperature/top_p` MUST 固定（见 REQ-012），并建议记录 `stop` 与 `top_k/beam_width`（如适用）。
- REQ-303: 模型可复现：`model.digest` MUST 标识具体版本（模型/参数/工具链）。
- REQ-304: 实现者 MUST 提供重放步骤：规范化 → 验证 → 策略检查 → 确定性解码；重放结果应与先前产出在 token 级别一致或在容差范围内一致。

# 7.2 自证据（Replay Artefacts）
- REQ-310: 生成系统 SHOULD 输出重放记录（时间、主机、实现版本）到 `header.implementation` 或外部日志，以满足审计需求。

# 8. 安全与合规（Security & Compliance）
- REQ-050: 若 Header `compliance` 包含 `gdpr`，MUST 在 `who.policy` 明示 `no_pii`。
- REQ-051: 若 `why.constraints` 禁止外部浏览，MUST 不包含 `web_browse` 等外部联网工具。
- REQ-052: 若 `why.constraints` 禁止外部浏览且 `what.task` 含 `http(s)://` URL，MUST 进行替换或标记（如 `[URL_REMOVED]`），并将该情况记录为策略违规或已修复。
- REQ-053: `how_to_do.tools` 中的每个工具 MUST 出现在 `who.capabilities`（能力沙箱，防越权）。

# 8.1 交叉一致性（Cross-field Invariants）
- REQ-180: `where.citations_required=true` ⇒ 证据条目数 ≥ 1。
- REQ-181: `how_to_do.tools ⊆ who.capabilities`。
- REQ-182: `gdpr ∈ header.compliance` ⇒ `no_pii ∈ who.policy`。
- REQ-183: `no_external_browse ∈ why.constraints` ⇒ `web_browse ∉ how_to_do.tools`。

# 8.2 字段锁与迭代增强（Locks & Iterative Refinement）
- REQ-344: 实现者 MAY 在 `body.how_meta.governance.locks` 提供 JSON Pointer 列表，标记为“禁止改写”的路径；当进行再生成/跨模型切换时，这些路径的值 MUST 保持不变。
- REQ-345: 实现者 SHOULD 在 `header.implementation.origins` 记录关键字段的来源（如 `user`、`ai:qwen`、`ai:deepseek`）以便审计；当来源为 `user` 时，系统默认视为锁定，除非用户显式解锁。

## 8.3 AI 遵守性测试与保障机制（Anchoring & Compliance）
- REQ-346（锚点优先级）：当存在用户输入（`origins` 包含 `user`）或显式 `locks` 时，AI 再生成 MUST 以这些路径值为锚点，不得覆盖；缺少值时方可补全。
- REQ-347（锁的操作语义）：
  - 锁定粒度：任意 JSON Pointer（指向标量/对象/数组均可）。
  - 优先级：`locks` > `origins` > 其它增强策略。
  - 解锁机制：仅当用户显式移除该指针或在 UI/API 中传入 `unlock=[...]` 时方可改写。
- REQ-348（一致性约束）：`why.constraints` 若禁止外部浏览，则 `how_to_do.tools` MUST 不含 `web_browse`；若 `where.citations_required=true`，`evidence` MUST 非空（与 8.1 保持一致）。
- REQ-349（跨轮检验）：实现者 SHOULD 提供“前/后对比”工具，校验 `locks` 指向路径的值保持不变；推荐扩展合格套件以执行该校验。
- REQ-350（失败处置）：当违反 `locks` 或一致性约束时，系统 MUST 回退到“上一版本值”，并记录违规与修复事件（可在 `header.implementation` 中追加记录）。

# 9. 符合性（Conformance）
- 实现者 MUST 通过以下测试：
  1) JSON Schema 校验通过（REQ-001）。
  2) 策略检查通过（REQ-050/051 等）。
  3) 规范化哈希一致性：相同 Envelope 计算的 `canonical_hash` 一致。
  4) 可复现性测试：相同输入与解码策略在多个平台上重放结果一致（或在定义的容差内一致）。

# 9.1 人机对齐（Alignment）
- REQ-320: `body.what.kpi` SHOULD 给出可度量的指标或验收条件（例如准确率≥阈值、覆盖率、JSON 校验通过率）。
- REQ-321: `body.why.goals` 与 `body.what.kpi` SHOULD 可映射（目标→指标）。
- REQ-322: 若指定 `how_much.quality_guidance` 或其他可度量标准，则 SHOULD 同时提供可计算的 `what.output_schema` 或外部评测脚本，以便对齐度可验证。
- REQ-323: `how_meta.governance.verification` SHOULD 包含 `schema_validate` 与 `policy_check`，并 MAY 包含 `self_check`（模型/规则的独立自检）。

# 10. 版本与兼容（Versioning）
- REQ-060: `pps_version` 采用语义化版本；1.0 对未来 1.x 的新增可选字段后向兼容。

# 11. 互操作最小子集（Interoperability Profile）
- REQ-070: 最小子集包括 Header+Body+Integrity 的上述必需字段，`how_meta` 可选。

# 12. 参考实现与符合性套件（Informative）
本标准包不包含任何脚本。实现者 MAY 使用“独立发布的参考实现/符合性套件”（Conformance Suite）进行工程级校验与基准评测，其中包含示例、校验与规范化工具以及 CI 用法。请以发布页面提供的链接与版本号为准。

# 附录 A（Informative）：受控约束词汇（中英同义）
- 禁止外部浏览 | no_external_browse
- 仅使用提供的证据 | use_provided_evidence
- 需要引用 | citations_required
- 禁止个人身份信息 | no_pii



# 附录 B（Informative）：PPS‑Content Profile 与严格度门槛（与领域无关）
本附录给出面向“内容创作/任务执行”的通用门槛，用于提升跨模型复现稳定性。它不改变主规范，仅作为可选的互操作 Profile。

## B.1 Profile 声明
- 在 `header.compliance` 中声明：
  - Profile：`pps-content`（或 `pps-core`、`pps-analysis`、`pps-code`、`custom`）
  - 严格度：`strict` | `balanced`（默认）| `permissive`
  - 示例：`["pps-content", "balanced"]`

## B.2 结构与类型要求（在本 Profile 下）
- `body.what.task` MUST 非空字符串。
- `body.who.audience` 若存在 MUST 为数组。
- `body.how_to_do.steps` 若存在 MUST 为数组。
- `body.how_much` 推荐采用“量化五要素”（与主规范兼容）：
  - `content_length`（篇幅/规模）
  - `structure_elements`（结构/段落/模块）
  - `detail_richness`（细节/要素密度）
  - `quality_guidance`（质量标准）
  - `cultural_depth`（文化/投入/深度）

> 注：以上字段名为推荐实践，落地实现可通过 Schema 做映射，但校验时需保证“量化要素≥N项已填”。

## B.3 最低门槛（随严格度）
- strict：
  - `why.goals` ≥ 4
  - `who.audience` ≥ 4
  - `how_to_do.steps` ≥ 6
  - `how_much` 五要素均已填写（5/5）
- balanced（默认）：3 / 3 / 5 / 5
- permissive：2 / 2 / 4 / 3

当严格度为 strict 时，未达标 SHOULD 作为 error；balanced/permissive 下可作为 warning。


# 附录 C（Informative）：最小可互操作样例（balanced 档）
以下样例仅演示结构与门槛，并非绑定具体体裁/领域。

```json
{
  "header": {
    "pps_version": "PPS-v1.0.0",
    "model": {"name": "example-model", "digest": "sha256-model-xyz", "data_cutoff": "2025-01-01"},
    "decode": {"seed": 0, "temperature": 0, "top_p": 1},
    "locale": "zh-CN",
    "compliance": ["pps-content", "balanced"],
    "created_at": "2025-10-01T12:00:00Z"
  },
  "body": {
    "what": {"task": "示例任务：撰写主题介绍"},
    "why": {"goals": ["传达核心要点", "提供实用信息", "促进理解与应用"]},
    "who": {"persona": "专业助手", "audience": ["初学者", "从业者", "决策者"]},
    "when": {"timeframe": "当前周期，阶段性交付"},
    "where": {"environment": "线上文档与通用工作环境"},
    "how_to_do": {"paradigm": "CoT", "steps": ["梳理要点", "组织结构", "撰写内容", "校对发布", "收集反馈"]},
    "how_much": {
        "content_length": "1000-1500字",
        "structure_elements": "3-4个主要段落，含标题与摘要",
        "detail_richness": "5-8个关键点，必要例证与数据",
      "quality_guidance": "逻辑清晰、术语统一、可读性高",
      "cultural_depth": "适度引用权威或行业背景"
    },
    "how_feel": {"tone": "专业友好", "style": "清晰", "audience_level": "intermediate"}
  },
  "integrity": {"canonical_hash": "sha256:TO_BE_FILLED_AFTER_CANONICALIZATION"}
}
```


# 附录 D（Informative）：校验清单（Checklists）
## D.1 结构与一致性
- [ ] JSON Schema 校验通过（REQ-001）
- [ ] `body.what.task` 非空（REQ-100）
- [ ] `who.audience` 为数组（若存在）
- [ ] `how_to_do.steps` 为数组（若存在）
- [ ] `where.citations_required=true` ⇒ `evidence` ≥ 1（REQ-180）
- [ ] `how_to_do.tools ⊆ who.capabilities`（REQ-181；可做宽松语义匹配）
- [ ] 约束冲突：`no_external_browse` ⇒ 不允许 `web_browse`（REQ-183）

## D.2 质量门槛（按严格度）
- strict：
  - [ ] `why.goals` ≥ 4
  - [ ] `who.audience` ≥ 4
  - [ ] `how_to_do.steps` ≥ 6
  - [ ] `how_much` 五要素均已填写（5/5）
- balanced（默认）：3 / 3 / 5 / 5
- permissive：2 / 2 / 4 / 3

## D.3 可复现性
- [ ] `decode.temperature=0` 且 `top_p=1`（确定性，REQ-012）
- [ ] 计算并存储 `integrity.canonical_hash`（REQ-030/300）
- [ ] 记录模型与解码参数，保证重放一致（REQ-040/302/303）

## D.4 可选接口/输出结构
 - [ ] 若使用 `how_interface.schema` 约束输出形态，其值为对象
 - [ ] 若仅在 `what.output_schema` 提供 Schema，运行时 MAY 复制至 `how_interface.schema` 用于校验（REQ-175）


# 附录 E（Informative）：PPS‑QR 可选绑定规范（Binding v1）
本附录定义“将 PPS 指令以二维码携带”的可选绑定方式，便于线下/跨端快速核验与复用。该绑定不改变主规范，仅约束二维码承载的文本格式与最小字段，以确保不同实现之间互操作。

## E.1 目标
- 扫码后可直接读取人类可读的 5W3H 指令摘要，并具备完整性核验所需信息。
- 不包含任何敏感/私密信息；以 `integrity.canonical_hash` 作为唯一完整性依据。

## E.2 载荷（UTF‑8 纯文本）
- MUST：
  - `pps_version`（来自 `header.pps_version`）
  - `created_at`（来自 `header.created_at`）
  - `task`（来自 `body.what.task`）
  - `canonical_hash`（完整值 `sha256:…`；若显示空间受限，可显示 `id_short` 但同时在载荷中留存完整哈希）
  - `verification_hint`（例如：对比哈希确认指令完整性）
  - `instruction`（按 5W3H 组织的可读指令文本；仅展示非空维度）
- SHOULD：
  - `id_short`：对 `canonical_hash` 的固定长度截断（建议后 12–16 位）
  - `provider_note`：人类可读说明（如“此结构化指令可跨模型复用”）
- MAY：
  - `signature` / `public_key_id`：若实现方采用签名
  - `retrieval_uri`：可选的 JSON Envelope 获取地址（不依赖网络即可核验）

建议文本组织：
```
PPS指令认证
指令任务: <task>
创建时间: <created_at>
指令ID: <id_short>
验证方式: 对比哈希值确认指令完整性
PPS标准: <pps_version>
full_hash: <sha256:...>

=== 完整指令内容 ===

任务目标 (What): ...
执行原因 (Why): ...
执行角色 (Who): ...
时间安排 (When): ...
执行场所 (Where): ...
执行方法 (How to do): ...
量化要素 (How much): ...
预期效果 (How feel): ...

=== 使用说明 ===
请按照以上内容完成任务
```

## E.3 编码与容错
- 字符编码：UTF‑8 纯文本。
- 纠错等级：L 或 M；内容过长时允许对可读描述“适度压缩”，但不得删除 5W3H 标题键。

## E.4 安全与隐私
- MUST 不包含个人身份信息、密钥、访问令牌等敏感数据。
- `id_short` 非敏感标识；严格核验依赖 `canonical_hash` 重算对比。

## E.5 核验流程（扫码端）
1. 读取 `canonical_hash` 与 5W3H 指令；
2. 从指令重建最小 Envelope（或经 `retrieval_uri` 获取 JSON Envelope）；
3. 进行规范化序列化（移除 `integrity`，字典键排序、紧凑 JSON）；
4. 计算 SHA‑256 与 `canonical_hash` 对比；
5. 一致则通过核验。

## E.6 版本化
- 绑定版本：`PPS‑QR Binding v1`；
- 当绑定格式新增可选字段时，对既有实现后向兼容；核心 MUST 字段不变。