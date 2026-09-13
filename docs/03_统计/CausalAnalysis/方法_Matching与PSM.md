---
title: 方法_Matching与PSM
update_time: "2026-09-13 21:51:07 CST"
tags:
  - statistics/causal-inference
  - causal-method
---
Matching 的目标是：

> 在观察性数据中，为处理组找到尽可能相似的对照组，从而降低可观测选择偏差。

## 1. 适用场景

- treatment 不是随机分配；
- 处理组和对照组在用户属性、历史行为、渠道来源等变量上明显不平衡；
- 认为选择偏差主要来自可观测变量；
- 希望估计 ATT，即已接受处理人群的增量效果。

业务例子：某功能由用户主动使用，使用者留存更高。直接比较使用者和未使用者会高估功能效果，需要先匹配历史活跃度、付费、渠道、新老用户等变量。

## 2. 核心假设

| 假设 | 含义 |
|---|---|
| 可忽略性 | 控制 $X$ 后，treatment 近似随机 |
| 共同支撑 | 处理组和对照组在倾向得分上有重叠 |
| SUTVA | 一个用户是否接受处理不影响另一个用户结果 |

## 3. CEM、MDM、PSM 的区别

| 方法 | 直觉 | 优点 | 局限 |
|---|---|---|---|
| CEM | 先把变量粗分桶，再做精确匹配 | 直观、可解释、平衡性强 | 维度高时容易匹配不上 |
| MDM | 用马氏距离找相似样本 | 不依赖单一倾向得分 | 高维距离可能失效 |
| PSM | 用接受 treatment 的概率降维匹配 | 将多维协变量压成一个 score | 倾向得分模型设错会有偏 |

## 4. PSM 基本步骤

1. 明确 treatment、outcome、匹配前变量；
2. 用处理前变量训练倾向得分模型：

$$
p(X)=P(T=1|X)
$$

3. 检查共同支撑区间；
4. 按倾向得分匹配或加权；
5. 做平衡性检验，例如 SMD；
6. 在匹配后样本上估计处理效应；
7. 做稳健性与敏感性分析。

## 5. 平衡性诊断

常看：

- 匹配前后倾向得分分布；
- covariate balance；
- standardized mean difference，通常希望小于 0.1；
- 被丢弃样本比例；
- 极端权重比例。

## 6. 连续 treatment：GPS

如果 treatment 不是 0/1，而是连续强度，例如广告曝光次数、补贴强度、推送频率，可以考虑广义倾向得分 GPS。

GPS 的目标不是匹配二元处理组，而是估计 dose-response function：

```text
不同 treatment 强度 t 下，平均结果 E[Y(t)] 如何变化
```

旧文档 [广义倾向性匹配得分](方法_Matching与PSM.md) 中已有 GPS 的建模流程，暂保留为扩展阅读。

## 7. 常见误用

| 误用 | 问题 |
|---|---|
| 把 treatment 后变量放进匹配变量 | 会控制掉真实处理效应 |
| 不看共同支撑 | 处理组和对照组根本不可比 |
| 只匹配不做平衡性检验 | 不知道偏差是否真的降低 |
| 认为 PSM 可以解决未观测混杂 | PSM 主要解决可观测选择偏差 |

## 8. 相关旧文档

- [Matching方法](方法_Matching与PSM.md)
- [广义倾向性匹配得分](方法_Matching与PSM.md)
- [因果效应估计方法](03_无实验场景效果评估决策树.md)


---

<!-- migrated-from: 07_方法_Matching与PSM.md -->

## 旧笔记整合：CEM、PSM 与代码实现

> 迁移说明：保留原 CEM 权重、PSMEstimator、balance check 等代码细节。

matching方法本质上是一种样本调整方法，目标是提升匹配后实验组和对照组的平衡性。一般地，匹配方式可以分为：
- 精确匹配，这种现实中一般很难实现
- 非精确匹配


