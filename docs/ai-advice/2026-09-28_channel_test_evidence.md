# 渠道测试与自动化 · 本轮改动与验收证据（2026-09-28）

对象：本机 OpenAI 兼容多渠道路由网关 `search_gateway`（:3100，Windows/nssm，`data/model_routes.json` 为编排真源，mtime 热加载）。
本轮把"能不能测"从散落在 4 个脚本里的判断收敛成一道统一闸门，把每日巡检从"只写警报"升级成"可交账的摘要"，并把编排写入收敛成单一入口。

## 0. 红线（郭老师拍板，不可协商）

1. 席位增删/替换必须郭老师拍板，禁止自行替换；失效当日提醒拍板。唯一已授权例外：免费链上出现非 0 费用字段的 openrouter 席位当日摘除。
2. 付费禁测红线：`deepseek / opencode / tokenrhythm / zenmux / ark-coding` 渠道与 `paid-fast` 全链绝不探测；网站审查只看不调。
3. 封存渠道（注册表 `get_sealed_channels()`，当前 7 个）不探测。
4. 改 `model_routes.json` 必须：备份 → JSON 校验 → healthz 验证 → 失败自动回滚 → 审计行。
5. 凭证/API key/token 绝不进入任何记忆文件、证据文件或 commit。

## 1. 改动清单

| 文件 | 作用 |
| --- | --- |
| `services/test_gate.py`（新增） | 统一"能不能测"判定。`verdict(cid, model, caller)` 返回 `(ok, code, msg)`，caller 分 `member_probe`（编排成员日检）/ `user_test`（控制台测试页）/ `health`。优先级：付费禁测渠道 → 封存渠道 → 纯付费链席位 → 渠道未注册 → 健康/不测标记 → （user_test）额度警戒 → （member_probe）日预算 |
| `services/api_gateway.py` | 控制台测试页（请求带 `_pin_channel` 或 `_test_console`）在进入回落链前逐候选过 `test_gate.verdict(caller="user_test")`，被拒者剔出链并在 `failures[]` 留痕；错误信息带中文原因。另：上游请求体剔除清单补 `_test_console`（见 §3 缺陷 D） |
| `scripts/daily_channel_refresh.py` | ①成员探测前先过统一闸门，挡下的进 `gate_skipped` 不静默丢；②streak 由"按次"改"按天"（同日重复探测不虚增，跨天才 +1），旧状态一次性迁移并备份；③清掉 9 个"永不归零"的孤儿 streak 键并写勘误警报；④落盘 `data/daily_summary_YYYYMMDD.json`（分型 OK/FAIL 计数、失败席含 streak、闸门挡下、免费名单快照新鲜度、清理明细、警报条数）；⑤摘除 OpenRouter 免费名单扫描（改由 12:00 专任务） |
| `services/routes_writer.py`（新增） | 编排唯一写入口：读 → mutator → 无变化直接返回 → 备份 → 序列化 + JSON 校验 → 原子替换 → healthz → 不健康自动回滚 → 审计行（APPLIED/REJECTED/ROLLED BACK） |
| `scripts/or_free_refresh.py`（新增，12:00 定时） | 抓 OpenRouter 目录（`order=newest` 同源 API），按"输入/输出/推理/缓存/图像等所有费用字段全为 0"判免费（递归摊平 `pricing` 含嵌套 `overrides` 阶梯价，排除 `min_prompt_tokens` 这类阈值字段）；当天过筛选线并直接经 `routes_writer` 改编排 |
| `services/web/api_page.html` | ①合并"01 模型目录 + 02 路由管理"为一页（`#/routes` 重定向到 catalog，路由详情折叠进目录）；②系统运维页新增"今日巡检"卡片，读 `/api/ops` 的 `daily_summary` |

## 2. 验收证据

### 2.1 统一闸门

- 单测 21 例全过，含负例：`zhipu → sealed_channel`、`mimo/mimo-v2.6-flash → paid_chain`、zscc 在 `health` 与 `member_probe` 下结论不同、`outside_free_whitelist`、`balance_guard`、`budget_exhausted`。
- 真 HTTP 端到端（隔离实例 `API_GATEWAY_PORT=3199`，不动线上）：
  - `pin=zenmux` → 502 `test_gate:forbidden_channel（付费禁测渠道（郭老师红线，永不探测））`
  - `pin=zhipu` → 502 `test_gate:sealed_channel（渠道已封存（注册表标记，不探测））`
  - `pin=mimo` → 502 `test_gate:paid_chain（该席位在付费链 paid-fast，禁测）`
  - `pin=edge-tts` → 502 `test_gate:unknown_channel（渠道未注册）`
  - 正例 `pin=groq / openai/gpt-oss-120b` → 200，真实 choices（闸门未误挡）
