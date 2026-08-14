# AI Hub 体系 · GitHub 项目全景（5 仓库介绍）

> 用途：给高级模型（GLM5.3 等）审查架构时看的全项目地图——每个仓库是什么、核心模块、当前状态、相互配合。
> 数据：2026-08-14 收集（本地 README + gh repo 描述）。

## 全景一句话
**这是"一个主人的数字资产 + 多 Agent 协作"的基础设施**：ai-hub-memory 是所有 Agent 的共享大脑（记忆），ai-resource-hub 是资源的"钱包/工具箱"（API/账号/额度），ai-hub 是统一操作台（网关/搜索/项目管理），feishu-data-hub 是飞书数据 → 公开数据的桥梁，english-teaching-production 是具体业务线（初中英语教学）。

## 1. ai-hub-memory（共享记忆，本项目）
- **定位**：多 Agent 共享记忆的唯一真源。
- **结构**：v2.1——MEMORY.json 路由 + global/（RULES/DECISIONS/RESOURCES/TOOLS）+ projects/（teaching/courseware/memory-system）+ inbox/（隔离暂存）+ scripts/（memory.py/check_memory.py/rotate_memory.py）+ skills/memory-router。
- **核心设计**：项目隔离 + 分层记忆 + Routing-before-Retrieval + Fail-Closed + 16 条宪法。
- **状态**：v2.1 已落地（隔离记忆 + sync 命令 + 工具手册）。

## 2. ai-resource-hub（AI 自助资源运营体系）
- **定位**：把主人的数字资源（API/账号/免费权益/工具/网关）统一收集、分类、授权给本地 AI 自主调用——AI 的"钱包和工具箱"。
- **结构**：方案书.md（主方案）+ docs/（问诊/操作手册/资源调研）+ exporter/（公开数据桥）+ feishu/（飞书 6 表构建）+ scheduler/（本地调度器 + SQLite）。
- **数据桥**：飞书表 → GitHub Pages 公开 JSON（manifest 校验 + fail-closed）。
- **状态**：方案书 v0.3 定稿；飞书 6 表已建；数据桥上线；调度器 M1。

## 3. ai-hub（统一 AI 聚合管理平台）
- **定位**：多网关 AI 服务管理平台——API 聚合中转、多引擎 AI 搜索、GitHub 项目管理、飞书数据同步。
- **结构**：00_中央平台/（FastAPI :8000：注册/发现/统计/面板）+ 06_组件编排器/（课件生成 :8791）+ 04_任务卡/ + tests/。
- **状态**：活跃开发；任务卡 001-016 大部分完成；资源数据桥接入门户（/api/resources）。

## 4. feishu-data-hub（飞书数据公开桥）
- **定位**：飞书多维表格 → GitHub Pages 公开导出，为 AI 工具提供可读的静态数据中心（英语教学/公考/教资/教师成长数据）。
- **结构**：config/ + content/（数据）+ lib/（导出逻辑）+ docs/ + examples/。
- **语言**：JavaScript。
- **状态**：已上线（2026-08-13 更新）。

## 5. english-teaching-production（初中英语教学生产体系）
- **定位**：初中英语教学生产体系——规范/工具/流程（供 AI 读取工作方法）。
- **结构**：00_总规划 + 00_格式规范 + 00_工具 + 01_数据 + 样例课件 + 策略文档（如阅读理解 3+2 混合策略）。
- **语言**：Python。
- **状态**：private；教学业务线（对应 projects/teaching）。

## 仓库关系图
```
            ai-hub-memory（共享记忆/大脑）
                 ▲ 读写                │ 路由
        ┌────────┴─────────┐          │
   多个 Agent（教学/课件/记忆系统）   projects/<id>/
        │
        │ 调用资源/工具
   ai-resource-hub（资源库/钱包）  ai-hub（操作台/网关/编排）
        │                           │
   feishu-data-hub（飞书数据桥）   english-teaching-production（教学业务线）
```

## 审查提示（给 GLM5.3）
- 5 个仓库职责是否有重叠/缺失？
- ai-hub-memory 与 ai-hub 的"中央平台"是否职责边界清晰？
- ai-resource-hub 的调度器与 ai-hub 的网关是否该整合？
- 数据流（飞书 → data-hub → 各消费方）是否合理？
