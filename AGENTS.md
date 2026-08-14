# AGENTS.md — 多 Agent 协作协议（启动引导）

> ⚡ **v2 已启用（2026-08-14）**：记忆已按项目隔离——三件套在 projects/<id>/ 下，读写必须走 `python scripts/memory.py`，路由表见 MEMORY.json，Agent 行为协议见 skills/memory-router/SKILL.md，全局规则见 global/RULES.md。以下条款在 v2 下仍有效，但「读 STATE+DECISIONS」指读当前项目的，写必须经 memory.py。
>
> ⚠️ 本文件是「启动引导」，不是「强制配置」。任何 Agent（Claude Code / ChatGPT / Kimi / 执行 Agent）接手任务前先读它。要真正保证「读到 + 照做」，靠 **hook + 交接命令模板兜底**，不能只靠本文件。
>
> **本仓库 = 多 Agent 共享记忆的唯一真源**。记忆以「项目」为原子单元，不是以「对话」为单元。

---

## 0. 读写时机判断（核心，先看这段）

### 何时「读」？—— 只在「新项目单元」开始时读，不是每次对话都读

**满足任一，读一次：**
- 接手一个**新的、独立的**项目 / 任务单元（用户提出一个新的独立目标，不是上一个的延续）
- 跨会话后**第一次**接触某个已记录的项目
- 用户明说「接手 / 继续 / 同步 XX 项目」

**跳过（不读）：**
- 同一个项目内的连续追问、调试、微调、改 bug
- 纯咨询 / 闲聊 / 不改变共享状态的问题
- 本会话内已经读过一次

### 何时「写」？—— 只在「可交付单元完成后」写，不是每个动作都写

**满足任一，写一次：**
- 一个**可交付单元**完成（能独立验收、别人可能要用到）
- 用户**拍板**了一个决策
- 产生了别的 Agent 会用到 / 需要知道的状态变化（资源、工具、路径、额度、账号）

**跳过（不写）：**
- 中间探索过程、未完成的东西
- 一次性、不再复用的内容
- 只在本地、别人不需要知道的细节

> 一句话记忆法：**新项目开始前读一遍，一个单元交付后写一条。** 判断不了就默认「先读 STATE 一眼」，宁读不重写。

---

## 1. 读什么 / 写什么

**读（两个小文件，一页纸，够快）：**
1. `STATE.md` —— 当前进度 / 卡点 / 下一步（当前状态快照）
2. `DECISIONS.md` —— 用户已敲板的决策（别推翻）

> 不需要读 `AGENTS.md`（协议本身）和 `CHANGELOG.md`（历史流水，需要回溯时才查）。

**写（三处，各司其职）：**
1. `CHANGELOG.md` —— **追加**一条流水（谁 / 何时 / 做了什么）
2. `STATE.md` —— **整体重写**（单写者，覆盖成最新快照），但必须**保留式更新**：
   - **稳定 ID（防语义覆盖，核心）**：STATE 中每个仍然有效、不能无声丢失的状态项，带稳定 ID 如 `[S-20260814-01]`。正常更新可改文字，**ID 必须保留**。
   - **删除必须声明**：某 ID 不再有效 → 先在 `CHANGELOG.md` 追加 `DROP S-xxx — 原因`，再从 STATE 删除该 ID。任何「ID 消失但无 DROP 记录」都是违规（pre-commit hook 会拦截）。
   - **局部恢复**：误删某条 → 用 `git show <GOOD_COMMIT>:STATE.md | grep "S-xxx"` 找回，手工插回最新版，CHANGELOG 追加 `RESTORE S-xxx — 来源`。
3. `DECISIONS.md` —— **追加**一条（仅当用户敲板决策，带日期）

---

## 2. 读写落地方式（Git 串行化，防冲突）

```
读：  gh repo clone 201650545/ai-hub-memory  （或 git pull --ff-only）
写：  git pull --ff-only 最新 → 重读 STATE+DECISIONS → 改文件 → commit → push
```

**防覆盖铁律（GPT 实读版问诊 2026-08-14 确认，最重要）：**
- **禁止按 Agent 旧上下文整页重建 STATE**。pull 后必须重读磁盘上的最新 STATE.md，在其基础上做保留式修改；未知条目默认保留，只有「明确完成/失效/被新事实取代」才允许删除（删除必须 DROP 声明）。
- **`git pull --ff-only`**：拉取阶段历史分叉就直接停下报错，不偷偷产生 merge（避免未注意的分叉合并）。
- **禁止 `reset --hard` + `force push`**（改写共享历史）：整提交撤销用 `git revert`，单文件恢复用 `git restore --source=<commit> -- <file>`。
- **push 失败（远端前进）**：禁止 force push；重新 `git pull --ff-only` → 重读最新记忆 → 重新合并本次变化 → 再 push。

