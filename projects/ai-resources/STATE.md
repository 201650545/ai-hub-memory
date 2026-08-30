# STATE.md — AI资源实测 项目状态

## 进行中
- 无。

## 已完成（最近）
- **[S-20260830-10]** 网关进程改普通权限运行，重启**免 UAC**（用户被反复 UAC 骚扰）：根因=早前用 `Start-Process -Verb RunAs` 启动 python 致网关提权、普通杀它必 Access denied、每次重启都弹 UAC 恶性循环；修复=一次性提权只**杀**旧提权进程 + **普通权限**启动新网关，实测普通 Stop-Process 可杀可启；正确重启姿势已写入 project_ai_gateway 记忆（禁止 -Verb RunAs 启动 python）。（2026-08-30）
- **[S-20260830-09]** ark 与 ark-flash 合并（用户：只用 ark 免费额度 + coding 套餐）——ark-flash 渠道删除，GA 模型并入内置 ark 渠道（channels.py models 加 deepseek-v4-flash-ga-260731 / pro-ga-260813，note 注明合并）；deepseek-free 组 9→8 成员（删 ark-flash），flash-ga 按模型名直调（包含搜索优先走 ark 免费）；渠道总数 20→19，火山方舟只剩 ark(免费)/ark-coding(套餐)。（2026-08-30）
- **[S-20260830-08]** 修正 S-20260830-05：coding 套餐渠道合并为**单渠道 ark-coding**（用户纠正「一个厂商的 3 个模型就一个渠道，别拆 3 渠道」）——models=[deepseek-v4-flash, glm-5.3-flash, deepseek-v4-pro]，base /api/coding/v3；unified 组 coding-plan={ark-coding: deepseek-v4-flash}，GLM/V4-Pro 按模型名直调；**新增编排组 glm-5.3-flash**={opencode→ark-coding}（openrouter/zenmux 收钱已剔除），实测 glm-5.3-flash 在 ark-coding 链路通。（2026-08-30）
- **[S-20260830-07]** 网关统一剥离 reasoning_content（用户拍板）：魔塔 DeepSeek V4 Pro 输出断续根因=thinking 逐 token 流式透传（实测 max_tokens=30 时 content 空/思考占满）；api_gateway.py 新增 _strip_reasoning_json + _SseReasoningStripper（SSE 逐行剥离，跨 chunk 容错），重启后实测 SSE 已无 reasoning_content。（2026-08-30）
- **[S-20260830-06]** CC Switch 直连渠道：provider「火山方舟 Coding」=Anthropic 端点 /api/coding + coding 专用 key（与模型服务 key 不同）+ 3 模型，apiFormat=anthropic，已写入 cc-switch.db（重启 CC Switch 生效）。（2026-08-30）
- **[S-20260830-05]** 火山方舟 Coding Plan Pro 套餐（49.9元/月）接入网关：OpenAI 兼容端点 https://ark.cn-beijing.volces.com/api/coding/v3（⚠️勿用 /api/v3 会额外扣费），unified 组 coding-plan，实测转发成功（deepseek-v4-flash→GA 正式版）。（2026-08-30）
- **[S-20260830-04]** B 类程序委派验证通过：Qoder CLI 分析脚本 / Trae 写码并存文件 / 豆包问答。（2026-08-30）
- **[S-20260830-03]** 豆包 adapter 修复 ask 提取截断（文本稳定检测，done 后 2 次相同才返回；新版 textEl 无 div[dir]、indicator 在 textEl 外）。（2026-08-30）

## 卡点
- 无。

## 下一步
- 无。