![Matching方法 2023-04-27 11.07.47.excalidraw](../../../附件/Excalidraw/Matching方法%202023-04-27%2011.07.47.excalidraw.md)

## CEM

> CEM  粗化精确匹配

广义匹配的基本思路就是：通过给特征分桶来做粗粒度匹配。

step1: matching
匹配部分主要是针对特征进行处理，达到实验和对照组的样本匹配。
- 对于离散型特征可以直接根据其取值进行分组，或者进行上一层维度聚合。对于连续型变量来说，就需要按照区间或者分位点进行适当分组
- 将所有样本归类后就可以放到相同的分层里了，其中没有实验或者对照组的样本层就需要进行移除
step2 平衡性检验
step3 推断
- 匹配后，需要对实验组/对照组本身的样本调整权重，假设实验组的样本权重都是1.那么对照组的权重需要按照如下方式进行
$$w_c = \frac{n_t/N_t}{n_c/N_c}$$
即实验组中该分层的比例：对照组中该分层的比例。
- 基于匹配后的样本再进行因果推断
step4 敏感性分析


### cem package

Matchit包原来是R package，由原作者开发。python-cem
API: https://cem-coarsened-exact-matching-for-causal-inference.readthedocs.io/en/latest/api.html#


简单举例：

```python
from cem import CEM
import pandas as pd
from scipy import stats
import statsmodels.api as sm
import numpy as np

c = CEM(df[xx_list], "T", "Y")   # T 是分组， Y是输出
schema = {
   'X1': ('cut', {'bins': 4}),
   'X2': ('qcut', {'q': 4}),
   'X3': ('qcut', {'q': 4})
   }
df["weight"]=c.match(schema)

df_matched=df[df["weight"]>0]
df_unmatched=df[df["weight"]==0]


## 估计处理效应
X=sm.add_constant(df_matched[["T"]+[f"X{i}"for i in range(1,7)]+["X7_A","X7_B","X7_C","X8"]])
wls = sm.WLS(df_matched["Y"],X, weights=df_matched["weight"]).fit()
print(wls.summary())


```



## PSM


共同支撑集： 匹配前实验组和对照组ps分(density)分布重合的面积。
> 两者如果没有重合的部分，则说明实验组和对照组本身差别很大，根本没办法进行匹配了


直观理解


问题，认为两者的概率近似就是同质的了？



