---
title: "skills"
created: 2026-10-09
updated: 2026-10-09
tags: [llm-wiki, migrated]
source: ["Input/rebuild_source_2026-10-09/AI-Agent/skills.md"]
wiki_type: concepts
topic: "AI与Agent"
migrated_from: "AI-Agent/skills.md"
review_status: structural
---

> 所属 Topic：[AI与Agent](../../topics/AI%E4%B8%8EAgent.md) · 类型：概念

skills市场
- clawhub： https://clawhub.ai/skills?sort=downloads&nonSuspicious=true
- https://skills.sh/


中文加速
```
clawhub config set registry https://cn.clawhub-mirror.com
```


## 搜索





## 金融

期货相关skills

[FineClaw](https://github.com/aifinlab/FinClaw/blob/main/README.md)


|  序号 | Skill 名称          | 主要功能                 | 点位预测能力                                                               | 数据来源/交易所     | 安装命令                                                            |
| :-: | ----------------- | -------------------- | -------------------------------------------------------------------- | ------------ | --------------------------------------------------------------- |
|  1  | **hyperclaw**     | Hyperliquid DEX 综合工具 | • 计算 SMA 移动平均线<br>• 识别支撑/阻力位<br>• 订单簿深度分析<br>• 多维度市场分析               | Hyperliquid  | 内置或通过 API 配置                                                    |
|  2  | **chart-image**   | K 线可视化与图表生成          | • 生成蜡烛图<br>• 标记支撑/阻力点位<br>• 可视化趋势线<br>• 出版级图表质量                      | 通用（可接入任意数据源） | `npx playbooks add skill openclaw/skills --skill chart-image`   |
|  3  | **Bybit Futures** | Bybit 永续合约交易         | • RSI 超买超卖识别<br>• EMA 交叉信号<br>• 布林带波动率通道<br>• 预设策略模板                 | Bybit        | `npx playbooks add skill openclaw/skills --skill bybit-futures` |
|  4  | **Binance Pro**   | 币安现货+期货交易            | • 125x 杠杆支持<br>• 技术指标计算（RSI/MACD/EMA/布林带）<br>• 持仓 PnL 统计<br>• 止损止盈设置 | Binance      | `npx playbooks add skill openclaw/skills --skill binance-pro`   |

|  序号 | Skill 名称           | 主要功能      | 点位预测能力                                                   | 数据源       | 安装命令                                                             |
| :-: | ------------------ | --------- | -------------------------------------------------------- | --------- | ---------------------------------------------------------------- |
|  5  | **finance-data**   | 金融数据获取与分析 | • 期货/外汇 K 线数据<br>• 帝纳波利点位计算<br>• 自定义时间框架分析<br>• 多市场数据聚合  | 期货、外汇等多市场 | `npx playbooks add skill openclaw/skills --skill finance-data`   |
|  6  | **trend-analysis** | 趋势分析      | • 多时间框架趋势识别<br>• 趋势延续/反转预测<br>• 关键点位标记                   | 通用        | `npx playbooks add skill openclaw/skills --skill trend-analysis` |
|  7  | **backtest-tool**  | 策略回测工具    | • 历史 K 线数据回测<br>• 支撑/阻力策略验证<br>• 形态识别准确率统计<br>• 优化入场出场点位 | 历史数据      | `npx playbooks add skill openclaw/skills --skill backtest-tool`  |
