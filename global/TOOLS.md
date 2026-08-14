# TOOLS.md — 环境工具运行手册（V2）

> 定位：**HOW**（怎么操作环境）——不是资源台账（RESOURCES.md=What），不是项目状态（projects/=Why）。
> 使用：需要外部系统时按需读对应章节；**实时状态不得信任历史**，运行前 Preflight。
> 安全：**不保存任何认证材料**（总原则：可保存"如何找到/验证认证"，不得保存任何能恢复认证的材料）。

## 0. 任务速查
| 我要做什么 | 首选工具 | Preflight | 章节 |
|-----------|---------|-----------|------|
| GitHub 仓库/PR/Issue | gh | gh auth status | §2 |
| 飞书表/文档/Bot | lark-cli | 认证状态检查 | §3 |
| 操作已登录网页/AI 引擎 | opencli | opencli doctor | §4 |
| 多引擎 AI 搜索/LLM 聚合 | 网关 :3000 | health check | §5 |

## 1. 首次使用检查（弱模型也照做）
1. 确认任务该用哪个工具（看 §0 速查）。
2. 读该工具章节。
3. 先执行只读 Preflight。
4. 确认当前 account/project/session 范围正确。
5. **先读后写**。
6. 遇到认证/scope/未知页面结构 → **停止猜测**。
7. 写操作遵守 global/RULES 和项目规则。

> **STOP 原则：UNKNOWN ≠ READY。核验失败就停，不根据旧状态推断当前状态。**（工具层的 Fail Closed）

## 2. GitHub CLI（gh）
- 用途：仓库操作/PR/Issue/认证管理。
- Preflight：`gh auth status`（登录态，keyring 存储）。
- 最少命令：
  ```bash
  gh repo clone 201650545/<repo>
  gh repo list 201650545
  gh pr list / gh issue list
  git pull --ff-only   # 记忆仓库专用，防分叉
  ```
- 成功标准：命令输出仓库/PR 列表；git 操作 exit 0。
- STOP：auth 失败 → 停止并请求人工重新登录；push 失败 → 禁止 force push（按 RULES）。
- 坑：凭证值绝不写记忆/commit。

## 3. 飞书 CLI（lark-cli）
- 用途：飞书多维表格/文档/Bot（教学制作工作流 / AI 自助资源库 6 表 / 创意点子表）。
- 认证：运行时检查（本次未在会话内核实）；不记录认证材料。
- 最少命令：
  ```bash
  lark-cli base ...   # 多维表格读写
  lark-cli doc ...    # 云文档
  lark-cli im ...     # 消息/Bot
  ```
- 成功标准：表格/文档数据返回；消息发送确认。
- STOP：认证失效 → 停止并请求人工处理；需扫码/手机验证 → 不自动代登（记待办）。
- 坑：飞书表是配置真源之一（ai-resource-hub 体系）；密级信息不写入。

## 4. Open CLI（opencli）
- 用途：浏览器自动化（日常 Chrome）+ 多站适配器 + 控 AI 引擎。
- Preflight：`opencli doctor`（浏览器桥接诊断）；`opencli skills list`（适配器清单）。
- 最少命令：
  ```bash
  opencli browser <session> open/state/find/click/type/eval/extract
  opencli skills list
  opencli doctor
  ```
- 成功标准：browser 返回元素/内容 JSON；doctor 显示桥接正常。
- STOP：页面结构未知 → 先 state 再操作，不盲猜选择器；session 失效（about:blank）→ 重新 open 目标 URL。
- 坑（[2026-08-14 / 1.8.6]）：
  - 镜像站账号池漂移 → 每次先读 panelAccountList 确认健康账号；
  - 界面形态（textarea vs contenteditable）随版本变 → 按页面实际适配；
  - Windows 长文本 → base64 + eval 注入，勿直接 CLI 传参；
  - 多链接提示词可能触发 Deep Research 空回复 → 单链接/内嵌版或转 Claude。

## 5. 统一 AI 搜索网关（:3000）
- 用途：4 大 AI 搜索（元宝/Kimi/秘塔/豆包）并发 + LLM 渠道聚合（DeepSeek 官方/Gemini/OpenRouter）。
- Preflight：GET /api/health（各引擎 + 上游状态）。
- 接口：
  ```bash
  GET  /api/health
  GET  /api/unified_stream?prompt=   # SSE 流式
  POST /v1/chat/completions          # OpenAI 兼容
  ```
- 成功标准：health 返回引擎状态；stream/chat 返回内容。
- STOP：health 超时/DOWN → 确认服务是否启动，不假装可用。
- 状态：runtime volatile；服务定位见环境 bootstrap（不用绝对本机路径）。

## 6. 通用安全红线
TOOLS 可保存"如何找到/验证认证"，**不得保存任何能直接或间接恢复认证的材料**。禁止：
- password / API key / access·refresh·session token / cookie / Authorization header
- OAuth code / 二维码认证数据 / private key / localStorage 认证值
- 完整 credential/env dump / 私人手机号·邮箱·账号池明细
- 带认证信息的 URL / 内部管理 URL / 私有网络地址
- 不必要的绝对本机路径（用逻辑名/相对路径/环境变量）；
- 日志、示例输出、截图中的秘密同样属于秘密。
> 高风险写操作（删除/覆盖/发消息/push/改外部表）→ 先按 global/RULES 确认，不自行执行。

## 7. 更新规则
- 只有**持久变化**才更新 TOOLS：命令变化 / 认证方式变化 / 新增或弃用工具 / 稳定 workaround 改变 / 服务永久迁移。
- 瞬时状态（session logout/Chrome 崩/账号池漂移/gateway 没启动）→ **现场检查解决，不 commit**。
- 工具达 6-8 个或 TOOLS 超 200-300 行 → 拆分 global/tools/<name>.md，TOOLS.md 只做入口+速查+安全。
- 凭证值永不写入；只记认证方式（keyring/浏览器 session/人工扫码）与核验方法。
