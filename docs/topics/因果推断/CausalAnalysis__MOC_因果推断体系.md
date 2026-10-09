---
title: MOC_因果推断体系
update_time: "2026-09-13 21:51:07 CST"
tags:
  - statistics/causal-inference
  - moc
created: 2026-10-09
updated: 2026-10-09
source: ["Input/rebuild_source_2026-10-09/03_统计/CausalAnalysis/MOC_因果推断体系.md"]
wiki_type: topics
topic: "因果推断"
migrated_from: "03_统计/CausalAnalysis/MOC_因果推断体系.md"
review_status: structural
---

> 所属 Topic：[因果推断](../%E5%9B%A0%E6%9E%9C%E6%8E%A8%E6%96%AD.md) · 类型：专题资料

# 因果推断体系

> 目标：把因果推断整理成一套面向业务策略评估的知识体系，重点服务「无法做 AB 实验 / AB 结果有偏 / 需要做增量价值评估」的场景。

## 1. 学习路径


![](../../media/Pasted%20image%2020220704225439.png)

把图里的判断逻辑整理成文字版：

```text
先判断能不能随机化
  ├─ 能随机化：优先 AB 实验 / 随机对照实验
  └─ 不能随机化：进入观察性因果推断
        ├─ 有随时间推移的反复观测结果？
        │   ├─ 有对照组时间序列？
        │   │   ├─ 干预前后观测样本较大：合成控制法 / 贝叶斯结构时间序列
        │   │   └─ 干预前后观测样本较少：DID 双重差分
        │   └─ 没有对照组时间序列：单组中断时间序列分析
        └─ 不是时间序列评估？
            ├─ 通过临界点/阈值设置干预：RDD 断点回归
            ├─ 存在只通过原因变量影响结果的第三方变量：IV 工具变量
            ├─ 存在可观测干预前协变量：Matching / PSM / IPW
            └─ 关注不同人群增量收益：CATE / Uplift
```



## 2. 总览与框架

| 编号 | 文档 | 解决的问题 |
|---|---|---|
| 01 | [因果推断导论](../../methods/%E5%9B%A0%E6%9E%9C%E6%8E%A8%E6%96%AD/CausalAnalysis__01_%E5%9B%A0%E6%9E%9C%E6%8E%A8%E6%96%AD%E5%AF%BC%E8%AE%BA.md) | 为什么相关不等于因果，为什么业务评估需要因果语言 |
| 02 | [AB实验与因果推断的关系](../../methods/%E5%9B%A0%E6%9E%9C%E6%8E%A8%E6%96%AD/CausalAnalysis__02_AB%E5%AE%9E%E9%AA%8C%E4%B8%8E%E5%9B%A0%E6%9E%9C%E6%8E%A8%E6%96%AD%E7%9A%84%E5%85%B3%E7%B3%BB.md) | AB 为什么是金标准，因果推断如何补齐不能 AB 的场景 |
| 03 | [无实验场景效果评估决策树](../../methods/%E5%9B%A0%E6%9E%9C%E6%8E%A8%E6%96%AD/CausalAnalysis__03_%E6%97%A0%E5%AE%9E%E9%AA%8C%E5%9C%BA%E6%99%AF%E6%95%88%E6%9E%9C%E8%AF%84%E4%BC%B0%E5%86%B3%E7%AD%96%E6%A0%91.md) | 面对一个业务策略，如何选择 DID / PSM / IV / 合成控制等方法 |
| 04 | [潜在结果框架](../../methods/%E5%9B%A0%E6%9E%9C%E6%8E%A8%E6%96%AD/CausalAnalysis__04_%E6%BD%9C%E5%9C%A8%E7%BB%93%E6%9E%9C%E6%A1%86%E6%9E%B6_ITE_ATE_ATT_CATE.md) | ITE、ATE、ATT、CATE、反事实等核心语言 |
| 05 | [结构因果模型](../../methods/%E5%9B%A0%E6%9E%9C%E6%8E%A8%E6%96%AD/CausalAnalysis__05_%E7%BB%93%E6%9E%84%E5%9B%A0%E6%9E%9C%E6%A8%A1%E5%9E%8B_DAG%E4%B8%8Edo_calculus.md) | DAG、混杂、后门路径、do-calculus 的基本直觉 |
| 06 | [偏差与识别假设](../../concepts/%E5%9B%A0%E6%9E%9C%E6%8E%A8%E6%96%AD/CausalAnalysis__06_%E5%81%8F%E5%B7%AE%E4%B8%8E%E8%AF%86%E5%88%AB%E5%81%87%E8%AE%BE_%E6%B7%B7%E6%9D%82%E9%80%89%E6%8B%A9%E5%81%8F%E5%B7%AE%E5%86%85%E7%94%9F%E6%80%A7.md) | 混杂、选择偏差、内生性、未观测混杂为什么会让结论失真 |

## 3. 方法体系

> 方法类统一用 `编号_方法_方法名` 命名，便于看出它们属于同一个体系。

