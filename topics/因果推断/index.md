---
title: "因果推断"
created: 2026-10-09
updated: 2026-10-11
tags: [llm-wiki, index]
source: ["Input/rebuild_source_2026-10-09/03_统计/CausalAnalysis/MOC_因果推断体系.md"]
merged_from: ["03_统计/CausalAnalysis/MOC_因果推断体系.md"]
wiki_type: topic
review_status: structural
topic: "因果推断"
---


# 因果推断

在随机实验或观察数据中建立可信反事实，并明确识别假设。

## 二级目录

按子领域浏览，文档类型见各篇的 `wiki_type` 元数据。

- [准实验方法](%E5%87%86%E5%AE%9E%E9%AA%8C%E6%96%B9%E6%B3%95/index.md)（7 篇）
- [基础与识别](%E5%9F%BA%E7%A1%80%E4%B8%8E%E8%AF%86%E5%88%AB/index.md)（6 篇）
- [学习资料](%E5%AD%A6%E4%B9%A0%E8%B5%84%E6%96%99/index.md)（1 篇）
- [软件实现](%E8%BD%AF%E4%BB%B6%E5%AE%9E%E7%8E%B0/index.md)（3 篇）

## 关键问题

没有直接可见的反事实时，怎样评估干预效果？

## 建议阅读路线

定义处理和结果 → 识别混杂与选择偏差 → 选择实验或准实验设计 → 诊断识别假设。

**关联 Topic**：[统计学基础](../%E7%BB%9F%E8%AE%A1%E5%AD%A6%E5%9F%BA%E7%A1%80/index.md)、[实验设计与AB测试](../%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/index.md)。

## 知识地图

