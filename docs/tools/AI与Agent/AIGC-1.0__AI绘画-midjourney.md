---
title: "AI绘画-midjourney"
created: 2026-10-09
updated: 2026-10-09
tags: [llm-wiki, migrated]
source: ["Input/rebuild_source_2026-10-09/AI-Agent/AIGC-1.0/AI绘画-midjourney.md"]
wiki_type: tools
topic: "AI与Agent"
migrated_from: "AI-Agent/AIGC-1.0/AI绘画-midjourney.md"
review_status: structural
---

> 所属 Topic：[AI与Agent](../../topics/AI%E4%B8%8EAgent.md) · 类型：工具

Midjourney完全运行在云端，没有专用客户端，用户需要通过Discord平台与Midjourney机器人进行交互。

## 1. 注册
官网 https://www.midjourney.com/home
首先注册midjourney账号，Midjourney并没有开发自己专属的客户端，而是将自己的主要功能完全放在了Discord平台上。因此，要使用Midjourney，还需要注册一个Discord账号。

Discord是由美国Discord公司开发的一款专为社群设计的免费网络实时通话软件与数字发行平台，类似于QQ群

https://discord.com/channels/@me


进入Discord的Midjourney服务器，可以看到它和其他聊天软件的界面很类似。可以在底部的聊天输入框中输入任意内容，并按Enter键发送，向频道或者聊天对象发送消息。更重要的是，可以在聊天输入框中发送命令，Midjourney机器人收到命令后会执行对应的操作

可以在Discord的Midjourney服务器上的公共频道中发送命令，Midjourney机器人会响应发送的命令。不过由于公共频道中通常有很多用户，发送的命令可能会很快被其他人的消息淹没，虽然机器人回应时会有提示，但有时仍需要在很多聊天记录中上下翻找，较为麻烦，因此，一般建议在正式绘画时和Midjourney机器人私聊。

图片版权问题：
免费用户生成的图片不属于自己，使用时要注明来源（来自Midjourney），且不可商用；付费用户（包括基础版、标准版、专业版用户）生成的图片属于自己，可用作任何用途，包括商用。

## 2.基本使用

/imagine 提示图片(可选) 提示文本  参数

提示词＝主体元素＋形容词＋风格词＋参数

| 功能                                     | 用法                         |     |
| -------------------------------------- | -------------------------- | --- |
| 图片纵横比                                  | --aspect 5:4   或者 --ar 5:4 |     |
| 混乱度(0-100), 默认是0                       | --chaos 1  或者 -c           |     |
| 排除指定物品不出现                              | --no <某物>                  |     |
| 图片细节度。 取值范围0.25，0.5，1默认1               | --quality   or --q         |     |
| seed种子值                                | --seed 数值                  |     |
| stop停止渲染 渲染过程生成步数为100，停止时间\br 越早，图像越模糊 |                            |     |
| 风格化 （1-1000），默认100                     | --stylize <数值>             |     |
| 图像融合                                   | /blend url1 url2 url3      |     |
| 重复                                     | --repeat 次数                |     |

提示图 /imagine  url1 url2   可以是网络可以访问的图片链接，也可以从本地上传。
> note: 与机器人私聊上传的图片，只要知道链接任何人都能访问，注意隐私



## 3案例
插图：

科技风格：user being inspired by the possibilities of an app, flat illustration for a tech company,by slack and dropbox, style of behance 

水彩画：Watercolor roses with long handle, bright colors, clipart, white background, isolated elements --ar 2:3--v 5.1
![](../../media/recovered/dc4cc0f6cebb-Pasted%20image%2020240609213420.png)

日本知名动画制作公司吉卜力工作室(Studio Ghibli)的作品有很大一部分使用了水彩风格，且具有非常鲜明的特色，这种风格被称为吉卜力风格，亦称宫崎骏风格。这种风格以鲜艳的色彩、精致的细节、温馨的画面以及梦幻般的氛围为特点，通常运用渐变色与柔和的笔触，营造出柔美且富有魔力的氛围。在Midjourney中可以使用关键词Studio Ghibli在绘画中使用这种风格。

提示词：Light watercolor, outside of a jazzy coffeeshop, bright, white background, few details, dreamy, Studio Ghibli --v 5





## 参考
《商用级AIGC绘画创作与技巧(Midjourney+Stable Diffusion)》