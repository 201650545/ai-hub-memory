# AI 资源台账

> ⚠️ **R3 指针化（2026-08-14 GLM 审查落地）**：本文件的额度/余额等**高时效数值**已不是真源——精确数值请查 **ai-resource-hub**（资源真源 + 飞书表 + scheduler/credentials.json 信任平面）。本文件只保留：平台清单、结论级判断（有无/够用/弃用）、登录态、最后核实日期。额度具体数字随时间变化，**以 ai-resource-hub 为准**。
>
> 生成：2026-08-13 ｜ 调查方式：分类交互式提问（10 类框架）+ 既有线索核验
> 数据来源：① 本轮用户确认（2026-08-13）② ai-resource-hub 验证记录《docs/资源调研/验证记录_2026-08-10.md》③ 飞书 AI 自助资源库 6 表（表1 账号资产汇总已回写 21 条）
> 凭证纪律：**全程未触碰/未记录任何 API key / token / 密码值**（凭证仅存在于本地 `D:\项目\ai-resource-hub\scheduler\credentials.json`）
> 标注规则：「已核实」= 实测确认；「待核实」= 未实测/未复测，**未编造任何数值**

---

## 类1 · API 账户（直连 API key）— 21 个平台（源自验证记录，已核实登录态）

### SiliconFlow 硅基流动
- 平台：cloud.siliconflow.cn ｜ 模型：DeepSeek 系 / Qwen3-Omni-Captioner / Qwen-Image（2 个限免）
- 额度：余额 **¥-0.1083（负余额已透支）**，代金券 1 张（详情待核实）；免费 token 疑似耗尽
- 访问：API key ×3（值不记录）｜ 用途：通用/生图 API 兜底
- 待确认：代金券详情、负余额是否影响限免模型调用

### DeepSeek
- 平台：platform.deepseek.com ｜ 模型：deepseek-v4-flash（主力）、deepseek-v4-pro
- 额度：余额 **¥26.59**（已核实）；近 30 天用量 12.19 亿 token，充值制
- 访问：API key 在用 ｜ 用途：AI Hub 网关主力 + 通用
- 待确认：无（余额清晰）

### 火山引擎 Ark — 🚫 弃用（用户 2026-08-13 拍板）
- 平台：console.volcengine.com/ark ｜ 模型：豆包 / DeepSeek 等（部分适用免费档）
- 额度：每日 200 万 token 免费档（未实测）；**用户决定：不充 API、不买 Token 套餐，不再维护**
- 状态：⚠️ opencli 实测未登录；弃用后无需登录核实

### 阿里云百炼 — 🚫 弃用（用户 2026-08-13 拍板）
- 平台：bailian.console.aliyun.com ｜ 模型：Qwen 全系
- 额度：新户 7000 万 token / 180 天（未实测）；**用户决定：不充 API、不买 Token 套餐，不再维护**
- 状态：⚠️ opencli 实测未登录；弃用后无需登录核实

### Groq
- 平台：console.groq.com ｜ 模型：llama-3.3-70b / gpt-oss / qwen3.6-27b / whisper / orpheus 等全系
- 额度：**Base 免费档**：Chat 30 RPM / 1K RPD（各模型具体 TPM 已实测）；STT 20 RPM；TTS 10 RPM（已核实）
- 访问：API（OpenAI 兼容）｜ 用途：推理/语音/翻译（免费高速）
- 待确认：API key 是否存在（未进密钥页）

### ModelScope 魔搭
- 平台：modelscope.cn ｜ 模型：开源模型推理社区
- 额度：**每日 250 魔粒**（签到自动化已上线，每日运行）
- 访问：网页 + API ｜ 用途：开源模型体验/推理
- 待确认：魔粒消耗规则

