---
title: "python-seaborn"
created: 2026-10-09
updated: 2026-10-09
tags: [llm-wiki, migrated]
source: ["Input/rebuild_source_2026-10-09/02_数据/DataVisulization/python-seaborn.md"]
wiki_type: concepts
topic: "数据科学工作流"
migrated_from: "02_数据/DataVisulization/python-seaborn.md"
review_status: structural
---

> 所属 Topic：[数据科学工作流](../../topics/%E6%95%B0%E6%8D%AE%E7%A7%91%E5%AD%A6%E5%B7%A5%E4%BD%9C%E6%B5%81.md) · 类型：概念

#todo
# seaborn

## 常用function





## 

时序类，转变下格式

```python
import numpy as np
import pandas as pd;
import matplotlib.pyplot as plt
# 构建 时间序列数据 从2000-1-31开始，以月份为间隔，构建100条记录
index = pd.date_range("1 1 2000", periods=100,freq="m", name="date")
data = np.random.randn(100, 4).cumsum(axis=0)

# 构建5列数据，列名分别为data a b c d
wide_df = pd.DataFrame(data, index, ["a", "b", "c", "d"])
"""
案例7：绘制时间序列数据
"""
sns.lineplot(data=wide_df)
plt.show()
```


背景设置 https://blog.csdn.net/dongzixian/article/details/102480875
https://zhuanlan.zhihu.com/p/27435863



