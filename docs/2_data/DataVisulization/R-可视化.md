# 基于R的
[TOC]

|   |  链接|说明  |
| --- | --- | --- |
| Flexdashboard | http://rmarkdown.rstudio.com/flexdashboard/ |  |
| Bookdown |  |  |

## rCharts
http://rdatascience.io/rCharts/

作者的github主页
http://ramnathv.github.io/rCharts

```r
#Install 
require(devtools)## 标题 ##
install_github('rCharts', 'ramnathv')
library(recharts)

```


## recharts

网上使用的多是`library(devtools),install_github("madlogos/recharts")` 其github上已经弃用，现在用的是
https://echarts4r.john-coene.com/
https://github.com/JohnCoene/echarts4r

其更新比较快，目前是2020-10-16版本
教程 https://echarts4r.john-coene.com/articles/get_started.html


 

## shiny

```r
# Define the location '/specialApp'
location /specialApp {
  app_dir /srv/shiny-server/myApp;
}
```


1.	jumbo 安装R

install.packages("shiny") 

这里http://www.rstudio.com/products/shiny/download-server/ 提供了下载链接，需要提供邮箱才会出现下载页面，选择对应Linux发行版的Shiny Server进行下载。我这里是CentOS 6.5.
执行如下命令：
wget -c http://download3.rstudio.org/centos-5.9/x86_64/shiny-server-1.2.3.368-x86_64.rpm
 
 `yum install –nogpgcheck shiny-server-1.2.3.368-x86_64.rpm`
 
 
 2.http://docs.rstudio.com/shiny-server/
 
 

 配置路径：
  /opt/shiny-server/config/default.config



现在Rshiny的前端图已经很好看了

Rshiny的例子
https://danielrivera1.shinyapps.io/Regression2/?_ga=2.36422883.2103375248.1623299619-1342804995.1612247225




## bookdown

bookdown是基于markdown，knitr用来进行write book的一个package。
其主要功能和markdown差不多，参考gitbook的方式，能基于Rmd或者md进行书写。


- 安装
加载一些html widgets
首先安装相应的支持包
```R
install.packages("webshot")
webshot::install_phantomjs()
```

- 输出格式
在`_output.yaml`中进行设置
(1)html格式
- gtbook style

- 生成
实时预览
serve_book(dir='.', output_dir="_book",preview=TRUE, in_session=TRUE)