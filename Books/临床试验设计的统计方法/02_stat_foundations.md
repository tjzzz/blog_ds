# 第 02 篇　统计基础：频率学派与贝叶斯方法

> 对应原书第 3 章。本篇不是统计学入门，而是为后续各篇准备**临床试验设计所需的统计工具箱**，并突出两个学派的差异。

## 学习目标

- 回顾极大似然、置信区间、假设检验、GLM、随机效应模型；
- 掌握生存分析三件套：Kaplan–Meier、log-rank、Cox 比例风险模型；
- 掌握贝叶斯推断：先验、后验、共轭先验、可信区间、Bayes 因子、模型平均、层次模型、决策论；
- 理解**后验预测分布**——后面 II 期“预测概率监测”的基础；
- 了解 MCMC（逆变换、拒绝抽样、Gibbs、Metropolis–Hastings）。

---

## 1. 两种统计哲学的核心差异

| 维度 | 频率学派 | 贝叶斯 |
|:---|:---|:---|
| 参数 $\theta$ | **未知常数** | **随机变量**，有分布 |
| 概率的含义 | 长期频率 | 信念/不确定性的度量 |
| 推断依据 | 抽样分布（假想的重复试验） | 后验分布 $\pi(\theta\mid D)$ |
| 先验信息 | 不直接使用 | 通过先验分布显式纳入 |
| 区间 | 置信区间：区间随机，参数固定 | 可信区间：参数随机，区间固定 |
| 假设检验 | $p$ 值、控制 I/II 类错误 | 后验概率、Bayes 因子 |
| 顺序/中期分析 | 需要 **α 消耗** 修正 | 后验自然更新，似然原则 |
| 典型应用（本书） | III 期、样本量计算 | I、II 期、自适应随机化 |

> 实践上，**贝叶斯设计也常通过模拟校准**，使其具有良好的频率学派性质（如 I 类错误率、检验效能）。这是目前监管认可的“贝叶斯设计，频率学派评价”的常见做法。

---

## 2. 基础概率

### 2.1 常用分布（与本书强相关）

| 分布 | 用途 |
|:---|:---|
| $\mathrm{Bernoulli}(p)$、$\mathrm{Bin}(n,p)$ | 二分类反应、DLT 计数 |
| $\mathrm{Beta}(a,b)$ | 概率的先验/后验（二项的共轭先验） |
| Beta–二项分布 | 未来响应数的预测分布 |
| Normal、$t$、$\chi^2$ | 连续终点、检验统计量 |
| Exponential、Weibull | 生存时间 |
| Dirichlet、Multinomial | 多分类结局（如毒性×疗效的 4 种组合） |

**Beta 分布**：$p\sim\mathrm{Beta}(a,b)$ 的密度

$$
f(p;a,b)=\frac{\Gamma(a+b)}{\Gamma(a)\Gamma(b)}p^{a-1}(1-p)^{b-1},\quad
E(p)=\frac{a}{a+b},\quad
\mathrm{Var}(p)=\frac{ab}{(a+b)^2(a+b+1)}.
$$

$a+b$ 可理解为先验的**“等效样本量”**（prior effective sample size）。

### 2.2 多元分布与 Copula

- 联合分布、条件分布、相关性；
- **Copula**：把边缘分布与相依结构分开建模，$F(x,y)=C\{F_X(x),F_Y(y)\}$（第 09 篇联合用药的 Clayton 型模型受其启发）。

### 2.3 随机变量的收敛

- 依概率收敛、依分布收敛、几乎处处收敛；
- 大数定律、中心极限定理（CLT）—— 样本量公式与正态近似的基础；
- Delta 方法、Slutsky 定理。

---

## 3. 频率学派方法

### 3.1 极大似然估计（MLE）

$$
\hat\theta=\arg\max_\theta L(\theta\mid D)=\arg\max_\theta\sum_i\log f(y_i;\theta).
$$

大样本下 $\hat\theta\ \dot\sim\ N\{\theta,\ I(\theta)^{-1}\}$，其中 Fisher 信息 $I(\theta)=-E\,\partial^2\ell/\partial\theta^2$。

