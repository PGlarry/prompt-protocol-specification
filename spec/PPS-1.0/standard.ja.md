---
title: Prompt Protocol Specification (PPS) v1.0 — 規範仕様書（日本語）
status: community-specification
version: 1.0.0
lang: ja
---

**言語 / Language / 语言 / 언어 / Idioma**：[中文](standard.md) · [English](standard.en.md) · [日本語](standard.ja.md) · [한국어](standard.ko.md) · [Español](standard.es.md)

---

## 目次

| セクション | 内容 |
|-----------|------|
| [§1](#1-スコープ) | スコープ |
| [§2](#2-用語) | 用語 |
| [§3](#3-データモデル規範スキーマ) | データモデル（8次元） |
| [§4](#4-ヘッダー必須) | ヘッダー |
| [§5](#5-ボディ必須) | ボディ |
| [§6](#6-インテグリティ必須) | インテグリティ |
| [§7](#7-決定性とリプレイ) | 決定性とリプレイ |
| [§8](#8-セキュリティとコンプライアンス) | セキュリティとコンプライアンス |
| [§9](#9-適合性) | 適合性 |
| [§10](#10-バージョニング) | バージョニング |
| [§11](#11-相互運用プロファイル) | 相互運用プロファイル |
| [§12](#12-リファレンス実装情報提供) | リファレンス実装 |
| [附属書 A](#附属書-a-情報提供制約語彙) | 制約語彙 |
| [附属書 B](#附属書-b-情報提供ppsコンテントプロファイルと厳密性しきい値) | 適合性しきい値 |
| [附属書 C](#附属書-c-情報提供最小相互運用可能例) | 最小例 |
| [附属書 D](#附属書-d-情報提供検証チェックリスト) | 検証チェックリスト |
| [附属書 E](#附属書-e-情報提供pps-qrオプションバインディング仕様) | PPS-QRバインディング |

---

# 1. スコープ

本仕様は、人間とAIのインタラクションに関する指示プロトコルである PPS（Prompt Protocol Specification）の最小相互運用可能実装を定義します。規範的要件は MUST / SHOULD / MAY（RFC 2119 準拠）で表現され、REQ 識別子を付与します。

# 2. 用語

- **エンベロープ（Envelope）**：単一インタラクションのプロトコルキャリア。`header`、`body`、`integrity` の3部で構成されます。
- **正規化（Canonicalization）**：安定したハッシュを生成するための JSON の決定論的な順序付けとシリアライゼーション。
- **決定論的デコード（Deterministic Decoding）**：再現可能なリプレイを可能にする固定デコードパラメータ。

# 3. データモデル（規範スキーマ）

実装者は `schema/pps-1.0.schema.json` に準拠したエンベロープを受け入れ、生成しなければなりません（MUST）（REQ-001）。

## 3.1 8次元とJSONパス（規範マッピング）

- **REQ-100（What）**：`body.what.task` を提供しなければなりません（MUST）。出力が構造化 JSON の場合、`body.what.output_schema` を提供すべきです（SHOULD）。
  - JSON パス：`/body/what/{task, input_schema?, output_schema?}`

- **REQ-110（Why）**：`body.why.goals` をリストすべきです（SHOULD）。制約は附属書 A の制御語彙（例：`no_external_browse`、`citations_required`、`use_provided_evidence`）から取るべきです（SHOULD）。
  - JSON パス：`/body/why/{goals?, constraints?}`

- **REQ-120（Who）**：`persona` を指定すべきです（SHOULD）。ツールを使用する場合、`who.capabilities` でホワイトリスト登録しなければなりません（MUST）。
  - JSON パス：`/body/who/{persona?, capabilities?, policy?}`

- **REQ-130（When）**：`timeframe` または `validity_window` のうち少なくとも一方を提供しなければなりません（MUST）。
  - JSON パス：`/body/when/{timeframe?, validity_window?, staleness_policy?}`

- **REQ-140（Where）**：`citations_required=true` の場合、少なくとも1件の `evidence` エントリを提供しなければなりません（MUST）。エビデンスには `digest` と `title` を含めるべきです（SHOULD）。
  - JSON パス：`/body/where/{environment?, evidence[], jurisdiction?, citations_required?}`

- **REQ-150（How-to-do）**：`paradigm` と `steps` を指定すべきです（SHOULD）。`tools` に記載するツールは REQ-181（ケイパビリティ制約）を満たさなければなりません（MUST）。
  - JSON パス：`/body/how_to_do/{paradigm?, steps?, tools?}`

- **REQ-160（How-much）**：*生成されるコンテンツそのもの*を対象とした定量的要素（長さ、構造、詳細密度、品質指針、文化的深度など）を指定すべきです（SHOULD）。フィールド名はオープンセットであり、ドメイン固有のキーと単位が許可されます。これらの定量化は生成コンテンツに関するものであり、システムリソースや呼び出しクォータに関するものではありません。
  - JSON パス：`/body/how_much/{content_length?, structure_elements?, detail_richness?, quality_guidance?, cultural_depth?}`

- **REQ-161（統合定量化コンテナとしての How-much）**：本仕様は *how much* と *how many* を別次元として区別しません。すべての量・リソース関連の定量化は `how_much` に統合されます。実装は同義フィールド（例：`how_many`）を `how_much` にマッピングして正規化しなければなりません（MUST）。

- **REQ-170（How-feel）**：`tone` と `style` を指定すべきです（SHOULD）。特定の受け手を対象とする場合、`audience_level` は列挙値から選ばなければなりません（MUST）。
  - JSON パス：`/body/how_feel/{tone?, style?, audience_level?}`

- **REQ-175（インターフェース / ガバナンス）**：出力インターフェースが JSON の場合、スキーマは `what.output_schema` または `how_interface.schema` の少なくとも一方に記載しなければなりません（MUST）。`what` にのみ記載する場合、実装者は検証のためにランタイムで `how_interface.schema` にコピーしてよいです（MAY）。

## 3.2 部分仕様と自動補完

- **REQ-340**：`what.task` は利用者が提供しなければならない最小入力です（MUST）。
- **REQ-341**：残りの7次元は省略または部分的に省略してよいです（MAY）。実装はデフォルトポリシー、検索結果、または推論によって補完します。
- **REQ-342**：自動補完が行われた場合、システムは補完または上書きされたフィールドを `header.implementation.filled_fields`（JSON ポインタ配列）に記録しなければなりません（MUST）。使用したデフォルト設定を `header.implementation.defaults_profile` に注記してよいです（MAY）。主要な仮定を `header.implementation.assumptions` に記録してよいです（MAY）。
- **REQ-343**：自動補完はガバナンス制約に違反してはなりません（MUST NOT）。例えば、宣言されていないケイパビリティを持つツールを注入することは権限昇格にあたります（REQ-181 参照）。`function_call` などのケイパビリティは、既存の `fn:*` ツール呼び出しを満たすためにのみ、準拠している場合にのみ追加してよいです（MAY）。

---

# 4. ヘッダー（必須）

- **REQ-010**：`PPS-vMAJOR.MINOR.PATCH` 形式の `pps_version` を含めなければなりません（MUST）。
- **REQ-011**：`model.name`、`model.digest`、`model.data_cutoff` を指定しなければなりません（MUST）。
- **REQ-012**：`decode.seed`、`decode.temperature`、`decode.top_p` を指定しなければなりません（MUST）。決定論的リプレイには `temperature=0`、`top_p=1` を使用します。
- **REQ-013**：`locale` を指定しなければなりません（MUST）。`header.created_at` には作成タイムスタンプを記録すべきです（SHOULD）。

---

# 5. ボディ（必須）

- **REQ-020**：フラットな8次元（`what`、`why`、`who`、`when`、`where`、`how_to_do`、`how_much`、`how_feel`）をすべて含めなければなりません（MUST）。
- **REQ-021**：`how_to_do`、`how_much`、`how_feel` は兄弟フィールドです。ツールは対応するケイパビリティが宣言されている場合にのみ使用できます。
- **REQ-022**：`where.citations_required=true` の場合、少なくとも1件のエビデンス（URI + digest またはタイトル）エントリを提供しなければなりません（MUST）。

---

# 6. インテグリティ（必須）

- **REQ-030**：`integrity.canonical_hash` を設定しなければなりません（MUST）。値はエンベロープを正規シリアライズし、SHA-256 を適用し、`sha256:` プレフィックスを付加することで計算されます。

---

# 7. 決定性とリプレイ

- **REQ-040**：リプレイ時はヘッダーの `model.digest` と `decode` パラメータを固定しなければなりません（MUST）。
- **REQ-041**：安定したトランケーションを得るために `stop` を指定すべきです（SHOULD）。

## 7.1 再現性

- **REQ-300**：エンベロープは正規化可能でなければなりません（MUST）。`body`、`header`、`integrity` のいずれかを変更するとハッシュが変わります。
- **REQ-301**：エビデンスの再現性：`where.evidence[].uri` がミュータブルなリソースを指す場合、`digest` と `title` のスナップショットフィールドも提供すべきです（SHOULD）。リプレイ時には digest が一致するローカルキャッシュを優先すべきです（SHOULD）。
- **REQ-302**：デコードの再現性：`decode.seed`、`temperature`、`top_p` は固定しなければなりません（MUST）（REQ-012 参照）。`stop` および `top_k` / `beam_width` も該当する場合は記録すべきです（SHOULD）。
- **REQ-303**：モデルの再現性：`model.digest` は特定のバージョン（モデルウェイト、パラメータ、ツールチェーン）を識別しなければなりません（MUST）。
- **REQ-304**：実装者はリプレイ手順（正規化 → 検証 → ポリシーチェック → 決定論的デコード）を文書化しなければなりません（MUST）。リプレイ出力は以前の出力とトークンレベルで一致するか、定義された許容範囲内に収まるべきです（SHOULD）。

## 7.2 ハッシュ安定性

- **REQ-305**：同一エンベロープを複数回正規化しても同じ `canonical_hash` が生成されなければなりません（MUST）（冪等性）。
- **REQ-306**：正規化アルゴリズムが変更される場合、`pps_version` をバンプしなければなりません（MUST）（MAJOR または MINOR）。

## 7.3 正規化アルゴリズム

クロスプラットフォームの一貫性を確保するため、実装は RFC 8785（JCS — JSON Canonicalization Scheme）と互換性のある最小実装を採用すべきです（SHOULD）：

- **入力**：エンベロープ全体。正規化前に `integrity.canonical_hash` を一時的に除去します。
- **文字列**：標準的な JSON エスケープを用いた UTF-8 エンコード。
- **オブジェクト**：キーを辞書順にソート。
- **配列**：元の順序を保持。
- **数値**：標準的な JSON 表現（末尾ゼロなし）。
- **出力**：正規化バイト列の SHA-256 に `sha256:` プレフィックスを付加。
- **書き戻し**：結果を `integrity.canonical_hash` に格納。

リファレンス実装：`tests/pps-conformance/canonicalize.js`

## 7.4 リプレイアーティファクト

- **REQ-310**：生成システムは `header.implementation` または外部監査ログにリプレイレコード（タイムスタンプ、ホスト、実装バージョン）を出力すべきです（SHOULD）。

---

# 8. セキュリティとコンプライアンス

- **REQ-050**：`header.compliance` に `gdpr` が含まれる場合、`who.policy` に `no_pii` を明示しなければなりません（MUST）。
- **REQ-051**：`why.constraints` で外部ブラウジングが禁止されている場合、`web_browse` その他の外部ネットワークツールを含めてはなりません（MUST NOT）。
- **REQ-052**：`why.constraints` で外部ブラウジングが禁止されており、かつ `what.task` に `http(s)://` URL が含まれる場合、置換またはフラグ付け（例：`[URL_REMOVED]`）し、ポリシー違反または自動修正イベントとして記録しなければなりません（MUST）。
- **REQ-053**：`how_to_do.tools` のすべてのツールは `who.capabilities` に含まれなければなりません（MUST）（ケイパビリティサンドボックス、権限昇格防止）。

## 8.1 クロスフィールド不変条件

- **REQ-180**：`where.citations_required=true` ⇒ エビデンスエントリ数 ≥ 1。
- **REQ-181**：`how_to_do.tools ⊆ who.capabilities`。
- **REQ-182**：`gdpr ∈ header.compliance` ⇒ `no_pii ∈ who.policy`。
- **REQ-183**：`no_external_browse ∈ why.constraints` ⇒ `web_browse ∉ how_to_do.tools`。

## 8.2 フィールドロックと反復的改良

- **REQ-344**：実装者は `body.how_meta.governance.locks` に JSON ポインタのリストを提供してよいです（MAY）。これらのパスを「書き込み保護」としてマークします。再生成またはモデル切り替え時、それらのパスの値は変更してはなりません（MUST NOT）。
- **REQ-345**：実装者は主要フィールドの出所を `header.implementation.origins`（例：`user`、`ai:qwen`、`ai:deepseek`）に記録すべきです（SHOULD）。出所が `user` のフィールドは、ユーザーが明示的にアンロックしない限りデフォルトでロック扱いとなります。

## 8.3 AIコンプライアンステストとアンカリング

- **REQ-346（アンカー優先度）**：ユーザー入力が存在する（`origins` に `user` を含む）か、明示的な `locks` が存在する場合、AI の再生成はそれらのパスをアンカーとして扱い、上書きしてはなりません（MUST NOT）。補完は値が存在しない場合にのみ許可されます。
- **REQ-347（ロック運用セマンティクス）**：
  - ロック粒度：任意の JSON ポインタ（スカラー、オブジェクト、配列）。
  - 優先度：`locks` > `origins` > その他の拡張ポリシー。
  - アンロックメカニズム：ユーザーがポインタを明示的に削除するか、UI または API で `unlock=[...]` を渡した場合にのみ上書き可能。
- **REQ-348（一貫性制約）**：`why.constraints` で外部ブラウジングが禁止されている場合、`how_to_do.tools` に `web_browse` を含めてはなりません（MUST NOT）。`where.citations_required=true` の場合、`evidence` は空であってはなりません（§8.1 と整合）。
- **REQ-349（クロスターン検証）**：実装者は `locks` 指定パスの値が変化していないことを確認するビフォア/アフター比較ツールを提供すべきです（SHOULD）。適合性スイートにこのチェックを含めることを推奨します。
- **REQ-350（失敗処理）**：`locks` または一貫性制約に違反した場合、システムは以前の値にロールバックし、違反と修復イベントを記録しなければなりません（MUST）（`header.implementation` に追記してよいです）。

---

# 9. 適合性

実装者は以下のテストに合格しなければなりません：
1. JSON スキーマ検証に合格すること（REQ-001）。
2. ポリシーチェックに合格すること（REQ-050/051 等）。
3. 正規ハッシュの一貫性：同一エンベロープは常に同じ `canonical_hash` を生成すること。
4. 再現性テスト：同一入力と同一デコード戦略でプラットフォーム間（または定義された許容範囲内）で一貫した出力が得られること。

## 9.1 人間とAIのアライメント

- **REQ-320**：`body.what.kpi` には測定可能な指標または受け入れ基準（例：精度 ≥ しきい値、カバレッジ率、JSON 検証合格率）を提供すべきです（SHOULD）。
- **REQ-321**：`body.why.goals` と `body.what.kpi` はマッピング可能であるべきです（SHOULD）（目標 → 指標）。
- **REQ-322**：`how_much.quality_guidance` またはその他の測定可能な基準が指定されている場合、アライメントが検証可能となるよう、計算可能な `what.output_schema` または外部評価スクリプトを提供すべきです（SHOULD）。
- **REQ-323**：`how_meta.governance.verification` には `schema_validate` と `policy_check` を含めるべきです（SHOULD）。`self_check`（独立したモデル/ルールベースの自己検証）を含めてよいです（MAY）。

---

# 10. バージョニング

- **REQ-060**：`pps_version` はセマンティックバージョニングに従います。v1.0 は将来の v1.x リリースで追加される新しいオプションフィールドと後方互換性があります。

---

# 11. 相互運用プロファイル

- **REQ-070**：最小サブセットは上記のヘッダー + ボディ + インテグリティの必須フィールドで構成されます。`how_meta` はオプションです。

---

# 12. リファレンス実装（情報提供）

本仕様パッケージはスクリプトをバンドルしません。実装者は別途公開されているリファレンス実装と適合性スイートを使用してよいです（MAY）。これには例、検証・正規化ツール、CI 使用ガイダンスが含まれます。権威あるリンクとバージョン番号はリリースページを参照してください。

---

# 附属書 A（情報提供）：制約語彙

| 中国語 | 英語キー |
|--------|----------|
| 禁止外部浏览 | `no_external_browse` |
| 仅使用提供的证据 | `use_provided_evidence` |
| 需要引用 | `citations_required` |
| 禁止个人身份信息 | `no_pii` |

---

# 附属書 B（情報提供）：PPSコンテントプロファイルと厳密性しきい値

本附属書はコンテンツ作成とタスク実行のためのドメイン非依存のしきい値を提供し、クロスモデル再現性の向上を目的としています。主仕様を変更するものではなく、オプションの相互運用プロファイルです。

## B.1 プロファイル宣言

`header.compliance` で宣言します：
- プロファイル：`pps-content`（または `pps-core`、`pps-analysis`、`pps-code`、`custom`）
- 厳密性：`strict` | `balanced`（デフォルト）| `permissive`
- 例：`["pps-content", "balanced"]`

## B.2 構造と型の要件（本プロファイル適用時）

- `body.what.task` は非空文字列でなければなりません（MUST）。
- `body.who.audience` は存在する場合、配列でなければなりません（MUST）。
- `body.how_to_do.steps` は存在する場合、配列でなければなりません（MUST）。
- `body.how_much` は5つの定量化要素を採用すべきです（SHOULD）（主仕様と互換）：
  - `content_length` — 長さ / スケール
  - `structure_elements` — 構造 / セクション / モジュール
  - `detail_richness` — 詳細 / 要素密度
  - `quality_guidance` — 品質基準
  - `cultural_depth` — 文化的コンテキスト / エンゲージメントの深さ

> 注：これらのフィールド名は推奨プラクティスです。実装はスキーマ経由で同等のフィールドをマッピングできますが、検証では「定量化要素 ≥ N フィールドが設定されていること」を確認しなければなりません。

## B.3 最小しきい値（厳密性別）

| レベル | `why.goals` | `who.audience` | `how_to_do.steps` | `how_much` 要素 |
|--------|:-----------:|:--------------:|:-----------------:|:---------------:|
| `strict` | ≥ 4 | ≥ 4 | ≥ 6 | 5 / 5 |
| `balanced`（デフォルト）| ≥ 3 | ≥ 3 | ≥ 5 | ≥ 3 / 5 |
| `permissive` | ≥ 2 | ≥ 2 | ≥ 4 | ≥ 2 / 5 |

`strict` ではしきい値未満をエラーとして報告すべきです（SHOULD）。`balanced` / `permissive` では警告として報告します。

---

# 附属書 C（情報提供）：最小相互運用可能例（balanced）

以下の例は構造としきい値のみを示すものであり、特定のジャンルやドメインに縛られません。

```json
{
  "header": {
    "pps_version": "PPS-v1.0.0",
    "model": {
      "name": "example-model",
      "digest": "sha256-model-xyz",
      "data_cutoff": "2025-01-01"
    },
    "decode": { "seed": 0, "temperature": 0, "top_p": 1 },
    "locale": "ja-JP",
    "compliance": ["pps-content", "balanced"],
    "created_at": "2025-10-01T12:00:00Z"
  },
  "body": {
    "what": { "task": "トピックに関する構造化された入門文を書く" },
    "why": {
      "goals": [
        "核心概念を伝える",
        "実践的な情報を提供する",
        "理解と応用を促進する"
      ]
    },
    "who": {
      "persona": "プロフェッショナルアシスタント",
      "audience": ["初心者", "実践者", "意思決定者"]
    },
    "when": { "timeframe": "現在のサイクル、段階的な納品" },
    "where": { "environment": "オンラインドキュメントおよび一般的な作業環境" },
    "how_to_do": {
      "paradigm": "CoT",
      "steps": [
        "重要なポイントを特定する",
        "構造を整理する",
        "コンテンツを草稿する",
        "レビューして公開する",
        "フィードバックを収集する"
      ]
    },
    "how_much": {
      "content_length": "1000〜1500文字",
      "structure_elements": "見出しとまとめを含む3〜4つのメインセクション",
      "detail_richness": "必要に応じて例とデータを含む5〜8つの重要ポイント",
      "quality_guidance": "論理的な流れ、用語の一貫性、高い可読性",
      "cultural_depth": "権威ある、または業界コンテキストへの適度な参照"
    },
    "how_feel": {
      "tone": "プロフェッショナルかつ親しみやすい",
      "style": "明確",
      "audience_level": "intermediate"
    }
  },
  "integrity": {
    "canonical_hash": "sha256:TO_BE_FILLED_AFTER_CANONICALIZATION"
  }
}
```

---

# 附属書 D（情報提供）：検証チェックリスト

## D.1 構造と一貫性

- [ ] JSON スキーマ検証に合格（REQ-001）
- [ ] `body.what.task` が非空（REQ-100）
- [ ] `who.audience` は存在する場合、配列である
- [ ] `how_to_do.steps` は存在する場合、配列である
- [ ] `where.citations_required=true` ⇒ `evidence` ≥ 1（REQ-180）
- [ ] `how_to_do.tools ⊆ who.capabilities`（REQ-181；意味的マッチング許可）
- [ ] 制約の競合：`no_external_browse` ⇒ `web_browse` 不可（REQ-183）

## D.2 品質しきい値（厳密性別）

- **strict**：
  - [ ] `why.goals` ≥ 4
  - [ ] `who.audience` ≥ 4
  - [ ] `how_to_do.steps` ≥ 6
  - [ ] `how_much` 要素すべて設定済み（5/5）
- **balanced**（デフォルト）：3 / 3 / 5 / 3
- **permissive**：2 / 2 / 4 / 2

## D.3 再現性

- [ ] `decode.temperature=0` かつ `top_p=1`（決定論的、REQ-012）
- [ ] `integrity.canonical_hash` が計算・格納済み（REQ-030 / REQ-300）
- [ ] モデルとデコードパラメータがリプレイ一貫性のために記録済み（REQ-040 / REQ-302 / REQ-303）

## D.4 オプションインターフェース / 出力構造

- [ ] `how_interface.schema` が出力形状を制約する場合、その値はオブジェクトである
- [ ] スキーマが `what.output_schema` にのみ存在する場合、ランタイムは検証のために `how_interface.schema` にコピーしてよい（REQ-175）

---

# 附属書 E（情報提供）：PPS-QRオプションバインディング仕様（Binding v1）

本附属書は QR コードで PPS 指示を伝搬するためのオプションバインディングを定義し、オフラインまたはデバイス間での迅速な検証と再利用を可能にします。主仕様を変更するものではなく、相互運用性を確保するために QR ペイロードのテキスト形式と最小フィールドのみを制約します。

## E.1 目的

- スキャン後、整合性検証に必要な情報とともに、人間が読める5W3H指示サマリーを直接読み取れること。
- 個人情報や機密情報を含まないこと。`integrity.canonical_hash` が唯一の整合性アンカーとなります。

## E.2 ペイロード（UTF-8 プレーンテキスト）

**必須（MUST）：**
- `pps_version`（`header.pps_version` から）
- `created_at`（`header.created_at` から）
- `task`（`body.what.task` から）
- `canonical_hash`（完全な値 `sha256:…`；表示スペースが限られる場合は `id_short` を表示してよいですが、完全なハッシュはペイロードに保持しなければなりません）
- `verification_hint`（例：「ハッシュを比較して指示の整合性を確認してください」）
- `instruction`（5W3H で整理された人間が読める指示テキスト；非空の次元のみ表示）

**推奨（SHOULD）：**
- `id_short`：`canonical_hash` の固定長切り詰め（末尾12〜16文字を推奨）
- `provider_note`：人間が読めるメモ（例：「この構造化指示はAIモデルをまたいで再利用できます」）

**任意（MAY）：**
- `signature` / `public_key_id`：実装が署名を使用する場合
- `retrieval_uri`：JSON エンベロープを取得するためのオプション URI（検証はネットワークアクセスに依存しません）

推奨テキストレイアウト：
```
PPS 指示証明書
タスク: <task>
作成日時: <created_at>
指示ID: <id_short>
検証: ハッシュを比較して指示の整合性を確認してください
PPSバージョン: <pps_version>
完全ハッシュ: <sha256:...>

=== 完全な指示 ===

What（何を）:     ...
Why（なぜ）:      ...
Who（誰が）:      ...
When（いつ）:     ...
Where（どこで）:  ...
How-to-do（方法）: ...
How-much（量）:   ...
How-feel（感触）: ...

=== 使用方法 ===
上記の内容に従ってタスクを完了してください。
```

## E.3 エンコードとエラー訂正

- 文字エンコード：UTF-8 プレーンテキスト。
- エラー訂正レベル：L または M。コンテンツが長すぎる場合、人間が読める説明を適度に圧縮してよいですが、5W3H の見出しキーを削除してはなりません（MUST NOT）。

## E.4 セキュリティとプライバシー

- 個人識別情報、鍵、アクセストークン、その他の機密データを含めてはなりません（MUST NOT）。
- `id_short` は非機密識別子です。厳密な検証は `canonical_hash` を再計算・比較することに依存します。

## E.5 検証フロー（スキャナー側）

1. `canonical_hash` と5W3H指示を読み取ります。
2. 指示から最小エンベロープを再構築します（または `retrieval_uri` 経由で JSON エンベロープを取得します）。
3. 正規シリアライゼーションを実行します（`integrity` を削除し、オブジェクトキーを辞書順にソートし、コンパクト JSON に変換）。
4. SHA-256 を計算し、`canonical_hash` と比較します。
5. 一致 → 検証合格。

## E.6 バージョニング

- バインディングバージョン：`PPS-QR Binding v1`。
- バインディング形式へのオプションフィールドの追加は既存の実装と後方互換性があります。MUST フィールドは変更されません。