> 说明：方法文档统一使用 `07_方法_...` 前缀，表示它们都属于第 07 组「因果方法体系」；后面的中文方法名用于区分具体方法。

| 编号 | 方法 | 典型使用场景 | 核心假设 |
|---|---|---|---|
| 07 | [方法_Matching与PSM](../../methods/%E5%9B%A0%E6%9E%9C%E6%8E%A8%E6%96%AD/CausalAnalysis__%E6%96%B9%E6%B3%95_Matching%E4%B8%8EPSM.md) | 处理组和对照组可观测特征不平衡 | 可观测变量充分控制选择偏差 |
| 07 | [方法_DID双重差分](../../methods/%E5%9B%A0%E6%9E%9C%E6%8E%A8%E6%96%AD/CausalAnalysis__%E6%96%B9%E6%B3%95_DID%E5%8F%8C%E9%87%8D%E5%B7%AE%E5%88%86.md) | 有处理前后和对照组，例如策略分批上线 | 平行趋势 |
| 07 | [方法_IV工具变量](../../tools/%E5%9B%A0%E6%9E%9C%E6%8E%A8%E6%96%AD/CausalAnalysis__%E6%96%B9%E6%B3%95_IV%E5%B7%A5%E5%85%B7%E5%8F%98%E9%87%8F.md) | 核心变量内生，但存在外生冲击或工具变量 | 相关性、排除限制、独立性 |
| 07 | [方法_合成控制法](../../methods/%E5%9B%A0%E6%9E%9C%E6%8E%A8%E6%96%AD/CausalAnalysis__%E6%96%B9%E6%B3%95_%E5%90%88%E6%88%90%E6%8E%A7%E5%88%B6%E6%B3%95.md) | 单城市、单国家、单业务单元上线策略 | 可由多个对照单元加权合成反事实 |
| 07 | [方法_RDD断点回归](../../methods/%E5%9B%A0%E6%9E%9C%E6%8E%A8%E6%96%AD/CausalAnalysis__%E6%96%B9%E6%B3%95_RDD%E6%96%AD%E7%82%B9%E5%9B%9E%E5%BD%92.md) | 存在明确分数线、阈值、规则边界 | 阈值附近个体近似随机 |
| 07 | [方法_异质性处理效应与Uplift](../../methods/%E5%9B%A0%E6%9E%9C%E6%8E%A8%E6%96%AD/CausalAnalysis__%E6%96%B9%E6%B3%95_%E5%BC%82%E8%B4%A8%E6%80%A7%E5%A4%84%E7%90%86%E6%95%88%E5%BA%94%E4%B8%8EUplift.md) | 评估不同人群的增量收益，做策略分层投放 | 个体/分层处理效应可被特征解释 |

## 4. 工具实践

| 编号 | 文档 | 说明 |
|---|---|---|
| 08 | [工具_DoWhy](../../tools/%E5%9B%A0%E6%9E%9C%E6%8E%A8%E6%96%AD/CausalAnalysis__%E5%B7%A5%E5%85%B7__08_%E5%B7%A5%E5%85%B7_DoWhy.md) | 因果建模、识别、估计、反驳四步框架 |
| 08 | [工具_EconML与CausalML](../../tools/%E5%9B%A0%E6%9E%9C%E6%8E%A8%E6%96%AD/CausalAnalysis__%E5%B7%A5%E5%85%B7__08_%E5%B7%A5%E5%85%B7_EconML%E4%B8%8ECausalML.md) | CATE、DML、Uplift 等机器学习因果工具 |
| 08 | [工具_StatsModels实现PSM_DID_IV](../../tools/%E5%9B%A0%E6%9E%9C%E6%8E%A8%E6%96%AD/CausalAnalysis__%E5%B7%A5%E5%85%B7__08_%E5%B7%A5%E5%85%B7_StatsModels%E5%AE%9E%E7%8E%B0PSM_DID_IV.md) | 面试和业务落地中最常用的 Python 统计实现路线 |

> 实验疑难问题不在本目录重复维护，统一查看 [实验设计与 AB 测试 Topic](../%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95.md)（原 MOC_高阶实验难题 文件未找到）。

## 5. 资料与读书笔记

| 编号 | 文档 | 说明 |
|---|---|---|
| 09 | [因果推断读书笔记与学习资源](../../cases/%E5%9B%A0%E6%9E%9C%E6%8E%A8%E6%96%AD/CausalAnalysis__09_%E8%B5%84%E6%96%99_%E5%9B%A0%E6%9E%9C%E6%8E%A8%E6%96%AD%E8%AF%BB%E4%B9%A6%E7%AC%94%E8%AE%B0%E4%B8%8E%E5%AD%A6%E4%B9%A0%E8%B5%84%E6%BA%90.md) | 原学习资源与两篇读书笔记已整合到这里 |

## 6. 迁移状态

旧文档内容已经迁移到 01-09 新体系中；已迁移的旧文件已移入系统废纸篓，不再作为正文入口维护。
