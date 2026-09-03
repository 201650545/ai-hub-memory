# DECISIONS.md — 记忆系统项目专属决策（append-only）

> 只追加。本项目的技术决策；跨项目决策见 global/DECISIONS.md。

## 2026-09-03
- [D-MEMSYS-20260903-01] **知识三工具单写真源定稿**（镜像版 extend 咨询，落 handbook 50-规范）：Obsidian=写知识（本地真源）｜GitHub=版本化+发布给 AI（镜像只读）｜飞书=管结构化动态数据（退出记忆主链，仅审计）。**同一种数据只允许一个可写真源，其余全部 mirror/projection/cache/audit**。记忆线改为：Claude 内部 Memory → D:\记忆（唯一密 canonical）→ git publish → yongtai-memory（AI 可读镜像）。飞书↔记忆 双向同步废止。
- [D-MEMSYS-20260903-02] **Obsidian 五库压两库**：合并为 Vault A=Work（Handbook+项目索引+项目文档）与 Vault B=Memory（单独保留，安全/生命周期边界，1 个不推荐）。合并 vault≠合并 git repo（各项目仓独立 .git）；Work 根不做大 git 仓。执行待调度（需关运行中 Obsidian）。

## 2026-08-14
- [D-MEMSYS-20260814-01] 记忆机制 = **采纳 GPT 实读版方案**：STATE 状态项加稳定 ID（S-xxx）+ 消失必 DROP 声明 + pre-commit hook 机械拦截 + `git pull --ff-only` + 禁 force push；备份只加按需 git bundle，不做定时备份服务。凭证误入历史 = key rotation 而非删文件。
- [D-MEMSYS-20260814-02] 记忆生命周期 = **采纳 GPT 膨胀/精简实读版方案**：append-only 重定义为「记录 immutable，ROTATE 唯一例外」；STATE ≤60 行/≤12 KiB/「已完成」≤8 条；CHANGELOG 200 条归档；DECISIONS 80 条 + D-ID + SUPERSEDES；STALE 只复核不自动删；archive 不可修改。
- [D-MEMSYS-20260814-03] 记忆线 = **项目作用域隔离 + 分层记忆 + Fail-Closed**（v2 定稿，见 global D-GLOBAL-20260814-01）。

- [D-20260814-01] 用户拍板 v2.1：隔离记忆机制（Quarantined Ingress），普通 Agent 不读全部 UNKNOWN，lazy daily consolidation 不建定时平台（2026-08-14）

- [D-20260814-02] 用户原则：对话内容本身就是记忆，Agent 代表用户与外部 AI 对话并控制在 3 轮内定稿，不反复（2026-08-14）

