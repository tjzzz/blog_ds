---
title: "Openclaw"
created: 2026-10-09
updated: 2026-10-09
tags: [llm-wiki, migrated]
source: ["Input/rebuild_source_2026-10-09/AI-Agent/Openclaw.md"]
wiki_type: tools
topic: "AI与Agent"
migrated_from: "AI-Agent/Openclaw.md"
review_status: structural
---

> 所属 Topic：[AI与Agent](../../topics/AI%E4%B8%8EAgent.md) · 类型：工具

## 基础概念

### 分层架构

根据你提供的截图，OpenClaw 采用分层架构设计，以下是核心目录和文件的详细说明：

#### 核心配置目录

| 路径 | 作用 |
| ------------------------------ | -------------------- |
| `.openclaw/` | 系统主配置目录，包含所有运行时配置和数据 |
| `.openclaw/openclaw.json` | 主配置文件，定义系统核心参数、连接信息等 |
| `.openclaw/openclaw.json.bak*` | 配置备份文件，支持版本回滚 |

#### 功能模块目录

| 路径 | 作用 |
|---|---|
| `completions/` | 任务完成记录和输出缓存 |
| `credentials/` | 凭证管理，存储各类API密钥、认证信息 |
| `cron/` | 定时任务配置，支持周期性作业调度 |
| `delivery-queue/` | 任务交付队列，管理异步任务分发 |
| `devices/` | 设备管理，处理多设备接入和协同 |
| `extensions/` | 扩展插件目录，支持自定义功能扩展 |
| `feishu/` | 飞书集成模块，处理企业级协作 |
| `identity/` | 身份认证中心，管理用户和权限 |
| `logs/` | 日志记录，系统运行轨迹追踪 |
| `media/` | 媒体资源存储，图片、音频、视频等 |
| `memory/` | 记忆存储，长期知识库和上下文缓存 |
| `workspace/` | 工作空间，包含核心文档和脚本 |

#### 工作空间关键文件

| 文件 | 作用 |  |
| ------------- | -------------------------------------------------- | --- |
| `AGENTS.md` | Agent 定义文档，描述各类智能代理配置 |  |
| `SOUL.md` | 系统灵魂文件，定义核心价值和行为准则 |  |
| `TOOLS.md` | 工具注册表，声明可用工具及其使用方式 |  |
| `IDENTITY.md` | 身份定义，系统角色和权限边界 |  |
| `USER.md` | 用户画像和个性化配置 |  |
| `MEMORY.md` | 记忆策略，定义知识存储和检索机制。长期记忆摘要：重要对话、知识的归档（Agent 每次会话都会读取） |  |

![](../../media/recovered/5af4a96760cd-openclaw_architecture%201.png)

### Session 持续时间

- **会话超时机制**：
  - 默认：2-4 小时无活动自动断开
  - 可配置：通过 `openclaw.json` 中的 `session.timeout` 参数调整
- **记忆保持周期**：
  - 短期记忆（Session Memory）：会话期间有效
  - 长期记忆：持久化存储到 `memory/` 目录
- **心跳检测**：`workspace/HEARTBEAT.md` 记录会话活跃状态
- **交互频率**：用户定期互动会延长 Session 生命周期
- **任务完成度**：任务完成后自动标记 Session 为完成状态

### 渠道 + 使用者消息是否共享

🔧 dmScope 的 4 种模式

- **模式一：main** — 所有私信共享同一个会话，适用于单人使用，追求连续性。
- **模式二：per-peer** — 按发送者隔离（跨渠道共享），适用于同一个人在不同渠道发消息共享会话。
- **模式三：per-channel-peer** — 按渠道 + 发送者隔离，适用于多人使用，推荐。
- **模式四：per-account-channel-peer** — 按账号 + 渠道 + 发送者隔离，适用于多账号收件箱场景。

⚙️ 如何配置？在 `~/.openclaw/openclaw.json` 中设置：
```json
{
  "session": {
    "dmScope": "per-channel-peer"
  }
}
```
修改后重启 Gateway：`openclaw gateway restart`

---

## 入门资源

- 官方文档：https://docs.openclaw.ai/zh-CN
- 教程：https://openclaw101.dev/zh/day/1
- 视频教程：https://www.youtube.com/watch?v=2ZZCyHzo9as
- DataWhale 教程：https://datawhalechina.github.io/hello-claw/cn/adopt/chapter1/

---

## 常用平台对比

