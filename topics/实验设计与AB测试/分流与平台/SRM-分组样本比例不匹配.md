---
title: "分组样本比例不匹配（SRM）：检测、诊断与处置"
created: 2026-10-09
updated: 2026-10-18
tags: [llm-wiki, ab-test, SRM, data-quality]
source:
  - "Input/rebuild_source_2026-10-09/03_统计/Experiment难题/分组样本比例不匹配.md"
wiki_type: methods
topic: "实验设计与AB测试"
migrated_from: "03_统计/Experiment难题/分组样本比例不匹配.md"
review_status: structural
---

> 所属 Topic：[复杂场景与治理](../复杂场景与治理/index.md) · 返回[实验设计与AB测试](../index.md)

# 分组样本比例不匹配（SRM）：检测、诊断与处置

## 1. SRM 检查回答什么

SRM（Sample Ratio Mismatch）指观察到的组间样本比例，与实验配置的随机分配比例存在统计上难以由随机波动解释的偏离。它是在线实验的重要数据质量信号：当随机分组或后续观测链路出现不对称问题时，实验数据可能不再对应原定的随机比较。

SRM 不是根因诊断，也不是所有可信度问题的总检验。它能提示“期望与观测不一致”，但不能仅凭一个 p 值判断问题来自分流、埋点、用户去重、受众规则还是数据 join。即使未检出 SRM，也仍可能存在组间同向数据丢失、口径错误或处理后筛样本等问题。

## 2. 如何检测：预期比例与观察计数

### 2.1 样本单位先于检验公式

SRM 的分母必须与实验随机化单位相匹配。用户级随机分配应先检查 assignment 日志中的去重用户数；不能把请求数、曝光事件数或转化数直接当成随机化人数。曝光、触发和指标样本的比例可以作为进一步的链路诊断，但应与 assignment SRM 分开解释。

设实验有 $K$ 个组，总随机化单位数为 $N$，配置给第 $k$ 组的预期比例为 $p_k$，则该组期望样本数为 $E_k=Np_k$，观察到的样本数为 $O_k$。Pearson 卡方统计量为：

$$
\chi^2=\sum_{k=1}^{K}\frac{(O_k-E_k)^2}{E_k}
$$

在独立多项分配且期望计数足以支持渐近近似时，统计量可与自由度 $K-1$ 的卡方分布比较，并据此计算 p 值。若是集群随机、区组/分层随机或其他非简单分配，应采用与设计相符的检验或模拟，不能机械套用上述参考分布。

### 2.2 最小计算例子

**示意：** 10,000 名用户计划按 50/50 随机分配，assignment 表中实际记录 A 组 4,700 人、B 组 5,300 人。两组期望人数各为 5,000：

$$
\chi^2=\frac{(4700-5000)^2}{5000}+\frac{(5300-5000)^2}{5000}=36
$$

在二组情况下自由度为 1；该结果提示比例偏离极不寻常，应暂停直接解释效果并调查数据链路。统计检验只说明观察结果与预期比例不相容，不会指出偏离原因。此例用于说明计算，不构成通用阈值建议。

### 2.3 告警规则不只是“看 p 是否小于 0.05”

阈值取决于平台监控目的、样本规模、检查频率和可接受的误报/漏报代价。用户量很大时，极小的比例偏差也可能得到很小的 p 值；运行中不断重复查看还会增加报警机会。因此应明确：

- 采用哪个随机化单位、数据源、分母、观察窗口和预期分配比例；
- 哪些阶段及哪些关键分层会触发质量告警；
- 如何处理重复监控、数据延迟和暂时未成熟的计数；
- 告警后谁负责诊断、在什么条件下恢复效果分析。

不要根据当次实验的结果临时挑选检验阈值或分层。Microsoft ExP 的公开实践将 SRM 纳入在线实验质量告警；KDD 论文将其描述为多类数据质量故障的征兆，并强调需诊断根因。

## 3. 常见根因：比例在哪一环开始偏离

