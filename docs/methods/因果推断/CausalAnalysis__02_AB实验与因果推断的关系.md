---
title: AB实验与因果推断的关系
update_time: "2026-09-13 21:37:43 CST"
tags:
  - statistics/causal-inference
  - statistics/experiment-design
created: 2026-10-09
updated: 2026-10-09
source: ["Input/rebuild_source_2026-10-09/03_统计/CausalAnalysis/02_AB实验与因果推断的关系.md"]
wiki_type: methods
topic: "因果推断"
migrated_from: "03_统计/CausalAnalysis/02_AB实验与因果推断的关系.md"
review_status: structural
---

> 所属 Topic：[因果推断](../../topics/%E5%9B%A0%E6%9E%9C%E6%8E%A8%E6%96%AD.md) · 类型：方法

# 02. AB实验与因果推断的关系

AB 实验本质上也是因果推断，只是它通过随机化把最难的问题提前解决了。

## 1. 为什么 AB 是金标准

AB 实验通过随机分组，让实验组和对照组在期望上只有 treatment 不同：

```text
随机化前：用户差异可能影响结果
随机化后：用户差异在实验组和对照组之间平均抵消
```

因此，在随机化有效、无干扰、实验执行一致的前提下：

$$
ATE pprox E(Y|T=1) - E(Y|T=0)
$$

## 2. 因果推断补齐 AB 做不了的场景

| 场景 | AB 的问题 | 可考虑的因果方法 |
|---|---|---|
| 策略已全量上线 | 没有随机对照组 | DID、合成控制 |
| 只能按国家/城市/版本分批上线 | 分组粒度粗，样本单元少 | DID、合成控制 |
| 功能由用户主动选择使用 | 选择偏差严重 | Matching、PSM、IPW |
| treatment 与未观测因素相关 | 内生性 | IV |
| 规则按阈值触发 | 无法随机，但阈值附近近似随机 | RDD |
| 关注哪些人更应该被触达 | 平均效应不够 | CATE、Uplift |

## 3. AB 与观察性因果推断的关键区别

| 维度 | AB 实验 | 观察性因果推断 |
|---|---|---|
| 分组 | 随机分组 | 自然发生或业务规则决定 |
| 可信度来源 | 随机化 | 识别假设 |
| 核心风险 | 实验污染、干扰、样本不足 | 混杂、选择偏差、内生性 |
| 主要产出 | 实验组 vs 对照组差异 | 经识别假设修正后的反事实估计 |

## 4. 和实验设计模块的衔接

如果业务能做 AB，优先走实验体系：

- [实验方案设计](../%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/ExperimentDesign__02_%E5%AE%9E%E9%AA%8C%E6%96%B9%E6%A1%88%E8%AE%BE%E8%AE%A1.md)
- [抽样平台与流量分组](../%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/ExperimentDesign__03_%E6%8A%BD%E6%A0%B7%E5%B9%B3%E5%8F%B0_%E6%B5%81%E9%87%8F%E5%88%86%E7%BB%84.md)
- [实验指标设计](../%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/ExperimentDesign__04_%E5%AE%9E%E9%AA%8C%E6%8C%87%E6%A0%87%E8%AE%BE%E8%AE%A1.md)
- [实验上线机制](../%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/ExperimentDesign__05_%E5%AE%9E%E9%AA%8C%E4%B8%8A%E7%BA%BF%E6%9C%BA%E5%88%B6.md)

如果 AB 不能做，或 AB 已经出现偏差，再进入本模块的方法体系。
