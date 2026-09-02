# 派发中心三级页 /dispatch/live · 运行实况 —— 完工报告 2026-09-01

任务：为 dispatch.py 增加运行实况日志（log_live），网关暴露三级页 + 2 个 API，新建 dispatch_live.html 实时观测页面，重启 :3100 并实测通过。

**结论：A/B/C/D 四步全部完成，实测全绿。**

---

## A) dispatch.py 改动摘要

| 位置（行号） | 改动 |
|---|---|
| L26 | `import uuid`（新增） |
| L33 | `LIVE_DIR = os.path.join(SERVICES, "dispatch_live")`（新增） |
| L70-80 | 新增 `log_live(task_id, event, payload)`：追加写 `dispatch_live/<task_id>.jsonl`，每行 `{ts, event, ...payload}`；写失败静默不阻断主流程 |
| L84-107 | 新增 `_run_streamed(cmd, task_id)`：`subprocess.Popen`（exec hook：pid/cmd）→ 按 ~4KB 增量读 stdout、回显终端并打 stream hook → `wait()` 返回退出码。stderr 保持继承不捕获（与原行为一致） |
| L144-153 | `run_a(args, task_id)`：改用 `_run_streamed`（原 subprocess.run） |
| L155-176 | `run_b(args, task_id)`：trae 分支与其余执行位均改用 `_run_streamed` |
| L178-182 | `run_c(args, task_id)`：补 exec hook（`pid=os.getpid(), cmd=[], note="C 级为 opencli 人工引导，无子进程"`） |
| L210-224 | main()：`task_id = uuid.uuid4().hex[:12]` + `t0`；`log_live('start', {tier, via, prompt[:500], paid})`；派发调用包 `try/finally`，finally 必调 `log_live('done', {tier, via, exit_code, ok, duration_ms})` |

- 4 个 hook 点齐：start（L214）/ exec（L94，Popen 启动时）/ stream（L101，每 ~4KB）/ done（L221，finally）
- 元数据齐全：ts / tier / via / pid / cmd / exit_code / ok / duration_ms
- `dispatch_history.jsonl` 落盘逻辑（log_history）原样保留未动
- 过程中修过一处 bug：`uuid4()` → `uuid.uuid4()`（NameError，实测时暴露并修复）

## B) api_gateway.py 改动摘要

