# 3.【解释性】LIME

《“Why Should I Trust You?” Explaining the Predictions of Any Classifier》

机器学习得到的模型有时候是一个black box不具有解释性，作者提出了一个问题，我们究竟是相信一个predict result，还是相信一个model。

本文作者主要是利用局部近似的方法，来对any classifier进行解释
一个大概的示意图
![](../../../Draft/media/15227606288131/15227612016423.jpg)


## 2.可解释性

* 可解释：首先必须是可解释的易懂的，在特征很多的时候，线性模型、梯度向量、可加模型等都不太适合。
* local faithfull：局部忠诚
* 与模型无关的，可解释any classifier


## 3 Local Interpretable Model-agnostic Explanations

LIME，首先区分两个东西

* features
* interpretable data representations

比如文本文类时具体的features是一个vector，而可解释的representation可能是是否出现某个关键词

基本原理示意图：
![](../../../Draft/media/15227606288131/15227612016423.jpg)

说明：



抽象的数学描述
![](../../../Draft/media/15227606288131/15227633252420.jpg)


作者在后面主要是讲了候选集是稀疏线性模型的方法

### 稀疏线性解释
即G为线性模型，一致性的度量$\pi_x=exp(-D(x,z)^2/\sigma^2)$, 在x局部用一个线性函数去近似

![](../../../Draft/media/15227606288131/15227718128055.jpg)
具体操作，先用lasso选择k个特征，然后用最小二乘学习特征的权重，K-LASSO
![](../../../Draft/media/15227606288131/15227724362604.jpg)



## lime

分类、连续、连续+分类 https://github.com/marcotcr/lime/blob/master/doc/notebooks/Tutorial%20-%20continuous%20and%20categorical%20features.ipynb


