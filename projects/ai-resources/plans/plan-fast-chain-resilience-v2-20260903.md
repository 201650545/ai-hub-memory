# RFC v2: fast 链抗脆弱性方案（2026-09-03 上线前评审）

> **Status**: proposed（v2 草稿，待 GPT 镜像版评审 + 郭老师拍板）
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

## 推荐的最小可行方案（v2 草稿）

**A + B 组合**：
- 保留 v2 8 渠道顺序
- **新增** sensetime 首位（如果 7890 挂测出可用，再确认推广）
- 文档化脆弱场景到 TOOLS.md §4.6
- 上 cherry studio 真实聊天回归（验证 T-05）

**否决方案 C/D/E**：
- C 语义风险 > 收益
- D 改客户端成本 > 收益
- E 本地模型能力不够

## 待 GPT 评审的 3 个问题

1. **A+B 是否合理？** 还有更便宜的 fallback 候选（如 cloudflare llama-3.3-70b、opencode deepseek-v4-flash 付费兜底）？
2. **capability 误标如何自动化检测？** 渠道加进来时自动跑 3 个标准测试（chat/vision/tools）验证实际能力 vs 声明？
3. **OR 4 key 池的弱 provider 限流** 是否有更聪明的 key 调度（如基于 health 状态切池）？

## 关联

- S-20260902-08：v1 siliconflow 兜底作废
- S-20260902-09：fast 链 v2 已上线
- T-20260902-08：v1 RFC 文档保留作历史
- T-20260903-01~05：STATE.md 新增漏项
