# RFC v2: fast 链抗脆弱性方案（2026-09-03 上线前评审）

> **Status**: finalized（已收 GPT 镜像版评审答复 2026-09-03，见 §GPT 评审裁决；执行方案=A+B′+F+G，F/G=P0）
> **Author**: 调度大脑（Claude）
> **Created**: 2026-09-03
> **Related**: S-20260902-08（v1 siliconflow 兜底被郭老师撤回）、S-20260902-09（fast 链 v2 改造已上线）、T-20260902-08（v1 RFC 文档）

## 背景

`D:\项目\services\search_gateway` 网关（:3100）暴露 5 个 unified 模型名（fast / deepseek-free / high-free / glm-5.3-flash / deepseek-v4-flash），每条链路由多个渠道按顺序 fallback。**fast 链 9-2 已完成 v2 改造**：从 6 渠道（xiaohongshu→groq→agnes→openrouter→zenmux→sensetime）扩到 8 渠道（xiaohongshu→gmi(M3)→mistral→openrouter(cohere)→groq→longcat→zenmux→sensetime），踢掉 agnes（SSL EOF 100% 复现，上游证书废）。

**遗留问题**：fast 链改造**只解决了"加模型+提速"**，**没解决"上游全挂时怎么办"**。v1 siliconflow 兜底方案（S-20260902-08）被郭老师撤回，作废原因："硅基流动兜不了底就不要它了"——siliconflow 充值档速度慢、且实测发现"7890 代理挂时硅基也救不了"。

## 实际观察的脆弱点

**1. 7890 代理挂（v1 RFC 已记录）**
- 9-2 fast 链周末"罢工"统计：326 条全 resolved，无一真正罢工；但 fc=9（fallback 9 次）出现 3 次，根因=7890 代理当时挂 → DEFAULT_CHAIN 兜底 → 走超时 fallback 30s+
- 修法=绕 7890 走直连，但 siliconflow 直连不稳

**2. 上游能力误标 → cherry studio 工具调用全废（S-20260902-07 已修）**
- xiaohongshu/dots3-note-prev 误标 tools=True，实际不支持 OpenAI tools 协议
- 修法=capability 改 false + capability_mismatch 跳过
- **风险**：未来新加渠道可能再次误标 capability，导致 cherry studio 工具调用又崩

**3. gmi M3 直连 403/1010（v2 新发现）**
- gmi M3 是 9-6 截止限免主力，必须走 :3100 网关（带 7890 代理）才能用
- 7890 挂时 gmi 也连带死
- 修法=内部 fallback 到 mistral/or/cohere，但这些也都走 7890

**4. OR 4 key 池部分 provider 弱（v2 实测）**
- 主 key + 3 pool = 4 key 轮询
- K2 池（pool[1]）命中多个 429（z-ai/glm-5.2、google/gemma-4、poolside/laguna）
- 不是 key 配额问题，是 provider 端限流
- 修法=OR 主走 K1（主 key 稳），K2/K3 作 fallback

**5. capability 误标已修，但未做回归测试**
- cherry studio 真实聊天 high-free 模型**还没实测过**（T-20260903-05 漏项）
- harness e2e 也未做（T-20260903-04 漏项）

## v2 候选方案（待 GPT 评审）

### 方案 A：现状（已上线）+ 文档化脆弱性
- fast 链 8 渠道顺序不动
- 接受 7890 挂时 fallback 慢（30s+）
- 仅做 SRE 监控 + 告警
- **优点**：零成本，简单
- **缺点**：郭老师 9-2 已说"接受慢"是兜底候选但没拍

### 方案 B：sensetime 移到首位
- sensetime/sensenova-6.8-flash-lite 直连可用，**不走 7890**
- 速度 1-3s，能力 < agnes-2.5-flash（但 v2 已加 gmi M3 主力兜底）
- 7890 挂时首位 sensetime 直连救场
- **优点**：唯一不依赖 7890 的渠道，0 额外成本
- **缺点**：能力比 agnes 弱，郭老师初筛标准不符

### 方案 C：本地缓存上一个成功回复（同类 prompt）
- :3100 内存里加 LRU（最近 100 个 prompt → response）
- fast 链全挂时返缓存
- **优点**：彻底解决 0 渠道可用场景
- **缺点**：语义不一致风险大；prompt 相似度判定复杂；多用户场景不适用

### 方案 D：失败时返 error + 友好降级到 /v1/chat/completions 直连
- 7890 挂时 :3100 不返回 502，而是告诉 cherry "请用 deepseek-v4-flash 链"
- 客户端需支持链切换
- **优点**：用户体验好
- **缺点**：需要 cherry studio 配合改，破坏 OpenAI 协议

### 方案 E：增加一台"冷备份"本地模型（llama.cpp / ollama）
- 本机 7B/13B 模型兜底
- **优点**：永不依赖外网
- **缺点**：本机显卡 8GB 显存紧张；郭老师 9-2 否决 siliconflow 原因是"快不够"——本地 7B 不可能快

## GPT 评审裁决（2026-09-03 收答复，7930 字）

> **结论**：不建议静态 A+B 收口。应为 **A + B′（sensetime 动态直连热备，非常态首位）+ F（故障域熔断/健康路由）+ G（capability contract test）**，其中 **F 应为 P0**——真正的 SPOF 不是单个模型渠道，而是 **7890 这个共享 egress failure domain**。
>
> **完整回复**：`D:\项目\logs\gpt_rfc_reply_20260903.md`；镜像站对话「㊽ 评审 Fast 链方案」。