### 智谱 BigModel
- 平台：open.bigmodel.cn ｜ 模型：GLM-4-Flash（永久免费）、GLM-5.2 旗舰
- 额度：⚠️ **2026-08-13 opencli 实测：无任何生效资源包**——付费「1 万亿 GLM-4.5 包」（2025-09-02 到期）+ 全部赠送包（实名 500 万 / 新户 100 次视频图片 / 200 万通用 / 200 万 GLM-4.5 / 600 万 GLM-4.1V / 1000 万 GLM-4.5-Air，均 2025-07~10 到期）**全部已失效**；仅 GLM-4-Flash 永久免费模型仍可用；财务：充值 ¥50、可用余额 ¥0
- 访问：API key ×3（值不记录）｜ 用途：通用/中文
- 待确认：⚠️ 需绑定手机号；如需付费额度走资源包购买

### Kimi / Moonshot
- 平台：platform.kimi.com（已从 moonshot.cn 迁新域名）｜ 模型：Kimi 系（含 K3 旗舰）
- 额度：**可用余额 ¥15.00（赠送奖励金）**（2026-08-13 opencli 实测）；今日/总消费 ¥0；⚠️ 奖励金不能用于 Kimi K3 模型，需充值解锁
- 访问：✅ **已登录**（opencli 实测）｜ 用途：长文本；**问诊兜底渠道**（D-GLOBAL-20260815-04：GPT 镜像站不可用时转 Kimi K3）
- 问诊操作：opencli 打开 kimi.com 官网，提问前开启 **K3 思考进阶模式**
- 待确认：API key 是否存在

### OpenRouter
- 平台：openrouter.ai ｜ 模型：**14 个 :free 免费模型**（402 库中）+ 400+ 付费模型聚合
- 额度：`:free` 不消耗余额（已核实）；**TOTAL AVAILABLE 余额数字未渲染**（2026-08-13 opencli 复测仍为空，SPA 异步问题）；近期交易 2 笔共 $14.20（Jun 7：$5.00 + $9.20）
- 访问：API key ×7（值不记录）｜ 用途：海外模型中转（免费主力）
- 待确认：Total available 余额具体数值（SPA 未渲染）

### HuggingFace
- 平台：huggingface.co（账号 GuoyT）｜ 模型：数百开源模型 Inference Providers 免费推理
- 额度：**慷慨免费档**（generous free tier，已核实政策）
- 访问：⚠️ Access Token 需人工通过 security-checkup 后创建 ｜ 用途：开源模型/推理
- 待确认：token 创建

### GitHub Models — ❌ 已退役
- 状态：**2026-07-30 官方完全退役**（playground/推理 API/BYOK 全关）
- 替代：Azure AI Foundry / GitHub Copilot

### Google Colab
- 平台：colab.research.google.com ｜ 交互式计算（非模型 API）
- 额度：免费 tier（usage limit 未实测）
- 待确认：Runtime GPU/TPU 型号需人工探测

### Together.ai — ⚠️ 无免费额度
- 状态：已登录但 $0.00，**read-only 模式，需充值 ≥$5 解锁**；归付费候选

### Mistral
- 平台：console.mistral.ai（Free 计划）｜ 模型：Mistral 全系
- 额度：**$10/月 API + $10/月 Vibe Code，21 天周期重置**（已核实；当前周期剩余 21 天）
- 待确认：API key 未创建（可选）

### 百度智能云千帆 — 🚫 弃用（用户 2026-08-13 拍板）
- 平台：console.bce.baidu.com/qianfan ｜ 模型：ERNIE 4.5T / X1T / DeepSeek 系等 9 款
- 额度：8000 万 Tokens 免费包 + 新人券 ¥1155（至 2026-09-15，未实测）；**用户决定：不充 API、不买 Token 套餐，不再维护**
- 状态：⚠️ opencli 实测未登录；弃用后无需登录核实

### 腾讯混元（旧平台）— ❌ 已退役
- 状态：**2026-09-30 全面停服**，功能迁移 TokenHub；旧 Key 无需维护

### 腾讯 TokenHub — 🚫 弃用（用户 2026-08-13 拍板）
- 平台：console.cloud.tencent.com/tokenhub ｜ 模型：DeepSeek V4 Pro/Flash、GLM-5.2、Kimi K3、MiniMax-M3 等
- 额度：新用户 100 万 Tokens / 90 天（未到账核实）；**用户决定：不充 API、不买 Token 套餐，不再维护**
- 状态：⚠️ opencli 实测未登录（微信扫码）；弃用后无需登录核实

