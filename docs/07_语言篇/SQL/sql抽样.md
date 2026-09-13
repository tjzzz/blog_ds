# sql抽样

## 随机抽样rand()
rand()函数可以返回一个0-1之间的随机值。



| 语法                                  | 说明                                                                                                                                                                                            |
|:------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| order by rand()&nbsp;               | 只启用一个reduce，全局排序比较耗时                                                                                                                                                                          |
| sort by rand()                      | 分区有序                                                                                                                                                                                          |
| distribute by rand() sort by rand() | distribute 和sort关键字可以保证在mapper和reducer阶段是随机的，这个时候等价于全局随机                                                                                                                                      |
| cluster by rand()                   | <p class="p1" style="margin: 0px; font-variant-numeric: normal; font-variant-east-asian: normal; font-stretch: normal; line-height: normal;">是 distribute by 和 sort by 的功能相结合，速度上会快一些<br></p> |  




(1) 按照原始的数据频次分布进行抽样

```sql
select xxx from my_table
distribute by rand() sort by rand()
limit 6000
```

```sql
select xxx from my_table
where rand() < 0.001    --- 先加一个预处理减少数据量
distribute by rand() sort by rand()
limit 6000
```




(2) 如果原始数据是按照频次汇总的，如何抽样？
比如数据是两列： user_id + 展现频次freq


```SQL
select
    *
from
    (
        select
            *, 
            concat('1', repeat(',1', freq)) as freq_str
        from
            base_table
    ) raw_tab 
LATERAL VIEW explode(split(freq_str, ',')) tmp as freq_raw
```


## tablesample()

### 分桶抽样(桶表抽样)

hive中分桶其实就是根据某一个字段Hash取模，放入指定数据的桶中，比如将表table按照ID分成100个桶，其算法是hash(id) % 100，这样，hash(id) % 100 = 0的数据被放到第一个桶中，hash(id) % 100 = 1的记录被放到第二个桶中。

分桶抽样语法： TABLESAMPLE (BUCKET x OUT OF y [ON colname])

其中x是要抽样的桶编号，桶编号从1开始，colname表示抽样的列(也就是按照那个字段分桶)，y表示桶的数量。 所以表达的意思是按照colname字段分成y桶，抽取其中的第x桶


```sql
select xxx from my_table
TABLESAMPLE (BUCKET 1 OUT OF 1000 [ON rand()])
limit 6000
```


## 参考
https://zhuanlan.zhihu.com/p/344631420

