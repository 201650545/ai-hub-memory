# 每日自动席位编排策略 · GPT 设计 R1（2026-09-28，截断存档）

> 来源：镜像站 GPT（Thinking · Extended），会话 vip-11/c/6aba2e16-834c-83ea-98a9-524b6bd26ac7
> 问诊包：`2026-09-28_auto_orchestration_问诊包.md`　证据：`2026-09-28_auto_orchestration_evidence.md`
> 送达核验：回复**首行原文引用**了只存在于证据文件末尾的核验码 QK7-4M2XN9 → 判定已实读仓库。
> 完整性：正文 10091 字符处被镜像站 `Message delivery timed out` **截断**，停在回滚规则中途；
> 缺「完整版前置条件 / 会失败的地方 / 日报与回滚入口形态」等后续段落 → R2 在同一会话要求从截断点续写。
> 以下整段逐字保留，不拆附录（拆了等于自己把送达证据搬走）。

---

QK7-4M2XN9

结论

把每日自动编排固定成一个 12:15 单次决策事务：00:23 的探针只产健康证据，12:00 的目录刷新只产资格证据，12:15 才把两者与最近 7 天真实流量合并，统一做增、删、替换、调序。现有运行时的“剔除 / 429 平移尾部 / 代理故障升首”继续作为请求级熔断，不得写回静态长期排序；静态排序只由每日编排器修改。现状确实是 16 链、免费两线 8+14 席，运行时目前只有上述三种动态改写。
GitHub

核心参数直接定死为：

参数	值
主决策时间	每日 12:15
性能窗口	最近 7 个自然日
普通新席观察期	3 个完整自然日
U 档观察期	7 个完整自然日
可参与性能调序最小实际请求样本	n_wire >= 5
可参与性能调序最小成功速度样本	n_speed >= 3
最小覆盖天数	coverage_days >= 3
新席升首额外门槛	n_wire >= 7 && coverage_days >= 5
普通调序后冻结	72 小时
单席单日最大位移	2 位
单日 membership 操作上限	2 个 ADD/DELETE；替换=2 个
单日调序席位上限	4 个
单日总 touched 席位上限	4 个唯一席位
单链 active 硬上限	free-high=10，free-flash=16
一次拟删 OR 席异常阈值	>2 个或 >10% 当前 OR active，整批停写
普通立即调序分差	≥15 分
中等分差	8–14 分连续 2 天才动
<8 分	不动
反向回摆	解冻后仍须反向差 ≥20 分连续 2 天

因此现在的几个反例会得到明确结果：

groq/qwen3.8-27b 的 n=5 / 3 天 / raw success=80% / 297.1 tok/s 已达到调序样本门槛；其那一次失败如果按证据分类为 RATE_LIMITED，不进入静态 reliability 分母，所以不会因为 80% raw success 被降。429 由运行时 cooldown / 平移尾部处理；静态编排仍可把它作为最快成熟席保留在前部。
GitHub

xiaohongshu 的 329ms TTFT 很强，但 11.2 tok/s 很弱；在 free-high 中 tok/s 权重大于 TTFT，因此不会因首 token 快就自动升。
GitHub

lightning n=1、三个 n=0、以及 gemini-lite n=4 都没有性能升降资格；不做“看起来差所以先降”。只有目录缺失/404、硬安全边界等非性能规则可以越过这个冻结。证据文件当前样本分布正是 0、1、4、5、7、8 这一档。
GitHub

策略规格（可直接编码的规则表与伪码）
1. 身份、状态文件和每天流程

今晚不等 seat_id。先用：

seat_key_v0 = chain + "\x1f" + channel + "\x1f" + model
deployment_key_v0 = channel + "\x1f" + model

deployment_key_v0 用来读共享 perf；seat_key_v0 用来保存某条链里的位置历史、冻结期和观察期。若同一链里出现重复 (channel, model)，该链当天停止自动写入并报警，因为 v0 身份无法区分两个实例。

新增：

data/orchestration_state.json
data/orchestration_decisions.jsonl
data/orchestration_last.txt

每日状态机：

时间	动作	只产出什么
00:23	现有 ChannelDailyRefresh	probe 结果、streak、错误分类；不改长期席序
12:00	OpenRouterFreeRefresh	validated OR whitelist、pricing、目录存在性；不改长期席序
12:15	AutoSeatOrchestrate	唯一一次 plan → safety gates → routes_writer
写入后立即	本地验证	JSON、成员语义、healthz、loaded hash
下一次 00:23	首轮 post-change 验证	验证昨天的 changed/promoted/new seats；必要时自动 rollback

证据文件已有 model_perf / daily_probe_state / daily_summary / OR free whitelist / routes_audit，并且唯一写入口已经要求备份、契约校验、JSON、原子写、healthz、指纹和回滚；编排器只调用这个入口，绝不自己 open(...,"w")。
GitHub

