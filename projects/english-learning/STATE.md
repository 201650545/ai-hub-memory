# STATE.md — 英语学习 项目状态

## 进行中
- 无。

## 已完成（最近）
- **[S-20260828-01]** 记忆架构 Phase M2 扩展：english-learning 建 MEMORY.md + ROUTER.md（2026-08-28）。①新建 projects/english-learning/MEMORY.md 稳定知识层（四节：系统架构/记忆策略 FSRS+消退提示/口语训练闭环/复习方法论），把 5 条 STATE 条目中反复验证的稳定结论提炼入 MEMORY。②新建 projects/english-learning/ROUTER.md 冷记忆路由索引骨架（索引表暂空——现有 5 条均处活跃期无归档批次）。③tier-plan 复核：keep-hot 4 (87.8%) / warm 0 / archive 0，全部合理。④按方案 M2 剩余：english-teaching / memory-system / nitian-theme 逐项目扩展；courseware / teaching 无 S- 条目暂缓。（凭证只写是否存在，无值）（2026-08-28）
- **[S-20260821-01]** [S-20260821-01] 英语学习进展与口语闭环方案（2026-08-21）  复习进展：Stage1翻译筛词复习31词；clinic 答错退回阶段0待次日复测；阶段0新学12词(child/lot/across/grade/grain/grant/hint/hip/holy/horn/illegal/immediate)并完成当日到期复习。  口语训练新闭环（取代已废弃的本地 faster-whisper 网页方案）：用户每天在豆包APP指定会话做英语语音口语练习；两个定时任务——早6:00发布当天三段式课程提示词(让它做什么/主题目标/具体要求)到固定会话，凌晨0:00读该会话豆包生成的今日汇报并把困难词幂等写入飞书词表。现已用 TraeWork Browser Extension 驱动用户真实Chrome连通豆包(已登录)并置顶固定会话。写飞书用本机npm全局lark-cli，record-search 精确查重防重复。GPT镜像站(ai问答宝)可用 opencli browser 打开+extract 读取。（2026-08-21）
- **[S-20260814-04]** # FSRS 调度字段已落地（记忆策略 v1，2026-08-11）

英语学习系统的 FSRS+消退提示已从「策略决策」落地为飞书字段 + AI 规则：

1. 字段落地（feishu-data-hub 的 learning-english 项目）
- learning-log 9→19 字段，新增：复习轮次/连续答对次数/连续答错次数/间隔天数/计划间隔天数/本次等级/FSRS难度/FSRS稳定度/下次复习时间/遗忘累计
- vocabulary 22→28 字段，新增：复习轮次/FSRS难度/FSRS稳定度/连续答对次数/连续答错次数/遗忘累计

2. AI 规则入口（8 条调度规则已写入）
- content/projects/learning-english/agent-guide.md 新增「记忆策略调度规则（FSRS+消退提示）」章节，含字段语义、数据架构职责、回退/re-learning、R6非毕业、中译英提前R3、同日不计间隔、冷启动轨迹、legacy_unverified 诊断
- 部署于 GitHub Pages：/projects/learning-english/agent-guide.md

3. 阶段三分析结论（352 条日志、130 词）
- 96% 词只测 1 次、94.6% 停在阶段0 → FSRS 闭环尚未真正跑起来
- 生产端（中英拼写 80...（2026-08-14）
- **[S-20260814-03]** # 英语学习下一步（2026-08-14）

到期复习3批待做：
- 批次1 R1补测5词（backlash/stretch/summon/augment/elevate，8-13 R2答错退回R1）
- 批次2 R2 27词（8-13总复习27词，3选1）
- 批次3 R3 15词（8-12 R2答对15词，中译英2选1）

复习完成后进入翻译筛词（新主题继续扩展词面），当天暴露新词自动记入词表+纳入复习队列，最后做当日总复习。

卡点：无。（2026-08-14）
- **[S-20260814-02]** # 英语学习当前状态（2026-08-14）

词表累计70+词在跟踪（轻量学习记录表 tblIeOhkaE40XANr）。

已完成：8-11 R1复习20词；8-12 R2复习20词（15对5错）+ 翻译筛词6篇暴露29词 + 27词总复习（23对4错）；8-13 R2复习20词（15对5错）+ 翻译筛词6篇（AI/习惯/广告/城市/教育/历史）暴露27词 + 27词总复习。

易混词5组待巩固：serve/survey、wired/weird、keep up/keep on、responsible/responsibility、aware/away。

需巩固词：wired、cross a line、promise（希望前景义）、keep up、backlash、stretch、summon、augment、elevate。（2026-08-14）
- **[S-20260814-01]** # 英语学习系统架构（项目事实）

英语学习系统 = 飞书多维表（base K15hbHNwtaY3BWs1STLcG092n4g，9表）+ GitHub feishu-data-hub（每小时自动同步）+ 对话式学习。

学习闭环：规划（学习计划表）→ 执行（对话内翻译/复习）→ 记录（学习日志表 tblWoRH8vkbVGgPi + 轻量学习记录表 tblIeOhkaE40XANr）→ 飞书同步 GitHub → 高级 AI 读取优化计划。

用户只看对话窗口，飞书表仅作存档给 Agent 查看，用户不看表。学习记录必须写回飞书形成闭环。（2026-08-14）
- 无。

## 卡点
- 无。

## 下一步
- 无。
