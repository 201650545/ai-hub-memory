# STATE.md — 当前状态（短期记忆）

> 单写者 + 整体覆盖，**不追加**。每次更新整页重写，保持一页能看完。

## 进行中
- **记忆机制问诊（进行中）**：已问 GPT「覆盖/主分记忆」架构（回复已落档）；「记忆备份/回退」问诊提示词已写好，**待 v4 Flash 执行问诊**（用户将切换 DeepSeek v4 Flash 去镜像站发问）。

## 已完成（最近）
- **门户资源清单雏形收尾**（2026-08-13）：ai-hub 00_中央平台/resources_bridge.py 数据桥链路复核通过（线上 GitHub Pages → /api/resources 实测返回 21 能力 + 21 实例，remote 源，manifest 字节校验 fail-closed 生效）；收尾修复 3 处——测试日期漂移 bug、LOCAL_DIR 路径解析、bridge 测试（18 用例）纳入 tests/run_all.py 回归；全量回归 36 通过 / 0 失败 / 4 跳过。已 push ai-hub 2d49b5e。
- **DeepSeek Harness 落地**（2026-08-13）：从源码装到 D:\DeepSeek\deepseek-harness（独立于 WorkBuddy）；Web UI :3080 跑通，headless 实测 API 通。
- **共享记忆读写协议落地**（2026-08-13）：AGENTS.md 增补「读写时机判断」；新增 交接命令.md 模板。
- 资源调查完成：10 类约 73 条资源，落 RESOURCES.md（2026-08-13）。
- 多 Agent 共享记忆骨架上线：https://github.com/201650545/ai-hub-memory（2026-08-13）。

## 卡点
- 无。

## 下一步
- v4 Flash 执行「记忆备份/回退」问诊 → 回复落档 ai-resource-hub docs/ai-advice/ → 提炼结论。
- 待用户拍板：是否落地「四文件 + UPDATES 保险层 + STATE 保留式更新」（GPT 建议的方案 A），还是先维持现状。
- 补 OpenCode Go / WorkBuddy 额度详情（待用户确认）。
