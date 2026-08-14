# STATE.md — 当前状态（短期记忆）

> 单写者 + 整体覆盖，**不追加**。每次更新整页重写，保持一页能看完。

## 进行中
- 无（待用户指派下一单元）。

## 已完成（最近）
- **门户资源清单雏形收尾**（2026-08-13）：ai-hub 00_中央平台/resources_bridge.py 数据桥链路复核通过（线上 GitHub Pages → /api/resources 实测返回 21 能力 + 21 实例，remote 源，manifest 字节校验 fail-closed 生效）；收尾修复 3 处——测试日期漂移 bug、LOCAL_DIR 路径解析（环境变量 + 多候选，实测命中 D:\项目\ai-resource-hub\public 本地回退）、bridge 测试（18 用例）纳入 tests/run_all.py 回归；全量回归 36 通过 / 0 失败 / 4 跳过（4 跳过 = 历史遗留共享组件缺失）。已 push ai-hub 2d49b5e。
- **DeepSeek Harness 落地**（2026-08-13）：从源码 git clone 装到 D:\DeepSeek\deepseek-harness（独立于 WorkBuddy）；pnpm 11.7 + node 24 编译 native 模块，解决此前搬包 ABI 不匹配问题；官方 key 从 Cherry Studio 读入 .env（gitignored）；Web UI :3080 跑通，headless 实测真实 API 返回正常。启动：cd D:\DeepSeek\deepseek-harness && node --import tsx/esm apps/cli/src/bin.ts web。
- **共享记忆读写协议落地**（2026-08-13）：AGENTS.md 增补「读写时机判断」（新项目开始前读、单元交付后写）；新增 交接命令.md（可直接复制给任何 Agent 的模板）。
- 资源调查完成：10 类约 73 条资源，落 RESOURCES.md（2026-08-13）。
- 多 Agent 共享记忆骨架上线：https://github.com/201650545/ai-hub-memory（2026-08-13）。
- 前端重构：5 个前端统一苹果浅色风 + 深色切换按钮（2026-08-12）。

## 卡点
- 无。

## 下一步
- 补 OpenCode Go / WorkBuddy 额度详情（待用户确认）。
- （可选）ai-hub 网关三件套缺失导致的 4 项回归 SKIP（test_gateway 渠道/test_engines/test_history/test_quota 依赖已删除的 03_共享组件）——如需恢复请单独开任务。
