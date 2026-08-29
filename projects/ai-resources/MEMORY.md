# MEMORY.md — ai-resources 稳定知识（长期语义记忆）

> 定位：本文件回答「**关于这个项目，我们已经确定了什么**」，不回答流水账。
> 与 STATE.md 的分工：STATE 回答「现在发生什么、下一步是什么」；MEMORY 回答「已确定的知识」。
> 与 ROUTER.md 的分工：ROUTER 是低语义路由索引（历史在哪里），MEMORY 是已提炼的稳定结论。
> 与 archive 的分工：历史**过程**进 archive，从过程中提炼出的**知识**留在这里。
> 维护：只有当某条经验被**多次**验证、或属架构级决定时才写入本文件；单次事件留在 STATE。
> 迁移意义：旧 STATE 条目之所以不能删，常因里面混着"事件 + 知识"。知识提炼到本文件后，事件部分才有条件进入 archive。

---

## 一、计费/免费核查方法论（反复验证确立）

1. **核查扣费必须扫「全集」**：不能只看编排组员（fast 五成员），必须扫描「全部可见模型名 → 上游解析名 → 逐模型价格」全集，否则会漏掉直呼模型名的扣费路径（S-20260829-05 教训：fast 五成员确 0 价，但 190 个可见模型名中 12 个会解析到 zenmux 收费款且 eligible=True）。
2. **「免费/收费」不能靠上游 /models 自证**：多数渠道不返回价格字段（如 AGNES 只返回 id/owned_by/supported_endpoint_types），需依据厂商口径 + 用户人工确认。
3. **延迟/质量类判断必须跨时窗多次复测**：单次时窗内的观测只能记为「当时现象」，不能写成渠道永久属性（S-20260829-02 教训：89.7s / 两次 120s 超时实为时窗性拥塞，不是下架/永久劣化；过快定级造成飞书状态与配置返工）。
4. **免费档与收费档可能只差后缀**：`agnes-2.5-flash` 免费 vs `agnes-2.5-pro` 收费；`zenmux inclusionai/ling-3.0-tiny` 无 `-free` 后缀但单价为 0，属命名误导不是收费风险。
5. **ZenMux 不是全免费渠道**：目录 166 款中仅 5 款价格全为 0（dots3-note-prev / ling-3.0-tiny / glm-4.7-flash-free / glm-4.6v-flash-free / agnes-2.5-flash），其余 161 款收费；渠道定义 `billing_tag`「🟢免费」是**错误口径**，后续勿再引用。

---

## 二、fast 编排与 Dots3（推理型模型）

1. fast 组的成员与顺序 = `unified_models.json` members + `routing.json` order；改后台顺序无需动 DSH（DSH 只传统一模型名 `fast`）。
2. **Dots3（dots3-note-prev）是推理型模型**：max_tokens 给小（如 16）时预算被 reasoning_content 吃光，HTTP 仍返回 200 但 `message.content` 为空（**静默空答案**，不报错）；正常回答普遍耗 130~260 completion tokens，调用方须给足（建议 ≥300）才能判别成败。
3. **改 fast 编排的正确顺序**：先 `POST /api/unified` 拿热加载 + DSH 同步，**再回填 tier 字段**——`set_unified_model` 是重建条目（只写 members/display），会**丢弃既有 tier 字段**（S-20260829-03 坑，已破坏过一次依赖 tier 的分层逻辑）。
4. 各渠道 Dots3 变体：xiaohongshu/dots3-note-prev（上游不提供价格字段，内测免费）、zenmux/dots-studio/dots3-note-prev（pricing 实测 0/0）、openrouter/dots-studio/dots-3-note-preview:free（实测 0/0）。
5. 还原/改道方法：`POST /api/unified` 恢复原成员 + `PUT /api/routing` 恢复 order，完整快照见 STATE S-20260829-03 ⑦。

---

## 三、飞书 Base 结构（模型资源）

1. 模型渠道数据**唯一真表 = 「模型资源总表」`tbl5ONs0gzE7I5xI`**（90 条，21 字段）；旧「模型白嫖渠道」`tbl40PAWYub8G5m8` **已不存在**（写入报 `800030104 not_found`），**勿再写旧 ID**。Base token：`StmDbTXQWaujshs9NpIc3UFpnAc`。
2. 分类层级：一级=厂商/模型系（千问/DeepSeek/GLM/GPT/Claude/混元/豆包/MiniMax/Kimi/Gemini/SenseNova/Step/开源社区/聚合/其他）→ 二级=具体模型 → 三级=获取渠道；通过分组视图实现层级浏览。
3. 关键字段：厂商、模型系(select 15 选项)、具体模型、渠道/活动名称、是否免费（**含「付费」选项**）、核实状态（仍有效/需更新/已失效/待核实）、网关落地状态(text)、具体模型、来源表、能力、API接入 等 21 字段。
4. select 值已归一化：核实状态复合值归到四标准选项，原文追加备注；旧两表重命名为「归档-」前缀保留不删除。

---

## 四、多 Agent 协同

1. 并行 Agent 可能同时改同一配置/同一文件（已观察：unified_models.json 三家成员被并发改成同向目标态）；改前先读现场、改后逐项核验终态与用户要求一致，无冲突残留。
2. 他人未提交改动不代提交、不代回退（channels.py 悬置状态由原 Agent 自行提交 `728439e` 了结）。
3. inbox 交接件须放 `pending/YYYY-MM/` 日期子目录才能被 `memory.py` 找到，直接放 `pending/` 根目录不被处理。

---

## 五、凭证与扣费边界

1. 真实 secret 只留本地凭证信任域，不入 Git/记忆/日志（与 devel-tools 线同一规则）。
2. **新功能必须先进 GPT Extended 设计评审**才能动代码：网关目前**没有"仅免费"闸门**（`channels.py` 的 `free_models` 只写健康状态、不参与路由判定），`free_only`/`block_paid` 类开关属新功能，已记 backlog 未动（S-20260829-05 ③）。