2. 样本资格：什么情况下能升、能降、多久才能动

定义最近 7 天：

Python
Run
WIRE_CLASSES = {
    "OK", "RATE_LIMITED", "MODEL_NOT_FOUND", "AUTH_OR_POLICY",
    "CONTRACT_ERROR", "UPSTREAM_ERROR", "TRANSPORT_ERROR",
}
n_wire = count(class in WIRE_CLASSES)
n_speed = count(class == "OK" and valid_ttft and valid_tok_s)
coverage_days = distinct_local_dates(class in WIRE_CLASSES)

严格状态表：

状态	条件	可升	可降	可删
NEW	入席未满 3 完整日	否	否	仅硬删除
INSUFFICIENT	满 3 日但 n_wire<5 或 n_speed<3 或覆盖 <3天	否	否	仅硬删除
MATURE	三项门槛全过	是	是	按删除规则
HEAD_ELIGIBLE	MATURE 且 n_wire>=7、覆盖≥5天	可升 #1	是	是
U_PROBATION	U 档未满 7 日	否，固定尾部	否	硬删除
U_MATURE	7 日复核已过	可调序但永不 #1	是	是
PRIVACY	隐私风险标记	永不升	固定绝对末位	硬删除

“满 3 日”按自然日，不按进程重跑次数；同日重复任务不会推进观察期，这与现有 streak 的日粒度保持一致。U 档的 ≥3 独立来源、7 日复核和禁首席保持硬约束。
GitHub

对当前样本，n=4 即使 0% 也不能靠性能规则降，n=1 更不能动。若连续三天真实健康分类都失败，则进入后面的 health quarantine，那不是小样本性能排名，而是独立故障规则。

3. 探针 + 真实流量：可以合用，但禁止直接把原始样本混成一个大池

完整版必须给 perf 增加：

JSON
"source": "probe" | "real"

每个 source 先独立做最近 7 天汇总。

TTFT/tok_s 不直接用全部 raw 样本算中位数，而是：

先算 每席 × source × day 的 p50
再算 7 天这些 daily-p50 的 median

这样一天 500 个真实请求不会把一天 1 个标准探针彻底淹没。

当 probe 和 real 都有 >=3 个 wire 样本且覆盖 >=2 天时：

ttft_effective = 0.40 * ttft_probe + 0.60 * ttft_real
tps_effective  = 0.40 * tps_probe  + 0.60 * tps_real
reliability    = 0.40 * rel_probe  + 0.60 * rel_real

只有一边达到最低速度样本，就用那一边；两边都不足就保持 INSUFFICIENT。

如果两份证据出现以下任一冲突，当天该席冻结调序：

abs(rel_probe - rel_real) > 25 个百分点
或 max(ttft_probe, ttft_real) / min(...) > 2.5
或 max(tps_probe, tps_real) / min(...) > 2.5

冻结不影响目录缺失/404等硬动作。

今晚如果 model_perf.json 还不能区分 source，就允许把现有数据作为一个 mixed 池使用，但有两个额外限制：单次最多移动 1 位、禁止产生新的首席。这样今晚能跑，不需要先改 perf schema。

4. 错误分型：外层 HTTP 与 provider 内层错误的判定顺序

判定优先级固定：

class	判定	静态编排允许动作
LOCAL_POLICY_SKIP	请求根本没发送：付费禁测、sealed、quota/privacy 等本地挡下	不计成功率、不计失败
NOT_DUE	因每日预算/日程没有发探针	不计任何指标
MODEL_NOT_FOUND	内层明确 model-not-found / no-such-model，或模型调用得到 404	DELETE
RATE_LIMITED	内层 rate-limit/429 优先于外层泛化错误；或 HTTP 429	保留；runtime cooldown；静态不罚 reliability
AUTH_OR_POLICY	401/403 或明确 unauthorized/forbidden/provider policy	保留；可健康隔离；不删除
CONTRACT_ERROR	400/422 且不是 model-not-found/rate-limit；schema/参数合同错误	保留；冻结；可能触发全局停写
UPSTREAM_ERROR	5xx 或明确 provider server/upstream	保留；计 reliability
TRANSPORT_ERROR	DNS/TLS/reset/timeout，无 HTTP	保留；计 reliability
OK	正常结构且请求完成	正常性能证据

也就是说，先看能确定语义的 provider structured error，再用外层 HTTP 补分类。429 与目录缺失永远是两个独立变量；目录不存在/404 删除，429/5xx/401 保留，正好保持现有裁决。
GitHub

静态可靠率定义：

reliability_den =
    OK + AUTH_OR_POLICY + CONTRACT_ERROR +
    UPSTREAM_ERROR + TRANSPORT_ERROR

usable_success = OK / reliability_den

