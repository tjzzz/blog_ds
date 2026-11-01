---
title: CUPED：用实验前信息提升实验灵敏度
created: 2026-10-09
updated: 2026-10-20
tags: [llm-wiki, experimentation, variance-reduction, CUPED]
source:
  - "Deng et al. (2013), Improving the Sensitivity of Online Controlled Experiments by Utilizing Pre-Experiment Data"
  - "Z_Project_DS/topics/实验设计与AB测试/灵敏度与提效/ab实验__04_CUPED与方差缩减.md"
wiki_type: methods
topic: "实验设计与AB测试"
review_status: reviewed
---

> 所属 Topic：[实验设计与AB测试](../index.md) · 类型：方法
>
> 相关主题：[CUPED 变体](CUPED变体.md) · [灵敏度与提效总览](index.md) · [指标变换与实验敏感性](指标变换与实验敏感性.md) · [MDE](../统计判断与决策/MDE.md) · [SRM-分组样本比例不匹配](../分流与平台/SRM-分组样本比例不匹配.md) · [pre-AA](pre-AA.md)

# CUPED：用实验前信息提升实验灵敏度

## 1. 先说结论：CUPED 是什么

**CUPED（Controlled-experiment Using Pre-Experiment Data）是一类协变量调整/方差缩减方法：利用随机化前已经观测到、且能预测实验期结果的用户信息，解释实验期结果中的自然差异，从而降低处理效应估计的标准误。**典型协变量是同一用户在实验前一段时间的同类指标，例如实验前 14 天消费预测实验期 14 天消费。

它不创造处理效果，也不替代随机化。目标通常仍是估计原始指标上的实验组与对照组平均差（ITT）；改变的是估计精度，而不是把结果“调成显著”。

直观地看：

```text
实验期结果 = 用户稳定差异 + 实验处理效应 + 随机噪声
                          ↑
             用实验前协变量解释并扣除可预测部分
```

如果实验前行为与实验期结果相关，扣除可预测的部分后，个体残差更小，组间均值差的标准误也可能更小。若协变量几乎没有预测力，CUPED 就几乎没有收益；若口径或分析做错，则可能引入偏差或错误标准误。

## 2. 从调整公式到方差收益

### 2.1 单个协变量的 CUPED 调整

对每个随机化单位 $i$，记：

- $Y_i$：实验期结果指标；
- $X_i$：实验开始前测得的协变量；
- $\bar X$：分析样本中 $X$ 的均值；
- $\theta$：用来调整 $X$ 与 $Y$ 关系的系数。

定义调整后的结果：

$$
Y_i^{\text{cuped}}=Y_i-\theta(X_i-\bar X).
$$

再用 $Y_i^{\text{cuped}}$ 计算实验组与对照组的均值差。减去中心化项是为了不改变总体均值尺度；在两组使用同一套中心和系数时，处理效应差的点估计在常见设计下保持为原始均值差。

为什么选这个形式？对固定的 $\theta$：

$$
\operatorname{Var}(Y-\theta X)
=\operatorname{Var}(Y)+\theta^2\operatorname{Var}(X)-2\theta\operatorname{Cov}(X,Y).
$$

令方差对 $\theta$ 最小，求导并令其为零：

$$
2\theta\operatorname{Var}(X)-2\operatorname{Cov}(X,Y)=0
\quad\Rightarrow\quad
\theta^*=\frac{\operatorname{Cov}(X,Y)}{\operatorname{Var}(X)}.
$$

代回可得：

$$
\operatorname{Var}(Y-\theta^*X)
=\operatorname{Var}(Y)(1-\rho_{XY}^2),
$$

其中 $\rho_{XY}$ 是 $X$ 与 $Y$ 的相关系数。这个式子说明：在线性关系和同一总体方差的理想情形下，相关性平方就是单个结果变量层面的方差削减比例。它不是对每个实验处理效应方差的无条件保证；有限样本、模型设定、协变量缺失、聚类/重复观测等都会改变实际效果。

### 2.2 处理效应标准误如何变化

若两组独立、随机化单位独立且组内调整后方差近似相同，每组 $n$ 个单位，则未调整的均值差方差近似为 $2\operatorname{Var}(Y)/n$；调整后约为 $2\operatorname{Var}(Y)(1-\rho^2)/n$。因此：

