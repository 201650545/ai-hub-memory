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
| OpenAI API 模型路由 | 网关 :3100 | GET /v1/models + /api/rate-limits | §6.6 |
| 夸克网盘列目录 | qk-list.cjs | node --check + 凭证存在 | §6 |

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
  - 多链接提示词可能触发 Deep Research 空回复 → 用单链接/内嵌版提示词规避；仍空回复则按「镜像站故障处理」（见下）报告用户，不自动兜底。
  - **切换 Extended（2026-08-21 实测）**：模型下拉是**自定义 Radix Select**，菜单项不暴露独立按钮索引，整段正则匹配会点中容器 DIV 导致失败；正确做法：先点开右下角「Auto」选择器（aria-haspopup=menu），再用 `document.querySelector('[class*=model-picker-thinking-effort-menu-item]').click()` 精确命中「Thinking · Extended」项（其内层 SPAN class 类似 `flex min-w-0 items-center gap-1`）。提交后务必重新抓取最后一轮（`[data-testid^=conversation-turn-]` 取 last.innerText），避免混用历史会话旧文本。
- **共享浏览器标签页纪律（用户拍板 2026-08-27，2026-08-28 补充闭环，强制）**：opencli 浏览器会话（如 n8hh7hyn）是**多进程/多 Agent 共享**的——其他任务可能正在用某个标签页（切到小红书/SambaNova/任意页面）。**已有标签页不要抢占、不要导航跳走别人的页面**；需要打开自己的目标时，一律**新建标签页**：`opencli browser <session> tab new "<url>"`（返回 target ID，后续命令用 `--tab <targetId>` 指向自己的标签）。**关闭闭环（2026-08-28，D-GLOBAL-20260828-01）**：① 由 AI 打开的标签页，任务完成后即 `tab close <targetId>` 关闭；② 新任务/不同类型任务时开新标签页，做完关闭旧的；③ **只关闭 AI 自己打开的标签页，绝不切换/关闭用户或其他 Agent 打开的标签页**。会话默认标签被占用时，先 `tab list` 看当前有哪些标签、谁在用，再决定新开。规则原因：2026-08-27 实测发现共享会话标签被反复切走导致镜像站问诊中断、注入内容丢失。
- **会话纪律（用户拍板 2026-08-15，2026-08-27 修订窗口轮次上限，强制）**：① 进入镜像站后**复用左侧历史会话**（点历史记录进入，不新开对话），再调模型为 Thinking·Extended；② **每个任务 ≤3 轮对答**完成（含 GPT 反问的交流，3 轮内必须解决回来执行）；③ **每窗口 ≤12 轮**，超了必须新开对话（新开后重新选模型）。详细步骤见 ai-resource-hub 操作手册 01 §9。
- **镜像站故障处理（2026-08-28 修订，D-GLOBAL-20260828-01：停用 Kimi 自动兜底）**：GPT 镜像站不可用/空回复/需第二意见时，**不自动转 Kimi**——直接向用户报告：故障现象、已尝试的账号与会话、建议动作（换账号/换会话/稍后重试），等用户指示。Kimi K3 仅在用户主动要求时使用。历史：2026-08-15~27 曾用 Kimi K3 自动兜底（D-GLOBAL-20260815-04，已废止）。：Claude 额度已用光，问诊兜底不再走 Claude。GPT 镜像站不可用/空回复/需第二意见时 → `opencli browser <s> open kimi.com`，提问前先开启 **K3 思考进阶模式**（界面找 K3 模型/进阶模式开关），再发送问题；长提示词同样 base64 + eval 注入。

- **`browser screenshot` 两个实测坑（2026-08-29，DSH 侧「截图失效」排障结论）**：
  ① **必须传 `path` 落盘**：省略位置参数时命令把整张 PNG 以 base64 直写 stdout（实测飞书 Base 页面 **886 KB** 单行），既塞爆 Agent 上下文又易被宿主管道截断。用法 `opencli browser <s> screenshot "<file>.png" --tab <id>`。
  ② **`cdp_timeout` 会间歇触发**：`Page.captureScreenshot` 默认超时 **60 秒**（`dist/src/browser/config.js` 的 `DEFAULT_BROWSER_COMMAND_TIMEOUT=60`）。重型页面在 `devicePixelRatio=2` 下光栅为 3200×1550（约 5 Mpx），实测**同一标签页一次 5s 成功、一次 >60s 超时**，报 `CDP command Page.captureScreenshot timed out after 60s`。opencli 在 `browser/errors.js` 把 `cdp_timeout` 标为 **non-retryable**，宿主不会自动重试，表现为「命令挂住后无结果」。
  处置优先级：用 `--width/--height` 降光栅（实测同一页 1280×720 立即成功）→ 需要大图时加 `--timeout <秒>`（或全局环境变量 `OPENCLI_BROWSER_COMMAND_TIMEOUT`）→ 治本是自动化 Chrome 启动加 `--force-device-scale-factor=1` 把光栅减半，但这会影响共享浏览器实例，须先确认无其他 Agent 在用。
  **已排除的错误归因（勿再重复排查）**：与运行账户无关——DSH 宿主虽以 SYSTEM 运行（node 监听 3080），但把 `HOME/USERPROFILE/APPDATA/LOCALAPPDATA/TEMP` 全部指向空目录后，`tab list` 与 `screenshot` 依旧正常，说明会话发现不依赖用户 profile 注册表；`tab list` 报 `active=False` 也不影响截图。
