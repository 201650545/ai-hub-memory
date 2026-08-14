# RULES.md — 全局规则（所有 Agent 必须遵守）

> 记忆系统 v2.1（Quarantined Ingress + Project-scoped Consolidation）。任何 Agent 接手任务前必须读本文件 + 对应项目 STATE。

## 记忆系统核心公式
Memory = Global Kernel + Project Namespace + Layered Retrieval + **Quarantined Ingress**；
**Routing before Retrieval**、**Multi-read / Single-write**、**Fail Closed**（定不了就拒绝，绝不猜）。

## 16 条宪法（v2.1）

R1'. 正式项目记忆的读取/搜索/写入/巩固必须携带明确 project_id；staging capture 不要求先确定 project_id，但必须携带 capture_scope，project_hint 可为已注册项目或 UNKNOWN。

R2. 正式记忆坚持 Routing before Retrieval：project_id 必须在读取项目正式记忆前唯一确定。staging capture 是唯一允许发生在项目路由完成前的持久化操作，但 staging 内容不得因此获得正式记忆权限。

R3. 普通项目 Agent 默认只能读：global + 当前项目正式记忆 + 当前项目 staging。提供 capture_scope 时可额外读该 scope 自己产生的 UNKNOWN。不得读其他项目 staging 或其他来源 UNKNOWN。

R4. 跨项目读取必须显式声明 read_scope/imports。UNKNOWN 全量扫描不属于普通跨项目读取能力，只有 settler/memory-router 在 consolidation 场景允许。

R5. 一次正式记忆操作只能有一个 write_scope。settle 必须指定且只能写一个 project_id；禁止一次 settle 同时修改多项目。staging capture/resolve 属 staging write_scope，不得夹带项目正式写入。

R6. Agent 不得指定实际记忆文件路径。正式路径由 Router 按 project+kind 决定；staging 路径由 Router 按 inbox id/date 决定。

R7. Fail Closed：正式 project scope 无法唯一确定时，宁可不读/不写/不 settle，绝不猜。纯内容语义判断只能形成 candidate_project，不得直接把 UNKNOWN 提升为正式 project_id。

R8. Archive 与 settled staging 均属冷历史，默认不可见。只有显式历史检索、审计或 consolidation 追溯才能进入。

R9. CHANGELOG、项目索引、staging receipt、META 等机械账本由脚本维护，Agent 不直接编辑。正式 memory write/settle 必须沿用脚本自动 CHANGELOG 记录。

R10. Staging 是 Quarantined Candidate Memory，不是正式共享记忆。UNKNOWN 表示「归属尚未确定」，绝不表示 GLOBAL/PUBLIC/所有项目可读。

R11. 普通项目 Agent 对 staging 的可见范围严格为：project_hint == current_project +（可选）capture_scope == current_scope 且 project_hint == UNKNOWN。默认禁止扫描全部 UNKNOWN。

R12. 只有 settler/memory-router 可全量扫描 UNKNOWN 并分类。确定性证据优先级：用户明确指定 > 已绑定 task/Skill > workspace/path > MEMORY.json alias。纯内容推理只能给 candidate；歧义留 UNKNOWN 并累积后批量询问用户。

R13. Consolidation 必须先判断「值不值得成为正式记忆」。candidate 可 promote / covered / discard。project/kind 未解决的 item 必须留在 pending，禁止为清空 inbox 强行分类写入。

R14. Consolidation 采用 Lazy Daily Consolidation，不建立 cron / GitHub Actions schedule / daemon / 其他定时平台。触发：会话/项目启动检查 + pending>=20 + UNKNOWN>=5 + 用户显式要求 + 存在前一日及更早 pending。到期只触发整理流程，不绕过 Fail Closed 自动猜 UNKNOWN。

R15. staging item 在 settle/discard 后不得无痕删除。原 candidate 移入 inbox/settled + 生成 receipt（disposition/final_project/kind/target_id/basis/时间）。settled 默认只读，修正通过新记录完成。

R16. 凭证/API key/token/secret 绝不进入任何 memory/staging 文件或 commit。capture 必须在文件落盘前执行 secret preflight 并 fail closed；pre-commit secret guard 作第二道防线。

## 命令
```bash
# 正式记忆
python scripts/memory.py route --project <id> --kind state|decision|changelog
python scripts/memory.py read --project <id> --file state|decision|changelog|staging [--capture-scope <scope>]
python scripts/memory.py search --project <id> --query <关键词>
python scripts/memory.py write --project <id> --kind state|decision --sid <S/D-ID> --content <内容>
python scripts/memory.py validate
python scripts/memory.py register --id <英文id> --name <中文名> --aliases <别名>

# 隔离记忆 staging
python scripts/memory.py capture --capture-scope <scope> [--project-hint <id|UNKNOWN>] [--kind-hint auto|state|decision] --content <内容>
python scripts/memory.py status (--settler | --project <id>) [--capture-scope <scope>]
python scripts/memory.py settle-plan (--all | --project <id>)
python scripts/memory.py resolve --id <I-ID> (--project <id> --basis ... | --candidate-project ... | --kind ... | --covered-by ... | --discard)
python scripts/memory.py settle --project <id> [--id <I-ID>] [--dry-run]
```

## 读写时机（原有协议保留）
- 新项目单元开始：读 RULES + 本项目 STATE + 相关 DECISIONS（+ 本项目 staging）。
- 可交付单元完成：正式记忆走 memory.py write；未定项目/会话中候选事实走 memory.py capture。
- 凭证/key 绝不进记忆文件或 commit。
- 改记忆前先 git pull --ff-only。

## global 的边界（克制！）
可以放：记忆系统规则、repo 约定、全 Agent 必须遵守的 invariant、真正跨所有项目的决策。
禁止放：任何单个项目的内容。判断标准：删除其中一个项目，这条记忆是否依然成立？否 → 不能进 global。
**唯一例外**：`global/PROJECTS.md` 为跨仓库 registry/index——仅允许记录项目身份、职责边界和项目间关系，不视为单项目正式记忆；项目状态与实现细节仍禁止进入 global。
