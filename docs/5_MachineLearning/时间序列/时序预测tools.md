

https://github.com/topics/traffic-prediction


https://zhuanlan.zhihu.com/p/67832773



## Prophet

相关介绍: https://zhuanlan.zhihu.com/p/52330017
论文: 《forecasting at scale》https://peerj.com/preprints/3190.pdf
facebook的prophet是进行时间序列相关建模的工具箱，并且提供了python和R的接口。除此之外时间序列的异常检测也可以使用该工具。

原理简单说明:
通常对于时间序列，常见的处理方式就是进行==序列分解==，将一条时间序列分解为季节趋势、趋势项、剩余项目。形式可以是加法或者乘法的形式。
$$y_t = S_t + T_t + R_t$$
在prophet中考虑了季节、趋势、节假日因素。即$y_t = g(t) + T_t + h_t + R_t$. 具体来说:

### 1 趋势项$g(t)$
prophet算法中，关于趋势项的预测有两种方式
(1) 基于逻辑回归
一般的sigmoid形式是$y=C/(1+e^{-k(x-m)})$，然而在实际场景中， 参数不会是常数的，而是随着时间变化的。所以在Prophet里面，作者将三个参数全部换成了随时间变化的函数$y=C(t)/(1+e^{-k(t)(x-m(t))})$

(2) 基于分段线性函数(默认的)
https://github.com/facebook/prophet/blob/master/python/fbprophet/forecaster.py

变点的选择 changepoint

**2.季节项**
傅里叶级数

关于prophet初始化时候的参数，可以参照`forecaster.py`



## Neural Prophet
官网简单的ppt说明：https://github.com/ourownstory/neural_prophet/blob/master/notes/NeuralProphet_Introduction.pdf

相比与prophet，主要更新如下：
-  第一个巨变是分解的分量增加了一个重量级的AR（自回归），这个是超级重量级的。并且AR模型用的是神经网络的方式. AR-net
- 第二个巨变是Pytorch作为backend
-  Global model 应该还在开发中，支持多个序列同时建模


![](../../../Draft/media/Pasted%20image%2020220301140318.png)


例子:

```python
from neuralprophet import NeuralProphet

## 默认，等同于prophet
m_baseline = NeuralProphet()
df_train, df_test = m_baseline.split_df(df, freq='D', valid_p = 0.20)
plt.figure(figsize=(20,16))
metrics = m_baseline.fit(df_train, freq='D',validation_df=df_test, plot_live_loss=True)

## 增加AR
m_add_lag = NeuralProphet(
    growth='off',
    n_lags=7,
    ar_sparsity=0.95,
    learning_rate = 0.003,
)


m_add_lag = NeuralProphet(
    growth='off',
    n_lags=7,
    num_hidden_layers=4,
    d_hidden=16,
    learning_rate=0.003,
)



## 增加lagged regressors
m = NeuralProphet(
    n_forecasts=24,
    n_lags=24,
    learning_rate=0.01,
)
m = m.add_lagged_regressor(names=xx_list)
m.highlight_nth_step_ahead_of_each_forecast(24)
metrics = m.fit(df, freq="H")


```



NeuralProphet详细的输入参数说明:
https://neuralprophet.com/html/hyperparameter-selection.html
- n_lags=0, 是否使用AR-net，用于指定自回归的阶数
- 模型训练相关参数： epochs，learning_rate, batch_size
- loss_func=Huber, 可以自己指定其他损失函数 torch.nn.modules.loss
- num_hidden_layers, d_hidden
- 趋势相关参数
	- trend_reg
- Seasonality Related Parameters
		- `yearly_seasonality`, `weekly_seasonality` and `daily_seasonality`



增加holidays和特殊events
```python
# history events
playoffs = pd.DataFrame({
    'event': 'playoff',
    'ds': pd.to_datetime([
        '2008-01-13', '2009-01-03', '2010-01-16',
        '2010-01-24', '2010-02-07', '2011-01-08',
        '2013-01-12', '2014-01-12', '2014-01-19',
        '2014-02-02', '2015-01-11', '2016-01-17',
        '2016-01-24', '2016-02-07',
    ]),
})

superbowls = pd.DataFrame({
    'event': 'superbowl',
    'ds': pd.to_datetime([
        '2010-02-07', '2012-02-05', '2014-02-02',
        '2016-02-07',
    ]),
})

events_df = pd.concat((playoffs, superbowls))

# NeuralProphet Object
m = NeuralProphet(loss_func="MSE")

# set the model to expect these events
m = m.add_events(["playoff", "superbowl"])

# create the data df with events
history_df = m.create_df_with_events(df, events_df)
metrics = m.fit(history_df, freq="D")


```