### MiniMax — 🚫 弃用（用户 2026-08-13 拍板）
- 状态：已登录，Token Plan 未订阅、积分余额 0；**用户决定：不买 Token Plan 订阅**；已有订阅 Key（sk-cp 前缀）闲置

### 零一万物 Yi — ❌ 已退役
- 状态：**平台停服**（停止在线体验/API/充值），开放余额退还；有余额按官方指引申请

### 讯飞星火 — 🚫 弃用（用户 2026-08-13 拍板）
- 平台：console.xfyun.cn ｜ 模型：Spark X2 / X2-Flash / Pro / Max / Ultra / Lite
- 额度：余额 ¥0.00、未实名（L0 受限）；**用户决定：不充 API、不买 Token 套餐，不再维护**

### 阶跃星辰 StepFun — 🚫 弃用（用户 2026-08-13 拍板）
- 平台：platform.stepfun.com ｜ 模型：Step 3.7 Flash / 3.5 Flash / Step 2 / Step 1
- 状态：未登录；**用户决定：不充 API、不买 Token 套餐，不再维护**

---

## 类2 · Agent 工具（编程 / 自动化 Agent）— 14 个

### WorkBuddy（本机主要执行 Agent，郭老师口中的 WorkBodySolo）
- 平台：本机 ｜ 模型：内置多模型
- 额度：付费账号（具体额度/积分机制待确认）
- 用途：教学课件、资源调查、多 Agent 体系执行位

### Trae Work（trae work）
- 平台：字节 Trae ｜ 模型：Claude/豆包 系
- 额度：**月 Pro 会员**（已确认）｜ 用途：编程/自动化
- 待确认：会员额度构成

### Codex（OpenAI）
- 平台：OpenAI ｜ 模型：GPT-5 系
- 额度：免费档（已确认）｜ 用途：多 Agent 体系**总指挥**
- 待确认：免费额度轮次规则

### Claude Code
- 额度：⚠️ **已用光**（2026-08-15 用户确认）；问诊/编程兜底不再走 Claude（改 Kimi K3，D-GLOBAL-20260815-04）｜ 用途：编程 Agent
- 待确认：登录通道（Claude 订阅？）

### Cursor / Windsurf
- 额度：免费档（已确认）｜ 用途：IDE 编程 Agent

### Trae（国内版）/ Qoder（qcoder.cn）
- 额度：免费档（已确认）｜ 用途：编程 IDE/Agent

### Kimi Code / QClaw / autoclaw
- 额度：免费档（已确认）｜ 用途：编程/自动化 Agent

### OpenCode Go（付费套餐，非免费档）
- 平台：opencode.ai ｜ 模型：多模型
- 额度：付费订阅约 $60/30 天，**滚动 5 小时 / 周 / 月 三窗口**（非每日刷新、会过期）
- 访问：网页版（无官方 API，额度需抓工作区页面）
- 用途：编程 Agent
- 待确认：当前订阅周期剩余额度

### Cline（免费档）
- 额度：免费档 ｜ 用途：开源 CLI 编程 Agent

### Cherry Studio
- 额度：免费（客户端）｜ 用途：**网关聚合客户端**（多 API 统一入口）

---

## 类3 · 购买的套餐 / 镜像站 — 2 个

### AI问答宝（Plus 多卡，已核实 2026-08-13）
- 平台：ai.wendabao.net（现跳 ai.wendabao-f.net）｜ 类型：套餐/镜像
- 额度：Plus 多卡共享；会员有效期至 **2026-10-28**
- 账号卡：GPT-5 ⑫/⑨/⑰ 等活跃卡 + 一批「受限」卡（受限时点右上角切换账号）
- 访问：opencli 连日常 Chrome
- 用途：ChatGPT Plus / Claude / DeepSeek R1 / Gemini / Grok 等镜像

### 67673 类中转站（历史线索）
- 类型：OpenAI 兼容中转 ｜ 状态：**待确认**（记忆线索，未获当前有效性确认，暂不计入可用资源）

