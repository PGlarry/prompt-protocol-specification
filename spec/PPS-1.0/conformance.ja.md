---
title: PPS v1.0 適合性 & テスト仕様
lang: ja
status: draft
version: 1.0.0
---

# 1. 範囲
PPS v1.0 の最小適合テストを定義する：Schema 検証、ポリシーチェック、再現性、ハッシュ一貫性。出力は人手レビューおよび CI を対象とする。

# 2. 必須検証項目
1) JSON Schema（REQ-001）：`spec/pps-1.0.schema.json`
2) ポリシーチェック（REQ-050/051/052/053、180..183、320..323）
3) 正規化ハッシュ一貫性（REQ-300）
4) デコード決定性（REQ-012/302）とクロスプラットフォームリプレイ（許容差内）

# 3. ツール & コマンド
- 正規化 / ハッシュ：`node tests/pps-conformance/canonicalize.js <file> --write`
- Schema 検証：`node tests/pps-conformance/validate.js <file>`
- ポリシーチェック：`node tests/pps-conformance/policy_checks.js <file> --json`
- 自動修復：`node tests/pps-conformance/auto_fix.js <file> --write`

# 4. 出力フォーマット（推奨）
ポリシーチェック `--json`：
```json
{ "pass": true, "warnings": [], "issues": [{ "type": "tool_capability_missing", "message": "..." }] }
```

# 5. CI 統合（推奨）
CI では `spec/examples/*.json` の各ファイルに対して順番に実行する：正規化 → Schema → ポリシー →（必要に応じて）自動修復 → 集約。失敗はパイプラインをブロックする。
