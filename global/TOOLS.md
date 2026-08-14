# TOOLS.md — 工具使用手册（三大关键工具 + 网关）

> 版本：2026-08-14 首版 ｜ 用途：任何 Agent 接手任务前，若要操作外部系统，先读本手册对应工具章节。
> 凭证纪律：只记「是否登录/登录方式/能力」，**绝不记凭证值**（红线）。状态变化时更新对应小节。

## 工具总览
| 工具 | 版本 | 用途 | 登录态（2026-08-14） |
|------|------|------|---------------------|
| `gh`（GitHub CLI） | 2.97.0 | 仓库操作/PR/Issue | 已登录 201650545（keyring，https） |
| `lark-cli`（飞书 CLI） | 1.0.65 | 飞书多维表格/文档/Bot | 未在本次会话核实登录态 |
| `opencli`（Open CLI） | 1.8.6 | 浏览器自动化/控 AI 引擎/多站适配器 | 依赖日常 Chrome 会话（各站登录态见 RESOURCES.md） |
| 统一网关 `:3000` | - | AI 搜索（元宝/Kimi/秘塔/豆包）+ LLM 聚合 | 2026-08-14 探测超时，可能未运行 |

---

## 1. GitHub CLI（gh）

**已打通**：登录 `201650545`（keyring 存 token，https 协议）；5 个仓库：ai-hub-memory / ai-resource-hub / ai-hub / feishu-data-hub / english-teaching-production。

**常用命令**：
```bash
gh auth status                 # 登录态检查
gh repo clone 201650545/<repo> # 克隆
gh repo list 201650545         # 列仓库
gh pr list / gh issue list     # PR / Issue
git pull --ff-only             # 拉最新（记忆仓库专用，防分叉）
```

**注意**：凭证值（token）绝不写进记忆/commit；git 操作用 `--ff-only` 防分叉；push 失败禁止 force push。

---

## 2. 飞书 CLI（lark-cli）

**已打通**：v1.0.65 可用。飞书集成：多维表格（教学制作工作流 / AI 自助资源库 6 表 / 创意游戏点子表）+ Bot「龙虾2号」。

**常用场景**：
```bash
lark-cli base ...    # 多维表格读写（AI 自助资源库 Base）
lark-cli doc ...     # 云文档
lark-cli im ...      # 消息/Bot
```

**注意**：飞书表是「配置真源」之一（ai-resource-hub 体系）；凭证/密级信息不写入；手机/微信扫码类登录不自动代登（记待办）。

---

## 3. Open CLI（opencli）

**已打通**：v1.8.6；浏览器自动化（操控日常 Chrome）+ 多站适配器 + 控 AI 引擎。

**核心子命令**：
```bash
opencli browser <session> <cmd>   # 浏览器自动化：open/state/find/click/type/eval/extract 等
opencli skills list               # 查看适配器/技能库（opencli-browser / adapter-author / autofix 等）
opencli doctor                    # 浏览器桥接诊断
```

**已控的 AI 引擎**（opencli browser）：doubao-app / chatgpt-app / codex / cursor 等 adapter；镜像站（问达宝）通过 localStorage 登录 + Thinking·Extended。

**实测坑（2026-08-14 记录）**：
- 镜像站账号池会漂移，每次操作先读 panelAccountList 确认健康账号；
- 界面版本不同，模型 pill / 编辑器形态（textarea vs contenteditable）要按页面实际适配；
- 长文本一律 base64 + eval 注入，避免 Windows 命令行解析失败；
- 多链接提示词可能触发 Deep Research 空回复 -> 用单链接/内嵌版或转 Claude。

---

## 4. 统一 AI 搜索网关（:3000）

**位置**：D:\项目\services\search_gateway（unified_gateway.py）。
**能力**：4 大 AI 搜索引擎（元宝/Kimi/秘塔/豆包）并发检索 + LLM 渠道聚合（DeepSeek 官方/Gemini/OpenRouter）。

**接口**：
```bash
GET  /api/health          # 各引擎 + 上游状态
GET  /api/unified_stream?prompt=  # SSE 流式搜索
POST /v1/chat/completions # OpenAI 兼容（model=yuanbao-search 等）
```

**状态**：2026-08-14 探测 /api/health 超时（可能未运行）；使用时先确认网关在线，不在线则重启 python unified_gateway.py。

---

## 更新规则
- 工具**能力/命令/坑**变化 -> 更新本文件对应章节（低频）。
- 工具**登录态/可用性**变化 -> 同步更新「工具总览」表 + 对应章节（中频）。
- **凭证值永不写入**；只记登录方式（keyring/网页/扫码）与状态。
