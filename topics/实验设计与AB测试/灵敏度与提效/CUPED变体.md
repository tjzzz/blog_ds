---
title: CUPED 变体：从协变量调整到稳健与设计感知的方差缩减
created: 2026-10-18
updated: 2026-10-20
tags: [llm-wiki, ab-test, CUPED, variance-reduction, causal-inference]
source:
  - "Deng et al. (2013), CUPED"
  - "Guo et al. (2021), MLRATE"
  - "Zhou et al. (2024), STATE"
  - "Lin & Crespo (2026), pre- and in-experiment covariate adjustment"
wiki_type: methods
topic: "实验设计与AB测试"
review_status: reviewed
---

> 所属 Topic：[实验设计与AB测试](../index.md) · 类型：方法
>
> CUPED 基础原理见 [CUPED](CUPED.md)；本文聚焦其扩展路线、适用问题与证据成熟度。

# CUPED 变体：从协变量调整到稳健与设计感知的方差缩减

## 1. 先建立分类框架：变体究竟改了什么

CUPED 的核心不是某一个固定公式，而是**利用实验处理前可用的信息，预测实验期结果中与处理效果无关的波动，再对处理效果估计做调整**。常见基础形式是：

$$
Y_i^{adj}=Y_i-\theta(X_i-\bar X),\qquad
\theta^*=\frac{\operatorname{Cov}(X,Y)}{\operatorname{Var}(X)}.
$$

当单个线性协变量 $X$ 能预测结果 $Y$ 时，该调整可降低结果方差。扩展方案通常沿着四个方向创新：

1. **预测更好**：从单一历史指标扩展到多个协变量或机器学习预测（CUPAC、MLRATE）。
2. **数据更难**：应对重尾、异常值、比例指标或稀疏结果（如 STATE）。
3. **可用信息更多**：在严格条件下使用实验期中间变量，而不只用实验前数据。
4. **设计更复杂**：针对 switchback、集群随机化等具有时间/群组依赖的实验，匹配随机化单位和推断方式。

## 2. 方法地图与证据成熟度

| 方法 | 改进点/基本机制 | 更适合的问题 | 主要代价或边界 | 证据状态 |
| --- | --- | --- | --- | --- |
| 多协变量回归调整 | 同时用多个处理前特征预测 $Y$，以回归残差或线性调整估计组间差 | 可用基线特征多、单一历史指标解释力有限 | 共线性、缺失、模型和标准误实现需治理 | 在线实验中常见的成熟方法；具体收益仍需本地验证 |
| CUPAC | 用模型 $\hat m(X)$ 将许多特征压缩成结果预测，再把预测作为调整协变量 | 高维、非线性基线特征；历史行为复杂 | 需防止训练泄漏/过拟合；训练预测与目标时期分布漂移会削弱收益 | DoorDash 有公开工程案例；非“必然优于 CUPED”保证 |
| MLRATE / 交叉拟合机器学习调整 | 分折训练预测模型，在未参与训练的样本上生成预测并估计 ATE | 高维特征，需兼顾灵活预测与稳健推断 | 计算和平台复杂度高；交叉拟合及影响函数方差要匹配 | NeurIPS 2021 论文及 Facebook A/A 指标案例 |
| STATE | Student-$t$ 重尾建模与机器学习结合，构造鲁棒 ATE 估计 | 收入、交易等尾部重且异常值影响明显的指标 | 方法与计算更复杂；需评估模型假设、目标量、校准 | KDD 2024 论文提出；作者报告了美团平台实验及模拟结果 |
| 实验前 + 实验期协变量 | 在 CUPED/CUPAC 基础上增加实验期间协变量以提高预测力 | 纯实验前特征预测力不足，且有合适的实验期信息 | 处理后变量若受处理影响，直接调整可能改变 estimand 或引入偏差；必须选可识别方案 | 2026 CLeaR/PMLR 发表方法，在 Etsy 多场实验评估；不是任意使用 post-treatment covariates 的许可 |
| Switchback 专用调整 | 以时间窗/地域等随机化单元建模历史预测、时段效应及相关性 | 市场网络干扰使用户级 A/B 不适用，采用地域×时间窗轮换 | 有效随机化单元少、时间自相关、carryover、集群不平衡；须设计感知推断 | DoorDash 2020 CUPAC 为应用案例；2026 新方案仍有预印本，成熟度较低 |
| 指标变换 / 截尾 | 改变结果变量的尺度或尾部贡献 | 长尾指标受极端值支配，且业务能接受相应估计目标 | 不等同协变量调整；可能改变 estimand，需事前定口径 | 与 CUPED 互补的敏感性处理；逐场景验证 |
| 流量比例 / 样本量优化 | 改变分配比例、增加流量或延长周期以增加信息量 | 流量充足且实验风险可控，希望降低标准误 | 不是方差缩减估计器；要权衡风险、机会成本和周期干扰 | 常规设计策略；需结合实验约束计算 |