```python
class PSMEstimator:
    def __init__(self,ps_model=LogisticRegression(penalty='none',class_weight=None),match_method="knn"):
        self.ps_model=ps_model
        self.match_method=match_method
        
    def fit_score(self,X,y):
        return self.ps_model.fit(X, y)
    
    def predict_score(self,X):
        ps_test = self.ps_model.predict_proba(X)[:, 1]
        return ps_test
    
    def roc_auc_score(self,X,y):
        return roc_auc_score(y, self.predict_score(X))
        
    
    def match(self,df,T_col,ps_name="ps",n_neighbors=1):
        # sample with replacement
        self.df=df
        self.T_col=T_col
        if self.match_method=="knn":
            treat=self.df[self.df[T_col]==1]
            control=self.df[self.df[T_col]==0]
            treat.reset_index(drop=True, inplace=True)
            control.reset_index(drop=True, inplace=True)
            neigh = NearestNeighbors(n_neighbors=n_neighbors,n_jobs=-1)
            neigh.fit(control[[ps_name]])
            distances, indices = neigh.kneighbors(treat[[ps_name]])
            indices = pd.DataFrame(indices,columns=["indice"])
            control['indice']=control.index
            df_matched=control.merge(indices,on=["indice"],how="inner").drop("indice",axis=1)
            self.df_matched=pd.concat((treat,df_matched),ignore_index=True)
            return self.df_matched     
        else:
            raise ValueError("Currently we only support knn method!")    
    def fit_match(self,df,X_cols,T_col,n_neighbors=1):
        self.T_col=T_col
        self.X_cols=X_cols
        # fit ps model
        self.fit_score(df[self.X_cols], df[self.T_col])
        # predict ps score
        df["ps"] = self.predict_score(df[self.X_cols])
        # match
        self.df_matched=self.match(df,self.T_col)
        return self.df_matched
        
    def estimate_effect(self,X_cols,Y_col='Y'):
        y=self.df_matched[Y_col]
        X=self.df_matched[[self.T_col]+X_cols]
        X = sm.add_constant(X)
        model = sm.OLS(y,X)
        results = model.fit()
        estimate=np.round(results.params[self.T_col],4)
        pvalue=np.round(results.pvalues[self.T_col],4)
        if pvalue<0.05:
            print(f"You get a significant treatment effect:{estimate}(pvalue={pvalue})")
        else:
            print(f"You get an insignificant treatment effect:{estimate}(pvalue={pvalue})")             
        return results.summary()
    
    def plot_scores(self,stat="count",common_norm=True):
        """
        Plots the distribution of propensity scores before and after matching between
        our test and control groups
        """
        assert 'ps' in self.df.columns, \
            "Propensity scores haven't been calculated, please fit and predict ps first!"
        f, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 5))
        
        sns.histplot(self.df,x="ps", hue=self.T_col, stat=stat,common_norm=common_norm,ax=ax1)
        ax1.set(xlabel='Propensity Scores',title='Propensity Scores Before Matching')
        
        sns.histplot(self.df_matched,x="ps", hue=self.T_col, stat=stat,common_norm=common_norm,ax=ax2)
        ax2.set(xlabel='Propensity Scores',title='Propensity Scores After Matching')      
        
    
    def balance_check(self,estimand="ATT",threshold_smd=0.1,threshold_vr=2,show=True):
        self.threshold_smd=threshold_smd
        self.threshold_vr=threshold_vr
        if estimand!="ATT":
            raise ValueError("Currently we don't support estimand other than ATT!")
    
        smd_all={"Covariates":[],"Mean Treated":[],"Mean Control":[],"SMD":[],"Pass SMD Check":[],"Var Ratio":[],"Pass VR Check":[],"eCDF Max":[]}
        for col in self.X_cols:
            control_array=self.df[self.df[self.T_col]==0][col].values
            treatment_array=self.df[self.df[self.T_col]==1][col].values
            t_avg,c_avg,smd,pass_smd,vr,pass_vr=self._calculate_smd(control_array,treatment_array,treatment_array)
            ks_stats,pvalue=stats.ks_2samp(control_array,treatment_array)
            smd_all["Covariates"].append(col)
            smd_all["Mean Treated"].append(t_avg)
            smd_all["Mean Control"].append(c_avg)
            smd_all["SMD"].append(smd)
            smd_all["Pass SMD Check"].append(pass_smd)
            smd_all["Var Ratio"].append(vr)
            smd_all["Pass VR Check"].append(pass_vr)
            smd_all["eCDF Max"].append(np.round(ks_stats,2))
        self.smd_all_df=pd.DataFrame(smd_all)

        smd_match={"Covariates":[],"Mean Treated":[],"Mean Control":[],"SMD":[],"Pass SMD Check":[],"Var Ratio":[],"Pass VR Check":[],"eCDF Max":[]}  
        for col in self.X_cols:
            control_array=self.df_matched[self.df_matched[self.T_col]==0][col].values
            treatment_array=self.df_matched[self.df_matched[self.T_col]==1][col].values
            all_treatment_array=self.df[self.df[self.T_col]==1][col].values
            t_avg,c_avg,smd,pass_smd,vr,pass_vr=self._calculate_smd(control_array,treatment_array,all_treatment_array)
            ks_stats,pvalue=stats.ks_2samp(control_array,treatment_array)
            smd_match["Covariates"].append(col)
            smd_match["Mean Treated"].append(t_avg)
            smd_match["Mean Control"].append(c_avg)
            smd_match["SMD"].append(smd)
            smd_match["Pass SMD Check"].append(pass_smd)
            smd_match["Var Ratio"].append(vr)
            smd_match["Pass VR Check"].append(pass_vr)
            smd_match["eCDF Max"].append(np.round(ks_stats,2))
        self.smd_match_df=pd.DataFrame(smd_match)
        if show==True:
            print("Summary of Balance for All Data")
            print(self.smd_all_df)
            print("-"*100)
            print("Summary of Balance for Matched Data")
            print(self.smd_match_df)
        return 
            
    def smd_plot(self,estimand="ATT",threshold_smd=0.1):
        if not hasattr(self,'smd_all_df'):
            self.balance_check(self,estimand=estimand,threshold_smd=threshold_smd,show=False)
        self.smd_all_df["status"]="All"
        self.smd_match_df["status"]="Matched"
        smd_plot_df=pd.concat([self.smd_all_df,self.smd_match_df])    
        smd_plot_df["absSMD"]= np.abs(smd_plot_df["SMD"])
        
        # plot
        plt.figure(figsize=(15,10))
        sns.set_style("whitegrid",{'grid.linestyle': '--'})
        sns.scatterplot(data=smd_plot_df,x="absSMD",y="Covariates",hue="status")
        plt.axvline(self.threshold_smd,linestyle ='--',color = 'red')
        return
    
    def ecdf_plot(self,X_cols):
        for col in X_cols:
            # get data
            all_c=self.df[self.df[self.T_col]==0][col].values
            all_t=self.df[self.df[self.T_col]==1][col].values
            matched_c=self.df_matched[self.df_matched[self.T_col]==0][col].values
            matched_t=self.df_matched[self.df_matched[self.T_col]==1][col].values
            ecdf_all_c=ECDF(all_c)
            ecdf_all_t=ECDF(all_t)
            ecdf_matched_c=ECDF(matched_c)
            ecdf_matched_t=ECDF(matched_t)
            ks_stats_all,pvalue_all=stats.ks_2samp(all_c,all_t)
            ks_stats_matched,pvalue_matched=stats.ks_2samp(matched_c,matched_t)
            
            
            # plot
            f, (ax1, ax2) = plt.subplots(1, 2, sharey=True, sharex=True, figsize=(15, 5))
            ax1.plot(ecdf_all_c.x, ecdf_all_c.y, label='Control')
            ax1.plot(ecdf_all_t.x, ecdf_all_t.y, label='Test')      
            ax1.set_title(f"eCDF plot of {col} for all data, KS test P-value: {np.round(pvalue_all,3)}")
            ax1.legend()
            
            ax2.plot(ecdf_matched_c.x, ecdf_matched_c.y, label='Control')
            ax2.plot(ecdf_matched_t.x, ecdf_matched_t.y, label='Test')
            ax2.set_title(f"eCDF plot of {col} for matched data, KS test P-value: {np.round(pvalue_matched,3)}")
            ax2.legend()
              
    def _calculate_smd(self,c_array,t_array,all_t_array):
        c_avg=np.round(c_array.mean(),2)
        t_avg=np.round(t_array.mean(),2)
        sf=all_t_array.std()
        smd=np.round((t_avg-c_avg)/sf,2)
        if np.abs(smd)>self.threshold_smd:
            pass_smd=False
        else:
            pass_smd=True
        if np.all((c_array==0)|(c_array==1)) and np.all((t_array==0)|(t_array==1)):
            vr=np.nan
            pass_vr=np.nan
        else:
            vr=np.round(np.var(t_array)/np.var(c_array),2)  
            if vr<self.threshold_vr and vr>1/self.threshold_vr:
                pass_vr=True
            else:
                pass_vr=False
        return t_avg,c_avg,smd,pass_smd,vr,pass_vr
        

        
        
        
```


