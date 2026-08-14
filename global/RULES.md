# RULES.md — 全局规则（所有 Agent 必须遵守）

> 这是记忆系统 v2 的 Global Kernel。任何 Agent 接手任务前必须读本文件 + 对应项目的 STATE。

## 记忆系统核心公式
Memory = Global Kernel + Project Namespace + Layered Retrieval；
**Routing before Retrieval**（先定项目再读记忆）、**Multi-read / Single-write**、**Fail Closed**（定不了就拒绝，绝不猜）。

## 9 条宪法
R1. 每次记忆操作必须带 project_id。
R2. project_id 在检索之前确定。
R3. 默认只能读取 global + 当前项目。
R4. 跨项目读取必须显式声明 read_scope/imports。
R5. 一次操作只能有一个 write_scope。
R6. Agent 不指定记忆文件路径，Router 根据 project+kind 决定。
R7. scope 不明确时 fail closed：宁可少读，不能猜着读/写。
R8. Archive 默认不可见，只有显式历史检索才进入。
R9. CHANGELOG 和 INDEX 由脚本维护，Agent 不直接编辑。

## 所有持久记忆操作必须走 memory.py
python scripts/memory.py read --project <id>
python scripts/memory.py search --project <id> --query <关键词>
python scripts/memory.py write --project <id> --kind state|decision --sid <S-ID> --content <内容>
python scripts/memory.py validate
python scripts/memory.py register --id <英文id> --name <中文名> --aliases <别名>   # 一键新建项目（先对话后注册）

## 读写时机（原有协议保留）
- 新项目单元开始时：读 RULES + 本项目 STATE + 相关 DECISIONS。
- 可交付单元完成后：memory.py write 写一次。
- 凭证/key 绝不进记忆文件或 commit。
- 改记忆前先 git pull --ff-only。

## global 的边界（克制！）
可以放：记忆系统规则、repo 约定、全 Agent 必须遵守的 invariant、真正跨所有项目的决策。
禁止放：任何单个项目的内容（教学素材/课件状态/某项目 TODO）。
判断标准：删除其中一个项目，这条记忆是否依然成立？否 → 不能进 global。
