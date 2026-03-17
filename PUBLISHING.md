# PPS v1.0 — 发布指南（Release & DOI）

本指南用于将 PPS（Prompt Protocol Specification）v1.0 发布为社区规范并生成可引用的 DOI。

## 1) 打标签与创建 Release

```bash
# 确认工作区干净
git status

# 打标签（轻量或附注均可，建议附注）
git tag -a v1.0.0 -m "PPS v1.0.0 Community Specification"

git push origin v1.0.0
```

然后在托管平台（GitHub/Gitee 等）创建 Release，附：
- 亮点与变更摘要（要点）
- 校验命令（见 README 与 spec/PPS-1.0/README）
- 许可与 IP 声明链接（LICENSE、spec/PPS-1.0/IP_NOTICE.md、STATUS.md）

## 2) 连接 Zenodo 并生成 DOI

1. 登录 Zenodo（https://zenodo.org/）
2. 关联仓库 → 选择允许创建 Release 时自动抓取归档
3. 在仓库创建 Release 后，Zenodo 会生成一个条目，包含：
   - 永久 DOI（如 10.5281/zenodo.xxxxxx）
   - 时间戳与版本
4. 将 DOI 回填到：
   - 根 README（引用/徽章）
   - spec/PPS-1.0/README（引用方式）

## 3) 版本与分支策略
- 遵循 semver：规范性更改 → minor/major；文案修正 → patch
- 长期维护分支：`main`（发布）、`next`（增量草案，可选）

## 4) 发布检查清单
- [ ] Schema 与脚本自测通过：`node tests/pps-conformance/summary.js`
- [ ] 文档无嵌套 how 残留；how_much 为开放容器
- [ ] 示例 `pps_version=PPS-v1.0.0`
- [ ] LICENSE（MIT）、文档许可（CC BY 4.0）与 IP_NOTICE
- [ ] STATUS.md 路线图更新

## 5) 沟通与采用
- 在 README 附“采用与致谢模板”（ADOPTION_TEMPLATE）
- 发表博客/演讲，介绍 PPS 的动机、结构与合格套件
- 跟踪采用者，汇总实践反馈进入 v1.0.x 增量
