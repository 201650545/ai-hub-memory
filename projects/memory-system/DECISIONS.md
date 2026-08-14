# DECISIONS.md — 记忆系统项目专属决策（append-only）

> 只追加。本项目的技术决策；跨项目决策见 global/DECISIONS.md。

## 2026-08-14
- [D-MEMSYS-20260814-01] 记忆机制 = **采纳 GPT 实读版方案**：STATE 状态项加稳定 ID（S-xxx）+ 消失必 DROP 声明 + pre-commit hook 机械拦截 + `git pull --ff-only` + 禁 force push；备份只加按需 git bundle，不做定时备份服务。凭证误入历史 = key rotation 而非删文件。
- [D-MEMSYS-20260814-02] 记忆生命周期 = **采纳 GPT 膨胀/精简实读版方案**：append-only 重定义为「记录 immutable，ROTATE 唯一例外」；STATE ≤60 行/≤12 KiB/「已完成」≤8 条；CHANGELOG 200 条归档；DECISIONS 80 条 + D-ID + SUPERSEDES；STALE 只复核不自动删；archive 不可修改。
- [D-MEMSYS-20260814-03] 记忆线 = **项目作用域隔离 + 分层记忆 + Fail-Closed**（v2 定稿，见 global D-GLOBAL-20260814-01）。
