# STATE.md — 当前状态（短期记忆）

> 单写者 + 整体覆盖，**不追加**。每次更新整页重写，保持一页能看完。

## 进行中
- **记忆机制改造（待用户拍板）**：两轮 GPT 问诊已完成（覆盖/主分记忆 + 备份/回退），结论一致指向「四文件 + UPDATES 不可变事件层 + STATE 保留式更新/来源指纹检测」；是否落地等用户决定。

## 已完成（最近）
- **记忆备份/回退问诊**（2026-08-14，v4 Flash 执行）：GPT-5.6 Thinking·Extended 完整回复（5324 字）落档 ai-resource-hub docs/ai-advice/gpt56_问诊回复_记忆备份回退_2026-08-14.md。核心结论：① 不做额外备份服务（Git + GitHub 已够，备份解决不了语义覆盖）② 发现机制 = STATE 顶部存 source_event_until/source_commit + UPDATES 事件清单 diff ③ 恢复 = 事件重放优先，git checkout/revert 仅限仓库级灾难/单错误 commit ④ 局部恢复 = 新增 repair 事件而非回滚 STATE ⑤ 凭证误入 = key rotation 而非删历史（历史不可逆），凭证不进记忆仓库。已 push ai-resource-hub 024467b。
- **记忆覆盖/主分记忆问诊**（2026-08-13）：GPT 回复落档 docs/ai-advice/gpt56_问诊回复_记忆架构_2026-08-14.md。结论：当前别上主+分记忆（按 Agent 分片是错的，应按不可变 event 分）；先「四文件 + UPDATES 保险层 + STATE 保留式更新」；未来几十 Agent 才演进 immutable events + 单写者 Memory Agent 投影。
- **门户资源清单雏形收尾**（2026-08-13）：ai-hub 数据桥链路复核通过，修复测试日期漂移/LOCAL_DIR 路径/bridge 测试纳入回归；全量回归 36 通过/0 失败/4 跳过。已 push ai-hub 2d49b5e。
- **DeepSeek Harness 落地**（2026-08-13）：源码装到 D:\DeepSeek\deepseek-harness，Web UI :3080 跑通。
- **共享记忆读写协议落地**（2026-08-13）：AGENTS.md 增补「读写时机判断」；新增 交接命令.md。
- 资源调查完成：10 类约 73 条资源，落 RESOURCES.md（2026-08-13）。

## 卡点
- 无。

## 下一步
- 用户拍板记忆机制改造方案（A：四文件 + UPDATES 保险层 + STATE 来源指纹；B：维持现状；C：其他），拍板后落地 AGENTS.md/文件结构。
- 补 OpenCode Go / WorkBuddy 额度详情（待用户确认）。
