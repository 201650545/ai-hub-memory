# STATE.md — AI资源实测 项目状态

## 进行中
- 无。

## 卡点（漏项 — 2026-09-03 郭老师指出）
- **T-20260903-01 漏项（部分受阻）：问 GPT 镜像版关于"反贷（兜底/fallback）"的事**。RFC v2 已写并 push GitHub（`https://github.com/201650545/ai-hub-memory/blob/master/projects/ai-resources/plans/plan-fast-chain-resilience-v2-20260903.md`, 提交 2988934）。GPT 镜像站注入遇阻：opencli browser gpt 试了 5+ 种点击策略（"新对话"按钮、ChatGPT 卡片、强制 hashchange、完整鼠标事件序列、轮询 10s）——URL 跳到 `/chat/1788418...` 但 body 仍是账号选择页内容（Vue SPA 路由未触发水合, 0 input/iframe）。TRAE SOLO send 派任务也超时 body=0（可能 chat workspace 未就绪）。**未注入 GPT 的兜底**：①RFC v2 全文已落 GitHub, 郭老师可直接打开链接给 ChatGPT 评审；②markdown 全文在 `D:\项目\ai-hub-memory\projects\ai-resources\plans\plan-fast-chain-resilience-v2-20260903.md`, 复制粘贴可走 Kimi K3/Claude 等其他 C 级入口（TOOLS §4.5）。**待办**：①郭老师如需真 GPT 反馈, 可手动打开镜像站粘贴 RFC（ai.wendabao-f.net ?utm_source=hidden-ncn），或换 kimi/openai-completions/pi-ai API 直调；②等 v2.8 镜像站前端水合修复后重试自动注入。（2026-09-03，调度大脑）
- **T-20260903-02 漏项（已完成）：fast 链抗脆弱性方案未独立成 RFC**。RFC v2 独立成文 `D:\项目\ai-hub-memory\projects\ai-resources\plans\plan-fast-chain-resilience-v2-20260903.md`, 5 候选方案 A-E + 推荐 A+B 组合 + 3 待 GPT 评审问题。已 push GitHub 提交 2988934。（2026-09-03，调度大脑）
- **T-20260903-03 漏项（已修正归属）：v2.8 汇报补登**——原记 ai-resources 错，v2.8 实际是 nitian-theme 项目 9-1 深夜交付的三任务汇报（`D:\游戏\逆天主题\workers\汇报_v2.8_双风格_大小境界_本尊分身.md`）。调度大脑 9-2 漏读未回写。**已修正**：9-2 补 S-20260902-10 到 nitian-theme CHANGELOG + STATE（4 项对照全过 + 追加修复节 + 真人风 3 视频），反思建立"汇报接收即回写 STATE"硬规则。ai-resources 漏项段不再保留此条。
- **T-20260903-04 漏项（已完成）：S-20260902-06 后续 e2e 验证未做**。TRAE 汇报"按约定明日再验"今日到期。**调度大脑 9-3 亲做 e2e**（TRAE send 超时 body=0 失败, 调度大脑 curl 直接实测）：①harness 模式 high-free 3 次（"ping"/"say hi"/"ping 2"等），3/3 X-Routed-Channel=gmi + X-Resolved-Model=MiniMaxAI/MiniMax-M3 + X-Fallback-Count=0 + content 正常；②cherry 协议 tool_choice=required + tools=function 实测——finish_reason=tool_calls + 1 tool_calls (get_weather({"location":"San Francisco"})) 解析正确, OpenAI 协议兼容 cherry studio 可直接消费。报告 `D:\项目\logs\e2e_harness_20260903.md`。**反思**: e2e 类任务调度大脑 curl 直接实测 < 5 分钟, 不必非等 TRAE；TRAE send 超时 body=0 多半是 SOLO chat workspace 未就绪, 可用 fallback 路径（调度大脑亲自跑 + cherry studio 实操）。（2026-09-03，调度大脑）
- **T-20260903-05 漏项（已完成）：cherry studio e2e 实测**。与 T-04 合并在同一 curl 测试中（tool_choice=required 实测通过）。**已验证 cherry studio 走 high-free 真实聊天能通, tool_calls 协议兼容**。（2026-09-03，调度大脑）

