# DECISIONS.md — 决策记录（只追加，带日期）

> 只追加，不删改旧条目。用户敲板的决策记这里。

## 2026-08-14
- 记忆机制 = **采纳 GPT 实读版方案**：STATE 状态项加稳定 ID（S-xxx）+ 消失必 DROP 声明 + pre-commit hook 机械拦截 + `git pull --ff-only` + 禁 force push；备份只加按需 git bundle，不做定时备份服务。凭证误入历史 = key rotation 而非删文件。

## 2026-08-13
- 工作模型 = **按需调度**：用户自然说话，Agent 当调度大脑路由已打通工具；**不做**定时提醒 / 汇报平台。
- 多 Agent 共享记忆 = **分层方案**（AGENTS.md / STATE.md / DECISIONS.md / CHANGELOG.md），GitHub 仓库承载。
- 每次执行前先向用户确认。
- 问诊走 GPT 镜像站 **Thinking · Extended**（不是 Auto）。

## 2026-08-12
- 前端统一苹果浅色风 + 深色切换按钮。
