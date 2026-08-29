# coordination/claims — 任务级协作租约（Claim / Lease）

> 用途：防多 Agent 重复做同一高成本任务（如计费核查、归档迁移、渠道盘点）。
> 这是**协作租约，不是数据库强锁**：Git 文件只是声明，靠「执行高成本任务前先查 claim」的纪律生效。
> 与「唯一真源」互补：claim 防重复劳动，唯一真源防副本分叉，两者不能互相替代。

## 约定

- 高成本任务（预计 >30 分钟或跨多文件写操作）执行前：`git pull --ff-only` → `claim --action list` → 无同 `subject_key` 活跃 claim 才 `create` → 完成后 `settle`。
- `subject_key` 是防撞的关键：按 `provider:<渠道>:<主题>` / `project:<项目>:<主题>` 格式填写，如 `provider:zenmux:pricing`。
- 到期未 settle 的 claim 视为过期，可重新认领（先看 `expires_at` 与 `claimed_at`）。
- 一个项目同一时间只允许一个 consolidation writer。

## 命令

```powershell
python scripts/memory.py claim --action list
python scripts/memory.py claim --action create --project ai-resources --subject-key "provider:zenmux:pricing" --task "ZenMux 计费逐模型核算" --expires 2026-08-30
python scripts/memory.py claim --action settle --claim-id C-20260829-01
```

## 文件格式

`YYYY-MM 不分组，直接放本目录`：`C-YYYYMMDD-NN.md`

```
claim_id: C-YYYYMMDD-NN
project: <项目线>
subject_key: <provider:渠道:主题>
task: ...
owner: session-xxx
claimed_at: 2026-08-29T00:00:00Z
expires_at: 2026-08-30
status: active|settled
```
