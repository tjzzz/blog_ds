## Featuretools

https://github.com/FeatureLabs/featuretools



参考：https://zhuanlan.zhihu.com/p/114943596



特征工程常见的方法分为两种：

1、针对单表的transform操作，例如log变换，特征编码等，都是在一张表上进行的；

2、groupby聚合操作，一般是跨表进行的，比如groupby min max mean等等。


## feature store
业界在用的feature store的信息：
https://www.featurestore.org/


![-w982](../../../Draft/media/16103451444602.jpg)


## Hopsworks

feature_store设计
- 离线数据存储在hive中，一个特征一列，一个feature_group作为一个table
- online数据mysql

query-planner: 可以直接写简单的特征提取而不是复杂的sql之间的关联



https://pypi.org/project/hops/



参考资料

https://zhuanlan.zhihu.com/p/339958634


## feast
