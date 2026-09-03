## 2026-08-15
- D-GLOBAL-20260815-01 新增：**自有知识解决不了 → 转问 GPT**（用户拍板）：Agent 对上游行为/资源/架构判断不定或自行试多次仍无把握时，转 GPT 镜像站 Thinking·Extended 问诊，故障转 Claude。落档 global/DECISIONS.md + global/RULES.md「问诊约定」。触发：API 集中转发任务中 UA 403/模型名/免费档判断靠埋头硬试耗时，GPT 一次给出完整方案（余额预检+熔断+免费渠道清单），印证该纪律价值。
# CHANGELOG.md — 操作记录（只追加）

> 只追加。每个 Agent 干完写一条「谁 / 何时 / 做了什么」。

## 2026-09-03
- [归档] DROP S-20260814-16 — 记忆线路由定稿，滚出「已完成」8 条窗口。
- Claude（调度大脑）：镜像版（vip-48 extend）咨询「Obsidian/GitHub/飞书 三角色定位」定稿 → 落 handbook `D:\通用规范\50-知识管理三工具规范.md`（单写真源法则 / Owner Source 表 / 2-vault / 四坑）。同时把 D:\记忆 README 由「本地=缓存+飞书双轨」修正为「D:\记忆=唯一秘密 canonical → GitHub yongtai-memory=镜像，飞书退出记忆主链（仅审计）」，Home.md 同口径，已 push yongtai-memory。新增 5 条 Claude 记忆入镜像（延长 extend/烧网关/DeepSeek Harness/浏览器元素定位/镜像生成器+下载自存）并补索引。
- Claude（调度大脑）：记忆项目审计修正——v2.8 限时执行位（GLM 5.3 flash 1 亿 token）已于 2026-09-02 到期，project_v28_execution_phase 改「历史阶段」口径，三大待办留待确认是否闭环；同步 Claude 记忆 + D:\记忆 镜像。

## 2026-08-21
- [归档] DROP S-20260814-19 — 记忆系统 v2.1 升级完成（S-20260814-21 已确认 v2.1 落地），"进行中"→"已完成"。
- [归档] DROP S-20260814-17 — 落地记忆系统 v2.1 全部 6 项优先级已由 S-20260814-21 完成，从"下一步"移除。
- [归档] DROP S-20260814-13 — 记忆生命周期方案落地，滚出「已完成」8 条窗口。
- [归档] DROP S-20260814-11 — 记忆膨胀/精简问诊（实读版），滚出「已完成」8 条窗口。
- DeepSeek Harness Agent：验证 v2.1 全部组件已落地——MEMORY.json v2.1 ✓ / memory.py 5 新命令 ✓ / inbox/ ✓ / RULES 16 宪法 ✓ / SKILL.md ✓ / check_memory.py ✓ / rotate_memory.py ✓ / 验收测试通过 ✓。唯一缺失：pre-commit hook 未安装（脚本存在但 .git/hooks/pre-commit 是 .sample）。已安装 pre-commit hook（链接 check_memory.py）。更新 memory-system STATE.md 消除"进行中"与"已完成"的矛盾。

