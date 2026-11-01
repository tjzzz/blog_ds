---
title: STATE：面向长尾指标的稳健 ATE 估计（Student-t + 变分 EM）
created: 2026-10-21
updated: 2026-10-21
tags: [llm-wiki, ab-test, STATE, variance-reduction, heavy-tailed, robust-estimation, causal-inference]
source:
  - "Zhou et al. (2024), STATE, KDD 2024"
  - "Liu & Rubin (1995), ECM / scale mixture of t"
  - "Budylin et al. (2018), ratio metrics in A/B"
wiki_type: methods
topic: "实验设计与AB测试"
review_status: reviewed
---

> 所属 Topic：[实验设计与AB测试](../index.md) · 子专题：[灵敏度与提效](index.md) · 类型：方法
>
> CUPED 基础见 [CUPED](CUPED.md)；CUPAC / MLRATE / STATE 的选型与关系见 [CUPED 变体](CUPED变体.md)。
> 本文聚焦 STATE 的机制、证据边界与落地判断，不重复 CUPED 基础推导。

# STATE：面向长尾指标的稳健 ATE 估计

## 1. 问题：高斯假设下的方差缩减，为何在长尾指标上失灵

经典方差缩减（CUPED、CUPAC、MLRATE）的回归调整，隐含一个未被言明的假设：**结果残差近似高斯分布**。但对 GMV、订单金额、停留时长、收入这类业务指标，真实分布往往是**重尾（heavy-tailed）**的——少数极端用户/订单把方差撑得极大。

重尾带来两个连锁问题：

1. **方差被极端值主导**：高斯似然下，每个样本权重固定为 1，平方损失对极端值极敏感，估计被少数离群点拉偏。
2. **协变量与结果的相关性被削弱**：离群点同时破坏「预处理特征 $X$ ↔ 实验期结果 $Y$」的样本内相关性，而方差缩减的收益正来自这个相关性（见 [CUPED 变体](CUPED变体.md) 第 3.1 节）。相关性一弱，CUPAC/MLRATE 也救不回来。

STATE（**S**tudent's **t**-distribution **A**TE es**t**imator）的核心思路：**不改变 CUPAC 那条「用 ML 预测分做协变量」的路线，只把回归的误差分布从高斯换成 Student-t，并用变分 EM 自动给离群点降权。** 它是对 CUPAC 的稳健化扩展，而不是另起炉灶的新范式。

## 2. 关键结论 / 心智模型

- STATE = **CUPAC 机制 + Student-t 稳健似然 + 变分 EM**。协变量部分与 CUPAC 完全相同（ML 预测分作为回归量），区别在于对残差建模。
- 鲁棒性不来自「更聪明的模型」，而来自 **Student-t 的尺度混合表示**：每个样本有一个潜变量精度 $\eta_i$，离群点的 $\eta_i$ 被自动压到接近 0，等于被「软删除」而非硬截断。
- 它**不改变 estimand**：计数的 ATE 仍是 ITT 算术平均处理效应 $\tau_c=E[Y(1)]-E[Y(0)]$。比率指标通过线性变换保无偏，见第 6 节。
- 收益是**条件性的**：只有指标确实重尾时 STATE 明显优于 CUPAC/MLRATE；指标近似高斯时 STATE 与之持平却多花 EM 计算。

## 3. 概念、术语与 estimand

| 符号 | 含义 |
|---|---|
| $Y_i$ | 第 $i$ 个单位的实验期结果（计数或比率分子） |
| $T_i\in\{0,1\}$ | 处理分配（随机化变量） |
| $X_i$ | 处理前特征（必须不受处理影响） |
| $\hat Y_i$ | ML 模型对 $E[Y\mid X]$ 的**样本外**预测（CUPAC 式代理） |
| $\epsilon_i$ | 回归残差，STATE 假设 $\epsilon_i\sim S_t(0,\sigma^2,\nu)$ |
| $\nu$ | Student-t 自由度，越小尾部越重 |
| $\eta_i$ | 潜变量精度缩放因子，$\eta_i\sim\text{Gamma}(\nu/2,\nu/2)$ |
| $\tau_c$ | 计数指标 ATE：$\tau_c=E[Y(1)]-E[Y(0)]$ |
| $\tau_r$ | 比率指标 ATE：$\tau_r=\frac{E[Y(1)]}{E[Z(1)]}-\frac{E[Y(0)]}{E[Z(0)]}$ |

