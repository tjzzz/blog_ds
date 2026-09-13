

# pyspark提交任务相关配置


相关配置

- spark.driver.memory  
- spark.executor.memory




##




上传包
https://www.jianshu.com/p/92be93cfbb97

https://blog.csdn.net/weixin_42649077/article/details/84976960



http://www.it1352.com/220302.html


http://ju.outofmemory.cn/entry/171843


## 端口
http://master:4040spark 默认端口是4040，如果被占用，就往下寻找4041，4042......可获得这些信息：（1）stages和tasks调度情况；（2）RDD大小及内存使用；（3）系统环境信息；（4）正在执行的executor信息。



---





https://blog.csdn.net/weixin_39966130/article/details/111025571



https://www.cnblogs.com/piperck/p/10121097.html


http://spark.apache.org/docs/latest/api/python/user_guide/python_packaging.html#using-pyspark-native-features

https://www.cnblogs.com/yanshw/p/12083488.html

## 1. 单独执行py

python依赖包问题：

### method1 
可以加载自己写的包，但是不能加载环境自带的那种
pyspark.SparkContext.addPyFile() 

### method2 conda
建议使用
conda-pack 来打包PYTHON独立运行时环境

(1) 先创建一个虚拟环境，在里面安装好各种包
```
conda create -y -n logstat_conda_env python=3.7
```


/root/miniconda3/envs/logstat_conda_env/bin/python ../run.py -e instar.yaml -m other 

```
conda install -c conda-forge conda-pack
conda pack -f -o pyspark_conda_env.tar.gz
```



## 任务并行

apt-get install parallel
https://www.myfreax.com/gnu-parallel/

## 删除任务

kinit -kt /tmp/bigdata.keytab bigdata

yarn application -kill application_1636027123861_53567


https://example.com:8443/gateway/cluster-topo/yarn/cluster/scheduler


hdfscli 


## QQ
1. 提交yarn集群后，发现自己任务所在的队列同时只能跑两个job

![](../../media/Pasted%20image%2020220101081827.png)

追查:
- 所在队列的配置，自己两个任务一个设置的是10g，一个设置的是15g。现在runing-containners各自是2个，所有算下来大概是50多g
- 优化
	- [ ] 改成one container? => --num-executors  2      　　 # executor 数量
	- [ ] 合并p1和p2的代码逻辑？
	- [ ] 实验下可否调整memory，能同时并行更多任务
	- [ ] 逻辑上，可以把一些费时的，不要求最新的单独处理先例行到一个表


实验记录:
- 最新结果： p1+p2一起跑，3个并发，2ml+1data-platform
	- 2:30, 到7.30跑完了40个。 10点58个完成，63all
