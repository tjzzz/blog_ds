---
title: "Rspark"
created: 2026-10-09
updated: 2026-10-09
tags: [llm-wiki, migrated]
source: ["Input/rebuild_source_2026-10-09/07_语言篇/hadoop&spark/Rspark.md"]
wiki_type: tools
topic: "编程与数据工程"
migrated_from: "07_语言篇/hadoop&spark/Rspark.md"
review_status: structural
---

> 所属 Topic：[编程与数据工程](../../topics/%E7%BC%96%E7%A8%8B%E4%B8%8E%E6%95%B0%E6%8D%AE%E5%B7%A5%E7%A8%8B.md) · 类型：工具

# Rspark

官网：
http://spark.rstudio.com/
内部 wiki（链接已移除）
http://gollum.baidu.com/sparkR-starter
 dplyr
https://cran.rstudio.com/web/packages/dplyr/vignettes/introduction.html



安装步骤：

```
install.packages("sparklyr")
library(sparklyr)
#spark_install(version = "1.6.2")
# install spark
spark_install(version = "2.1.0")
```

18机器上root用户登陆,安装成功

```
#安装
install.pacakges(sparklyr)
spark_install(version = "2.1.0")
```


## list

http://wiki.baidu.com/pages/viewpage.action?pageId=35960132



## 使用demo

```{r}
# 连接
library(sparklyr)
library(dplyr)
sc <- spark_connect(master = "local")
```
或者是直接通过Rstudio的交互界面连接：
![](../../media/15113303775917/15116808579896.jpg)


在18机器的Rstudio上测试一些模型试验效果










