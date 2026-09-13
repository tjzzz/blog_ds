# blog_ds 博客维护 SOP（中文）

> 本文件是博客的维护记录与操作手册，新接手或隔久了回来照着做即可。
> 线上地址：https://tjzzz.github.io/blog_ds/
> 模板来源：[foam-mkdocs-template](https://github.com/Jackiexiao/foam-mkdocs-template)

---

## 1. 这是什么

- **技术栈**：MkDocs + Material 主题 的静态博客，用 **Obsidian** 写 Markdown，靠 **GitHub Actions** 自动部署到 **GitHub Pages**。
- **发布链路**：本地 `git push` → Actions 跑 `mkdocs gh-deploy --force` → 自动发到 `tjzzz.github.io/blog_ds/`（约 1–2 分钟生效）。
- **本地仓库**：`Z_BlogDS`（已从 iCloud 同步移出，独立维护，避免 `.git`/`.obsidian` 历史冲突）。

## 2. 目录结构（方案 A，2026-09-10 重组）

`docs/` 顶层按数字编号分 **12 类**，MkDocs 无显式 `nav`、自动按目录生成导航：

```
docs/
├─ 01_工具          基础工具（git / markdown / jupyter …）
├─ 02_数据          数据获取 / 可视化 / DS 实践
├─ 03_统计          统计推断 + causal_analysis（因果分析）
├─ 04_机器学习      机器学习主目录
├─ 05_深度学习      深度学习
├─ 06_推荐系统      推荐系统
├─ 07_强化学习      强化学习
├─ 08_业务专题      指标体系 / PDCA / 数据驱动方法论
├─ 09_语言篇        R / Python / SQL 等语言
├─ 10_论文          论文笔记
├─ 11_刷题          算法刷题
├─ 12_效率工具      效率工具 + Working Process
├─ index.md         首页
├─ media/           文章配图（站点根路径引用 /blog_ds/media/xxx.png）
└─ js/extra.js      自定义前端脚本
```

> 不进站点：`.gitignore` 忽略 `Draft/`、`Media/`、`.obsidian` 等本地草稿/杂物，不会被发布；12 个分类目录均为正式内容。

仓库其余层：`mkdocs.yml`（配置）、`requirements.txt`（依赖，须与 `ci.yml` 一致）、`.github/workflows/ci.yml`（部署）、`.obsidian/`（Obsidian 编辑环境，已清理）、`.git/`（→ github.com/tjzzz/blog_ds → Actions → gh-pages → 线上）。

## 3. 本地预览（写稿时必开）

```bash
cd Z_BlogDS
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt      # 或按 ci.yml 里钉的版本装
.venv/bin/mkdocs serve
# 浏览器打开 http://127.0.0.1:8000
```

⚠️ **版本一致性铁律**：`requirements.txt` 和 `ci.yml` 里 `mkdocs-material` 的版本号必须完全相同，否则本地预览和线上长得不一样、甚至 build 报错。

## 4. 写稿规范

- 在 `docs/` 对应分类下新建/编辑 `.md`。
- **配图**：图片丢进 `docs/media/`，正文用站点根路径引用：
  `![](/blog_ds/media/你的图.png)`
- **双链**：`[[笔记名]]`、`![[图片]]` 这类 Obsidian/roam 语法由 `roamlinks` 插件自动转成网页链接，照常用即可。
- 首页改 `docs/index.md`，导航/分类在 `mkdocs.yml` 的 `nav`（如有）或按目录自动生成。

## 5. 发布流程（日常就这四步）

```bash
git add -A
git commit -m "feat: 新增/修改 xxx"
git push origin master        # 或 main，以仓库默认分支为准
```

推送后 Actions 自动部署，刷新 https://tjzzz.github.io/blog_ds/ 验收。

## 6. 维护记录与注意事项

- **2026-09-10 清理 `.obsidian`**：移除了非博客内容（统一进 `~/废纸篓/Z_BlogDS_obsidian_cleanup_20260910/`，可恢复）：
  - iCloud 同步冲突残留：`*NSConflict-*` 文件；
  - 旧重复 workspace 文件（`workspace 2`、`workspace 2.json` 等）；
  - macOS 元数据 `.DS_Store`；
  - 4 个**已禁用**的插件目录：`obsidian-textgenerator-plugin`(14M)、`obsidian-mind-map`(3.8M)、`webpage-html-export`(3.2M)、`digitalgarden`(1M)，合计约 22M。
  - **保留**：10 个启用插件（dataview / kanban / excalidraw / markdown-table-editor / find-unlinked-files / chatgpt-md / search-on-internet / heatmap-calendar / mx-bili-plugin / media-extended）+ 核心配置。`.obsidian` 由 41M 降至 19M。
- **已移出 iCloud**：本仓库不再走 iCloud 同步，避免 `.git` 历史与多设备 workspace 冲突。
- **依赖版本钉死**：`mkdocs-material` 当前版本见 `requirements.txt` 与 `ci.yml`（二者已对齐）。升级大版本（如 5.x → 9.x）有 breaking change，必须先改 `mkdocs.yml` 适配再本地 `mkdocs build` 验证，确认无误后再 push。
- **安全项**：`mkdocs.yml` 的 `extra_javascript` 里引用了 `polyfill.io`（该服务 2024 年已停服且曾被劫持），升级版本时建议一并删除该行。
- **2026-09-10 目录重组（方案 A）**：`docs/` 顶层由混排旧命名（21 项，含 `6_DeepLearning` 与 `6_RecommendSystem` 撞号、缺 3/8）统一为数字编号 12 类（`01_工具`…`12_效率工具`）；`causal_analysis` 归回 `03_统计/`；`9专题-指标体系PDCA` 与 `数据驱动` 并入 `08_业务专题`；`ds实践系列` 并入 `02_数据`；根目录游离的 `Working Process.md` 收编进 `12_效率工具`；清理 17 个 reorganization 遗留的死空目录（移 `~/废纸篓/blog_ds_deaddirs_20260910/`，可恢复）。MkDocs 无显式 `nav`、按目录自动生成导航，重命名不影响构建。

## 7. 常见问题速查

| 现象 | 排查 |
|---|---|
| 本地预览和线上长得不一样 | 检查 `requirements.txt` 与 `ci.yml` 的 `mkdocs-material` 版本是否一致 |
| 图片不显示 | 确认 md 里用的是 `/blog_ds/media/xxx.png`，且文件确实在 `docs/media/` |
| `mkdocs build` 报错 | 多半是 `mkdocs.yml` 的 `markdown_extensions` 写法过时（如老 `codehilite` 在 9.x 需改为 `pymdownx.highlight`） |
| 部署没生效 | GitHub → Settings → Actions → Workflow permissions 需为 `Read and write`；看 Actions 日志 |

---

_Last maintained: 2026-09-10_
