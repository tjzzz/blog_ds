---
title: "20260509_workbuddy的专家设置"
created: 2026-10-09
updated: 2026-10-09
tags: [llm-wiki, migrated]
source: ["Input/rebuild_source_2026-10-09/Agent实战手记/20260509_workbuddy的专家设置.md"]
wiki_type: cases
topic: "AI与Agent"
migrated_from: "Agent实战手记/20260509_workbuddy的专家设置.md"
review_status: structural
---

> 所属 Topic：[AI与Agent](../../topics/AI%E4%B8%8EAgent.md) · 类型：案例

#小红书素材 


## WorkBuddy 专家/Agent 机制概览

### 一、已有专家体系

WorkBuddy 官方提供的专家能力分两类：

|类型|说明|适用场景|
|---|---|---|
|**专家（单Agent）**|独立人设、方法论、工具链，单线处理|单领域明确任务|
|**专家团（多Agent团队）**|团长拆解+多团员并行协作|跨领域复杂链路任务|

但 **自定义创建专家目前没有UI入口**，是通过文件系统层面的配置来实现的。




## 结构目录

可以自己修改或者配置