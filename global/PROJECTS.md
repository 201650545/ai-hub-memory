# PROJECTS.md — 项目全景（5 GitHub 仓库介绍）

> 用途：任何 Agent 接手任务前，读本文件即理解整个项目体系，无需逐个翻 GitHub 仓库。
> 本文件是「记忆中的项目地图」——各仓库详细内容见各自仓库，这里是全景与关系。
> 更新：仓库定位/结构/状态变化时同步更新本文件。

## 全景一句话
这是「一个主人的数字资产 + 多 Agent 协作」的基础设施：**ai-hub-memory**（共享记忆/大脑）统领全局，**ai-resource-hub**（资源库/钱包）提供 API/账号/额度，**ai-hub**（操作台）聚合网关/搜索/编排，**feishu-data-hub**（数据桥）把飞书数据公开化，**english-teaching-production**（教学业务线）承载具体业务。

## 1. ai-hub-memory — 共享记忆（本项目）
- 定位：多 Agent 共享记忆的唯一真源（你正在读的这个仓库）。
- 结构：MEMORY.json 路由 + global/（RULES/DECISIONS/RESOURCES/TOOLS/PROJECTS）+ projects/（teaching/courseware/memory-system）+ inbox/ + scripts/ + skills/。
- 核心：项目隔离 + 分层记忆 + Routing-before-Retrieval + Fail-Closed + 16 条宪法。
- 状态：v2.1 落地（隔离记忆 + sync 命令 + 工具手册）。

## 2. ai-resource-hub — AI 自助资源运营体系
- 定位：把数字资源（API/账号/免费权益/工具/网关）统一收集、分类、授权给本地 AI 自主调用——AI 的「钱包和工具箱」。
- 结构：方案书.md + docs/（问诊/操作手册/资源调研）+ exporter/（公开数据桥）+ feishu/（6 表）+ scheduler/（本地调度器 + SQLite）。
- 关键：飞书表是资源配置真源；数据桥（manifest 校验 + fail-closed）导到 GitHub Pages；凭证只在本地 credentials.json。
- 状态：方案书 v0.3；6 表已建；数据桥上线；调度器 M1。

## 3. ai-hub — 统一 AI 聚合管理平台
- 定位：多网关 AI 服务管理——API 聚合中转、多引擎 AI 搜索、GitHub 项目管理、飞书数据同步。
- 结构：00_中央平台/（FastAPI :8000）+ 06_组件编排器/（课件生成 :8791）+ 04_任务卡/ + tests/。
- 状态：活跃开发；任务卡 001-016 大部分完成；资源数据桥接入门户（/api/resources）。

## 4. feishu-data-hub — 飞书数据公开桥
- 定位：飞书多维表格 → GitHub Pages 公开导出，为 AI 工具提供可读的静态数据中心（英语教学/公考/教资/教师成长数据）。
- 结构：config/ + content/ + lib/ + docs/ + examples/（JavaScript）。
- 状态：已上线（2026-08-13）。

## 5. english-teaching-production — 初中英语教学生产体系
- 定位：初中英语教学生产——规范/工具/流程（供 AI 读取工作方法）。
- 结构：00_总规划 + 00_格式规范 + 00_工具 + 01_数据 + 样例课件 + 策略文档（Python）。
- 状态：private；教学业务线（对应 projects/teaching）。

## 仓库关系
```
   ai-hub-memory（记忆/大脑） ←→ 多个 Agent
        ▲ 读写                      │
        │                           ▼
   ai-resource-hub（资源/钱包）  ai-hub（操作台/网关）
        │                           │
   feishu-data-hub（数据桥）  english-teaching-production（业务线）
```
- 数据流：飞书表 → feishu-data-hub 公开 → 各 AI 读取；ai-resource-hub 调度器 → 本地调用；ai-hub 网关 → 聚合转发。

## 给 Agent 的提示
- 接手任务：先读本文件（全景）→ global/RULES（规则）→ 对应项目 STATE（状态），即可开工，无需翻各仓库。
- 涉及资源/凭证：看 global/RESOURCES.md（What）与 ai-resource-hub 的 credentials.json（本地）。
- 涉及工具：看 global/TOOLS.md（How）。
