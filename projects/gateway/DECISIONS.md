# DECISIONS.md — AI 搜索网关（:3100）项目专属决策（append-only）

> 只放本项目（`D:/项目/ai-hub/search_gateway`）的裁决。跨项目规则在 `global/DECISIONS.md`。
> 每条都写清「谁定的 / 原话或口径 / 落到哪段代码 / 什么时候会失效」，方便后续 Agent 不再问第二遍。

## 2026-09-28
- [D-GW-20260928-01] **席位增 / 删 / 替换 / 调序的日常决策权移交 Agent**（用户 2026-09-28 晚，逐字）：
  「**增删替换永远不是我要做的事情，永远不是我拍板**」「**每天定时定点确定增删替换的事情，是由你去做**」。
  用户保留的是「策略本身」的讨论权（模型更新周期 / 重要节点随机出现）。
  落地：`scripts/auto_orchestrate.py` 每日 12:15 计划任务 `AutoSeatOrchestrate`；
  `services/routes_writer.py` 免审批集合 = `seat_add / seat_reorder / auto_remove_nonzero_price /
  auto_remove_hard_boundary / auto_rollback / speed_line_sync`，且**调用方身份也要对得上**（防冒名）。
- [D-GW-20260928-02] **新的合格免费模型自动接入**（同批口径，源自 D-GW-20260928-01）：
  OpenRouter 当日全 0 价白名单 ∩ AA≥28 ∩ 输出文本 ∩ 非禁碰名单 → 12:15 自动进 free-flash/free-high。
  判定权威是 OR 目录 `pricing` 递归摊平后全部数值字段为 0（阈值字段除外，`-1` 算非 0）。
- [D-GW-20260928-03] **魔搭（modelscope）渠道只配 DeepSeek-V4.1-Flash 一席**（用户 2026-09-28 夜，逐字）：
  「**魔塔社区就配DeepSeek V4.1 flash就可以了**」。
  落地：`orchestration_policy.CHANNEL_MODEL_ALLOW`，**只限制新接入，不据此删已有席**（裁决说的是配几个，不是让谁下线）。
- [D-GW-20260928-04] **V4 / V4-PRO / V4-Flash / MiniMax-M3 这几代不考虑**（用户此前裁决，本轮补记录）：
  落地 `NON_GOAL_SUBSTR / NON_GOAL_EXACT`；匹配口径特意做成**不误伤 `DeepSeek-V4.1-Flash`**（用例 12）。
- [D-GW-20260928-05] **新增一条「纯快线」`fast`：只看速度，不看能力**（用户 2026-09-28 夜，逐字）：
  「**那我编排一条模型为 fast 的模型，就是纯快，不管能力。我可以用它来做测试、做脚本，做那些事情**」。
  口径（Agent 落地时的解释，如与用户后续意见冲突以用户为准）：
  ① 排序唯一键 = 本机 7 日实测 tok/s（并列看 TTFT），AA / 能力带不参与准入也不参与排序；
  ② **硬边界一条不放**：付费禁测渠道、封存渠道、伪免费禁碰名单、OR 全 0 价判定、非文本输出、
     渠道裁决与「不考虑」裁决、隐私席（`stealth/space-bunny-alpha` 一律不进，测试流量内容不可控）；
  ③ 速度也要证据：窗口内无有效 tok/s、成功实测 <3 条、可用率 <0.7 的不进——「不猜速度」与「不猜能力」是同一条纪律；
  ④ 线长上限 8，单日换席预算 4（首次建线不算换席），预算独立于生产两线；
  ⑤ 与 `paid-fast` 是两条线：`fast` 的取数池只从免费线（含旧别名）来，付费链成员不自动流入。
  详见 `projects/gateway/进展记录-20260928-深夜.md`。
- [D-GW-20260928-06] **U 档 / 速度型模型的实测口径：只认本机实测**（教训固化）：
  `openrouter/nvidia/nemotron-3.5-lightning:free` 社区标 670 tok/s，本机实测 **20.9**（差 32 倍）；
  同一模型跨渠道差 25 倍（groq 487.5 vs cloudflare 19.5）。今后任何"快"的判断，
  引用社区数字一律作废，必须有 `data/model_perf.json` 的本机样本支撑。

- [D-GW-20260928-07] **多模态维护先补"探针分型"，再谈自动化**（用户 2026-09-28 深夜，逐字：
  「**按你的默认顺序先补探针分型**」）。理由链：我给的三个缺口里，"9 席从未实测"是另外两个的前提
  ——没有实测，任何自动增删替换都只能瞎排。落地见 `projects/gateway/进展记录-20260928-深夜2-探针分型.md`：
  6 类新分型（tts_mimo/tts_clone/tts_edge/realtime_reach/jev_reach/video_submit），
  覆盖从 40/49 提到 **48/49**，唯一不覆盖的是 `paid-fast/mimo-v2.6-flash`（付费禁测红线，本该不测）。
  随这条定下的两条口径：① **弱探针要自报家门**——`realtime_reach`/`jev_reach` 只验在册与可达，
  不声明成能力实测；② **容量类失败（429/5xx/队列满）保留席位**，连续 3 天才报警且文案不得写"是否下架"，
  与判定表一致。

## 待失效 / 待复查
- 旧别名 `free-fast / free-balanced / free-heavy` 隐藏保留至 **2026-10-05**（另一项目迁移期）。
  删除前必须先把只挂在旧别名上的快席（现知 `groq/openai/gpt-oss-120b`，129.9 tok/s）挪进 live 线，
  否则它会从 `fast` 的取数池里掉出去。
- 样本缺 `source / outcome_class / probe_epoch` 字段 → reliability 自动降序、40/60 合并、
  基于真实流量的性能回滚保持关闭；这三条是开"完整版"闸门的前置（D-GW 设计 R2-B 第 1-4 项）。
