---
title: CUPED
created: 2026-10-09
updated: 2026-10-09
tags: [llm-wiki, entity, experimentation, variance-reduction]
source: ["docs/03_统计/ab实验/04_CUPED与方差缩减.md", "docs/03_统计/Experiment难题/☆如何提升实验灵敏度.md"]
status: pilot
wiki_type: concepts
topic: "实验设计与AB测试"
migrated_from: "entities/CUPED.md"
review_status: structural
---

> 所属 Topic：[实验设计与AB测试](../../topics/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95.md) · 类型：概念

# CUPED

**定义**：利用干预前、与结果相关的协变量，减少实验指标估计的方差。它改变估计精度，不替代随机化或修复分流错误。

**使用前检查**：协变量必须在处理前确定；明确缺失值和口径；比较调整前后的估计与标准误；检查结果是否因异常值或人群变化而不稳。

**来源与延伸**：[CUPED 与方差缩减](../../methods/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/ab%E5%AE%9E%E9%AA%8C__04_CUPED%E4%B8%8E%E6%96%B9%E5%B7%AE%E7%BC%A9%E5%87%8F.md)；[实验灵敏度](../../methods/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/Experiment%E9%9A%BE%E9%A2%98__%E2%98%86%E5%A6%82%E4%BD%95%E6%8F%90%E5%8D%87%E5%AE%9E%E9%AA%8C%E7%81%B5%E6%95%8F%E5%BA%A6.md)；[实验效率与方差缩减](../../relationships/%E5%AE%9E%E9%AA%8C%E6%95%88%E7%8E%87%E4%B8%8E%E6%96%B9%E5%B7%AE%E7%BC%A9%E5%87%8F.md)。
