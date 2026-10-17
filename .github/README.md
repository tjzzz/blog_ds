# Project_DS：数据科学 LLM Wiki

本地 Obsidian Vault 与公开博客共用同一目录。博客地址：<https://tjzzz.github.io/blog_ds/>。

## 阅读结构

从 [`topics/index.md`](../topics/index.md) 的 13 个 Topic 进入；每个主题的 `index.md` 通向子领域目录，子领域的 `index.md` 列出文章。概念、方法、工具和案例正文按子领域放置，每篇正文的 `wiki_type` 元数据标记文档类型。一个页面只维护一份，其他主题通过链接引用。

[`relationships/`](../relationships/index.md)解释知识之间的联系；[`syntheses/`](../syntheses/index.md)整合跨主题问题。页面字段与维护方式见 [`wiki-schema.md`](../wiki-schema.md)。

## 来源与迁移

`Input/` 是私有原始资料层，现有 `.gitignore` 排除它。迁移时处理了 393 篇 Markdown；搬迁后的本地库目前没有当时生成的 393 篇完整原稿快照。现存 `Input/legacy_docs_2026-10-09/` 中有 338 篇经哈希核对的旧文备份。379 篇可迁移正文中，372 篇已进入公开 Wiki；7 篇涉及个人资料或部署信息的文章放在 `Input/private_pending_review_2026-10-09/`，待审后处理。正文统一放在“Topic / 子领域 / 文章”三级目录。旧编号目录已删除，旧博客 URL 通过 404 页中的迁移表跳转到新地址；这是一种浏览器跳转，旧地址仍会先返回 404 状态。

本轮完成的是**全库结构归位与链接修复**。迁移页标记 `review_status: structural`，表示旧文中的事实、过时信息和外部来源尚需逐篇核查，不能当作新近审定的结论。新增 AI 与 Agent 内容也在此范围内。

## 图片

旧图尽量从当前 Vault 和本机备份恢复，放在 `media/recovered/`。8 张找不到原文件的图片使用明确标注的占位图，见 [`syntheses/待找回图片.md`](../syntheses/待找回图片.md)。Excalidraw 原稿仍在本地 `附件/`；未导出的图稿在正文中标注原始路径。

## 本地检查

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python config/scripts/wiki_lint.py
.venv/bin/mkdocs build --clean --strict -f config/mkdocs.yml
.venv/bin/python config/scripts/check_site_output.py
.venv/bin/mkdocs serve -f config/mkdocs.yml
```

校验脚本使用仓库内的迁移映射检查公开页面，并核对当前可用的 338 篇旧文备份；如果找回 `Input/rebuild_source_2026-10-09/`，还会逐文件核对完整原稿哈希。

博客由 `.github/workflows/ci.yml` 在 `master/main` 推送后构建并发布到 GitHub Pages。MkDocs 只收录 `topics/`、`relationships/`、`syntheses/`、`media/`、`js/`、主题静态资源 `assets/` 和四个根目录站点页；`Input/` 等本地资料不进入构建。公开前检查待提交文件和图片；公开仓库中已提交的文件同样可见，私有原始资料不得提交。
