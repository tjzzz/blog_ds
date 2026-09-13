#nlp

embedding-嵌入/向量化，是深度学习中的一个“基础核心操作”，其使用场景非常广泛。


# 基础概念
形式上来说，embedding就是用一个低维稠密的向量表示一个对象(比如，一个词、商品等等)， 而embedding一开始也是源自于nlp中词向量生成问题开始的。


## [word2vec](word2vec.md)

2013年google提出


## item2vec

在Word2vec 诞生之后，Embedding的思想迅速从自然语言处理领域扩散到几乎所有机器学习领域，推荐系统也不例外。
推荐系统中通过矩阵分解产生了用户隐向量和物品隐向量，如果从Embedding的角度看待矩阵分解模型，则用户隐向量和物品隐向量就是一种用户Embedding向量和物品Embedding向量。由于Word2vec的流行，越来越多的Embedding方法可以被直接用于物品Embedding向量的生成，而用户Embedding 向量则更多通过行为历史中的物品Embedding 平均或者聚类得到。利用用户向量和物品向量的相似性，可以直接在推荐系统的召回层快速得到候选集合，或在排序层直接用于最终推荐列表的排序。正是基于这样的技术背景，微软于2016年提出了计算物品Embedding向量的方法Item2vec。

Item2vec 利用的“物品序列”是由特定用户的浏览、购买等行为产生的历史行为记录序列。
$$\frac{1}{K}\sum_{i=1}^K\sum_{j\ne i}^K log p(w_j|w_i)$$
- item2vec与word2vec的主要区别在于item2vec没有时间窗口的概念，它认为序列中任意两个物品都是相关的。
- 



## Graph embedding
Word2vec和由其衍生出的Item2vec是Embedding技术的基础性方法，但二者都是建立在“序列”样本（比如句子、用户行为序列）的基础上的。在实际场景中，很多时候数据对象之间有时候是呈现的图的结构。
![](../../../Input/media/Pasted%20image%2020230602221019.png)

Graph Embedding是一种对图结构中的节点进行Embedding编码的方法。最终生成的节点Embedding 向量一般包含图的结构信息及附近节点的局部相似性信息。几种主流的graph embedding方式如下：

### DeepWalk
> 早期，影响力较大的Graph Embedding方法是于2014年提出的DeepWalk
《Billion-scale Commodity Embedding for E-commerce Recommenderin Alibaba》

它的主要思想是在由物品组成的图结构上进行随机游走，产生大量物品序列，然后将这些物品序列作为训练样本输入Word2vec 进行训练，得到物品的Embedding。因此，DeepWalk可以被看作连接序列Embedding和GraphEmbedding的过渡方法。

### Node2vec
> 2016年，斯坦福大学的研究人员在DeepWalk的基础上更进一步，提出了Node2vec模型

网络的“同质性”指的是距离相近节点的Embedding应尽量近似。
“结构性”指的是结构上相似的节点的Embedding 应尽量近似，图4-8中节点U和节点s6都是各自局域网络的中心节点，结构上相似，其Embedding的表达也应该近似，这是“结构性”的体现。

如何设置node节点之间的跳转关系？
假设当前从t跳转到v，然后再从v跳转到下一个节点x。从v跳转到下一个节点x的概率是与(t,x)之间的距离有关的。$p_{vx}=a(t, x)w_{vx}$
- wvx表示边vx的权重
- a(t, x)，当d(t, x) =0时， a=1/p，距离为0，即返回t
- 当d(t, x) = 1时候， a=1
- 当d(t, x) =2时候， a =1/q

![300](../../../Input/media/Pasted%20image%2020230603164331.png)

同质性相同的物品很可能是同品类、同属性，或者经常被一同购买的商品，而结构性相同的物品则是各品类的爆款、各品类的最佳凑单商品等拥有类似趋势或者结构性属性的商品


### EGES
> 2018年，阿里巴巴公布了其在淘宝应用的Embedding方法EGES(Enhanced Graph Embedding with Side Information)[9]，其基本思想是在DeepWalk生成的Graph Embedding基础上引入补充信息。

如何融合一个物品的多个Embedding向量，使之形成物品最后的Embedding呢？最简单的方法是在深度神经网络中加入平均池化层，将不同Embedding平均起来。为了防止简单的平均池化导致有效Embedding信息的丢失，阿里巴巴在此基础上进行了加强，对每个Embedding 加上了权重
![](../../../Input/media/Pasted%20image%2020230603172058.png)



#toread https://zhuanlan.zhihu.com/p/328481154


