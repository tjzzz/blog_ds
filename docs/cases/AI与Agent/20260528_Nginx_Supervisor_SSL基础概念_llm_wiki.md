---
title: "Nginx / Supervisor / SSL 基础概念 - LLM Wiki风格"
date: 2026-05-28
tags:
  - nginx
  - supervisor
  - ssl
  - https
  - 部署
  - 运维
  - llm-wiki
  - 新手友好
description: "面向初学者的 Nginx、Supervisor、SSL 基础概念解释，包含三者在生产部署中的角色定位、工作原理和相互关系。配合 FastAPI 商业项目阿里云部署方案使用。"
created: 2026-10-09
updated: 2026-10-09
source: ["Input/rebuild_source_2026-10-09/Agent实战手记/20260528_Nginx_Supervisor_SSL基础概念_llm_wiki.md"]
wiki_type: cases
topic: "AI与Agent"
migrated_from: "Agent实战手记/20260528_Nginx_Supervisor_SSL基础概念_llm_wiki.md"
review_status: structural
---

> 所属 Topic：[AI与Agent](../../topics/AI%E4%B8%8EAgent.md) · 类型：案例

## Mental Model

把你部署到服务器上的 Web 应用想象成**一家餐馆**：

```
┌──────────────┐     ┌─────────────┐     ┌────────────┐
│   SSL/HTTPS  │  =  │   防盗门     │  =  │ 客人信息不 │
│              │     │             │     │ 会被偷听   │
└──────────────┘     └─────────────┘     └────────────┘
┌──────────────┐     ┌─────────────┐     ┌────────────┐
│    Nginx     │  =  │  前台服务员   │  =  │ 接待客人、 │
│              │     │             │     │ 传菜、上菜 │
└──────────────┘     └─────────────┘     └────────────┘
┌──────────────┐     ┌─────────────┐     ┌────────────┐
│  Supervisor  │  =  │    保姆      │  =  │ 厨师倒了？ │
│              │     │             │     │ 立刻扶起来 │
└──────────────┘     └─────────────┘     └────────────┘
```

> **一句话**：Supervisor 保命，Nginx 分流，SSL 加密。三者配你的 FastAPI 代码 = 完整生产环境。

---

## 📊 三件套对比

| 维度 | SSL / HTTPS | Nginx | Supervisor |
|------|------------|-------|-----------|
| **角色** | 加密传输 | 反向代理 + 静态文件 | 进程守护 |
| **比喻** | 防盗门 | 前台服务员 | 保姆 |
| **面向谁** | 用户浏览器 ↔ 服务器 | 用户请求 → 后端 | 你的应用进程 |
| **解决什么** | 防止中间人窃听/篡改 | 端口转发、SSL 终结、负载均衡 | 崩溃自动重启、开机自启 |
| **费用** | ¥0（Let's Encrypt） | ¥0（开源） | ¥0（开源） |
| **配置频率** | 3 月自动续期 | 一次配好，基本不动 | 一次配好，基本不动 |
| **替代品** | 付费证书 | Caddy, HAProxy, Traefik | systemd, pm2, docker restart |
| **能不能不用？** | ❌ 支付/登录必须 | ⚠️ 可以但强烈不建议 | ⚠️ 可以但半夜挂了没人管 |

---

## 🎯 我需要装哪个？

| 你的情况 | SSL | Nginx | Supervisor |
|----------|:---:|:-----:|:----------:|
| 有域名，需要 HTTPS | ✅ | ✅ | — |
| 用户要输入密码/支付 | ✅ | ✅ | — |
| 只想 IP:端口跑着玩玩 | — | — | — |
| 怕应用挂了没人知道 | — | — | ✅ |
| 服务器重启后不想手动启动 | — | — | ✅ |
| 静态文件多，想减轻后端压力 | — | ✅ | — |
| 未来可能多台服务器 | — | ✅ | — |
| 完全不想碰运维 | → 用 PaaS（Fly.io / Railway） |

---

## 一、SSL / HTTPS

### 本质

HTTP 是**明信片**（沿途每个路由器都能看），HTTPS 是**密封信封**（只有收件人能打开）。

