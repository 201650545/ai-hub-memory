# STATE.md — 当前状态（短期记忆）· memory-system 项目

> 单写者 + 整体覆盖，**保留式更新**。稳定 ID（S-xxx）必须保留，删除必须先在 CHANGELOG 声明 DROP。
> source_event_until: 2026-08-14-v21定稿 | last_rebuild: 2026-08-14

## 进行中
- **[S-20260814-19] 记忆系统 v2.1 升级（定稿待落地）**：Quarantined Ingress + Project-scoped Consolidation——inbox/ + memory.py 5 新命令 + R1'~R16 宪法 + lazy daily consolidation；落地按 GPT 实现优先级。

## 已完成（最近）
- **[S-20260814-21]** v2.1 已落地：MEMORY.json v2.1 + memory.py 5 新命令 + inbox/ + RULES 16 条宪法 + hook inbox 守卫；验收测试通过（teaching 只见 A+C 不见 B+D）（2026-08-14）
- **[S-20260814-20] 隔离记忆 v2.1 定稿（GPT 3 轮闭环）**（2026-08-14）：GPT 确认实读（24 处引用）；代表用户拍板 4 点；v2.1 定稿 20484 字落档 ai-resource-hub `ad40620`。
- **[S-20260814-18] 记忆系统 v2 落地**（2026-08-14）：MEMORY.json + memory.py + SKILL.md + 三件套移入 projects/ + hook 多项目适配。
- **[S-20260814-16] 记忆线路由定稿（三方交叉）**（2026-08-14）：网关+Claude+GPT 一致，落档（`dc087d6`/`0c46589`）。
- **[S-20260814-15] 多项目记忆隔离问诊**（2026-08-14）：Claude Sonnet 5 交叉校验（GPT 镜像站故障转 Claude），push `216eb76`。
- **[S-20260814-13] 记忆生命周期方案落地**（2026-08-14）：AGENTS §2.5 + hook 扩展 + rotate_memory.py + DECISIONS D-ID。
- **[S-20260814-11] 记忆膨胀/精简问诊（实读版）**（2026-08-14）：GPT-5.6 Extended 8587 字确认实读，push `bf8a4d9`。
- **[S-20260814-02] 记忆备份/回退问诊（实读版）**（2026-08-14）：确认实读，push `e3478e2`。

## 卡点
- 无。

## 下一步
- **[S-20260814-17] 落地记忆系统 v2.1**：按 GPT 实现优先级——① RULES+SKILL+MEMORY.json 升级 v2.1（R1'~R16）② inbox/ + capture + secret preflight ③ filtered staging read/status（验收：teaching 只见 A+C 不见 B+D）④ resolve + settle-plan ⑤ settle（复用正式 write）⑥ check_memory 加 inbox 守卫 + rotate_memory 项目化。
- 补 OpenCode Go / WorkBuddy 额度详情（待用户确认）。
