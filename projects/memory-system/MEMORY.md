# MEMORY.md — memory-system 稳定知识（长期语义记忆）

> 定位：本文件回答「关于这个项目，我们已经确定了什么」，不回答流水账。
> 与 STATE.md 的分工：STATE 回答「现在发生什么、下一步是什么」；MEMORY 回答「已确定的知识」。
> 与 ROUTER.md 的分工：ROUTER 是低语义路由索引（历史在哪里），MEMORY 是已提炼的稳定结论。
> 维护：只有当某条经验被**多次**验证、或属架构级决定时才写入本文件；单次事件留在 STATE。
> 本项目的核心事实：**记忆系统 = Memory = Global Kernel + Project Namespace + Layered Retrieval；Routing before Retrieval，Multi-read/Single-write，Fail Closed**（D-GLOBAL-20260814-01 v2 定稿，多模型交叉问诊三方一致）。

---

## 一、架构总览（当前版本 v2.1）

1. **三层组件**：`MEMORY.json`（路由表）+ `memory.py`（唯一读写路由器）+ `inbox/`（隔离入口，pending/settled/receipts/META）。
2. **memory.py 5 新命令**：`capture` / `status` / `settle-plan` / `resolve` / `settle`（v2.1 加入，配合 `sync` 批量导入）。
3. **宪法**：RULES 16 条（R1'~R16），含 FF-only、保留式更新、禁 force push、S-ID+DROP 规则、凭证机械阻止、key rotation。
4. **pre-commit hook**：`scripts/check_memory.py` 链接为 `.git/hooks/pre-commit`——凭证扫描 + STATE S-ID 消失检测（无 DROP 删 ID 拦截）。
5. **项目注册**：`MEMORY.json` 的 `projects` 清单定义项目作用域（含 aliases/path/imports），新项目经 `memory.py` 注册入清单并落 `projects/<pid>/`。

## 二、分层记忆模型

1. **Candidate Layer**（临时记忆）→ **HOT**（`STATE.md` 当前状态，≤60 行/≤12 KiB/「已完成」≤8 条）→ **WARM**（长期语义记忆 = `MEMORY.md` + 全局文件）→ **DORMANT/ARCHIVE**（长期情景记忆 = `archive/`，不可修改）。
2. **Router 必须低语义、强定位**：ROUTER.md 只存路由元数据（memory_id/kind/topic_keys/entities/period/status/archive_ref/source_ids/superseded_by/sha256_16），不存结论；迁移 archive 时**必须**同步新增索引行，否则等于永久丢失；`sha256_16` 迁移前后必须一致。
3. **封存的是上下文占用，不是信息本身。封存不是删除。** 冷记忆必须可通过 ROUTER 索引召回，否则等于永久丢失。

## 三、生命周期与归档规则

1. **append-only 重定义为「记录 immutable，ROTATE 唯一例外」**——同 commit 原样进 archive。
2. **STATE 硬限额**：≤60 行 / ≤12 KiB / 「已完成」最近 ≤8 条；超窗口 DROP 进 CHANGELOG，不建 STATE archive。
3. **CHANGELOG**：只追加，200 条触发归档到 `archive/changelog/`；**DECISIONS**：80 条低频归档 + D-ID + SUPERSEDES；STALE 只复核不自动删。
4. **S-ID 规范**：`S-YYYYMMDD-NN`；任何 ID 消失必须 CHANGELOG 追加 DROP，pre-commit hook 机械拦截。
5. **备份策略**：不做定时备份服务，强化「可证明地重建」——UPDATES 不可变事件层 + 事件重放优先于 git checkout；凭证走 key rotation 而非删历史。

## 四、读取协议与隔离

1. **Quarantined Ingress（隔离记忆，v2.1 用户拍板）**：普通 Agent 不读全部 UNKNOWN；lazy daily consolidation 不建定时平台（D-20260814-01）。
2. **读取协议**：Routing before Retrieval；索引页 + 本项目页 + decisions-for 过滤；单写者 + 整体覆盖，保留式更新。
3. **凭证纪律**：凭证绝不入记忆（pre-commit 拦截）；对他人未提交改动不代提交、不代回退，保留原样至其本人处理。
