---
title: "rnn-综述"
created: 2026-10-09
updated: 2026-10-09
tags: [llm-wiki, migrated]
source: ["Input/rebuild_source_2026-10-09/05_深度学习/rnn/rnn-综述.md"]
wiki_type: topics
topic: "深度学习"
migrated_from: "05_深度学习/rnn/rnn-综述.md"
review_status: structural
---

> 所属 Topic：[深度学习](../%E6%B7%B1%E5%BA%A6%E5%AD%A6%E4%B9%A0.md) · 类型：专题资料

# 【综述】

为了处理序列数据，rnn引入了隐藏状态hidden state的概念。如下图所示

![-w705](../../media/15837577303219/15837580278747.jpg)

说明: x1,x2,...代表时间序列上不同时刻的向量，在x1时刻，当前的隐状态h0和当前的输入x1，进行叠加得到了新的隐状态h1.以此类推。

而最终输出就是在隐状态h的基础上再进行一次计算。最终输出如下。这样就完成了序列输入(x1,x2,....xn),输出(y1, y2 ....yn)的过程

![-w722](../../media/15837577303219/15837582220421.jpg)

实际中按照输入和输出的变量个数可以有如下的一些情形：

* N vs 1
* 




## 参考
https://zhuanlan.zhihu.com/p/28054589