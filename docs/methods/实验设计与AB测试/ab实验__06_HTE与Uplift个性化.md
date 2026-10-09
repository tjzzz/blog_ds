---
title: "06 HTE 与 Uplift 个性化 — 从「平均效应」到「谁受益」"
date: 2026-10-09
tags:
  - ab-test
  - HTE
  - CATE
  - Uplift
  - 个性化
  - 因果
  - llm-wiki
description: "异质处理效应(HTE)与 Uplift 建模：ATE vs CATE、Uplift 四类人群、Qini/AUUC 评估、因果森林。当前学界+工业最热方向。对接 vault 因果推断体系。"
created: 2026-10-09
updated: 2026-10-09
source: ["Input/rebuild_source_2026-10-09/03_统计/ab实验/06_HTE与Uplift个性化.md"]
wiki_type: methods
topic: "实验设计与AB测试"
migrated_from: "03_统计/ab实验/06_HTE与Uplift个性化.md"
review_status: structural
---

> 所属 Topic：[实验设计与AB测试](../../topics/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95.md) · 类型：方法

## Mental Model

传统 AB 只回答「**平均来看**新策略有没有用」（ATE）。但业务真正想问的是「**对谁有用**」——给所有人推，可能一半人无效甚至反感。

```
ATE（平均）： 推了之后整体 +2%        ← 太粗
CATE（异质）：老客 +8% / 新客 -1% / 沉默客 +5%   ← 能定向
Uplift：      只给「推了才转化」的人推  ← 最省成本
```

> **一句话**：HTE/CATE 把「平均效应」拆成「每个人的效应」；Uplift 进一步找「**因为你的干预才改变**」的那批人，做精准干预。

---

## 📊 核心概念

| 概念 | 含义 |
|------|------|
| **ATE** | 平均处理效应（全员平均） |
| **CATE / HTE** | 条件/异质处理效应：给定特征 X 下的个体效应 τ(x) = E[Y(1)-Y(0)\|X] |
| **Uplift** | 干预带来的**增量**，等价于 CATE 的干预决策视角 |
| **因果森林** | 随机森林的因果版，直接估 τ(x)（如 GRF） |

### Uplift 四类人群（经典划分）
| 人群 | 不干预 | 干预 | 是否值得推 |
|------|--------|------|-----------|
| **Sure Thing** | 会转化 | 会转化 | ❌ 浪费资源 |
| **Do Something** | 不转化 | 转化 | ✅ 核心目标 |
| **Do Nothing** | 转化 | 不转化 | ❌ 反而害 |
| **Lost Causes** | 不转化 | 不转化 | ❌ 无效 |

### 评估指标
- **Qini 曲线 / AUUC**：Uplift 模型的 ROC 类评估（按预测 uplift 降序排序，看累积增益）

---

## 🎯 实战用法
- 用实验数据训 CATE/Uplift 模型 → 对高 uplift 人群定向投放，省成本提 ROI
- 与 [05_MAB与客户分群路由](ab%E5%AE%9E%E9%AA%8C__05_MAB%E4%B8%8E%E5%AE%A2%E6%88%B7%E5%88%86%E7%BE%A4%E8%B7%AF%E7%94%B1.md) 结合：MAB 选策略，Uplift 选人群
- 与 [07_网络效应与干扰](../../concepts/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/ab%E5%AE%9E%E9%AA%8C__07_%E7%BD%91%E7%BB%9C%E6%95%88%E5%BA%94%E4%B8%8E%E5%B9%B2%E6%89%B0.md) 注意：社交产品里「对谁推」还要考虑溢出

---

## 🔥 为什么是当下最热
- 学界+工业从 ATE 全面转向 CATE：Snap 数亿用户 HTE 框架实测效果 **6×** 于常规显著实验；HBS 跨 362 实验/700 万客户验证协同增效
- 与「指标建设」「个性化增长」主线强相关（vault 1.3 因果推断、1.4 指标体系）

---

## 🔗 关联笔记

- 因果底座：[潜在结果框架](../%E5%9B%A0%E6%9E%9C%E6%8E%A8%E6%96%AD/CausalAnalysis__04_%E6%BD%9C%E5%9C%A8%E7%BB%93%E6%9E%9C%E6%A1%86%E6%9E%B6_ITE_ATE_ATT_CATE.md)（待补）、因果推断.md（待补）
- 分流承接：[05_MAB与客户分群路由](ab%E5%AE%9E%E9%AA%8C__05_MAB%E4%B8%8E%E5%AE%A2%E6%88%B7%E5%88%86%E7%BE%A4%E8%B7%AF%E7%94%B1.md)
- 干扰注意：[07_网络效应与干扰](../../concepts/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/ab%E5%AE%9E%E9%AA%8C__07_%E7%BD%91%E7%BB%9C%E6%95%88%E5%BA%94%E4%B8%8E%E5%B9%B2%E6%89%B0.md)
- 总入口：[MOC_ab实验方法图谱](../../topics/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/ab%E5%AE%9E%E9%AA%8C__MOC_ab%E5%AE%9E%E9%AA%8C%E6%96%B9%E6%B3%95%E5%9B%BE%E8%B0%B1.md)

**更新日期**：2026-10-09