| 链路位置 | 常见原因 | 典型表现 |
|---|---|---|
| 分配配置/随机化 | 分流代码或配置错误、随机化键不稳定、重复入组/掉组、实验运行中调整流量 | assignment 计数已偏离配置；可能从特定端、版本、人群或时间开始 |
| 受众过滤/触发 | 两组使用不同过滤条件；触发条件记录不全；分析只保留受处理影响的触发者 | assignment 比例正常，triggered 人群比例异常 |
| 曝光/处理交付 | 某个 variant 加载失败、崩溃，或曝光事件在一组漏记 | assignment 接近预期，exposure 之后的漏斗出现偏离 |
| 结果遥测 | 客户端埋点丢失、服务端/客户端口径差异、去重或 join 逻辑有组别差异 | 原始 assignment 正常，指标样本或宽表出现 SRM |
| 时间与配置变更 | 实验中途改流量、版本、人群或指标口径，但未按时间段记录 | 全周期比例异常，或偏离集中在变更之后 |

SRM 往往像“发烧”一样指向系统有异常，却需要沿数据产生链路追根因。Microsoft/KDD 的 SRM 诊断研究也将其定位为多种故障的共同症状，而非独立的错误类型。

## 4. 诊断流程：先确定偏离发生在哪张表

```text
1. 核对实验配置、分配比例、随机化单位和计数窗口
        ↓
2. 检查 assignment 表：实际被分到各组的单元数是否偏离？
        ↓
3. 若 assignment 正常，依次检查 exposure → trigger → metric 样本
        ↓
4. 按端、版本、渠道、日期、人群或数据表定位偏离起点
        ↓
5. 对照分流/埋点/客户端/指标变更记录，提出并验证根因
        ↓
6. 修复或重建数据，再按同一预设口径复核
```

建议至少保留 assignment、exposure、trigger 和 outcome 的独立计数。若只剩最终分析宽表，通常很难区分随机分配错误与后续观测链路错误。

## 5. 处置原则

| 诊断结果 | 处理建议 |
|---|---|
| 分流或配置错误 | 暂停效果结论；修复配置/代码后重新运行，不能把问题当作普通抽样波动 |
| 某组埋点或数据连接丢失 | 若能从可信原始日志补齐，重建数据后重新做质量检查；无法恢复时，标记当前分析不可直接用于原决策 |
| 中途调流或版本变化 | 保留变更时间线；只有阶段边界明确、估计目标可解释且数据可比时，才考虑分阶段分析 |
| 仅某端/渠道异常 | 先查异常机制；是否限定人群或分层报告应由事前目标与故障范围决定，不要为得到显著结果事后删组 |
| assignment 正常而触发样本异常 | 检查触发规则及日志；主要分析通常回到按随机分配定义的 ITT，触发分析需另行说明选择条件和因果解释限制 |
| 根因无法定位或无法修复 | 暂停效果解释；记录限制，修复链路后重做，或重新定义可回答的问题 |

核心原则：**SRM 未解释前，不要仅凭统计显著性做上线决策；也不要通过随意删样本、改窗口或事后加权把 SRM“修正掉”。**

## 6. 平台应提供的预防与监控能力

- 正式实验前支持 A/A 或空转，覆盖实际分流和日志链路；
- 实时记录预期配置与实际 assignment 计数，支持按预定规则报警；
- 提供分端、版本、渠道、日期等必要诊断视图；
- 将 assignment、exposure、trigger 与 outcome 计数分开保存并可追溯关联；
- 留存流量、受众、版本、指标口径等配置变更历史；
- 分析报告展示 SRM 检查、使用口径、报警处置和未解决问题。

pre-AA 是上线前的链路演练，SRM 是正式实验中的比例异常监控，二者配合但不可互相替代。pre-AA 的校准目标和适用边界见[pre-AA：正式实验前的校准与检查](../灵敏度与提效/pre-AA.md)。

## 参考资料

- Aleksander Fabijan et al., [Diagnosing Sample Ratio Mismatch in Online Controlled Experiments: A Taxonomy and Rules of Thumb for Practitioners](https://www.microsoft.com/en-us/research/publication/diagnosing-sample-ratio-mismatch-in-online-controlled-experiments-a-taxonomy-and-rules-of-thumb-for-practitioners/), KDD 2019.
- Microsoft Experimentation Platform, [Data Quality: Fundamental Building Blocks for Trustworthy A/B Testing Analysis](https://www.microsoft.com/en-us/research/articles/data-quality-fundamental-building-blocks-for-trustworthy-a-b-testing-analysis/).
- Microsoft Experimentation Platform, [Diagnosing Sample Ratio Mismatch in A/B Testing](https://www.microsoft.com/en-us/research/articles/diagnosing-sample-ratio-mismatch-in-a-b-testing/).
