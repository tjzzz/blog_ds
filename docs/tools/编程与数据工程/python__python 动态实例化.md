---
title: "python 动态实例化"
created: 2026-10-09
updated: 2026-10-09
tags: [llm-wiki, migrated]
source: ["Input/rebuild_source_2026-10-09/07_语言篇/python/python 动态实例化.md"]
wiki_type: tools
topic: "编程与数据工程"
migrated_from: "07_语言篇/python/python 动态实例化.md"
review_status: structural
---

> 所属 Topic：[编程与数据工程](../../topics/%E7%BC%96%E7%A8%8B%E4%B8%8E%E6%95%B0%E6%8D%AE%E5%B7%A5%E7%A8%8B.md) · 类型：工具

# Python动态实例化：如何动态导入模块中类的字符串名称



https://cloud.tencent.com/developer/ask/41307




```
module = __import__(module_name)
class_ = getattr(module, class_name)
instance = class_()

```

