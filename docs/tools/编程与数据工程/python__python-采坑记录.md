---
title: "python-采坑记录"
created: 2026-10-09
updated: 2026-10-09
tags: [llm-wiki, migrated]
source: ["Input/rebuild_source_2026-10-09/07_语言篇/python/python-采坑记录.md"]
wiki_type: tools
topic: "编程与数据工程"
migrated_from: "07_语言篇/python/python-采坑记录.md"
review_status: structural
---

> 所属 Topic：[编程与数据工程](../../topics/%E7%BC%96%E7%A8%8B%E4%B8%8E%E6%95%B0%E6%8D%AE%E5%B7%A5%E7%A8%8B.md) · 类型：工具

# 采坑记录

计算余弦函数的反函数

```
RuntimeWarning: invalid value encountered in arccos
angles.append(np.arccos(value))
```
这里value的值必须是[-1, 1] 因为计算精度问题，可能实际数值是0.9999但是搞成了1.000002这样的



