# STATE.md — 当前状态（短期记忆）

> 单写者 + 整体覆盖，**不追加**。每次更新整页重写，保持一页能看完。

## 进行中
- （无）

## 已完成（最近）
- **DeepSeek Harness 落地**（2026-08-13）：从源码 git clone 装到 `D:\DeepSeek\deepseek-harness`（独立于 WorkBuddy）；pnpm 11.7 + node 24 编译 native 模块，解决此前搬包 ABI 不匹配问题；官方 key 从 Cherry Studio 读入 `.env`（gitignored）；Web UI `:3080` 跑通，headless 实测真实 API 返回正常。启动：`cd D:\DeepSeek\deepseek-harness && node --import tsx/esm apps/cli/src/bin.ts web`。
- **共享记忆读写协议落地**（2026-08-13）：AGENTS.md 增补「读写时机判断」（新项目开始前读、单元交付后写）；新增 `交接命令.md`（可直接复制给任何 Agent 的模板）。
- 资源调查完成：10 类约 73 条资源，落 `RESOURCES.md`（2026-08-13）。
- 多 Agent 共享记忆骨架上线：https://github.com/201650545/ai-hub-memory（2026-08-13）。
- 前端重构：5 个前端统一苹果浅色风 + 深色切换按钮（2026-08-12）。

## 卡点
- 无。

## 下一步
- 补 OpenCode Go / WorkBuddy 额度详情（待用户确认）。
- 门户资源清单雏形（`D:\项目\00_中央平台` 接入 ai-resource-hub 资源表，方案已备）。