---

## 类4 · 网页版 AI 产品 — 10 个（全部在用，免费档）

| 资源 | 厂商 | 额度 | 用途 |
|---|---|---|---|
| Kimi 网页版 | 月之暗面 | 免费档 | 长文本/文档 |
| 豆包 网页版 | 字节 | 免费档 | 通用/对话 |
| 腾讯元宝 | 腾讯 | 免费档 | 通用/联网 |
| ChatGPT web | OpenAI | 免费档（镜像站另有 Plus 多卡） | 海外最强通用 |
| Claude web | Anthropic | ⚠️ 已用光（2026-08-15） | 写作/编程（兜底改 Kimi K3） |
| 智谱清言 | 智谱 | 免费档 | 通用/中文 |
| 文心一言 | 百度 | 免费档 | 通用/中文 |
| 通义千问 | 阿里 | 免费档 | 通用/中文 |
| Gemini | Google | 免费档 | 海外通用 |
| Grok | xAI | 免费档 | 海外通用/联网 |

---

## 类5 · 生图 / 视频 / 多模态 — 5 个（均无付费额度）

| 资源 | 厂商 | 额度 | 用途 |
|---|---|---|---|
| 即梦 | 字节 | 免费积分 | 生图/视频 |
| 可灵 | 快手 | 免费档 | 视频生成 |
| 海螺 | MiniMax | 免费档 | 视频/多模态 |
| 豆包生图 | 字节 | 随账号免费 | 生图 |
| 智谱生图 | 智谱 | 随账号免费 | 生图 |

> 备注：Midjourney / LibLib **无付费额度**；AI Hub 生图集成（ChatGPT镜像+豆包+千问）为规划中能力，未计入

---

## 类6 · AI 搜索 / 搜索引擎 — 9 个（登录态已全部实测 2026-08-13）

### 独立 AI 搜索网站（4 个，均免费档）

| 资源 | 登录态（opencli 实测） | 额度 | 用途 |
|---|---|---|---|
| Perplexity | ✅ 已登录（有历史会话） | 免费档 | 深度搜索 |
| 秘塔 | ✅ 已登录（有历史记录） | 免费 | 中文搜索 |
| 知乎直答 | ✅ 已登录（有历史记录） | 免费 | 知识问答 |
| 纳米AI搜索 | ⚠️ **未登录**（游客可用，历史不同步） | 免费 | 中文搜索 |

### AI Hub 搜索网关（引擎注册表实测：实际 5 源，非六源）
> 位置：`D:\项目\services\search_gateway\engines.py`（ENGINES 注册表）｜ 实现方式：opencli 操控网页端（非 API）

| 源 | 登录态（opencli 实测） | 引擎 id |
|---|---|---|
| 腾讯元宝 | ✅ 已登录 | yuanbao |
| 字节豆包 | ✅ 已登录 | doubao |
| 月之暗面 Kimi | ✅ 已登录 | kimi |
| 通义千问 | ✅ 已登录 | qianwen |
| Meta AI | ⚠️ **未登录**（Log in 页） | metaai |

> ⚠️ **重要更正**：网关实际注册 **yuanbao/doubao/kimi/qianwen/metaai 五源**——**Perplexity 与 Grok 不在其中**（与「六源并发」描述不符）；Meta AI 未登录，实际可用 4 源。

---

## 类7 · 浏览器自动化 / CLI 工具 — 2 个

### opencli（@jackwener/opencli v1.8.6）
- 平台：本地 daemon + Chrome 扩展 ｜ 能力：桥接本地 Chrome 真实浏览（已登录态复用）
- 额度：免费开源 ｜ 用途：网页验证/自动化操作（SmartEdu 视频、资源调研等）
- 状态：唯一浏览器自动化方案（已确认）

### WorkBuddy 内置浏览器能力
- 能力：agent-browser / playwright 通道 ｜ 额度：内置 ｜ 用途：网页交互/截图

---

## 类8 · 本地模型 / 推理服务 — 无

- 状态：**无本地模型**，全部走云端 API（已确认）