## 2026-08-14
- [归档] DROP S-20260814-01 — 记忆系统 v2 升级完成，滚出「已完成」8 条窗口。
- [归档] DROP S-20260814-09 — 记忆守卫落地完成，滚出「已完成」8 条窗口。
- v4 Flash：确认多 Agent 记忆上报完成——各 Agent 按上报指令同步，**新建 2 个项目**：english-teaching（英语教学：3 学生 + 新优生黄浩昀计划/诊断/3+2 改革）+ english-learning（英语学习：FSRS 调度字段落地/8 条规则/阶段三分析）；另有 Agent 补 capture 兜底 + inbox 占位。MEMORY.json 现注册 5 项目（teaching/courseware/memory-system/english-teaching/english-learning），validate 通过。提交见远端 `fbcb97b`/`e4ae45b`/`9f7c225`/`be9b83e`。
- v4 Flash：落地 GLM 审查 9 条建议（按用户批准）——R2 write/settle 内置强制 git pull --ff-only（Fail-Closed 同构）✓ R3 RESOURCES.md 头部指针化声明（额度数值真源归 ai-resource-hub）✓ R5 PROJECTS 路由补 courseware 行 + teaching/courseware↔english-teaching 映射 ✓ R6 AGENTS/TOOLS 端口路径改指针 ✓ R7 RULES 加 R17 决策优先级 ✓ R8 status 加 inbox 超阈值停留提醒 ✓ R9 TOOLS 加公开数据消费规范 ✓ R1/R4 调度器落位约定 + 数据桥收敛待办记录。push `eb9ae94`。
- v4 Flash：GLM5.3 架构审查报告落档（Trae 侧执行，实核本地仓库）——总评「方向正确不需重构，问题在重不在缺」；4 实质问题：F1 双管道（exporter vs feishu-data-hub）/ F2 资源台账双真源（RESOURCES.md 额度快照）/ F3 并发写防护未下沉脚本 / 决策优先级缺失；9 条建议 R1-R9（P0：write/settle 内置强制 pull + RESOURCES 指针化 + 数据桥收敛；P1：路由表补全 + TOOLS 去快照化 + 决策优先级；P2：调度器落位约定 + status 提醒 + 消费规范）。落档 ai-resource-hub `fc168f4`。**3 决策点待用户拍板**（数据桥收敛方向 / RESOURCES 指针化 / 调度器 M1 落位）。
- v4 Flash：GPT 审查 PROJECTS 全景方案（实读确认）→ 采纳 5 分法（RULES=MUST/PROJECTS=WHERE/RESOURCES=WHAT/TOOLS=HOW/STATE=NOW）+ PROJECTS 瘦身为纯路由图（29 行，删状态/版本/端口）+ RULES 补跨仓库 registry 例外；拍板 3 点（例外/global_read 保留/删状态字段）落地 push `1dfda9b`。落档 ai-resource-hub `464a5ac`。
- v4 Flash：新增 `global/PROJECTS.md` 项目全景（5 GitHub 仓库完整介绍：ai-hub-memory/ai-resource-hub/ai-hub/feishu-data-hub/english-teaching-production + 关系图 + Agent 提示）——**进入记忆常读层**（MEMORY.json global_read + 根 STATE 导航 + AGENTS 读清单），任何 Agent 读记忆即懂全局，无需翻各仓库。push `165b3e2`。
- v4 Flash：交付 `memory.py sync` 记忆同步命令——Agent 把各自项目的记忆批量导入 ai-hub-memory（单文件 --file / 批量 --dir；自动判断 state/decision；生成稳定 ID 写 STATE/DECISIONS + 自动 CHANGELOG；R16 secret preflight；--dry-run 预览）；SKILL.md + 交接命令同步用法。push ai-hub-memory `cfdecb1`。另生成《架构浓缩包》（docs/架构浓缩包_GLM审查_2026-08-14.md，供 GLM5.3 单文件审查省资源），push `3491106`。
- v4 Flash：安装并验证夸克网盘 Skill（官方 install.sh 确认已是最新 1.0.11，服务端地址与用户提供一致；无需覆盖，qk-list.cjs 未受影响）；授权已有效（config.json 有 currentUserId + accessToken）；端到端实测 qk-list 列根目录成功（17 文件夹 + 4 文件：6-奥数/7-课本/3-初中英语/教资 等）。备份 qk-list.cjs 于 D:\DeepSeek\qk-list.cjs.bak。
- v4 Flash：新增工具能力「夸克网盘列目录（qk-list）」——操作文档（D:\项目\docs\夸克网盘列目录_qk-list_操作文档.md）已验证（skill 目录存在、qk-list.cjs node --check 通过、凭证路径与文档一致）；按 TOOLS.md HOW 定位写入 §6（用途/命令/自检/STOP/坑/指向原文档），凭证值零泄漏；AGENTS §3 保持单一真源。push ai-hub-memory `2a1dc23`。
- v4 Flash：建 global/TOOLS.md 工具手册（三大工具 gh/lark-cli/opencli + 网关 :3000），GPT 优化后 V2（任务速查 + 首次使用检查 + 工具操作卡 + STOP 原则 + 安全红线扩展 + 三层分离 TOOLS=How/RESOURCES=What/projects=Why）；AGENTS §3 精简为只留 TOOLS.md 引用（消除 4/5 引擎漂移）。落档 ai-resource-hub `ee302d9`，push ai-hub-memory `2df5a12`。
- v4 Flash：问诊 GPT「隔离记忆」并在同一对话完成 3 轮闭环——GPT 确认实读仓库（24 处引用 + MEMORY.json/RULES/memory.py 独有内容）；我方代表用户拍板 4 点（UNKNOWN 仅 settler 可全扫 / R1→R1' / lazy daily 不建定时 / 语义只给候选）；GPT 出 **v2.1 定稿**（20484 字）：16 条宪法 R1'~R16 + inbox/（pending/settled/receipts/META）+ memory.py 5 新命令（capture/status/settle-plan/resolve/settle）+ 读取过滤公式 + 验收测试 + 2 个 v2 遗留修复。落档 ai-resource-hub `ad40620`（gpt56_问诊回复_隔离记忆_v21定稿_2026-08-14.md）。**待落地 v2.1**。
- [归档] DROP S-20260814-03 — 记忆备份/回退问诊（未读版）完成，被实读版 S-20260814-02 取代，滚出窗口。
- [归档] DROP S-20260814-14 — 落地多项目隔离被并入记忆系统 v2（S-20260814-17），滚出窗口。
- [归档] DROP S-20260813-04 — 记忆覆盖/主分记忆问诊完成，滚出「已完成」8 条窗口，细节保留于本流水与落档。
- [归档] DROP S-20260814-12 — 落地记忆生命周期完成（已并入 S-20260814-13 交付），滚出窗口。
- [归档] DROP S-20260813-05 — 门户资源清单雏形收尾完成，滚出「已完成」8 条窗口，细节保留于本流水。
- v4 Flash：多模型交叉问诊「记忆线/记忆路由」——AI 搜索网关（元宝）+ Claude Sonnet5（#2）+ GPT-5.6 Extended（#2）三方意见高度一致：**项目作用域隔离 + 分层记忆 + Routing-before-Retrieval + Fail-Closed**。GPT 定稿：新增 MEMORY.json（路由表）+ memory.py（唯一读写路由器）+ memory-router/SKILL.md（行为协议），现有三件套移入 projects/<project_id>/；核心公式「Memory = Global Kernel + Project Namespace + Layered Retrieval；Routing before Retrieval，Multi-read/Single-write，Fail Closed」。落档 ai-resource-hub（claude `dc087d6` + gpt `0c46589`）。**待按此方案升级记忆系统 v2**。
- v4 Flash：问诊「多 Agent 多项目记忆隔离」——GPT 镜像站账号池当日故障（vip-11 实读空回复/vip-15/17 菜单打不开/vip-12 无回复），按手册 00 兜底转 **Claude Sonnet 5** 交叉校验，回复 5103 字落档 ai-resource-hub `docs/ai-advice/claude_sonnet5_问诊回复_多项目记忆隔离_2026-08-14.md`。核心结论：**STATE 用方案 B（索引页 STATE.md + 每项目页 STATE/<项目>.md，预算下沉每项目独立）**；DECISIONS/CHANGELOG 用方案 A（强制 [全局]/[项目:xx] 标签 + 脚本过滤，不物理拆分）；S-ID 改 `S-<项目码>-日期-NN`（存量无前缀不回填，归属记忆系统项目）；hook 改逐文件 glob 检测 + 索引页保护；新读取协议 = 索引页 + 本项目页 + decisions-for.sh。已 push ai-resource-hub `216eb76`。
- v4 Flash：落地**记忆生命周期**（膨胀方案 D-20260814-02 拍板后执行）——AGENTS.md 新增 §2.5「记忆生命周期/归档」（STATE 60 行/12KiB/完成 8 条硬限额 + ROTATE 例外 + CHANGELOG 200 条归档 + DECISIONS D-ID + STALE 时效）；check_memory.py 扩展 4 组检查（size guard/归档阈值/archive 锁/STALE）；新增 scripts/rotate_memory.py（changelog/decisions 显式归档，不自动 commit）；DECISIONS 加 D-ID 体系。待验证 + push。
- [归档] DROP S-20260813-06 — DeepSeek Harness 落地完成，滚出「已完成」8 条窗口，细节保留于本流水。
- [归档] DROP S-20260813-07 — 共享记忆读写协议落地完成，滚出窗口，细节保留于本流水。
- [归档] DROP S-20260813-08 — 资源调查完成，滚出窗口，细节保留于 RESOURCES.md。

