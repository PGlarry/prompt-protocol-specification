---
title: Prompt Protocol Standard (PPS) v1.0 — ベストプラクティス（参考情報）
lang: ja
status: draft
version: 1.0.0
---

# 1. 設計ガイドライン
- **What** を骨格に：一文のタスク + 構造化 KPI。
- **Why** を制約の列挙に：機械可読な短いフレーズ（"外部ブラウズ禁止"、"引用必須"、"プライバシーポリシー"など）。
- **Who** 能力ホワイトリスト：使用可能なツール名のみを宣言し、未宣言の能力はデフォルトで拒否。
- **When** 時制ポリシー：`timeframe` または `validity_window` を提供し、`staleness_policy` を宣言する（例："期限切れは拒否 / 低品質処理"）。
- **Where** エビデンス & 環境：`environment` を固定する。`citations_required=true` の場合は `evidence`（uri・digest・title）を提供し、管理素材を優先する。必要に応じて `jurisdiction` を明記する。外部リンクコンテンツは注入防止のためインライン化またはプレースホルダーで置換する。
- **How-to-do** 透明性：ステップ形式またはパラダイムラベル（ReAct / CoT / ToT）。
- **How-much** "コンテンツ本体"に向けた定量化：`content_length`（ボリューム）、`structure_elements`（段落 / 章 / モジュール）、`detail_richness`（詳細密度）、`quality_guidance`（品質指針）、`cultural_depth`（文化 / 深度）。トークン / 時間 / コストなどシステム層の意味論は避ける。
- **How-feel** スタイル：レジスター、受講者レベル。

ヒント：`how_many` は使用せず、すべての定量化を `how_much` 内で表現する。

## 1.1 最小 8 次元テンプレート（コピー可）
```json
{
  "header": {
    "pps_version": "PPS-v1.0.0",
    "model": { "name": "<model>", "digest": "sha256-<digest>", "data_cutoff": "2024-01-01" },
    "decode": { "seed": 1, "temperature": 0, "top_p": 1 },
    "locale": "ja-JP",
    "implementation": { "vendor": "local", "version": "1.0.0", "filled_fields": [], "defaults_profile": "strict" }
  },
  "body": {
    "what": { "task": "<コアタスク>", "output_schema": { } },
    "why": { "goals": ["<目標>"], "constraints": ["use_provided_evidence", "no_external_browse"] },
    "who": { "persona": "<役割>", "capabilities": ["json_output"] },
    "when": { "timeframe": "今週" },
    "where": { "environment": "prod", "citations_required": true, "evidence": [] },
    "how_to_do": { "paradigm": "ReAct", "steps": ["エビデンスを読む", "出力を統合する"], "tools": [] },
    "how_much": { "content_length": "800〜1200字", "structure_elements": "3〜4段落", "detail_richness": "5〜8ポイント" },
    "how_feel": { "tone": "フォーマル", "style": "簡潔", "audience_level": "mixed" },
    "how_interface": { "format": "json", "schema": {} }
  },
  "integrity": { "canonical_hash": "" }
}
```

# 2. 再現性
- `seed/temperature/top_p/stop` を固定し、入力エビデンスを正規化する。外部検索については URI + ダイジェストでアンカーする。

# 3. セキュリティ & コンプライアンス
- URL 注入：実行可能な外部リンクではなく引用指向のコンテンツを生成する。`http(s)` を明示的に除去またはプレースホルダーで置換する。
- ツール越権：能力とツールを分離し、先に宣言してから使用する。越権テストケースを CI に追加する。
- GDPR：`who.policy` に `no_pii` を明記し、出力側で匿名化ルールを適用する。

# 4. 自己チェック & 自動修復
- 自己チェッカー：生成後に schema / ポリシー / セルフチェックを実行する。失敗した場合は自動修復に移行する（競合ツールの無効化、エビデンス補充、ポリシー注入）。
  - ルール例：`gdpr ⇒ no_pii`、`citations_required ⇒ evidence≥1`、`no_external_browse ⇒ url_removed + tools-{web_browse}`。

## 4.1 反復的拡張とロック（実践）
- `how_meta.governance.locks` にロックパスを明記する（例：`/body/where`）。ターン / モデルをまたいで変更せず、アンロックフィールドにのみ拡張的な書き換えを適用する。
- `header.implementation.origins` に由来を記録する：`user` は最高優先度でデフォルトロック；`ai:*` はモデルの貢献を追跡する。

# 5. 合成 & パイプライン
- マルチステージは `P2 ∘ P1` として連鎖する。各ステージで独自の `canonical_hash` と予算を保持し、集約前に重複排除とバージョンロックを行う。

# 6. バージョン管理
- `PPS-vMAJOR.MINOR.PATCH` を使用する。MAJOR は破壊的変更の場合のみ引き上げる。サンプルと CI は対象バージョンを明記する。