---

## 类9 · 中转 / 代理 — 3 个

### ZSCC（api.zscc.in）
- 平台：api.zscc.in ｜ 模型：压缩模型 **minimax-m3-cc**（已配）；默认模型待定
- 额度：机制待确认 ｜ 用途：API 中转（低成本压缩模型）

### AI Hub 网关
- 平台：AI Hub 项目（D:\项目\ai-hub）｜ 模型：**DeepSeek V4 Flash（0731）+ Gemini 3.6 Flash** 双 API 渠道（中转+额度管理）
- 额度：DeepSeek 走类1余额（¥26.59）；Gemini 走免费 tier（经网关）
- 用途：统一 API 聚合 + 搜索网关（元宝/豆包/Kimi/千问/Meta AI 五源，Perplexity/Grok 未接入）+ 生图集成（规划）

### Cherry Studio 网关
- 平台：Cherry Studio 客户端内置 ｜ 模型：聚合多厂商 API
- 用途：桌面端多模型统一调用

---

## 类10 · 办公 / 集成 / 其他 — 7 个

| 资源 | 用途 | 备注 |
|---|---|---|
| 飞书 | 多维表格（教学制作工作流 / AI 自助资源库 6 表 / 创意游戏点子表）+ Bot「龙虾2号」 | 核心集成 |
| 微信 | 公众号文章搜索技能 / 文章采集 | |
| 企业微信 | 办公通讯 | |
| Telegram | 通讯/机器人 | |
| GitHub | 代码托管 + Pages 公开数据桥（ai-hub、ai-resource-hub、feishu-data-hub 等 5 仓库） | |
| 钉钉 | 办公协作 | |
| Notion | 笔记/知识库 | |

---

## 汇总统计

- **资源总数：约 73 条**（类1:21 平台（其中 7 个已弃用）/ 类2:14 工具 / 类3:2 / 类4:10 网页版 / 类5:5 生图 / 类6:9 搜索 / 类7:2 自动化 / 类8:0 / 类9:3 中转 / 类10:7 集成）
- **额度机制已明确：约 27 条**（DeepSeek ¥26.59、Groq 30RPM、ModelScope 250魔粒/日、Mistral $20/月、OpenRouter 14 free、SiliconFlow 负余额、**智谱无生效资源包（实测）**、**Kimi ¥15 赠送（实测）**、Trae Work Pro 会员、网页版/搜索/生图全免费等）
- **🚫 已弃用（用户 2026-08-13 拍板：不充 API、不买 Token 套餐）：7 个**——火山引擎、阿里百炼、百度千帆、腾讯 TokenHub、MiniMax、讯飞星火、阶跃星辰（原待确认项清零，不再维护）
- **待确认：约 4 项**（AI问答宝详情、67673 有效性、ZSCC 额度机制、OpenRouter 余额数字（SPA 未渲染）；Gemini 网关细节并入 AI Hub）
- **已退役/不可用：4 个**（GitHub Models、腾讯混元旧、零一万物、Together.ai 无免费）

## opencli 网页实测记录（2026-08-13，补充于提问之后）

### 第一轮（API 平台，7 个）
- 抓取：OpenRouter、智谱、火山、阿里百炼、TokenHub、Kimi、百度千帆（串行单会话）
- **状态更新 2 项**：① Kimi 已登录、余额 ¥15 赠送（原「未登录」已修正）；② 智谱资源包全部失效、仅 GLM-4-Flash 永久免费（原「2000 万新户」已修正）
- 未登录 4 项（火山/阿里/TokenHub/百度）→ 用户随后拍板弃用；OpenRouter 余额 SPA 未渲染

### 第二轮（AI 搜索，9 个）
- 抓取：Perplexity、秘塔、知乎直答、纳米AI搜索、元宝、豆包、千问、Meta AI、Grok
- **独立搜索站 4 个**：Perplexity/秘塔/知乎直答 ✅ 已登录；纳米 ⚠️ 未登录
- **AI Hub 网关五源**：元宝/豆包/Kimi/千问 ✅ 已登录；Meta AI ⚠️ 未登录；**更正：网关实际 5 源，不含 Perplexity/Grok**
- Grok 网页空白（加载问题，未确认）
- 全程未触碰任何凭证值