- 生产路径（不带测试标记）不经闸门：以 monkeypatch 计数验证，未改判定行为。

### 2.2 每日巡检（00:58 全量真跑，33/33 可探成员）

- chat 19 OK / 2 FAIL，image 3/0，asr 6/0，caption 1/0，tts 2/0。
- 两条真实失败席：`openrouter/qwen/qwen3.8-27b:free`（上游 429）、`sensetime/deepseek-flash`（tpm/rpm 限流）——streak 均 6 天，等郭老师拍板，未动席位。
- streak 迁移：状态键 42 → 33，清理 9 个孤儿键（`ling-3.0-flash-vl:free`、`typesafe/jev-1.13`、`mimo-v2.6-flash`、`agnes-video-2.5-flash`、`mimo-v2.5-tts*`、`gemini-3.8-live*`、`gemini-2.5-flash-native-audio-latest`），并写 `[勘误·模型策略维护]` 警报行。
- 同日不虚增已证：迁移前两席 `streak=6, last=00:23:02`，同日 00:58 再失败仍为 6。
- 运维页"今日巡检"卡片两分支浏览器验证：线上旧进程无 `daily_summary` 时显示"尚无摘要"；喂入真实摘要后渲染 11 行（分型计数 / 两席连续 6 天 / 两个免费名单新鲜度 / 清理 9 个 / 新增警报 2 条），卡片 529×322 无横向溢出。

### 2.3 编排写入口

- 三条分支（正常应用 / 校验失败 REJECTED / healthz 不通过 ROLLED BACK）全部实测，生产文件零污染，审计行落 `data/routes_audit.log`。
- 12:00 OpenRouter 任务已挂到 Windows 计划任务并跑通一轮：21 个全 0 支出模型入白名单快照，非免费的 `openrouter/typesafe/jev-1.13` 当日摘除（属红线 1 的已授权例外）。

## 3. 本轮发现并已修的缺陷

- **D（自己引入的回归）**：新增私有标记 `_test_console` 未进上游剔除清单，groq 严格校验回 400 `property '_test_console' is unsupported`。2026-09-18 为 `_pin_channel` 写过同一处剔除，这次没回头找同类参数处理点。已修，并把"正例必须用挑剔渠道"写进验收。
- **C**：白名单快照文件曾把 437 条 `excluded` 审计一并写入，5KB → 238KB，而 `quota_guard._allow_via_snapshot` 每请求 `json.loads` 且无缓存 → 直接放大每次请求开销。拆成独立审计文件，快照回到 5011 字节。
- **B**：闸门顺序缺陷——未注册渠道先返回 `unknown_channel`，导致付费禁测判定来不及生效；已把两条禁测判定提到最前。
- **A**：`paid-fast` 过度拦截——同席位若还挂在免费链上（zscc 双档席位）应按免费身份测；改为仅当该席位档集合恰为 `{paid-fast}` 才禁测。
- **历史**：chat 探针此前 `ProxyHandler({})` 强制直连 + 探针专用 UA，与运行时链路不一致，造成 groq/gemini 三席假故障（streak 虚高 5 天）。已改为走渠道自己的代理 + 运行时 UA；结论是"探针链路必须与运行时链路一致，否则测的是环境不是渠道"。

## 4. 现状与未决

- 线上 :3100 仍是旧进程：Python 侧改动（闸门、`_test_console` 修复、`daily_summary`）需重启窗口才生效；前端 HTML 实时读盘已生效。
- 编排 14 链 / 43 席位；探针可覆盖 33 席，其余为 voice-realtime / video-gen / jev / 未注册渠道。
- 待拍板：两条连续 6 天 429 的席位是否摘除或替换。
- Shadow 模式（只记账不放量）尚未落地。

## 5. 请裁定的开放问题

见问诊包第七段（与本文同仓，但以问诊包为准）。

---

（本轮核验码，要求对方在回复第一行原文引用）：GC-904317-2C72
