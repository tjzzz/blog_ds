# 1.直接抓取网页
 BeautifulSoup

## 参考资料

* https://cuiqingcai.com/1319.html


## 1.基础操作
Beautiful Soup将复杂HTML文档转换成一个复杂的树形结构,每个节点都是Python对象,所有对象可以归纳为4种:

* Tag
Tag 是什么？通俗点讲就是 HTML 中的一个个标签，例如


* NavigableString
既然我们已经得到了标签的内容，那么问题来了，我们要想获取标签内部的文字怎么办呢？很简单，用 .string 即可，例如

* BeautifulSoup

* Comment


## 2.遍历文档树

（1）直接子节点
> 要点：.contents  .children  属性

.contents

tag 的 .content 属性可以将tag的子节点以列表的方式输出


print soup.head.contents 

print soup.head.contents 



## CSS选择器
我们在写 CSS 时，标签名不加任何修饰，类名前加点，id名前加 `#`，在这里我们也可以利用类似的方法来筛选元素，用到的方法是 soup.select()，返回类型是 list