SSL 证书 = 一把公钥，由 CA（证书机构）签名担保"这个公钥确实属于这个域名"。浏览器内置了信任的 CA 列表，验证通过就显示 🔒。

### 用户感知

```
🔒 https://你的域名.com    ← 有小锁
⚠️ http://你的域名.com     ← 浏览器标"不安全"
```

### 费用

| 来源 | 价格 | 适合 |
|------|------|------|
| **Let's Encrypt**（推荐） | ¥0 | 所有项目，certbot 自动续期 |
| 阿里云免费证书 | ¥0 | 国内 ECS 用户 |
| 付费企业证书 | ¥2000+/年 | 银行、政府等 EV 验证场景 |

> ⚠️ **微信支付 / 支付宝回调强制要求 HTTPS**，没证书支付走不通。

### 申请（一行搞定）

```bash
# 前提：域名已解析到服务器 IP
certbot --nginx -d your-domain.com
```

certbot 自动配 Nginx + 设置定时续期，之后就不用管了。

### TLS 握手（简化版）

浏览器和服务器在传输数据前，先握手协商加密密钥：

```
浏览器                                  服务器
  │                                       │
  │── ① ClientHello ───────────────────→ │   "我支持 TLS 1.3, 这些加密算法"
  │                                       │
  │←─ ② ServerHello + 证书 ──────────── │   "用这个算法, 这是我的证书(含公钥)"
  │                                       │
  │  ③ 浏览器验签：证书是可信 CA 发的？    │
  │     域名匹配？证书过期了吗？            │
  │                                       │
  │── ④ 用公钥加密 pre-master secret ──→ │   双方各自派生 session key
  │                                       │
  │←────── ⑤ 加密通信开始 ────────→      │   后续全部用 session key 对称加密
```

> TLS 1.3 只需要 1-RTT（一次往返），比旧版本快。Let's Encrypt 证书走的就是这个流程。

### 证书文件说明

certbot 申请后生成两个关键文件：

| 文件 | 内容 | 用途 |
|------|------|------|
| `fullchain.pem` | 你的证书 + 中间 CA 证书（链） | Nginx `ssl_certificate` |
| `privkey.pem` | 你的私钥 | Nginx `ssl_certificate_key`，**绝对不能泄露** |

> 证书链 = 站点证书 ← 中间 CA ← 根 CA（浏览器内置信任）。缺中间 CA 会导致部分设备（特别是 Android）报证书错误。所以用 `fullchain.pem` 而不是 `cert.pem`。

### HSTS：强制 HTTPS

加一行 header，告诉浏览器"以后访问这个域名，只用 HTTPS，别试 HTTP"：

```nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```

效果：第一次 HTTPS 访问后，浏览器 1 年内不会尝试 HTTP，杜绝 SSL stripping 攻击。

---

## 二、Nginx

### 本质

**反向代理服务器**。站在用户和你的应用之间，接收请求 → 决定发给谁 → 返回结果。

### 为什么不能直接把 FastAPI 暴露出去

| 直接暴露 (`uvicorn --host 0.0.0.0 --port 8000`) | 经过 Nginx |
|------------------------------------------------|-----------|
| 用户访问 `http://ip:8000`，难记 | 用户访问 `https://域名`，正常 |
| 无法配 HTTPS | Nginx 处理 SSL，后端不用管 |
| 端口可能被防火墙挡 | 走 80/443 标准端口 |
| 没有限流/缓存/压缩 | Nginx 自带这些能力 |

### Nginx 做的三件事

```
用户 → https://域名
         │
    ┌────▼─────────────────────┐
    │         Nginx            │
    │                          │
    │  ① SSL 终结（解密 HTTPS） │
    │  ② 反向代理（转发给后端） │
    │  ③ 静态文件（直接返回）   │
    └────────┬─────────────────┘
             │ http://127.0.0.1:8000
    ┌────────▼─────┐
    │   FastAPI    │
    └──────────────┘
```

### 最小配置

```nginx
# /etc/nginx/conf.d/fastapi.conf
server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate     /etc/nginx/ssl/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /var/www/myapp/static/;
    }
}
```

### 替代品速览