- v4 Flash：落地**记忆守卫**（实读版 GPT 方案拍板后执行）——AGENTS.md 写入协议升级（ff-only/保留式更新/禁 force push/S-ID+DROP 规则/凭证机械阻止/key rotation）；新增 pre-commit hook（scripts/check_memory.py：凭证扫描 + STATE S-ID 消失检测，三项测试全过——无 DROP 删 ID 拦截 ✓ / 有 DROP 删除通过 ✓ / 凭证进入暂存拦截 ✓）；STATE.md 全部状态项加稳定 S-ID + 来源指纹；.gitignore 屏蔽凭证；交接命令.md 同步新协议。已 push ai-hub-memory `ad731a1`。
- v4 Flash：问诊 GPT「记忆膨胀/精简/生命周期」（vip-12 Extended，强制实读，回复 8587 字确认实读——核对当前 STATE 22 行/已完成 7 条），落档 ai-resource-hub `docs/ai-advice/gpt56_问诊回复_记忆膨胀精简_2026-08-14.md`。核心：① append-only 重定义为「记录 immutable，ROTATE 是唯一例外」（同 commit 原样进 archive）② STATE 硬限额 60 行/12KiB/最近完成 8 条，超窗口 DROP 进 CHANGELOG，不建 STATE archive ③ CHANGELOG 200 条触发归档到 archive/changelog/ ④ DECISIONS 80 条低频归档 + 增 D-ID + SUPERSEDES ⑤ 时效 = S-ID 用 Git 最后修改时间报 STALE（只 warning 不删）。push ai-resource-hub `bf8a4d9`。
- Claude：问诊 GPT（镜像站 vip-11 Thinking·Extended）「多 Agent 记忆覆盖/主分记忆」架构，回复落档 ai-resource-hub `docs/ai-advice/gpt56_问诊回复_记忆架构_2026-08-14.md`（结论：当前别上主+分，先用「四文件 + UPDATES 不可变事件保险层 + STATE 保留式更新」；未来几十 Agent 才演进 immutable events + 单写者 Memory Agent 投影）。已 push ai-resource-hub `347b951`。
- Claude：写好「记忆备份/回退」问诊提示词（含给 v4 Flash 的执行说明 + 给 GPT 的 5 问题），落 ai-resource-hub `docs/ai-advice/问诊_记忆备份回退_提示词_2026-08-14.md`，**待 v4 Flash 执行问诊**（用户将切换 DeepSeek v4 Flash 去镜像站发问）。
- v4 Flash：执行「记忆备份/回退」问诊——按用户指示核实 Thinking·Extended（effort=Extended 确认 checked）；首次 Thinking·Standard 仅得 570 字截断回复，切 Extended 重发得完整版（5324 字）；回复落档 ai-resource-hub `docs/ai-advice/gpt56_问诊回复_记忆备份回退_2026-08-14.md`（核心结论：不做额外备份服务，强化「可证明地重建」——UPDATES 不可变事件层 + STATE 顶部来源指纹检测语义覆盖 + 事件重放优先于 git checkout；凭证走 key rotation 而非删历史）。已 push ai-resource-hub `024467b`。
- v4 Flash：应用户要求重发「记忆备份/回退」问诊为**强制实读版**——单链接（AGENTS.md raw）+ 强制实读指令；GPT 回复 4537 字且**确认实读**（引用标记 GitHub +1 / git-scm.com +1 / oaicite + 引用 AGENTS.md §0/§1/§2/§6 原文），落档 ai-resource-hub docs/ai-advice/gpt56_问诊回复_记忆备份回退_实读版_2026-08-14.md（**替代未读版**）。核心新增结论：STATE 状态项加稳定 ID（S-xxx），任何 ID 消失必须 CHANGELOG 追加 DROP，pre-commit hook 机械拦截；回退禁用 reset --hard + force push，优先 git revert / restore --source；备份只加按需 git bundle。已 push ai-resource-hub e3478e2。

