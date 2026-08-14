# STATE.md — 当前状态（短期记忆）

> 单写者 + 整体覆盖，**保留式更新**。每次更新整页重写，但稳定 ID（S-xxx）必须保留，删除必须先在 CHANGELOG 声明 DROP。
> source_event_until: 2026-08-14-记忆守卫落地 | source_commit: ccd7221 | last_rebuild: 2026-08-14

## 进行中
- **[S-20260814-01] 记忆机制改造（进行中）**：实读版 GPT 方案已拍板落地中——AGENTS.md 已升级、pre-commit 守卫已装；余下：验证 hook + 更新交接命令 + push。

## 已完成（最近）
- **[S-20260814-02] 记忆备份/回退问诊（实读版）**（2026-08-14，v4 Flash）：单链接强制实读 AGENTS.md 后 GPT 回复 4537 字，**确认实读**（GitHub +1 / git-scm +1 / oaicite 引用 + AGENTS.md §0/§1/§2/§6 原文），落档 ai-resource-hub `docs/ai-advice/gpt56_问诊回复_记忆备份回退_实读版_2026-08-14.md`（替代未读版）。核心：① 备份 = Git+GitHub 已够，只加按需 git bundle ② 发现语义覆盖 = STATE 状态项加稳定 ID + 消失必 DROP + pre-commit hook ③ 回退 = 禁 reset --hard + force push，优先 git revert / restore --source ④ 局部恢复 = git show 找回 + RESTORE 事件 ⑤ 凭证 = credentials.json 机械阻止 + key rotation。push `e3478e2`。
- **[S-20260814-03] 记忆备份/回退问诊（未读版）**（2026-08-14，v4 Flash）：GPT-5.6 Extended 回复 5324 字（未实读仓库，方向与实读版一致但缺细节），push `024467b`。
- **[S-20260813-04] 记忆覆盖/主分记忆问诊**（2026-08-13）：结论：当前别上主+分记忆，先「四文件 + UPDATES 保险层 + STATE 保留式更新」。
- **[S-20260813-05] 门户资源清单雏形收尾**（2026-08-13）：ai-hub 数据桥复核通过，修复 3 处，全量回归 36 过/0 败/4 跳。push `2d49b5e`。

- **[S-20260813-07] 共享记忆读写协议落地**（2026-08-13）：AGENTS.md 增补读写时机判断；新增 交接命令.md。
- **[S-20260813-08] 资源调查完成**：10 类约 73 条资源，落 RESOURCES.md。

## 卡点
- 无。

## 下一步
- **[S-20260814-09] 完成记忆守卫落地**：验证 pre-commit hook 拦截生效（故意违规测试）→ 更新交接命令.md → push ai-hub-memory。
- **[S-20260814-10] 更新交接命令.md**：同步新的写入协议（ff-only/保留式更新/稳定 ID/禁 force push）。
- 补 OpenCode Go / WorkBuddy 额度详情（待用户确认）。
