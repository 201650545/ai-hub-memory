# STATE.md — 当前状态（短期记忆）

> 单写者 + 整体覆盖，**不追加**。每次更新整页重写，保持一页能看完。

## 进行中
- **记忆机制改造（待用户拍板）**：三轮 GPT 问诊完成（覆盖/主分记忆 + 备份/回退未读版 + 备份/回退实读版），最新**实读版**结论最可信；是否落地等用户决定。

## 已完成（最近）
- **记忆备份/回退问诊（实读版）**（2026-08-14，v4 Flash）：单链接强制实读 AGENTS.md 后 GPT 回复 4537 字，**确认实读**（GitHub +1 / git-scm +1 / oaicite 引用标记 + AGENTS.md §0/§1/§2/§6 原文引用），落档 ai-resource-hub `docs/ai-advice/gpt56_问诊回复_记忆备份回退_实读版_2026-08-14.md`（替代未读版）。核心：① 备份 = Git + GitHub 已够，只加按需 git bundle（不做定时备份）② 发现语义覆盖 = STATE 状态项加稳定 ID（S-xxx）+ 消失必 DROP + pre-commit hook 机械拦截 ③ 回退 = 禁 reset --hard + force push，优先 git revert / restore --source ④ 局部恢复 = git show 找旧条 + 手工插回 + RESTORE 事件 ⑤ 凭证 = credentials.json 必须 untracked/.gitignore + commit 前机械阻止 + key rotation。已 push ai-resource-hub `e3478e2`。
- **记忆备份/回退问诊（未读版）**（2026-08-14，v4 Flash）：GPT-5.6 Extended 回复 5324 字落档（未实读仓库，方向与实读版一致但缺细节），已 push `024467b`。
- **记忆覆盖/主分记忆问诊**（2026-08-13）：GPT 回复落档 `docs/ai-advice/gpt56_问诊回复_记忆架构_2026-08-14.md`。结论：当前别上主+分记忆，先「四文件 + UPDATES 保险层 + STATE 保留式更新」。
- **门户资源清单雏形收尾**（2026-08-13）：ai-hub 数据桥复核通过，修复 3 处，全量回归 36 过/0 败/4 跳。push `2d49b5e`。
- **DeepSeek Harness 落地**（2026-08-13）：源码装 D:\DeepSeek\deepseek-harness，Web UI :3080 跑通。
- **共享记忆读写协议落地**（2026-08-13）：AGENTS.md 增补读写时机判断；新增 交接命令.md。
- 资源调查完成：10 类约 73 条资源，落 RESOURCES.md（2026-08-13）。

## 卡点
- 无。

## 下一步
- 用户拍板记忆机制改造方案（实读版 GPT 建议：STATE 加稳定 ID + DROP 记录 + pre-commit hook + 按需 git bundle；或维持现状），拍板后落地 AGENTS.md/文件结构。
- 补 OpenCode Go / WorkBuddy 额度详情（待用户确认）。