## 2026-08-13
- Claude：接手「门户资源清单雏形」收尾——复核 ai-hub `00_中央平台/resources_bridge.py` 数据桥链路（线上 GitHub Pages 实测返回 21 能力+21 实例）；修复 3 处：① 测试日期漂移（make_index 硬编码 2026-08-11 超 48h 新鲜期致 test_remote_ok 失败 → 改动态当前时间）② `LOCAL_DIR` 路径解析错误（原指向不存在的 `ai-hub/ai-resource-hub/public`，改环境变量+多候选探测，实测命中 `D:\项目\ai-resource-hub\public`）③ 将 test_resources_bridge（18 用例）纳入 `tests/run_all.py` 回归套件；全量回归 36 通过/0 失败/4 跳过（4 跳过为历史遗留共享组件缺失），已 push ai-hub `2d49b5e`。
- Claude：问诊 GPT（镜像站 Extended）多 Agent 共享记忆方案，回复存档 `docs/问诊_多Agent共享记忆_20260813.md`。
- Claude：搭共享记忆 4 文件骨架（AGENTS/STATE/DECISIONS/CHANGELOG）。
- Claude：创建公开仓库 `ai-hub-memory` 并推送骨架（https://github.com/201650545/ai-hub-memory）。
- Claude：写资源调查任务书（分类交互式提问），交接给执行 AI。
- Claude：复核执行 AI 资源调查台账（纠正 OpenCode Go 档位、补 AI问答宝实情），落 `RESOURCES.md`。
- Claude：按用户确认再修正——WorkBuddy（=WorkBodySolo）非 Pro 会员（Trae Work 才是），OpenCode Go 额度规则确认。
- Claude：DeepSeek Harness 从源码装到 `D:\DeepSeek\deepseek-harness`（独立于 WorkBuddy），官方 key 填 `.env`，Web UI `:3080` 跑通 + headless 实测 API 通。
- Claude：AGENTS.md 增补「读写时机判断」规则（新项目开始前读、单元交付后写），新增 `交接命令.md` 可复制模板。

