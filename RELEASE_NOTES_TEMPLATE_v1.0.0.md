# PPS v1.0.0 — Release Notes (ZH/EN)

## 简介 (Introduction)
- 本次发布为 Prompt Protocol Specification（PPS）v1.0.0 的社区规范版本，提供 5W3H 扁平八维结构、开放量化容器（how_much）与完整的符合性套件（Schema/Policy/Locks/Hash）。
- This release publishes PPS v1.0.0 as a community, patent‑free specification with flat 5W3H dimensions, open quantification container (how_much), and a complete conformance suite (Schema/Policy/Locks/Hash).

## 亮点 (Highlights)
- 扁平 8 维映射（what/why/who/when/where/how_to_do/how_much/how_feel）
- how_much 采用开放键名（跨体裁量化，不含系统配额语义）
- 交叉一致性与越权策略校验（禁外链、证据要求、工具能力匹配）
- 锁一致性机制与校验工具（locks_compliance）
- 规范化哈希（canonical_hash）与离线验证工具（pps-verify）

## 兼容性 (Compatibility)
- JSON Schema: `spec/pps.schema.json` / `spec/pps-1.0.schema.json`
- Policy/Hash/Locks：`tests/pps-conformance/*`
- 示例均为 `PPS-v1.0.0`

## 许可证与 IP (License & IP)
- Docs: CC BY 4.0；Code/Tools: MIT；Spec is patent‑free (no patents filed or claimed)
- PPS 与 5W3H 完全开放，任何人可自由实现与商业化，无需专利授权，详见 `spec/PPS-1.0/IP_NOTICE.md`

## 一键校验 (One‑command checks)
```bash
node tests/pps-conformance/summary.js
```

## 升级说明 (Upgrade Notes)
- 若此前实现使用嵌套 how 结构或固定 how_much 五要素：
  - 迁移至扁平键：`how_to_do`、`how_much`、`how_feel`
  - how_much 改为开放键集合，策略脚本不再绑定字段名

## 已知问题 (Known Issues)
- 对抗用例（Expected‑Fail）会在策略或锁检查中失败，属设计行为

## 鸣谢 (Credits)
- Authors, contributors, and adopters

---

## English Summary
- PPS v1.0.0 (Community Specification) — flat 5W3H, open how_much, conformance suite
- Patent‑free (no patents filed); Docs CC BY 4.0; Tools MIT; see IP_NOTICE.md
- Run `node tests/pps-conformance/summary.js` to validate examples
