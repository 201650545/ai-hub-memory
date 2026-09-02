# coordination/LOCKS.md — 本机资源互斥锁协议（MEMREORG P0-2，GPT R3 终版 2026-09-01）

## 边界：claims 与 locks 分工

| 协调对象 | 机制 | 位置 | Git 跟踪 |
|---|---|---|---|
| 文件/目录编辑认领（异步） | `coordination/claims/` | 本仓库，入 Git | 是 |
| 端口、NSSM 服务、单实例进程（秒级互斥） | `scripts/resource_lock.py` | `global/runtime/locks/`（gitignored） | 否 |

**为什么机器级锁不放 Git**：Git 的 commit/push/pull 时延是秒级以上，挡不住端口抢占这类秒级 race（实例：Claude Code 裸占 :3100 事故）。锁协议入 Git（本文档），锁状态在机器本地。

## 用法

```bash
python scripts/resource_lock.py acquire --resource port:3100 --owner Claude --ttl 900
python scripts/resource_lock.py acquire --resource port:3100 --owner gateway --ttl 86400 --pid 34776  # 绑定持有进程
python scripts/resource_lock.py release --resource port:3100 --owner Claude
python scripts/resource_lock.py list
```

- resource 命名建议：`port:<n>` / `service:<nssm 名>` / `process:<关键进程>`
- **pid 语义**：默认 `--pid 0` = TTL-only 预约（Agent 预约资源用这个）；显式传存活进程 pid 则该进程一死锁即 STALE（长驻服务持有用这个，由服务自身启动脚本调用并传自身 pid）
- 退出码：0 成功；3 资源被占（换资源或等 TTL）；4 释放被拒（owner 不匹配且锁有效）；5 IO 错误
- acquire 前先 `list`；启动网关等长驻服务前必须先 acquire，第二个实例应在启动前失败退出，而不是抢端口后 fail-closed

## 语义与约束

1. **TTL lease**：锁默认 900s。TTL 过期或持有人 pid 已死即视为 STALE，下一个 acquire 原子接管。**TTL 必须设 ≥ 预期任务时长**，长任务宁可加大 TTL。
2. **原子性**：占位用 `O_CREAT|O_EXCL`，并发竞态只有一个赢家；输家收到退出码 3。
3. **释放**：owner 匹配才可释放；持有人崩溃后无需显式释放（pid 死亡即 STALE）。
4. **非轮转**：本锁不做排队/公平性，只做互斥。复杂编排归调度器，不归锁。
5. 锁文件是机器瞬态：在 `global/runtime/` 下，已被 .gitignore 隔离（P0-1），永不入共享真源。

## 验证记录（2026-09-01）

- 同资源（port:3100）连续两次 acquire：第二次退出码 3（BUSY），✓ 秒级互斥成立
- 错误 owner 释放：退出码 4 被拒；正确 owner 释放：退出码 0
- TTL=1 过期后另一 owner acquire：接管成功
- pid 绑定锁：持有进程存活时第二 acquire 退出码 3；进程被 TerminateProcess 后另一 owner 立即接管成功（pid 死亡 → STALE）
