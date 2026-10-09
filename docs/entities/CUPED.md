---
title: CUPED
created: 2026-10-09
updated: 2026-10-09
tags: [llm-wiki, entity, experimentation, variance-reduction]
source: ["docs/03_统计/ab实验/04_CUPED与方差缩减.md", "docs/03_统计/Experiment难题/☆如何提升实验灵敏度.md"]
status: pilot
---
# CUPED

**定义**：利用干预前、与结果相关的协变量，减少实验指标估计的方差。它改变估计精度，不替代随机化或修复分流错误。

**使用前检查**：协变量必须在处理前确定；明确缺失值和口径；比较调整前后的估计与标准误；检查结果是否因异常值或人群变化而不稳。

**来源与延伸**：[CUPED 与方差缩减](../03_统计/ab实验/04_CUPED与方差缩减.md)；[实验灵敏度](../03_统计/Experiment难题/☆如何提升实验灵敏度.md)；[实验效率与方差缩减](../relationships/实验效率与方差缩减.md)。