---

<!-- migrated-from: 07_方法_Matching与PSM.md -->

## 旧笔记整合：GPS 广义倾向得分

> 迁移说明：连续 treatment 的 GPS 内容作为 Matching/PSM 扩展。

# 1. 与二分类的PSM对比

您的问题很好,论文中为什么不直接基于二分类的PSM模型做扩展来实现连续治疗的匹配和效应评估呢?

主要有以下几点原因:

1. 二分类PSM中的倾向得分平衡性质不再适用。在连续治疗中,不能简单地对不同治疗水平进行分组,割断治疗的连续范围。

2. 连续治疗中,每个单位都接受了不同水平的治疗,没有明确的治疗组和对照组。因此不适合用PSM的近邻匹配方法。

3. PSM中通过匹配实现的无关随机化假设在连续治疗中也不成立。必须引入弱无关假设来取代。

4. 广义倾向得分保留了二分类PSM中的平衡性质,可以有效调控混杂变量的影响。

5. 广义倾向得分建模更为灵活,可以直接对整个剂量-反应函数建模。不需要进行分组比较。

6. 广义模型可以避免PSM中匹配过程引入的额外随机误差。

总之,直接从二分类PSM扩展到连续治疗情况非常复杂。引入广义倾向得分是一个相对更适合的方法,可以保留PSM的一些优点,同时处理连续治疗带来的特殊问题。这篇论文给出了一个可行的广义模型框架和推断方法。


