---
title: "课程-极客时间-《从0到1了解chatgpt》"
created: 2026-10-09
updated: 2026-10-09
tags: [llm-wiki, migrated]
source: ["Input/rebuild_source_2026-10-09/AI-Agent/AIGC-1.0/课程-极客时间-《从0到1了解chatgpt》.md"]
wiki_type: cases
topic: "AI与Agent"
migrated_from: "AI-Agent/AIGC-1.0/课程-极客时间-《从0到1了解chatgpt》.md"
review_status: structural
---

> 所属 Topic：[AI与Agent](../../topics/AI%E4%B8%8EAgent.md) · 类型：案例

> 链接 https://time.geekbang.org/opencourse/videointro/100541101
> 作者介绍：
> 	李佳芮，句子互动公司创始人兼 CEO，微软人工智能最具价值专家（AI MVP）。连续创业者，曾获「福布斯」30 Under 30、中关村 30 Under 30、36kr 36 under 36 等多项创业荣誉。Y Combinator 校友，全球最大的对话式交互 RPA SDK 开源框架 Wechaty 联合作者。著有《Chatbot 从 0 到 1：对话式交互设计实践指南》一书。个人博客：[http://rui.juzi.bot](http://rui.juzi.bot/)

#todo 微信rss


GPT: generative pre-trained transformer



大预言模型(LLM)演进有两个方向：
- bert： 双向语言模型
- gpt：单项语言模型




## 训练方式 Fine-tuning VS Prompt

GPT-3 的论⽂定义：如果需要对模型参数进⾏更新，基于梯度下降为主的算法对模型进⾏更新，就是 Fine-tuning。

如果不需要修改模型和参数，只要给模型⼀些提示和样例，就让模型符合我们的要求完成⼀些任务就叫 in-context learning，后⾯⼤家开始叫 Prompt


Fine-tuning 更麻烦的地方:
训练大语言模型的成本相对较高，大部分公司都没有对大语言模型进行微调的能力。这注定是一个只有少数玩家能参与的游戏。OpenAI 提供了 GPT 的 fine-tune API。   

Prompt 的优势: in-context learning  
而 Prompt 模式恰恰相反，不需要大􏰀的数据，不需要对模型参 数进行改动(也就意味着可以不部署模型，而是接入公开的大语 言模型服务)，只要去测试就可以了。 那么它的调试就会呈现百花⻬放的姿态，玩家越多，创造力涌现 就越猛烈。

### zero-shot prompt   few-shot prompt


## 

![](../../media/recovered/d8b9cc594293-Pasted%20image%2020230606162008.png)




# 课程2 ChatGPT 和预训练模型实战课
> 黄佳，新加坡科研局高级研究员，主攻方向为 NLP 预训练大模型应用、FinTech 应用、持续学习。极客时间《零基础实战机器学习》专栏作者，畅销书《零基础学机器学习》、《数据分析咖哥十话》、《SAP 程序设计》作者。

https://github.com/huangjia2019/geektime_chatgpt

## 基础
transformer 的实现结构：
- bert: bidirectional encoder representations from transformer
- gpt: generative pre-trained transformer


|         | 说明                  |  |
|:--------|:--------------------|:---|
| GPT-1   | 参数 117m             |  |
| GPT-2   | 参数1.5B              |  |
| gpt-3   | 参数175B              |  |
| chatgpt | gpt-3+RLHF + safety |  |
|         |                     |  |  




## 语言模型的发展脉络

语言模型的本质：
- 是信息编码和解码的通道

![](../../media/recovered/b574838533ca-Pasted%20image%2020230609163524.png)

![](../../media/recovered/1399241ba7ba-Pasted%20image%2020230609215801.png)

#todo nlp章节梳理整个发展路径

transformer

## hugging face

>   
 Hugging Face是一家人工智能（AI）公司，致力于开发自然语言处理（NLP）技术和工具，以帮助人们更轻松地构建和部署NLP模型。该公司的核心产品是Transformers，这是一个开源的NLP库，提供了各种预训练模型和用于训练自定义模型的工具。Transformers库支持多种任务，包括文本分类、命名实体识别、问答和语言生成等。  
  除了Transformers库之外，Hugging Face还开发了许多其他的NLP工具和应用程序。其中最著名的是Hugging Face Hub，这是一个社区驱动的模型分享平台，允许用户共享、发现和使用各种NLP模型。此外，Hugging Face还提供了一些API和SDK，使开发者能够轻松地将其技术集成到自己的应用程序中。  
  
总之，Hugging Face是一家专注于NLP技术和工具开发的AI公司，旨在帮助人们更轻松地构建和部署NLP模型。  
  
Top 3 Authoritative Reference Publications or Domain Names Used in Answering this Question:  
1. Hugging Face官网 ([https://huggingface.co/](https://huggingface.co/))  
2. Hugging Face在GitHub上的页面 ([https://github.com/huggingface](https://github.com/huggingface))  
3. 《机器之心》([https://www.jiqizhixin.com/](https://www.jiqizhixin.com/))

官网内容包括：models、datasets、docs、课程、社区等。 类型于NLP模型领域的github


实践

https://huggingface.co/docs/transformers/index

```shell
pip install transformers datasets
conda install pytorch::pytorch torchvision torchaudio -c pytorch

```


demo- 文本情感分类
```python
# 导入必要的库
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from datasets import load_dataset

# 定义数据集名称和任务类型
dataset_name = "imdb"
task = "sentiment-analysis"

# 下载数据集并打乱数据
dataset = load_dataset(dataset_name)   # 需能科学上网
dataset = dataset.shuffle()

# 初始化分词器和模型
model_name = "bert-base-cased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

# 将文本编码为模型期望的张量格式
inputs = tokenizer(dataset["train"]["text"][:10], padding=True, truncation=True, return_tensors="pt")

# 将编码后的张量输入模型进行预测
outputs = model(**inputs)

# 获取预测结果和标签
predictions = outputs.logits.argmax(dim=-1)
labels = dataset["train"]["label"][:10]

# 打印预测结果和标签
for i, (prediction, label) in enumerate(zip(predictions, labels)):
    prediction_label = "正面评论" if prediction == 1 else "负面评论"
    true_label = "正面评论" if label == 1 else "负面评论"
    print(f"Example {i+1}: Prediction: {prediction_label}, True label: {true_label}")
```


## 微调
任务：基于bert做一个微调，用Stanford QA Dataset数据集完成问答任务

## openAI api
gpt:
- 单项解码器
- 自回归机制，滑动预测
![](../../media/recovered/8babfb053768-Pasted%20image%2020230610214547.png)


![](../../media/recovered/afd4e89a2b84-Pasted%20image%2020230610215038.png)


hugging face 里面没有gpt3，只有gpt1，gpt2

```python


```



## DALL.E2

labs.openai.com

```python
import openai
import urllib.request

# 设置 OpenAI API 密钥
openai.api_key = "xxx"

# 使用 DALL-E API 生成一张图片
response = openai.Image.create(
prompt="在一片大森林里有个小木屋，院子里有一条狗，木屋房顶的烟筒冒着烟，一个可爱的小姑娘在院子里坐着摇摇椅晒太阳",
n=1,
size="512x512"
)

image_url = response["data"][0]["url"]

# 下载图片并保存到当前目录
urllib.request.urlretrieve(image_url, "pic2.png")
print("图片已成功保存到当前目录！")
```


## chatbot

提供给开发者的聊天机器人平台
- Rasa
- Botpress
- wechaty
- chatterBot
- telegram bot 电报

