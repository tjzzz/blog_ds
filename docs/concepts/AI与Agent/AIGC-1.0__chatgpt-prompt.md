---
title: "chatgpt-prompt"
created: 2026-10-09
updated: 2026-10-09
tags: [llm-wiki, migrated]
source: ["Input/rebuild_source_2026-10-09/AI-Agent/AIGC-1.0/chatgpt-prompt.md"]
wiki_type: concepts
topic: "AI与Agent"
migrated_from: "AI-Agent/AIGC-1.0/chatgpt-prompt.md"
review_status: structural
---

> 所属 Topic：[AI与Agent](../../topics/AI%E4%B8%8EAgent.md) · 类型：概念

#prompt

https://learningprompt.wiki

prompt engineering 现在 AI 的发展还比较早期，了解和学习 PE 价值相对比较大，但长远来看可能会被淘汰。这个「长远」可能是 3 年，亦或者 1 年。


## 一些实践小技巧
一些小技巧：
- 如果你无法用文字准确解释问题或指示，你可以在 prompt 里增加一些案例。
比如给xx起名

```
Suggest three names for an animal that is a superhero.

Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: Horse
Names:
```

- 在prompt中在家一些role(角色)相关的内容
```
假设你是一个小学老师，很擅长xxxx，请帮我把如下的xxx
```


- 技巧5：使用 ”“” 符号将指令和需要处理的文本分开
```
Please summarize the following sentences to make them easier to understand.

Text: """
OpenAI is an American artificial intelligence (AI) research laboratory consisting of the non-profit OpenAI Incorporated (OpenAI Inc.) and its for-profit subsidiary corporation OpenAI Limited Partnership (OpenAI LP). OpenAI conducts AI research with the declared intention of promoting and developing a friendly AI. OpenAI systems run on the fifth most powerful supercomputer in the world.[5][6][7] The organization was founded in San Francisco in 2015 by Sam Altman, Reid Hoffman, Jessica Livingston, Elon Musk, Ilya Sutskever, Peter Thiel and others,[8][1][9] who collectively pledged US$1 billion. Musk resigned from the board in 2018 but remained a donor. Microsoft provided OpenAI LP with a $1 billion investment in 2019 and a second multi-year investment in January 2023, reported to be $10 billion.[10]
"""
```


- 信息提取的时候可以指定输出的格式

```
Extract the important entities mentioned in the article below. First extract all company names, then extract all people names, then extract specific topics which fit the content and finally extract general overarching themes  
Desired format:  
Company names: <comma_separated_list_of_company_names>  
People names: -||-  
Specific topics: -||-  
General themes: -||-
```



## prompt框架


### 基础框架

查阅了非常多关于 ChatGPT prompt 的框架资料，我目前觉得写得最清晰的是 Elavis Saravia [总结](https://github.com/dair-ai/Prompt-Engineering-Guide/blob/main/guides/prompts-intro.md)的框架，他认为一个 prompt 里需包含以下几个元素：

-   **Instruction（必须）：** 指令，即你希望模型执行的具体任务。
-   **Context（选填）：** 背景信息，或者说是上下文信息，这可以引导模型做出更好的反应。
-   **Input Data（选填）：** 输入数据，告知模型需要处理的数据。
-   **Output Indicator（选填）：** 输出指示器，告知模型我们要输出的类型或格式。

### CRISPE Prompt Framework

另一个我觉得很不错的 Framework 是 [Matt Nigh](https://github.com/mattnigh/ChatGPT3-Free-Prompt-List) 的 CRISPE Framework，这个 framework 更加复杂，但完备性会比较高，比较适合用于编写 prompt 模板。CRISPE 分别代表以下含义：

-   **CR：** Capacity and Role（能力与角色）。你希望 ChatGPT 扮演怎样的角色。
-   **I：** Insight（洞察力），背景信息和上下文（坦率说来我觉得用 Context 更好）。
-   **S：** Statement（指令），你希望 ChatGPT 做什么。
-   **P：** Personality（个性），你希望 ChatGPT 以什么风格或方式回答你。
-   **E：** Experiment（尝试），要求 ChatGPT 为你提供多个答案。



技巧7 zero-shot chain of thought
这个技巧使用起来非常简单，只需要在问题的结尾里放一句 `Let‘s think step by step` （让我们一步步地思考），模型输出的答案会更加准确。




## 实践案例

https://learningprompt.wiki/docs/chatGPT/tutorial-extras/搭建基于知识库内容的机器人