RATE_LIMITED 不在这个分母里，另算：

rate_limit_rate = RATE_LIMITED / n_wire

所以“4 OK + 1 429”不会变成 80% 静态可靠率。

5. 长期限流/故障怎么处理

不删除，但允许尾部隔离：

连续 3 个自然日：
    每天至少有 1 次实际发送，
    且三天都没有 OK，
    且原因只属于 RATE_LIMITED /
                  AUTH_OR_POLICY /
                  UPSTREAM_ERROR /
                  TRANSPORT_ERROR
=> THROTTLED_OR_DEGRADED_TAIL，至少锁尾 72h

升级：

连续 7 天无 OK => 保留 + 永久尾部，审计 severity=ERROR
连续 14 天无 OK => 仍不删除，severity=CRITICAL，每日摘要继续列出

任何一天出现 OK，连续无 OK streak 清零；但已产生的 72h movement lock 不提前解除。

CONTRACT_ERROR 单独处理，因为它更可能是调用契约或探针代码出问题：

同日 >=3 个不同席出现 CONTRACT_ERROR
或 >=20% 当日实际探测席出现 CONTRACT_ERROR
=> 全局 HALT_NO_WRITE
6. free-high 和 free-flash 的长期排序公式

所有 speed score 都用当前可比较成熟席之间的百分位 rank，不用 raw 297 和 11.2 直接相加。

Python
Run
tps_pct  = percentile_rank(tok_s, higher_is_better)   # 0..100
ttft_pct = percentile_rank(ttft_ms, lower_is_better) # 0..100
rel_pct  = 100 * usable_success

free-high：

第一键：AA 能力带绝对优先
S4+ > S4 > S3 > S2
较低能力带不得因速度超车较高能力带

同一能力带内：
high_score =
    0.70 * tps_pct
  + 0.20 * ttft_pct
  + 0.10 * rel_pct

因此 329ms / 11.2 tok/s 不会因为 TTFT 一项异常好就被当作 high 的最快席。

free-flash：

AA>=28 只是准入门槛，不作为主排序权重

flash_score =
    0.60 * ttft_pct
  + 0.30 * tps_pct
  + 0.10 * rel_pct

因此 6171ms / 174.6 tok/s 的席在 flash 中不会因为生成阶段快就自动压过真正首 token 快的席；它必须靠整体 60/30 权重胜出。样本只有 n=4 时，目前甚至还没资格参与这个比较。
GitHub

可靠率再加两个硬 gate：

usable_success < 70%:
    DEGRADED_TAIL，不参与正常 promotion

70% <= usable_success < 90%:
    可正常保留/小幅下降，但不得成为 #1

>=90%:
    正常
7. 防抖和 A→B→A

计划排序得到 target_position 后，不直接照搬。

Python
Run
delta = candidate.score - displaced.score

if delta >= 15:
    eligible_today = True
elif 8 <= delta < 15:
    eligible_today = same_direction_streak >= 2
else:
    eligible_today = False

调完后：

lock_until = today + 72h
max_position_change_per_day = 2

如果下一次想朝相反方向移动：

必须先过 72h
且反向 delta >=20
且反向条件连续 2 个决策日成立

分数完全相同或差 <1 时，以昨日现有顺序为 tie-breaker，不用模型名排序，从源头避免无意义交换。

8. 新席自动接入

准入函数只有一个：

Python
Run
def eligible_for_admission(seat):
    if channel in PAID_NEVER_TOUCH: return False
    if channel in get_sealed_channels(): return False
    if seat in explicit_denylist: return False
    if not pricing_all_numeric_zero_recursive(...): return False
    if aa >= 28: return True
    if is_U and independent_sources >= 3: return True
    return False

而且同一个硬边界函数必须在两层执行：

候选接入前：eligible_for_admission(...)
真实 dispatch 前：runtime_allowed(...)

写完 route 后再离线逐席执行一次：

Python
Run
assert runtime_allowed(member, ordinary_request_ctx)

任何付费禁测渠道、sealed、denylist、OR 不在当前 validated 免费白名单、pricing 有 -1 或 nested override 非零，却得到 True，视为 GATE_INTEGRITY_BROKEN，整次编排回滚并停写。付费禁测、sealed、OR 全零 pricing、显式禁碰名单必须同时保护接入面和运行时面，这些都是文件里的硬边界。
GitHub

新模型首次进哪条链：

正式 AA band >= S2
    -> 先进入 free-high

AA>=28 但 band < S2
    -> 先进入 free-flash

U：
    按临时能力带套上面规则，
    但前 7 日固定观察尾部且永不做首席

所有新 active member：

绝不继承某个被删席的位置
统一插到“非隐私席中的绝对尾部”
观察 3 天

隐私风险席：

