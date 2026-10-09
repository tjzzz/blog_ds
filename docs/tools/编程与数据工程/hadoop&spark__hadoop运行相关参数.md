---
title: "hadoop运行相关参数"
created: 2026-10-09
updated: 2026-10-09
tags: [llm-wiki, migrated]
source: ["Input/rebuild_source_2026-10-09/07_语言篇/hadoop&spark/hadoop运行相关参数.md"]
wiki_type: tools
topic: "编程与数据工程"
migrated_from: "07_语言篇/hadoop&spark/hadoop运行相关参数.md"
review_status: structural
---

> 所属 Topic：[编程与数据工程](../../topics/%E7%BC%96%E7%A8%8B%E4%B8%8E%E6%95%B0%E6%8D%AE%E5%B7%A5%E7%A8%8B.md) · 类型：工具

# hadoop运行相关参数



在任务运行时候修改参数

|  任务   |   命令  |
| --- | --- |
| kill任务 | hadoop job -kill ${job-id} |
| 修改优先级 |job -set-priority ${job-id} ${priority}|
| 修改map并发 | hadoop job -set-map-capacity job-id n |
| 修改reduce并发 | hadoop job -set-reduce-capacity job-id n |
| 任务挂起 | hadoop job -suspend ${job-id} $hours |


