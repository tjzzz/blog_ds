---
title: Wiki 结构与维护规范
created: 2026-10-09
updated: 2026-10-09
tags: [llm-wiki, schema]
source: []
status: active
---
# Wiki 结构与维护规范

## 从哪里进入

先选 [Topic](topics/index.md)，沿关键问题和阅读路线进入文章。正文按 [概念](concepts/index.md)、[方法](methods/index.md)、[工具](tools/index.md)、[案例](cases/index.md)分工；[关系](relationships/index.md)解释概念之间怎样作用，[综合分析](syntheses/index.md)回答跨主题决策问题。

Topic 是导航，不复制正文。一篇文章可以从多个 Topic 引用，正文只维护一处。旧专题 MOC 和 TOC 保留为 Topic 下的资料页。

## 来源与信息保存

- `Input/` 是原始资料层，默认不进入公开 Git 仓库。2026-10-09 迁移前的 393 篇 Markdown 原文及 SHA-256 清单保存在本地 `Input/rebuild_source_2026-10-09/`；其中 379 篇正文已迁入新结构。
- 迁移正文保留旧文内容，增加 Topic 回链、类型和来源元数据；链接改为新路径。`docs/` 中的文章最多位于“分类 / Topic”两级文件夹。旧 URL 由网站的 404 页面在浏览器中跳转，不再保留旧目录跳转页。迁移只完成**结构归位**，不表示旧结论已经重新核实。
- `review_status: structural` 表示仅完成结构迁移；核查原始依据、修订论证并处理过时内容后，才改为 `reviewed`。
- 私密凭证不得进入 `docs/`。涉及账号、个人路径、邮箱或部署地址的 7 篇文章及旧目录里的非 Markdown 附件已移至本地 `Input/private_pending_review_2026-10-09/`，待人工审定公开范围。

## 页面字段

新正文至少记录 `title`、`created`、`updated`、`tags`、`source`、`topic`、`wiki_type`、`review_status`；迁移文章还记录 `migrated_from`。`source` 指向原始文件或公开来源。仅引用旧笔记时，应明确它是**已有笔记**，不能包装成外部一手证据。

## 摄取和维护

一次处理一个来源：完整阅读 → 摘出可以核实的结论和疑点 → 更新一处正文 → 把它接入相关 Topic 和关系页 → 记录到 [更新日志](wiki-log.md)。定期检查断链、重复概念、矛盾、过时内容和孤立页面。

## 图片和发布

图片统一放在 `docs/media/`。本轮找回的旧素材在 `docs/media/recovered/`；[8 张待找回原图](syntheses/%E5%BE%85%E6%89%BE%E5%9B%9E%E5%9B%BE%E7%89%87.md)暂用明确标注的占位图，原始引用仍记录在私有快照。新增图片要确认来源和公开权限。

发布前检查待提交文件、敏感内容、图片和 MkDocs 构建。`blog_ds` 是公开仓库：即使文件不在 `docs/`，只要被提交到仓库，也能在 GitHub 上被读取。
