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
 ![[../../../Excalidraw/uplift 2022-05-26 21.32.29.excalidraw]]


## 3. 评估
比较典型的评估指标是Qini curve

$$\mathrm{Qini}=\frac{n_{t, 1}(\phi)}{N_{t}}-\frac{n_{c, 1}(\phi)}{N_{c}}$$

其中nt1和nc1分别表示实验组和对照组中outcome为1的人数