### 3.2 矩估计与广义矩估计（GMM）

- **矩估计**：令样本矩 = 总体矩，解方程；
- **GMM**：矩条件 $E\{g(Y;\theta)\}=0$ 多于参数时，最小化加权二次型
  $$\hat\theta=\arg\min_\theta\ \bar g(\theta)^\top W\,\bar g(\theta).$$

### 3.3 置信区间

$100(1-\alpha)\%$ 置信区间 $[L(Y),U(Y)]$ 满足 $\Pr\{L(Y)\le\theta\le U(Y)\}=1-\alpha$。
对大样本的 MLE：$\hat\theta\pm z_{\alpha/2}\,\widehat{\mathrm{se}}(\hat\theta)$。

> **误读警示**：“该区间以 95% 概率含真值”是对**可信区间**的解释，不是置信区间；置信区间的 95% 指**程序**的长期覆盖率。

### 3.4 假设检验

- 设定 $H_0$ 与 $H_1$；
- **第 I 类错误**：$\alpha=\Pr(\text{拒绝 }H_0\mid H_0\text{ 真})$；
- **第 II 类错误**：$\beta=\Pr(\text{接受 }H_0\mid H_1\text{ 真})$；**效能** $=1-\beta$；
- **$p$ 值**：在 $H_0$ 下，观察到至少与实际统计量同样极端的概率。

常见检验：Wald、似然比（LRT）、Score；对二项比例用精确二项检验或正态近似。

### 3.5 广义线性模型（GLM）与拟似然

$$
g\{E(Y_i)\}=x_i^\top\beta,\quad \mathrm{Var}(Y_i)=\phi\,V\{E(Y_i)\}.
$$

- 连续：恒等链接；二分类：logit 链接；计数：log 链接；
- **拟似然（quasi-likelihood）**只需指定均值与方差函数；相关数据可用 **GEE**（第 05 篇样本量相关数据会用到）。

### 3.6 随机效应模型

$$
y_{ij}=x_{ij}^\top\beta+b_i+\varepsilon_{ij},\quad b_i\sim N(0,\sigma_b^2),\ \varepsilon_{ij}\sim N(0,\sigma^2).
$$

患者内相关性的来源；ATD 设计（第 03 篇）与多中心试验都会用到。

---

## 4. 生存分析

### 4.1 基本量

设 $T$ 为事件时间，则

- 生存函数 $S(t)=\Pr(T>t)$；
- 风险函数（瞬时风险）$h(t)=\lim_{\Delta\to0}\Pr(t\le T<t+\Delta\mid T\ge t)/\Delta$；
- 累积风险 $H(t)=\int_0^t h(u)\,du$，$S(t)=\exp\{-H(t)\}$。

**指数分布**：$h(t)=\lambda$，$S(t)=e^{-\lambda t}$，中位生存时间 $=\ln2/\lambda$。

**删失（censoring）**：只观察到 $\min(T,C)$ 及事件指示 $\delta=I(T\le C)$。

### 4.2 Kaplan–Meier 估计

设不同事件时间 $t_{(1)}<\dots<t_{(m)}$，在 $t_{(i)}$ 的**风险集人数**为 $n_i$，**事件数**为 $d_i$：

$$
\hat S(t)=\prod_{t_{(i)}\le t}\Big(1-\frac{d_i}{n_i}\Big).
$$

方差由 **Greenwood 公式**：$\widehat{\mathrm{Var}}\{\hat S(t)\}=\hat S(t)^2\sum_{t_{(i)}\le t}\frac{d_i}{n_i(n_i-d_i)}$。

> **自一致性（self-consistency）**：KM 可视为把删失观测的概率质量“向右重新分配”——这一思想在第 08 篇（分数 3+3、fCRM）中被借用来处理延迟毒性。

### 4.3 Log-rank 检验

比较两组生存曲线。在每个事件时间 $t_{(i)}$ 构造 $2\times2$ 表，统计量

