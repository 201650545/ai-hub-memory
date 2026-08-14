# Agent 记忆同步操作文档（memory.py sync）

> 用途：让任何 Agent（或调度 Agent 如 GLM5.3）把各 Agent 各自项目的记忆批量同步进共享记忆仓库 ai-hub-memory。
> 状态：2026-08-14 已实现 + 实测通过（单文件/批量/dry-run 均验证）。
> 读本文档即可执行，无需额外解释。

---

## 1. 背景与目标

多 Agent 协作系统中，各 Agent 在做不同项目（教学 teaching / 课件 courseware / 记忆系统 memory-system），各自积累了记忆但**尚未同步到共享记忆仓库**。本命令让 Agent 把自己的记忆按项目导入共享仓库，之后任何窗口/任何模型读 `projects/<项目>/STATE.md` 就能知道各项目当前情况，不再依赖某个固定会话。

## 2. 前置条件

1. **共享记忆仓库**已克隆（或先克隆）：
   ```bash
   gh repo clone 201650545/ai-hub-memory
   cd ai-hub-memory
   # 或本地已有则 git pull --ff-only
   ```
2. **Python 3** 可用（`python --version`）。
3. **记忆文件**已就绪：Agent 的记忆以 `.md`/`.txt` 文件形式存在（每个文件 = 一条记忆，文件名任意，内容为该条记忆正文）。

## 3. 核心命令

```bash
# ① 单条记忆同步
python scripts/memory.py sync --project <项目id> --file <记忆文件.md>

# ② 批量同步（一个目录下所有 .md/.txt）
python scripts/memory.py sync --project <项目id> --dir <记忆目录>

# ③ 先预览不写入（dry-run，强烈建议先跑）
python scripts/memory.py sync --project <项目id> --dir <记忆目录> --dry-run
```

**项目 id**（见 MEMORY.json 路由表）：
| id | 中文 | aliases |
|----|------|---------|
| teaching | 教学 | 教学/课程/教案 |
| courseware | 课件 | 课件/PPT/slides |
| memory-system | 记忆系统 | 记忆系统/memory |

> 新项目：先 `python scripts/memory.py register --id <英文id> --name <中文名> --aliases <别名>` 一键建线，再 sync。

## 4. 命令自动做什么（无需人工干预）

| 功能 | 说明 |
|------|------|
| 自动判断类型 | 内容含「决策/拍板/约定/今后/以后/规则」→ 写入该项目的 DECISIONS.md（生成 D-ID）；否则 → 写入 STATE.md（生成 S-ID） |
| 自动生成稳定 ID | 按「项目+当天日期+序号」递增，不冲突（S-YYYYMMDD-NN / D-YYYYMMDD-NN） |
| 自动写 CHANGELOG | 每次同步自动追加流水（脚本维护，Agent 不用手动记） |
| 凭证预检 | 内容含疑似凭证（sk-/AIza/Bearer/app_token 等）→ 拒绝该条，不落盘（安全红线） |
| 防膨胀 | 单条正文截断到 600 字；STATE 超 60 行/8 条由 hook 拦截 |

## 5. 完整执行步骤（GLM5.3 或任何 Agent 照做）

### 步骤 A：确认仓库最新
```bash
cd ai-hub-memory
git pull --ff-only
```

### 步骤 B：确认项目存在（不存在先注册）
```bash
python scripts/memory.py validate   # 结构校验
python scripts/memory.py route --project teaching --kind state   # 应输出路径，不存在则报错
```

### 步骤 C：收集各 Agent 的记忆文件
- 让每个 Agent 把自己的记忆导出为 .md/.txt（一条记忆一个文件，或一个目录打包）。
- 按项目归类：教学的记忆 → teaching；课件的记忆 → courseware；记忆系统相关的 → memory-system。

### 步骤 D：dry-run 预览（必须先做）
```bash
python scripts/memory.py sync --project teaching --dir <教学记忆目录> --dry-run
```
检查输出：每条将写入什么类型（state/decision）、什么 ID、什么正文前 50 字。确认无误再正式执行。

### 步骤 E：正式同步
```bash
python scripts/memory.py sync --project teaching --dir <教学记忆目录>
python scripts/memory.py sync --project courseware --dir <课件记忆目录>
python scripts/memory.py sync --project memory-system --dir <记忆系统记忆目录>
```

### 步骤 F：提交推送
```bash
git add -A
git commit -m "memory: sync <项目> 记忆"   # pre-commit hook 自动校验
git push
```
> hook 若拦截（如超行数/漏 DROP/凭证）→ 按提示修复（补 DROP 声明/精简/移除凭证）后重试，**禁止 --no-verify 绕过**。

## 6. 同步后验证（自检清单）

- [ ] `python scripts/memory.py validate` 通过（结构 OK）
- [ ] `projects/<项目>/STATE.md` 能看到新增 S-ID 条目
- [ ] `projects/<项目>/DECISIONS.md` 能看到决策类条目（如适用）
- [ ] `projects/<项目>/CHANGELOG.md` 有自动追加的同步记录
- [ ] `git status` 干净（已提交推送）
- [ ] 任一文件无凭证明文（accessToken 等绝不该出现）

## 7. 常见问题（踩坑）

| 问题 | 原因与解法 |
|------|-----------|
| sync 报「unknown project_id」 | 项目未注册。先 `register` 建线，或用正确 id/别名 |
| 同步后 hook 拦截「STATE 超 8 条」 | STATE 已完成区超窗口。先在 CHANGELOG 补 DROP 旧条目再同步 |
| 某条被 SKIP | 内容含疑似凭证（R16 保护）。检查该文件，去掉凭证后重试 |
| dry-run 显示 kind 判断不符 | 内容触发词导致。用 `--kind state|decision` 显式指定 |
| 一条记忆很长 | 脚本自动截断到 600 字（防膨胀）。长内容应拆成多条或先精简 |

## 8. 结果形态（同步后共享记忆的样子）

```
ai-hub-memory/
└── projects/
    ├── teaching/   STATE.md（进行中/已完成/卡点/下一步） + DECISIONS.md + CHANGELOG.md
    ├── courseware/  同结构
    └── memory-system/  同结构
```

之后任何窗口/任何模型：读 `projects/<项目>/STATE.md` 即知该项目当前状态；想处理哪个项目就做哪个，不绑窗口。

---
（完）
