---
title: "python-不同数据类型&及其转换"
created: 2026-10-09
updated: 2026-10-09
tags: [llm-wiki, migrated]
source: ["Input/rebuild_source_2026-10-09/07_语言篇/python/python-不同数据类型&及其转换.md"]
wiki_type: tools
topic: "编程与数据工程"
migrated_from: "07_语言篇/python/python-不同数据类型&及其转换.md"
review_status: structural
---

> 所属 Topic：[编程与数据工程](../../topics/%E7%BC%96%E7%A8%8B%E4%B8%8E%E6%95%B0%E6%8D%AE%E5%B7%A5%E7%A8%8B.md) · 类型：工具

# 不同数据类型&及其转换



list转dataframe. `DataFrame(list[list])`

```
from pandas import DataFrame, Series
_list = [[1,2,3,4],[5,6,7,8]]    #包含两个不同的子列表[1,2,3,4]和[5,6,7,8]
df = DataFrame(_list)      #这时候是以行为标准写入的
```

list 转Series

```
ser = Series(_list)
```

series 转numpy的ndarray。 

```
ser.as_matrix()
```

dataframe转numpy的ndarray  

```
df.as_matrix()
df.values
np.array(df)
```



