---
title: "course_deeplearningAI"
created: 2026-10-09
updated: 2026-10-09
tags: [llm-wiki, migrated]
source: ["Input/rebuild_source_2026-10-09/AI-Agent/AIGC-1.0/course_deeplearningAI.md"]
wiki_type: concepts
topic: "AI与Agent"
migrated_from: "AI-Agent/AIGC-1.0/course_deeplearningAI.md"
review_status: structural
---

> 所属 Topic：[AI与Agent](../../topics/AI%E4%B8%8EAgent.md) · 类型：概念

> https://www.deeplearning.ai/short-courses/
> 目前的这个还没字幕，可以同步看b站的翻译 https://www.bilibili.com/video/BV16u411p7KQ/?spm_id_from=333.337.search-card.all.click&vd_source=3a5163a381447858570b69e534a7abb8




https://learn.deeplearning.ai/chatgpt-building-system/lesson/1/introduction


```python
import os
import openai
import tiktoken

openai.api_key  = 'xxxx'

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]
    #return response
```