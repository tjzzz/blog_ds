

> github: https://github.com/catboost/catboost


CatBoost 和 XGBoost、LightGBM 并称为 GBDT 的三大主流神器，都是在 GBDT 算法框架下的一种改进实现。XGBoost 被广泛的应用于工业界，LightGBM 有效的提升了 GBDT 的计算效率，而俄罗斯的搜索巨头YandexYandex 的 CatBoost 号称是比 XGBoost 和 LightGBM 在算法准确率等方面表现更为优秀的算法。



catboost是基于 **对称决策树** 为基学习器实现的gbdt框架

> 对称决策树（Symmetric Decision Tree）是一种用于分类和回归的机器学习模型，它使用树形结构来表示决策规则。与传统决策树不同的是，对称决策树在每个节点处都会对特征进行对称变换，并选择最优的对称变换方式。对称决策树的主要优点在于它可以处理非线性问题，并且在处理高维数据时具有很好的表现。此外，它还可以处理缺失数据和异常值。
> 对称：即树的每个层级上的分裂特征与规则是一致。

![](https://picx.zhimg.com/80/v2-c602a29255ff89ae8f0e5ac06a3f37d4_1440w.webp?source=1940ef5c)

## 类别特征处理

分类特征的处理方式一般可以采用：one-hot编码、频率编码、属性均值(Target Statistics)等

CatBoost的类别特征处理的核心思想是：**Ordered Target Encoding**

CatBoost算法的设计初衷是为了更好的处理GBDT特征中的categorical features。在处理 GBDT特征中的categorical features的时候，最简单的方法是用 categorical feature 对应的**标签的平均值来替换**。**在决策树中，标签平均值将作为节点分裂的标准**。

这种方法有一个显而易见的缺陷，就是通常特征比标签包含更多的信息，如果强行用标签的平均值来表示特征的话，**当训练数据集和测试数据集数据结构和分布不一样的时候会出条件偏移问题**。


#todo 具体算法



## 参考
- https://www.zhihu.com/question/62873937/answer/2571911237
- https://zhuanlan.zhihu.com/p/504646498
	- https://mp.weixin.qq.com/s/v54P5kBiMk3GL4esuut46w