**estimand 锁定**：STATE 论文（Zhou et al., 2024）明确把计数 ATE 定义为对照组与处理组的期望差，ATE 估计量即回归系数 $a_1$ 的极大似然估计。比率指标在线性变换后仍以证明方式保持对同一 $\tau_r$ 的无偏（第 6 节）。

## 4. 方法机制

### 4.1 两阶段：ML 代理 + Student-t 回归（与 CUPAC 的关系）

**阶段一（ML 代理，等同 CUPAC）**：训练模型 $g(X)$ 预测 $E[Y\mid X]$，用 **cross-fitting**（分折训练、在未参与训练的样本上生成预测）得到代理 $\hat Y_i$，保证 $\hat Y_i\perp T_i$，从而调整不引入偏差。这一步与 CUPAC / MLRATE 完全一致。

> **关系澄清：多协变量回归调整是 CUPAC 的特例。** 如果把「阶段一的预测模型」取为线性、且直接把原始预处理特征放进回归，CUPAC 就退化成多协变量回归调整。CUPAC 的泛化，是用模型学出的单一预测分 $\hat Y_i$ 替代多个原始协变量，可非线性、高维、避免共线/缺失治理。STATE 站在 CUPAC 这一层之上——它复用 $\hat Y_i$，只改残差分布。

**阶段二（稳健回归）**：把 $\hat Y_i$ 作为回归量，但残差改用 Student-t：

$$
Y_i = a_0 + a_1 T_i + a_2 \hat Y_i + \epsilon_i,\qquad \epsilon_i \sim S_t(\epsilon\mid 0,\sigma^2,\nu)
$$

ATE 估计 = 系数 $a_1$ 的 MLE。

### 4.2 Student-t 的尺度混合表示

Student-t 可写成「高斯 + 精度上的 Gamma」的尺度混合（Liu & Rubin, 1995），这是 STATE 能跑 EM 的关键：

$$
\epsilon_i \mid \eta_i \sim \mathcal{N}\!\left(0,\frac{\sigma^2}{\eta_i}\right),\qquad
\eta_i \sim \mathcal{G}\!\left(\frac{\nu}{2},\frac{\nu}{2}\right)
$$

其中 $\mathcal{G}(\eta\mid a,b)=\frac{b^a}{\Gamma(a)}\eta^{a-1}e^{-b\eta}$ 为 Gamma 密度。边缘积分后得到自由度为 $\nu$ 的 Student-t。$\eta_i$ 是「第 $i$ 个样本的精度缩放」，方差被缩放为 $\sigma^2/\eta_i$——离群点会对应极小的 $\eta_i$，从而极大方差、极小权重。

### 4.3 变分 EM：目标、E-step、M-step

直接优化 $\sum_i \ln S_t(Y_i\mid a^\top x_i,\sigma^2,\nu)$ 无解析解。STATE 用 Jensen 不等式构造证据下界 **ELBO / 变分自由能 $\mathcal{F}$**，对潜变量 $\eta_i$ 做变分推断并交替优化：

- **E-step**（固定参数，优化变分后验）：
  $$
  q(\eta_i)=\mathcal{G}(\eta_i\mid \xi_i,\zeta_i),\quad
  \xi_i=\frac{\nu}{2}+\frac12,\quad
  \zeta_i=\frac{\nu}{2}+\frac{(Y_i-a^\top x_i)^2}{2\sigma^2},\quad
  \langle\eta_i\rangle=\frac{\xi_i}{\zeta_i}
  $$