| 工具 | 定位 | 适合 |
|------|------|------|
| **Caddy** | 更简单的 Nginx | 自动 HTTPS，配置极简 |
| **HAProxy** | 专业负载均衡 | 高并发 TCP/HTTP 分发 |
| **Traefik** | 云原生反向代理 | Docker/K8s 自动服务发现 |

### Location 匹配优先级（经典坑）

Nginx 的 `location` 不是按书写顺序匹配，而是按**优先级**：

```
优先级 高 → 低
  ①  = /exact       精确匹配
  ②  ^~ /prefix      前缀匹配（匹配后不再检查正则）
  ③  ~  \.php$       区分大小写的正则
  ④  ~* \.jpg$       不区分大小写的正则
  ⑤  /prefix          普通前缀（最宽松）
  ⑥  /                兜底
```

**常见踩坑**：

```nginx
# ❌ 你以为静态文件走 /static/，实际可能被 ~ \.php$ 截胡
location ~ \.php$ { ... }
location /static/ { alias /var/www/static/; }   # 如果请求 /static/test.php，先命中上面的正则！

# ✅ 加 ^~ 禁止正则匹配
location ^~ /static/ { alias /var/www/static/; }
```

### WebSocket 代理

FastAPI 的 WebSocket 端点需要 Nginx 升级连接：

```nginx
location /ws {
    proxy_pass http://127.0.0.1:8000;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_read_timeout 86400s;   # WebSocket 长连接不能断
}
```

> 关键：`proxy_http_version 1.1` + `Upgrade` + `Connection "upgrade"` 三件套，缺一个 WebSocket 就连不上。

### Upstream 负载均衡

流量大了，启动多个 FastAPI 实例，Nginx 帮你在它们之间分配请求：

```nginx
upstream fastapi_cluster {
    # 默认轮询（round-robin）
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
    server 127.0.0.1:8003;

    # 其他策略：
    # least_conn;              # 最少连接
    # ip_hash;                 # 同 IP 固定到同一台（session 亲和）
    # server xxx:8001 weight=3;  # 加权（性能好的机器多分配）
}

server {
    location / {
        proxy_pass http://fastapi_cluster;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 常用安全头

```nginx
# 防点击劫持
add_header X-Frame-Options "SAMEORIGIN" always;

# 防 MIME 类型嗅探
add_header X-Content-Type-Options "nosniff" always;

# 启用浏览器 XSS 过滤器
add_header X-XSS-Protection "1; mode=block" always;

# HSTS（前面讲过）
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```

---

## 三、Supervisor

### 本质

**进程守护工具**。盯着你的应用进程，挂了就重启。

### 有 vs 没有

| 场景 | 没有 Supervisor | 有 Supervisor |
|------|----------------|---------------|
| 关 SSH 窗口 | ❌ 服务停 | ✅ 继续跑 |
| 代码报错崩溃 | ❌ 挂了没人管 | ✅ 秒级自动重启 |
| 服务器重启 | ❌ SSH 上去手动启动 | ✅ 开机自启 |
| 想看状态 | ❌ `ps aux \| grep` 猜 | ✅ `supervisorctl status` |

### 配置

```ini
; /etc/supervisord.d/fastapi.ini
[program:fastapi]
command=/var/www/myapp/venv/bin/gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 127.0.0.1:8000
directory=/var/www/myapp
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/fastapi.err.log
stdout_logfile=/var/log/fastapi.out.log
```

### 常用命令

```bash
supervisorctl status              # 查看所有进程
supervisorctl start fastapi       # 启动
supervisorctl stop fastapi        # 停止
supervisorctl restart fastapi     # 重启
supervisorctl tail fastapi        # 实时日志
```

> ⚠️ 别用 `screen`/`tmux` 跑生产服务——SSH 一断全完。也别手动 `python main.py &` 后台跑——崩了没人知道。

### systemd：Supervisor 的替代方案

现代 Linux 发行版自带 systemd，可以不装 Supervisor 直接用它管理服务。**推荐新项目优先考虑 systemd**，少一个依赖。

```ini
; /etc/systemd/system/fastapi.service
[Unit]
Description=FastAPI Application
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/myapp
ExecStart=/var/www/myapp/venv/bin/gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 127.0.0.1:8000
Restart=always
RestartSec=3
StandardOutput=append:/var/log/fastapi.out.log
StandardError=append:/var/log/fastapi.err.log

