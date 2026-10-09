---
title: "tensorflo"
created: 2026-10-09
updated: 2026-10-09
tags: [llm-wiki, migrated]
source: ["Input/rebuild_source_2026-10-09/07_语言篇/tf/tensorflo.md"]
wiki_type: tools
topic: "编程与数据工程"
migrated_from: "07_语言篇/tf/tensorflo.md"
review_status: structural
---

> 所属 Topic：[编程与数据工程](../../topics/%E7%BC%96%E7%A8%8B%E4%B8%8E%E6%95%B0%E6%8D%AE%E5%B7%A5%E7%A8%8B.md) · 类型：工具

# TF2.0 
https://tensorflow.google.cn/tutorials/images/classification


```
一个简单的方法是创建一个新的 Model 来输出你所感兴趣的层：

from keras.models import Model

model = ...  # 创建原始模型

layer_name = 'my_layer'
intermediate_layer_model = Model(inputs=model.input,
                                 outputs=model.get_layer(layer_name).output)
intermediate_output = intermediate_layer_model.predict(data)
或者，你也可以构建一个 Keras 函数，该函数将在给定输入的情况下返回某个层的输出，例如：

from keras import backend as K

get_3rd_layer_output = K.function([model.layers[0].input],
                                  [model.layers[3].output])
layer_output = get_3rd_layer_output([x])[0]

```