- **M-step**（固定变分后验，更新参数）代表性更新：
  $$
  a_1=\frac{\sum_i (Y_i-a_0-a_2\hat Y_i)\,T_i\,\langle\eta_i\rangle}{\sum_i \langle\eta_i\rangle\,T_i^2},\qquad
  \sigma^2=\frac1N\sum_i (Y_i-a_0-a_1T_i-a_2\hat Y_i)^2\,\langle\eta_i\rangle
  $$
  自由度 $\nu$ 由对应非线性方程解出。迭代至收敛。

### 4.4 异常值如何被自动降权（鲁棒性核心）

看 E-step 的 $\zeta_i$：它正比于**残差平方** $(Y_i-a^\top x_i)^2$。

- 正常点：残差小 → $\zeta_i$ 小 → $\langle\eta_i\rangle$ 接近 1 → 权重正常。
- 离群点：残差极大 → $\zeta_i$ 极大 → $\langle\eta_i\rangle=\xi_i/\zeta_i$ **趋近 0**。

而 M-step 里 $a_1,\sigma^2$ 等所有更新都以 $\langle\eta_i\rangle$ 作为权重。于是离群点因 $\eta_i\to0$ 被自动赋予近零权重——这是「软降权」，不是 winsorize 那种硬截断，也不需要人工选阈值。这就是 Student-t 鲁棒性的全部机制。

### 4.5 ATE 估计 = $a_1$ 的 MLE

论文明确写道：ATE 估计就是基于上述两式的 $a_1$ 极大似然估计。在随机化实验、$T\perp X$、交叉拟合保证 $\hat Y_i\perp T_i$ 的前提下，该估计对 $\tau_c$ 保持无偏，同时因离群降权显著降低方差。

## 5. 最小示意例子（示意，非真实数据）

设某计数指标（如下单数）残差近似 $t_3$（自由度 3，明显重尾）。对照组与处理组各 1000 人，真实 ATE=2。

- 高斯回归：1 个极端用户（如下单 5000 的异常值）会把斜率估计拉偏数倍，方差被它主导。
- STATE：该异常点残差大 → $\zeta_i$ 大 → $\langle\eta_i\rangle\approx0$ → 在 $a_1$ 更新中权重趋零，估计基本不被它影响。

要点：STATE 不改变点估计的中心（无偏），改变的是**估计的稳定性**——同样样本下标准误更小、更易显著。示意仅用于建立直觉，真实收益取决于指标实际重尾程度。

## 6. 比率指标扩展：线性变换保无偏

比率指标 $\tau_r=\frac{E[Y(1)]}{E[Z(1)]}-\frac{E[Y(0)]}{E[Z(0)]}$（如客单价 = GMV / 订单数）更难，因为**分析单位（分母 $Z$）≠ 随机化单位**，普通回归调整与稳健估计不能直接套用。

STATE 的做法（论文第 4 节）：构造新标签

$$
P_i=\kappa_1 Y_i-\kappa_2 Z_i,\qquad \text{取 } \kappa_1=Z_c,\ \kappa_2=Y_c
$$

则 $\Delta P = Y_t Z_c - Z_t Y_c$，再定义 $\Delta U=\frac{\Delta P}{E Z_t\,E Z_c}$。

- **Property 1（已证明无偏）**：利用 $Y_t,Z_t\perp Y_c,Z_c$，严格推出 $E[\Delta U]=\tau_r$。
- **Property 2（近似）**：delta method 给出方差，在真实实验「干预增量极小、$\alpha_t\approx\alpha_c$」（Budylin et al., 2018 的行业经验）时，$\mathrm{Var}(\Delta U)\approx\mathrm{Var}(\Delta R)$。**严格等号仅当 $\alpha_t=\alpha_c$ 成立，实际为近似。**

为何此前工作做不好：要么忽略分子分母相关性，要么错误假设变换系数为常数。STATE 通过这套线性变换把比率问题转回计数式稳健回归。

## 7. 假设、边界与局限

