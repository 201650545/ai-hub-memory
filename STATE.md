# STATE.md — 当前状态（短期记忆）

> 单写者 + 整体覆盖，**保留式更新**。每次更新整页重写，但稳定 ID（S-xxx）必须保留，删除必须先在 CHANGELOG 声明 DROP。
> source_event_until: 2026-08-14-记忆线定稿 | source_commit: 0c46589 | last_rebuild: 2026-08-14

## 进行中
- **[S-20260814-01] 记忆系统 v2 升级（方案已定稿，待落地）**：三方交叉（网关+Claude+GPT）确认方案——项目作用域隔离 + 分层记忆 + Routing-before-Retrieval + Fail-Closed；落地项：MEMORY.json + memory.py + memory-router/SKILL.md + 三件套移入 projects/<id>/。

## 已完成（最近）
- **[S-20260814-16] 记忆线路由定稿（三方交叉）**（2026-08-14）：AI 搜索网关（元宝命名空间隔离方向）+ Claude Sonnet5 #2（路径即身份/环境变量路由）+ GPT-5.6 Extended #2（MEMORY.json+memory.py+SKILL 定稿）三方一致。落档 ai-resource-hub（claude `dc087d6`/gpt `0c46589`）。
- **[S-20260814-15] 多项目记忆隔离问诊**（2026-08-14）：Claude Sonnet 5 交叉校验（GPT 镜像站故障转 Claude），回复落档，push `216eb76`。
- **[S-20260814-13] 记忆生命周期方案落地**（2026-08-14）：AGENTS §2.5 + hook 扩展 + rotate_memory.py + DECISIONS D-ID。
- **[S-20260814-11] 记忆膨胀/精简问诊（实读版）**（2026-08-14）：GPT-5.6 Extended 8587 字确认实读，push `bf8a4d9`。
- **[S-20260814-02] 记忆备份/回退问诊（实读版）**（2026-08-14）：确认实读，push `e3478e2`。
- **[S-20260814-09] 记忆守卫落地（完成）**（2026-08-14）：AGENTS 升级 + hook + 稳定 ID + .gitignore + 交接命令。push `ad731a1`/`6e6228a`。
- **[S-20260814-10] 交接命令更新（完成）**（2026-08-14）：同步新写入协议。

## 卡点
- 无。

## 下一步
- **[S-20260814-17] 落地记忆系统 v2**：按定稿方案——建 MEMORY.json（项目路由表：teaching/courseware/memory-system + aliases）、写 memory.py（route/read/search/write/validate 五命令）、写 memory-router/SKILL.md（R1-R9 宪法）、三件套移入 projects/<id>/、hook 适配（project_id 校验/S-ID 项目内唯一/CHANGELOG 脚本维护）。
- 补 OpenCode Go / WorkBuddy 额度详情（待用户确认）。
