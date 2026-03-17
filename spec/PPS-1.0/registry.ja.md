---
title: PPS v1.0 管理語彙レジストリ
lang: ja
status: draft
version: 1.0.0
---

# 1. 制約（Constraints）
- `no_external_browse` | 外部ブラウズを禁止
- `use_provided_evidence` | 提供されたエビデンスのみ使用
- `citations_required` | 引用が必要
- `no_pii` | 個人識別情報を禁止

# 2. 能力（Capabilities）
- `web_browse` | 外部ブラウズ
- `function_call` | 関数呼び出し
- その他のツール名は「ツール名 = 能力名」ルールに従う

# 3. パラダイム（Paradigms）
- `ReAct`, `CoT`, `ToT`, `Plan-Execute`, `None`

# 4. 用語の正規化（Normalization）
- `how_many` ⇒ `how_much` に正規化

# PPS v1.0 推奨語彙（非規範的）

本文書は、実装者がさまざまなジャンル・シナリオで再利用できる「推奨語彙」を提供する。標準 Schema の自由度と互換性は変更しない。実装は必要に応じて採用またはカスタマイズできる。組織内部のスタイルガイドとの整合を推奨する。

## how_much（コンテンツ定量化コンテナ）推奨フィールド
- 汎用（テキスト / レポート / 記事）
  - content_length: 例 "800〜1200字"、"5〜7万字"
  - structure_elements: 例 "3〜4段落"、"10〜12章"
  - detail_richness: 例 "各段落3〜5ポイント"、"データと図表を含む"
  - quality_guidance: 例 "用語統一・検証可能・引用規格準拠"
  - cultural_depth: 例 "分野背景 / 規格比較 / ローカライズ対応"
- 旅行 / ガイド
  - poi_count: "50以上の観光地"
  - price_ranges: "入場料0〜150元"、"宿泊80〜2000元/泊"
  - itinerary_days: "1〜5日間の旅程"
- コード / 開発
  - module_count: "3〜5モジュール"
  - api_count: "2〜3つのAPIエンドポイント"
  - test_coverage_hint: "サンプルテストケース + 基本分岐カバレッジ"
- 歌詞 / 詩
  - line_count: "16〜24行"
  - stanza_count: "3〜4連"
  - rhyme_scheme: "AABB / ABAB"
- チュートリアル / チェックリスト
  - steps_count: "5〜8ステップ"
  - checklist_items: "10〜15項目"

注：上記はあくまで例示である。`how_much` は文字列またはオブジェクトで構わない。フィールド名や単位は強制されない。ドメイン固有のカスタマイズを推奨する。
