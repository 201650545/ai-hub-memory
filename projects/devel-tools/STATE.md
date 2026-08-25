# STATE.md — 工具链/DSH 开发 项目状态

## 进行中
- 无。

## 已完成（最近）
- **[S-20260825-01]** API 转发网关 :3100 渠道管理五连修 + zenmux 接入 + DSH 切本地网关（2026-08-25）。①统一编排新建保存失败修复（POST /api/unified 落 do_POST）；②cdVendor 加 GEMMUX；③channel_health 三失败分支改回 ch.get(models) 兜底（停用/无 key 渠道模型不再显示 0）；④渠道管理新增自定义渠道+隐藏渠道：channels.json 增 custom_channels/hidden_channels，_save_config 后必调 _merge_custom_into_globals() 把自定义塞回模块级 CHANNELS/CHANNEL_ORDER（免改 ~20 处调用点），ordered_channels()=CHANNEL_ORDER 减 hidden 用于全部展示/聚合循环；端点 POST /api/channels（含 proxy 字段）、PUT /api/channels/<cid>/hidden、DELETE /api/channels/<cid>（仅自定义可删）；前端 #/channels 加新增弹窗+已隐藏恢复区；⑤渠道列表美化：图标 46px 磁贴、名称 16px、计费徽章挪副行；⑥zenmux 渠道接入：Cherry Studio sqlite 读 provider（baseUrl https://zenmux.ai/api/v1 + key），全量 165 模型调查，模型=用户启用 4 个（deepseek-v4-flash-vision-exp-free/dots3-note-prev/ling-3.0-tiny/glm-4.7-flash-free）且策展 selected 同步设置；**zenmux 必须走本机代理 http://127.0.0.1:7890 直连超时**，POST 白名单因此补 proxy 字段；实测 ling-3.0-tiny 全链路通（z-ai 免费模型上游 429 属上游拥挤非网关问题）。⑦DSH settings.yaml 重写：唯一 provider=local-gateway(:3100/v1)，删 opencode-go/openrouter/modelscope/sensetime/agnes/zscc/xiaohongshu 七个直连，30 模型清单取自 GET /v1/models（备份 settings.yaml.bak-20260825），agent-default-model=local-gateway/deepseek-v4-flash。**运维坑：重启 :3100 必须 Get-CimInstance 杀光所有 api_gateway.py 进程再起单个**——旧 listener 未死会继续占端口跑旧代码，新端点 404 早加端点正常，极易误判代码未生效（本次 DELETE 曾中招）。前端视觉验收（#34 美化+新弹窗）待郭老师浏览器目检。（2026-08-25）
- **[S-20260815-05]** R18 checkpoint 全链路最终验证（S-20260815-10）（2026-08-15）
## 已完成（最近）
- **[S-20260815-04]** R18 Memory Checkpoint 落地（2026-08-15，GPT 评审定稿）：RULES.md 加 R18（事件优先+10 用户回合 watchdog），AGENTS.md/SKILL.md 同步引用，memory.py 新增 bootstrap（唯一入口注入规则+上下文）与 checkpoint（幂等保存+自动 commit/push）命令。（2026-08-15）
- **[S-20260815-03]** 换 Agent 无缝衔接的交接消息模板（用户 2026-08-15 定稿；完整流程见 ai-hub-memory/docs/Agent记忆上报指令.md 的「指令正文」）。交接时把下面整段发给当前 Agent：当前阶段已完成，请做好收尾交接：1) 读取 ai-hub-memory/docs/Agent记忆上报指令.md 的「指令正文」照着做，把本项目阶段成果整理成记忆写入共享记忆仓库(ai-hub-memory)；2) 关键动作：git pull --ff-only；判断归属（已注册项目 teaching/courseware/memory-system/english-teaching/english-learning/devel-tools 直接写，全新项目用 register，拿不准用 capture，清单以 MEMORY.json 为准）；python scripts/memory.py write --project 项目id --kind state --sid S-日期-序号 --content 交接内容(做了什么/验收/下一步/遗留)；python scripts/memory.py validate；git add -A && git commit -m memory-项目名-阶段交接 && git push；3) 回报项目 id + SID + 是否已 push。凭证绝不写入记忆；pre-commit 拦截按提示修复，禁 --no-verify。（2026-08-15）
- **[S-20260815-02]** GitHub 本地只读镜像备份设施上线：本机 _github-mirror 下以 git mirror（裸仓库）镜像全部 5 个 GitHub 仓库（ai-hub-memory/ai-resource-hub/ai-hub/feishu-data-hub 公开可匿名拉取 + english-teaching-production 私有）。方向严格 GitHub→本地，mirror 只 fetch 不 push、本地不可改动（mirror 裸仓库机制保证）。每日 22:00 由 Windows 计划任务 dsh-github-mirror-daily 自动 fetch --prune 同步；同步脚本 sync_mirrors.ps1 与日志 _sync.log 同目录，零凭证落盘。私有仓 english-teaching-production 已实测：本机 SYSTEM 上下文 git 可匿名验证/经本机会话凭据成功 fetch，daily 增量更新可用（无需额外配置）；仅当其此前未被本机凭据覆盖时才需用户侧一次授权。（2026-08-15）
- **[S-20260815-01]** DSH 模型 429 重试默认值调优：DEFAULT_MAX_RETRIES 从 2 改为 20（deepseek-harness packages/llm/llm/src/retry-policy.ts）。这是所有提供方省略 retryPolicy 时的共用默认预算（EMPTY_RESPONSE/RATE_LIMIT/SERVER/TIMEOUT/TRANSPORT），429(RATE_LIMIT) 因此由 2 次记为 20 次；显式配置不受影响。同步更新双语 README + 补丁 5 处测试断言默认值，449 单测通过、build:lib 产物含 =20。需重启 DSH Web 进程后生效（运行中进程仍用旧默认）。（2026-08-15）
- 无。

## 卡点
- 无。

## 下一步
- 无。
