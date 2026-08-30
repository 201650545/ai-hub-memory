# 网关 content_filter 被归一化为假"Token上限"——DSH fast 截断复发实证

（2026-08-30 03:5x UTC / 本地 19:5x；诊断线：QoderWork 会话，claim C-20260830-02；转交网关线收尾）

## 结论
用户报"fast 从最初能流式回答，现在总答到 Token 上限就不回答"。实证：**与 65536 预算完全无关**，真因是上游 xiaohongshu/dots3-note-prev 返回 `finish_reason=content_filter`（内容审核拦截正文），网关归一化层把它改写：
- `content_filter → length`：DSH 渲染"已达到输出 token 上限"横幅（误导性假象）；
- `content_filter → stop`：DSH 显示"正常结束"但正文为空（无声不回答）。
触发条件与上下文强相关：该会话上下文已达 13.8 万 token、塞满当日敏感工作内容（提 API key/爬页面/网关配置），审核反复误杀；短上下文请求同一晚均正常。

## 证据链（全部自然落盘，零人造探针）
1. 网关服务 err 日志（D:\项目\services\search_gateway\runs\_svc_3100.err-*.log）：
   - `finish_reason content_filter → length 归一化 (18:17:08 / 18:19:00 / 18:28:46)`
   - `finish_reason content_filter → stop 归一化 (18:49:39 / 18:51:38 / 19:03:17 / 19:14:47)`
2. DSH session-60403630 session.jsonl.zstd turn 对照（时间秒级吻合）：
   - turn68/70/72 → turn/end reason=max-tokens（假"Token上限"），对应→length 三行
   - turn74/75/77/78-2 → turn/end completed 但 assistant 消息仅 reasoning 无正文，对应→stop 四行
   - 异常响应 usage 一律 `inputTokens:0, outputTokens:0`（上游被过滤时不计费不计数）；同晚会话正常响应 usage 真实（如 input 138629/output 1254，input 135139/output 573）——证明模型上下文并未溢出、预算从未烧满
3. 预算配置完好：~/.dsh/settings.yaml llm-pi-ai.providers.local-gateway.models[fast].maxTokens=65536（deepseek-free 同），sync_dsh_models 保留补丁未被破坏
4. 路由正常：route-log/telemetry 显示 resolved=xiaohongshu/dots3-note-prev、fallback_count=0、errors/failures 空——不是选路失败
5. 昨日已有先兆：STATE S-20260829-14-DSH ④ 记录"03:49-04:26 连续 5 次 Provider content_filter"——同一现象间歇存在，本次是长上下文将其放大为"总是"

## 他线在途（请勿重复施工）
工作区 D:\项目\services\search_gateway 有未提交改动（api_gateway.py/_has_content_filter_only + 流式 inspect 决策 content_filter→换下一渠道；upstream_outcome.py），注释已点名"Fast 模型想完就停"。今日 18:16:47 / 18:48:03 / 19:11:21 三次 NSSM 重启应为该线部署测试（最后一次 commit b5876ea 19:14:08）。18:48 后"→length 假横幅"未再出现，方向正确。

## 遗留尾巴（转交项）
1. **流式 failover 未触发实证**：19:14:47（turn78/2，重启 19:11:21 之后的新代码）仍走"→stop 归一化"且 telemetry fallback_count=0——流式路径的 content_filter-only 检测/换渠道在当前运行版未生效，需排查（或该版尚不含流式分支）。
2. `→ length` 映射建议彻底移除：把审核拦截伪装成"Token 上限"直接造成本次误诊，宁可诚实报错。
3. 全成员都被过滤时的最终兜底：应向客户端返回可辨识的"上游安全过滤"信号（或至少 error 事件），而非无声空正文。
4. 提交时注意：工作区另有 resource_config.py / tests 未提交改动，勿互相扫走（先例：S-20260829-12 ⑤）。

## 验证口径（用户拍板纪律，长期有效）
不做人造负载/数字探针。修复是否生效只看：①网关 err 日志 content_filter 行为（failover 日志 vs 归一化日志）；②telemetry JSONL fallback_count>0 且最终 resolved 换成员；③DSH 真实会话 turn 正常出正文。自然使用即取证。

## 关联档案
- ai-hub-memory/projects/ai-resources/STATE.md S-20260829-08/-09/-10/-11/-12-DSH/-13-DSH（预算线完整史，本次证实其 R3 结论仍成立：预算方案无回归）
- coordination/claims/C-20260830-02.md（本诊断租约）
