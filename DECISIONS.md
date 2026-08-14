# DECISIONS.md — 决策记录（只追加，带日期）

> 只追加，不删改旧条目。用户敲板的决策记这里。

## 2026-08-14
- [D-20260814-01] 记忆机制 = **采纳 GPT 实读版方案**：STATE 状态项加稳定 ID（S-xxx）+ 消失必 DROP 声明 + pre-commit hook 机械拦截 + `git pull --ff-only` + 禁 force push；备份只加按需 git bundle，不做定时备份服务。凭证误入历史 = key rotation 而非删文件。
- [D-20260814-02] 记忆生命周期 = **采纳 GPT 膨胀/精简实读版方案**：① append-only 重定义为「记录 immutable，ROTATE 是唯一例外」（旧记录同 commit 原样进 archive/）② STATE 硬限额 ≤60 行/≤12 KiB/「已完成」≤8 条（hook 强制，超窗口 DROP 进 CHANGELOG，不建 STATE archive）③ CHANGELOG 200 条触发归档到 archive/changelog/YYYY/ ④ DECISIONS 80 条低频归档 + 增 D-ID + SUPERSEDES 链 ⑤ STALE 时效警告（进行中 14 天/下一步/卡点 30 天，只复核不自动删）⑥ archive/ 已提交文件不可修改。：STATE 状态项加稳定 ID（S-xxx）+ 消失必 DROP 声明 + pre-commit hook 机械拦截 + `git pull --ff-only` + 禁 force push；备份只加按需 git bundle，不做定时备份服务。凭证误入历史 = key rotation 而非删文件。

## 2026-08-13
- 工作模型 = **按需调度**：用户自然说话，Agent 当调度大脑路由已打通工具；**不做**定时提醒 / 汇报平台。
- 多 Agent 共享记忆 = **分层方案**（AGENTS.md / STATE.md / DECISIONS.md / CHANGELOG.md），GitHub 仓库承载。
- 每次执行前先向用户确认。
- 问诊走 GPT 镜像站 **Thinking · Extended**（不是 Auto）。

## 2026-08-12
- 前端统一苹果浅色风 + 深色切换按钮。
