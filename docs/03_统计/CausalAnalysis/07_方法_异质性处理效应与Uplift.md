---
title: 方法_异质性处理效应与Uplift
update_time: "2026-09-13 21:51:07 CST"
tags:
  - statistics/causal-inference
  - causal-method
  - uplift
---

# 07. 方法：异质性处理效应与 Uplift

平均效果回答的是：整体有没有增量。异质性处理效应回答的是：

> 哪些人被处理后增量更大？哪些人没有增量，甚至负向？

## 1. 核心概念

| 概念 | 含义 |
|---|---|
| ITE | 单个个体的处理效应 |
| CATE | 给定特征后的平均处理效应 |
| Uplift | treatment 相比 no treatment 的增量响应 |

Uplift 的典型形式：

$$
lift(x) = E[Y|T=1, X=x] - E[Y|T=0, X=x]
$$

## 2. 适用场景

- 营销、广告、推送、权益发放；
- 不是所有用户都值得触达；
- 平均效果不显著，但怀疑某些人群有效；
- 需要把策略资源分配给增量最高的人群。

## 3. 常见建模方式

| 方法 | 直觉 |
|---|---|
| S-learner | 一个模型同时输入 $X$ 和 $T$ |
| T-learner | treatment 和 control 各训练一个模型，再相减 |
| X-learner | 先估计伪 treatment effect，再建模异质性 |
| DR learner | 结合倾向得分和结果模型，做双重稳健估计 |
| Uplift tree | 直接按增量差异做树分裂 |

## 4. 评估指标

常见评估：

- Qini curve；
- uplift curve；
- 分桶后 treatment-control 差异；
- top-k 人群增量收益；
- 策略收益模拟。

Qini 的一个常见表达是：

$$
\mathrm{Qini}=\frac{n_{t, 1}(\phi)}{N_{t}}-\frac{n_{c, 1}(\phi)}{N_{c}}
$$

其中 $n_{t,1}$ 和 $n_{c,1}$ 分别表示排序到某个比例 $\phi$ 时，实验组和对照组中 outcome 为 1 的人数。

## 5. 注意事项

- Uplift 模型最好基于随机实验或可信准实验数据训练；
- 如果 treatment 本身有强选择偏差，直接训练 uplift 会学到偏差；
- 不要只看响应率，要看增量响应；
- 需要区分“本来就会转化的人”和“被触达后才转化的人”。

## 6. 相关旧文档

- [uplift](07_方法_异质性处理效应与Uplift.md)
- [工具-econML&causalML](工具/08_工具_EconML与CausalML.md)


---

<!-- migrated-from: 07_方法_异质性处理效应与Uplift.md -->

## 旧笔记整合：Uplift 原始笔记

> 迁移说明：保留原问题定义、Qini 指标和 Excalidraw 引用。

Uplift models用于预测一个treatment的增量反馈价值。
举个例子来说，假如我们想知道对一个用户展现一个广告的价值，通常的模型只能告诉我们用户在展示广告后的购买意愿很强，但事实很有可能是他们在被展示广告之前就已经很想购买了。Uplift models聚焦于用户被展示广告后购买意愿的增量。

## 1. 问题定义
即回答如下的问题
$$lift = P(y|treatment) - P(y|no treatment)$$

而一般我们的建模是预测
$$outcome = P(y|treatment)$$

![|200](https://pic1.zhimg.com/v2-5eca5d508effd41f7569f3923b74f2b4_b.jpg)


但是在现实生活中，对于单个人，不存在这样的反事实。即既受到treatment也受到not treated的应用。

## 2. 方法
1. 分别对实验组和对照组建模，然后求差值。


根据定义，有
$lift = E(y|t) - E(y|c)$
 ![[../../../附件/Excalidraw/uplift 2022-05-26 21.32.29.excalidraw.md]]


## 3. 评估
比较典型的评估指标是Qini curve

$$\mathrm{Qini}=\frac{n_{t, 1}(\phi)}{N_{t}}-\frac{n_{c, 1}(\phi)}{N_{c}}$$

其中nt1和nc1分别表示实验组和对照组中outcome为1的人数