**严格成立所需 / 论文依赖的假设**
- 随机化实验，$T\perp X$，样本近似 i.i.d.（第 2.1 节）。
- 交叉拟合保证 $\hat Y_i\perp T_i$，否则调整可能引入偏差。
- 残差位置参数 $u=0$（论文设定，不损一般性）。
- 比率无偏性证明成立；比率方差一致性仅在 $\alpha_t\approx\alpha_c$ 下近似。

**明确陈述的局限（第 5.4 节）**
- **高斯指标下无优势且有额外开销**：论文原话「When metric follows a Gaussian distribution, the STATE method is comparable with the state-of-the-art methods, but introduces extra computational cost.」50 万观测需约 30–60 秒 EM。
- 收益随指标重尾程度而变，非恒定。
- 比率变换的方差一致性只是近似。
- Winsorization 对阈值敏感（低阈值降低覆盖度、增偏）；Huber 回归鲁棒性有限且不敌 STATE。

**不要误读**
- 「超过 50% 方差缩减」主要针对**重尾分布**场景；高斯下 STATE 与 CUPAC/MLRATE 持平。
- 论文「只需一半样本量 / 一半实验周期」是「方差与所需样本量成反比」的**推论**，由重尾场景实验数据支撑，不是独立定理。

> **第三方复现注记（2026-10 调研，需警惕）**：GitHub 上一个第三方复现（forestqin/survey_state_variance_reduce）在仿真中发现，当处理效应对**全体用户均匀**时 STATE 无偏、方差缩减极高（甚至报出 99%，与论文 84% 量级不同，源于仿真设置差异）；但当效应仅作用于**部分人群（局部异质处理效应 HTE）**时，STATE 的 ATE 出现**明显偏差**。这指向一个论文未充分讨论的风险：Student-t 稳健似然对极端值的降权，可能与处理效应的局部异质性纠缠，从而在高 HTE 场景下引入偏倚。落地前必须在自家指标上做 A/A（验证零效应下无偏、覆盖度正常）与真实实验对照，不可直接搬用美团的 80%+ 数字。

## 8. 实证结果：区分事实与推论

| 场景 | 方法 | 方差缩减 % | 来源 |
|---|---|---|---|
| 模拟·计数（含 0.5% 离群） | DIM / CUPED / CUPAC / MLRATE / **STATE** | 0 / 28.7 / 32.6 / 32.4 / **84.1** | 论文 Table 1（事实） |
| 模拟·计数（同上）经验覆盖度 | 各法约 94–95.6% | STATE 95.6% | 论文 Table 1（事实） |
| 模拟·比率 | CTRM / **STATE** | 55.7 / **90.1** | 论文 Table 2（事实） |
| 美团 A/A·订单数(orders) | CUPAC/MLRATE / **STATE** | 54.6 / **70.5** | 论文 Table 3（事实，平台数据） |
| 美团 A/A·用户 GMV | CUPAC/MLRATE / **STATE** | 44.4 / **80.7** | 论文 Table 3（事实，平台数据） |
| 美团 A/A·客单价(比率) | CTRM / **STATE** | 21.8 / **91.6** | 论文 Table 6（事实，平台数据） |

读表要点：
- STATE 在重尾计数（尤其 GMV）和比率指标上优势最大；在订单数这种相对不那么重尾的指标上，相对 CUPAC 的领先收窄。
- 这些是**论文自身模拟与美团单一平台**的结果，不是跨场景通用基准。落地前必须在自家指标上做 A/A 与真实实验对照。
- 「一半样本 / 一半周期」是推论，见第 7 节。

## 9. 与相近方法比较

| 方法 | 机制 | 何时更合适 | 相对 STATE 的位置 |
|---|---|---|---|
| CUPAC / MLRATE | 高斯似然下用 ML 预测分做回归调整 | 指标近似高斯或轻度偏态；需要成熟工程路径 | STATE 的「前置阶段」，STATE 在其上加 Student-t 似然 |
| Winsorize / 截尾 | 硬压或删除极端值 | 极端值确为噪声/数据错误 | 阈值敏感、可能改 estimand；STATE 是软降权且不改 estimand |
| Huber 回归 | 对大残差线性化损失 | 轻度鲁棒需求 | 论文称其鲁棒性有限、不敌 STATE |
| 指标变换（log 等） | 改变结果尺度 | 长尾但可接受相应估计目标 | 与 STATE 互补，但可能改变 estimand，须事前定口径 |

