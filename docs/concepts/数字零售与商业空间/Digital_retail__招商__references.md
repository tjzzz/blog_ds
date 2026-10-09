---
title: "references"
created: 2026-10-09
updated: 2026-10-09
tags: [llm-wiki, migrated]
source: ["Input/rebuild_source_2026-10-09/08_业务专题/Digital_retail/招商/references.md"]
wiki_type: concepts
topic: "数字零售与商业空间"
migrated_from: "08_业务专题/Digital_retail/招商/references.md"
review_status: structural
---

> 所属 Topic：[数字零售与商业空间](../../topics/%E6%95%B0%E5%AD%97%E9%9B%B6%E5%94%AE%E4%B8%8E%E5%95%86%E4%B8%9A%E7%A9%BA%E9%97%B4.md) · 类型：概念

## 文献1-非线性规划

Development of a Nonlinear Integer Optimization Model for Tenant Mix Layout in a Shopping Centre-2020

### introduction
关于TMP(tenant mix problem)的相关研究比较少，

早期的研究的规划问题，主要考虑的限制条件如下：
-  including total leasable area, 
- the upper and lower limits of each type of business area, 
- the upper and lower limits of each size of a shop, 
- the maximum amount of interior decoration allowance

作者目的：考虑store和store之间的交互，shpping centre可以看做是一个生态系统，不同的业态组合是消费者选择后进化的产物。



### 文献综述
整体来说TMP包括三个决策：
 - the division of physical space [18–20], 
 - the selection of retail types,
 - and the brand level of stores [18].

实际的场景中包含两种情况：
1. 针对商场整体的布局做分配，
2. 只针对特定空位置安排合适的业态和店铺


