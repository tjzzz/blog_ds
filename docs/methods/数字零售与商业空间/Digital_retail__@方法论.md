---
title: "@方法论"
created: 2026-10-09
updated: 2026-10-09
tags: [llm-wiki, migrated]
source: ["Input/rebuild_source_2026-10-09/08_业务专题/Digital_retail/@方法论.md"]
wiki_type: methods
topic: "数字零售与商业空间"
migrated_from: "08_业务专题/Digital_retail/@方法论.md"
review_status: structural
---

> 所属 Topic：[数字零售与商业空间](../../topics/%E6%95%B0%E5%AD%97%E9%9B%B6%E5%94%AE%E4%B8%8E%E5%95%86%E4%B8%9A%E7%A9%BA%E9%97%B4.md) · 类型：方法

# 方法总结

## 0. 搭建指标体系

现有的客流指标体系

-   指标的显著性。
    -   Ab test产出显著性
    -   问题指标归因
-   指标的有效性：能够反映出好坏的变化
    -   指标设计的区分度
    -   回溯历史事件(节假日、活动、疫情等在指标层面是否体现)

1.  ## 方法论1 SOP - 诊断-归因-改进
    

SOP: 分别看客流指标(进店数，深逛数，深逛数v2, 有效客流数等等)与gmv关系即可，当前的分析已有

> 建模的结果可以为我们提供SOP指标的构造灵感：将top的几个柔和成一个有业务意义的指标，比如深逛其实就是停留时长大于xx的个数，比如构造有效客流数，价值客流数等等作为目标GMV的前瞻性指标

### 2.1 诊断

诊断： 对研究对象(mall/store/业态)给出定量评估，

评估的角度包括：

-   集团角度：跨场评估
-   场角度：同场、同业态、同楼层等

评估方法：

(1) 直接评估: 直接对比目标指标，比如对比GMV

(2) 可比评估：因为每个个体受到的影响因素是不同的，将其他因素控制的条件下进行比较。比如:

Y(A) = f(Z=z1, X=x1), Y(B) = f(Z=z2, X=x2), 我们其实是希望知道 Y(A')= f(Z=z2, X=x1)的结果和Y(B)的对比情况。所以对比方法：将所有对象的Z 设置成统一的，根据模型预测得到新的结果

Yk' = f(Z=z0, X=xk ), e.g 一般意义上一线城市的一个场服装业态的收入大概是多少？(其他控制变量设置一般取值，然后进行模型预测)

> 类比特征重要性的计算思路PDP方式

### 2.2 归因

以store粒度为例，归因是回答为什么当前该store的表现是这样，为什么和其他同类别的store有差别，比如同一品牌不同场。

通过建立模型 Y = f(x1, x2, ...xk)。然后利用shap解释 $$y=y_{base} +\phi_1 + \phi_2 + .... + \phi_k$$ shape可以给出每个case下的每个特征的定量贡献，并且具有可加性。

e.g

$$y_i = base + factor_{1i} + factor_{2i} + ... + factor_{ki}$$

$$y_j = base + factor_{1j} + factor_{2j} + ... + factor_{kj}$$

个体i和个体j在y上的表现具体是由哪些因素导致的看以通过贡献看出来

#### 品牌-同一个场

通过shap对模型做分析，能够给出各个因素(客群，店铺位置，店铺属性等等)对目标的贡献，从而定位出来该店铺表现好或差的原因

#### 品牌-跨场

-   场因素、客群因素、店铺位置因素等等，定位出影响的因素，比如以雷达图展示
-   反事实预测：如果我把表现差的其他客观因素改成和表现好的一样，新的预测值是否能达到好的效果，从而定位出是客观因素导致的，还是本身经营问题。
-   对于客观因素(客群、位置等)我们可以有对应的建议，参见2.3部分

#### Mall- 跨场

类似品牌跨场，给出其当前表现，以及在可对比情况下的对比结果，从而定位出主要问题(客观因素，主观经营)

### 2.3 改进

根据分解思路中定位的问题，最终定位到的业务上比较好操作或者是落地的因素无非是：

-   **场的因素**

业态布局、店铺类型、动线设计(如何量化评估？)

-   **店铺的因素**

包括业态、位置、面积等等

-   **人/客群 关联****@****一鸣 客群分析**

> 目前缺乏一个比较系统化的对客群的分析方法，可以将当前的一些零散的分析模块整合在一起。

分析该人群的特点，从而进行营销活动导流

-   该人群的画像特点，输出显著diff的特征表述，比如和总体计算PHI指数。画像标签可以是线上+线下，可以再store/mall这个粒度进行打通，当做建模的特征
-   该人群的行为特点： 逛店偏好，关联店铺，
-   该人群在哪里：热力分布，场内动线
-   后续加上模型应用：潜客预测

2.  ## 方法论2
    

根据分解关系中的因果图，推断出关键节点的关系，从而能给出每个节点对最终结果GMV的影响。可以在此图的基础上进行各种推断。也可以将已有的模型结果纳入此图中4

3.  ## 产品demo
    

场 -> 店铺 -> 客群、店铺

# ML-建模

[Mall建模体系](https://aibee.feishu.cn/docs/doccnPgEgfy2GFiZhCNT1Kco9se)

1.  ## 组内调研结果
    

当前建模的发现汇总：[【保密】购物中心行业数据探索](https://aibee.feishu.cn/docs/doccnT6NjM6D630ikZ8UasfkMGc)

课题

**主要发现**

**备注**

[GMV与线下客流建模（店铺级）](https://aibee.feishu.cn/docs/doccnPWxIy5pB52an8HPEMvWkxd#wm3nzu)

杨邹

1.  深逛人数和进店人数有强相关关系（cor =0.92)
2.  店铺面积与进店人数和深逛人数有强正相关性（0.84；0.8）
3.  过店人数与GMV负相关？

[客流指标与GMV](https://aibee.feishu.cn/docs/doccnk5A3a9Ir5xMPgNGdbBcQcq) 柳姐

![](https://aibee.feishu.cn/space/api/box/stream/download/asynccode/?code=YTAyZmE4OTc5Yjc1MjFlODRiNGIyZDg3YjM1YmQ4M2ZfR013UktkSTZRMnVqS3BGYWFQQllMVWFzZlF3RmdjbXVfVG9rZW46Ym94Y25QVzdZdkkwNFFiRUxsV3dsdGZWc2piXzE2NDcyMjkwNTc6MTY0NzIzMjY1N19WNA)

[印力租金因素可视化分析](https://aibee.feishu.cn/docs/doccnxoe6ZSxig2nin0o3S2onHd)

莫栖

1.  租金坪效正相关因素：平均日营业额、过店客流量、
2.  租金坪效负相关因素：店铺面积，提成租金（bug）
3.  相关性较高因素：楼层（首层最高，可能和首次业态类型及客流较多相关）

[Mall商铺租金建模](https://aibee.feishu.cn/docs/doccnIT0PuTnGD2FWCM44ETTZkc#nqbtxe) 晓帅

正: 过去一年平均日营业额，租金类型=固定与提成取最高

负：出租面积，提成租金，

[笔单价影响因素分析](https://aibee.feishu.cn/docs/doccngwl2GkmYnXwps3BrCwtIYg) 莫栖

停留时长 charles

停留时长对GMV的贡献与店铺相关，不建议作为核心指标来提升

1.  整体上店内平均停留时长与GMV坪效（log）呈负相关性
2.  相关性受三级业态甚至单店铺影响较大。
3.  停留时长越长，不代表GMV收益率会更高。
4.  过店越多，停留越短。

深逛人数

北极星指标-深逛V2.

用来做其他运营场景的Y值来优化。摆脱对GMV的直接依赖

人数与人次

1.  无论是工作日或节假日，进店**人数**的相关性都比进店人次更高。
2.  珠宝、儿童、美容、快时尚、主力店，进店人数相关性更高；其他、餐饮、电器、休闲娱乐，进店人次相关性更高；
3.  进店人数和人次都不对特殊业态-车产生影响

mall-GMV[跨场GMV建模](https://aibee.feishu.cn/docs/doccnBjL9BtW1Z8Nq7UMaCU8h6g)

store-GMV [跨场Brand GMV建模](https://aibee.feishu.cn/docs/doccnvNBzq33o9nPz2IgvI3egyf)

[Store GMV - V4](https://aibee.feishu.cn/docs/doccnqTH1eusAxjJ1CKNZUznoug)

# 参考资料

[《为什么：关于因果关系的新科学》](https://aibee.feishu.cn/docs/doccnNgaOnW4mQbioH8xupwcBSm)

因果关系梳理参考 [【保密】购物中心行业数据探索](https://aibee.feishu.cn/docs/doccnT6NjM6D630ikZ8UasfkMGc)

[GMV&租金建模.pptx](https://aibee.feishu.cn/file/boxcnQhWR2WHrDu4qUg7mZjKGJg?office)