- [导论](%E5%9F%BA%E7%A1%80%E4%B8%8E%E8%AF%86%E5%88%AB/CausalAnalysis__01_%E5%9B%A0%E6%9E%9C%E6%8E%A8%E6%96%AD%E5%AF%BC%E8%AE%BA.md)：相关、干预与反事实。
- [潜在结果框架](%E5%9F%BA%E7%A1%80%E4%B8%8E%E8%AF%86%E5%88%AB/CausalAnalysis__04_%E6%BD%9C%E5%9C%A8%E7%BB%93%E6%9E%9C%E6%A1%86%E6%9E%B6_ITE_ATE_ATT_CATE.md)：个体和平均处理效应。
- [偏差与识别假设](%E5%9F%BA%E7%A1%80%E4%B8%8E%E8%AF%86%E5%88%AB/CausalAnalysis__06_%E5%81%8F%E5%B7%AE%E4%B8%8E%E8%AF%86%E5%88%AB%E5%81%87%E8%AE%BE_%E6%B7%B7%E6%9D%82%E9%80%89%E6%8B%A9%E5%81%8F%E5%B7%AE%E5%86%85%E7%94%9F%E6%80%A7.md)：混杂、选择偏差与内生性。
- [无实验场景评估决策树](%E5%87%86%E5%AE%9E%E9%AA%8C%E6%96%B9%E6%B3%95/CausalAnalysis__03_%E6%97%A0%E5%AE%9E%E9%AA%8C%E5%9C%BA%E6%99%AF%E6%95%88%E6%9E%9C%E8%AF%84%E4%BC%B0%E5%86%B3%E7%AD%96%E6%A0%91.md)：依据可获得的对照和时间结构选择设计。
- [方法总览](#因果推断体系)：DID、匹配、RDD、IV 与合成控制。

## 关键关系

[随机化与因果识别](../../relationships/%E9%9A%8F%E6%9C%BA%E5%8C%96%E4%B8%8E%E5%9B%A0%E6%9E%9C%E8%AF%86%E5%88%AB.md)连接实验和观察性研究。每个方法页后续应补充适用前提、主要威胁、诊断方法和原始来源。

## 因果推断体系

> 整合自已有笔记：`03_统计/CausalAnalysis/MOC_因果推断体系.md`。内容尚待逐条核验。

### 因果推断体系

> 目标：把因果推断整理成一套面向业务策略评估的知识体系，重点服务「无法做 AB 实验 / AB 结果有偏 / 需要做增量价值评估」的场景。

### 1. 学习路径


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



### 2. 总览与框架

| 编号 | 文档 | 解决的问题 |
|---|---|---|
| 01 | [因果推断导论](%E5%9F%BA%E7%A1%80%E4%B8%8E%E8%AF%86%E5%88%AB/CausalAnalysis__01_%E5%9B%A0%E6%9E%9C%E6%8E%A8%E6%96%AD%E5%AF%BC%E8%AE%BA.md) | 为什么相关不等于因果，为什么业务评估需要因果语言 |
| 02 | [AB实验与因果推断的关系](%E5%9F%BA%E7%A1%80%E4%B8%8E%E8%AF%86%E5%88%AB/CausalAnalysis__02_AB%E5%AE%9E%E9%AA%8C%E4%B8%8E%E5%9B%A0%E6%9E%9C%E6%8E%A8%E6%96%AD%E7%9A%84%E5%85%B3%E7%B3%BB.md) | AB 为什么是金标准，因果推断如何补齐不能 AB 的场景 |
| 03 | [无实验场景效果评估决策树](%E5%87%86%E5%AE%9E%E9%AA%8C%E6%96%B9%E6%B3%95/CausalAnalysis__03_%E6%97%A0%E5%AE%9E%E9%AA%8C%E5%9C%BA%E6%99%AF%E6%95%88%E6%9E%9C%E8%AF%84%E4%BC%B0%E5%86%B3%E7%AD%96%E6%A0%91.md) | 面对一个业务策略，如何选择 DID / PSM / IV / 合成控制等方法 |
| 04 | [潜在结果框架](%E5%9F%BA%E7%A1%80%E4%B8%8E%E8%AF%86%E5%88%AB/CausalAnalysis__04_%E6%BD%9C%E5%9C%A8%E7%BB%93%E6%9E%9C%E6%A1%86%E6%9E%B6_ITE_ATE_ATT_CATE.md) | ITE、ATE、ATT、CATE、反事实等核心语言 |
| 05 | [结构因果模型](%E5%9F%BA%E7%A1%80%E4%B8%8E%E8%AF%86%E5%88%AB/CausalAnalysis__05_%E7%BB%93%E6%9E%84%E5%9B%A0%E6%9E%9C%E6%A8%A1%E5%9E%8B_DAG%E4%B8%8Edo_calculus.md) | DAG、混杂、后门路径、do-calculus 的基本直觉 |
| 06 | [偏差与识别假设](%E5%9F%BA%E7%A1%80%E4%B8%8E%E8%AF%86%E5%88%AB/CausalAnalysis__06_%E5%81%8F%E5%B7%AE%E4%B8%8E%E8%AF%86%E5%88%AB%E5%81%87%E8%AE%BE_%E6%B7%B7%E6%9D%82%E9%80%89%E6%8B%A9%E5%81%8F%E5%B7%AE%E5%86%85%E7%94%9F%E6%80%A7.md) | 混杂、选择偏差、内生性、未观测混杂为什么会让结论失真 |

### 3. 方法体系

> 方法类统一用 `编号_方法_方法名` 命名，便于看出它们属于同一个体系。

> 说明：方法文档统一使用 `07_方法_...` 前缀，表示它们都属于第 07 组「因果方法体系」；后面的中文方法名用于区分具体方法。

| 编号 | 方法 | 典型使用场景 | 核心假设 |
|---|---|---|---|
| 07 | [方法_Matching与PSM](%E5%87%86%E5%AE%9E%E9%AA%8C%E6%96%B9%E6%B3%95/CausalAnalysis__%E6%96%B9%E6%B3%95_Matching%E4%B8%8EPSM.md) | 处理组和对照组可观测特征不平衡 | 可观测变量充分控制选择偏差 |
| 07 | [方法_DID双重差分](%E5%87%86%E5%AE%9E%E9%AA%8C%E6%96%B9%E6%B3%95/CausalAnalysis__%E6%96%B9%E6%B3%95_DID%E5%8F%8C%E9%87%8D%E5%B7%AE%E5%88%86.md) | 有处理前后和对照组，例如策略分批上线 | 平行趋势 |
| 07 | [方法_IV工具变量](%E5%87%86%E5%AE%9E%E9%AA%8C%E6%96%B9%E6%B3%95/CausalAnalysis__%E6%96%B9%E6%B3%95_IV%E5%B7%A5%E5%85%B7%E5%8F%98%E9%87%8F.md) | 核心变量内生，但存在外生冲击或工具变量 | 相关性、排除限制、独立性 |
| 07 | [方法_合成控制法](%E5%87%86%E5%AE%9E%E9%AA%8C%E6%96%B9%E6%B3%95/CausalAnalysis__%E6%96%B9%E6%B3%95_%E5%90%88%E6%88%90%E6%8E%A7%E5%88%B6%E6%B3%95.md) | 单城市、单国家、单业务单元上线策略 | 可由多个对照单元加权合成反事实 |
| 07 | [方法_RDD断点回归](%E5%87%86%E5%AE%9E%E9%AA%8C%E6%96%B9%E6%B3%95/CausalAnalysis__%E6%96%B9%E6%B3%95_RDD%E6%96%AD%E7%82%B9%E5%9B%9E%E5%BD%92.md) | 存在明确分数线、阈值、规则边界 | 阈值附近个体近似随机 |
| 07 | [方法_异质性处理效应与Uplift](%E5%87%86%E5%AE%9E%E9%AA%8C%E6%96%B9%E6%B3%95/CausalAnalysis__%E6%96%B9%E6%B3%95_%E5%BC%82%E8%B4%A8%E6%80%A7%E5%A4%84%E7%90%86%E6%95%88%E5%BA%94%E4%B8%8EUplift.md) | 评估不同人群的增量收益，做策略分层投放 | 个体/分层处理效应可被特征解释 |

### 4. 工具实践

| 编号 | 文档 | 说明 |
|---|---|---|
| 08 | [工具_DoWhy](%E8%BD%AF%E4%BB%B6%E5%AE%9E%E7%8E%B0/CausalAnalysis__%E5%B7%A5%E5%85%B7__08_%E5%B7%A5%E5%85%B7_DoWhy.md) | 因果建模、识别、估计、反驳四步框架 |
| 08 | [工具_EconML与CausalML](%E8%BD%AF%E4%BB%B6%E5%AE%9E%E7%8E%B0/CausalAnalysis__%E5%B7%A5%E5%85%B7__08_%E5%B7%A5%E5%85%B7_EconML%E4%B8%8ECausalML.md) | CATE、DML、Uplift 等机器学习因果工具 |
| 08 | [工具_StatsModels实现PSM_DID_IV](%E8%BD%AF%E4%BB%B6%E5%AE%9E%E7%8E%B0/CausalAnalysis__%E5%B7%A5%E5%85%B7__08_%E5%B7%A5%E5%85%B7_StatsModels%E5%AE%9E%E7%8E%B0PSM_DID_IV.md) | 面试和业务落地中最常用的 Python 统计实现路线 |

> 实验疑难问题不在本目录重复维护，统一查看 [实验设计与 AB 测试 Topic](../%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/index.md)（原 MOC_高阶实验难题 文件未找到）。

### 5. 资料与读书笔记

| 编号 | 文档 | 说明 |
|---|---|---|
| 09 | [因果推断读书笔记与学习资源](%E5%AD%A6%E4%B9%A0%E8%B5%84%E6%96%99/CausalAnalysis__09_%E8%B5%84%E6%96%99_%E5%9B%A0%E6%9E%9C%E6%8E%A8%E6%96%AD%E8%AF%BB%E4%B9%A6%E7%AC%94%E8%AE%B0%E4%B8%8E%E5%AD%A6%E4%B9%A0%E8%B5%84%E6%BA%90.md) | 原学习资源与两篇读书笔记已整合到这里 |

### 6. 迁移状态

旧文档内容已经迁移到 01-09 新体系中；已迁移的旧文件已移入系统废纸篓，不再作为正文入口维护。
