---
title: 工具_StatsModels实现PSM_DID_IV
update_time: "2026-09-13 21:37:43 CST"
tags:
  - statistics/causal-inference
  - python
  - statsmodels
---

# 08. 工具：StatsModels 实现 PSM、DID、IV

业务面试和日常分析里，StatsModels 的重要性很高，因为它能清楚表达统计模型、系数、标准误和显著性。

## 1. PSM 的基础实现路线

```python
# 1. 用 sklearn / statsmodels 估计 propensity score
# 2. 用 nearest neighbors 做匹配
# 3. 检查匹配前后 balance
# 4. 在匹配后样本上估计 treatment effect
```

旧文档 [Matching方法](07_方法_Matching与PSM.md) 中已有一版 PSMEstimator 代码，后续可以整理成可运行 notebook。

## 2. DID 的基础回归

```python
import statsmodels.formula.api as smf

model = smf.ols(
    'y ~ treat + post + treat:post + C(unit) + C(date)',
    data=df
).fit(cov_type='cluster', cov_kwds={'groups': df['unit']})

print(model.summary())
```

`treat:post` 的系数就是 DID 估计量。

## 3. IV / 2SLS 的基础思路

```text
第一阶段：T ~ Z + X
第二阶段：Y ~ T_hat + X
```

实际实现可以用：

- `statsmodels` 手动两阶段；
- `linearmodels.iv.IV2SLS`；
- DoWhy 的 IV estimator。

## 4. 输出时必须包含

| 内容 | 说明 |
|---|---|
| treatment 定义 | 策略、功能、曝光、版本、地区等 |
| outcome 定义 | 收入、留存、转化、时长等 |
| 识别假设 | 为什么可以解释为因果 |
| 样本范围 | 分析总体和排除规则 |
| 标准误 | 是否 cluster、robust |
| 稳健性 | 换窗口、换对照、placebo、balance check |

## 5. 后续补充方向

- PSM 完整 notebook；
- DID 事件研究图；
- IV 弱工具变量检验；
- 合成控制 Python 实现；
- CATE / uplift 评估模板。
