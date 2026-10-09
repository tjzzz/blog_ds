---
title: "实验设计与AB测试"
created: 2026-10-09
updated: 2026-10-09
tags: [llm-wiki, index]
source: []
wiki_type: topic
review_status: structural
topic: "实验设计与AB测试"
---


# 实验设计与AB测试

设计可比较的实验，检查执行质量，估计效果并做上线决策。

## 关键问题

怎样设计并执行可信的线上对照实验？

## 建议阅读路线

定义目标和实验单元 → 随机分配与样本量 → 运行监控 → 效应估计 → 护栏和上线决策。

**关联 Topic**：[统计学基础](%E7%BB%9F%E8%AE%A1%E5%AD%A6%E5%9F%BA%E7%A1%80.md)、[因果推断](%E5%9B%A0%E6%9E%9C%E6%8E%A8%E6%96%AD.md)、[业务指标与诊断](%E4%B8%9A%E5%8A%A1%E6%8C%87%E6%A0%87%E4%B8%8E%E8%AF%8A%E6%96%AD.md)。

从下列分类进入全文。这里的分类是导航；页面保留原文并标注迁移来源，内容核验按专题继续维护。

## 专题资料（2）

- [MOC_实验设计顶层设计](%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/ExperimentDesign__MOC_%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E9%A1%B6%E5%B1%82%E8%AE%BE%E8%AE%A1.md)
- [MOC_ab实验方法图谱](%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/ab%E5%AE%9E%E9%AA%8C__MOC_ab%E5%AE%9E%E9%AA%8C%E6%96%B9%E6%B3%95%E5%9B%BE%E8%B0%B1.md)

## 概念（10）

- [ab-test](../concepts/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/ExperimentDesign__ab-test.md)
- [interleaving介绍](../concepts/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/ExperimentDesign__interleaving%E4%BB%8B%E7%BB%8D.md)
- [☆辛普森悖论](../concepts/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/Experiment%E9%9A%BE%E9%A2%98__%E2%98%86%E8%BE%9B%E6%99%AE%E6%A3%AE%E6%82%96%E8%AE%BA.md)
- [时序干扰与长期效应](../concepts/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/Experiment%E9%9A%BE%E9%A2%98__%E6%97%B6%E5%BA%8F%E5%B9%B2%E6%89%B0%E4%B8%8E%E9%95%BF%E6%9C%9F%E6%95%88%E5%BA%94.md)
- [触发偏差与幸存者偏差](../concepts/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/Experiment%E9%9A%BE%E9%A2%98__%E8%A7%A6%E5%8F%91%E5%81%8F%E5%B7%AE%E4%B8%8E%E5%B9%B8%E5%AD%98%E8%80%85%E5%81%8F%E5%B7%AE.md)
- [02_贝叶斯胜率](../concepts/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/ab%E5%AE%9E%E9%AA%8C__02_%E8%B4%9D%E5%8F%B6%E6%96%AF%E8%83%9C%E7%8E%87.md)
- [07_网络效应与干扰](../concepts/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/ab%E5%AE%9E%E9%AA%8C__07_%E7%BD%91%E7%BB%9C%E6%95%88%E5%BA%94%E4%B8%8E%E5%B9%B2%E6%89%B0.md)
- [业务_如何搭建ab平台](../concepts/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/%E4%B8%9A%E5%8A%A1_%E5%A6%82%E4%BD%95%E6%90%AD%E5%BB%BAab%E5%B9%B3%E5%8F%B0.md)
- [AB实验](../concepts/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/AB%E5%AE%9E%E9%AA%8C.md)
- [CUPED](../concepts/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/CUPED.md)

## 方法（19）

