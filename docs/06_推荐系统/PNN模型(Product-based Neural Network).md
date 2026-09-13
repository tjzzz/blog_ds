> 在NeuralCF的基础上，加入多组特征。2016年，上海交通大学的研究人员提出的PNN[5]模型。


网络结构：
![500](../../Input/media/Pasted%20image%2020230601170249.png)
- 乘积层部分：z表示的是内积操作部分，p表示的是外积操作部分。无论是内积还是外积，都要求前面embedding向量的维度相同。



与deep crossing模型的区别在于，PNN用乘积层代替了stacking层，即不同特征的embedding向量不是简单的拼接，而是两两乘积操作之后再拼接。

product层特征交叉的两种方式：
- 内积$g_{inner} = <f_i, f_j>$
- 外积 $g_{outer}=f_if_j^T$，生成的是一个矩阵