sensitive_request=True  -> runtime 直接 LOCAL_POLICY_SKIP
普通请求                -> 永久固定整条链最后一席
性能成绩不能解除这个限制

证据中的 space-bunny-alpha 类席因此不会因跑分快自动往前。
GitHub

链 active 硬上限先定：

free-high = 10
free-flash = 16

超过后，新资格仍进入自动候选状态，但不再把 active list 继续膨胀；等待后续 DELETE/替换窗口。

9. 删除和替换

DELETE 只允许下面四类：

1. validated OR 全量目录单次查无
2. 调用明确 404 / MODEL_NOT_FOUND
3. 后来发现违反硬边界：付费/sealed/denylist/pricing非零
4. 同一 active route 中确认是无效重复项

对 OR 目录，必须先验证：

抓取成功
JSON 正常
total_count 存在
实际分页累计数 == total_count

然后才允许“单次缺失即摘”。这个严格遵守已经拍板的单次规则。
GitHub

若某席删除，自动补位顺序：

free-high：

同链 qualified candidate
→ 非 privacy
→ 非 U 优先
→ 能力带高
→ 已 MATURE 优先
→ high_score 高
→ current candidate age 老

free-flash：

同链 qualified candidate
→ 非 privacy
→ 非 U 优先
→ 已 MATURE 优先
→ flash_score 高
→ AA band 高作最终 tie-break

即使替代者已有历史 perf，新加入 active chain 也一律尾部观察 3 天，不继承被删位置。

10. 每日变更硬上限，以及什么时候只报警不动

普通每日事务：

membership_ops <= 2
order_moves <= 4
unique_touched_seats <= 4
one_seat_max_move <= 2 positions

replacement = DELETE + ADD = 2 membership_ops，所以当天完成一次替换后不得再做额外增删；仍可在 touched 总数允许范围内做排序。

以下任一成立，当天 route 文件零写入，只生成报警和 decision ledger：

停写条件	阈值
daily_summary 缺失/JSON 坏/不是当天	立即停
OR refresh 失败、total_count 校验失败	立即停
model_perf.json 无法解析	立即停
当天 00:23 pipeline 未成功完成	立即停
proposed membership ops	>2
proposed order moves	>4
unique touched	>4
OR 单日拟摘	>2 个 或 >10% active OR 席
CONTRACT_ERROR 爆发	≥3 席或 ≥20%
任一硬禁模型通过 runtime allow gate	立即停
同链出现重复 v0 key	立即停
计划写后有效可用成员低于昨日的 50%	立即停
writer healthz 或 loaded hash 不一致	自动 rollback，此后当天停写

这里“停写”不等于继续冒险发请求：runtime 的 paid/sealed/denylist/OR whitelist 仍独立生效，所以异常席即便还存在 JSON 里也必须被运行时挡住。

11. 写坏后的发现和自动回滚

写入当天立即做的是结构正确性：

routes_writer contract PASS
JSON PASS
all members semantic gate PASS
healthz PASS
loaded_routes_sha256 == written_bytes_sha256

下一次 00:23 不增加总探针数，只把昨天 touched seats 放到各渠道现有探针预算中的最前面，作为 verify_pending；不追加探针额度。

首轮验证：

新席/升位席出现 MODEL_NOT_FOUND
    -> 删除该席；若是 yesterday plan 唯一新增，可局部反做

昨天被提升至 top3 的席：
    昨日最后有效 probe=OK
    今日首轮出现非 RATE_LIMITED 的 hard failure
并且同席真实流量自改动后也出现 >=1 同类 failure
    -> rollback 昨日整次编排

性能回归不凭一个探针就回滚。要求“双证据”：

free-high：

今日 probe tok_s < 被替换席昨日 p50 的 60%
且 TTFT 没有改善至少 30%
且自改动后 real 已有 >=3 个 OK，real 也满足同方向退化
=> rollback

free-flash：

今日 probe TTFT > 被替换席昨日 p50 的 1.8 倍
且绝对增加 >=1000ms
且 tok_s 没有提高至少 50%
且 >=3 个 real OK 同方向退化
=> rollback

如果没有 3 个 real OK，不立即回滚性能排序；连续两个 00:23 probe 日都命中同一退化条件再自动回滚。这样不会靠多发探针获取置信度。

12. 一键回滚入口

提供双击即可用的：

rollback_last.cmd

内容只调用编排器：

bat
@echo off
py -3 tools\auto_orchestrate.py rollback --last-applied --reason MANUAL_ONE_CLICK
pause

rollback 自己仍必须调用 routes_writer 唯一入口，不能 copy backup model_routes.json。

行为：

读取 routes_audit.log 最后一个 APPLIED
取其 backup_file
JSON 校验
原子写
healthz
loaded hash 校验
写 ROLLED_BACK 审

Message delivery timed out. Please try again.

Retry