## 关联位置
- 既有飞书台账：AI 自助资源库 Base `StmDbTXQWaujshs9NpIc3UFpnAc`（表1 账号 21 条 / 表2 凭证 5 条 / 表3 能力 21 条 / 表4 实例 21 条）
- 本台账为**横跨 10 类的手头资源总览**，与飞书 API 台账互补（飞书侧重 API 平台，本台账含工具/网页/镜像/集成）

---

## 登录登记表（会调登录的网站 · 2026-08-13 整理）

> 登录方式来源：验证记录「登录方式总览」+ opencli 实测。**密码类一律不代登、不记录密码值**（安全红线）。

### A. 需要登录操作（当前未登录 / 需人工动作）— 4 个

| 网站 | 类型 | 登录方式 | 现状 | 建议 |
|---|---|---|---|---|
| n.cn 纳米AI搜索 | AI 搜索 | 微信/手机 | 未登录（游客可用） | 可选：登录仅同步历史，不登也不影响使用 |
| meta.ai | AI 搜索(网关源) | Meta/Google | 未登录 | **建议不考虑**：价值低，网关可换 Perplexity |
| grok.com | 网页版 AI | Google | 页面空白未确认 | 可选：若常用 Grok 则登 |
| huggingface.co/settings/tokens | API 平台 | 账号密码(已登录) | **security-checkup 拦截** | **必须本人操作**：过安全验证后才能看/建 token（AI 无法代点） |

### B. 已登录、免操作（实测确认）— 15 个

| 网站 | 登录方式 | 备注 |
|---|---|---|
| ChatGPT web | Google | ✅ |
| Claude web | Google | ⚠️ 额度已用光（2026-08-15，不再作问诊兜底） |
| Gemini | Google | ✅ |
| Kimi (kimi.com / platform.kimi.com) | 微信/手机 | ✅ 余额 ¥15 赠送 |
| 腾讯元宝 | 微信/QQ | ✅ 网关源 |
| 字节豆包 | 手机 | ✅ 网关源 |
| 通义千问 | 阿里/手机 | ✅ 网关源 |
| Perplexity | Google | ✅ |
| 秘塔 | 微信/手机 | ✅ |
| 知乎直答 | 知乎 | ✅ |
| OpenRouter | Google/邮箱 | ✅ 14 free 模型 |
| DeepSeek | 手机/邮箱 | ✅ 余额 ¥26.59 |
| Groq | Google | ✅ 免费 Base 档 |
| 智谱 BigModel | 账号密码/手机 | ✅ 已登录（资源包全失效）；⚠️ 可选绑手机 |
| ModelScope 魔搭 | 账号密码 | ✅ 250 魔粒/日 |

### C. 已弃用 / 退役，不登录（用户拍板或官方停服）— 11 个

| 网站 | 原因 |
|---|---|
| 火山引擎 Ark | 🚫 弃用 |
| 阿里云百炼 | 🚫 弃用 |
| 百度智能云千帆 | 🚫 弃用 |
| 腾讯 TokenHub | 🚫 弃用 |
| MiniMax | 🚫 弃用 |
| 讯飞星火 | 🚫 弃用 |
| 阶跃星辰 StepFun | 🚫 弃用 |
| GitHub Models | ❌ 退役 2026-07-30 |
| 腾讯混元旧 | ❌ 退役 2026-09-30 停服 |
| 零一万物 Yi | ❌ 退役停服 |
| Together.ai | ⚠️ 无免费额度需充值，不启用 |

### D. 登录方式待确认 / 不适用 — 4 个

| 网站 | 说明 |
|---|---|
| AI问答宝（镜像） | 登录方式待确认 |
| 67673 中转站 | 有效性未确认 |
| ZSCC api.zscc.in | 页面已开「船仓 API 加油站」，无登录提示（中转面板） |
| Grok | 页面空白，加载/登录方式待确认 |