## 2026-08-12
- Claude：重构编排器画布为苹果浅色 + 加深色切换按钮。
- D-20260814-01 用户拍板 v2.1：隔离记忆机制（Quarantined Ingress），普通 Agent 不读全部 UNKNOWN，（2026-08-14，脚本自动记录）
- D-20260814-02 用户原则：对话内容本身就是记忆，Agent 代表用户与外部 AI 对话并控制在 3 轮内定稿，不反复（2026-08-14，脚本自动记录）
- S-20260814-21 v2.1 已落地：MEMORY.json v2.1 + memory.py 5 新命令 + inbox/ + RULES（2026-08-14，脚本自动记录）- D-GLOBAL-20260815-02 代表用户执行（用户 2026-08-15 拍板，对 D-GLOBAL-20260813-03 的项目内例外）：用户不懂技（2026-08-15，脚本自动记录）
- S-20260815-01 读记忆响应协议 GPT 复核结论（2026-08-15，Thinking·Extended 实读）：README+AGE（2026-08-15，脚本自动记录）
- [归档] DROP S-20260814-02 — 记忆备份/回退问诊（实读版）完成并入后续，滚出「已完成」8 条窗口。
- [归档] DROP S-20260814-15 — STATE「已完成(最近)」超限旧项下沉，全文见 archive/projects/memory-system/2026/2026-08-30.md。（2026-08-30，pre-commit 拦截修复）
