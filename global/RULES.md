# RULES.md — 全局规则（所有 Agent 必须遵守）

> 记忆系统 v2.1（Quarantined Ingress + Project-scoped Consolidation）。任何 Agent 接手任务前必须读本文件 + 对应项目 STATE。

## 记忆系统核心公式
Memory = Global Kernel + Project Namespace + Layered Retrieval + **Quarantined Ingress**；
**Routing before Retrieval**、**Multi-read / Single-write**、**Fail Closed**（定不了就拒绝，绝不猜）。

## 18 条宪法（v2.1 + R18 Memory Checkpoint）

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

R17. **决策优先级（GLM 审查 2026-08-14）**：项目域内冲突时**项目决策胜出**；global 只维护跨项目 invariant，不覆盖项目专属决策。项目决策要覆盖全局规则时，需显式声明「对全局 D-xxx 的项目内例外」。

R18. **自动记忆检查（Memory Checkpoint，GPT 评审 2026-08-15 定稿）**：出现以下任一事件时主动检查是否产生值得跨会话保留的信息——可交付单元完成、用户拍板决策、关键共享状态变化、Agent/会话交接；若连续约 10 个用户回合均未发生检查，则强制执行一次兜底检查。**检查不等于写入**：符合 R13「值不值得成为正式记忆」才写正式记忆——项目明确则用 memory.py write/checkpoint，项目未定则 capture，无新增价值则跳过。可控的会话结束/交接前必须执行 checkpoint；异常中断以最近一次成功 checkpoint 为恢复点。「轮」定义为「一个用户 prompt = 一个用户回合」，由平台生命周期 hook 机械计数（DSH onTurnCommitted / Claude Code UserPromptSubmit），不依赖模型自行数轮次。会话内由 Agent 生命周期事件触发的 checkpoint 不违反 R14（R14 禁止的是给 consolidation 搭建 cron/daemon 定时平台）。

**GLM 审查约定（2026-08-14）**：
- **调度器 M1 落位（R1）**：代码住 ai-hub 网关模块，数据读 ai-resource-hub（公开 JSON / 本地 credentials.json 信任平面），接口单向只读——M1 动工前按此约定。
- **数据桥收敛（R4，缓一步待办）**：飞书→GitHub Pages 双管道（exporter + feishu-data-hub）未来收敛为 feishu-data-hub 单管道；当前保留 exporter（已上线，ai-resource-hub 依赖），单独规划后再动。

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

## 问诊约定（D-GLOBAL-20260815-01 / D-GLOBAL-20260815-04）
- 上游/resource/架构现象搞不定或自行尝试多次仍无把握 → 转 GPT 镜像站（Thinking·Extended）问诊；**GPT 不可用 → 转 Kimi K3 兜底**（kimi.com 官网，提问前开 K3 思考进阶模式；Claude 额度已用光，不再转 Claude，D-GLOBAL-20260815-04）。
- 别埋头硬试：upstream 403/报错、免费档/价格、模型名/鉴权、厂商资源可用性等不确定判断，直接问最先进模型，用其结论复核再落地。
- 问诊操作一律经 **opencli** 操控浏览器执行（GPT 镜像站见操作手册 01；Kimi K3 见 global/TOOLS.md §4）。
- **问诊同频与实读证明（用户拍板 2026-08-27，强制）**：每完成一次镜像 GPT 问诊，必须先把本轮结论/状态变更 commit + push 到 GitHub 记忆仓库，再发起下一轮问诊——让 GPT 与仓库始终同频。问诊包必须明确要求 GPT **先读仓库真实内容**，并埋一个**只有实际读取该文件才能获得、无法从对话上下文猜出的核验令牌**，要求 GPT 在回复开头原文引用；引用不出即判定未实读，本轮问诊作废重问（或按上一条转 Kimi K3 兜底）。
- **CC Switch Takeover 边界（D-GLOBAL-20260828-02）**：在已验证的 CC Switch v3.14.1 中，启用本地 proxy 必须视为**会修改 Claude Code 全局配置并接管其出口**的操作。未经用户明确授权修改当前 Claude Code 链路，不得 enable/re-enable proxy；`live_takeover_active=0` **不得**作为"未接管"的判断依据。任何获批的 takeover 必须先保存可验证回退基线（settings SHA + provider 现状 + 代理状态 + 被改动配额原值），并在临时任务结束后恢复原态，或另行取得永久切流授权。

## 读写时机（原有协议保留）
- 新项目单元开始：读 RULES + 本项目 STATE + 相关 DECISIONS（+ 本项目 staging）。
- 可交付单元完成：正式记忆走 memory.py write；未定项目/会话中候选事实走 memory.py capture。
- 凭证/key 绝不进记忆文件或 commit。
- 改记忆前先 git pull --ff-only。

## global 的边界（克制！）
可以放：记忆系统规则、repo 约定、全 Agent 必须遵守的 invariant、真正跨所有项目的决策。
禁止放：任何单个项目的内容。判断标准：删除其中一个项目，这条记忆是否依然成立？否 → 不能进 global。
**唯一例外**：`global/PROJECTS.md` 为跨仓库 registry/index——仅允许记录项目身份、职责边界和项目间关系，不视为单项目正式记忆；项目状态与实现细节仍禁止进入 global。