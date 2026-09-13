# mysql

mac安装
```
brew install mysql
```


安装及配置
https://www.jianshu.com/p/e69ddc8a47b7

https://www.jianshu.com/p/11ce77ceab3d



```
#查看端口
mysql> show global variables like 'port';


```

## 1 基础语法

### 连接join 

现在考虑怎样才能高效实现要求呢？常见的多表关联有左连接、右连接、内连接，哪些能帮助我们来实现上述要求呢？

左连接的语法：表A LEFT JOIN 表B ON 关联条件                      (从表B中找出与表A满足关联条件的行)

右连接的语法：表A RIGHT JOIN 表B ON 关联条件                   (从表A中找出与表B满足关联条件的行)

内连接的语法：表A INNER JOIN 表B ON 关联条件                   (求出表A和表B的公共集)







## 2 导入导出
### 数据读取
```python


conf = {
	'host': xxx,
	'user': xxx,
	'password': xxx,
	'database': xxx

}

import pandas as pd
import pymysql

def fetch_data(user_cmd):
		
	db_con = pymysql.connect(host=conf['host'], user=conf['user'], password=conf['password'], database=conf['database'], local_infile=True)
	
	res = pd.read_sql(user_cmd, db_con)
	
	db_con.close()

return res

cmd = "select * from xxx limit 10"

df = fetch_data(cmd)


```


`pd.read_sql`也可以执行delette，drop等操作，但是删除插入更新操作没有返回值，程序会抛出SourceCodeCloseError，并终止程序。如果想继续运行，可以try捕捉此异常。


### pandas 数据导入mysql
https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html
注意：  
1.pandas将数据转换为DataFrame时会把**缺失值**用**nan**填充~  
2.如果直接将数据用pymysql写入数据库会报错！此时需要将**nan**替换成**None** , 因为None插入数据库会被填写Null 也就是数据库中的空值。

全表替换：df=df.where(df.notnull(),None)  
单列替换：df[‘列名1’]=df[‘列名1’].where(df.notnull(),None)



(1) 使用pandas的`to_sql()`函数

pd 的 `to_sql` 不能使用 `pymysql` 的连接，否则就会直接报错。
```python
from sqlalchemy import create_engine
engine = create_engine("mysql+pymysql://root:z123456@127.0.0.1:3306/routeapp?charset=utf8")


with engine.begin() as conn:  
 data.to_sql(name='表名',con=conn,if_exists='append',index=False)

```

if_exists: 表如果存在怎么处理：
- append：追加
- replace：删除原表，建立新表再添加
- fail：什么都不干

注意传入数据的列数必须是一致的，不能多不能少，列的名字必须一致，顺序可以不一致。to_sql会将数据条转成dict形式


(2) local file方式，要求列名必须一致对齐



## 3. SQLAlchemy

https://blog.csdn.net/qq_36622490/article/details/109850409

https://www.osgeo.cn/sqlalchemy/core/connections.html


## 4. 问题debug
```
show processlist
```

-   Id: 就是这个线程的唯一标识，当我们发现这个线程有问题的时候，可以通过 kill 命令，加上这个Id值将这个线程杀掉。前面我们说了show processlist 显示的信息时来自information_schema.processlist 表，所以这个Id就是这个表的主键。
-   User: 就是指启动这个线程的用户。
-   Host: 记录了发送请求的客户端的 IP 和 端口号。通过这些信息在排查问题的时候，我们可以定位到是哪个客户端的哪个进程发送的请求。
-   DB: 当前执行的命令是在哪一个数据库上。如果没有指定数据库，则该值为 NULL 。
-   Command: 是指此刻该线程正在执行的命令。这个很复杂，下面单独解释
-   Time: 表示该线程处于当前状态的时间。
-   State: 线程的状态，和 Command 对应，下面单独解释。
-   Info: 一般记录的是线程执行的语句。默认只显示前100个字符，也就是你看到的语句可能是截断了的，要看全部信息，需要使用 show full processlist。