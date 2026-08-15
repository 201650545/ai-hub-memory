---
name: memory-router
description: 多 Agent 多项目共享记忆路由协议。任何 Agent 在读写 ai-hub-memory 记忆前必须加载本 Skill，按 R1-R9 确定项目作用域并调用 memory.py，杜绝跨项目串读/串写。
---

# memory-router — 记忆路由协议

## 核心公式
Memory = Global Kernel + Project Namespace + Layered Retrieval
**Routing before Retrieval**（先定项目再读记忆）· **Multi-read / Single-write** · **Fail Closed**

## 第一步：确定 project_id（R1/R2）
按以下优先级（顺序判定，无法唯一确定就 fail closed）：
1. 调用时显式 --project 参数
2. 当前任务/Skill 已绑定 project_id
3. workspace/path → MEMORY.json 映射
4. 别名唯一匹配（MEMORY.json aliases，如 教学/课件/记忆系统）
5. 无法唯一确定 → 拒绝读写，报告用户要求明确项目

## 读（R3/R4/R8）
**入口（R18，2026-08-15 起）**：进入项目记忆线用 `python scripts/memory.py bootstrap --project <id>`——一次性注入 R18 Checkpoint 规则 + 项目 STATE/DECISIONS + 可见 staging + MEMORY_PROJECT_ID/MEMORY_CHECKPOINT_POLICY 绑定变量，替代分别 read RULES/STATE/DECISIONS。
默认只读：global/RULES.md + global/DECISIONS.md + projects/<当前项目>/*
跨项目读必须显式声明（LINKS.json / imports）——默认禁止。
深度读取顺序（page fault）：STATE → DECISIONS → CHANGELOG → archive（archive 默认不可见）。

## 写（R5/R6/R9）
- 一次操作只能有一个 write_scope（单写）。
- **Agent 不指定文件路径**，只声明 project + kind + sid + content，路径由 memory.py 决定。
- CHANGELOG 和 INDEX 由脚本自动维护，Agent 不直接编辑。
- 凭证/key 绝不写入任何记忆文件。

## 命令
```bash
python scripts/memory.py route --project <id> --kind state|decision   # 查看路由路径
python scripts/memory.py read --project <id> --file state|decision|changelog
python scripts/memory.py search --project <id> --query <关键词>
python scripts/memory.py write --project <id> --kind state|decision --sid S-xxx --content <内容>
python scripts/memory.py checkpoint --project <id> --kind state|decision --content <内容> [--checkpoint-id <session>:<turn>]  # R18：幂等保存 + 自动 commit/push（推荐日常自动保存用这个）
python scripts/memory.py validate

# 隔离记忆 staging（v2.1）
python scripts/memory.py capture --capture-scope <scope> [--project-hint <id|UNKNOWN>] --content <内容>
python scripts/memory.py status --settler   # 仅 settler 可全量查看
python scripts/memory.py settle-plan --all   # 只读规划
python scripts/memory.py resolve --id <I-ID> --project <id> --basis user  # 或 --discard / --covered-by
python scripts/memory.py settle --project <id> --dry-run   # 单项目晋升

# 同步 Agent 记忆（把 Agent 各自项目的记忆导入 ai-hub-memory）
python scripts/memory.py sync --project <id> --file <来源.md> [--kind auto|state|decision] [--dry-run]
python scripts/memory.py sync --project <id> --dir <目录> [--kind auto] [--dry-run]   # 批量
```

## Fail Closed（R7，最重要）
scope 不明确 → 正式项目记忆：宁可少读/不写，绝不猜。但**可以 capture 到隔离区**（v2.1）：
- 无法唯一确定 project_id → 正式记忆 Fail Closed；
- 但产生值得跨会话保留的候选事实 → 允许 `memory.py capture`（project_hint=UNKNOWN）；
- UNKNOWN 内容不得获得正式项目记忆权限，不得读其他项目线。

## 项目路由表
见仓库根 MEMORY.json（teaching / courseware / memory-system + aliases）。


## 新项目流程（先对话，后定项目）

用户开启一个新任务时，**不需要提前在仓库建项目**。流程：

1. **对话开始时**：按 R1-R7 判断 project_id——MEMORY.json 有匹配项目 → 走该项目记忆线；**没有匹配** → 只读 global/（RULES+DECISIONS），正常干活，不读/不写任何项目线（fail-closed，不猜）。
2. **对话中**：正常执行任务，不写记忆（任务未完成/项目未定）。
3. **对话结束、确定是新项目**：用户说「记为新项目 XX」或你判断这确实是个独立项目 → 运行：
   ```bash
   python scripts/memory.py register --id <英文id> --name <中文名> --aliases <别名1,别名2>
   git add -A && git commit -m "memory: register project <id>" && git push
   ```
4. **之后**：该项目拥有独立记忆线，后续读写走正常路由。

判断新项目（和已有项目的边界）：
- 已有教学/课件/记忆系统 → 复用，不新建。
- 明确的新领域/新目标（如英语教学、毕业设计）→ 新建。
- 拿不准 → 问用户确认，不擅自建。

## 全局规则
所有 Agent 必须遵守 global/RULES.md（含 9 条宪法、读写时机、凭证红线）。
