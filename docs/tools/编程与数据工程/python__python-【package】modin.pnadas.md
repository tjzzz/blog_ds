---
title: "python-【package】modin.pnadas"
created: 2026-10-09
updated: 2026-10-09
tags: [llm-wiki, migrated]
source: ["Input/rebuild_source_2026-10-09/07_语言篇/python/python-【package】modin.pnadas.md"]
wiki_type: tools
topic: "编程与数据工程"
migrated_from: "07_语言篇/python/python-【package】modin.pnadas.md"
review_status: structural
---

> 所属 Topic：[编程与数据工程](../../topics/%E7%BC%96%E7%A8%8B%E4%B8%8E%E6%95%B0%E6%8D%AE%E5%B7%A5%E7%A8%8B.md) · 类型：工具

# 【package】modin.pnadas

安装`pip install modin`

测试数据`test.data`的大小是1.3G

```
import pandas
import modin.pandas
import time

t0 = time.time()
df1 = pandas.read_csv('test.data')
t1 = time.time()
df2 = modin.pandas.read_csv('test.data')
t2 = time.time()

print(t1-t0, t2-t1)
## 15.78716492652893 3.3300700187683105
```

modin.pandas实现了pandas的大部分函数功能，可以覆盖到日常的主要操作，
https://modin.readthedocs.io/en/latest/UsingPandasonRay/dataframe_supported.html



**问题**
在jupyter中我终止了运行后，再次用modin.padnas.pd.read_csv就报错了。


1.1.1. Error During execution: ArrowIOError: Broken Pipe
One of the more frequently encountered issues is an ArrowIOError: Broken Pipe. This error can happen in a couple of different ways. One of the most common ways this is encountered is from pressing CTRL + C sending a KeyboardInterrupt to Modin. In Ray, when a KeyboardInterrupt is sent, Ray will shutdown. This causes the ArrowIOError: Broken Pipe because there is no longer an available plasma store for working on remote tasks. This is working as intended, as it is not yet possible in Ray to kill a task that has already started computation.

The other common way this Error is encountered is to let your computer go to sleep. As an optimization, Ray will shutdown whenever the computer goes to sleep. This will result in the same issue as above, because there is no longer a running instance of the plasma store.

Solution

Restart your interpreter or notebook kernel.




