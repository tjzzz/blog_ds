# Project_DS：数据科学 LLM Wiki

本地 Obsidian Vault 与公开博客共用同一目录。博客地址：<https://tjzzz.github.io/blog_ds/>。

## 阅读结构

从 [`docs/topics/index.md`](docs/topics/index.md) 的 13 个 Topic 进入，再进入以下四种正文：

- [`docs/concepts/`](docs/concepts/index.md)：概念和定义
- [`docs/methods/`](docs/methods/index.md)：方法、模型和适用条件
- [`docs/tools/`](docs/tools/index.md)：工具、环境和工程实践
- [`docs/cases/`](docs/cases/index.md)：案例、实战与学习记录

[`docs/relationships/`](docs/relationships/index.md)解释知识之间的联系；[`docs/syntheses/`](docs/syntheses/index.md)整合跨主题问题。页面字段与维护方式见 [`docs/wiki-schema.md`](docs/wiki-schema.md)。

## 来源与迁移

`Input/` 是私有原始资料层，现有 `.gitignore` 排除它。`Input/rebuild_source_2026-10-09/` 保存迁移前 393 篇 Markdown 原文、逐文件 SHA-256 和素材修复记录。379 篇可迁移正文中，372 篇已进入公开分类；7 篇涉及个人资料或部署信息的文章放在 `Input/private_pending_review_2026-10-09/`，待审后处理。`docs/` 只保留“分类 / Topic / 文章”两级目录。旧编号目录已删除，旧博客 URL 通过 404 页中的迁移表跳转到新地址；这是一种浏览器跳转，旧地址仍会先返回 404 状态。

本轮完成的是**全库结构归位与链接修复**。迁移页标记 `review_status: structural`，表示旧文中的事实、过时信息和外部来源尚需逐篇核查，不能当作新近审定的结论。新增 AI 与 Agent 内容也在此范围内。

## 图片

旧图尽量从当前 Vault 和本机备份恢复，放在 `docs/media/recovered/`。8 张找不到原文件的图片使用明确标注的占位图，见 [`docs/syntheses/待找回图片.md`](docs/syntheses/待找回图片.md)。Excalidraw 原稿仍在本地 `附件/`；未导出的图稿在正文中标注原始路径。

## 本地检查

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/wiki_lint.py
.venv/bin/mkdocs build --clean --strict
.venv/bin/mkdocs serve
```

校验脚本使用仓库内的迁移映射检查公开页面；本机若保留 `Input/rebuild_source_2026-10-09/` 私有快照，还会逐文件核对原稿哈希。

博客由 `.github/workflows/ci.yml` 在 `master/main` 推送后构建并发布到 GitHub Pages。公开前检查待提交文件和图片；公开仓库中 `docs/` 之外的已提交文件同样可见，私有原始资料不得提交。
