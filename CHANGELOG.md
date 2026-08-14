# CHANGELOG.md — 操作记录（只追加）

> 只追加。每个 Agent 干完写一条「谁 / 何时 / 做了什么」。

## 2026-08-14

- v4 Flash：落地**记忆守卫**（实读版 GPT 方案拍板后执行）——AGENTS.md 写入协议升级（ff-only/保留式更新/禁 force push/S-ID+DROP 规则/凭证机械阻止/key rotation）；新增 pre-commit hook（scripts/check_memory.py：凭证扫描 + STATE S-ID 消失检测，三项测试全过——无 DROP 删 ID 拦截 ✓ / 有 DROP 删除通过 ✓ / 凭证进入暂存拦截 ✓）；STATE.md 全部状态项加稳定 S-ID + 来源指纹；.gitignore 屏蔽凭证；交接命令.md 同步新协议。已 push ai-hub-memory `ad731a1`。
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
