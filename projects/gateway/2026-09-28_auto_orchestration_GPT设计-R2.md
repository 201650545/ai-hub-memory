# 每日自动席位编排策略 · GPT 设计 R2（2026-09-28 补充段，完整）

> 来源：镜像站 GPT（Thinking · Extended），与 R1 同会话（自动席位编排策略）。
> 本轮问题：只补 R1 截断后缺失的四段（P0 清单 / 完整版前置条件 / 决策账本与日报 / 失败面）+ 两个事实疑问 Q1 Q2。
> 送达核验：R1 已以首行引用文末核验码 QK7-4M2XN9 证明实读仓库；本轮为同会话续写，未再要求引用。
> 完整性：4269 字符，结尾是 Q2 正答，未出现投递超时残文。
>
> 以下整段逐字保留。

---

A 今晚最小可落地版（P0）清单

tools/auto_orchestrate.py：实现 load_inputs() → build_plan_p0() → validate_plan_p0() → apply_via_routes_writer() → write_reports()。

gateway/orchestration_policy.py：实现 seat_key_v0(chain,channel,model)、classify_outcome_legacy()、rank_high_p0()、rank_flash_p0()、runtime_allowed()。

data/orchestration_state.json：保存 first_seen_date/move_lock_until/last_position/verify_pending/last_decision_id。

data/orchestration_decisions.jsonl：append-only；每次运行至少写一行 RUN，每个计划动作再写一行 ACTION。

data/orchestration_last.txt：每次原子覆盖，供人类快速查看；另做 rollback_last.cmd。

顺序固定：读取→schema/日期预检→构造 v0 身份→硬边界全量复验→成熟度计算→生成计划→数量上限校验→唯一 writer→hash/healthz→账本。

mixed perf 只允许 n_wire>=5 && n_speed>=3 && coverage_days>=3 的席做相邻 ±1 调序；position==1 禁止由性能产生变化。

P0 不增加任何 probe；verify_pending 只改变已有预算内的探测优先级。

今晚不做：稳定 seat_id、probe/real 权重合并、跨链 deployment 联动、request/attempt 归因、基于真实流量的性能 rollback。

今晚也不做：模型 alias 迁移、同链重复 (channel,model) 自动处理；发现重复直接 HALT_DUPLICATE_V0_KEY。

B 完整版前置条件顺序表

统一 outcome 分型：先补 outer_http/inner_code/outcome_class；未完成前关闭“三日无 OK 尾置”和任何 reliability 自动降序。

perf source 字段：写入 probe|real；未完成前关闭 40/60 合并、probe-real 冲突冻结、真实流量参与 rollback。

probe_epoch：字段 probe_epoch_id/probe_date/probe_recipe_version；未完成前关闭“连续两个 00:23 同方向退化”判定，避免同轮重跑被当两天。

稳定 seat_id 内嵌 routes：首次迁移生成 UUID 并永久保留；未完成前关闭 alias/rename 继承、remove→readd 识别、同链重复 deployment。

perf 写入 seat_id + route_name：未完成前关闭席级真实流量回归和链级性能归因。

request_id/attempt_index/position_at_dispatch：未完成前关闭 fallback-depth、首席失败成本、位置变化因果指标。

policy 单一实现：evaluate_seat_policy() 同供 admission/plan/runtime；未完成前新模型可发现但禁止自动 ADD。

历史迁移校验：要求 mapped_routes==active_routes、duplicate_seat_id==0；未通过前完整版保持 P0 模式。

C 每日决策账本与日报形态

JSONL 公共字段：ts,run_id,record_type,status,decision_id,chain,seat_id,seat_key_v0,action,reason_code。

证据字段：n_wire,n_speed,coverage_days,ok,rate_limited,usable_success,ttft_ms,tok_s,score,old_pos,new_pos；未知写 null。

来源字段：P0 写 perf_source:"mixed"；完整版加 probe_n,real_n,probe_score,real_score,probe_epoch_id。

可追溯字段：routes_sha_before,routes_sha_after,catalog_sha,perf_sha,backup_file,rule_version。

HALTED：record_type:"RUN", status:"HALTED", reason_code:"..."，并写 proposed_ops、触发阈值实际值。