| 优先级 | 方案 | 建议 | 理由 |
|---|---|---|---|
| P0 | 按故障域熔断（整组跳过），不逐渠道 fallback | 必做 | 7890 挂时应一次判断整组跳过，而非让 7 渠道依次超时 |
| P0 | capability 自动 contract test + fail-closed | 必做 | capability 误标比普通 5xx 更危险=「假健康」 |
| P1 | sensetime 动态升权（非常态首位） | 做 | 正常保高质量渠道优先；代理故障时 sensetime 立即变 #1 |
| P1 | 独立直连 Cloudflare Workers AI 热备 | 推荐 | 多一独立故障域，有比 llama-3.3-70B 更合适的免费额度模型 |
| P1 | route/channel circuit breaker + deadline budget | 必做 | 消灭 30s+ 串行死亡链 |
| P2 | 延迟 hedging / selective racing | 有条件做 | 解决尾延迟，不能无脑全量双发 |

## 定稿执行方案（替代原 A+B 草稿）

目标收敛为 4 个执行项：
1. **[P0] F·故障域熔断**：识别 7890 共享故障域，健康探测 -> 整组短路跳过，熔断阈值+短路恢复（消灭 30s+ 串行死亡链）。
2. **[P0] G·capability contract test**：渠道注册时自动跑 chat/vision/tools 三测验证声明 vs 实际，fail-closed（防「假健康」重演）。
3. **[P1] B′·sensetime 动态升权**：正常时保现有高质量渠道首位；7890 故障探测触发 sensetime 升 #1，恢复后回落。
4. **[P1] Cloudflare Workers AI 直连热备**：接入一个不依赖 7890 的免费额度独立故障域。

原方案 B（sensetime 常态首位）**否决常态**：能力弱于 agnes/M3，仅作故障态热备。
C/D/E 维持否决（C 语义风险、D 破 OpenAI 协议、E 本地能力不足）。

待办：**P0 两项已落地（2026-09-03）**：F 新增 `fault_domains.py`（proxy 域反应式熔断 + `request_deadline_s=30` 封死链；配置 `data/search_gateway/fault_domains.json`）注入 `api_gateway.py:route_completion`；G 新增 `capability_verify.py`（chat/vision/tools 三测 + fail-closed 写回 `model_capabilities.json`），`save_custom_channel` 注册后异步触发。E2E 验证过：转发放通无回归、死渠道注册被 chat:false 隔离、假 tools 渠道被 `check_candidate` 排除。**P1 B′ 已落地（同日）**：`fault_domains.promote_on_proxy_down(chain)`（`any_proxy_tripped` 时把 `promote_channels` 里的**直连**渠道升链首，恢复按实时 trip 自动回落；`fault_domains.json` 的 `promote_channels=["sensetime","cloudflare"]`）注入 `route_completion` 链构建后。进程内验证：正常态零改动、熔断时 sensetime 升 #1、恢复回落、代理渠道不升权。**P1 Cloudflare 直连热备仅剩凭据**：网关侧机制已就位——CF 用既有 POST /api/channels 注册为**无 proxy** 直连自定义渠道即自动成独立故障域，命名为 `cloudflare` 自动纳入热备；只差郭老师填 Workers AI 账号/Worker endpoint/key，注册模板见下。

## Cloudflare Workers AI 直连热备（P1）— 填凭据即激活

机制已由 B′ 覆盖：无 proxy 直连渠道=独立故障域；`promote_channels` 里列了 `cloudflare`，注册即自动纳入 7890 挂时的热备升权。只差一步——郭老师有 Workers AI 账号后，用既有 `POST /api/channels` 注册该自定义渠道（id 命名 `cloudflare`），definition 填以下字段即可（其余栏位照抄 sensetime）：

```json
{
  "id": "cloudflare",
  "name": "Cloudflare Workers AI 直连",
  "provider": "Cloudflare Workers AI",
  "billing_type": "free_quota",
  "billing_tag": "🟢 免费额度",
  "icon": "/img/brand/cloudflare.png",
  "base_url": "https://<你的-worker域名>.workers.dev/v1",
  "env_key": "CLOUDFLARE_AI_TOKEN",
  "api_format": "openai",
  "proxy": "",
  "free": true,
  "speed": "medium",
  "default_model": "<Worker 里 OpenAI 兼容路由映射的模型名>",
  "models": ["<Worker 里映射的模型名>"]
}
```

要点：`proxy` 留空（关键——否则又回 7890 死亡域）；`base_url` 指到你的 OpenAI 兼容 Worker（暴露 `/v1/chat/completions`）；key 走网关 `env_key` 机制。注册后 G 会自动跑 capability 三测并 fail-closed，确认真活才进链。模型建议选免费额度下比 llama-3.3-70B 更合适的（GPT 评审提示）。

## 评审 3 问均已答复（2026-09-03 收）

1. **A+B 是否合理 / 有更优 fallback？** → 否决静态 A+B，改 A+B′+F+G；F 按故障域熔断为 P0；Cloudflare Workers AI 作独立直连热备（P1）。
2. **capability 误标如何自动化检测？** → G：渠道注册时自动跑 chat/vision/tools 三测 + fail-closed（P0）。
3. **OR 4 key 弱 provider 限流调度？** → 归属延迟 hedging/health 切池（P2 有条件做），优先补齐被动快速落点（优先落地 P0 两项）。

## 关联

- S-20260902-08：v1 siliconflow 兜底作废
- S-20260902-09：fast 链 v2 已上线
- T-20260902-08：v1 RFC 文档保留作历史
- T-20260903-01~05：STATE.md 新增漏项
