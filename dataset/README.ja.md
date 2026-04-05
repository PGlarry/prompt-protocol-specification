# PPS-Bench：意図アライメント研究のための多言語並列プロンプトデータセット

**[English](README.md) | [中文](README.zh.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Español](README.es.md)**

---

## 概要

PPS-Benchは、**人間とAIの相互作用における構造化意図伝達**の研究を目的としたオープンな多言語ベンチマークデータセットです。3言語・複数のプロンプト条件とアブレーション設定・6つのAIモデル・3つのタスクドメインにわたる並列プロンプトを提供し、各レコードには目標アライメント（GA）評価スコアが付いています。Paper 4 では s-ICMw と DS も含まれます。

本データセットはPPS（プロンプトプロトコル仕様）研究論文に付随して公開され、再現可能な実験を支援し、プロンプトエンジニアリングコミュニティの参照コーパスとして機能します。

---

## データセット統計

| 次元 | 詳細 |
|------|------|
| 総レコード数（重複含む） | **8,820件** |
| 一意な実験レコード数 | **8,280件** |
| 言語 | ZH（中国語）・EN（英語）・JA（日本語） |
| プロンプト条件 | 6種類（A / B / C / D / E / F）+ Paper 4 単一次元アブレーション |
| AIモデル | Claude・GPT-4o・Gemini 2.5 Pro・DeepSeek・Qwen・Kimi |
| タスクドメイン | 旅行・ビジネス・技術 |
| ドメインあたりのタスク数 | 20件 |
| 評価指標 | 目標アライメントスコア（1〜5点、DeepSeek-V3による評価）; Paper 4 には s-ICMw と DS も含む |

---

## 6つのプロンプト条件

| ID | 名称 | 説明 |
|----|------|------|
| **A** | シンプルプロンプト | 一文のタスク説明（ベースライン） |
| **B** | 構造化JSON（PPS生） | レンダリングなしの生PPS JSON |
| **C** | 手動5W3H（自然言語） | 手動作成の5W3H自然言語版 |
| **D** | AI拡張5W3H（PPS完全版） | [lateni.com](https://lateni.com)のAI意図拡張で生成した8次元完全PPSプロンプト |
| **E** | CO-STAR | CO-STARフレームワークで構造化されたプロンプト |
| **F** | RISEN | RISENフレームワークで構造化されたプロンプト |

**D条件**のプロンプトは[lateni.com](https://lateni.com)プラットフォームで生成されました。各D条件プロンプトには8次元すべて（What/Why/Who/When/Where/How-to-do/How-much/How-feel）と、SHA-256フィンガープリント・バージョン・タイムスタンプを含むPPSメタデータが含まれています。

> 注：lateni.comの拡張アルゴリズムは独自技術です。生成されたプロンプト内容は完全に公開されています。

---

## Paper 4 単一次元アブレーション

Paper 4 は独立したデータパッケージとして公開され、`FULL` と 7 つの次元削除条件
（`-why`, `-who`, `-when`, `-where`, `-how_to_do`, `-how_much`, `-how_feel`）を含みます。
公開対象は Paper 4 本文で直接使用したデータに限定され、`v2` 忠実度スコアや将来の IST 理論論文向け解析は含みません。

---

## ファイル構造

```
dataset/
├── README.md                   ← 英語
├── README.zh.md                ← 中国語
├── README.ja.md                ← 日本語（本ファイル）
├── README.ko.md                ← 韓国語
├── README.es.md                ← スペイン語
├── data/
│   ├── paper1/
│   ├── paper2/
│   ├── paper3/
│   ├── paper4/
│   │   ├── pps_bench_paper4_zh.jsonl  ← 1,440件
│   │   ├── pps_bench_paper4_en.jsonl  ← 720件
│   │   ├── pps_bench_paper4_ja.jsonl  ← 720件
│   │   └── pps_bench_paper4.jsonl     ← 2,880件
│   └── pps_bench_full.jsonl           ← 8,820件の全データ
└── statistics/
    └── summary.json            ← データセットメタデータ
```

---

## レコードスキーマ

```json
{
  "id": "ja-claude-travel-D-T01",
  "lang": "ja",
  "model": "claude",
  "model_version": "claude-sonnet-4-20250514",
  "condition": "D",
  "condition_name": "AI-Expanded 5W3H (PPS Full)",
  "domain": "travel",
  "pair_id": "T01",
  "topic": "東京",
  "prompt": "...",
  "output": "...",
  "goal_alignment": 5,
  "ga_reasoning": "..."
}
```

---

## 主要結果

| 条件 | 全体平均GA | 説明 |
|------|-----------|------|
| A | 4.463 | ベースライン（シンプルプロンプト） |
| B | 4.141 | 生JSON — 最低スコア |
| C | 4.683 | 手動5W3H |
| D | 4.930 | AI拡張5W3H（PPS完全版） |
| E | 4.978 | CO-STAR |
| F | 4.983 | RISEN |

**注目の発見**：構造化プロンプト（D/E/F）により言語間スコアの分散が最大24倍削減（σ：0.470 → 0.020）され、意図伝達の言語非依存性が示されました。

---

## 引用

```bibtex
@dataset{pps_bench_2026,
  title     = {PPS-Bench: A Multilingual Parallel Prompt Dataset for Intent Alignment Research},
  author    = {[著者]},
  year      = {2026},
  url       = {https://github.com/PGlarry/prompt-protocol-specification},
  note      = {4本の論文にまたがる8,820件（ユニーク 8,280件）のレコード}
}
```

---

## ライセンス

本データセットは [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) ライセンスの下で公開されています。