**关系澄清：多协变量回归调整是 CUPAC 的特例。** 上表把两者分列，但机制上并不对立：多协变量回归调整等价于「用线性模型 $\hat m(Z)=\beta^\top Z$ 直接在回归中放入原始预处理特征」的 CUPAC；CUPAC 的泛化在于把协变量换成模型学出的预测分 $\hat m(Z)$，可非线性、高维、规避共线/缺失治理。判断是否从多协变量升级到 CUPAC，看原始线性特征是否够用，而非方法新旧。两者关系与 STATE 的承袭位置见 [STATE](STATE.md) 第 4.1 节。

### 本文范围

本文聚焦 CUPED 方法族：多协变量和预测式调整、CUPAC、MLRATE、STATE，以及实验期协变量和 switchback 等特定扩展。分层/后分层、Doubly Robust（DR）、指标变换/截尾、流量比例与样本量优化是相关的提效或估计路线，但并非 CUPED 变体；统一放在[灵敏度与提效总览](index.md)的提效地图中说明，避免把不同设计、估计器和优化手段混成同一类。

“CUPAC”“深度 CUPED”等名称在不同论文/平台里可能指不同实现。对任何机器学习扩展，重点检查训练数据是否与评估数据分离或交叉拟合、预测特征是否全为处理前信息、最终标准误是否覆盖模型估计不确定性，以及估计目标是否仍匹配业务问题。

**来源口径提醒**：Switchback 上的 CUPAC 有 DoorDash 2020 年公开文章与同期技术稿作为专门案例；不要将其与常规在线 A/B 的方法比较研究混为一谈，也不要把个案结果当作通用基准。

## 3. CUPAC：把“一个历史协变量”扩展成“预测分数”

### 3.1 机制

传统 CUPED 常用历史同指标 $X=Y_{pre}$。CUPAC（Control Using Predictions As Covariates）先用一组处理前特征 $Z$ 训练预测器：

$$
\hat m(Z_i)\approx E[Y_i\mid Z_i],
$$

再将样本外预测 $\hat m(Z_i)$ 当作协变量，按回归调整/控制变量的思路估计实验组和对照组差异。预测器可以捕获非线性和多变量关系，因此在基线行为由多个变量共同决定时，可能比单一的 $Y_{pre}$ 更有预测力。（若预测模型取为线性且直接使用原始预处理特征，CUPAC 即退化为多协变量回归调整——后者是前者的线性特例，见第 2 节关系澄清与 [STATE](STATE.md) 第 4.1 节。）

