# STATE.md — 当前状态（短期记忆）

> 单写者 + 整体覆盖，**保留式更新**。每次更新整页重写，但稳定 ID（S-xxx）必须保留，删除必须先在 CHANGELOG 声明 DROP。
> source_event_until: 2026-08-14-多项目隔离问诊 | source_commit: 216eb76 | last_rebuild: 2026-08-14

## 进行中
- **[S-20260814-01] 多项目记忆隔离（待用户拍板）**：Claude 方案已落档——STATE 用方案 B（索引+分页）、DECISIONS/CHANGELOG 用方案 A（标签）、S-ID 加项目码；5 个待拍板点待定。

## 已完成（最近）
- **[S-20260814-15] 多项目记忆隔离问诊**（2026-08-14）：GPT 镜像站故障转 Claude Sonnet 5 交叉校验，回复 5103 字落档 `docs/ai-advice/claude_sonnet5_问诊回复_多项目记忆隔离_2026-08-14.md`，push `216eb76`。
- **[S-20260814-13] 记忆生命周期方案落地**（2026-08-14）：AGENTS §2.5 + hook 扩展 + rotate_memory.py + DECISIONS D-ID。
- **[S-20260814-11] 记忆膨胀/精简问诊（实读版）**（2026-08-14，v4 Flash）：GPT-5.6 Extended 回复 8587 字确认实读，落档，push `bf8a4d9`。
- **[S-20260814-02] 记忆备份/回退问诊（实读版）**（2026-08-14，v4 Flash）：确认实读，push `e3478e2`。
- **[S-20260814-09] 记忆守卫落地（完成）**（2026-08-14）：AGENTS 升级 + hook + STATE 稳定 ID + .gitignore + 交接命令。push `ad731a1`/`6e6228a`。
- **[S-20260814-10] 交接命令更新（完成）**（2026-08-14）：同步新写入协议。
- **[S-20260814-03] 记忆备份/回退问诊（未读版）**（2026-08-14）：push `024467b`。

## 卡点
- 无。

## 下一步
- **[S-20260814-14] 落地多项目隔离**：用户拍板 Claude 方案 + 5 个待确认点后——AGENTS 加多项目协议、STATE 拆索引+分页、hook 改逐文件检测、S-ID 加项目码、新增 scripts（regen-index/decisions-for/changelog-for）。
- 补 OpenCode Go / WorkBuddy 额度详情（待用户确认）。