## 已完成（最近）
- **[S-20260831-01]** 三级派发统一入口 dispatch.py 落地（用户 2026-08-31 拍板，D-GLOBAL-20260831-01）：`D:\项目\services\dispatch.py` 统一派发 A/B/C 三级——A 免费模型（subagent→:3100）/ B 程序 Agent（trae-solo 默认锁 DeepSeek V4 Flash 正式版、备选 qoder CLI）/ C 浏览器（opencli）。付费边界默认全免费，--paid 才允许付费模型。实测 A 级两次真实调用通过、TRAE 链路可用。**派发可视化已接入网关**：:3100 新增 `/dispatch` 苹果风液态玻璃页面 + `/api/dispatch/status`（免鉴权只读）——三级矩阵卡片 + 执行位状态（:3100/trae/qoder/opencli/modelscope 计划任务）+ 最近派发历史（dispatch.py 落盘 dispatch_history.jsonl，网关读取渲染），实测 DOM 全绿渲染成功。**修复 modelscope-daily 魔粒守护 JSON 解析崩溃**（用户报 "Unexpected non-whitespace character after JSON"）：魔塔余额接口返回非 JSON 时 `r.json()` 抛错，改 `r.text()` + 容错解析（含 JSON+尾随行场景），5 用例全过。TOOLS.md §4.5 已加章节。（2026-08-31）
- **[S-20260830-10]** 网关进程改普通权限运行，重启**免 UAC**（用户被反复 UAC 骚扰）：根因=早前用 `Start-Process -Verb RunAs` 启动 python 致网关提权、普通杀它必 Access denied、每次重启都弹 UAC 恶性循环；修复=一次性提权只**杀**旧提权进程 + **普通权限**启动新网关，实测普通 Stop-Process 可杀可启；正确重启姿势已写入 project_ai_gateway 记忆（禁止 -Verb RunAs 启动 python）。（2026-08-30）
- **[S-20260830-09]** ark 与 ark-flash 合并（用户：只用 ark 免费额度 + coding 套餐）——ark-flash 渠道删除，GA 模型并入内置 ark 渠道（channels.py models 加 deepseek-v4-flash-ga-260731 / pro-ga-260813，note 注明合并）；deepseek-free 组 9→8 成员（删 ark-flash），flash-ga 按模型名直调（包含搜索优先走 ark 免费）；渠道总数 20→19，火山方舟只剩 ark(免费)/ark-coding(套餐)。（2026-08-30）
- **[S-20260830-08]** 修正 S-20260830-05：coding 套餐渠道合并为**单渠道 ark-coding**（用户纠正「一个厂商的 3 个模型就一个渠道，别拆 3 渠道」）——models=[deepseek-v4-flash, glm-5.3-flash, deepseek-v4-pro]，base /api/coding/v3；unified 组 coding-plan={ark-coding: deepseek-v4-flash}，GLM/V4-Pro 按模型名直调；**新增编排组 glm-5.3-flash**={opencode→ark-coding}（openrouter/zenmux 收钱已剔除），实测 glm-5.3-flash 在 ark-coding 链路通。（2026-08-30）
- **[S-20260830-07]** 网关统一剥离 reasoning_content（用户拍板）：魔塔 DeepSeek V4 Pro 输出断续根因=thinking 逐 token 流式透传（实测 max_tokens=30 时 content 空/思考占满）；api_gateway.py 新增 _strip_reasoning_json + _SseReasoningStripper（SSE 逐行剥离，跨 chunk 容错），重启后实测 SSE 已无 reasoning_content。（2026-08-30）
- **[S-20260830-06]** CC Switch 直连渠道：provider「火山方舟 Coding」=Anthropic 端点 /api/coding + coding 专用 key（与模型服务 key 不同）+ 3 模型，apiFormat=anthropic，已写入 cc-switch.db（重启 CC Switch 生效）。（2026-08-30）
- **[S-20260830-05]** 火山方舟 Coding Plan Pro 套餐（49.9元/月）接入网关：OpenAI 兼容端点 https://ark.cn-beijing.volces.com/api/coding/v3（⚠️勿用 /api/v3 会额外扣费），unified 组 coding-plan，实测转发成功（deepseek-v4-flash→GA 正式版）。（2026-08-30）
- **[S-20260830-04]** B 类程序委派验证通过：Qoder CLI 分析脚本 / Trae 写码并存文件 / 豆包问答。（2026-08-30）

## 卡点
- 无。

## 下一步
- 无。
