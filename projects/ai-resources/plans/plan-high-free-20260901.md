# High Free 方案 v1（郭老师 2026-09-01 拍板）

## 1. 背景与目标

- `deepseek-free` 链 = "免费 + 响应快"，已用 8 渠道串联（gmi→nvidia→bai→sensetime→openrouter→modelscope→siliconflow→opencode，2026-08-31 S-20260831-03 决策把 opencode 挪到链尾做付费垫底）。
- 用户新决策：**新建 `high-free` 链**，定位"免费 + 能力强"——筛选门槛 = **模型能力 ≥ MiniMax M3**（"推理主力/1M 上下文/多模态"，GMI Cloud promo 描述）。
- 与 deepseek-free 解耦：两链目标不同，混用会导致"何时优先"的政治问题。

## 2. 筛选基线（≥ MiniMax M3）

MiniMax M3 描述 = **"推理主力 / 1M 上下文 / 多模态"**。由此推导 High Free 入链门槛（4 条全满足）：

| # | 门槛 | 排除项 |
|---|---|---|
| 1 | 上下文 ≥ 128K | 8K/16K/32K 的"轻量小模型" |
| 2 | 推理等级 = 旗舰/主力/Pro/Max/Ultra | lite / flash / tiny / nano / mini / small / 8b/3b/2.5b |
| 3 | 多模态/工具/推理至少一项 ≥ M3 | 纯文本迷你模型 |
| 4 | 价格 = 0（class=free，含 quota+account_bound 7 天窗口） | 任何 class=paid/unknown |

> 例外：`flash-next` 类专攻低延迟/高并发的旗舰档可入（如 Qwen3.8-Flash-Next，定位"next" 级别不是"lite"）。
> 例外：模型名带 `-it` 的指令微调版（gemma-4-31b-it）= 同款基础模型指令优化版，可入。

## 3. 候选清单（按当前 `channel_models.json` 渠道×模型 拉表）

| # | 渠道 | 模型 | 上下文 | 等级 | 多模态 | 价格 | 评 |
|---|---|---|---|---|---|---|---|
| 1 | modelscope | deepseek-ai/DeepSeek-V4-Pro-0813 | 128K | Pro | 文本 | free(积分) | ✅ |
| 2 | openrouter | nvidia/nemotron-3-ultra-550b-a55b:free | 1M | Ultra | 文本 | free | ✅ |
| 3 | openrouter | nvidia/nemotron-3.5-lightning:free | 1M | Lightning | 文本 | free | ✅ |
| 4 | openrouter | thinkingmachines/inkling:free | 待查 | 主力 | 文本 | free | ⚠️ 需验 |
| 5 | openrouter | poolside/laguna-s-2.1:free | 待查 | S 级 | 文本 | free | ⚠️ 需验 |
| 6 | openrouter | inclusionai/ling-3.0-flash-fin:free | 待查 | Flash | 文本 | free | ⚠️ 需验 |
| 7 | openrouter | minimax/minimax-m3:free | 1M | 主力 | 多模态 | free | ✅（基线） |
| 8 | openrouter | google/gemma-4-31b-it:free | 待查 | 31B-it | 文本 | free | ⚠️ 需验 |
| 9 | gmi | MiniMaxAI/MiniMax-M3 | 1M | 主力 | 多模态 | free(9/6 止) | ✅（基线） |
| 10 | ark-coding | deepseek-v4-pro-ga-260813 | 128K | Pro | 文本 | subscription | ❌ paid chain 不入 free 链 |
| 11 | ark-coding | glm-5.3-flash | 128K | Flash | 文本 | subscription | ❌ 等级 flash 但已订阅定位不入 free |
| 12 | sensetime | deepseek-v4-flash | 128K | Flash | 文本 | free(限免) | ❌ 等级=flash 不入 |
| 13 | opencode | deepseek-v4-flash | 128K | Flash | 文本 | paid | ❌ |
| 14 | opencode | glm-5.3-flash | 128K | Flash | 文本 | paid | ❌ |
| 15 | bai | deepseek-v4-flash | 128K | Flash | 文本 | free(限免) | ❌ flash |
| 16 | bai | deepseek-v4-flash-vision-exp | 128K | Flash-Exp | 视觉 | free(限免) | ❌ flash 不入（但 vision 加分可复议） |
| 17 | nvidia | deepseek-ai/deepseek-v4-flash-0731 | 128K | Flash | 文本 | free | ❌ flash |
| 18 | longcat | LongCat-2.0 | 128K | 主力 | 文本 | free(每日重置) | ✅ |
| 19 | mistral | mistral-large-2512 / mistral-large-latest | 128K | Large | 文本 | free(1B/月) | ✅ |
| 20 | mistral | codestral-2508 / codestral-latest | 256K | Codestral | 文本 | free(1B/月) | ✅（代码专精，定位与 high-free 互补） |
| 21 | zenmux | inclusionai/ling-3.0-tiny | 待查 | Tiny | 文本 | free | ❌ tiny |
| 22 | zenmux | z-ai/glm-4.7-flash-free | 待查 | Flash | 文本 | free | ❌ flash |
| 23 | xiaohongshu | dots3-note-prev | 待查 | 主力 | 文本 | free(内测) | ⚠️ 需验 |
| 24 | groq | qwen/qwen3.8-27b | 待查 | 27B | 文本 | free(限速) | ⚠️ 等级=27B 算主力可入 |
| 25 | agnes | agnes-2.5-flash | 待查 | 2.5-Flash | 文本+图 | free | ❌ flash 不入 |
| 26 | cloudflare | @cf/meta/llama-3.3-70b-instruct-fp8-fast | 128K | 70B | 文本 | free(10K n/天) | ✅（70B 主力档） |
| 27 | cloudflare | @cf/zai-org/glm-4.7-flash | 待查 | Flash | 文本 | free | ❌ flash |
| 28 | cloudflare | @cf/ibm-granite/granite-4.0-h-micro | 待查 | Micro | 文本 | free | ❌ micro |
| 29 | siliconflow | deepseek-ai/DeepSeek-V3.2 | 128K | V3.2 | 文本 | free(额度) | ✅（deepseek-V3 系列不算 flash） |
| 30 | siliconflow | deepseek-ai/DeepSeek-V3.1-Terminus | 128K | V3.1 | 文本 | free(额度) | ✅ |
| 31 | siliconflow | deepseek-ai/DeepSeek-R1 | 128K | R1-Reasoning | 文本 | free(额度) | ✅（推理专精） |

