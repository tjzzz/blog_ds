
## 1基本原理
略
- 随机化实验
- 假设检验

## 2. AB test 敏感性

【ab test的基本问题】:
假设实验组和对照组分别是$y_t$和$y_c$， 最终进行假设检验的统计量是t检验
$$t = \frac{\bar Y_t-\bar Y_c}{\sqrt Var(\bar Y_t-\bar Y_c)}$$


$$t = \frac{Y_t-Y_c}{\sqrt {\sigma^2_t/n + \sigma^2_c/n}}$$



**提高敏感性的方法**：

(1) 增加样本量
(2) 减少抽样方差 variance reduction
- metric transformation
	对于长尾分布的metric，需要先对数据做一定的转换。比如对于极端值直接使用分位点:
	    - ![](../../../Draft/media/16143408366768.jpg)
	    - 衡量指标使用中位数，而非均值

- CUPED(Controlled Experiment Using Pre-Experiment Data) 该方法在实际中一般都会比较有效
回归调整：
假设我们的目标变量是Y，我们可以找到一个和Y相关性比较高的特征X，并且X不受到实验分组影响。定义一个新的目标变量$Y'=Y -\theta X$
则有:
$$Var(Y')=Var(Y)(1-\rou^2)$$
从而Y'的方差是要比Y的方差小的，而且X与Y相关性越大，这个差值的方差越小。
比如：如果实验的观察变量是每周酒店订阅数，那么协变量可以是开始实验之前的那周酒店的订阅量


- post- stratification [13] 分层采样

- 作者提出的variance-weighted estimators
根据前面分层采样的方式，不同的数据group可以采用不同的权重，这个估计量还是无偏的，所以可以设计合适的权重让总体的方差尽可能小。
![](../../../Draft/media/Pasted%20image%2020220601224526.png)


### 确定样本量
整体确定样本量的方法是类似的，不同的指标细节会有不同，大致都是根据置信区间保证误差在一定范围内，然后反解出样本量
[参数估计-样本量的确定](../参数估计-样本量的确定.md)



## 3. 常见问题

### (1) ab-test的结果和实际上线后的结果不一致
比如ab-test的时候发现指标上涨10%，但是上线后指标却是持平

1. ab-test实验是否合理
	1. 样本量是否充足，指标结果是统计显著的吗
	2. 实验时间短，可能有”新奇效应“
	3. 实验人群和线上人群不一致，比如区域、流量源
2. 外部环境。比如不同时间段、节假日、政策、舆论等




## reference

提高实验敏感性 《Variance-Weighted Estimators to Improve Sensitivity in Online Experiments》

[9]  William Fithian and Daniel Ting. 2017. Family learning: nonparametric statistical inference with parametric efficiency.