# 2.方法介绍

问题设定：
假设我们研究一个经济问题，目标变量是Y，政策因素是T(这里T是一个连续型变量)，其他控制变量X，一共有N个样本，i=1....N。我们分析的目标是估计平均效应函数 $E(Y_i(t))$

建立广义倾向得分模型一般需要满足如下两个假定：

(1) 弱无混淆性假定。即在控制了可观测的混淆变量 X 后，处理变量 T 与结果变量 Y( t) 相互独立。
$$Y(t) \perp T| X, \forall t \in T$$
(2) 平衡性质

在给定控制变量的条件下，假设处理变量的条件密度函数为$r(t, X)=f(t|X)$，则广义倾向得分定义为R=r(T, X)


## 建模流程

(1) 估计处理变量T的分布
$$T_i|X_i - N(\beta_0 +\beta_1X_i, \sigma^2)$$
这里简化成正态分布，也可以根据实际数据的情况采取对数正态分布或者其他参数估计方法。通过极大似然估计，可以得到$\beta_0, \beta_1, \sigma^2$ 的估计。则广义倾向得分GPS的估计是:
$$\hat R_i = \frac{1}{\sqrt{2\pi\hat \sigma^2}}exp^{-\frac{(T_i-\hat\beta_0 -\hat\beta_1X_i)^2}{2\sigma^2}}$$

  

(2) 估计Y的条件期望
用处理变量Ti和广义得分变量R_i 估计结果变量Y。这里可以使用参数方法进行近似，论文作者采取的是多项式拟合。然后用最小二乘法估算出相关的参数。

$$E(Y_i|T_i, R_i) = \alpha_0 + \alpha_1T_i + \alpha_2*T_i^2 +\alpha_3 R_i + \alpha_4R_i^2 + \alpha_5T_iR_I$$
(3) 根据第二步中估计的参数，可以计算不同处理强度t下结果变量的平均值。

$$E(Y(t)) = \frac{1}{N}\sum_{i=1}^N(\hat\alpha_0 + \hat\alpha_1t + \hat\alpha_2*t^2 + \hat\alpha_3 r(t, X_i) + \hat\alpha_4r(t, X_i)^2 + \hat\alpha_5t \hat r(t, X_i)$$
而对于不同处理水平下的标准误和置信区间可通过 bootstrap 方法得到。




# 参考
![财税激励政策对高新技术企业...于广义倾向得分法的实证研究_马玉琪](../../../papers/GPSM-财税激励政策对高新技术企业...于广义倾向得分法的实证研究_马玉琪.pdf)
