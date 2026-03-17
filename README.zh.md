# PPS — 提示词协议规范

<div align="center">

**[English](README.md) · [中文](README.zh.md) · [日本語](README.ja.md)**

[![License: MIT](https://img.shields.io/badge/工具-MIT-blue.svg)](LICENSE)
[![Docs: CC BY 4.0](https://img.shields.io/badge/文档-CC%20BY%204.0-green.svg)](spec/PPS-1.0/IP_NOTICE.md)
[![Version](https://img.shields.io/badge/PPS-v1.0.0-orange.svg)](spec/PPS-1.0/standard.md)
[![Status](https://img.shields.io/badge/状态-社区规范-brightgreen.svg)](STATUS.md)

*面向人机交互的开放8维度结构化指令框架*

</div>

---

## 什么是 PPS？

自然语言提示词存在**意图传递损耗**——用户的真实需求与实际传达给 AI 的内容之间存在系统性偏差。PPS（提示词协议规范）通过提供结构化、机器可验证的指令信封来解决这一问题。

PPS 基于 **5W3H 模型**构建：*What（做什么）、Why（为何做）、Who（为谁做）、When（何时做）、Where（在哪做）、How-to-do（怎么做）、How-much（做多少）、How-feel（什么感觉）*——8个维度完整刻画任意 AI 任务。

```json
{
  "pps_header": {
    "pps_version": "PPS-v1.0.0",
    "model": { "name": "qwen-max", "digest": "sha256:abc123", "data_cutoff": "2025-01-01" },
    "decode": { "seed": 42, "temperature": 0.7, "top_p": 0.95 },
    "locale": "zh-CN"
  },
  "pps_body": {
    "what": { "task": "撰写中国新能源汽车市场竞争格局分析报告" },
    "why": { "goals": ["支持战略投资决策"], "constraints": ["no_pii"] },
    "who": { "persona": "资深行业分析师", "audience": ["高级管理层"] },
    "when": { "timeframe": "2024年数据，当前市场快照" },
    "where": { "environment": "董事会汇报材料", "jurisdiction": "CN" },
    "how_to_do": { "paradigm": "CoT", "steps": ["市场规模测算", "波特五力分析", "TOP5品牌分析", "趋势预测"] },
    "how_much": { "content_length": "2000字", "structure_elements": "5个章节含数据表格", "detail_richness": "10+个数据支撑点" },
    "how_feel": { "tone": "专业", "style": "数据驱动", "audience_level": "expert" }
  },
  "pps_integrity": {
    "canonical_hash": "sha256:TO_BE_FILLED_AFTER_CANONICALIZATION"
  }
}
```

---

## 为什么选择 PPS？

来自受控实验的实证结果（60个主题 × 3个大模型 × 3种条件，共540份输出）：

| 指标 | 简单提示词（A） | PPS渲染版（C） | 提升幅度 |
|------|:---------------:|:--------------:|:--------:|
| **意图对齐度** | 4.34 | **4.61** | *p* = 0.006，*d* = 0.374 |
| 需要追问轮数 | ≈ 3.3轮 | ≈ 1.1轮 | **降低66%** |
| 首次展开准确率 | — | **85%** 准确或非常准确 | — |

> 完整方法与结果：[论文（arXiv）](https://arxiv.org/abs/PENDING) · [实验数据](experiments/)

**核心发现**：传统评估指标因"约束评分不对称"现象虚高了简单提示词的得分——无约束提示词在约束遵从维度上得到满分，是空洞的真命题。当以用户意图对齐度（`goal_alignment`）评估时，结构化 PPS 提示词显著优于简单提示词，在高歧义领域尤为突出（商业分析：*d* = 0.895）。

---

## 仓库结构

```
prompt-protocol-specification/
├── spec/
│   └── PPS-1.0/
│       ├── standard.md          # 规范性规范文本（中文）
│       ├── standard.en.md       # 规范性规范文本（英文）  [即将发布]
│       ├── best-practices.md    # 实现最佳实践
│       ├── conformance.md       # 符合性级别
│       ├── security-privacy.md  # 安全与隐私要求
│       ├── versioning.md        # 版本策略
│       ├── benchmark.md         # 基准测试方法
│       ├── registry.md          # 受控词汇表
│       └── IP_NOTICE.md         # 专利与知识产权声明
├── schema/
│   ├── pps-1.0.schema.json      # JSON Schema（严格版）
│   └── pps.schema.json          # JSON Schema（基础版）
├── spec/examples/               # 带注释的示例信封文件
├── tests/pps-conformance/       # 符合性测试套件（Node.js）
├── tools/
│   └── pps-verify.js            # 命令行验证工具
├── STATUS.md                    # 规范路线图与治理
└── PUBLISHING.md                # 发布与DOI指南
```

---

## 快速开始

**验证一个信封文件：**
```bash
node tests/pps-conformance/validate.js spec/examples/minimal.json
```

**运行全部符合性检查：**
```bash
node tests/pps-conformance/summary.js
```

**计算规范化哈希：**
```bash
node tools/pps-verify.js spec/examples/minimal.json
```

**环境要求：** Node.js ≥ 16

---

## 符合性级别

PPS 定义三种符合性级别，在 `header.compliance` 中声明：

| 级别 | `why.goals` | `who.audience` | `how_to_do.steps` | `how_much` 字段数 |
|------|:-----------:|:--------------:|:-----------------:|:-----------------:|
| `strict`（严格） | ≥ 4 | ≥ 4 | ≥ 6 | ≥ 3 |
| `balanced`（均衡） | ≥ 3 | ≥ 3 | ≥ 5 | ≥ 2 |
| `permissive`（宽松） | ≥ 2 | ≥ 2 | ≥ 4 | ≥ 1 |

---

## 学术引用

如在学术研究中使用 PPS，请引用：

```bibtex
@article{peng2026pps,
  title     = {PPS: Structured Intent Transmission — An Empirical Study of a
               5W3H-Based Prompt Protocol for Human-AI Interaction},
  author    = {Peng, Gang},
  year      = {2026},
  note      = {arXiv preprint, cs.HC},
  url       = {https://github.com/PGlarry/prompt-protocol-specification}
}
```

---

## 相关资源

- **5W3H 平台**：[https://www.lateni.com](https://www.lateni.com) — 生产环境实现
- **书籍**：*Super Prompt: 5W3H*（Amazon KDP，2025年4月）——实践指南

---

## 许可证

- **规范文档**（`spec/`）：[CC BY 4.0](spec/PPS-1.0/IP_NOTICE.md) — 署名后可自由使用、分享、改编
- **工具与测试**（`tools/`、`tests/`）：[MIT](LICENSE)
- **专利声明**：PPS 规范不主张任何专利，详见 [IP_NOTICE.md](spec/PPS-1.0/IP_NOTICE.md)

---

<div align="center">
<sub>作者：<a href="https://www.lateni.com">彭刚</a> · 惠州学院 · 惠州拉特尼人工智能科技有限公司</sub>
</div>
