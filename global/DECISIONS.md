# DECISIONS.md — 全局决策（跨所有项目，append-only）

> 只追加。这里只放「删除任何一个项目后依然成立」的决策。项目专属决策在各项目的 DECISIONS.md。

## 2026-08-15
- [D-GLOBAL-20260815-01] **自有知识解决不了 → 转问 GPT**：当 Agent 对上游行为/资源/架构/外部服务现象判断不定、或已自行尝试多次仍无把握时，不要埋头硬试，转 GPT 镜像站（Thinking·Extended）问诊。典型场景：upstream 403/报错、免费档/价格判断、模型名/鉴权方式、某厂商资源的可用性确认。GPT 镜像站故障时转 Claude 兜底（沿用 D-20260813-04）。
- [D-GLOBAL-20260815-02] **代表用户执行**（用户 2026-08-15 拍板，对 D-GLOBAL-20260813-03 的项目内例外）：用户不懂技术细节，Agent 代表用户处理所有技术决策，不逐项向用户确认技术问题；拿不准的架构/资源/外部行为判断转 GPT 镜像站（Thinking·Extended）问诊，问诊轮次≤3 轮须收敛；GPT 回复后自主选用最推荐方案直接落地执行；完成只告知用户「项目已可用」，不汇报技术细节。

## 2026-08-14
- [D-GLOBAL-20260814-01] 记忆系统 v2 = **项目作用域隔离 + 分层记忆 + Routing-before-Retrieval + Fail-Closed**（三方交叉定稿：AI 搜索网关 + Claude Sonnet5 + GPT-5.6 Extended）。核心公式：Memory = Global Kernel + Project Namespace + Layered Retrieval；Multi-read / Single-write；scope 不明确拒绝读写。落地：MEMORY.json + memory.py + memory-router/SKILL.md。

## 2026-08-13
- [D-GLOBAL-20260813-01] 工作模型 = **按需调度**：用户自然说话，Agent 当调度大脑路由已打通工具；**不做**定时提醒 / 汇报平台。
- [D-GLOBAL-20260813-02] 多 Agent 共享记忆 = **GitHub 仓库承载**（唯一真源），记忆以项目为原子单元。
- [D-GLOBAL-20260813-03] 每次执行前先向用户确认。
- [D-GLOBAL-20260813-04] 问诊走 GPT 镜像站 **Thinking · Extended**（不是 Auto）；GPT 镜像站故障时转 Claude 兜底。

## 2026-08-12
- [D-GLOBAL-20260812-01] 前端统一苹果浅色风 + 深色切换按钮。