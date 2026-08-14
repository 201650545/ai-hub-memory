# STATE.md — 当前状态（短期记忆）

> 单写者 + 整体覆盖，**保留式更新**。每次更新整页重写，但稳定 ID（S-xxx）必须保留，删除必须先在 CHANGELOG 声明 DROP。
> source_event_until: 2026-08-14-生命周期落地 | source_commit: 待提交 | last_rebuild: 2026-08-14

## 进行中
- **[S-20260814-01] 记忆生命周期治理（进行中）**：膨胀方案已拍板（D-20260814-02），正在落地——AGENTS §2.5 已加、hook 扩展完成、rotate_memory.py 已建；余下：DECISIONS D-ID 已加，验证 + push。
- **[S-20260814-12] 落地记忆生命周期（进行中）**：AGENTS 增「记忆生命周期/归档」段（§2.5）✓、check_memory.py 加 size guard + STALE + archive 锁 ✓、新增 scripts/rotate_memory.py ✓、DECISIONS 加 D-ID ✓；待验证 + push。

## 已完成（最近）
- **[S-20260814-13] 记忆生命周期方案落地**（2026-08-14）：AGENTS §2.5 生命周期段 + check_memory.py 扩展（size/归档阈值/archive 锁/STALE）+ rotate_memory.py + DECISIONS D-ID。
- **[S-20260814-11] 记忆膨胀/精简问诊（实读版）**（2026-08-14，v4 Flash）：GPT-5.6 Extended 回复 8587 字**确认实读**，落档 `docs/ai-advice/gpt56_问诊回复_记忆膨胀精简_2026-08-14.md`，push `bf8a4d9`。
- **[S-20260814-02] 记忆备份/回退问诊（实读版）**（2026-08-14，v4 Flash）：确认实读，备份=Git+GitHub+按需 bundle；语义覆盖=稳定 ID+DROP+hook；回退=禁 force push；凭证=key rotation。push `e3478e2`。
- **[S-20260814-09] 记忆守卫落地（完成）**（2026-08-14）：AGENTS 协议升级 + pre-commit hook（三项测试过）+ STATE 稳定 ID + .gitignore + 交接命令同步。push `ad731a1`/`6e6228a`。
- **[S-20260814-10] 交接命令更新（完成）**（2026-08-14）：同步新写入协议（ff-only/保留式更新/稳定 ID/禁 force push）。
- **[S-20260814-03] 记忆备份/回退问诊（未读版）**（2026-08-14）：push `024467b`。
- **[S-20260813-04] 记忆覆盖/主分记忆问诊**（2026-08-13）：当前别上主+分，先四文件+保留式更新。

## 卡点
- 无。

## 下一步
- **[S-20260814-14] 验证生命周期落地**：测试新 hook 检查（size 超限拦截/archive 锁/rotate 脚本）→ push ai-hub-memory。
- 补 OpenCode Go / WorkBuddy 额度详情（待用户确认）。
