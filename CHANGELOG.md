# CHANGELOG.md — 操作记录（只追加）

> 只追加。每个 Agent 干完写一条「谁 / 何时 / 做了什么」。

## 2026-08-14
- Claude：问诊 GPT（镜像站 vip-11 Thinking·Extended）「多 Agent 记忆覆盖/主分记忆」架构，回复落档 ai-resource-hub `docs/ai-advice/gpt56_问诊回复_记忆架构_2026-08-14.md`（结论：当前别上主+分，先用「四文件 + UPDATES 不可变事件保险层 + STATE 保留式更新」；未来几十 Agent 才演进 immutable events + 单写者 Memory Agent 投影）。已 push ai-resource-hub `347b951`。
- Claude：写好「记忆备份/回退」问诊提示词（含给 v4 Flash 的执行说明 + 给 GPT 的 5 问题），落 ai-resource-hub `docs/ai-advice/问诊_记忆备份回退_提示词_2026-08-14.md`，**待 v4 Flash 执行问诊**（用户将切换 DeepSeek v4 Flash 去镜像站发问）。

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