一些发现：
Consumer behaviour in a shopping centre can create **retail externalities** [理论-零售空间布局](Digital_retail__%E5%9F%BA%E7%A1%80%E7%9F%A5%E8%AF%86__%E7%90%86%E8%AE%BA-%E9%9B%B6%E5%94%AE%E7%A9%BA%E9%97%B4%E5%B8%83%E5%B1%80.md)in stores due to shopping attitudes, such as multipurpose shopping, comparison shopping, and reducing search costs, and those externalities have been widely identified [6,  [21](Digital_retail__%E6%8B%9B%E5%95%86__references.md#21), [22](Digital_retail__%E6%8B%9B%E5%95%86__references.md#22)]

barbell shopping center model: 两头放一些大型的或者餐饮店，中间放一些小的店铺

分析可见性、店铺大小等对sale的影响

模拟在给定tenant mix下的消费者行为。分析客流密度和业态集中度的关系[[41](Digital_retail__%E6%8B%9B%E5%95%86__references.md#41)]



### 研究方法
作者的研究粒度：业态+brand level

基本假定：
-  The attraction of a store is directly proportional to its size.
-  Anchor store generates retail externalities but is not affected by the externalities of other stores.
-  Each floor has a main type of retail； floor theme

目标：rent
 

Rent  = Basic rent + Excess rent

 
（1）basic rent
$$Basic rent = f(AREA,FLOOR,LEVEL,POSITION,TYPE)=S_{f,x,y}r_b c_f c_h c_{po} $$

作者这里使用归一化的方式，即选择一个指定的参考点，然后其他位置按照系数进行折算

- rB：Basic 坪效 for the first floor
- cf： Adjustment coefficient of the floor 
- ch: Adjustment coefficient of shop grade
- c_po: 这里对location的计算和落位预测里的很相似，也是考虑了entrance和elevator....
![](../../media/recovered/c951cc734ca0-Pasted%20image%2020220304133754.png)


> 折算定价法


（2） excess rent
 提成租金是与store的销售额有关的

$$SALES = f(TYPE, LEVEL, EXTERNALITY, POSITION)$$

retail externalities: The externalities of the anchor store and similar agglomeration externalities


- 根据前面假定，其中 the externality of the anchor store使用的引力模型来计算
$w1 = \frac{S_{anchor}S_{(f,x,y)}}{d_{anchor}^2}$

-  similar agglomeration externalities
对该主题楼层下的某个主题店铺(f, x, y)
![](../../media/recovered/020096c3a33a-Pasted%20image%2020220417221042.png)


其中：
$S_{trav}$：  the maximum i-type store area that potential consumers are willing to search for to find desired goods. 
求导$g/S_i$ 
![](../../media/recovered/2f96336f3512-Pasted%20image%2020220417222428.png)


对于主题楼层下的非主题店铺 the nontheme store is affected by the spillover effect of theme store aggregation
![](../../media/recovered/2d2571c64130-Pasted%20image%2020220417223357.png)


![](../../media/recovered/2af75525eca1-Pasted%20image%2020220417220105.png)


### model
![](../../media/recovered/441430e16693-Pasted%20image%2020220417224706.png)

![](../../media/recovered/676c1d5635e8-Pasted%20image%2020220417224810.png)


![](../../media/recovered/4fe0777e8cb4-Pasted%20image%2020220417224833.png)


最终的优化目标：

![](../../media/recovered/21c601688a2d-Pasted%20image%2020220417224931.png)

### 计算方法
最终转化为一个非线性优化问题，使用GA[[47](Digital_retail__%E6%8B%9B%E5%95%86__references.md#47)]算法来求解
设定：
- 一个个体表示搜索空间中的一个解
- 因为整个搜索空间非常大，所以如果每次都是随机生成的话很难收敛，设置一些限制：设置不同等级的面积限制、不同业态类型的面积范围（brand level 划分出5级，area setting: 根据面积大小划分成几个档次）


算法过程：
```
Input information about the shopping centre to be laid out Initialize the tenant layout population under logical constraints Set parameters of the GA  
Do
	For each iteration  
	- Calculate the fitness of all individuals in the population
	- Find and then save the best solution and elite individuals in this generation into the next generation population 
	- Use the roulette method to select the individuals  who can enter the next iteration
	- The selected individual genes are crossed and mutated under logical constraints  
	- Update the population

	End  
Until default number of iterations


```



### 案例
用了重庆的一个商场的数据
![](../../media/recovered/5fa40b9f1c07-Pasted%20image%2020220418114316.png)

后续计划：
- We hope that the model proposed in this paper can be incorporated into software tools in the future to provide better decision-making information for shopping centre retail space planning.
- 当前只考虑了两种外部性，后续可以考虑不同业态之间的

code: http://downloads.hindawi.com/journals/ace/2020/2787351.f1.pdf
[code](Digital_retail__%E6%8B%9B%E5%95%86__code.md)


QQ:
- 推荐的角度
- 主题区域，每层楼大概会有自己的业态主题，而且对于较大的场来说，还会划分出不同的区域
- 输入是不同的业态组合表现，输出是整体的客流/gmv表现，算法去学习背后的关系



## 文献2-

Finding Prospects for Shopping Centers: a machine learning approach


综述

void analysis
 


 

基本数据是
mall_id, 各个业态的个数

To set this up as a machine learning problem, each training case consisted of removing one store from a center and then predicting its type from the remaining stores in the center.-默认当前的配置是相对好的？

base版本是按照当前场内的业态频次挑选最高的
模型版本用的RF


## 文献3 ☆☆☆
 Shoppingcenterdesign using a facility layout assignment approach. 文献综述中提到了很多方法，可以深入再看看

The maximum flow capturing problem
作者的问题目标：设置合理的店铺布局，是客流分布尽量均衡

核心概念： ![](../../media/recovered/93f214591172-Pasted%20image%2020220308172712.png)

将每个区域的客流表示成we的加权(周边店铺考虑距离)




## A Method for Determining Optimal Tenant Mix (Including Location) in Shopping Centers
1990年代：The academic findings generally parallel professional knowledge about the nature of store attributes and location
- Rent subsidies go to those that produce these externalities while rent premiums are paid by those that “free ride.  吸引客流的租金少，其他的租金高一些
- 租金坪效随着面积增大而减小
- 有竞争关系的同业态会相对分散 #ra

Selecting Tenants in a Shopping Mall” (Bean, et al. (1988))
非线性整数规划问题， 包括：店铺类型、店铺大小(三种类型)、位置类型(三种)
Homart’s Market Research Group can estimate a store’s sales over the study horizon given its type, size, location class, and the number of stores of its type in the mall



### 作者方案

数据采集：合作方的商场数据







## 参考资料


1.  A virtual reality tool to measure shoppers’ tenant mix preferences,
41. J. Hirsch, M. Segerer, K. Klein, and T. Wiegelmann, “The analysis of customer density, tenant placement and coupling inside a shopping centre with GIS,” Journal of Property Re- search, vol. 33, no. 1, pp. 37–63, 2016.

#toread
https://www.doc88.com/p-3048710646806.html

硕士论文：中国购物中心租户组合策略研究 https://www.docin.com/p-916561762.html





考虑因素：
- location
- 交互影响
- 布局应该使消费者尽可能的路过更多的店铺
- 从消费者的消费需求：有的是多目的购物、对比购物、直达目的型




可以再学习下：
- J. C. Bean, C. E. Noon, S. M. Ryan, and G. J. Salton, Selecting tenants in a shopping mall,
- A virtual reality tool to measure shoppers’ tenant mix preferences,
- J. Hirsch, M. Segerer, K. Klein, and T. Wiegelmann, “The analysis of customer density, tenant placement and coupling inside a shopping centre with GIS,” Journal of Property Re- search, vol. 33, no. 1, pp. 37–63, 2016.



#### 21 

[21] D. H. Gatzlaff, G. T. Sirmans, and B. A. Diskin, “The effect of anchor tenant loss on shopping center rents,” Journal of Real Estate Research, vol. 9, no. 1, pp. 99–110, 1994.

#### 22
[22] M. J. Eppli and J. D. Shilling, “Changing economic per- spectives on the theory of retail location,” in Megatrends in Retail Real Estate, J. D. Benjamin, Ed., vol. 3, Berlin, Germany, Springer, 1996, Research Issues in Real Estate.


#### 41
 [41] J. Hirsch, M. Segerer, K. Klein, and T. Wiegelmann, “The analysis of customer density, tenant placement and coupling inside a shopping centre with GIS,” Journal of Property Re- search, vol. 33, no. 1, pp. 37–63, 2016.
#### 47
 U. Aickelin and K. A. Dowsland, “Enhanced direct and in- direct genetic algorithm approaches for a mall layout and tenant selection problem,” Journal of Heuristics, vol. 8, no. 5, pp. 503–514, 2002.