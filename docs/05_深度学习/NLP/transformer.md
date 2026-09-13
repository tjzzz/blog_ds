> [Attention Is All You Need](https://link.zhihu.com/?target=https%3A//arxiv.org/abs/1706.03762)

#todo 

本身是一种seq2seq


## 整体结构

transformer的整体机构主要由encoder和decoder两大部分组成，

大致的训练过程如下：

### 1. 输入
transformer中单词的输入表示x由单词embedding和位置embeding两个部分相加得到。
Transformer 中除了单词的 Embedding，还需要使用位置 Embedding 表示单词出现在句子中的位置。**因为 Transformer 不采用 RNN 的结构，而是使用全局信息，不能利用单词的顺序信息，而这部分信息对于 NLP 来说非常重要。**所以 Transformer 中使用位置 Embedding 保存单词在序列中的相对或绝对位置。



![Drawing 2023-04-18 19.08.18.excalidraw](../../../附件/Excalidraw/Drawing%202023-04-18%2019.08.18.excalidraw.md)







## 参考

https://zhuanlan.zhihu.com/p/338817680
https://www.youtube.com/watch?v=ugWDIIOHtPA&list=PLJV_el3uVTsOK_ZK5L0Iv_EQoL1JefRL4&index=61
