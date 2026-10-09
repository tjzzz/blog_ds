---
title: "原理篇—AutoRec"
created: 2026-10-09
updated: 2026-10-09
tags: [llm-wiki, migrated]
source: ["Input/rebuild_source_2026-10-09/06_推荐系统/原理篇—AutoRec.md"]
wiki_type: concepts
topic: "推荐系统"
migrated_from: "06_推荐系统/原理篇—AutoRec.md"
review_status: structural
---

> 所属 Topic：[推荐系统](../../topics/%E6%8E%A8%E8%8D%90%E7%B3%BB%E7%BB%9F.md) · 类型：概念

> 2015年由澳大利亚国立大学提出的AutoRec，它将自编码器(AutoEncoder)的思想和协同过滤结合，提出了一种单隐层神经网络推荐模型

[自编码器ing](../%E6%B7%B1%E5%BA%A6%E5%AD%A6%E4%B9%A0/%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5__%E8%87%AA%E7%BC%96%E7%A0%81%E5%99%A8ing.md)

AutoRec也是针对的用户x物品共线矩阵，对一个物品i 来说，所有m 个用户对它的评分可形成一个m 维的向量r(i)=(R1i，…，Rmi)，AutoRec 要解决的问题是构建一个重建函数h(r；θ)，使所有该重建函数生成的评分向量与原评分向量的平方残差和最小.
![](../../media/recovered/9504ca5446e1-Pasted%20image%2020230531161119.png)


该模型结构代表的重建函数的具体形式:
$$h(r;\theta)=f(Wg(WR+u) +b)$$
整体的目标函数就是：
$$min \sum |r^i - h(r_i;\theta)|^2 + \lambda /2 (|W|^2_F + |V|^2_F)$$
这是一个非常标准的三层神经网络，模型的训练利用梯度反向传播即可完成。


与协同过滤算法一样，AutoRec也分为基于物品的AutoRec和基于用户的AutoRec。以上介绍的AutoRec输入向量是物品的评分向量，因此可称为I-AutoRec(Item based AutoRec)，如果换做把用户的评分向量作为输入向量，则得到U-AutoRec (User based AutoRec)