## 10. 实践建议与常见误区

落地 STATE 前至少做：
- 确认指标确实重尾（看残差 QQ 图、尾部指数、极端值占比）；高斯指标上 STATE 是净亏（多 EM 开销）。
- 代理 $\hat Y_i$ 必须样本外 / 交叉拟合生成，且特征全在分配前可得——否则无偏性失效。
- 与 DIM、经典 CUPED、CUPAC 并列报告 A/A 覆盖度与真实实验效果，验证零效应下的假阳性率。
- 比率指标用第 6 节变换，并确认 $\alpha_t\approx\alpha_c$ 近似是否成立；不成立时方差一致性只是近似。
- 评估计算成本（EM 迭代），大流量指标确认时延可接受。

常见误区：
- 把「超过 50% 方差缩减」当通用承诺（实为特定重尾场景 + 单一平台）。
- 在高斯指标上硬上 STATE 求「前沿」——净增成本无收益。
- 用 STATE 掩盖数据质量问题（极端值是真实高价值用户还是脏数据？压低权重可能改变业务含义）。

## 11. 常见疑问：均值渐近正态，为何还要用重尾分布建模个体结果

一个常见反驳：A/B 最终比较的是均值，而根据大数定律 / 中心极限定理，样本均值渐近服从正态分布，那为何还要在个体层面用 Student-t 这种重尾分布建模？

这个直觉对了一半，但混淆了两个层次：

- **第 1 层**：单个观测 $Y_i$ 的分布（STATE 建模的对象，重尾 Student-t）。
- **第 2 层**：均值差 $\bar Y_t-\bar Y_c$ 的抽样分布（「渐近正态」说的那个）。

STATE 在第 1 层建模，但它要估计、要比较的仍是第 2 层的均值差——estimand 仍是算术平均 ATE（论文设定残差位置 $u=0$，ATE 即 $a_1$ 的 MLE）。STATE 完全同意「最终比均值」，问题在于「用高斯假设去估这个均值差」在重尾下会失稳。

「CLT 会救你」在三种情况下失灵：

1. **方差可能不存在**。Student-t 自由度 $\nu\le2$ 时方差无穷，CLT 的 $\sqrt n$ 收敛前提直接失效，均值收敛到稳定分布、速率慢于 $\sqrt n$。GMV、收入类指标在观测区间常落在此区制，这恰恰是最该用 STATE 的时候。
2. **方差有限但尾重**（$\nu$ 较小，如 3–5）。CLT 收敛慢，中等样本量下均值抽样分布仍明显比正态胖，正态 p 值 / 置信区间校准失真。
3. **回归调整的好处来自压低残差方差，而残差方差在重尾下被极端值主导**。高斯 OLS 用平方损失，少数离群点把回归系数、以及更关键的残差方差估计（即标准误）拉爆：标准误失真且不稳，导致统计功效流失、覆盖度偏离名义值。STATE 用潜精度 $\eta_i$ 在系数和尺度估计里同时给离群点降权，本质是对回归调整模型做迭代重加权最小二乘（IRLS）/ 稳健 M 估计。

需要澄清的边界：STATE 不改变 estimand，也没有「打败 CLT」，只是让有限样本下均值差及其标准误的估计更稳。当指标近似高斯时，STATE 与高斯方法表现持平却多花 EM 计算（论文第 5.4 节局限），这正好印证上述直觉——轻尾时 CLT 已经够用。

> 一句话：**「均值渐近正态」说的是第 2 层；STATE 修的是第 1 层残差建模，让第 2 层的均值差估计和标准误不被少数极端值拖垮；当尾巴重到方差都不存在时，正态近似本身就不成立。**

> 注：严格讲大数定律只保证样本均值收敛到总体均值（一致性），正态近似是中心极限定理的结论；二者都描述**估计量**而非**数据**的分布。

