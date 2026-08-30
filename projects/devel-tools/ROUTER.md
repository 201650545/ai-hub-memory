# ROUTER.md — devel-tools 冷记忆路由索引

> 定位：本文件是 **Router / Gate**，只保存**路由元数据**，**不保存完整结论**。
> 它回答的问题是「关于这个主题，以前发生过事情，历史在**这里**」，而不是「最后的解决方案是什么」。
> 为什么不在索引里写长摘要：若把历史结论复制进索引，过两年 ROUTER.md 会变成第二个 STATE.md，且必然出现「正文更新了摘要没更新」的不一致。
> **Router 必须低语义、强定位。**
> 分工：稳定知识 → `MEMORY.md`；当前状态 → `STATE.md`；历史过程 → `archive/`；本文件只负责把关键词路由到位置。

## 字段定义

`memory_id | kind | topic_keys | entities | period | status | archive_ref | source_ids | superseded_by | sha256_16`

| 字段 | 含义 |
|---|---|
| memory_id | 稳定 SID |
| kind | incident / decision / template / handoff / verification |
| topic_keys | 用于路由命中的主题词（小写、逗号分隔） |
| entities | 涉及的文件、端口、渠道、进程等实体 |
| period | 归属期（YYYY-MM） |
| status | resolved / superseded / active |
| archive_ref | 正文位置（`archive/...` 或 `STATE.md`） |
| source_ids | 来源 SID |
| superseded_by | 被哪条取代 |
| sha256_16 | 正文 sha256 前 16 位，用于校验原文未被改写 |

## 索引表

| memory_id | kind | topic_keys | entities | period | status | archive_ref | source_ids | superseded_by | sha256_16 |
|---|---|---|---|---|---|---|---|---|---|
| S-20260815-03 | template | 交接模板, agent上报, memory.py, capture, settle | ai-hub-memory, docs/Agent记忆上报指令.md | 2026-08 | resolved | archive/projects/devel-tools/2026/2026-08.md | — | — | 5cbcc5d2e9a4a785 |
| S-20260827-06 | handoff | phase1, 失败归一化, route-plan, failover, 流式commit | upstream_outcome.py, :3100, PID32912, refactor/monorepo-20260812 | 2026-08 | resolved | archive/projects/devel-tools/2026/2026-08.md | S-20260827-05 | S-20260827-07 | d7afced3d08f39b7 |

## Agent 怎么用（两种唤醒）

**A. 临时召回（＝MoE 的一次 expert activation）**
1. 用关键词在本表 `topic_keys` / `entities` 中查找命中行；
2. 按 `archive_ref` 打开正文（如 `archive/projects/devel-tools/2026/2026-08.md#S-20260827-14`）；
3. 历史进入本轮上下文，**文件本身不搬回**，任务结束后仍留在 archive。

**B. 持久重新激活**
若旧问题真正再次成为当前状态：**不要把旧正文搬回 STATE**，而是新建 STATE 条目并写 `reactivates: 旧SID`。
这样旧记忆仍是当时的真实历史，新条目描述新现实。

**按 SID 精确 recall**
`archive_ref` + `#<SID>` 即可精确定位；`sha256_16` 用于确认正文未被改写。

## 维护规则

1. 条目迁移到 archive 时**必须同步新增本表一行**，否则等于永久丢失。
2. 不在本表写结论、不写长摘要。
3. `sha256_16` 迁移前后必须一致（不一致说明正文被改写，判迁移失败）。
4. STATE.md 中的活跃条目无需在上表重复索引（它们直接在 STATE 可见）。
| archive-devel-tools-20260830 | incident | devel-tools-state-archive | devel-tools | 2026-08 | resolved | archive/projects/devel-tools/2026/2026-08-30.md | S-20260815-01..S-20260828-05 | | |
