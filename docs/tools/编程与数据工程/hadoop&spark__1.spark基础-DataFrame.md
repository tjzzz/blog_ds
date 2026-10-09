---
title: "1.spark基础-DataFrame"
created: 2026-10-09
updated: 2026-10-09
tags: [llm-wiki, migrated]
source: ["Input/rebuild_source_2026-10-09/07_语言篇/hadoop&spark/1.spark基础-DataFrame.md"]
wiki_type: tools
topic: "编程与数据工程"
migrated_from: "07_语言篇/hadoop&spark/1.spark基础-DataFrame.md"
review_status: structural
---

> 所属 Topic：[编程与数据工程](../../topics/%E7%BC%96%E7%A8%8B%E4%B8%8E%E6%95%B0%E6%8D%AE%E5%B7%A5%E7%A8%8B.md) · 类型：工具

# 1.spark基础-DataFrame


spark SQL是spark处理结构化数据的一个模块。


```
df.printSchema()
df.select(df['name'], df['age'] + 1).show()
df.groupBy("age").count().show()
```


**dataframe使用sql的方式进行操作**
SparkSeession的sql函数可以让应用程序以编程的方式运行SQL查询，并将结果以一个dataframe返回。例如：

```
# Register the DataFrame as a SQL temporary view
df.createOrReplaceTempView("people")
sqlDF = spark.sql("SELECT * FROM people")
sqlDF.show()
```



## spark.df 与pandas.df的转化

spark的dataframe与pandas的dataframe略微不同(https://blog.csdn.net/u013613428/article/details/78138857)，可以通过如下的方式进行转化

```python
# spark转pandas
spark_df.toPandas()
# pandas 转spark
sqlContext = SQLContext(SparkContext())
sparkContext= sqlContext.createDataFrame(df)
```
注意如果pandas的dataframe中有空值，在转spark的df时候会报错，需要将缺失数据
`df =df.replace(np.NaN, '')`


pyspark系列--pyspark读写dataframe
https://zhuanlan.zhihu.com/p/34901558

