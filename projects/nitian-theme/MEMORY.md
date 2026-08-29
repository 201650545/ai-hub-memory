# MEMORY.md — 逆天主题 稳定知识（长期语义记忆）

> 定位：本文件回答「关于这个项目，我们已经确定了什么」，不回答流水账。
> 与 STATE.md 的分工：STATE 回答「现在发生什么、下一步是什么」；MEMORY 回答「已确定的知识」。
> 与 ROUTER.md 的分工：ROUTER 是低语义路由索引（历史在哪里），MEMORY 是已提炼的稳定结论。
> 维护：只有当某条经验被**多次**验证、或属架构级决定时才写入本文件；单次事件留在 STATE。
> 状态提示：本项目为「**已挂起**」——用户明确不再主动推进，只执行用户明确指令。当前未决项（Seedance 2.0 开通、两风格视频验收）见 STATE.md 卡点节。

---

## 一、项目结构与部署三处

1. **项目根 = `D:\游戏\逆天主题`**：`assets/animations/` 破境视频、`assets/ui/chronicle-img/` 编年史配图（index.json + digests.json）、`assets/ui/models/` 3D GLB、`workers/` 全部生成脚本、`dsh-plugin/` 插件包。
2. **引擎源** = `C:\Users\郭永涛\.dsh\nitian-stage\lib\client.js`；改后**必须复制到两处**：`.dsh\profiles\web\node_modules\nitian-dsh-theme\lib\` 与 `D:\游戏\逆天主题\dsh-plugin\pkg\lib\`。
3. **部署三处 hash 必须一致**；client 端热更新（浏览器 Ctrl+F5），host 端改 `src\index.ts` 需重启 DeepSeekHarness 服务（需用户批 UAC）。
4. DSH 网页 = `http://127.0.0.1:3080`。

## 二、网关与渠道

1. **API 转发 = :3100、AI 搜索 = :3000**；渠道配置在 `D:\项目\data\search_gateway\channels.json`（含各渠道 key，**严禁外传、密钥 gitignore 不入库**）。
2. 用户分工指示：**只用已选模型防扣费**、少用 kimi 搜索、复杂搜索可用 GPT 镜像 Extended、快速模型干重复活主 Agent 做高质量任务。

## 三、官方素材原则

1. **官方优先**：腾讯仙逆官方海报/立绘为真源；**无官方不硬凑假图**——空缺境界用立绘/背景/徽印过渡。
2. 官方人物形象做二创锚点：Seedream 图生图（官方形象锚定）+ Seedance 视频手尾帧。
3. 文件命名/映射以 manifest 真源为准（`canon_aligned_manifest` 中 poster_01 等文件名与实际磁盘语义命名不符，映射前必须逐文件核实）。

## 四、生成管线 API（实测破解的契约）

1. **AGNES 视频 2.5-flash**：`POST apihub.agnes-ai.com/v1/videos {model,prompt,mode:'text'}`——**mode 必填且只认 `text`**（t2v/text-to-video 全拒）→ `GET /v1/videos/{id}` 轮询 → `completed` 后 `metadata.url` 下载 mp4（5s/720P/约37s）。
2. **Seed3D-2.0**：`POST /api/v3/contents/generations/tasks {model:doubao-seed3d-2-0-260328, content:[{type:image_url,image_url:{url:dataURL}}]}` → 任务 `cgt-*` → `succeeded` 后 `content.file_url` 下载 zip（内含 `mesh_textured_pbr.glb`）。
3. **Seedream 5.0 生图**：`size` 最小 3,686,400 像素（竖版用 1728x2304），1024x1024 直接 400 InvalidParameter。
4. **商汤 sensenova-u1.5-lite 生图**：`token.sensenova.cn/v1/images/generations`（OpenAI images 兼容，b64_json 返回，key 同 sensetime 渠道）；**不在 /chat/completions**（404）；`size` 必须 32 倍数∈[512,4096] 且比例≤3:1，16:9 用 2048x1152。
5. **编年史引言管线**（gen_chron_digest_v2.py）：modelscope 429 → fallback 链 modelscope→opencode(UA: `openai-completions/pi-ai`)→sensetime；**sensetime 大提示词会思考耗尽 max_tokens 致 content 空**（reasoning 有内容）→ max_tokens 提到 6000+ 分 3 批（每批 10 境）。
6. **GPT-Extend 深爬彩蛋**：opencli 桥接问达宝镜像（Thinking·Extended），单任务 ≤3 轮，按镜像站手册流程执行。

## 五、引擎架构关键常量

1. **24 境天梯**：凝气→筑基→结丹→元婴→化神→婴变→问鼎→阴虚阳实→窥涅/净涅/碎涅→空涅/空灵/空玄/空劫→踏天九桥；**空劫拆四境**（金尊/天尊/跃天尊/大天尊 = 15-18，区间 3e14-4.5e14/4.5e14-6.5e14/6.5e14-8.5e14/8.5e14-1e15），踏天九桥 19-27；硬编码索引：`isBridge i>=18`、`桥字[i-18]`、大境界边界 `[3,6,10,18]`。
2. **货币演变**：仙玉→香火（空境）→愿力（踏天）；天梯单位制 K/M/B/T/P（K→M、M→B、B→T、T→P，踏天 1P 起步每桥约 ×3）。
3. **破境视频分档**：小境界 4.3s 简约版；跨大境界（进入 M/B/T/P）6.8s 豪华版 = 46 粒子四色爆发+三环+震屏+强闪光；M/B/T/P 四档专属视频 `bt_m/bt_b/bt_t/bt_p`（元婴星蓝/问鼎鎏金/碎涅暗红/踏天金桥）。
4. **音效引擎**：FM 钟琴（非谐波泛音）+ 合成卷积混响 + 氛围垫底；音量 localStorage `nitian.vol` 默认 0.6。
5. **编年史数据**：`assets/ui/chronicle.json`（彩蛋 149/语录 77，[GPT] 前缀标记来源）；卷轴面板入口 = 左下「录」按钮。
6. **host ALLOWED 白名单**：新视频/新资产路由必须加白名单否则 404；缺 `.js`/`.mp4` MIME 需补（ES module import 会因 octet-stream 被拒）。
7. **立牌交互**：可拖拽（位置 localStorage 记忆）+ 可收起成 58px 圆头像 + 拖拽阈值 6px 区分点按。

## 六、工程纪律与教训

1. **绝不内联复杂 python 在 PowerShell**（转义反复破坏），一律写补丁/脚本文件再执行。
2. `package.json` 被 PowerShell `Set-Content` 加 BOM 会致 loader JSON.parse 崩；ASCII 编码 touch 会把中文路径毁成 ??（用 Write 工具修复）。
3. 大模型（sensetime）小 max_tokens 会**静默返回空 content**（HTTP 200）；调用前给足预算，无法判别的加告警。
4. 对上游延迟/可用类判断必须**跨时窗多次复测**后才改配置与状态，单次时窗观测只能记为「当时现象」。