**并发规则（GPT 纠正，重要）：**
- 「append-only 不免疫冲突」：两个 Agent 同时追加同一文件，Git 在 EOF 区域仍会 merge conflict。
- 正确姿势：**不同 Agent 不改同一个文件**；或按 `git pull 最新 → 改 → push` 串行化。
- `STATE.md` = 单写者 + 整体重写；`DECISIONS.md` / `CHANGELOG.md` = 追加，但同一时刻一个写者。

---

## 2.5 记忆生命周期 / 归档（GPT 实读版问诊 2026-08-14 拍板）

- **STATE 是当前状态投影，不是历史库**：保持 ≤60 行、≤12 KiB；「已完成（最近）」最多保留 8 条。超出窗口的完成项必须先在 CHANGELOG 记录 `DROP`，再从 STATE 移除；**不单独建立 STATE archive**（旧快照天然在 Git 历史里）。
- **append-only 的准确定义**：历史记录 immutable；正常写入只允许追加。**ROTATE 是唯一例外**——旧记录可从热文件移出，但必须在同一 commit 中原样进入 `archive/`，不得改写其内容。
- **CHANGELOG 归档**：建议月切换或达到 200 条时归档到 `archive/changelog/YYYY/`；DECISIONS 低频归档（80 条为阈值），归档后仍有效的长期决策在热文件保留简短引用。
- **archive/ 是冷历史，不是第二套记忆系统**：Agent 默认不读 archive（CHANGELOG 本就回溯才查）；已提交的 archive 文件禁止普通修改，修正只能追加 `CORRECTION` / `SUPERSEDES` 记录。
- **时效度（STALE）**：STATE 的进行中/下一步/卡点允许脚本按 Git 最后修改时间报告 STALE（进行中 14 天 / 下一步 30 天 / 卡点 30 天）。STALE 只要求复核，**不得自动删除**；删除仍必须满足 DROP 规则（时间老 ≠ 事实失效）。
- **DECISIONS 稳定 D-ID**：决策带 `[D-YYYYMMDD-NN]`，变更用 `SUPERSEDES D-xxx` 链，归档后仍可无歧义引用。

> 归档执行：`python scripts/rotate_memory.py changelog|decisions`（显式触发，不自动 commit/push）；守卫：pre-commit hook 检查 size/STALE/archive 锁。

---

## 3. 工具地图（已打通）
- **完整工具手册见 `global/TOOLS.md`**（gh / lark-cli / opencli / 网关 :3000 的能力、命令、登录态、坑）。
- 三大关键工具：`gh`=GitHub、`lark-cli`=飞书、`opencli`=浏览器/多站适配器（另：`tg`、`wecom-cli`=企业微信、`wx`=微信、notion、obsidian、longbridge…）
- opencli browser 控 AI 引擎：doubao-app / chatgpt-app / codex / cursor 等 adapter。
- 统一网关 `:3000`（`D:\项目\services\search_gateway`，opencli 控 5 引擎：元宝/豆包/Kimi/千问/Meta AI）。
- 编排器 `:8791`（课件生成）。
- DeepSeek Harness `:3080`（`D:\DeepSeek\deepseek-harness`，源码构建，独立于 WorkBuddy）。

## 4. 工作模型
按需调度：用户自然说一句话，Agent 当调度大脑，自己判断该打哪个已打通工具（飞书表→lark-cli、仓库→gh、搜索→网关多引擎、额度→台账），去查、去连、去汇总、去解决。**不搭定时提醒/汇报平台**。

## 5. 分工边界
- 课件 / 配套练习「生成」→ 执行 Agent（我只写命令 + 复核）。
- 删除 / 归档 / 改名 / 规范编辑 / 整理 → 我（Claude Code）。
- 前端方案 → Kimi K3；架构方案 → 最先进模型把关。
- 每次执行前先向用户确认。

## 6. 安全红线
- 凭证值只进 `scheduler/credentials.json`（信任平面）；绝不进 chat / 报告 / commit / 飞书 / logs。
- **机械阻止（GPT 实读版问诊 2026-08-14）**：`scheduler/credentials.json` 必须 `untracked + .gitignore`；commit 前由 pre-commit hook 扫描，任何疑似凭证（sk-/AIza/Bearer/app_token 等模式）进入 index 即拒绝。
- **凭证误入历史（key rotation，不是删文件）**：Git 历史不可逆，删文件不等于安全；误提交 = 立即废弃该 key（rotation），再处理历史（git filter-repo + 所有 clone 重新同步）。
- 不创建 / 删除 API key，不充值，不绑卡，不订阅。