[Install]
WantedBy=multi-user.target
```

```bash
systemctl daemon-reload           # 重载配置
systemctl start fastapi           # 启动
systemctl enable fastapi          # 开机自启
systemctl status fastapi          # 查看状态
journalctl -u fastapi -f          # 实时日志
```

| 对比 | Supervisor | systemd |
|------|-----------|--------|
| 安装 | 需要 pip install | 系统自带 |
| 配置复杂度 | 简单 | 稍复杂（更多字段） |
| 日志 | `supervisorctl tail` | `journalctl -u` |
| Web 管理界面 | ✅ 内置 | ❌ 需额外工具 |
| 依赖管理（先启动数据库再启动应用） | ❌ 需配 priority | ✅ `After=` / `Requires=` |
| 推荐场景 | CentOS 7 老系统 | CentOS 8+ / Ubuntu 16+ |

---

## 🗺️ 完整请求链路

```
用户浏览器
   │  https://your-domain.com
   ▼
┌──────────────────────────┐
│    互联网（SSL 加密）      │
└──────────────────────────┘
   │  :443
   ▼
┌──────────────────────────┐
│  Nginx                   │
│  ├─ 解密 HTTPS           │
│  ├─ 静态文件？→ 直接返回  │
│  └─ API 请求？→ 转发     │
└──────────────────────────┘
   │  http://127.0.0.1:8000（内网）
   ▼
┌──────────────────────────┐
│  FastAPI（你的代码）      │
│  ├─ 业务逻辑             │
│  ├─ 数据库               │
│  └─ 支付接口             │
└──────────────────────────┘
   ▲
   │  盯着 👀
┌──────────────────────────┐
│  Supervisor              │
│  ├─ 活着？→ 不打扰       │
│  ├─ 挂了？→ 马上重启     │
│  └─ 重启后？→ 自动启动   │
└──────────────────────────┘
```

---

## 🚀 新服务器一键部署

```bash
# ---------- 1. 安装 ----------
yum install -y nginx certbot python3-certbot-nginx
pip3 install supervisor

# ---------- 2. Supervisor ----------
cat > /etc/supervisord.d/fastapi.ini << 'EOF'
[program:fastapi]
command=/var/www/myapp/venv/bin/gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 127.0.0.1:8000
directory=/var/www/myapp
autostart=true
autorestart=true
stderr_logfile=/var/log/fastapi.err.log
stdout_logfile=/var/log/fastapi.out.log
EOF

systemctl start supervisord
supervisorctl update
supervisorctl start fastapi

# ---------- 3. Nginx（先 HTTP，后升级 HTTPS）----------
cat > /etc/nginx/conf.d/fastapi.conf << 'EOF'
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

systemctl restart nginx

# ---------- 4. SSL 证书 ----------
# 确保域名已解析到服务器 IP
certbot --nginx -d your-domain.com

# ---------- 5. 验证 ----------
curl http://127.0.0.1:8000/health     # FastAPI 活着？
supervisorctl status                    # Supervisor 在盯？
curl https://your-domain.com/health     # Nginx + SSL 通了？
```

> 配好后日常只需要 `supervisorctl status` 看一眼 + 偶尔 `supervisorctl tail fastapi` 翻翻日志。三件套基本零维护。

---

## 🔥 排错速查

### 502 Bad Gateway

**含义**：Nginx 收到了请求，但转发给后端时，后端没响应（进程死了/没启动/端口不对）。

```bash
# 第一步：后端活着吗？
curl http://127.0.0.1:8000/health

# 第二步：Supervisor 状态
supervisorctl status
# 如果显示 FATAL / STOPPED → 看错误日志
supervisorctl tail fastapi stderr

