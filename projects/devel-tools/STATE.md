# STATE.md — 工具链/DSH 开发 项目状态

## 进行中
- 无。

## 已完成（最近）
- **[S-20260815-02]** GitHub 本地只读镜像备份设施上线：本机 _github-mirror 下以 git mirror（裸仓库）镜像全部 5 个 GitHub 仓库（ai-hub-memory/ai-resource-hub/ai-hub/feishu-data-hub 公开可匿名拉取 + english-teaching-production 私有）。方向严格 GitHub→本地，mirror 只 fetch 不 push、本地不可改动（mirror 裸仓库机制保证）。每日 22:00 由 Windows 计划任务 dsh-github-mirror-daily 自动 fetch --prune 同步；同步脚本 sync_mirrors.ps1 与日志 _sync.log 同目录，零凭证落盘。私有仓 english-teaching-production 已实测：本机 SYSTEM 上下文 git 可匿名验证/经本机会话凭据成功 fetch，daily 增量更新可用（无需额外配置）；仅当其此前未被本机凭据覆盖时才需用户侧一次授权。（2026-08-15）
- **[S-20260815-01]** DSH 模型 429 重试默认值调优：DEFAULT_MAX_RETRIES 从 2 改为 20（deepseek-harness packages/llm/llm/src/retry-policy.ts）。这是所有提供方省略 retryPolicy 时的共用默认预算（EMPTY_RESPONSE/RATE_LIMIT/SERVER/TIMEOUT/TRANSPORT），429(RATE_LIMIT) 因此由 2 次记为 20 次；显式配置不受影响。同步更新双语 README + 补丁 5 处测试断言默认值，449 单测通过、build:lib 产物含 =20。需重启 DSH Web 进程后生效（运行中进程仍用旧默认）。（2026-08-15）
- 无。

## 卡点
- 无。

## 下一步
- 无。
