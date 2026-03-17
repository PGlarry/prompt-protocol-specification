# Contributing to PPS

**[English](#contributing-to-pps) · [中文](#参与贡献) · [日本語](#コントリビューション)**

Thank you for your interest in contributing to the Prompt Protocol Specification.

## How to Contribute

### Reporting Issues
- Use [GitHub Issues](https://github.com/PGlarry/prompt-protocol-specification/issues) to report bugs, ambiguities, or gaps in the specification.
- Clearly label issues: `bug`, `clarification`, `enhancement`, or `question`.

### Proposing Changes
1. Open an issue first to discuss the proposed change.
2. Fork the repository and create a branch: `fix/your-description` or `feat/your-description`.
3. Make your changes following the conventions below.
4. Submit a Pull Request referencing the issue.

### Specification Conventions
- Normative requirements use **MUST / SHOULD / MAY** (RFC 2119).
- Each normative statement carries a unique **REQ-NNN** identifier.
- New requirements must not conflict with existing REQ numbers; propose a new number in your PR.
- Examples in `spec/examples/` must be valid against `schema/pps-1.0.schema.json`.

### Scope of Changes
| Type | Process |
|------|---------|
| Typo / formatting | Direct PR, no issue required |
| Clarification (non-normative) | Issue + PR |
| New normative requirement | Issue discussion first, then PR |
| Breaking change (MAJOR bump) | Issue discussion + maintainer approval |

## Code of Conduct
Be respectful and constructive. This project follows the [Contributor Covenant](https://www.contributor-covenant.org/) v2.1.

---

## 参与贡献

感谢您对提示词协议规范的关注。

### 提交问题
- 使用 [GitHub Issues](https://github.com/PGlarry/prompt-protocol-specification/issues) 报告错误、歧义或规范空白。
- 请使用标签：`bug`、`clarification`、`enhancement` 或 `question`。

### 提交修改
1. 先开 Issue 讨论您的修改方案。
2. Fork 仓库，创建分支：`fix/描述` 或 `feat/描述`。
3. 按照以下规范进行修改。
4. 提交 Pull Request 并关联对应的 Issue。

### 规范约定
- 规范性要求使用 **MUST / SHOULD / MAY**（RFC 2119）。
- 每条规范性声明带有唯一的 **REQ-NNN** 编号。
- 新增要求不得与现有 REQ 编号冲突，请在 PR 中提议新编号。
- `spec/examples/` 中的示例必须通过 `schema/pps-1.0.schema.json` 校验。

---

## コントリビューション

PPS への貢献に関心をお寄せいただきありがとうございます。

### 問題の報告
- バグ、曖昧な記述、仕様の不足は [GitHub Issues](https://github.com/PGlarry/prompt-protocol-specification/issues) でご報告ください。
- ラベルを使用してください：`bug`、`clarification`、`enhancement`、`question`。

### 変更の提案
1. まず Issue を開いて提案内容を議論してください。
2. リポジトリをフォークし、ブランチを作成：`fix/説明` または `feat/説明`。
3. 以下の規約に従って変更を行ってください。
4. 対応する Issue を参照した Pull Request を提出してください。
