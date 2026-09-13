---
update_time: "2026-09-11 11:41:44 CST"
---


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