关键收益仍来自“预测值与实验期结果的样本外关联”，而不是“用了机器学习”这个标签。若预测器只是在训练数据上拟合得好、样本外相关性很弱，实际方差缩减不会按训练 $R^2$ 保证。DoorDash 的公开材料介绍了基于预测作为协变量的 CUPAC，并报告其 switchback 场景的实验周期缩短案例；这是特定公司与指标的经验，不可直接外推。[DoorDash 工程文章](https://careersatdoordash.com/blog/improving-experimental-power-through-control-using-predictions-as-covariate-cupac/)

### 3.2 何时从 CUPED 升级到 CUPAC

优先考虑 CUPAC 的理由通常是：基线可用特征较丰富、实验期结果与多变量非线性关系明显、能离线训练并稳定部署模型。若当前同指标历史值已高度预测未来值，复杂模型未必值得其开发、验证和维护成本。

落地时至少要做：

- 所有输入在分配处理前可得；
- 用历史数据或交叉拟合，确保预测对训练外样本生成；
- 监控预测值与实际指标在不同时段/用户层的校准和相关性；
- 估计量和标准误覆盖模型训练与抽样带来的不确定性；
- 与单变量 CUPED、未经调整的差分估计做 A/A 与真实实验对照。

## 4. MLRATE 与机器学习回归调整：灵活性配上推断保护

MLRATE（Machine Learning Regression-Adjusted Treatment Effect）使用机器学习预测潜在结果/实验结果来做 ATE 回归调整，并采用 **cross-fitting（交叉拟合）**：把样本分折，每一折的预测由未使用该折观测训练的模型生成，再用这些样本外预测估计处理效应。

交叉拟合的作用是降低同一数据既训练预测器、又评估调整后效果造成的过拟合偏差；它不是让任意模型都自动有效的魔法。推断还需满足论文中的正则条件、估计一致性和合适的标准误计算。

Guo 等人的 NeurIPS 2021 论文提出 MLRATE，并报告在 48 个 Facebook A/A 结果指标上的比较：其估计方差比简单均值差低 70% 以上，比只用实验前同一指标做单变量调整低约 19%。这是文中数据集合与实现下的结果，不是任何实验的预期收益。[原始论文与 NeurIPS 页面](https://papers.nips.cc/paper_files/paper/2021/hash/488b084119a1c7a4950f00706ec7ea16-Abstract.html)

**与 CUPAC 的关系**：CUPAC强调“预测值作为协变量”的工程路径；MLRATE强调“机器学习预测 + 设计过的 ATE 估计与推断”的方法框架。两者会重叠，但不能只按算法是否用 ML 来判断统计有效性。

## 5. STATE：面向长尾/重尾指标的鲁棒 ATE 路线

传统线性协变量调整在重尾收入指标上可能被极端值影响；异常值还可能削弱历史协变量对实验期结果的相关性。STATE（Student's t-distribution ATE estimator）将 Student-$t$ 重尾建模与机器学习结合，并用变分 EM 等方法估计鲁棒 ATE；作者也讨论将方法扩展到比例指标。[STATE 原论文（KDD 2024）](https://arxiv.org/abs/2407.16337)

它的定位是**针对重尾结果分布的专门建模/估计框架**，而不是给 CUPED 加一个稳健标准误就等价得到 STATE。评价时需明确：目标仍是原始算术平均处理效应，还是鲁棒模型下的另一种位置/效应量？极端值是噪声、数据错误还是有业务意义的真实用户？如果指标本身要代表总收入，简单压低高付费用户权重可能提升统计稳定度，却改变决策含义。

不要把论文所报告的“超过 50% 方差缩减”直接当作通用承诺；它来自作者的模拟及特定平台数据，并依赖模型和比较基准。

## 6. 实验期信息：更强预测力与更高偏差风险

只用实验前变量最安全，但对稀疏、延迟或低频指标，实验前信号可能较弱。2026 年 Lin 与 Crespo 在 CLeaR/PMLR 发表的研究提出结合 pre-experiment 与 in-experiment 数据的方差缩减框架，并在 Etsy 多场在线实验中评估额外方差收益。[PMLR 2026 原论文](https://proceedings.mlr.press/v323/lin26a.html)

关键边界是：**实验发生后观测到的变量可能已经受处理影响。**若直接把处理后的中介变量、曝光量、点击量或触发状态作为普通协变量调整，可能改变 estimand、引入 post-treatment bias，甚至把真实处理效果部分“控制掉”。论文框架对候选变量和估计量有专门条件与推断，而非授权把任意实验期变量塞进 CUPED。

采用这类方法前应确认：候选实验期变量是否对处理不敏感/均值平衡、该条件如何验证、是否跨实验或用独立数据筛选、估计目标是否仍是原始 ITT、标准误是否与变量筛选和估计流程匹配。如果做不到，优先使用预处理变量、可识别的分层设计或独立确认。

## 7. Switchback：必须按设计结构做方差缩减

Switchback 常用于网络干扰明显的市场：以地域和时间窗等集群/时段为分配单位轮换处理，而不是将每个用户独立随机。其估计方差受时间自相关、集群数、簇大小不平衡、carryover 和跨集群溢出影响。

DoorDash 的 CUPAC 工程文章及其 switchback 技术稿说明，可用需求、供给、地域、时段等处理前/外生预测信号提高 switchback 灵敏度。[DoorDash CUPAC 实践](https://careersatdoordash.com/blog/improving-experimental-power-through-control-using-predictions-as-covariate-cupac/)；[Switchback CUPAC 技术稿](https://www.researchgate.net/publication/345698207_Control_Using_Predictions_as_Covariates_in_Switchback_Experiments)。这些是行业案例/技术稿，不能取代当前实验的设计感知推断。

截至本文撰写时（2026-10-18），又有面向 switchback 的设计感知方差缩减新工作，包括 CUPED/CUPAC/DR 的 regime 比较，以及基于多个历史滞后、周期时间特征、簇与小时固定效应的扩展 CUPED；相关工作目前以 2026 arXiv 预印本为主，证据成熟度低于经过多场景外部复核的生产方法。[Switchback 方差缩减比较（预印本）](https://arxiv.org/abs/2606.27662)；[多变量 switchback CUPED（预印本）](https://arxiv.org/abs/2608.24038)

## 8. 如何选择：不要按“新”选，要按瓶颈选

| 现有瓶颈 | 优先评估 | 先做的验证 |
| --- | --- | --- |
| 历史同指标已很有预测力 | 经典 CUPED | 估计样本外相关性、方差比和调整后的标准误 |
| 可用预处理特征丰富，关系明显非线性 | CUPAC / MLRATE | 时间外验证、交叉拟合、A/A 校准、推断覆盖率 |
| 重尾/极端值支配方差 | 先检查数据质量与 estimand，再评估 STATE、稳健估计、截尾等 | 真实与异常尾部拆解；保持业务效应定义一致；做敏感性分析 |
| 预处理预测信息弱、实验期有高预测力变量 | 研究专用的 pre + in-experiment 方法 | 变量处理敏感性、偏差/覆盖率、外部验证；严禁随意调整处理中介 |
| 市场网络干扰导致 switchback | 设计感知 CUPAC/协变量调整 | 以随机化单位聚类推断，检查时间自相关、carryover 和簇数 |

## 9. 研究与上线的审计清单

- 这项方法是经典 CUPED 的等价写法、工程扩展，还是改变了目标估计量/数据假设的新估计器？
- 目标是 ITT 算术平均效应、分层加权效应，还是鲁棒位置参数/其他效应？
- 协变量何时产生？会不会被处理影响？是否在训练/选择阶段泄漏了当前实验结果？
- 方差缩减数字是在训练内、A/A、模拟注入、单一公司生产数据，还是跨场景独立验证中得到？
- p 值、区间和标准误是否覆盖模型拟合、分层/筛选及集群/时序依赖？
- 结果是否与简单差分、经典 CUPED 并列报告？是否验证零效应下的假阳性率/区间覆盖率？
- 提升灵敏度后，是否保留预设检验、多重比较、停止规则和数据质量治理？

**总原则**：扩展模型只应在它解决了明确的方差瓶颈、同时保留目标 estimand 和校准推断时投入使用。复杂度本身不是“前沿价值”。

## 附录：原始论文与延伸资料

1. **CUPED 原始论文**：Deng, Xu, Kohavi & Walker, “Improving the Sensitivity of Online Controlled Experiments by Utilizing Pre-Experiment Data,” WSDM 2013. [DOI](https://doi.org/10.1145/2433396.2433413)；[作者公开 PDF](https://www.exp-platform.com/Documents/2013-02-CUPED-ImprovingSensitivityOfControlledExperiments.pdf)。这是本文讨论的基础方法来源。
2. **CUPAC**：DoorDash, [Improving Experimental Power through Control Using Predictions as Covariate](https://careersatdoordash.com/blog/improving-experimental-power-through-control-using-predictions-as-covariate-cupac/)（公司工程实践，2020）。
3. **机器学习回归调整 / MLRATE**：Guo et al., “Machine Learning for Variance Reduction in Online Experiments,” NeurIPS 2021. [论文页面](https://papers.nips.cc/paper_files/paper/2021/hash/488b084119a1c7a4950f00706ec7ea16-Abstract.html)；[论文 PDF](https://proceedings.neurips.cc/paper/2021/file/488b084119a1c7a4950f00706ec7ea16-Paper.pdf)。
4. **大规模协变量调整与实践风险**：Masoero, Hains & McQueen, “Leveraging Covariate Adjustments at Scale in Online A/B Testing,” KDD 2023 Workshop. [Amazon Science 页面](https://www.amazon.science/publications/leveraging-covariate-adjustments-at-scale-in-online-a-b-testing)；[论文 PDF](https://assets.amazon.science/40/8e/b774d62741159f2016f5e3978630/leveraging-covariate-adjustments-at-scale-in-online-a-b-testing.pdf)。
5. **STATE**：Zhou et al., “STATE: A Robust ATE Estimator of Heavy-Tailed Metrics for Variance Reduction in Online Controlled Experiments,” KDD 2024. [arXiv 论文](https://arxiv.org/abs/2407.16337)；[DOI](https://doi.org/10.1145/3637528.3672352)。
7. **Pre + in-experiment covariates**：Lin & Crespo, “Variance Reduction Combining Pre-Experiment and In-Experiment Data,” CLeaR 2026, PMLR 323:699–717. [PMLR 页面与论文](https://proceedings.mlr.press/v323/lin26a.html)。
8. **Switchback 专用前沿研究（预印本，未视为定论）**：[Design-Aware Variance Reduction for Switchback Experiments](https://arxiv.org/abs/2606.27662)；[CUPED on Steroids: Multivariate Covariate Adjustment for Switchback Experiments](https://arxiv.org/abs/2608.24038)。
