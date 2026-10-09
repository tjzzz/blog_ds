---
title: 偏差与识别假设
update_time: "2026-09-13 21:37:43 CST"
tags:
  - statistics/causal-inference
created: 2026-10-09
updated: 2026-10-09
source: ["Input/rebuild_source_2026-10-09/03_统计/CausalAnalysis/06_偏差与识别假设_混杂选择偏差内生性.md"]
wiki_type: concepts
topic: "因果推断"
migrated_from: "03_统计/CausalAnalysis/06_偏差与识别假设_混杂选择偏差内生性.md"
review_status: structural
---

> 所属 Topic：[因果推断](../../topics/%E5%9B%A0%E6%9E%9C%E6%8E%A8%E6%96%AD.md) · 类型：概念

# 06. 偏差与识别假设：混杂、选择偏差、内生性

因果方法的核心不是模型，而是识别假设。不同方法本质上是在不同假设下构造可信反事实。

## 1. 常见偏差

| 偏差 | 现象 | 典型修正方向 |
|---|---|---|
| 混杂 | 第三个变量同时影响 treatment 和 outcome | 控制变量、Matching、PSM、回归调整 |
| 选择偏差 | 谁进入处理组不是随机的 | PSM、IPW、DID、IV |
| 内生性 | treatment 与误差项相关 | IV、自然实验 |
| 幸存者偏差 | 只看留下来的人 | 重新定义分析总体、补齐流失路径 |
| 触发偏差 | 只看真正触发策略的人 | ITT / TOT 区分、触发前变量控制 |
| 时序干扰 | 策略前后环境变化 | DID、合成控制、时间固定效应 |
| 溢出效应 | 处理组影响对照组 | 网络实验、cluster randomization |

## 2. 识别假设比估计方法更重要

同一个模型，在不同假设下含义完全不同。

例如回归：

```text
Y ~ T + X
```

只有当 $X$ 已经充分控制混杂时，$T$ 的系数才可以解释为因果效应。否则它只是条件相关。

## 3. 方法和假设对应

| 方法 | 主要假设 |
|---|---|
| Matching / PSM | 可观测变量充分控制选择偏差 |
| DID | 若没有处理，处理组和对照组会保持平行趋势 |
| IV | 工具变量只通过 treatment 影响 outcome |
| 合成控制 | 多个对照单元加权后可复现处理单元的反事实趋势 |
| RDD | 阈值附近个体不能精确操纵 treatment |
| Uplift / CATE | 训练数据的 treatment 分配机制可信 |

## 4. 面向业务的排查顺序

1. treatment 是自然选择还是业务分配？
2. 处理前，处理组和对照组是否已经不同？
3. 是否有处理前趋势数据？
4. 是否存在外部冲击或工具变量？
5. 是否存在用户间相互影响？
6. 是否需要估计整体增量还是分人群增量？

相关旧文档：

- [概念与研究框架_因果](../../methods/%E5%9B%A0%E6%9E%9C%E6%8E%A8%E6%96%AD/CausalAnalysis__04_%E6%BD%9C%E5%9C%A8%E7%BB%93%E6%9E%9C%E6%A1%86%E6%9E%B6_ITE_ATE_ATT_CATE.md)
- [因果效应估计方法](../../methods/%E5%9B%A0%E6%9E%9C%E6%8E%A8%E6%96%AD/CausalAnalysis__03_%E6%97%A0%E5%AE%9E%E9%AA%8C%E5%9C%BA%E6%99%AF%E6%95%88%E6%9E%9C%E8%AF%84%E4%BC%B0%E5%86%B3%E7%AD%96%E6%A0%91.md)