- **STOP**：截图报 `cdp_timeout` 不要盲目重跑，先降视口或加 `--timeout`；反复失败才考虑页面被原生对话框阻塞（用 `browser dialog` 处理）。

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
- **启动（2026-08-15 拆分为两个独立网关）**：
  - AI 搜索网关：python <search_gateway 目录>/search_gateway.py（:3000；SEARCH_GATEWAY_PORT 覆盖）。引擎：元宝/豆包/Kimi/通义。页面 /aggregate、报告 /reports/、API /api/search_aggregate、SSE /api/unified_stream。
  - API 转发网关：python <search_gateway 目录>/api_gateway.py（:3100；API_GATEWAY_PORT 覆盖）。OpenAI 兼容 /v1/chat/completions + /api/channels（key 管理）。渠道顺序 CHANNEL_ORDER：opencode(OpenCode Go, 用户 2026-08-15 提供, key 存 data/search_gateway/channels.json)→deepseek→gemini→openrouter→groq→siliconflow→dashscope→zhipu。DeepSeek key 从 DSH .env 注入 DEEPSEEK_API_KEY。
  - **OpenCode Go 渠道已验证可用（2026-08-15）**：base_url https://opencode.ai/zen/go/v1，模型 deepseek-v4-flash 转发 200（含 reasoning_content）；stream 正常结束。**关键坑**：opencode 由 Cloudflare 保护，默认 python UA 直接 403（error 1010，按浏览器签名封禁）；请求必须带 User-Agent: openai-completions/pi-ai（channels.py 中 opencode 条目 ua 字段已配置，chat_completion/_get_json 均使用渠道 UA）。另：model_to_chain 中 deepseek-* 模型首选 opencode、fallback deepseek；流式转发检测到 [DONE] 即结束连接，避免上游 keep-alive 挂起。reasoning_effort 非必需（纯 UA 修复即可 200）。
  - **新增渠道（2026-08-16）**：modelscope（魔塔社区 api-inference.modelscope.cn，模型 deepseek-ai/DeepSeek-V4-Flash-0731 等，key 取自 Cherry Studio）与 sensetime（商汤日日新 token.sensenova.cn，模型 deepseek-v4-flash/glm-5.2/sensenova-6.8-flash-lite）。模型路由：deepseek-ai/ 前缀→modelscope；sensenova-→sensetime；无前缀 deepseek-v4-flash/glm-5.2→opencode+sensetime fallback。注意：modelscope 上 ZhipuAI/GLM-5.2 上游返回空 choices（未部署）；sensetime sensenova 响应字段是 reasoning 非 content 且吃 max_tokens。
  - **再增渠道（2026-08-16）**：agnes（AGNES AI apihub.agnes-ai.com/v1，agnes-2.5-flash 等）与 zscc（api.zscc.in，kimi-k3-cc/claude-opus-4-8/claude-sonnet-5/deepseek-v4-flash-cc），key 均取自 Cherry Studio。坑：zscc 根路径是网页，OpenAI 兼容必须在 /v1（base_url 需含 /v1），/models 也走 /v1/models（渠道级 models_path 字段）；agnes-* 模型路由优先 agnes（勿写成 zscc 优先）。
  - **ZSCC 禁测（用户 2026-08-16 拍板）**：zscc 渠道很贵，禁止任何测试/探测请求。代码已固化：channels.py 的 NO_TEST_CHANNELS={"zscc"}（健康检查不探测、静态标记可达）；api_gateway /api/channels/zscc/test 拦截返回 no_test；页面快速测试列表自动排除 zscc。以后任何 Agent 不得对 zscc 发起 chat/completions 测试。
  - **模型反查功能（2026-08-16）**：channels.py 新增 all_models()（聚合所有在线渠道模型去重）、model_providers(model)（包含搜索反查支持某模型的所有渠道）、_channel_sort_key()（排序键：免费优先→速度快优先→渠道顺序）。每个渠道加 speed 字段（fast/medium/slow）。api_gateway 新增 /api/models、/api/model_providers?model=xxx 端点。前端重新设计为苹果官网风格（浅色+SF Pro+大圆角），核心功能：搜索模型→自动反查所有支持它的 API 提供商→按免费/速度智能排序展示。
  - **Gemini 多模态接入（2026-08-16）**：Google 被墙需走本机 mihomo 代理 127.0.0.1:7890（Sparkle/Clash 内核，间歇不稳约 80% 成功率）。channels.py 新增 _urlopen/_build_opener 代理辅助 + gemini 渠道配 proxy 字段，chat_completion/channel_health 走代理。key 取自 Cherry Studio（AIzaSy...）。gemini-3.5-flash/flash-latest/3.1-flash-lite 支持多模态图像理解（已 E2E 验证识别颜色）；gemini-3.1-flash-image 是图像生成模型，免费配额 429 已剔除。当前支持多模态的渠道：gemini。
  - **AI Hub 前端+搜索引擎大重构（2026-08-18）**：①AI 搜索网关前端(web/hub_page.html+aggregate.html)与报告(report.html)全部改为苹果风(#0071e3/#1d1d1f/#d2d2d7)；②编排画布(:8791)已能打开——canvas_server.py 加心跳上报 central，画布 emoji→线性SVG；③引擎适配修复：doubao/kimi/qianwen 页面改版后选择器全失效，已逐一实地重调——doubao(输入改contenteditable,DOM适配 submit .send-btn-wrapper+extract 重写)、kimi(submit .send-button-container+extract .chat-content-item-assistant)、qianwen(type输入+button.size-8.border-0+extract)。实测 kimi 稳定ok、doubao 会话异常时超时、qianwen 站点端限流；④_llm_summarize 端口 bug 修复：原来调 :3000(搜索网关只认 yuanbao-search，拒 deepseek)改为 :3100(API网关)，综合结论能正常生成。⑤启动脚本 services/start_all.ps1(独立进程起 3 网关)。
  - **DSH/Harness 接入本地网关（2026-08-16）**：settings.yaml 新增 local-gateway provider（baseURL http://127.0.0.1:3100/v1，api openai-completions，headers Authorization: Bearer local-gateway 占位——pi-ai 无 key 会抛 No API key）。agent-default-model.provider=local-gateway model=deepseek-v4-flash。这样 Harness 里用 deepseek-v4-flash 自动走网关免费优先路由（modelscope 免费优先于 opencode 付费）+ 模型名映射 + 多模态。注意：agent-default-model 是 per-session 注册的 namespace，不出现在全局 settings.describe；新会话才生效。网关运行依赖 DSH 后台 job（sandbox 会杀独立 Start-Process 进程），持久化需用户自行运行 services/start_all.ps1 或开机自启。
  - 旧 unified_gateway.py（合并版）已废弃不再启动。
  - **中央平台网关管理与首页（2026-08-16）**：config/gateways.json 注册表已更新为拆分后的两个网关（search_gateway :3000 + api_gateway :3100）。两网关启动时经 services/search_gateway/heartbeat.py 自动注册（POST /api/gateways）+ 每 30s 心跳上报 central :8000，中央首页 / 与 dashboard 实时显示在线状态。心跳失败静默降级不阻塞网关；CENTRAL_URL 可关（空串）。

## 6. 夸克网盘列目录（qk-list）
- 用途：列出夸克网盘根目录内容（官方 skill 只有语义搜索，无法列目录）。**根目录 100% 可靠；子目录导航不可用**（fid 会话级临时标识）。
- 前置：官方 skill 已装并授权（凭证 OAuth 后自动写入 skill 的 config.json，**只读不打印**）。
- 已交付命令（无需实现）：
  ```bash
  node "<skill>/scripts/qk-list.cjs"           # 列出根目录
  node "<skill>/scripts/qk-list.cjs" --all     # 翻页取全部
  node "<skill>/scripts/qk-list.cjs" --size 200 # 自定义每页
  ```
  - stdout 输出 NDJSON（type:"result" 含 dirs/files/dir_count/file_count）
  - stderr 打印 [DIR]/[FILE] 人类可读列表
- 自检：`node --check qk-list.cjs` 通过；根目录能列出目标文件夹（如「6-奥数」「7-课本」）。
- STOP：认证失败/凭证缺失 → 停止并请求人工重新授权；不自行猜测 token。
- 坑（[2026-08-14]）：
  - 签名头 x-pan-token = sha256("POST&/open/v1/file/list&<毫秒tm>&signKey")；client-id 必须写死 third_party_agent；
  - req_id 必须 UUIDv4；空 keyword 搜索会 400（search 无法枚举目录，必须走 file/list）；
  - 修改 minified 文件别用 bash 双引号传 \n（用脚本文件打补丁 + node --check 验证）。
- 详细逆向方法论/完整代码/凭证结构：见 docs 目录《夸克网盘列目录_qk-list_操作文档.md》（HOW 详解，本手册只放速用）。

## 6.5 公开数据消费规范（R9，GLM 审查 2026-08-14）
- 读取 GitHub Pages 公开 JSON（ai-resource-hub / feishu-data-hub）前，**先读 catalog/status**。
- `is_stale=true` 时**回退飞书真源或提示用户**，不用陈旧数据决策。
- 新鲜度：数据生成时间 vs 当前时间，超阈值视为 stale。

## 6.6 OpenAI API 模型路由网关（:3100）
- 用途：OpenAI-compatible LLM 路由网关（多厂商聚合 + 自动 fallback），与 :3000 AI 搜索网关**相互独立**。
- 入口：`http://127.0.0.1:3100`（API_GATEWAY_PORT 覆盖）。
- 关键文件（services/search_gateway/）：
  - `api_gateway.py`：HTTP 服务 + 路由/failover 编排
  - `channels.py`：渠道层、key 池轮换、健康缓存
  - `rate_limit.py`：容量准入（try_acquire）+ 429/空壳熔断
  - `upstream_outcome.py`：失败归一化（Phase 1）—— 上游错误统一为 Outcome 枚举（SUCCESS/RATE_LIMIT/QUOTA/AUTH/MODEL_UNAVAILABLE/OVERLOADED/PROTOCOL_ERROR/TIMEOUT），`classify_http_status`/`classify_shell` 归一化、`is_breaker` 判定熔断类型
  - `quota.py`：本地额度统计（独立于 :3000 记账）
- 配置（data/search_gateway/）：`unified_models.json`（统一模型组）、`routing.json`（用户手工渠道顺序）、`channels.json`（渠道 key）。
- 主要机制：统一模型 → 用户人工渠道顺序 → health eligibility → rate-limit eligibility（try_acquire 95/85 滞后）→ upstream attempt → **失败归一化（upstream_outcome）** → failover（HTTP 429 / 200+quota 空壳 / timeout / 503 / blocked 本地 skip）。熔断类型（RATE_LIMIT/QUOTA/AUTH/OVERLOADED）触发指数退避跳过。
- **流式 commit point（Phase 1 不变量）**：failover 只允许发生在 response commit 前——首包验证（_peek_stream）通过即视为已提交，此后不得换上游继续输出，避免客户端收到多模型拼接。
- Preflight：
  ```bash
  # 1. 进程在跑
  Get-NetTCPConnection -LocalPort 3100 -State Listen
  # 2. 模型列表
  curl http://127.0.0.1:3100/v1/models
  # 3. 健康 + 限流台账
  curl http://127.0.0.1:3100/api/health
  curl http://127.0.0.1:3100/api/rate-limits
  # 4. 最近路由决策日志
  curl http://127.0.0.1:3100/api/route-log
  # 5. 路由可观测（Phase 1）：候选渠道链 + 每渠道 eligible/reason/state/blocked_in
  curl http://127.0.0.1:3100/api/route-plan?model=<统一模型名>
  ```
- STOP：runtime SHA 与文档不一致时先核代码；**UNKNOWN != READY**。
- 注意：动态资源状态（某渠道剩余额度/是否 503/今日 429）不属于 TOOLS，现场查 `/api/health`、`/api/rate-limits`、`/api/route-log`、`/api/route-plan`。
- 基线：Phase 0 冻结于 refactor/monorepo-20260812 @ `gateway-baseline-20260827`；Phase 1（失败归一化 + route-plan 可观测 + commit point + 8-case 回归）完成于 2026-08-27（见 projects/devel-tools/STATE.md）。

## 6.7 CC Switch 本地代理（Claude Code 出口）

- **CC Switch v3.14.1 已知行为（2026-08-27 实测）**：开启 local proxy 会把 `~/.claude/settings.json` 的 `ANTHROPIC_BASE_URL` 指向本地 proxy（默认 `127.0.0.1:15721`），并可能重写 `ANTHROPIC_*_MODEL` 为 Claude 官方别名（`claude-opus-4-8` / `claude-sonnet-4-6` / `claude-haiku-4-5` / `claude-fable-5`）；原 provider 模型信息会被移到对应 `*_MODEL_NAME` 字段。`proxy_live_backup` 表可用于恢复开 proxy 前的配置。执行 Agent **不得**仅依据 DB 中 `live_takeover_active` 判断 takeover 状态，必须以实际 Claude settings / 出口为准。
- **proxy 只认 current provider**：转发目标由 `providers.is_current=1` 的那一条决定，且**忽略客户端传入的模型名**（日志实证：发 `gateway-3100:deepseek-v4-flash` 与 `deepseek-v4-flash`，上游收到的都是现用 provider 自己的模型串）。因此**不存在"按请求选 provider"的隔离能力**，要换出口必须翻全局 current provider，会波及所有复用同一 settings.json 的 Claude Code 会话。
- provider 的 API 格式存于 `providers.meta` 的 `apiFormat` 字段（实测取值：`anthropic` / `openai_chat`），不在 `settings_config` 里；`settings_config` 就是写入 Claude settings 的那份 JSON。
- 配置载体是 `~/.cc-switch/cc-switch.db`（`journal_mode=delete`），**无控制 API**（进程零监听端口时即为未开代理）；改库需先停 app，否则可能被应用侧内存缓存回写覆盖。
- 凭证分层（2026-08-27 阶段3 实证，勿再误判）：**live `~/.claude/settings.json` 里的 `ANTHROPIC_AUTH_TOKEN` 是 CC Switch 给 proxy 自建的客户端 token（长度约 13），不是上游 key**；上游真值只存在 `providers.settings_config.env.ANTHROPIC_AUTH_TOKEN`，proxy 用它在转发时打上游。因此接自建网关时，应把网关 key 只写 provider 侧，不要试图写进 live。
- `proxy_live_backup` 会回灌旧凭证：当 `live_matches_current_proxy=false` 时 CC Switch 会用该行「补齐 Live」，若该行 `original_config` 内是别的 provider 的 token，每轮启动都会把旧 token 同时灌回 live 与 provider，表现为"我写的 provider key 被吃掉"（实测长度从网关 key 变回旧 provider 的 42 位）。排查顺序：先确认备份行内容，再怀疑覆盖逻辑。
- 正确接入顺序：停 app → 清/校正 `proxy_live_backup` → 写 provider（含上游 key、`meta.apiFormat`）→ 改 `currentProviderClaude` 与 `is_current` → 开 `proxy_enabled/enabled` → 启 app → 用 `:3100 /api/route-log` 与 CC Switch `请求目标` 日志双向确认。回退时必须用**原 provider 的 `settings_config`** 作为 live 凭证真源（备份行可能已被污染）。
- 取证：CC Switch 自身日志 `~/.cc-switch/logs/cc-switch.log` 会打印 `[Claude] >>> 请求目标: <url> (model=<上游模型>)` 与 `[FWD-003]` 上游失败原因，是判断"到底打到哪、被谁 429"的唯一可靠依据。

## 7. 通用安全红线
TOOLS 可保存"如何找到/验证认证"，**不得保存任何能直接或间接恢复认证的材料**。禁止：
- password / API key / access·refresh·session token / cookie / Authorization header
- OAuth code / 二维码认证数据 / private key / localStorage 认证值
- 完整 credential/env dump / 私人手机号·邮箱·账号池明细
- 带认证信息的 URL / 内部管理 URL / 私有网络地址
- 不必要的绝对本机路径（用逻辑名/相对路径/环境变量）；
- 日志、示例输出、截图中的秘密同样属于秘密。
> 高风险写操作（删除/覆盖/发消息/push/改外部表）→ 先按 global/RULES 确认，不自行执行。

## 8. 更新规则
- 只有**持久变化**才更新 TOOLS：命令变化 / 认证方式变化 / 新增或弃用工具 / 稳定 workaround 改变 / 服务永久迁移。
- 瞬时状态（session logout/Chrome 崩/账号池漂移/gateway 没启动）→ **现场检查解决，不 commit**。
- 工具达 6-8 个或 TOOLS 超 200-300 行 → 拆分 global/tools/<name>.md，TOOLS.md 只做入口+速查+安全。
- 凭证值永不写入；只记认证方式（keyring/浏览器 session/人工扫码）与核验方法。
