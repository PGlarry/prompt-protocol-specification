# PPS — プロンプト・プロトコル仕様

<div align="center">

**[English](README.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md)**

[![License: MIT](https://img.shields.io/badge/ツール-MIT-blue.svg)](LICENSE)
[![Docs: CC BY 4.0](https://img.shields.io/badge/ドキュメント-CC%20BY%204.0-green.svg)](spec/PPS-1.0/IP_NOTICE.md)
[![Version](https://img.shields.io/badge/PPS-v1.0.0-orange.svg)](spec/PPS-1.0/standard.md)
[![Status](https://img.shields.io/badge/ステータス-コミュニティ仕様-brightgreen.svg)](STATUS.md)

*人間とAIのインタラクションのための、オープンな8次元構造化指示フレームワーク*

</div>

---

<div align="center">

### 今すぐ試す · 書籍を読む · 仕様を探索する

| | |
|---|---|
| **5W3Hプラットフォーム** | [https://www.lateni.com](https://www.lateni.com) — PPSエンベロープをオンラインで設計・体験 |
| **書籍** | [*Super Prompt: 5W3H — 全領域対応 AIプロンプト設計の完全ガイド*](https://www.amazon.com/dp/B0F3Z25CHC)<br>彭剛（Peng Gang）著 · Amazon KDP · 2025年4月 · ASIN: B0F3Z25CHC |

</div>

---

## PPSとは何か

自然言語プロンプトには**意図伝達の損失**という問題があります。ユーザーが本当に必要としていることと、AIシステムに実際に伝わることの間には、システム的なずれが生じています。PPS（プロンプト・プロトコル仕様）は、構造化された機械検証可能な指示エンベロープを提供することで、この問題を解決します。

PPSは**5W3Hモデル**を基盤としています：*What（何をするか）、Why（なぜするか）、Who（誰のためにするか）、When（いつするか）、Where（どこでするか）、How-to-do（どうやってするか）、How-much（どれだけするか）、How-feel（どんな感じにするか）* ——8つの次元で、あらゆるAIタスクを完全に記述します。

```json
{
  "pps_header": {
    "pps_version": "PPS-v1.0.0",
    "model": { "name": "gpt-4o", "digest": "sha256:abc123", "data_cutoff": "2025-01-01" },
    "decode": { "seed": 42, "temperature": 0.7, "top_p": 0.95 },
    "locale": "ja-JP"
  },
  "pps_body": {
    "what": { "task": "日本のEV市場における競合分析レポートを作成する" },
    "why": { "goals": ["戦略的投資判断を支援する"], "constraints": ["no_pii"] },
    "who": { "persona": "シニア産業アナリスト", "audience": ["経営幹部"] },
    "when": { "timeframe": "2024年データ、現在の市場スナップショット" },
    "where": { "environment": "取締役会プレゼンテーション資料", "jurisdiction": "JP" },
    "how_to_do": { "paradigm": "CoT", "steps": ["市場規模算定", "ファイブフォース分析", "主要5社分析", "トレンド予測"] },
    "how_much": { "content_length": "2000字", "structure_elements": "データ表を含む5章構成", "detail_richness": "10以上のデータポイント" },
    "how_feel": { "tone": "プロフェッショナル", "style": "データドリブン", "audience_level": "expert" }
  },
  "pps_integrity": {
    "canonical_hash": "sha256:TO_BE_FILLED_AFTER_CANONICALIZATION"
  }
}
```

---

## なぜPPSを使うのか

制御された実験（60トピック × 3つのLLM × 3条件、540件の出力）からの実証結果：

| 指標 | シンプルプロンプト（A） | PPSレンダリング（C） | 改善幅 |
|------|:---------------------:|:-------------------:|:------:|
| **意図整合スコア** | 4.34 | **4.61** | *p* = 0.006、*d* = 0.374 |
| 必要な追加質問回数 | 約3.3回 | 約1.1回 | **66%削減** |
| 初回展開の正確率 | — | **85%** が正確または非常に正確 | — |

> 詳細な方法論と結果：[論文（arXiv）](https://arxiv.org/abs/PENDING) · [実験データ](experiments/)

**主要な知見**：従来の評価指標では、「制約スコアリングの非対称性」により、シンプルプロンプトが過大評価される傾向があります。制約のないプロンプトは制約遵守スコアで満点を取ってしまうためです。ユーザーの意図整合度（`goal_alignment`）で評価すると、構造化PPSプロンプトがシンプルプロンプトを有意に上回り、特に曖昧度の高いドメインで顕著です（ビジネス分析：*d* = 0.895）。

---

## リポジトリ構成

```
prompt-protocol-specification/
├── spec/
│   └── PPS-1.0/
│       ├── standard.md          # 規範的仕様書（中国語）
│       ├── standard.en.md       # 規範的仕様書（英語）
│       ├── standard.ja.md       # 規範的仕様書（日本語）
│       ├── best-practices.md    # 実装ベストプラクティス
│       ├── conformance.md       # 適合性レベル
│       ├── security-privacy.md  # セキュリティとプライバシー要件
│       ├── versioning.md        # バージョンポリシー
│       ├── benchmark.md         # ベンチマーク方法論
│       ├── registry.md          # 制御語彙一覧
│       └── IP_NOTICE.md         # 特許・知的財産権通知
├── schema/
│   ├── pps-1.0.schema.json      # JSON Schema（厳格版）
│   └── pps.schema.json          # JSON Schema（基本版）
├── spec/examples/               # 注釈付きエンベロープサンプル
├── tests/pps-conformance/       # 適合性テストスイート（Node.js）
├── tools/
│   └── pps-verify.js            # CLI検証ツール
├── STATUS.md                    # 仕様ロードマップとガバナンス
└── PUBLISHING.md                # リリースとDOIガイド
```

---

## クイックスタート

**エンベロープの検証：**
```bash
node tests/pps-conformance/validate.js spec/examples/minimal.json
```

**全適合性チェックの実行：**
```bash
node tests/pps-conformance/summary.js
```

**正規化ハッシュの計算：**
```bash
node tools/pps-verify.js spec/examples/minimal.json
```

**動作環境：** Node.js ≥ 16

---

## 適合性プロファイル

PPSは3つの適合性レベルを定義しており、`header.compliance` で宣言します：

| プロファイル | `why.goals` | `who.audience` | `how_to_do.steps` | `how_much` フィールド数 |
|------------|:-----------:|:--------------:|:-----------------:|:-----------------------:|
| `strict`（厳格） | ≥ 4 | ≥ 4 | ≥ 6 | ≥ 3 |
| `balanced`（バランス） | ≥ 3 | ≥ 3 | ≥ 5 | ≥ 2 |
| `permissive`（寛容） | ≥ 2 | ≥ 2 | ≥ 4 | ≥ 1 |

---

## 学術引用

PPSを学術研究で使用する場合は、以下を引用してください：

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

## 関連リソース

- **5W3Hプラットフォーム**：[https://www.lateni.com](https://www.lateni.com) — PPSエンベロープをオンラインで設計・体験
- **書籍**：[*Super Prompt: 5W3H — 全領域対応 AIプロンプト設計の完全ガイド*](https://www.amazon.com/dp/B0F3Z25CHC)
  彭剛（Peng Gang）著 · Amazon KDP · 2025年4月 · ASIN: B0F3Z25CHC

---

## ライセンス

- **仕様ドキュメント**（`spec/`）：[CC BY 4.0](spec/PPS-1.0/IP_NOTICE.md) — 帰属表示の上、自由に使用・共有・改変可能
- **ツールとテスト**（`tools/`、`tests/`）：[MIT](LICENSE)
- **完全オープン**：PPSと5W3HはTCP/IPと同様、完全にオープンで特許フリーです（特許の出願・主張なし）。誰でも自由に実装・商業化できます。詳細は [IP_NOTICE.md](spec/PPS-1.0/IP_NOTICE.md) をご覧ください。

---

<div align="center">
<sub>作成者：<a href="https://www.lateni.com">彭剛（Peng Gang）</a> · 恵州学院 · 恵州ラテニ人工知能科技有限公司</sub>
</div>
