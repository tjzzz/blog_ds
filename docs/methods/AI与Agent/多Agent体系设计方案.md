---
tags:
  - openclaw
  - agent
  - workflow
  - memory
  - "#小红书素材"
created: 2026-05-09
title: "多Agent体系设计方案"
updated: 2026-10-09
source: ["Input/rebuild_source_2026-10-09/AI-Agent/多Agent体系设计方案.md"]
wiki_type: methods
topic: "AI与Agent"
migrated_from: "AI-Agent/多Agent体系设计方案.md"
review_status: structural
---

> 所属 Topic：[AI与Agent](../../topics/AI%E4%B8%8EAgent.md) · 类型：方法

# 多 Agent 体系设计方案

## 背景

每次新开 WorkBuddy 聊天窗口都需要重新交代背景，不同领域的问题混在一起没有上下文隔离。
需求：建立多 Agent 体系，每个 Agent 有独立的角色设定和记忆，互不干扰。

## 核心设计原则

| 原则 | 说明 |
|------|------|
| **Agent 维度隔离** | 记忆按 Agent 划分，不按 Workspace 划分 |
| **配置 + 记忆 + 工作空间** | 每个 Agent 目录下包含 agent/（配置）+ workspace/（项目+记忆） |
| **OpenClaw 格式** | 兼容 OpenClaw 平台，便于跨平台迁移 |
| **一句话切换** | 说「切换到 xxx」即可加载对应 Agent 的角色和记忆 |

## 目录结构

```
~/.workbuddy/agents/{agent-name}/
├── agent/
│   ├── SOUL.md           # Agent 身份定义（你是谁、性格、能力、行为准则）
│   ├── IDENTITY.md       # Agent 元数据（名称、emoji、标签、平台兼容）
│   └── USER.md           # 用户信息（该场景下你的身份、偏好、业务背景）
└── workspace/
    ├── memory.md          # 长期记忆（人工+AI 维护的精要信息，跨会话保持）
    └── memory/
        └── YYYY-MM-DD.md  # 每日会话记忆（AI 对话结束时自动追加）
```

### 记忆力隔离对比

| 维度 | 旧方式 | 新方式 |
|------|--------|--------|
| 记忆归属 | 按项目/workspace | 按 Agent |
| 切换开销 | 每次说明背景 | 一句话「切换到 xxx」 |
| 跨平台迁移 | WorkBuddy 限定 | OpenClaw 兼容 |
| 会话历史 | 分散在各 workspace | 集中到 Agent 目录 |

## 切换机制（agent-switch skill）

通过 WorkBuddy 的 Skill 系统实现：

```
你说 "切换到 trade-news"
      ↓
Skill 触发读取 ~/.workbuddy/agents/trade-news/
      ├── agent/SOUL.md       → 注入角色身份
      ├── agent/USER.md       → 注入用户背景
      ├── workspace/memory.md → 注入长期记忆
      └── workspace/memory/2026-05-09.md → 注入当日记忆
      ↓
输出：「已切换到 trade-news Agent」
```

Skill 文件位于：`~/.workbuddy/skills/agent-switch/SKILL.md`

### 记忆写入规则
- **每日记忆**：AI 对话结束时自动追加到 `workspace/memory/YYYY-MM-DD.md`
- **长期记忆**：重要决策/偏好同时写入 `workspace/memory.md`
- **30 天清理**：旧每日文件蒸馏后删除

## 已有 Agent

| Agent 名称     | 角色                | 状态    |
| ------------ | ----------------- | ----- |
| `zzzheng`    | 主 Agent（全能 AI 助手） | ✅ 已配置 |
| `data-agent` | 数据分析专家            | ✅ 已迁移 |


## 待办
- [ ] 创建交易分析类 Agent（trade-data, trade-macro, trade-news, trade-technical）
- [ ] 实际使用中验证 agent-switch 流程
- [ ] 将已有 workspace 迁移至对应 Agent 目录

---

*注：此方案遵循 OpenClaw 标准格式，同时兼容 WorkBuddy 平台。*