$$
\frac{SE_{\text{cuped}}}{SE_{\text{raw}}}\approx\sqrt{1-\rho^2},
\qquad
\frac{n_{\text{cuped}}}{n_{\text{raw}}}\approx 1-\rho^2
$$

其中样本量比是保持相同 MDE、显著性水平和功效时的近似等效关系。举例：如果相关系数约为 $0.6$，理想化方差比为 $1-0.6^2=0.64$，即方差约降 36%、标准误约乘 $0.8$；在其他条件不变时，所需样本量可能约为原来的 64%。**此为公式示意，不是任何产品的实测承诺。**

原始 CUPED 论文报告，在其 Bing 在线实验案例中，某些指标的方差缩减约 50%，并指出这在其设置下相当于约两倍流量或约一半实验时长达到相同灵敏度。该数字是论文中特定实验集合的经验结果，不应外推为所有业务的默认收益。[原始论文](https://doi.org/10.1145/2433396.2433413)

## 3. 一个小例子：用户消费的稳定差异

假设目标是比较每用户实验期 14 天收入。重度付费用户往往在不同时间窗都消费较多，因此用户实验前 14 天收入 $X$ 与实验期收入 $Y$ 正相关。若 $\operatorname{Corr}(X,Y)=0.7$，最优线性调整的理想方差比为：

$$
1-0.7^2=0.51.
$$

也就是在理想化关系下，调整后的结果方差约为未调整的一半。分析不是比较“实验前收入”和“实验期收入”的差异来代替随机对照，而是先对每个用户的实验期结果扣除由实验前行为预测出的部分，再比较随机分配的两组。

示例协变量：

| 实验期目标指标 $Y$ | 可考虑的实验前协变量 $X$ |
| --- | --- |
| 14 天人均收入 | 处理前 14/28 天人均收入、付费天数、历史消费层级 |
| 7 天活跃天数 | 处理前 7/28 天活跃天数 |
| 点击/会话数 | 处理前同类点击数、会话数 |
| 留存或转化 | 处理前活跃、历史转化倾向等预处理变量 |

选择不是“越多越好”：预测力、可用率、业务口径稳定性、泄漏风险与分析复杂度都要一起考虑。

## 4. 为什么 CUPED 不会把随机实验变成观察性分析

随机化使处理分配在期望上与处理前特征独立。只要 $X$ 真正是在处理前确定、并且分析没有因处理后变量或选择性筛样本而破坏随机化，$X$ 可用来提高精度；处理效应仍由组间比较识别。

实践中要特别区分：

- **处理前变量**：随机分配/处理前已确定，原则上可作为调整变量；
- **处理后变量**：可能受实验影响的点击、曝光、购买、触发状态等，不能因为它预测 $Y$ 就直接当成 CUPED 基线变量；条件化于处理后变量可能改变 estimand 或引入偏差；
- **实验期协变量**：有更广义的回归调整或控制变异量方法，但不应简单当作传统 pre-experiment CUPED；要单独说明识别条件和推断方法。

CUPED 也不能修复错误分流、SRM、埋点缺失、组间差异化数据丢失或实验干扰。先确认实验可信，再做方差缩减；正式实验中的 SRM 检测见 [SRM-分组样本比例不匹配](../分流与平台/SRM-分组样本比例不匹配.md)，正式实验前的流程演练见 [pre-AA](pre-AA.md)。

## 5. 实施流程：从设计到报告

### 5.1 事前定义分析计划

在看实验结果前确定：主要指标及其窗口、随机化/分析单位、协变量口径和时间窗、调整模型、缺失值处理、主要估计量与标准误算法。若尝试多个协变量或模型，应在历史数据或独立样本上开发并验证，不以当前实验显著性挑方案。

### 5.2 生成处理前特征

以随机化单位为粒度聚合 $X$。用户级随机化则通常一名用户一行；若按租户、门店、地区等集群随机，推断也必须尊重集群层级，不能把用户行当独立样本。窗口需在处理开始前结束，并保证每个单位的时间窗定义一致。

### 5.3 估计调整系数

单协变量线性调整通常使用：

$$
\hat\theta=\frac{\widehat{\operatorname{Cov}}(X,Y)}{\widehat{\operatorname{Var}}(X)}.
$$

可在合并样本或不含处理标签的设计中估计共同斜率；更一般的多协变量场景，可使用线性回归/广义回归调整。关键是推断应反映系数估计的不确定性，并避免因组别特异斜率、分层结构或缺失处理不当而低估标准误。成熟分析平台往往把调整估计和相应方差计算作为整体实现，而不是只生成一个校正指标后机械套用不匹配的检验。

### 5.4 估计处理效应并做诊断

比较实验组与对照组的调整结果，输出处理效应、标准误/置信区间，以及原始估计作为参照。检查调整前后点估计是否出现超出预期的明显变化；若变化很大，应排查协变量时间边界、错误连接、缺失机制、样本构成和模型设定。CUPED通常主要提升精度，不能仅凭“标准误下降”就认定分析正确。

### 5.5 评估真实收益

在历史数据或 A/A 数据上验证：协变量预测力、方差比、不同时间窗口稳定性、缺失用户表现、极端值敏感性和实际标准误变化。不要只看某一场实验的 p 值是否越过阈值。历史 A/A 能检验无处理差异下的校准/数据流程，但不能单独证明存在真实效果时功效一定提高。

## 6. 缺失值、长尾与特殊分析单位

### 缺失基线协变量

新用户没有历史行为是常态，不等于应删除。可以考虑：缺失指示变量 + 合理填补、预先定义的新老用户分层、回归模型对缺失机制的处理等。选择取决于缺失是否与用户类型相关、是否跨实验组平衡，以及目标总体是否仍是全部随机化用户。若只保留“有历史记录者”，结论将转向该子群体；如有可能，需报告覆盖率与总体定义。

### 长尾指标

CUPED 可以对原始收入/时长用基线协变量调整，也可用变换后的协变量预测原始结果；这与直接把结果 $Y$ 改成 log/截尾指标不是一回事。前者可保留原始均值效应目标，后者会改变 estimand。长尾、小样本或高杠杆点可能令回归斜率和标准误不稳，应配合稳健性检查、预先定义的指标口径和合适推断方法。参见 [指标变换与实验敏感性](指标变换与实验敏感性.md)。

### 非用户级指标与集群随机化

当处理按租户、门店、地区或其他集群分配时，个体结果相关；标准误必须按随机化单位/实际相关结构计算。不能因为数据表里有大量用户记录，就把它们视为大量独立随机化样本。Microsoft 对 tenant-randomized 实验的公开讨论展示了随机化单位与用户级设计不同会造成显著功效损失，且配对并非总能改善功效。[Microsoft Research：Tenant-randomized A/B](https://www.microsoft.com/en-us/research/articles/why-tenant-randomized-a-b-test-is-challenging-and-tenant-pairing-may-not-work/)

## 7. CUPED 扩展与相关方法

CUPED 与 CUPAC、MLRATE、STATE 等方法的关系、适用边界及证据成熟度，统一见 [CUPED 变体](CUPED变体.md)。该页也比较了分层/后分层、DR、实验期协变量、switchback 调整，以及指标变换和样本量优化等相关路线。

## 8. 常见误区与故障排查

| 误区 | 为什么不妥 | 建议 |
| --- | --- | --- |
| “CUPED 自动缩短实验一半” | 收益依赖预测相关性、指标、样本结构和估计实现 | 用历史/AA 数据评估方差比，报告不确定性和覆盖率 |
| 使用实验触发、点击、购买等处理后行为做基线 | 变量可能已被处理影响，条件化会改变因果问题 | 严格截断在随机化/处理前；处理后信息另按专门方法分析 |
| 只分析有历史数据的用户 | 可能改变目标人群并引入选择偏差 | 保留目标总体，设计缺失处理并报告覆盖率/敏感性 |
| 调整后更显著就认为有业务效果 | 显著性是信号与标准误的共同结果；模型选择也会带来选择性 | 同时报告原始与调整结果、效应量、区间和预设分析计划 |
| CUPED 解决 SRM 或埋点问题 | 方差缩减不修复实验执行/数据可信度 | 先做 SRM、曝光、埋点与样本完整性检查 |
| 对每组分别随意拟合模型/调系数 | 可能增加估计不稳定或错误标准误 | 用预先规定的共同调整方法和与设计匹配的推断 |
| 直接把 log(Y) 当成“CUPED” | 非线性变换改变估计目标，不是协变量调整 | 区分结果变换与协变量校正，分别解释 estimand |

## 9. 与 MDE、实验决策的连接

若调整使处理效应标准误乘以 $r<1$，在效应、显著性水平、功效目标和其他假设不变时，MDE 也大致乘以 $r$；或保持原 MDE 时，样本量近似按方差比缩小。这个关系将 CUPED 与 [MDE](../统计判断与决策/MDE.md) 接起来。

但更精确的样本量收益要用实际调整后方差和计划中的检验/分析方法重算。CUPED 不保证让任何实验更早结束；若采用序贯停止规则，还必须采用与之匹配的序贯推断，不能因为加了 CUPED 就随意反复窥视并按固定样本 p 值停止。参见 [序贯分析](../统计判断与决策/序贯分析.md)。

## 10. 实施前核对清单

- [ ] 估计目标是原始指标上的 ITT，还是一个变换后的指标？写清楚。
- [ ] 随机化单位、分析单位和标准误聚类层级是否一致？
- [ ] 协变量是否在处理前完整确定？是否有任何曝光后字段或时间泄漏？
- [ ] 协变量对目标结果有足够预测力，且预测关系在时间/人群间相对稳定吗？
- [ ] 缺失用户如何处理？是否会改变目标总体？
- [ ] $\theta$/模型选择和估计推断是否预先规定、正确计入不确定性？
- [ ] 原始与调整结果、方差比、置信区间和覆盖率是否一起报告？
- [ ] SRM、埋点、样本成熟度、长尾和干扰等基础问题是否已检查？
- [ ] 多指标/多方案和持续查看规则是否另行处理？

## 附录：原始论文与延伸资料

1. **原始论文（建议优先阅读）**：Alex Deng, Ya Xu, Ron Kohavi, Toby Walker. “Improving the Sensitivity of Online Controlled Experiments by Utilizing Pre-Experiment Data.” *WSDM 2013*, pp. 123–132. [DOI / ACM 页面](https://doi.org/10.1145/2433396.2433413)；[作者公开 PDF](https://www.exp-platform.com/Documents/2013-02-CUPED-ImprovingSensitivityOfControlledExperiments.pdf)。论文提出 CUPED，介绍非用户级指标、部分基线数据缺失和协变量选择，并报告 Bing 实验案例的结果。
2. Alex Deng et al. “Improving the Sensitivity of Online Controlled Experiments: Case Studies at Netflix.” *KDD 2016*. [KDD 页面](https://www.kdd.org/kdd2016/subtopic/view/improving-the-sensitivity-of-online-controlled-experiments-case-studies-at-)。可作为大规模实验中方差缩减方法实践的延伸阅读；不应把单一案例外推为普遍收益。
3. Microsoft Research, [Why Tenant-Randomized A/B Test is Challenging and Tenant-Pairing May Not Work](https://www.microsoft.com/en-us/research/articles/why-tenant-randomized-a-b-test-is-challenging-and-tenant-pairing-may-not-work/)。用于理解随机化单位、集群结构与功效的关系。
4. **CUPAC / switchback 实践**：DoorDash, [Improving Experimental Power through Control Using Predictions as Covariate (CUPAC)](https://careersatdoordash.com/blog/improving-experimental-power-through-control-using-predictions-as-covariate-cupac/)（2020）；Tang, Huang, Kastelman & Bauman, *Control Using Predictions as Covariates in Switchback Experiments*（2020 技术稿，[可读稿](https://www.researchgate.net/publication/345698207_Control_Using_Predictions_as_Covariates_in_Switchback_Experiments)）。用于特定 marketplace switchback 场景，不是用户级独立 A/B 的默认结果。
5. **STATE 原始论文**：Zhou et al., “STATE: A Robust ATE Estimator of Heavy-Tailed Metrics for Variance Reduction in Online Controlled Experiments.” [arXiv:2407.16337](https://arxiv.org/abs/2407.16337)。论文提出重尾指标的鲁棒 ATE 估计框架；文中的实证收益属于其研究数据和对照方法范围。
6. **CUPED/CUPAC/DR 对比案例**：Staponaite et al., “Variance Reduction in Online Marketplace A/B Testing.” *KDD-UMC 2025*. [论文 PDF](https://kdd2025.kdd.org/wp-content/uploads/2025/07/CameraReady-05.pdf)。该研究基于历史 marketplace 实验并注入合成处理效应比较方法；需按论文设计解释其 CI 宽度结果，不应直接当成任意产品的预期节省。

本篇整合原有 [pre-AA](pre-AA.md) 与[灵敏度与提效总览](index.md) 中关于 CUPED 的核心材料，并以原始论文补足推导、适用边界与引用。原文中独立的 pre-AA 内容保留在该文件；本篇为 CUPED 的统一主笔记。
