# STATE.md — 当前状态（短期记忆）

> 单写者 + 整体覆盖，**保留式更新**。每次更新整页重写，但稳定 ID（S-xxx）必须保留，删除必须先在 CHANGELOG 声明 DROP。
> source_event_until: 2026-08-14-膨胀问诊 | source_commit: bf8a4d9 | last_rebuild: 2026-08-14

## 进行中
- **[S-20260814-01] 记忆生命周期治理（待用户拍板）**：膨胀问诊回复已落档，方案待拍板——append-only 重定义为 ROTATE 例外、STATE 60 行/12KiB/完成 8 条硬限额、CHANGELOG 200 条归档、DECISIONS 增 D-ID、STALE 时效警告。

## 已完成（最近）
- **[S-20260814-11] 记忆膨胀/精简问诊（实读版）**（2026-08-14，v4 Flash）：GPT-5.6 Extended 回复 8587 字**确认实读**（核对当前 STATE 22 行/已完成 7 条），落档 `docs/ai-advice/gpt56_问诊回复_记忆膨胀精简_2026-08-14.md`，push `bf8a4d9`。
- **[S-20260814-02] 记忆备份/回退问诊（实读版）**（2026-08-14，v4 Flash）：确认实读，核心：备份=Git+GitHub 已够+按需 bundle；语义覆盖=稳定 ID+DROP+hook；回退=禁 force push 优先 revert/restore；凭证=key rotation。push `e3478e2`。
- **[S-20260814-09] 记忆守卫落地（完成）**（2026-08-14）：AGENTS 协议升级 + pre-commit hook（凭证扫描+S-ID 消失检测，三项测试过）+ STATE 稳定 ID + .gitignore + 交接命令同步。push `ad731a1`/`6e6228a`。
- **[S-20260814-10] 交接命令更新（完成）**（2026-08-14）：同步新写入协议（ff-only/保留式更新/稳定 ID/禁 force push）。
- **[S-20260814-03] 记忆备份/回退问诊（未读版）**（2026-08-14）：push `024467b`。
- **[S-20260813-04] 记忆覆盖/主分记忆问诊**（2026-08-13）：结论：当前别上主+分，先四文件+保留式更新。
- **[S-20260813-05] 门户资源清单雏形收尾**（2026-08-13）：ai-hub 数据桥复核，修复 3 处，回归 36 过/0 败/4 跳。push `2d49b5e`。

## 卡点
- 无。

## 下一步
- **[S-20260814-12] 落地记忆生命周期**：用户拍板膨胀方案后——AGENTS 增「记忆生命周期/归档」段、check_memory.py 加 size guard + STALE + archive 锁、新增 scripts/rotate_memory.py、DECISIONS 加 D-ID。
- 补 OpenCode Go / WorkBuddy 额度详情（待用户确认）。
