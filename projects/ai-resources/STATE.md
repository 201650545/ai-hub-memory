# STATE.md — AI资源实测 项目状态

## 进行中
- 无。

## 卡点（漏项 — 2026-09-03 郭老师指出）
- **T-20260903-01 漏项：问 GPT 镜像版关于"反贷（兜底/fallback）"的事**（2026-09-03，郭老师拍桌）。本轮 fast 链 v2 改造（S-20260902-09）**没有按郭老师原话先问 GPT 镜像版**确认 fast 链 fallback 抗脆弱性方案就直接加模型上线。**待办**：写一段方案 v2（含 7890 代理脆弱性、OR cohere 实际限流测试、Qwen3-235B 已下线等 9-2/9-3 新事实）发给 GPT 镜像版（chatgpt.com / chat.openai.com 镜像）问优化建议——尤其"fast 链遇到上游全挂（gfw/7890/dns）时降级策略"是否合理。已查过反馈记录 `feedback_mirror_chat_history.md`、`workflow_gpt_repo_sync.md`（问 GPT 三步：让它读 GitHub、push 上下文、精简提示词）。注意：用户镜像站聊天历史 ≤30 条，到 30 删一半。
- **T-20260903-02 漏项：fast 链抗脆弱性方案未独立成 RFC**（承接 S-20260902-08 郭老师撤回 siliconflow 兜底后留下的"真问题"）。S-20260902-08 末尾已记"fast 链抗脆弱性方案待重新设计（候选：拉长 zenmux 健康间隔、sensenova 首位、接受慢）"，但 v2 改造只解决了"加新模型+提速"，**没解决"上游全挂时怎么办"**。候选：①把 sensetime 移到首位（sensenova-6.8-flash-lite 直连可用，但能力 < agnes，郭老师标准不符）；②本地缓存上一个成功回复（同类 prompt）；③接受慢（30s+ fallback）。**待办**：写 RFC v2 发 GPT 镜像版征求意见。
- **T-20260903-03 漏项：v2.8 汇报中模块×验收项/变更清单/验证/已知偏差的规范没自动校验**（2026-09-02 郭老师 v2.8 汇报后我没自动对照 TOOLS.md §4.5 的汇报模板生成校验报告，CHANGELOG S-20260902-**没记这条 v2.8 汇报的接收与归档**）。**待办**：补一条 S-20260902-10 = v2.8 汇报接收 + 归档 + 与 TOOLS.md §4.5 对照检查。
- **T-20260903-04 漏项：S-20260902-06 后续 e2e 验证未做**（harness ai-resource-hub 真请求 + X-Routed-Channel 头验证）。TRAE 汇报"按约定明日再验"，明天=今天（9-3），我未派发。**待办**：派 TRAE SOLO CN（DeepSeek V4 Flash 正式版）跑 e2e：启 :3100、注册 aiResourceHub profile、model=high-free 调一次、验证响应头含 X-Routed-Channel 字段。
- **T-20260903-05 漏项：cherry studio e2e 实测 harness ai-resource-hub 真实请求**（同 T-04 但走 cherry 客户端）。CHANGELOG S-20260902-06 末尾"已知偏差 e2e 按约定明日再验"今日到期。**待办**：同上 e2e，验证 high-free 模型走 cherry studio 真实聊天能通。

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
