# STATE.md — 逆天主题 项目状态

## 进行中
- 无。

## 已完成（最近）
- **[S-20260902-01]** 真人风大境界破境视频×3 生成+实测验收（2026-09-02，郭老师拍板『先出3条大境界』）：gen_bt_real_majors.py（agnes-video-2.5-flash t2v，5.17s/1280×704）产出 bt_b_real/bt_t_real/bt_p_real.mp4（2323575/2006703/2512065B）落 assets/animations，提示词=任务书v1大境界模板×bt_real_demo真人风句式，密钥运行时读 channels.json 未入脚本。网络坑：apihub.agnes-ai.com 直连TCP超时（DNS正常Cloudflare IP 443被掐）必须走本机代理 127.0.0.1:7890，代理链路又抖（SSL UNEXPECTED_EOF 频发），脚本加指数退避重试（429等30s不轰炸）后 3/3 成。agent-browser tab new 实测（style=real 可见前台）：问鼎 bt_b_real t 1.10→2.31s 推进无回退；碎涅 bt_t_real 0.94→2.15s；踏天一桥 bt_p_real 密集探针 0.49→5.17s 完整播到片尾；2D 回归（面板真实 UI 切回）bt_p.mp4 正常。至此 4 大境界真人风齐（元婴 bt_m_real+本批3条），real 风不再回退。测试事故非引擎bug：上一场大境界 9000ms 清场定时器 vid.pause()（L663）会按停 9s 内新触发的 enter 视频（测试节奏竞态，密集复测干净，真实使用间隔>9s 无影响）。复位：demoTokens 3999700000000（用户点过演示按钮留 866M、测试被 enter(18) 灵力对齐顶到 999999473421130，均归位）、style=2d 等效默认、空涅境复验。汇报已追加节。待郭老师目检 3 条真人风后按同管线批量铺 23 条小境界 bt_XX_real.mp4。（2026-09-02）（2026-09-02）
- **[S-20260901-04]** 用户反馈『没有看见境界变化的动画』→ 定位并修复 addDemo 大境界误判 bug：＋1M/＋1B/＋1T 按钮先改 idx 再 enter(idx)，enter 内 prev===i 致 major 恒 false，v2.7 全境播视频掩盖、v2.8 视频门控 major 后暴露——＋按钮跨大境界只剩短闪不播视频。修复 addDemo 不预改 idx、跨界传 enter(ni)（client.js L808-816），node --check ×2 过，副本已同步。复验：＋1B 跨问鼎播全演出（bt_b.mp4+76 粒子+9s）；＋1T 跨空涅短演出 2.8s；境内＋1M 无演出。另注：复位态 4.0002T 在空涅，境内＋按钮本无演出属正常；旧标签页必须刷新才加载新 client.js（tab new 同 URL 会复用旧页）。demoTokens 已复位 3999700000000。汇报已追加修复节。（2026-09-01）
- **[S-20260901-03]** 任务C 本尊/分身收尾验收通过：FS_CHARS 02~05 分身立绘映射（L87-92）、立牌「分身」按钮 .cfs（L383-385/L513）、paint 分身渲染越界归本尊（L596-604）、compFenshen 持久化（L793-798）；素材 fenshen_02_zhuji~05_huashen.png ×4（上会话 gen_fenshen_v28.py 生成，路由 200）。实测：按钮仅 02~05 显示、切换许木/王林与立绘正常不 404、reload 持久化、收起/拖拽/3D 无回归。注意：真实修为 513.72M（婴变 06），平时按钮不显示，需面板入此境跳 02~05。汇报：D:\游戏\逆天主题\workers\汇报_v2.8_双风格_大小境界_本尊分身.md（§9 格式，交郭老师转复核）。（2026-09-01）
- **[S-20260901-02]** 任务B 双风格切换（2D 动漫/真人写实）收尾验收通过：loadOpts 默认 style:2d（L168）、面板「破境风格」选择器（L529/L823 持久化）、real 风取 bt_XX_real.mp4 缺失 onerror 回退 2D（L630-645）。实测：style=real reload 保持；元婴播 bt_m_real.mp4 推进正常；问鼎 bt_b_real 404 自动回退 bt_b.mp4 无报错。现状：真人风视频仅元婴 1 条（上会话用 bt_real_demo 同源复制），其余大境界回退 2D，批量生成待后续 agnes-video 任务。（2026-09-01）
- **[S-20260901-01]** 任务A 大/小境界破境分化收尾验收通过（代码为上会话完成，本会话逐行核对+浏览器实测）：小境界不播视频无粒子、2800ms 清场（≤3s 达标）；大境界保留视频+46+30 两波粒子+震屏、9000ms 清场。改动点 client.js enter() L620-663（major=[3,6,10,18] 不限方向、vid&&btVid&&major 才播、时长 major 9000/minor 2800）。stage 与安装副本 diff 一致，node --check ×2 通过。demoTokens 已复位 3999700000000。（2026-09-01）
- **[S-20260828-01]**  记忆架构 Phase M2 扩展：nitian-theme 建 MEMORY.md + ROUTER.md。详情见 git 历史 + archive（SID 可溯）。
- **[S-20260827-04]**  其他 Agent 会用到的事实。详情见 git 历史 + archive（SID 可溯）。
- **[S-20260827-03]**  逆天主题（DSH 换皮）本窗口进度 2026-08-27。已交付：①编年史卷轴面板（引擎 v2.3，左下「录」按钮，27 张境界卡=配图+卷轴引言+大事记+语录+彩蛋徽章，Esc。详情见 git 历史 + archive（SID 可溯）。

## 卡点
- **Seedance 选型（等用户开通 2.0-mini/2.0-fast）**：数据面探测+opencli 控制台实测确认（2026-08-27）——①Doubao-Seedance-1.5-pro(251215) 模型广场标注**即将下线**，虽控制台开通管理显示『已开通 剩2,000,000/2,000,000 tokens』，但数据面 6 个 ID 变体全部 404 NotFound，200 万免费额度实际作废；②账号只有一个：2131120133（控制台/SSO/网关 ark key 同账号，此前怀疑双账号是误判，arkcli owner_trn 2101178540 是 IAM 租户 ID 不是账号 ID）；③账号免费额度实况（arkcli usage balance --type free-quota）：seed3d-2-0 剩191万tokens、hitem3d-2-0 剩50万、hyper3d-gen2 剩15万、seedream-5-0 剩27/50张，**Seedance 全系无免费额度**；④现役活动折后价（开通管理页实测）：2.0-mini=0.0092元/千tokens(720p/5s≈1元,480p≈0.44元)、2.0-fast=0.02775(720p≈3元)、2.5=0.05544(720p≈6元)、1.0-pro-fast已开通实测480p 0.21元/条(49,005 tokens)；⑤账号已开安心体验模式（免费额度耗尽自动暂停不误扣费）；⑥arkcli 1.0.22 已装（npm @volcengine/ark-cli，postinstall 需单独跑；SSO 已登录，skill 同步报错可忽略）；⑦待用户开通 2.0-mini（性价比首选）和/或 2.0-fast 后即可批量出破境视频。

## 下一步
- 无。（等待：用户开通 Seedance 2.0-mini/2.0-fast 后批量出破境视频；两风格示例验收）