| 平台/方案 | 入门成本 | 模型费用 | 技术门槛 | 适用人群 |
| ------------------- | ---------- | ---------------------- | ------------- | ---------- |
| **阿里云** | 17.8元/月起 | 7.9-39.9元/月 | 低（一键镜像） | 个人开发者、中小企业 |
| **智谱 AutoClaw** | **免费** | **免费**（内置模型） | **极低**（客户端安装） | **普通用户首选** |
| **Kimi Claw** | 199元/月 | 含在套餐内 | 低 | Kimi 重度用户 |
| **MiniMax MaxClaw** | 订阅会员价 39? | 含在套餐内 | 低 | 需要多端协同用户 |
| **本地部署** | 0元（自有电脑） | 按 Token 计费（10-100元+/月） | **高**（需技术背景） | 极客、隐私敏感用户 |
| **第三方代装** | 300-800元/次 | 另计 | 无（付费服务） | 不愿折腾的用户 |

---

## 各大平台详情

### 智谱 AutoClaw

- 官网：https://autoglm.zhipuai.cn/autoclaw/
- Coding Plan：https://www.bigmodel.cn/glm-coding?ic=8M39XSNNIK&closedialog=true

### Kimi Claw

- Kimi 平台定价：https://platform.kimi.com/docs/pricing/chat-k26

### 微信 QClaw

- 官网：https://claw.guanjia.qq.com/

### Coze

- 每月 49 元
- 订阅页：https://code.coze.cn/subscription-paywall

### 字节跳动（飞书 / 扣子 / 秒答）

- 飞书 Claw：https://openclaw.feishu.cn/home
- 扣子 Agent
- 秒答

### AliClaw（阿里云）

- 活动页：https://www.aliyun.com/activity/ecs/clawdbot?userCode=t1dwdo7u
- 机器环境：https://swasnext.console.aliyun.com/servers/cn-shanghai
- Coding Plan 用量：https://bailian.console.aliyun.com/cn-beijing/?tab=coding-plan#/efm/detail
- WebUI 界面：
  ![](../../media/recovered/f67225ffa603-Pasted%20image%2020260312095045%201.png)
- 机器账号：root / Zzz.

### DuClaw（百度）

- Coding Plan：https://console.bce.baidu.com/qianfan/resource/subscribe
- 服务器：https://console.bce.baidu.com/ls/#/ls/instance/list
- DuClaw 控制台：https://console.bce.baidu.com/duclaw/#/duclaw
  ![](../../media/recovered/69259dacd0e2-Pasted%20image%2020260312095234%201.png)

#### DuClaw 的 Skills

直接对接百度搜索、学术、网盘。文件内容可以直接同步到网盘。

### 微信 Workbuddy

（暂无详细内容）

-> 查看 API 密钥和配置：`Agent工作流/agent/Openclaw-API配置`（库外参考）

---

## Coding Plan & AIP 收费

- DeepSeek 定价：https://api-docs.deepseek.com/zh-cn/quick_start/pricing/
- Kimi 平台定价：https://platform.kimi.com/docs/pricing/chat-k26

---

## 集成指南

### OpenClaw 接入飞书教程

```
### 第一步：在飞书开放平台创建应用

1. **访问飞书开放平台**
    - 打开 https://open.feishu.cn/
    - 使用飞书账号登录
2. **创建企业自建应用**
    - 进入「开发者后台」→「创建企业自建应用」
    - 填写应用名称（如：OpenClaw AI 助手）
    - 上传应用图标
3. **获取凭证信息**
    - 在应用详情页，找到「凭证与基础信息」
    - 记录以下信息：
        - **App ID**（应用ID）
        - **App Secret**（应用密钥）

### 第二步：配置应用权限

在飞书开放平台配置以下权限：

| 权限名称 | 权限标识 | 用途 |
| ------- | -------------------------- | -------- |
| 获取与发送消息 | im:message | 收发消息 |
| 获取用户信息 | contact:user.base:readonly | 获取用户基本信息 |
| 接收消息 | im:message:receive_as_bot | 接收用户消息 |

### 第三步：配置事件订阅

1. 在应用后台找到「事件订阅」
2. 配置请求网址（Webhook URL）
3. 开启以下事件：
    - `im.message.receive_v1`（接收消息）

### 第四步：在 OpenClaw 中添加飞书渠道

终端

Test feishu channel add

终端

Check feishu capabilities

终端

Search for more specific Feishu config

根据详细的教程资料，我来为您提供完整的飞书接入指南：
```


