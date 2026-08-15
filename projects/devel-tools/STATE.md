# STATE.md — 工具链/DSH 开发 项目状态

## 进行中
- 无。

## 已完成（最近）
- **[S-20260815-01]** DSH 模型 429 重试默认值调优：DEFAULT_MAX_RETRIES 从 2 改为 20（deepseek-harness packages/llm/llm/src/retry-policy.ts）。这是所有提供方省略 retryPolicy 时的共用默认预算（EMPTY_RESPONSE/RATE_LIMIT/SERVER/TIMEOUT/TRANSPORT），429(RATE_LIMIT) 因此由 2 次记为 20 次；显式配置不受影响。同步更新双语 README + 补丁 5 处测试断言默认值，449 单测通过、build:lib 产物含 =20。需重启 DSH Web 进程后生效（运行中进程仍用旧默认）。（2026-08-15）
- 无。

## 卡点
- 无。

## 下一步
- 无。
