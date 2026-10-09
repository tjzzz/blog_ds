---
title: "PNN模型(Product-based Neural Network)"
created: 2026-10-09
updated: 2026-10-09
tags: [llm-wiki, migrated]
source: ["Input/rebuild_source_2026-10-09/06_推荐系统/PNN模型(Product-based Neural Network).md"]
wiki_type: methods
topic: "推荐系统"
migrated_from: "06_推荐系统/PNN模型(Product-based Neural Network).md"
review_status: structural
---

> 所属 Topic：[推荐系统](../../topics/%E6%8E%A8%E8%8D%90%E7%B3%BB%E7%BB%9F.md) · 类型：方法

> 在NeuralCF的基础上，加入多组特征。2016年，上海交通大学的研究人员提出的PNN[5]模型。


网络结构：
![500](../../media/recovered/02f951683076-Pasted%20image%2020230601170249.png)
- 乘积层部分：z表示的是内积操作部分，p表示的是外积操作部分。无论是内积还是外积，都要求前面embedding向量的维度相同。



与deep crossing模型的区别在于，PNN用乘积层代替了stacking层，即不同特征的embedding向量不是简单的拼接，而是两两乘积操作之后再拼接。

product层特征交叉的两种方式：
- 内积$g_{inner} = <f_i, f_j>$
- 外积 $g_{outer}=f_if_j^T$，生成的是一个矩阵
