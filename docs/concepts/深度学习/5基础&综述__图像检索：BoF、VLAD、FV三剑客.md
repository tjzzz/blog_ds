---
title: "图像检索：BoF、VLAD、FV三剑客"
created: 2026-10-09
updated: 2026-10-09
tags: [llm-wiki, migrated]
source: ["Input/rebuild_source_2026-10-09/05_深度学习/5基础&综述/图像检索：BoF、VLAD、FV三剑客.md"]
wiki_type: concepts
topic: "深度学习"
migrated_from: "05_深度学习/5基础&综述/图像检索：BoF、VLAD、FV三剑客.md"
review_status: structural
---

> 所属 Topic：[深度学习](../../topics/%E6%B7%B1%E5%BA%A6%E5%AD%A6%E4%B9%A0.md) · 类型：概念

# 图像检索：BoF、VLAD、FV三剑客


## BoF(bag of features)
其实就是BOW(bag of words)在图像领域的应用。
* step1: 视觉单次提取，提取所有图片的图片特征
* step2：构建视觉词典。对图片特征进行聚类，假设聚成k个类，这k个类的类中心就相当于k个基本词汇
* step3: 图像表示。统计每张图在每个聚类总的特征个数，这样每张图就可以用一个分布直方图表示，或者是一个k维向量表示。
* step4: 图像检索.


## VALAD
与Bof有一些类似，只是最后图像表示的时候，不是用的特征个数。而是用的x与其类中心的累积残差。