$$
Z=\frac{\sum_i\big(d_{1i}-E_{1i}\big)}{\sqrt{\sum_i V_i}},\quad E_{1i}=d_i\frac{n_{1i}}{n_i},
$$

$V_i$ 为超几何方差。$Z\sim N(0,1)$（渐近）。对**比例风险**备择最有效。

### 4.4 Cox 比例风险模型

$$
h(t\mid x)=h_0(t)\exp(\beta^\top x).
$$

- $\exp(\beta_j)$ 为**风险比（HR）**；
- 通过**偏似然**估计 $\beta$，不需要指定 $h_0(t)$：
  $$
  L_p(\beta)=\prod_{i:\delta_i=1}\frac{\exp(\beta^\top x_i)}{\sum_{k\in R(t_i)}\exp(\beta^\top x_k)}.
  $$
- 两样本情形下，log-rank 检验等价于 Cox 模型中 Score 检验。

### 4.5 治愈率模型（Cure Rate Model）

当一部分患者永不发生事件时：

$$
S(t)=\pi+(1-\pi)\,S_u(t),
$$

$\pi$ 为“治愈比例”，$S_u$ 为未治愈者的生存函数。生存曲线会收敛到非零平台。

---

## 5. 贝叶斯方法

### 5.1 Bayes 定理

$$
\pi(\theta\mid D)=\frac{L(D\mid\theta)\,\pi(\theta)}{\int L(D\mid\theta)\pi(\theta)\,d\theta}\ \propto\ \text{似然}\times\text{先验}.
$$

### 5.2 先验的获取（prior elicitation）

- **无信息/模糊先验**：如 $\mathrm{Beta}(1,1)$，或大方差正态；
- **信息性先验**：来自历史数据、专家意见；
- **折扣历史数据**：保持先验均值不变，但扩大方差，减小等效样本量（II 期设计中常用）。
  例：历史上 40 人中 8 人有效，先验均值 $0.2$；取 $\mathrm{Beta}(4,16)$ 相当于只相信 20 人的信息。

### 5.3 共轭先验：Beta–二项（本书的主力）

若 $p\sim\mathrm{Beta}(a,b)$，$Y\mid p\sim\mathrm{Bin}(n,p)$，观察到 $Y=y$，则

$$
p\mid y\sim\mathrm{Beta}(a+y,\ b+n-y),\qquad E(p\mid y)=\frac{a+y}{a+b+n}.
$$

后验均值是先验均值与样本频率的**加权平均**：

$$
E(p\mid y)=\underbrace{\frac{a+b}{a+b+n}}_{\text{先验权重}}\cdot\frac{a}{a+b}+\underbrace{\frac{n}{a+b+n}}_{\text{数据权重}}\cdot\frac{y}{n}.
$$

其他共轭对：Normal–Normal、Gamma–Poisson、Dirichlet–Multinomial（多分类）。

### 5.4 可信区间

- **等尾可信区间**：后验 $\alpha/2$ 与 $1-\alpha/2$ 分位数；
- **最高后验密度（HPD）区间**：包含 $1-\alpha$ 后验概率的最短区间。

### 5.5 Bayes 因子与 Jeffreys 标度

对 $H_i$ 与 $H_k$：

$$
\mathrm{BF}_{ik}=\frac{P(D\mid H_i)}{P(D\mid H_k)},\qquad
\text{后验几率}=\mathrm{BF}\times\text{先验几率}.
$$

**Jeffreys 标度**（以 $\log_{10}\mathrm{BF}_{ik}$ 计）：

| $\log_{10}\mathrm{BF}$ | 证据 |
|:---:|:---|
| $0\sim 1/2$ | 几乎不值一提 |
| $1/2\sim 1$ | 实质性（substantial） |
| $1\sim 2$ | 强 |
| $>2$ | 决定性 |

> 例：三个先验概率相等的假设，若 $\mathrm{BF}_{1,2}=\mathrm{BF}_{1,3}=10^{1/2}$，则 $P(H_1\mid D)=1/(1+2\times10^{-1/2})\approx0.61$。这就是第 03 篇“贝叶斯混合设计”中 **0.61 阈值**的来源。

