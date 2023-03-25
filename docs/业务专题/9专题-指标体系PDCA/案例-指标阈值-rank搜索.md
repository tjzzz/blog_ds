
## 1.dab类指标

newpo, po, rank, rr, f1 最终计算方式都是 $$dab_{xx} = 0.5\frac{\sum awin -\sum bwin}{\sum awin + \sum bwin + \sum tie}$$

其中awin，bwin，tie可以按照不同的逻辑或方法进行计算。

$$p_1 = \frac{\sum awin}{\sum awin + \sum bwin + \sum tie}$$

$$p_2 = \frac{\sum bwin}{\sum awin + \sum bwin + \sum tie}$$



基于有点有diff的流量：
每次pv下，awin，bwin，tie必然出现且只出现其一。因此p1可以看做策略好的概率， p2可以看做基线好的概率。 概率本身是服从两点分布的，每次pv取0或1，样本量较大的时候(一般interleaving实验的样本量足够大了)，可以近似成正态分布，即有

$$p_1 - N(P_1,P_1(1-P_1)/n1 )$$
$$p_2 - N(P_2,P_2(1-P_2)/n1 )$$

所以两者的差也是近似正态分布，有(注意P1与P2并不是相互独立的)

$$p_1 - p_2 ~ N(P_1 - P_2, \frac{(P_1+P_2-(P_1-P_2)^2)}{n})$$

所以dab的置信区间就是

$$[\frac{p_1 -p_2}{2}- z_{\alpha}\sqrt \frac{p_1+p_2-(p_1-p_2)^2}{4n}, \frac{p_1 -p_2}{2}+ z_{\alpha}\sqrt \frac{p_1+p_2-(p_1-p_2)^2}{4n}]$$

## 根据空转确定阈值
空转时候理论上两边是没diff的，但是因为随机波动，产出的指标数据肯定不可能完全等于0，大概率上也是服从一个正态分布。根据小概率原理，在5%和95%的置信点上可以认为是异常值，就策略和基线不是持平而是有显著diff。
对应的阈值就是


 $$z_{\alpha}\sqrt \frac{p_1+p_2-(p_1-p_2)^2}{4n}= z_{\alpha}\sqrt \frac{p}{2n}$$
 
 所以这个阈值是与本身的p值的大小有关，与样本量也有关。
 
 


