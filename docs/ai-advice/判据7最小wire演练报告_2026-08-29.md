# 判据7 最小 wire 演练报告（GPT 终审 R2 必改②）

日期：2026-08-29　进程：API3100Gateway PID 36440（演练全程不变）
靶 pair：(modelscope, Qwen/Qwen2.5-72B-Instruct)——非生产路由对象，零生产影响
方法：真实 publish CLI + 真实网关 wire（status 端点 / route-plan 端点），无人工压测

## 步骤与 wire 证据

| # | 动作 | wire 证据 |
|---|------|-----------|
| 0 | 重启加载 D2 修正代码 | PID 36440；status credential_refs= {"total":0,"mapped":0,"unmapped":0,"semantics":"channel_name_mapped"}（旧代码为 resolved 键）→ D2 修正 wire 落网 |
| 1 | 基线 | live=20260829T-drill-empty（0 资源）；route-plan modelscope: eligible=true, resource_block=null |
| 2 | publish gateway_resources.candidate.drill-exp.json | publish_status=published, gateway_ack=true, gen=20260829T-drill-exp, previous=…drill-empty |
| 3 | status ACK | active_generation_id=20260829T-drill-exp, resource_count=1, last_reload_status=ok |
| 4 | route-plan 出口 | modelscope: eligible=false, reason=resource_expired, resource_block={"reason":"resource_expired","resource_id":"res-drill-exp"} |
| 5 | publish gateway_resources.candidate.drill-exp-restore.json（空代） | publish_status=published, gateway_ack=true, gen=20260829T-drill-exp-restore, previous=…drill-exp |
| 6 | route-plan 恢复 | modelscope: eligible=true, reason=null, resource_block=null |
| 7 | 历史归档 | resource_history/ 含 20260829T-drill-empty.json、20260829T-drill-exp.json（两跳发布各自归档前代） |

## 结论

- **判据7 提升 PASS**：expiry 计算态已实证影响路由出口（active+已过期 → resource_expired 封锁；空代发布后同 PID 恢复放行），闭环链 generation→publish→ACK→route-plan→恢复 完整。
- **D2 修正 wire 证据**：同一 PID 的 status 端点已输出 mapped/unmapped + semantics=channel_name_mapped，不再出现 resolved 字样；modelscope 为真渠道故 mapped=1（drill-exp 代）。
- 无生产影响：靶 pair 非生产路由对象；全程未触碰 limits/capabilities precedence（保持 shadow/static 默认零行为改变）。