## merlion

https://github.com/salesforce/Merlion#getting-started
https://opensource.salesforce.com/Merlion/v1.1.0/index.html


![](../../../Draft/media/Pasted%20image%2020220301141438.png)

merlion主要支持的功能：

- merlion.models
	- [`merlion.models.anomaly`](https://opensource.salesforce.com/Merlion/v1.1.0/merlion.models.anomaly.html#module-merlion.models.anomaly "merlion.models.anomaly"): Anomaly detection models
	-   [`merlion.models.anomaly.change_point`](https://opensource.salesforce.com/Merlion/v1.1.0/merlion.models.anomaly.change_point.html#module-merlion.models.anomaly.change_point "merlion.models.anomaly.change_point"): Change point detection models
	-   [`merlion.models.forecast`](https://opensource.salesforce.com/Merlion/v1.1.0/merlion.models.forecast.html#module-merlion.models.forecast "merlion.models.forecast"): Forecasting models
	-   [`merlion.models.anomaly.forecast_based`](https://opensource.salesforce.com/Merlion/v1.1.0/merlion.models.anomaly.forecast_based.html#module-merlion.models.anomaly.forecast_based "merlion.models.anomaly.forecast_based"): Forecasting models adapted for anomaly detection. Anomaly scores are based on the residual between the predicted and true value at each timestamp.
	-   [`merlion.models.ensemble`](https://opensource.salesforce.com/Merlion/v1.1.0/merlion.models.ensemble.html#module-merlion.models.ensemble "merlion.models.ensemble"): Ensembles & automated model selection of models for both anomaly detection and forecasting.
	-   [`merlion.models.automl`](https://opensource.salesforce.com/Merlion/v1.1.0/merlion.models.automl.html#module-merlion.models.automl "merlion.models.automl"): AutoML layers for various models
- merlion.transform
- merlion.post_process
- merlion.evaluate
- merlion.plot




异常检测：

- 模型初始化
所有的模型初始化都是通过`ModelClass(config)`的方式

```python
## 1. 模型初始化
from merlion.models.anomaly.isolation_forest import IsolationForest, IsolationForestConfig
from merlion.models.anomaly.windstats import WindStats, WindStatsConfig
from merlion.models.anomaly.forecast_based.prophet import ProphetDetector, ProphetDetectorConfig

# Import a post-rule for thresholding
from merlion.post_process.threshold import AggregateAlarms
# Import a data processing transform
from merlion.transform.moving_average import DifferenceTransform


config1 = IsolationForestConfig()
model1  = IsolationForest(config1)

# We use a WindStats model that splits each week into windows of 60 minutes
# each. Anomaly scores in Merlion correspond to z-scores. By default, we would
# like to fire an alert for any 4-sigma event, so we specify a threshold rule
# which achieves this.
config2 = WindStatsConfig(wind_sz=60, threshold=AggregateAlarms(alm_threshold=4))
model2  = WindStats(config2)

# Prophet is a popular forecasting algorithm. Here, we specify that we would like
# to pre-processes the input time series by applying a difference transform,
# before running the model on it.
config3 = ProphetDetectorConfig(transform=DifferenceTransform())
model3  = ProphetDetector(config3)



```

```python
## 2.模型训练

model.train(train_data=train_data, anomaly_lables=None)


scores = model.get_anomaly_score(test_data)
labels = model.get_anomaly_label(test_data)

```



## 1.2 数据预处理
tslearn：开源的时间序列机器学习python工具包
tsfresh：开源的时间序列特征提取python工具包
https://tsfresh.readthedocs.io/en/latest/text/quick_start.html


pyts：开源的时间序列分类Python工具包。提供预处理工具及若干种时间序列分类算法

