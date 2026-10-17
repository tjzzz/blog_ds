---
title: Wiki 结构与维护规范
created: 2026-10-09
updated: 2026-10-11
tags: [llm-wiki, schema]
source: []
status: active
wiki_type: site
---
# Wiki 结构与维护规范

## 从哪里进入

先选 [Topic](topics/index.md)，沿关键问题和阅读路线进入文章。正文按子领域保存在 `topics/<主题>/<子领域>/`；页面元数据 `wiki_type` 标明概念、方法、工具、案例等类型。[关系](relationships/index.md)解释概念之间怎样作用，[综合分析](syntheses/index.md)回答跨主题决策问题。

每个 Topic 维护 `topics/<主题>/index.md` 主入口；每个子领域目录以自己的 `index.md` 列出文章。主题级 MOC、TOC 与导读内容并入主入口，原始来源记录在 `source` 和 `merged_from`；专题范围较窄的综述仍可作为独立资料页。Topic 提供导航，一篇正文只放在一个主归属主题的子领域目录中，其他 Topic 通过链接引用。

## 来源与信息保存

- `Input/` 是原始资料层，默认不进入公开 Git 仓库。2026-10-09 迁移处理了 393 篇 Markdown，其中 379 篇正文进入新结构或私有待审区。搬迁后的本地库目前没有完整的 393 篇原稿快照；`Input/legacy_docs_2026-10-09/` 中尚有 338 篇逐文件哈希核对的旧文备份。
- 迁移正文保留旧文内容，增加 Topic 回链、类型和来源元数据；链接改为新路径。项目根目录就是 MkDocs 文档源，正文位于“Topic / 子领域 / 文章”三级目录。旧 URL 由网站的 404 页面在浏览器中跳转，不再保留旧目录跳转页。迁移只完成**结构归位**，不表示旧结论已经重新核实。
- `review_status: structural` 表示仅完成结构迁移；核查原始依据、修订论证并处理过时内容后，才改为 `reviewed`。
- 私密凭证不得进入公开页面目录。涉及账号、个人路径、邮箱或部署地址的 7 篇文章及旧目录里的非 Markdown 附件已移至本地 `Input/private_pending_review_2026-10-09/`，待人工审定公开范围。

## 页面字段

新正文至少记录 `title`、`created`、`updated`、`tags`、`source`、`topic`、`wiki_type`、`review_status`；迁移文章还记录 `migrated_from`。`wiki_type` 使用 `concepts`、`methods`、`tools`、`cases` 标记正文类型；主题入口为 `topic`，主题综述文章为 `topics`，细分专题页为 `subtopic`，跨主题页面分别为 `relationship` 或 `synthesis`。`source` 指向原始文件或公开来源。仅引用旧笔记时，应明确它是**已有笔记**，不能包装成外部一手证据。

## 摄取和维护

一次处理一个来源：完整阅读 → 摘出可以核实的结论和疑点 → 更新一处正文 → 把它接入相关 Topic 和关系页 → 记录到 [更新日志](wiki-log.md)。定期检查断链、重复概念、矛盾、过时内容和孤立页面。

## 图片和发布

图片统一放在 `media/`。本轮找回的旧素材在 `media/recovered/`；[8 张待找回原图](syntheses/%E5%BE%85%E6%89%BE%E5%9B%9E%E5%9B%BE%E7%89%87.md)暂用明确标注的占位图，原文件名记录在待找回清单。新增图片要确认来源和公开权限。

发布前检查待提交文件、敏感内容、图片和 MkDocs 构建。MkDocs 配置只收录明确列出的公开页面目录。`blog_ds` 是公开仓库：即使文件没有进入网站，只要被提交到仓库，也能在 GitHub 上被读取。