### 5.6 贝叶斯模型平均（BMA）

模型不确定时，不选单一模型，而用后验模型概率加权：

$$
E(\theta\mid D)=\sum_{k=1}^K E(\theta\mid M_k,D)\,P(M_k\mid D),\qquad
P(M_k\mid D)=\frac{P(D\mid M_k)P(M_k)}{\sum_l P(D\mid M_l)P(M_l)}.
$$

数据支持得越好的模型权重越大 → 自动稳健（BMA-CRM 的核心，见第 03 篇）。

### 5.7 贝叶斯层次模型

$$
y_{g}\mid\theta_g\sim f(\cdot\mid\theta_g),\quad\theta_g\mid\mu,\tau^2\sim N(\mu,\tau^2),\quad(\mu,\tau^2)\sim\text{超先验}.
$$

**“部分合并”（partial pooling）**：各亚组估计向总体均值**收缩**（shrinkage），在小样本亚组中借用信息 → BATTLE 试验就用此思想。

### 5.8 决策论

选择决策 $a$ 使**后验期望损失**最小：

$$
a^*=\arg\min_a\int L(a,\theta)\,\pi(\theta\mid D)\,d\theta.
$$

- 平方损失 → 后验均值；
- 绝对损失 → 后验中位数；
- 非对称损失（EWOC，第 03 篇）→ 后验分位数。

### 5.9 后验预测分布

对未来数据 $\tilde Y$：

$$
p(\tilde y\mid D)=\int p(\tilde y\mid\theta)\,\pi(\theta\mid D)\,d\theta.
$$

**Beta–二项预测**：若 $p\mid y\sim\mathrm{Beta}(a+y,b+n-y)$，未来 $N-n$ 人中有效数 $X$ 满足

$$
P(X=x\mid y)=\binom{N-n}{x}\frac{B(a+y+x,\ b+N-y-x)}{B(a+y,\ b+n-y)},\quad B(u,v)=\frac{\Gamma(u)\Gamma(v)}{\Gamma(u+v)}.
$$

> **频率学派的预测**是在某个固定参数值下算未来数据的概率；**贝叶斯预测**对参数不确定性取平均。

---

## 6. 马尔可夫链蒙特卡罗（MCMC）

当后验没有闭式时需要抽样：

| 方法 | 思路 |
|:---|:---|
| **逆变换抽样** | $U\sim U(0,1)$，$X=F^{-1}(U)$ |
| **拒绝抽样** | 找提议分布 $g$ 与常数 $M$ 使 $f\le Mg$；以概率 $f(x)/\{Mg(x)\}$ 接受 |
| **Gibbs 抽样** | 依次从各参数的**全条件分布**抽样 |
| **Metropolis–Hastings** | 从提议 $q(\theta^*\mid\theta)$ 抽候选，以概率 $\min\Big\{1,\dfrac{\pi(\theta^*)q(\theta\mid\theta^*)}{\pi(\theta)q(\theta^*\mid\theta)}\Big\}$ 接受 |

实用注意：燃烧期（burn-in）、收敛诊断、自相关与有效样本量。

---

## 要点回顾

1. 贝叶斯的“后验 = 似然 × 先验”，Beta–二项共轭是早期试验设计的**核心计算引擎**。
2. 后验预测分布 → 预测概率监测（第 04 篇）。
3. Bayes 因子 + Jeffreys 标度 → 决策阈值（如 0.61）。
4. BMA 让设计对模型设定更稳健；层次模型实现跨亚组借用。
5. 生存分析：KM → log-rank → Cox；KM 的自一致性思想用于延迟毒性处理。

## 思考题

1. 先验 $\mathrm{Beta}(0.4,1.6)$ 的等效样本量和先验均值各是多少？数据 $y=3,n=10$ 后后验均值是多少？
2. 为什么中期监测在频率学派需要调整 $\alpha$，而贝叶斯“似然原则”下似乎不需要？这对监管意味着什么？
3. 推导 Beta–二项预测分布，并说明为何 $N$ 不同时预测概率会不同。
