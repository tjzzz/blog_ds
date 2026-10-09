---
title: "04 CUPED 与方差缩减 — 提效 + 前校准锚点"
date: 2026-10-09
tags:
  - ab-test
  - CUPED
  - 方差缩减
  - pre-AA
  - 灵敏度
  - llm-wiki
description: "用协变量砍方差、缩短实验时长：CUPED 原理、CUPAC/分层/后分层/STATE 进阶、pre-AA(A/A)前校准与方差预估。对接 vault《Experiment难题/☆如何提升实验灵敏度》。"
created: 2026-10-09
updated: 2026-10-09
source: ["Input/rebuild_source_2026-10-09/03_统计/ab实验/04_CUPED与方差缩减.md"]
wiki_type: methods
topic: "实验设计与AB测试"
migrated_from: "03_统计/ab实验/04_CUPED与方差缩减.md"
review_status: structural
---

> 所属 Topic：[实验设计与AB测试](../../topics/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95.md) · 类型：方法

## Mental Model

实验要测出差异，要么**加样本量(n)**，要么**砍方差(σ²)**。CUPED 是后者——它用「实验前就已知的用户特征」先把噪声减掉，让信号更清楚。

```
普通指标：  Y = 真实效应 + 大噪声
CUPED 后：  Y' = Y − θ·(X − X̄)  ⇒ 噪声变小，MDE 更小 / 同样 n 更早显著
```

> **一句话**：CUPED 用「实验前协变量 X（如历史行为）」对指标做回归调整，剔除可解释的波动，等效于**不增加样本量却提升灵敏度**。pre-AA 则是实验前的「校准演习」——先空跑一次确认系统干净、估好方差。

---

## 📊 CUPED 原理

1. 实验前收集协变量 X（用户历史指标值，随机化前已存在）
2. 用对照/全量数据回归 `Y ~ X` 得斜率 θ
3. 调整指标：`Y_cuped = Y − θ·(X − X_mean)`
4. 对 `Y_cuped` 做常规检验 → 方差下降，所需样本量下降

**前提**：X 必须与 Y 相关（相关性越高，方差砍得越多），且 X 在**随机化前**确定（不能是实验导致的）。

### 进阶变体（行业已主流）
| 方法 | 思路 |
|------|------|
| **CUPAC** | 用 ML 模型预测 Y 作为协变量（比线性 θ 更强） |
| **分层 CUPED / 后分层** | 先分层再调整 |
| **STATE / Doubly Robust** | 结合倾向得分，更稳健 |
| **switchback 中的方差缩减** | 在时序实验里同样可用（KDD2025） |

---

## 🧪 pre-AA（A/A 测试）— 前校准锚点

在正式实验**前**跑一次「两组都用旧版本」的空实验：

| 目的 | 说明 |
|------|------|
| **系统健康检查** | 若 A/A 出现「显著差异」→ 分流/SRM 有 bug，不能上线真实验 |
| **方差预估** | 用 A/A 数据估真实 σ，反推更准的样本量 |
| **校准基线** | 给 CUPED 的 θ、护栏阈值提供经验值 |

> ⚠️ vault 里 [分组样本比例不匹配](Experiment%E9%9A%BE%E9%A2%98__%E5%88%86%E7%BB%84%E6%A0%B7%E6%9C%AC%E6%AF%94%E4%BE%8B%E4%B8%8D%E5%8C%B9%E9%85%8D.md)（SRM）就是 A/A / 真实验都要查的第一道关。

---

## 🎯 组合拳位置（真实成熟平台）
```
设计(power) → pre-AA(校准+估方差) → 运行(分流) → 分析(CUPED 砍方差 + 序贯/贝叶斯) → 决策
```
CUPED 与 pre-AA 是前后两端的「提效 + 校准」锚点，贯穿全程（见 [MOC_ab实验方法图谱](../../topics/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/ab%E5%AE%9E%E9%AA%8C__MOC_ab%E5%AE%9E%E9%AA%8C%E6%96%B9%E6%B3%95%E5%9B%BE%E8%B0%B1.md)）。

---

## ⚠️ 踩坑
- X 与实验处理**有因果关联** → CUPED 偏倚（必须随机化前）
- 协变量选得差（不相关）→ 白做，甚至引入噪声
- 只上 CUPED 不查 SRM → 系统性偏依旧在（见 [08_实验治理与护栏](ab%E5%AE%9E%E9%AA%8C__08_%E5%AE%9E%E9%AA%8C%E6%B2%BB%E7%90%86%E4%B8%8E%E6%8A%A4%E6%A0%8F.md)）

---

## 🔗 关联笔记

- vault 疑难对接：[☆如何提升实验灵敏度](Experiment%E9%9A%BE%E9%A2%98__%E2%98%86%E5%A6%82%E4%BD%95%E6%8F%90%E5%8D%87%E5%AE%9E%E9%AA%8C%E7%81%B5%E6%95%8F%E5%BA%A6.md)
- 序贯让它更早停：[03_序贯分析](ab%E5%AE%9E%E9%AA%8C__03_%E5%BA%8F%E8%B4%AF%E5%88%86%E6%9E%90.md)
- SRM 防火墙：[08_实验治理与护栏](ab%E5%AE%9E%E9%AA%8C__08_%E5%AE%9E%E9%AA%8C%E6%B2%BB%E7%90%86%E4%B8%8E%E6%8A%A4%E6%A0%8F.md)
- 地基样本量：[01_假设检验与p值](ab%E5%AE%9E%E9%AA%8C__01_%E5%81%87%E8%AE%BE%E6%A3%80%E9%AA%8C%E4%B8%8Ep%E5%80%BC.md)
- 总入口：[MOC_ab实验方法图谱](../../topics/%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1%E4%B8%8EAB%E6%B5%8B%E8%AF%95/ab%E5%AE%9E%E9%AA%8C__MOC_ab%E5%AE%9E%E9%AA%8C%E6%96%B9%E6%B3%95%E5%9B%BE%E8%B0%B1.md)

**更新日期**：2026-10-09
