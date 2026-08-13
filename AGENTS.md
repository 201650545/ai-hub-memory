# AGENTS.md — 多 Agent 协作协议（启动引导）

> ⚠️ 本文件是「启动引导」，**不是「强制配置」**。任何 Agent（Claude Code / ChatGPT / Kimi / 执行 Agent）接手任务前先读它。要真正保证「读到 + 照做」，靠 **hook + 每次问诊 prompt 模板兜底**，不能只靠本文件。

## 0. 开工前必读（bootstrap）
1. 读 `STATE.md` —— 了解当前进度 / 卡点 / 下一步。
2. 读 `DECISIONS.md` —— 了解用户已敲板的决策，**别推翻**。
3. 做完在 `CHANGELOG.md` 末尾追加一条（谁 / 何时 / 做了什么）。
4. 用户敲板的决策，追加进 `DECISIONS.md`（带日期）。

## 1. 工具地图（已打通）
- opencli 外部 CLI：`lark-cli`=飞书、`gh`=GitHub、`tg`、`wecom-cli`=企业微信、`wx`=微信、notion、obsidian、longbridge…
- opencli browser 控 AI 引擎：doubao-app / chatgpt-app / codex / cursor 等 adapter。
- 统一网关 `:3000`（`D:\游戏\ds_v4_cli`，opencli 控 4 大 AI 搜索）。
- 编排器 `:8791`（课件生成）。

## 2. 工作模型
按需调度：用户自然说一句话，Agent 当调度大脑，自己判断该打哪个已打通工具（飞书表→lark-cli、仓库→gh、搜索→网关多引擎、额度→台账），去查、去连、去汇总、去解决。**不搭定时提醒/汇报平台**。

## 3. 分工边界
- 课件 / 配套练习「生成」→ 执行 Agent（我只写命令 + 复核）。
- 删除 / 归档 / 改名 / 规范编辑 / 整理 → 我（Claude Code）。
- 前端方案 → Kimi K3；架构方案 → 最先进模型把关。
- 每次执行前先向用户确认。

## 4. 并发规则（GPT 纠正，重要）
- **「append-only 不免疫冲突」**：两个 Agent 同时追加同一文件，Git 在 EOF 区域仍会 merge conflict。
- 正确姿势：**不同 Agent 不改同一个文件**；或按 `git pull 最新 → 改 → push` 串行化。
- `STATE.md` = 单写者 + 整体重写；`DECISIONS.md` / `CHANGELOG.md` = 追加，但同一时刻一个写者。

## 5. 安全红线
- 凭证值只进 `scheduler/credentials.json`（信任平面）；绝不进 chat / 报告 / commit / 飞书 / logs。
- 不创建 / 删除 API key，不充值，不绑卡，不订阅。
