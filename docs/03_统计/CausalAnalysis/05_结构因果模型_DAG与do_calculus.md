---
title: 结构因果模型_DAG与do_calculus
update_time: "2026-09-13 21:37:43 CST"
tags:
  - statistics/causal-inference
---

# 05. 结构因果模型：DAG 与 do-calculus

结构因果模型关注的是：变量之间的因果结构是什么，以及在这个结构下能否识别干预效果。

## 1. DAG 的基本元素

| 元素 | 含义 |
|---|---|
| 节点 | 变量，例如 treatment、outcome、confounder |
| 有向边 | 因果影响方向 |
| 路径 | 变量之间的连接关系 |
| 后门路径 | 从 treatment 指向 outcome 的非因果路径 |
| collider | 两个箭头共同指向的变量，错误控制可能引入偏差 |

## 2. 混杂的 DAG 表达

```text
C -> T -> Y
C ------> Y
```

$C$ 同时影响 treatment 和 outcome。此时直接比较 $T=1$ 和 $T=0$ 会混入 $C$ 的影响。

## 3. 后门准则

如果控制一组变量 $X$ 后，能阻断所有从 $T$ 到 $Y$ 的后门路径，就可以识别 $T$ 对 $Y$ 的因果效应。

直觉：

```text
把非因果路径堵住，只保留 T -> Y 的因果路径
```

## 4. do 操作

普通条件概率：

$$
P(Y|T=t)
$$

表示观察到 $T=t$ 时 $Y$ 的分布。

干预概率：

$$
P(Y|do(T=t))
$$

表示人为把 $T$ 设置为 $t$ 后 $Y$ 的分布。

因果推断的目标是从观察数据中识别干预分布。

## 5. 业务使用方式

业务上不一定要完整使用 do-calculus，但必须能画清楚：

- treatment 是什么；
- outcome 是什么；
- 哪些变量同时影响 treatment 和 outcome；
- 哪些变量是 treatment 之后才发生，不能作为控制变量；
- 哪些变量是 collider，控制后反而引入偏差。

相关旧文档：

- [因果分析](01_因果推断导论.md)
- [【读书笔记】为什么：关于因果关系的新科学](09_资料_因果推断读书笔记与学习资源.md)
- [工具-do_why](工具/08_工具_DoWhy.md)