**新加候选（来自 OpenRouter 自拉 /api/v1/models 走 7890 代理 0 价 18 款筛 7 款）**：
| # | 渠道 | 模型 | 上下文 | 等级 | 多模态 | 价格 | 评 |
|---|---|---|---|---|---|---|---|
| 32 | openrouter | google/gemma-4-26b-a4b:free | 待查 | 26B-MoE | 文本 | free | ⚠️ 26B 算主力可入 |
| 33 | openrouter | liquid/lfm-2.5-2.6b:free | 待查 | 2.6B | 文本 | free | ❌ 2.6B 太小不入 |
| 34 | openrouter | minimax/minimax-m2.7:free | 1M | M2.7 | 多模态 | free | ✅（M3 兄弟） |
| 35 | openrouter | minimax/minimax-m3:free | 1M | 主力 | 多模态 | free | ✅（已列=7） |
| 36 | openrouter | nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free | 待查 | 30B-A3B-Reasoning | 多模态 | free | ✅（30B 推理+多模态+推理专精） |
| 37 | openrouter | nvidia/nemotron-3-super-120b-a12b:free | 待查 | 120B | 文本 | free | ✅（120B 超大主力） |
| 38 | openrouter | z-ai/glm-5.2:free | 128K | 5.2 主力 | 文本 | free | ✅ |

## 4. high-free 链建议（待用户拍板）

```json
"high-free": {
  "order": [
    "gmi",                // MiniMaxAI/MiniMax-M3（基线·9/6 到期前首位）
    "openrouter",         // 7 款 0 价主力（nemotron-ultra/minimax-m3/...）
    "modelscope",         // DeepSeek-V4-Pro 积分
    "longcat",            // LongCat-2.0 每日重置
    "mistral",            // mistral-large/codestral 1B/月
    "cloudflare",         // llama-3.3-70b 10K n/天
    "siliconflow",        // DeepSeek-V3.2/V3.1/R1 额度
    "groq"                // qwen3.8-27b 限速兜底
  ],
  "disabled": ["ark", "ark-coding", "opencode"]
}
```

**为什么不放 ark-coding**：用户 08-30 把 coding 套餐从 deepseek-free 摘出来（避免烧订阅），high-free 也照此执行。

**为什么不放 bai/sensetime/nvidia**：`flash` 等级被基线排除；其中 bai-vision-exp 可复议（vlm 强但仍是 flash）。

**为什么不放 agnes**：2.5-flash 等级不够；agnes 在 fast 链已经定位"快速补充"。

## 5. 与 fast 链的关系

- `fast` 链定位 = 快（Dots3→Groq→Agnes→OpenRouter Dots3→ZenMux→Sensetime）。
- `deepseek-free` 链 = 免费 + 主流推理（不挑能力）。
- `high-free` 链 = 免费 + 强能力（≥ M3）。
- 三链目标正交，selector 同名"deepseek-free"/"high-free"/"fast"各走各的，不重叠。

## 6. 执行清单（谁做什么）

- [ ] **方案作者**（Claude 本轮）：写本方案 v1
- [ ] **评估者**（WorkBuddy / hy4-preview）：逐条校验 §3 候选（上下文/等级/多模态）并标 ⚠️→✅/❌
- [ ] **写代码者**（Claude 待命）：改 `routing.json` + `unified_models.json` + `channel_models.json` + `model_pricing.json`
- [ ] **验收**（郭老师）：重启网关、跑 A 级免费任务验 `high-free` selector 真落到 Pro/Ultra 模型

## 7. 风险与回退

1. **9/6 后 gmi 失效**：届时 `high-free` 第一位应自动转给 `openrouter` minimax-m3:free，已在 order 排第 2 自然承接。
2. **RPS/RPM 限速**：长链多渠道，selector 失败自动跳下一位（同 deepseek-free 现有机制）。
3. **M3 限免变收费**：gmi 在 promos 状态变化时 class 会从 free→unknown，enforce 后自动落拦截侧，需重排。
4. **回退**：routing.json 改前必备份为 `_routing_backup_<date>_b4highfree.json`，按 S-20260831-03 决策保留 _bak 习惯。

## 8. 待决项（拍板后写 CHANGELOG）

- [ ] §3 候选哪些入 high-free
- [ ] §4 order 顺序是否同意
- [ ] 是否同步在 selector 名称上加 `high-free`，让 Cherry Studio / DSH 自动同步（依赖 channels.py 模型自动拉取）
- [ ] high-free 链 disabled 名单：ark / ark-coding / opencode（建议）还是更严

## 附：当前 deepseek-free 链（基线对照）

```json
"deepseek-free": {
  "order": ["gmi", "nvidia", "b ai", "sensetime", "openrouter", "modelscope", "siliconflow", "opencode"],
  "disabled": ["ark"]
}
```
