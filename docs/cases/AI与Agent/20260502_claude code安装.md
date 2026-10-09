---
title: "20260502_claude code安装"
created: 2026-10-09
updated: 2026-10-09
tags: [llm-wiki, migrated]
source: ["Input/rebuild_source_2026-10-09/Agent实战手记/20260502_claude code安装.md"]
wiki_type: cases
topic: "AI与Agent"
migrated_from: "Agent实战手记/20260502_claude code安装.md"
review_status: structural
---

> 所属 Topic：[AI与Agent](../../topics/AI%E4%B8%8EAgent.md) · 类型：案例

## 标题


如何才能

## mac上安装claude code

```

brew install --cask claude-code
## 如果没有homebrew，/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```



linux 上

```
npm install -g @anthropic-ai/claude-code

```

这个时候因为没法使用cluade，所以连接会有问题，不着急，可以配置的

![](../../media/recovered/8bae79ff84ea-Pasted%20image%2020260502213546.png)



## 接入模型


根据自己的模型api的配置，比如我用的是百度的coding plan，一般官网都有介入教程：
https://cloud.baidu.com/doc/qianfan/s/0mn2mnemj




vim ~/.claude/settings.json 


### 接入飞书

`npx -y lark-channel-bridge@latest start`

### 桌面版