# 第三步：端口被占用？
lsof -i :8000
# 或
ss -tlnp | grep 8000
```

| 原因 | 检查 | 修复 |
|------|------|------|
| 后端进程挂了 | `supervisorctl status` | `supervisorctl restart fastapi` |
| 端口号写错 | Nginx 配置里的 `proxy_pass` 和 FastAPI 启动端口一致吗？ | 改配置 `systemctl restart nginx` |
| 后端监听 127.0.0.1 但 Nginx 连 localhost | 确保两边一致（统一用 `127.0.0.1` 或 `localhost`） | 统一即可 |
| 防火墙挡了内网 | `iptables -L` | 内网 127.0.0.1 不应该被挡 |

### 504 Gateway Timeout

**含义**：Nginx 转发请求给后端了，但后端处理太久，Nginx 等不及就断了。

```nginx
# 加长超时（默认 60s）
location / {
    proxy_pass http://127.0.0.1:8000;
    proxy_read_timeout 300s;       # 等后端响应的最长时间
    proxy_connect_timeout 60s;     # 连接后端的最长时间
    proxy_send_timeout 300s;       # 发送请求给后端的最长时间
}
```

> 如果某个接口就是慢（导出报表、批量处理），给那个接口单独配 `location` 加超时，不要全局放大。

### 证书过期

```bash
# 检查证书到期时间
openssl s_client -connect your-domain.com:443 -servername your-domain.com 2>/dev/null | openssl x509 -noout -dates

# certbot 续期是否正常
certbot renew --dry-run

# 如果自动续期失败，手动续
certbot renew --force-renewal
systemctl reload nginx
```

> certbot 续期后需要 `reload` Nginx（不是 `restart`，reload 不中断连接）。可以在 crontab 加一句：`0 3 * * * certbot renew --quiet && systemctl reload nginx`

### 端口冲突

```bash
# 谁在占用 80 / 443？
ss -tlnp | grep -E ':80 |:443 '

# 杀掉占用进程
fuser -k 80/tcp
```

常见冲突：Caddy 和 Nginx 同时装，都抢 80/443。二选一。

### Nginx 配置有语法错误

```bash
# 改完配置先测语法，别直接 restart！
nginx -t

# 语法 OK 才 reload
systemctl reload nginx
```

> `restart` = 停掉再启动，瞬间丢所有连接。`reload` = 不停机加载新配置。日常改配置用 `reload`。

---

## 🔄 日常运维流程

### 更新代码（标准操作）

```bash
# 1. 拉代码
cd /var/www/myapp
git pull origin main

# 2. 装依赖（如果有新增）
source venv/bin/activate
pip install -r requirements.txt

# 3. 重启应用（Supervisor 方式）
supervisorctl restart fastapi

# 或者 systemd 方式
systemctl restart fastapi

# 4. 验证
curl http://127.0.0.1:8000/health
curl https://your-domain.com/health
```

### 零停机重启（gunicorn）

gunicorn 支持平滑重启：不丢请求，逐个 worker 替换。

```bash
# 发送 HUP 信号 = 优雅重启
kill -HUP $(cat /var/run/gunicorn.pid)

# 或者在 Supervisor 配置里：
# stopsignal=HUP
```

### 部署后检查清单

```bash
□ curl https://域名/health                 # HTTPS 通不通
□ curl -I https://域名                      # 看响应头有没有 HSTS
□ supervisorctl status                      # 进程活着
□ tail -f /var/log/fastapi.err.log          # 没有异常报错
□ openssl s_client -connect 域名:443 </dev/null 2>/dev/null | grep Verify  # 证书 OK
```

### 查看访问日志

```bash
# Nginx 访问日志（谁在访问你的 API）
tail -f /var/log/nginx/access.log

# 只看 API 请求，过滤掉静态文件
tail -f /var/log/nginx/access.log | grep -v '/static/'
```

---

## 🔗 参考

- Nginx 官方文档：https://nginx.org/en/docs/
- Nginx 配置生成器：https://nginxconfig.io/
- Supervisor 官方文档：http://supervisord.org/
- Let's Encrypt：https://letsencrypt.org/zh-cn/
- certbot：https://certbot.eff.org/

---

**更新日期**：2026-05-28
**适用场景**：FastAPI 商业项目阿里云轻量服务器部署
**关联笔记**：20260528_FastAPI商业项目阿里云部署方案_llm_wiki（资料已移出公开 Wiki，待脱敏）
