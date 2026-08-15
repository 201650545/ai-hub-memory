# AI Hub Memory — 多 Agent 共享记忆

> **多 Agent 协作的唯一记忆真源。** 任何 Agent（Claude / ChatGPT / Kimi / 执行 Agent / 高级模型）接手任务前读这里，即掌握全部项目状态、规则与资源，无需翻 5 个仓库。

![Status](https://img.shields.io/badge/status-active-blue) ![Version](https://img.shields.io/badge/version-v2.1-green)

---

## 它是什么

一套「模型无关」的多 Agent 共享记忆系统：多个 AI Agent 做不同项目（教学、课件、记忆系统、英语学习…），共用一个 GitHub 仓库作记忆真源。**记忆不绑定任何模型**——换模型、换窗口，读一遍记忆即可无缝接手。

## 5 仓库体系

| 仓库 | 职责 |
|------|------|
| **ai-hub-memory**（本仓库） | 共享记忆 / 路由规则 / 项目状态 |
| ai-resource-hub | AI 资源运营与配置来源（API/账号/额度） |
| ai-hub | 统一操作台（网关/搜索/编排） |
| feishu-data-hub | 飞书数据 → GitHub Pages 公开桥 |
| english-teaching-production | 教学业务生产体系 |

> 5 仓库全景见 `global/PROJECTS.md`；职责边界：RULES=MUST / PROJECTS=WHERE / RESOURCES=WHAT / TOOLS=HOW / STATE=NOW。

## 核心设计（v2.1）

- **项目隔离**：`projects/<id>/` 物理隔离，Agent 默认只读 global + 自己项目，跨项目必须显式声明。
- **分层记忆**：L0 工作记忆（不落盘）→ L1 隔离暂存 inbox（允许 UNKNOWN）→ L2 项目 STATE → L3 DECISIONS/CHANGELOG/archive。
- **隔离暂存（Quarantined Ingress）**：对话中产生的候选事实先 capture 到 inbox（不确定归属可 UNKNOWN），settle 时定项目正式写入——「先对话、后定项目」无痛。
- **16 条宪法（R1'~R16）**：Routing before Retrieval、Fail Closed、Multi-read / Single-write、稳定 ID + DROP、凭证绝不入库等。
- **机械守卫**：pre-commit hook 拦凭证 / S-ID 消失 / size 超限 / archive 不可改 / inbox 不可改。
- **防膨胀**：STATE ≤60 行 / 完成 8 条；CHANGELOG/DECISIONS 超阈值归档；STALE 只复核不自动删。

## 目录结构

```
ai-hub-memory/
├── MEMORY.json        # 路由表：项目注册 + staging 配置
├── STATE.md           # 全局索引（一行一项目）
├── AGENTS.md          # Agent 协议（读什么/写什么/时机判断）
├── global/            # 全局常读（Agent 启动装载）
│   ├── RULES.md       #   16 条宪法
│   ├── PROJECTS.md    #   5 仓库项目地图
│   ├── DECISIONS.md   #   全局决策
│   ├── RESOURCES.md   #   资源台账（What）
│   └── TOOLS.md       #   工具手册（How）
├── projects/          # 各项目记忆线
│   ├── teaching/        STATE/DECISIONS/CHANGELOG
│   ├── courseware/
│   ├── memory-system/
│   └── english-teaching/ english-learning/
├── inbox/             # 隔离暂存（pending/settled/receipts/META）
├── scripts/
│   ├── memory.py       #   唯一读写入口（11 命令）
│   ├── check_memory.py #   pre-commit hook
│   └── rotate_memory.py#   归档
└── skills/memory-router/SKILL.md  # Agent 行为协议
```

## 快速上手（Agent 视角）

### 读记忆（新项目单元开始）
```bash
gh repo clone 201650545/ai-hub-memory   # 或 git pull --ff-only
cd ai-hub-memory
# 依次读：global/PROJECTS.md → global/RULES.md → global/DECISIONS.md
# → projects/<你的项目>/STATE.md
```

### 写记忆（交付后）
```bash
# 单条
python scripts/memory.py write --project <id> --kind state --sid S-xxx --content "内容"
# 批量同步 Agent 记忆
python scripts/memory.py sync --project <id> --dir <记忆目录>
# 对话中不想定归属的候选记忆
python scripts/memory.py capture --capture-scope session:xxx --content "内容"
git add -A && git commit -m "memory: ..." && git push
```

## 常用命令

```bash
# 正式记忆
memory.py route --project <id> --kind state|decision|changelog
memory.py read --project <id> --file state|decision|changelog|staging
memory.py search --project <id> --query <关键词>
memory.py write --project <id> --kind state|decision --sid <S/D-ID> --content <内容>
memory.py validate
memory.py register --id <英文id> --name <中文名> --aliases <别名>   # 新建项目

# 隔离暂存
memory.py capture --capture-scope <scope> [--project-hint <id|UNKNOWN>] --content <内容>
memory.py status --settler
memory.py settle-plan --all
memory.py resolve --id <I-ID> --project <id> --basis user
memory.py settle --project <id> --dry-run

# 同步 Agent 记忆
memory.py sync --project <id> --dir <目录> [--dry-run]
```

## 关键文档

- `global/PROJECTS.md` — 5 仓库项目地图
- `global/RULES.md` — 16 条宪法
- `global/TOOLS.md` — 工具手册（gh/lark-cli/opencli/网关/夸克）
- `global/RESOURCES.md` — 资源台账
- `docs/Agent记忆同步操作文档_memory-sync.md` — 各 Agent 上报记忆
- `docs/Agent记忆上报指令.md` — 发给 Agent 的记忆上报指令模板

## 安全红线

- 凭证/key/token **绝不写入**任何记忆文件或 commit（hook 会拦）。
- 凭证误入历史 = key rotation（废弃 key），不是删文件。
- 只记认证方式（keyring/浏览器 session/人工扫码），不记认证材料。

---
由多 Agent 协作维护 · 记忆以项目为原子单元
