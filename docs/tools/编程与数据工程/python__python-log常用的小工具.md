---
title: "python-log常用的小工具"
created: 2026-10-09
updated: 2026-10-09
tags: [llm-wiki, migrated]
source: ["Input/rebuild_source_2026-10-09/07_语言篇/python/python-log常用的小工具.md"]
wiki_type: tools
topic: "编程与数据工程"
migrated_from: "07_语言篇/python/python-log常用的小工具.md"
review_status: structural
---

> 所属 Topic：[编程与数据工程](../../topics/%E7%BC%96%E7%A8%8B%E4%B8%8E%E6%95%B0%E6%8D%AE%E5%B7%A5%E7%A8%8B.md) · 类型：工具

# log常用的小工具


## pyinter 区间相关运算
`pyinter` 包是用来处理区间相关运算的.

创建区间，区间有开区间和闭区间，可以用如下方法创建。 

* 创建左闭右开 `pyinter.closedopen(5, 10)`
* 创建闭区间 `pyinter.closed(5,10)`
* 开区间 `pyinter.open(5,10)`


**IntervalSet**
A class to hold collections of intervals, otherwise known as discontinuous ranges

```python
import pyinter
## 取一下区间的并集
res = [[22, 51], [176, 179], [177, 179]]
intervals = pyinter.IntervalSet([pyinter.closed(a, b) for a,b in res])
```

参考: https://pyinter.readthedocs.io/en/latest/

## ordered_yaml_load

```
def ordered_yaml_load(yaml_path, Loader=yaml.Loader,
                      object_pairs_hook=OrderedDict):
    """
    顺序load yaml结构
    #exp_info = yaml.load(open(exp_conf))
    ### 因为在读取metric的时候需要保证metric的顺序，
    # 但是默认的yaml.load()进来的词典是不保证顺序的
    # 参考： http://axiaoxin.com/article/220/
    """
    class OrderedLoader(Loader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))
    OrderedLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
                                  construct_mapping)
    with open(yaml_path) as stream:
        return yaml.load(stream, OrderedLoader)
```

## python查看和更改当前工作目录
```
import os
os.getcwd()    #获取当前工作目录
os.chdir("目标目录")   #修改当前工作目录
```