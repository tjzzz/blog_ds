---
title: 方法_异质性处理效应与Uplift
update_time: "2026-09-14 10:17:38 CST"
tags:
  - statistics/causal-inference
  - causal-method
  - uplift
---
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

### 3.1 数据长什么样

Uplift 建模需要同时有 treatment 和 control 两类样本。最基本的数据结构是：

| user_id | T 是否触达 | Y 是否转化/收益 | X 用户特征 |
|---|---:|---:|---|
| u1 | 1 | 1 | 活跃度、历史付费、国家、渠道、设备等 |
| u2 | 1 | 0 | 活跃度、历史付费、国家、渠道、设备等 |
| u3 | 0 | 1 | 活跃度、历史付费、国家、渠道、设备等 |
| u4 | 0 | 0 | 活跃度、历史付费、国家、渠道、设备等 |

其中：

- `T=1`：用户接受 treatment，例如看到广告、收到优惠券、被推送；
- `T=0`：用户没有接受 treatment；
- `Y`：结果变量，可以是是否转化、收入、留存、点击等；
- `X`：treatment 之前已经存在的用户特征，不能使用 treatment 之后才产生的变量。

最终目标不是预测：

```text
P(Y=1 | T=1, X)
```

而是估计：

```text
uplift(X) = E[Y | T=1, X] - E[Y | T=0, X]
```

也就是同一类用户被触达和不被触达之间的增量差异。

### 3.2 S-learner：一个模型同时输入 X 和 T

S-learner 把实验组和对照组数据合并，只训练一个模型：

$$
Y = f(X, T)
$$

预测时，同一个用户特征 $X=x$ 要预测两次：

```text
预测接受 treatment 的结果：y1 = f(x, T=1)
预测不接受 treatment 的结果：y0 = f(x, T=0)
uplift(x) = y1 - y0
```

如果用线性模型，为了让不同人群有不同 uplift，通常要加入交互项：

$$
Y_i = \beta_0 + \beta_T T_i + \beta_X X_i + \theta (T_i \times X_i) + \epsilon_i
$$

如果只有一个特征 $X$，那么：

$$
uplift(x) = \beta_T + \theta x
$$

如果有多个特征 $X_1, X_2, ..., X_p$，则可以写成：

$$
uplift(x) = \beta_T + \sum_j \theta_j x_j
$$

这里：

- $\beta_T$：平均 treatment 效果；
- $\theta_j$：第 $j$ 个特征如何改变 treatment 效果；
- $\theta_j > 0$：这个特征越高，treatment 增量越大；
- $\theta_j < 0$：这个特征越高，treatment 增量越小。

如果 $Y$ 是二分类，比如是否转化，可以用逻辑回归或树模型。注意此时不要直接把 logit 系数当 uplift，最好用预测概率差：

```text
uplift(x) = P_hat(Y=1 | T=1, X=x) - P_hat(Y=1 | T=0, X=x)
```

### 3.3 T-learner：实验组和对照组各建一个模型

T-learner 分别训练两个模型：

$$
m_1(x)=E[Y|T=1,X=x]
$$

$$
m_0(x)=E[Y|T=0,X=x]
$$

然后计算：

$$
\hat\tau(x)=m_1(x)-m_0(x)
$$

具体步骤：

1. 用 treatment 样本训练模型 $m_1(x)$；
2. 用 control 样本训练模型 $m_0(x)$；
3. 对每个用户分别预测 $m_1(x)$ 和 $m_0(x)$；
4. 两个预测结果相减，得到该用户的 uplift。

T-learner 的优点是直观，适合 treatment 和 control 数据量都比较充足的场景；缺点是两个模型分别训练，可能带来模型误差不稳定。

### 3.4 X-learner：先构造伪 treatment effect

X-learner 更适合 treatment 和 control 样本量不均衡的场景。

基本步骤：

1. 先训练两个结果模型：$m_1(x)$ 和 $m_0(x)$；
2. 对 treatment 样本，构造伪效应：

$$
D_i^1 = Y_i - m_0(X_i)
$$

3. 对 control 样本，构造伪效应：

$$
D_i^0 = m_1(X_i) - Y_i
$$

4. 再用 $X$ 去预测这些伪效应，得到不同人群的 uplift。

直觉是：

```text
先用模型补出每个样本缺失的反事实结果，再建模个体增量差异。
```

### 3.5 DR learner：倾向得分 + 结果模型

DR learner 会同时使用：

- 倾向得分模型：$e(x)=P(T=1|X=x)$；
- treatment 结果模型：$m_1(x)$；
- control 结果模型：$m_0(x)$。

它会构造一个双重稳健的伪 outcome：

$$
\phi_i = m_1(X_i)-m_0(X_i) + \frac{T_i(Y_i-m_1(X_i))}{e(X_i)} - \frac{(1-T_i)(Y_i-m_0(X_i))}{1-e(X_i)}
$$

然后再用 $X$ 去预测 $\phi_i$，得到 CATE / uplift。

它的好处是：如果倾向得分模型和结果模型中有一个设得比较准，估计仍然相对稳健。

### 3.6 Uplift tree：按增量差异切分人群

Uplift tree 不直接预测结果，而是寻找能让 treatment-control 差异最大的人群切分。

例如：

```text
历史付费高 + 最近活跃高：触达后增量大
历史付费低 + 最近流失：触达后增量小
```

它适合做策略分层解释，但通常需要足够大的实验样本，否则树的切分容易不稳定。

### 3.7 方法对比

| 方法 | 怎么用数据 | 怎么得到 uplift | 适用场景 |
|---|---|---|---|
| S-learner | 实验组和对照组合并，T 作为特征 | 同一个用户分别设 T=1 和 T=0 预测，结果相减 | 简单基线，样本较少时可用 |
| T-learner | T=1 和 T=0 分开建模 | 两个模型预测值相减 | 两组样本都充足 |
| X-learner | 先补反事实，再预测伪效应 | 用伪 treatment effect 建模 | treatment/control 不均衡 |
| DR learner | 倾向得分 + 结果模型 | 构造双重稳健伪 outcome 后建模 | 观察性数据或存在选择偏差 |
| Uplift tree | 按 treatment-control 差异切分 | 每个叶子节点内算增量 | 需要可解释分群 |

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

- 原 uplift 旧文档内容已合并到本篇
- [工具_EconML与CausalML](08_工具_EconML与CausalML.md)


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