| 位置（行号） | 改动 |
|---|---|
| L102 | `DISPATCH_LIVE_DIR = os.path.join(os.path.dirname(BASE_DIR), "dispatch_live")`（新增） |
| L198-204 | `_needs_auth`：免鉴权元组加 `"/dispatch/live"`；新增 `path.startswith("/api/dispatch/live")` 前缀放行（覆盖 /list 与 /<task_id>） |
| L1186-1201 | do_GET 新增 3 个路由：`/dispatch/live` → `_read_page("dispatch_live.html")`（与 dispatch.html 同模式）；`/api/dispatch/live/list` → `dispatch_live_list()`；`/api/dispatch/live/<task_id>` → `dispatch_live_events()`（task_id 正则白名单 `[0-9a-zA-Z_-]{1,64}` 防目录穿越，不存在回 404） |
| L1663-1718 | 新增 `dispatch_live_list()`：扫描 dispatch_live/*.jsonl，首行取 start 元数据（ts/tier/via/prompt），末行 done 事件判定 running/done，附 exit_code/ok/duration_ms/stream_count/stream_bytes，按 start_ts 倒序 |
| L1720-1737 | 新增 `dispatch_live_events(task_id)`：返回完整事件流（坏行跳过） |

- 未删任何现有路由/端点；未改 channels.py（mtime 2026-08-31 03:13，早于本次任务；git status 里的 M 为用户既有改动）

## C) 新建 search_gateway/web/dispatch_live.html（23891B，375 行）

- 复用 dispatch.html 的 5 主题 × 5 风格系统：完整复制 5 个 data-style 变量块（monet/vangogh/ink/modern/liquid）× light/dark CSS 变量 + gw-theme/gw-style/gw-accent localStorage 引导脚本
- header 标题：**「运行实况 · 派发中心三级页」**；「← 返回派发中心」链接回 /dispatch
- 主体两栏：左栏任务列表（start_ts 倒序，最多 8 个，点击选中）；右栏详情 = 元信息 + prompt 框 + **纵向时间线**（start/exec/done 节点 + 连续 stream 聚合节点，每节点带 `+ms` 相对 start 偏移）+ **工具调用列表**（stdout 行启发式识别 🔧/tool call/调用工具/function call/Execute 痕迹）+ **stdout 流**（`<details>` 折叠展开，展开态跨轮询保持）
- 轮询 1.5s 刷 `/api/dispatch/live/list` + 当前选中任务 jsonl；未选中/选中项消失自动选最新
- running 状态：任务条目 + 详情头均加 CSS `breath` 呼吸点动画 + 「● LIVE」渐变标
- 隐私：`sk-*` / `Bearer xxx` / `token=xxx` / `api_key=xxx` 命中的 stdout 行整行红橙底高亮、命中片段加 `.pv` 红橙加粗标签——**只高亮不遮蔽**，内容完整可见

## D) 实测记录

### 1. 重启 :3100（按 S-20260831-04 协议）

```
netstat -ano | grep :3100 → LISTENING PID 50824
Stop-Process -Id 50824 -Force（taskkill //PID 被 Git Bash 转义吃掉，改用 PowerShell）
端口释放后 NSSM 服务自动拉起新实例 PID 29080（跑新代码）
手动起的 6004 被 fail-closed 正确拒绝（端口占用保护，符合 R1-04 裁定）
日志：search_gateway/logs/api_gateway_3100_restart_20260901b.{log,err}
```

### 2. curl http://127.0.0.1:3100/dispatch/live

```
GET /dispatch/live -> 200 (23891B)   # 全量 HTML，title=运行实况 · 派发中心三级页
```

### 3. curl http://127.0.0.1:3100/api/dispatch/live/list

```json
{
 "time": "08:39:35", "count": 1,
 "tasks": [{
   "task_id": "13b3b66059e7", "start_ts": 1788277167.79, "start_time": "08:39:27",
   "tier": "A", "via": "subagent", "prompt": "回复OK",
   "status": "done", "exit_code": 0, "ok": true, "duration_ms": 2349,
   "stream_count": 1, "stream_bytes": 3
 }]
}
```

### 4. 派发 A 级任务 `python dispatch.py "回复OK"` → live 页捕获验证

- 命令输出：`OK`（exit 0）
- 落盘：`dispatch_live/13b3b66059e7.jsonl` 存在，**逐行 json.loads 全部 parse OK，4 事件：start → exec → stream → done**

```json
[{"ts":1788277167.79,"event":"start","tier":"A","via":"subagent","prompt":"回复OK","paid":false},
 {"ts":1788277167.81,"event":"exec","pid":40500,"cmd":["...python.exe","...\\subagent.py","回复OK"]},
 {"ts":1788277170.14,"event":"stream","bytes":3,"text":"OK\n"},
 {"ts":1788277170.14,"event":"done","tier":"A","via":"subagent","exit_code":0,"ok":true,"duration_ms":2349}]
```

- `curl /api/dispatch/live/13b3b66059e7` → 200 + 上述完整事件流（见上）
- 回归：`/dispatch` 200 全量 HTML、`/api/dispatch/status` 200 parse OK、`/healthz` 200、`/v1/models` 401（网关 key 鉴权正常，非本次改动影响）

## 失败 / 未做的事 + 原因

1. **taskkill //PID 失败两次**：Git Bash 把 `//PID` 转义成无效参数、`cmd //c "taskkill /PID"` 引号被吃。改用 PowerShell `Stop-Process -Force` 成功。协议目的（杀旧进程、释放端口）已达成。
2. **curl 首测挂起 / 显示 0B**：系统代理拦截（响应头带 `Proxy-Connection: keep-alive`），curl 走代理导致连接不关。加 `--noproxy '*'` 后全部正常——环境问题，非代码问题，浏览器访问不受影响。
3. **手动重启实例未成为最终服务**：杀掉 50824 后 NSSM 服务管理器抢先自动拉起 29080（新代码）。手动实例被 fail-closed 拒绝（这正是 R1-04 设计的保护行为）。最终对外服务 = NSSM 管理的 PID 29080，**已在跑全部新端点**，无需干预。
4. **B/C 级任务未实测派发**：任务书 D) 只要求派 A 级任务验证；B/C 走同一 `_run_streamed`/`log_live` 代码路径，A 级通过已覆盖 4 个 hook 点。
5. **C 级（浏览器）无子进程**：run_c 只打印引导信息，exec hook 记 `pid=os.getpid(), cmd=[]` 并注明「无子进程」，stream 事件天然为空——结构性限制，非缺陷。

## 硬规则核对

- ✅ 只改了 dispatch.py、api_gateway.py、新建 dispatch_live.html（未动 dispatch.html 本体）
- ✅ channels.py 未动（mtime 2026-08-31 03:13 < 任务开始时间）
- ✅ 未删除任何现有路由/端点（回归测试全 200/401 如常）
- ✅ JSON 改动全部 parse OK（api 接口 json.tool + jsonl 逐行 loads 验证）
- ✅ :3100 已重启 + /dispatch/live 200 OK + A 级任务 live 捕获验证通过
