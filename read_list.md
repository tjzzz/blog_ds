---
title: DS 阅读清单
wiki_type: reading-list
update_time: 2026-10-17
---

# DS 阅读清单

记录梳理笔记时发现、值得后续用 `$tool-read-explain` 逐篇精读的资料。按 topic 归类；状态约定：`待读` → `阅读中` → `已读`。精读完成后，可补充阅读笔记链接或关键问题。


## A/B 实验与贝叶斯胜率

| 资料 | 关注点 | 状态 |
| --- | --- | --- |
| [Bayesian A/B Testing for Business Decisions](https://arxiv.org/abs/2003.02769) | 多臂/多方案下如何用后验概率回答业务问题；比较 `P(best)`、胜过对照及有意义提升等决策目标。 | 待读 |
| [Spotify: Why Spotify Is Not Using Bayesian A/B Testing](https://www.engineering.atspotify.com/2026/9/why-spotify-is-not-using-bayesian-a-b-testing) | 贝叶斯 A/B 不是单一方法；先验、停止规则与目标保证如何影响结果，及 Spotify 不采用贝叶斯模式的理由。 | 待读 |
| [Firebase A/B Testing inference methods](https://firebase.google.com/docs/ab-testing/ab-concepts) | Google Firebase 产品文档中的频率学推断：t 检验、比例 z 检验、p 值和置信区间。注意这是 Firebase 产品实践，不代表 Google 全部内部平台。 | 待读 |

## 多重比较、赢家诅咒与经验贝叶斯

| 资料 | 关注点 | 状态 |
| --- | --- | --- |
| [Empirical Bayes Estimation of Treatment Effects with Many A/B Tests: An Overview](https://pubs.aeaweb.org/doi/10.1257/pandp.20191003) | 多个实验中如何区分真实有效果的方案与“运气好”的赢家；经验贝叶斯收缩。 | 待读 |
| [Amazon Science: Overcoming the winner’s curse](https://www.amazon.science/publications/overcoming-the-winners-curse-leveraging-bayesian-inference-to-improve-estimates-of-the-impact-of-features-launched-via-a-b-tests) | 在 Amazon 多项 A/B 测试的累计影响估计中比较贝叶斯与频率学估计；重点看先验设定错误时的表现。 | 待读 |
| [Meta: Improving Treatment Effect Estimators Through Experiment Splitting](https://ai.meta.com/research/publications/improving-treatment-effect-estimators-through-experiment-splitting/) | Facebook News Feed 实验中的效应收缩估计，以及估计方法对上线决策的影响。 | 待读 |
| [Bayesian Hybrid Shrinkage (2026, arXiv preprint)](https://arxiv.org/abs/2603.12867) | Meta 平台数据上的经验贝叶斯收缩方法；关注局部收缩、选择偏差与区间覆盖。预印本，阅读时留意证据成熟度。 | 待读 |

## 方差缩减与 CUPED

| 资料 | 关注点 | 状态 |
| --- | --- | --- |
| [Microsoft ExP: CUPED、Delta method 与 tenant 随机实验分析](https://www.microsoft.com/en-us/research/articles/why-tenant-randomized-a-b-test-is-challenging-and-tenant-pairing-may-not-work/) | CUPED、随机化单位与分析单位不一致时的方差估计，以及集群随机实验中的功效和平衡问题。 | 待读 |
| [Booking.com: How Booking.com increases the power of online experiments with CUPED](https://booking.ai/how-booking-com-increases-the-power-of-online-experiments-with-cuped-995d186fff1d) | 预实验数据如何降低在线实验指标方差、提升检验功效；含工程实现示例。 | 待读 |
| [ByteDance-affiliated authors: CUPED inference paper (2026, arXiv preprint)](https://arxiv.org/abs/2606.18750) | CUPED/回归调整、多臂与两阶段抽样中的方差估计和推断有效性；作者称相关方法已集成到字节实验平台。预印本，需区分论文结论与平台实践披露。 | 待读 |

## 序贯检验与持续监控

| 资料 | 关注点 | 状态 |
| --- | --- | --- |
| [Netflix: Sequential A/B Testing, Part 1 — Continuous Data](https://research.netflix.com/publication/sequential-a-b-testing-keeps-the-world-streaming-netflix-part-1-continuous) | 连续型指标下固定时点分析与 any-time-valid 推断；任意时点查看数据时如何保持统计有效性。 | 待读 |
| [Netflix: Sequential A/B Testing, Part 2 — Counting Processes](https://research.netflix.com/publication/sequential-a-b-testing-keeps-the-world-streaming-netflix-part-2-counting-processes) | 计数型指标的序贯 A/B 检验与持续监控。 | 待读 |
| [在线序贯检验研究](https://jmlr2020.csail.mit.edu/papers/v22/21-0383.html) | 在线实验/序贯检验的方法与理论保证。 | 待读 |

## 大规模实验平台与工程实践

| 资料 | 关注点 | 状态 |
| --- | --- | --- |
| [The Anatomy of a Large-Scale Experimentation Platform](https://doi.org/10.1109/ICSA.2018.00009) | Microsoft ExP 大规模实验平台的架构组件与设计取舍。 | 待读 |
| [Booking.com: Scaling Experimentation Quality](https://booking.ai/scaling-experimentation-quality-at-booking-com-726152ee4ef0) | Booking.com 如何将实验质量、功效规划、运行时长和决策规范纳入平台治理。 | 待读 |
| [A framework for Multi-A(rmed)/B(andit) Testing with Online FDR Control](https://papers.nips.cc/paper_files/paper/2017/file/f0204e1d3ee3e4b05de4e2ddbd39e076-Paper.pdf) | 多臂老虎机实验的分配机制、效率收益与评估限制；辨别优化流量与无偏效果评估的不同目标。 | 待读 |
