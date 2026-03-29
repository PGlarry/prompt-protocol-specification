# PPS-Bench：面向意图对齐研究的多语言平行提示词数据集

**[English](README.md) | [中文](README.zh.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Español](README.es.md)**

---

## 概述

PPS-Bench 是一个用于研究**人-AI交互中结构化意图传递**的开放多语言基准数据集。数据集提供跨3种语言、6种提示词格式、3个AI模型、3个任务领域的平行对比，每条记录均附有意图对齐（GA）评分。

本数据集配套 PPS（提示词协议规范）系列研究论文发布，支持可复现实验，并作为提示词工程社区的参考语料库。

---

## 数据集统计

| 维度 | 详情 |
|------|------|
| 总记录数 | **4,440 条** |
| 语言 | ZH（中文）、EN（英文）、JA（日文） |
| 提示词条件 | A / B / C / D / E / F（共6种） |
| AI 模型 | Claude、GPT-4o、Gemini 2.5 Pro、DeepSeek、Qwen、Kimi |
| 任务领域 | 旅行、商务、技术 |
| 每领域任务数 | 20 条 |
| 评估指标 | 意图对齐分数（1-5分，由 DeepSeek-V3 评判） |

### 按论文分类

| 论文 | 语言 | 模型 | 条件 | 记录数 |
|------|------|------|------|--------|
| 论文1 | ZH | DeepSeek / Qwen / Kimi | A / B / C | 120（旅行领域） |
| 论文2 | EN + JA | DeepSeek / Qwen / Kimi | A / B / C | 1,080 |
| 论文3 | ZH + EN + JA | Claude / GPT-4o / Gemini | A / B / C / D / E / F | 3,240 |
| **合计** | | **6个模型** | | **4,440** |

---

## 6种提示词条件说明

| ID | 名称 | 描述 |
|----|------|------|
| **A** | 简单提示词 | 一句话任务描述（基线） |
| **B** | 结构化 JSON（PPS 原始） | 未渲染的原始 PPS JSON |
| **C** | 手动5W3H（自然语言） | 人工撰写的5W3H自然语言版本 |
| **D** | AI扩展5W3H（PPS完整版） | 通过 [lateni.com](https://lateni.com) AI自动扩展生成的8维度完整PPS指令 |
| **E** | CO-STAR | 使用 CO-STAR 框架结构化的提示词 |
| **F** | RISEN | 使用 RISEN 框架结构化的提示词 |

**D条件**提示词由 [lateni.com](https://lateni.com) 平台生成，该平台基于5W3H框架实现AI辅助意图扩展。每条D条件指令包含完整8个维度（What/Why/Who/When/Where/How to do/How much/How feel），并附有PPS元数据（SHA-256指纹、版本号、时间戳）。

> 注：lateni.com 的扩展算法为专有技术，不开源。生成后的提示词内容完全公开。

---

## 文件结构

```
dataset/
├── README.md                   ← 英文说明
├── README.zh.md                ← 中文说明（本文件）
├── README.ja.md                ← 日文说明
├── README.ko.md                ← 韩文说明
├── README.es.md                ← 西班牙文说明
├── data/
│   ├── pps_bench_zh.jsonl      ← 1,080 条中文记录
│   ├── pps_bench_en.jsonl      ← 1,080 条英文记录
│   ├── pps_bench_ja.jsonl      ← 1,080 条日文记录
│   └── pps_bench_full.jsonl    ← 3,240 条完整数据
└── statistics/
    └── summary.json            ← 数据集元信息
```

---

## 记录字段说明

JSONL 文件每行为一条记录：

```json
{
  "id": "zh-claude-travel-A-T01",
  "lang": "zh",
  "model": "claude",
  "model_version": "claude-sonnet-4-20250514",
  "condition": "A",
  "condition_name": "Simple Prompt",
  "domain": "travel",
  "pair_id": "T01",
  "topic": "东京",
  "prompt": "帮我写一篇东京旅游攻略。",
  "output": "...",
  "goal_alignment": 5,
  "ga_reasoning": "The output perfectly aligns with..."
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | 字符串 | 唯一记录标识符 |
| `lang` | 字符串 | 语言代码：`zh` / `en` / `ja` |
| `model` | 字符串 | 模型名称：`claude` / `gpt4o` / `gemini` |
| `model_version` | 字符串 | 实验使用的具体模型版本 |
| `condition` | 字符串 | 提示词条件：`A`–`F` |
| `condition_name` | 字符串 | 条件的可读名称 |
| `domain` | 字符串 | 任务领域：`travel` / `business` / `technical` |
| `pair_id` | 字符串 | 领域内任务编号（T01–T20、B01–B20、tech_01–tech_20） |
| `topic` | 字符串 | 任务主题关键词 |
| `prompt` | 字符串 | 实际发送给模型的完整提示词 |
| `output` | 字符串 | 模型输出内容 |
| `goal_alignment` | 整数 | 意图对齐分数：1–5（5=完美对齐） |
| `ga_reasoning` | 字符串 | 评判模型的评分理由 |

---

## 核心实验结果

| 条件 | 全局平均 GA | 说明 |
|------|------------|------|
| A | 4.463 | 基线（简单提示词） |
| B | 4.141 | 原始 JSON — 最差，尤其损害较弱的模型 |
| C | 4.683 | 手动5W3H |
| D | 4.930 | AI扩展5W3H（PPS完整版） |
| E | 4.978 | CO-STAR |
| F | 4.983 | RISEN |

**关键发现**：结构化提示词（D/E/F）将跨语言得分方差降低高达24倍（σ：0.470 → 0.020），证明了意图传递的语言无关性。

---

## Python 使用示例

```python
import json

# 加载中文记录
records = []
with open("data/pps_bench_zh.jsonl", encoding="utf-8") as f:
    for line in f:
        records.append(json.loads(line))

# 对比同一任务不同条件
task = [r for r in records if r["pair_id"] == "T01" and r["model"] == "claude"]
for r in task:
    print(f"条件 {r['condition']}: GA={r['goal_alignment']} | {r['prompt'][:60]}...")
```

```python
import pandas as pd

# 加载完整数据集
df = pd.read_json("data/pps_bench_full.jsonl", lines=True)

# 按条件和模型计算平均 GA
pivot = df.groupby(["condition", "model"])["goal_alignment"].mean().unstack()
print(pivot)
```

---

## 引用格式

如果您在研究中使用了 PPS-Bench，请引用：

```bibtex
@dataset{pps_bench_2026,
  title     = {PPS-Bench: A Multilingual Parallel Prompt Dataset for Intent Alignment Research},
  author    = {[作者]},
  year      = {2026},
  url       = {https://github.com/PGlarry/prompt-protocol-specification},
  note      = {3,240条记录，涵盖3种语言、6种提示词条件、3个AI模型}
}
```

---

## 相关资源

- **PPS 规范文档**：[spec/PPS-1.0/](../spec/PPS-1.0/)
- **PPS 提示词生成平台**：[lateni.com](https://lateni.com)
- **研究论文**：参见仓库根目录 README

---

## 许可证

本数据集以 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 协议发布。您可以自由使用、分享和改编数据用于任何目的，但需注明来源。
