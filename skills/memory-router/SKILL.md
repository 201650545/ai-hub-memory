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
python scripts/memory.py validate
```

## Fail Closed（R7，最重要）
scope 不明确 → 宁可少读/不写，绝不猜。报错：
> [memory] ERROR: unknown project_id / fail closed

## 项目路由表
见仓库根 MEMORY.json（teaching / courseware / memory-system + aliases）。

## 全局规则
所有 Agent 必须遵守 global/RULES.md（含 9 条宪法、读写时机、凭证红线）。
