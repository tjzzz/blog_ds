---
topic: AIGC
category: 应用
tag: 图片素材
title: "AIGC应用-图片素材"
created: 2026-10-09
updated: 2026-10-09
tags: [llm-wiki, migrated]
source: ["Input/rebuild_source_2026-10-09/AI-Agent/AIGC-1.0/AIGC应用-图片素材.md"]
wiki_type: concepts
migrated_from: "AI-Agent/AIGC-1.0/AIGC应用-图片素材.md"
review_status: structural
---

> 所属 Topic：[AI与Agent](../../topics/AI%E4%B8%8EAgent.md) · 类型：概念

#aigc应用 #ppt  #思维导图


## 图片素材

可以利用aigc来自动生成图片素材，同时也可以让他充当搜索引擎的角色帮我们找已有的素材。


注意：
由于使用Unsplash API生成图片的方式是**随机**获取相关图片，因此每次请求可能会得到不同的图片。如果看到不错的图，请务必记得及时保存。  
那ChatGPT是在Unsplash里搜索图片吗？不是，这里ChatGPT只是根据文本生成了对应的Unsplash图片链接，即chatgpt只是生成了对应的关键词，然后用markdown语法渲染出来图片效果。

详细的情况可以参考其官方API https://unsplash.com/documentation



prompt:
> 现在你是一个搜索引擎，寻找我告诉你的图片，找到以后用Markdown语言生成，不要用反引号，不要用代码框，你需要用Unsplash API，遵循以下的格式: ![](https://source.unsplash.com/1600x900/?< PUT YOUR QUERY HERE >)，并且帮图片的原始链接也附上






<hr class="__chatgpt_plugin">

role::assistant

![](https://source.unsplash.com/1600x900/?sea)

<hr class="__chatgpt_plugin">

role::user

现在你是一个搜索引擎，寻找我告诉你的图片，找到以后用Markdown语言生成，不要用反引号，不要用代码框，你需要用Unsplash API，遵循以下的格式: ![](https://source.unsplash.com/1600x900/?< PUT YOUR QUERY HERE >)

<hr class="__chatgpt_plugin">

role::assistant

好的，请稍等，我来为您找一张sea的图片。

![](https://source.unsplash.com/1600x900/?sea)

<hr class="__chatgpt_plugin">

role::user

帮我找一张cat在吃东西的图片

<hr class="__chatgpt_plugin">

role::assistant

很抱歉，我找不到符合条件的图片。

<hr class="__chatgpt_plugin">

role::user

找一张猫在吃东西的照片

<hr class="__chatgpt_plugin">

role::assistant

好的，请稍等，我来为您找一张猫在吃东西的照片。

![](https://source.unsplash.com/1600x900/?cat,eating)

<hr class="__chatgpt_plugin">

role::user
我需要做一个ppt，目前缺少一张背景图，请帮我找一个高端大气上档次的商务风格的背景图


<hr class="__chatgpt_plugin">

role::assistant

好的，请稍等，我来为您找一个高端大气上档次的商务风格的背景图。

![](https://source.unsplash.com/1600x900/?business,background)

<hr class="__chatgpt_plugin">

role::user

颜色稍微有点亮，找一个偏冷色系的图片

<hr class="__chatgpt_plugin">

role::assistant

好的，请稍等，我来为您找一个偏冷色系的商务风格背景图。

![](https://source.unsplash.com/1600x900/?business,background,cold)

<hr class="__chatgpt_plugin">

role::user


<iframe src="//player.bilibili.com/player.html?aid=528330606&bvid=BV1GM41137H3&cid=1119682532&page=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"> </iframe>