- [01_实验可行性分析](../methods/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/ExperimentDesign__01_%E5%AE%9E%E9%AA%8C%E5%8F%AF%E8%A1%8C%E6%80%A7%E5%88%86%E6%9E%90.md)
- [02_实验方案设计](../methods/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/ExperimentDesign__02_%E5%AE%9E%E9%AA%8C%E6%96%B9%E6%A1%88%E8%AE%BE%E8%AE%A1.md)
- [03_抽样平台_流量分组](../methods/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/ExperimentDesign__03_%E6%8A%BD%E6%A0%B7%E5%B9%B3%E5%8F%B0_%E6%B5%81%E9%87%8F%E5%88%86%E7%BB%84.md)
- [04_实验指标设计](../methods/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/ExperimentDesign__04_%E5%AE%9E%E9%AA%8C%E6%8C%87%E6%A0%87%E8%AE%BE%E8%AE%A1.md)
- [05_实验上线机制](../methods/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/ExperimentDesign__05_%E5%AE%9E%E9%AA%8C%E4%B8%8A%E7%BA%BF%E6%9C%BA%E5%88%B6.md)
- [AB实验常见问题](../methods/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/ExperimentDesign__AB%E5%AE%9E%E9%AA%8C%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98.md)
- [实验方式](../methods/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/ExperimentDesign__%E5%AE%9E%E9%AA%8C%E6%96%B9%E5%BC%8F.md)
- [流量分组_各流量域架构.excalidraw](../methods/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/ExperimentDesign__%E6%B5%81%E9%87%8F%E5%88%86%E7%BB%84_%E5%90%84%E6%B5%81%E9%87%8F%E5%9F%9F%E6%9E%B6%E6%9E%84.excalidraw.md)
- [☆如何提升实验灵敏度](../methods/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/Experiment%E9%9A%BE%E9%A2%98__%E2%98%86%E5%A6%82%E4%BD%95%E6%8F%90%E5%8D%87%E5%AE%9E%E9%AA%8C%E7%81%B5%E6%95%8F%E5%BA%A6.md)
- [分组样本比例不匹配](../methods/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/Experiment%E9%9A%BE%E9%A2%98__%E5%88%86%E7%BB%84%E6%A0%B7%E6%9C%AC%E6%AF%94%E4%BE%8B%E4%B8%8D%E5%8C%B9%E9%85%8D.md)
- [多重检验与显著性窥探](../methods/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/Experiment%E9%9A%BE%E9%A2%98__%E5%A4%9A%E9%87%8D%E6%A3%80%E9%AA%8C%E4%B8%8E%E6%98%BE%E8%91%97%E6%80%A7%E7%AA%A5%E6%8E%A2.md)
- [高阶实验难题_指标污染与口径漂移](../methods/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/Experiment%E9%9A%BE%E9%A2%98__%E9%AB%98%E9%98%B6%E5%AE%9E%E9%AA%8C%E9%9A%BE%E9%A2%98_%E6%8C%87%E6%A0%87%E6%B1%A1%E6%9F%93%E4%B8%8E%E5%8F%A3%E5%BE%84%E6%BC%82%E7%A7%BB.md)
- [高阶实验难题_网络效应与溢出干扰](../methods/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/Experiment%E9%9A%BE%E9%A2%98__%E9%AB%98%E9%98%B6%E5%AE%9E%E9%AA%8C%E9%9A%BE%E9%A2%98_%E7%BD%91%E7%BB%9C%E6%95%88%E5%BA%94%E4%B8%8E%E6%BA%A2%E5%87%BA%E5%B9%B2%E6%89%B0.md)
- [01_假设检验与p值](../methods/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/ab%E5%AE%9E%E9%AA%8C__01_%E5%81%87%E8%AE%BE%E6%A3%80%E9%AA%8C%E4%B8%8Ep%E5%80%BC.md)
- [03_序贯分析](../methods/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/ab%E5%AE%9E%E9%AA%8C__03_%E5%BA%8F%E8%B4%AF%E5%88%86%E6%9E%90.md)
- [04_CUPED与方差缩减](../methods/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/ab%E5%AE%9E%E9%AA%8C__04_CUPED%E4%B8%8E%E6%96%B9%E5%B7%AE%E7%BC%A9%E5%87%8F.md)
- [05_MAB与客户分群路由](../methods/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/ab%E5%AE%9E%E9%AA%8C__05_MAB%E4%B8%8E%E5%AE%A2%E6%88%B7%E5%88%86%E7%BE%A4%E8%B7%AF%E7%94%B1.md)
- [06_HTE与Uplift个性化](../methods/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/ab%E5%AE%9E%E9%AA%8C__06_HTE%E4%B8%8EUplift%E4%B8%AA%E6%80%A7%E5%8C%96.md)
- [08_实验治理与护栏](../methods/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/ab%E5%AE%9E%E9%AA%8C__08_%E5%AE%9E%E9%AA%8C%E6%B2%BB%E7%90%86%E4%B8%8E%E6%8A%A4%E6%A0%8F.md)