SKIPPED：席级写 action:"SKIP"，如 reason_code:"INSUFFICIENT_EVIDENCE"，保留 n_wire/coverage_days。

NOOP：仍写 RUN 行，status:"NOOP", proposed_ops:0，不能用“没有日志”代表无动作。

orchestration_last.txt：①RUN/status/time；②HASH/backup；③OPS counts；④HIGH order；⑤FLASH order。

后续行：⑥DECISIONS 每个 touched seat 一段 from→to + reason + n/days/tps/ttft/rel/score。

⑦SKIPPED/HALTED reason + actual/threshold；⑧VERIFY immediate/next_probe；⑨ROLLBACK command。

人类只看 1、3、6、7、8 五行：运行结果、改动规模、每项数字依据、为何停/跳过、验证是否成功。

所有浮点落盘统一：rate/score 4 位小数，TTFT 整数 ms，tok/s 1 位，避免同值因序列化抖动产生 diff。

D 这套设计会失败的地方

上游集体限流：rate_limited / n_wire >= 0.60 且涉及 >=3 渠道；报警 UPSTREAM_RATE_LIMIT_STORM，冻结性能调序。

OR 目录 API 抖动/残缺：fetched_count != declared_total，或候选删除 >2 / >10% active_or；报警 CATALOG_INTEGRITY_RISK。

真实流量分布突变：某链近 24h 请求量较前 7 日同 weekday 中位数变化 >3x 或 <0.33x；标记 TRAFFIC_REGIME_SHIFT。

probe 与 real 长期背离：连续 3 天 |rel_probe-rel_real|>25pp 或 TTFT/TPS 比值 >2.5x；标记 EVIDENCE_DIVERGENCE，冻结该席调序。

链被少数渠道占满：任一 channel 占 active >50% 或 top4 中占 >=3 席；报警 CHANNEL_CONCENTRATION，禁止该渠道继续自动 ADD。

小样本永久饥饿：active_age_days>=7 && n_wire<5；报警 EVIDENCE_STARVATION，保持位置冻结，不加 probe 配额。

调用契约整体漂移：单日 CONTRACT_ERROR >=3 席或 >=20% 实发席；报警 CONTRACT_REGRESSION，全局零写。

状态/路由身份漂移：state seat_key 无法映射 active route >0 或重复 key >0；报警 IDENTITY_DRIFT，当天零写。

Q1：是有意改动。 不沿用“能力带→success_rate→tok_s”。在 free-high 中，我明确要改成“能力带绝对优先；同带内 0.70 TPS + 0.20 TTFT + 0.10 reliability”。原因不是忽略可靠性，而是 429 已从静态 reliability 分母剔除，并且 <70%、70–90% 已另有硬 gate；如果再把 success_rate 放第二排序键，97% 与 100% 这种小差异会压过数倍 TPS 差异，重新制造你给的 groq 反例。P0 mixed 模式也按这个目标公式算分，只是限制 ±1 且不得产生新首席。

Q2：对，你指出的稀疏流量问题成立；我把准确判定顺序收紧为：

① hard failure:
   verify probe = MODEL_NOT_FOUND / policy violation
   => 立即按硬规则处理，不等 real。

② 非性能故障:
   verify probe 非429 hard failure
   AND 改动后 real >=1 个同类 failure
   => 回滚；
   否则等下一 probe epoch，再次同类 failure => 回滚。

③ 性能退化，real 对该 touched seat 有 >=3 OK:
   probe 命中退化阈值
   AND real >=3 OK 也命中同方向阈值
   => 当日回滚。

④ 性能退化，real <3 OK:
   第一个独立 probe_epoch 命中 => 标记 VERIFY_SUSPECT，不回滚；
   下一自然日不同 probe_epoch 再命中同一退化条件 => 回滚。

⑤ 第二天 probe 恢复正常:
   清除 VERIFY_SUSPECT；不得拿两三天后零散 real 样本追溯触发旧 rollback。

所以低流量席确实主要走“两个独立自然日 probe epoch 连续退化”路径；不是缺陷，而是刻意避免为了凑 real>=3 增加请求或让一个孤立探针直接推翻已写编排。