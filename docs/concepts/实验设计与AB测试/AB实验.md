---
title: AB 实验
created: 2026-10-09
updated: 2026-10-09
tags: [llm-wiki, entity, experimentation]
source: ["docs/03_统计/ExperimentDesign/MOC_实验设计顶层设计.md", "docs/03_统计/ab实验/MOC_ab实验方法图谱.md"]
status: pilot
wiki_type: concepts
topic: "实验设计与AB测试"
migrated_from: "entities/AB实验.md"
review_status: structural
---

> 所属 Topic：[实验设计与AB测试](../../topics/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95.md) · 类型：概念

# AB 实验

**定义**：按预先确定的随机化单元把对象分配到不同方案，比较预先约定的结果指标，以估计干预效果。

**成立条件**：分配机制执行正确；实验单元、指标窗口与分析单元一致；溢出、样本流失和同时发生的变更得到检查。随机化解决的是组间可比性，实施偏差仍可能破坏结论。

**常见误解**：`p < 0.05` 不等于效果大，也不等于上线收益确定。还要看效应量、区间、护栏指标和实验质量。

**来源与延伸**：[实验设计](../../topics/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/ExperimentDesign__MOC_%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E9%A1%B6%E5%B1%82%E8%AE%BE%E8%AE%A1.md)；[AB 方法图谱](../../topics/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/ab%E5%AE%9E%E9%AA%8C__MOC_ab%E5%AE%9E%E9%AA%8C%E6%96%B9%E6%B3%95%E5%9B%BE%E8%B0%B1.md)；[随机化与因果识别](../../relationships/%E9%9A%8F%E6%9C%BA%E5%8C%96%E4%B8%8E%E5%9B%A0%E6%9E%9C%E8%AF%86%E5%88%AB.md)。
