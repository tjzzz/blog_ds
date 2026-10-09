---
title: "特征处理—特征选择"
created: 2026-10-09
updated: 2026-10-09
tags: [llm-wiki, migrated]
source: ["Input/rebuild_source_2026-10-09/04_机器学习/Features&Data/特征处理—特征选择.md"]
wiki_type: concepts
topic: "机器学习"
migrated_from: "04_机器学习/Features&Data/特征处理—特征选择.md"
review_status: structural
---

> 所属 Topic：[机器学习](../../topics/%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0.md) · 类型：概念

# 特征处理—特征选择

## 1. 简单筛选方法
比如单变量的特征选择，可以通过相关系数等

## 2. 基于学习模型的特征排序

- 回归模型的系数
- 正则化模型lasso/岭回归
- 随机森林
- 决策树



### 基于IV值
> 适用：有监督、二分类

IV值即information value，用来表示特征对目标预测的贡献程度。

IV值的计算是以 WOE 编码（来源：私有原始笔记 `Input/9专题-商业化/银行-评分卡模型.md#WOE编码`）值为基础的，

$$IV_i = (\frac{bad_i}{bad_T} -\frac{good_i}{good_T})*WOE_i$$
$$IV = \sum_1^n IV_i$$
IV值的计算是对WOE值的加权和，是用来衡量WOE表示的变量对二分类变量之间关系的强度。


其中$WOE_i = log(\frac{bad_i}{bad_T} /\frac{good_i}{good_T})$
所以可以看到其实是两个熵$IV = \sum p_ilog(p_i) - q_ilog(q_i)$


一般地
V值取值含义：
（1）IV<0.02：无用特征
（2）0.02<IV<0.1：弱价值特征
（3）0.1<IV<0.3：中价值特征
（4）0.3<IV<0.5：强价值特征
（5）IV>0.5：价值过高，不真实


### stepwise的变量选择
- 前向
- 后向
- 逐步


### 基于模型特征重要性的方式
决策树，gbdt，xgb。。。


## 参考
https://blog.csdn.net/kebu12345678/article/details/78437118
https://zhuanlan.zhihu.com/p/36539125