## 13. 实现与工具现状（2026-10 调研）

STATE 本身尚无官方开源实现；经典 CUPED/CUPAC 类有现成库，但均不含 Student-t 稳健扩展。

**STATE 的实现现状**
- 官方：论文（arXiv:2407.16337 / KDD 2024）未发布官方代码，ACM 补充材料仅有演示视频。
- 第三方：GitHub `forestqin/survey_state_variance_reduce` 含仿真与 DIM/CUPED/STATE 对比，但仅 1 star、未审计，且其复现暴露了 HTE 下有偏风险（见第 7 节注记）。若要用，建议 fork 后审计再上。
- 自实现路径：基于论文 + Liu & Rubin (1995) 的 ECM/尺度混合，变分 EM 的全部 E-step/M-step 公式已在本卡第 4.3–4.4 节列全，落到 NumPy 即可。

**现成的「重尾 / 稳健」替代（比自写变分 EM 省事，且更灵活）**
- **贝叶斯 Student-t 回归（PyMC / NumPyro / Stan）**：直接对残差设 Student-t 似然做回归，自动鲁棒，等价于 STATE 的降权目标，还能给出后验不确定性；约几十行即可，天然适配交叉拟合后的代理回归。**落地 STATE 思路时最推荐的现成路线。**
- **statsmodels.RLM**：Huber / MAD 等稳健线性模型，工程简单，但损失函数非 t 似然，论文称其鲁棒性有限、不敌 STATE，适合轻量稳健需求。
- **R `robustbase::lmrob`**：MM 估计稳健回归。

以上均非「STATE 的变分 EM」，但都能实现「重尾下稳健 ATE」这一核心目标。

**经典 CUPED / CUPAC 类现成库（注意：无 Student-t 稳健扩展，即无 STATE）**
- `ambrosia`：含 CUPED / MultiCUPED / MLVarianceReducer，ML 方差缩减最接近 CUPAC 思路。
- `cuped-lite`：纯 NumPy/SciPy 的轻量经典 CUPED。
- `xpyrment`：企业级实验库，CUPED + 比率 CUPED + mSPRT + DiD 等，功能最全。
- `pfngouin`：pingouin 扩展，用 TabPFN / XGBoost 做预测驱动 CUPED。

**落地建议**：先用 ambrosia / xpyrment 把 CUPAC/MLRATE 基线做 A/A 对照，再用 PyMC 写 Student-t 回归对照重尾指标上差距是否如论文所示；不要一上来就自实现变分 EM。

## 14. 来源与延伸阅读

1. **STATE 原论文（KDD 2024）**：Zhou, Sun, Li, Fan, Jiang, Zheng, Li, “STATE: A Robust ATE Estimator of Heavy-Tailed Metrics for Variance Reduction in Online Controlled Experiments.” [arXiv:2407.16337](https://arxiv.org/abs/2407.16337)；[DOI](https://doi.org/10.48550/arXiv.2407.16337)。本文方法、公式编号、Table 1–6 数字与第 5.4 节局限均出自此文。
2. **尺度混合基础**：Liu & Rubin (1995), “ML estimation of the t distribution using EM and its extensions,” *Statist. Comput.* 用于 Student-t 的 ECM / 尺度混合表示。
3. **比率指标实践**：Budylin et al. (2018), “A/B 实验中的比率指标”相关行业经验（小干预效应下 $\alpha_t\approx\alpha_c$），被 STATE 第 4 节引用为方差一致性近似的前提。
4. **前置方法**：[CUPED](CUPED.md)（Deng et al., 2013）；[CUPED 变体](CUPED变体.md)（含 CUPAC / MLRATE 选型与「多协变量回归是 CUPAC 特例」的关系）。

---

**本文范围**：只讲 STATE 的机制、证据边界与选型判断。CUPED 基础推导、CUPAC/MLRATE 的通用比较、switchback 与实验期协变量等扩展，统一在 [CUPED 变体](CUPED变体.md) 与 [灵敏度与提效](index.md) 处理，避免把不同估计器混成同一类。
