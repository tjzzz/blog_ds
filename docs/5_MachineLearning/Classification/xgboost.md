# xgboost
xgboost是在梯度提升()
## xgboost原理

我们重新来考虑 Tree Boosting. 给定含n个样本m个特征的数据集:
$${D}=\{(x_i,y_i)\}\,(|\mathcal{D}|=n,\,x_i\in\,\mathbb{R}^{m},y_i\in\mathbb{R})$$
假定基础模型是CART决策树，当决策树的叶子数为T时，Tree将输入值划分到T个区域，每一个区域都有指定的值，令 $q: R^M -> {1,2,...T}$为树的结构，则决策树的输出可以表示为
$$b(x)=w_{q(x)}$$
XGBoost 不考虑梯度，直接将损失函数泰勒展开直到二阶导数，并添加正则项

$$L^t=\sum_{i=1}^{n}l(y_i,\hat{y_i}^{(t-1)}+f_{t}(x_i))+\Omega(f_t)$$

二阶泰勒逼近可以快速优化上述问题

$$L^t =\sum_{i=1}^n[l(y_i,\hat{y_i}^{t-1})+g_i f_t(x_i)+\frac{1}{2}h_{i}f_{t}^{2}(x_i)]+\Omega(f_t)$$


其中g和h是l的一阶导数和二阶导数（自变量为 $ \hat y$ ) 可以看到第一项是常数项，所以我们只需要优化第二项。另外指定正则项为
$$ \Omega(f_t)=\gamma_{}T+\frac{1}{2}\lambda\sum_{j=1}^{T}w_{j}^{2}$$

则上式可以重写为
$$\tilde{\mathcal{L}}^{(t)}=\sum_{i=1}^{n}[g_{i}f_{t}(x_i)+\frac{1}{2}h_{i}f_{t}^{2}(x_i)]+\gamma_{}T+\frac{1}{2}\lambda\sum_{j=1}^{T}w_{j}^{2}$$

$$\tilde{\mathcal{L}}^{(t)}=\sum_{j=1}^{T}[(\sum_{i\in\,I_j}g_i)w_j+\frac{1}{2}(\sum_{i\in\,I_j}h_i+\lambda)w_{j}^{2}]+\gamma T$$

其中 $ I_j =\{i|q(x_i)=j\}$ . 对于固定的决策树结构 q(x), 我们可以计算叶子j上的最优权重 $w_j^{*}$

$$G_j=\sum_{i\in I_j}g_i,H_{j}=\sum_{i\in I_j}h_i, w_{j}^{ }=-\frac{G_j}{H_j+\lambda}$$

![](../../../Draft/media/Pasted%20image%2020220513163807.png)




## 工具使用

http://xgboost.readthedocs.io/en/latest/python/python_intro.html





xgb中计算特征重要性的有以下几种不同的方式。默认是使用weight的方式，建议使用gain
```python
xgboost.plot_importance(model, importance_type=xxx)
```

* 'weight': the number of times a feature is used to split the data across all trees.在所有树中一个特征被用来分裂数据的次数
* 'gain': the average gain across all splits the feature is used in.
* 'cover': the average coverage across all splits the feature is used in.
* 'total_gain': the total gain across all splits the feature is used in.
* 'total_cover': the total coverage across all splits the feature is used in.



# 其他问题

 ## xgboost特征是可复用的

## xgboost 更改损失函数
xgboost的默认损失函数

#todo https://blog.csdn.net/zwqjoy/article/details/109311133


