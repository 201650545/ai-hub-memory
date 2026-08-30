# STATE.md — 逆天主题 项目状态

## 进行中
- 无。

## 已完成（最近）
- **[S-20260828-01]**  记忆架构 Phase M2 扩展：nitian-theme 建 MEMORY.md + ROUTER.md。详情见 git 历史 + archive（SID 可溯）。
- **[S-20260827-04]**  其他 Agent 会用到的事实。详情见 git 历史 + archive（SID 可溯）。
- **[S-20260827-03]**  逆天主题（DSH 换皮）本窗口进度 2026-08-27。已交付：①编年史卷轴面板（引擎 v2.3，左下「录」按钮，27 张境界卡=配图+卷轴引言+大事记+语录+彩蛋徽章，Esc。详情见 git 历史 + archive（SID 可溯）。
- **[S-20260827-02]**  配图纠偏+两风格破境视频示例+蓄力交互。详情见 git 历史 + archive（SID 可溯）。
- **[S-20260827-01]**  编年史配图上线+卷轴面板。详情见 git 历史 + archive（SID 可溯）。
- **[S-20260826-10]**  正字修正。详情见 git 历史 + archive（SID 可溯）。
- **[S-20260826-09]**  GPT-Extend深爬补彩蛋成功。详情见 git 历史 + archive（SID 可溯）。
- **[S-20260826-08]**  全量需求对账与TODO backlog。详情见 git 历史 + archive（SID 可溯）。

## 卡点
- **Seedance 选型（等用户开通 2.0-mini/2.0-fast）**：数据面探测+opencli 控制台实测确认（2026-08-27）——①Doubao-Seedance-1.5-pro(251215) 模型广场标注**即将下线**，虽控制台开通管理显示『已开通 剩2,000,000/2,000,000 tokens』，但数据面 6 个 ID 变体全部 404 NotFound，200 万免费额度实际作废；②账号只有一个：2131120133（控制台/SSO/网关 ark key 同账号，此前怀疑双账号是误判，arkcli owner_trn 2101178540 是 IAM 租户 ID 不是账号 ID）；③账号免费额度实况（arkcli usage balance --type free-quota）：seed3d-2-0 剩191万tokens、hitem3d-2-0 剩50万、hyper3d-gen2 剩15万、seedream-5-0 剩27/50张，**Seedance 全系无免费额度**；④现役活动折后价（开通管理页实测）：2.0-mini=0.0092元/千tokens(720p/5s≈1元,480p≈0.44元)、2.0-fast=0.02775(720p≈3元)、2.5=0.05544(720p≈6元)、1.0-pro-fast已开通实测480p 0.21元/条(49,005 tokens)；⑤账号已开安心体验模式（免费额度耗尽自动暂停不误扣费）；⑥arkcli 1.0.22 已装（npm @volcengine/ark-cli，postinstall 需单独跑；SSO 已登录，skill 同步报错可忽略）；⑦待用户开通 2.0-mini（性价比首选）和/或 2.0-fast 后即可批量出破境视频。

## 下一步
- 无。（等待：用户开通 Seedance 2.0-mini/2.0-fast 后批量出破境视频；两风格示例验收）