## 先前试点说明（保留）

# 统计与实验

## 核心问题

如何设计可信的比较，估计策略效果，并决定是否上线？先确认指标、实验单元、随机分配和样本量，再检查实施质量，最后解释效应量与不确定性。

## 知识地图

1. **设计**：[实验设计顶层设计](%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/ExperimentDesign__MOC_%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E9%A1%B6%E5%B1%82%E8%AE%BE%E8%AE%A1.md)、[实验方案设计](../methods/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/ExperimentDesign__02_%E5%AE%9E%E9%AA%8C%E6%96%B9%E6%A1%88%E8%AE%BE%E8%AE%A1.md)。
2. **推断**：[AB 实验方法图谱](%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/ab%E5%AE%9E%E9%AA%8C__MOC_ab%E5%AE%9E%E9%AA%8C%E6%96%B9%E6%B3%95%E5%9B%BE%E8%B0%B1.md)、[假设检验与 p 值](../methods/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/ab%E5%AE%9E%E9%AA%8C__01_%E5%81%87%E8%AE%BE%E6%A3%80%E9%AA%8C%E4%B8%8Ep%E5%80%BC.md)。
3. **提效**：[CUPED 与方差缩减](../methods/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/ab%E5%AE%9E%E9%AA%8C__04_CUPED%E4%B8%8E%E6%96%B9%E5%B7%AE%E7%BC%A9%E5%87%8F.md)、[实验灵敏度](../methods/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/Experiment%E9%9A%BE%E9%A2%98__%E2%98%86%E5%A6%82%E4%BD%95%E6%8F%90%E5%8D%87%E5%AE%9E%E9%AA%8C%E7%81%B5%E6%95%8F%E5%BA%A6.md)。
4. **质量**：[实验治理与护栏](../methods/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/ab%E5%AE%9E%E9%AA%8C__08_%E5%AE%9E%E9%AA%8C%E6%B2%BB%E7%90%86%E4%B8%8E%E6%8A%A4%E6%A0%8F.md)、[样本比例不匹配](../methods/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/Experiment%E9%9A%BE%E9%A2%98__%E5%88%86%E7%BB%84%E6%A0%B7%E6%9C%AC%E6%AF%94%E4%BE%8B%E4%B8%8D%E5%8C%B9%E9%85%8D.md)。

## 关键关系

- [随机化怎样支撑因果识别](../relationships/%E9%9A%8F%E6%9C%BA%E5%8C%96%E4%B8%8E%E5%9B%A0%E6%9E%9C%E8%AF%86%E5%88%AB.md)
- [方差缩减怎样改善实验效率](../relationships/%E5%AE%9E%E9%AA%8C%E6%95%88%E7%8E%87%E4%B8%8E%E6%96%B9%E5%B7%AE%E7%BC%A9%E5%87%8F.md)
- [实验方法选择](../syntheses/%E5%AE%9E%E9%AA%8C%E6%96%B9%E6%B3%95%E9%80%89%E6%8B%A9.md)

## 待核对

旧笔记中关于贝叶斯方法、可选停止与错误率的表述需补一手统计来源，不能只依据旧卡片相互引用。
