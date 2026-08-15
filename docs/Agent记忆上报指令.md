# Agent 记忆上报指令（发给各项目 Agent）

> 用途：用户把本文件中的「指令正文」复制发给不同项目的 Agent，让它们把自己项目的记忆同步进共享记忆仓库 ai-hub-memory。
> 使用：用户先确定每个 Agent 的项目（教学 teaching / 课件 courseware / 记忆系统 memory-system / 或新项目），然后发对应指令。

---

## 指令正文（复制这一段发给 Agent）

---

你现在是一个【<项目名>】项目的 Agent。任务结束前，请把你在这个项目里产生的、值得其他 Agent 知道的记忆，同步到共享记忆仓库 ai-hub-memory。

### 第一步：确认你的项目
- 你的项目 id 是：<项目id>（teaching=教学 / courseware=课件 / memory-system=记忆系统 / english-teaching=英语教学 / english-learning=英语学习 / devel-tools=工具链）。完整清单以仓库根 MEMORY.json 的 projects 键为准。
- 如果这是一个全新项目（上面三个都不是），先注册：
  ```bash
  python scripts/memory.py register --id <英文id> --name <中文名> --aliases <别名>
  ```
- **如果归属拿不准**（分不清属于教学/课件/记忆系统哪个，又不像全新项目）→ 不要强行归类，改用隔离区上报（capture），由 settler 审核后再归类：
  ```bash
  python scripts/memory.py capture --capture-scope <你的Agent名> --project-hint UNKNOWN --content "<一条记忆内容>"
  ```
  > 上报后即可结束，**不需要走下面第二步到第六步**（settle 是审核方做的事，不是你）；一条记忆 capture 一次。

### 第二步：整理你的记忆（什么该记）
把记忆写成 .md 或 .txt 文件，**一条记忆一个文件**（或放同一个目录），内容为：
- ✅ 可交付成果（做了什么、结果如何）
- ✅ 拍板的决策（用户定的、项目内的重要约定）
- ✅ 当前卡点 / 下一步
- ✅ 其他 Agent 会用到的事实（路径、工具、数据源）
- ❌ 凭证/key/密码（绝不写！会被拦截）
- ❌ 中间过程、一次性闲聊
- ❌ 超长内容（单条 600 字内，长内容拆多条）

### 第三步：拉取记忆仓库
```bash
gh repo clone 201650545/ai-hub-memory   # 没有则克隆
cd ai-hub-memory
git pull --ff-only                      # 已有则拉到最新
```

### 第四步：同步你的记忆
把整理好的记忆文件/目录同步进你的项目：
```bash
# 先预览（不写入，看将同步什么）
python scripts/memory.py sync --project <项目id> --dir <你的记忆目录> --dry-run

# 确认无误后正式同步
python scripts/memory.py sync --project <项目id> --dir <你的记忆目录>

# 单条记忆（可选）
python scripts/memory.py sync --project <项目id> --file <某条记忆.md>
```

### 第五步：提交推送
```bash
git add -A
git commit -m "memory: sync <项目名> 记忆"
git push
```
- 命令会自动：判断每条是状态还是决策、生成稳定 ID、写 CHANGELOG、拦截凭证。
- 若 pre-commit hook 拦截（超行数/漏 DROP/凭证）→ 按提示修复后重试，**禁止 --no-verify 绕过**。

### 第六步：验证
```bash
python scripts/memory.py validate
python scripts/memory.py read --project <项目id> --file state    # 应看到你的 S-ID 条目
python scripts/memory.py read --project <项目id> --file decision # 应看到决策（如有）
```

---

## 发给各 Agent 时的填法示例

| Agent / 项目 | 填项目名 | 填项目 id |
|-------|---------|-----------|
| 教学 | 教学 | teaching |
| 课件 | 课件 | courseware |
| 记忆系统 | 记忆系统 | memory-system |
| 英语教学 | 英语教学 | english-teaching |
| 英语学习 | 英语学习 | english-learning |
| 工具链/DSH 开发 | 工具链/DSH 开发 | devel-tools |
| 全新项目 | （你的中/英文名） | <英文id>（先 register，下方见） |

> 项目清单是动态的：以仓库根 MEMORY.json 的 projects 键为准（现为上述 6 个项目）。新增项目后请同步更新本表。

---
（完）
