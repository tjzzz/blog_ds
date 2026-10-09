---
update_time: "2026-09-13 20:10:59 CST"
tags:
  - statistics/experiment-design
  - experiment/ab-test
title: "ab-test"
created: 2026-10-09
updated: 2026-10-09
source: ["Input/rebuild_source_2026-10-09/03_统计/ExperimentDesign/ab-test.md"]
wiki_type: concepts
topic: "实验设计与AB测试"
migrated_from: "03_统计/ExperimentDesign/ab-test.md"
review_status: structural
---

> 所属 Topic：[实验设计与AB测试](../../topics/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95.md) · 类型：概念

# ab-test

## 1. 基本原理

AB Test 的核心是随机化实验和假设检验：

- 通过随机分组，让实验组和对照组在实验处理之外尽量可比；
- 通过指标差异和统计检验，判断观察到的差异是否可能由随机波动造成；
- 通过护栏指标、分层分析和长期观察，判断策略是否适合上线。

## 2. 敏感性与样本量

AB 实验是否“检得出来”，本质上取决于组间差异、样本量和指标方差。

这部分已整理到实验难题文档：

- [☆如何提升实验灵敏度](../../methods/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/Experiment%E9%9A%BE%E9%A2%98__%E2%98%86%E5%A6%82%E4%BD%95%E6%8F%90%E5%8D%87%E5%AE%9E%E9%AA%8C%E7%81%B5%E6%95%8F%E5%BA%A6.md)

其中包括：

- t 检验视角下的敏感性公式；
- 增加样本量；
- metric transformation / 长尾指标处理；
- CUPED 方差缩减；
- post-stratification；
- variance-weighted estimators；
- 更敏感的前置指标和 interleaving。

样本量基础见：

- [参数估计-样本量的确定](../../methods/%E7%BB%9F%E8%AE%A1%E5%AD%A6%E5%9F%BA%E7%A1%80/%E5%8F%82%E6%95%B0%E4%BC%B0%E8%AE%A1-%E6%A0%B7%E6%9C%AC%E9%87%8F%E7%9A%84%E7%A1%AE%E5%AE%9A.md)

## 3. 常见问题

AB 实验常见问题已单独整理：

- [AB实验常见问题](../../methods/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/ExperimentDesign__AB%E5%AE%9E%E9%AA%8C%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98.md)

典型问题：实验里指标上涨，但全量上线后大盘持平。排查时优先看：

1. 实验是否可信：样本量、显著性、SRM、日志质量；
2. 实验人群和全量人群是否一致；
3. 是否存在新奇效应、长期效应或外部环境变化；
4. 全量上线实现是否和实验 treatment 一致。

## 4. Reference

- Variance-Weighted Estimators to Improve Sensitivity in Online Experiments
- William Fithian and Daniel Ting. 2017. Family learning: nonparametric statistical inference with parametric efficiency.
