
---
#hive #sql
---

# 1.基础知识

## join方式

left join： 尽量左边的表小一些，可以加快速度
right join 用的不多，一般可以用left join重写
inner join
full join


## group by
聚合函数

需要注意的是 where以及having的细节

### group by having

where 语句在使用聚合函数时候不能使用，所以如果在group by后还有筛选需要使用having函数。

当同时含有where⼦句、group by ⼦句 、having⼦句及聚集函数时，执⾏顺序如下：
1、执⾏where⼦句查找符合条件的数据；
2、使⽤group by ⼦句对数据进⾏分组；
3、对group by ⼦句形成的组运⾏聚集函数计算每⼀组的值；

比如



## window函数-查询分组的topN
https://blog.csdn.net/weixin_45003816/article/details/103721121
https://zhuanlan.zhihu.com/p/92654574

窗口函数的基本用法
```
<窗口函数> over (partition by xxx order by xxx)
```

常见的window函数：
### rank类
它们通过排序特定列来为每行分配一个排名。如果给出了任何分区列，则行将在其所属的分区组中排名
- row_number: 分组后每一行会有一个唯一的编号
- rank: 也为每一组的行生成一个序号，与ROW_NUMBER()不同的是如果按照ORDER  
BY的排序，如果有相同的值会生成相同的序号，并且接下来的序号是不连序的。例如两个相同的行生成序号3，那么接下来会生成序号5。
- dense_rank:  和rank类似，不同的是如果有相同的序号，那么接下来的序号不会间断。也就是说如果两个相同的行生成序号3，那么接下来生成的序号还是4。
- NTILE (integer_expression) 按照指定的数目将数据进行分组，并为每一组生成一个序号


比如：筛选每个部门中薪水的topN
```sql

WITH T AS (SELECT *, ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY employee_salary DESC) AS rank_in_dep FROM employee_salary)

SELECT * FROM T WHERE rank_in_dep
```



### 聚合类
sum, avg, count, max, min 注意这里最终的结果是累积的。都是针对自己记录前面(包括自己)的数据范围做操作.

注意：
(1) count(*) over(partition by 分组字段 )  等同于group by 只是数据行数不变
这种用法在上一篇中已将讲过，是2005、2008中新增的功能。

(2) count(*) over(partition by 分组字段  order by 字段)
这种用法就是先按照分组字段分组，然后在每一个分组中排序，那么这个时候count计算的是一个 累积的值。




### lag和lead
对于时序类的数据，希望计算最近3天、相邻的差值的时候可以使用。
lag(指标名, num, defaultvalue)   # 取出同一字段前面第num行
lead(指标名, num, defaultvalue)  # 后面的第n行

比如:
```sql
SELECT name,
       --用户名
       checkdate,
       --抄表日期
       pq,
       --抄表值
       lag(pq,1,0) over(partition BY name
                        ORDER BY checkdate DESC) AS pq1 --前一天抄表值
FROM dim_a_check;
```

## 数据重复问题




## null问题

- sql语句过滤条件中，= 或者!= (等价于<>)只能判断基本的数据类型，即null不会做判断。
- `<=>` 既能判断null又能判断基本类型

null的判断 is null， is not null

`<=>` 是NULL安全的等值比较运算符，该操作符作用类似“=”。区别为当符号两边出现NULL值时，=操作符会返回NULL，而<=>会返回1（两边操作数都为NULL时）或者0（一边操作数为NULL）。

例子：挑选referee_id不是2的(注意其中有null)

```sql
select name from customer
where referee_id != 2 or referee_id is null
```

```SQL
select name from customer
where not referee_id <=> 2
```


## 常用的

### case when



### 从指定行数查

offset：查询结果偏移量（从第⼏⾏开始显⽰）
limit：限制查询结

比如 select * from xx offset 2 limit 10 即查询第3-12行
```
select * from xxx limit 2, 10
```






## update
```sql
update table_name 
set course_name='DB',course_grade=3.5
WHERE course_id=2;

```


## delete
用delete命令删除表中的重复数据， id+email两列
MySQL环境下：

```sql
delete from Person 
where Id not in (
    select * from(
        select min(Id)
        from Person
        group by Email) t);
```

注意：在MYSQL中，不能先Select一个表的记录，再按此条件Update和Delete同一个表的记录，否则会出错：You can't specify target table 'xxx' for update in FROM clause.

解决方法：使用嵌套Select——将Select得到的查询结果作为中间表，再Select一遍中间表作为结果集，即可规避错误。



## Examples

### 分布topN
考察窗口函数
[184. 部门工资最高的员工](https://leetcode-cn.com/problems/department-highest-salary/)
```SQL

select Department, Employee, salary from

(select *, RANK() over (partition by Department order by salary desc ) as rnk

from

(select e.name as Employee, Department.name as Department, salary from Employee e left join

Department on e.departmentId = Department.id

) b

) c where rnk =1

```





# 2. tools
sql 数据血缘
http://sqllineage.com/doc


## sqlflow
https://github.com/sqlparser/sqlflow_public






hive时间戳


1 日期转为时间戳
select unix_timestamp(string date, date的格式)

```sql
select unix_timestamp('2019-08-15 16:40:00','yyyy-MM-dd HH:mm:ss')   --1565858400
```

2 时间戳转日期

from_unixtime(bigint unixtime,string format)
如果时间戳是13位的话，需要先转成10位的。

```sql
select from_unixtime(1565858389,'yyyy-MM-dd HH:mm:ss')
select from_unixtime(cast(1553184000488/1000 as int),'yyyy-MM-dd HH:mm:ss')   --2019-03-22 00:00:00
```



