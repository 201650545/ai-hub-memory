# PROJECTS — 跨仓库项目地图

> 目的：帮助 Agent 判断「当前任务属于哪里、下一步读哪里」。
> 边界：只记录仓库身份、职责边界、权威来源和跨仓库关系；**不记录**版本、任务进度、端口、详细目录、额度或运行状态（那些在 README/STATE/RESOURCES/TOOLS）。
> 更新原则：仅在仓库新增/删除/改名、核心职责、权威来源或跨仓库关系变化时更新。

## 一句话全景
- ai-hub-memory = 记忆（共享记忆/路由）
- ai-resource-hub = 资源（AI 资源运营/配置真源）
- ai-hub = 操作（网关/搜索/编排）
- feishu-data-hub = 数据桥（飞书 → 公开静态数据）
- english-teaching-production = 教学业务（教学生产规范/工具/流程）

## 仓库路由表
| Repo | 负责什么 | 不负责什么 | 深入读取 |
|------|---------|-----------|---------|
| ai-hub-memory | Agent 共享记忆、路由规则、项目状态 | 业务实现、资源实时状态 | MEMORY.json / 对应 project STATE |
| ai-resource-hub | AI 资源运营与配置来源（API/账号/额度） | Agent 记忆规则 | repo README / 资源真源 |
| ai-hub | AI 网关、搜索、编排操作面 | 资源台账真源 | repo README |
| feishu-data-hub | 飞书数据公开/静态桥接 | 飞书业务数据的编辑逻辑 | repo README |
| english-teaching-production | 教学生产规范、工具和流程 | 通用 Agent 基础设施 | repo README / teaching STATE |

## 关系
- 飞书数据 → feishu-data-hub → AI 消费端
- 资源配置 → ai-resource-hub → ai-hub / Agents
- ai-hub-memory → 为所有 Agent 提供共享记忆
- english-teaching-production → 教学业务执行层

## 下一跳
- 不知道任务属于哪里 → 本页判断
- 已确定 memory project → 对应项目 STATE
- 资源/额度 → RESOURCES / ai-resource-hub
- 环境操作 → TOOLS
- 实现细节 → 对应 repo README/代码
