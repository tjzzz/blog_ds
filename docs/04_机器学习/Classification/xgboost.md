
# xgboost原理

## 算法原理

> 回顾下前面介绍提升树整体的算法过程(这里统一下标记)
> a) $F_0(x)=0$
> b) $F_m(x)=F_{m-1}(x) + f(x;\Theta_m), m=1,2...M$
   在给定$F_{m-1}(x)$的时候，需要求解:
$$\hat\Theta_m = argmin \sum_1^n L(y_i, F_{m-1}(x_i) + f(x_i;\Theta_m))$$
这里： F_m 表示当前算法累积到第m步的所有树，f_m表示第m颗树

下面来具体说下xgboost的算法过程：
【设定】给定含n个样本m个特征的数据集:
$${D}=\{(x_i,y_i)\}\,(|\mathcal{D}|=n,\,x_i\in\,\mathbb{R}^{m},y_i\in\mathbb{R})$$
假定基础模型是CART决策树，当决策树的叶子数为T时，Tree将输入值划分到T个区域，每一个区域都有指定的值，令 $q: R^M -> {1,2,...T}$为树的结构，则决策树的输出可以表示为
$$b(x)=w_{q(x)}$$

按照提升树部分的介绍，第t步其损失函数形式如下(这里在前面损失函数的基础上还考虑了正则项即树的复杂程度)：
$$L^t=\sum_{i=1}^{n}l(y_i,\hat{y_i}^{(t-1)}+f_{t}(x_i))+\Omega(f_t)$$
- 这里的$\hat y^{t-1}=F_{t-1}$ 表示前t-1颗树的预测结果
- $f_t(x)$ 表示第t颗树对样本的预测结果
- $\Omega(f_t)$ 表示树的复杂程度


为了解决上面这个优化问题大致的思路是：1、使用泰勒展开；2、将常数项忽略（因为我们的目标是找最小值）；3、转换一些符号，使式子更简洁

先回顾下泰勒展开公式：
![600](https://pic4.zhimg.com/80/v2-c8e642abebf7657b29544ebb6ef1aa1f_720w.jpg)

所以有：
$$\sum_{i=1}^{n}l(y_i,\hat{y_i}^{(t-1)}+f_{t}(x_i))+\Omega(f_t)=\sum_{i=1}^n[l(y_i,\hat{y_i}^{t-1})+g_i f_t(x_i)+\frac{1}{2}h_{i}f_{t}^{2}(x_i)]+\Omega(f_t)$$
并且指定正则化部分形式如$$ \Omega(f_t)=\gamma_{}T+\frac{1}{2}\lambda\sum_{j=1}^{T}w_{j}^{2}$$
- 其中g和h是L的一阶导数和二阶导数（自变量为 $f_t(x)$ ) ，可以看到第一项是常数项，所以我们只需要优化第二项
- T表示树中叶子结点的个数，$w_j$ 表示该树中第j个叶子结点的值


则上式可以重写为
$$\tilde{\mathcal{L}}^{(t)}=\sum_{i=1}^{n}[g_{i}f_{t}(x_i)+\frac{1}{2}h_{i}f_{t}^{2}(x_i)]+\gamma_{}T+\frac{1}{2}\lambda\sum_{j=1}^{T}w_{j}^{2}$$

$$\tilde{\mathcal{L}}^{(t)}=\sum_{j=1}^{T}[(\sum_{i\in\,I_j}g_i)w_j+\frac{1}{2}(\sum_{i\in\,I_j}h_i+\lambda)w_{j}^{2}]+\gamma T$$

其中 $I_j =\{i|q(x_i)=j\}$ . 对于固定的决策树结构 q(x), 我们可以计算叶子j上的最优权重 $w_j^{*}$

$$G_j=\sum_{i\in I_j}g_i,H_{j}=\sum_{i\in I_j}h_i, w_{j}^{ }=-\frac{G_j}{H_j+\lambda}$$

![](../../../media/Pasted%20image%2020220513163807.png)

## 树结构生成
贪心算法生成树结构

分裂点如何选择？
假设一个特征取值是1,2,...10 那么如何能够快速



# 常用参数
http://xgboost.readthedocs.io/en/latest/python/python_intro.html

https://xgboost.readthedocs.io/en/latest/parameter.html




xgb中计算特征重要性的有以下几种不同的方式。默认是使用weight的方式，建议使用gain
```python
xgboost.plot_importance(model, importance_type=xxx)
```

* 'weight': the number of times a feature is used to split the data across all trees.在所有树中一个特征被用来分裂数据的次数
* 'gain': the average gain across all splits the feature is used in.
* 'cover': the average coverage across all splits the feature is used in.
* 'total_gain': the total gain across all splits the feature is used in.
* 'total_cover': the total coverage across all splits the feature is used in.


## xgb-spark分布式版本
xgb https://xgboost.readthedocs.io/en/stable/tutorials/spark_estimator.html
lgb https://microsoft.github.io/SynapseML/docs/features/lightgbm/about/



# 常见问题

1. 缺失值处理
这个算法实际上做的是一件非常简单的事情。对于第k个特征，我们首先将样本中第k个特征的特征值为缺失值的样本全部剔除。然后我们正常进行样本划分。最后，我们做两个假设，一个是缺失值全部摆左子结点，一个是摆右子节点。哪一个得到的增益大，就代表这个特征最好的划分。总结一下，就是缺失值都摆一起，选最好的情况。

2. xgboost特征是可复用的


3. 

## xgboost 更改损失函数
xgboost的默认损失函数

#todo https://blog.csdn.net/zwqjoy/article/details/109311133





# 参考
https://zhuanlan.zhihu.com/p/562983875
