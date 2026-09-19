# Cloudflare Workers AI 渠道实测报告

> 测试日期：2026-09-19 ｜ 执行：调度大脑（Claude）
> 渠道：`cloudflare`（自定义渠道，网关 :3100 ｜ account `2e173393481e624a4865732206ba3f97`）
> 端点：`https://api.cloudflare.com/client/v4/accounts/<acc>/ai/v1`（直连，无 proxy）
> 免费档：10,000 neurons/天

---

## 一、结论速览

| 项 | 结果 |
|---|---|
| 端到端（网关转发） | ✅ 通，返回带 `neurons` 计费字段 |
| 云端目录文本模型 | 31 个 |
| **免费档可用** | **21 个**（目录 68%） |
| 免费档不可用（403 require paid） | 10 个 |
| 已下架 | 1 个（`@cf/qwen/qwen2.5-7b-instruct-awq`） |
| 网关当前暴露 | **仅 3 个**（配置写于 8/28，已过期） |
| 最新速模型 | `@cf/qwen/qwen3-30b-a3b-fp8` — 97 tok/s |
| 最省 neurons 的大模型 | `@cf/openai/gpt-oss-120b` — 11.4 neurons/次（879 次/天） |

**核心问题：配置严重过期。** 7 个配置模型里 1 个已下架、3 个从未暴露给网关；同时目录里有 6 个免费档可用且**性价比远高于现有配置**的模型没被启用。

---

## 二、渠道现有配置（2026-08-28 写入）实测

| 配置模型 | 可用 | 延迟 | tok/s | neurons | 判定 |
|---|---|---|---|---|---|
| `@cf/meta/llama-3.3-70b-instruct-fp8-fast` | ✅ | 2976ms | 38.3 | 17.74 | 可用，性能垫底 |
| `@cf/meta/llama-3.1-8b-instruct-fp8` | ✅ | 1477ms | 13.3 | 2.46 | 可用，极慢 |
| `@cf/meta/llama-3.2-3b-instruct` | ✅ | 2018ms | 70.0 | 2.67 | 可用，小而快 |
| `@cf/meta/llama-3.2-1b-instruct` | ✅ | 2064ms | — | — | 可用，无价值 |
| `@cf/qwen/qwen2.5-7b-instruct-awq` | ❌ | — | — | — | **已下架** No such model |
| `@cf/ibm-granite/granite-4.0-h-micro` | ✅ | 2661ms | 19.5 | **0.88** | 最省，但太慢 |
| `@cf/zai-org/glm-4.7-flash` | ✅ | 11178ms | 44.4 | 7.40 | 首字极慢（11s） |

> 网关 `/v1/models` 实际只暴露 3 个：`granite-4.0-h-micro` / `llama-3.3-70b-instruct-fp8-fast` / `glm-4.7-flash`。
> 另 4 个配置模型（llama-3.1-8b / llama-3.2-3b / llama-3.2-1b / qwen2.5-7b）不在统一模型表里，转发不可达。

---

## 三、免费档可用模型全表（实测）

按 neurons 升序（同工作量 ≈120 输出 token）：

| # | 模型 | tok/s | neurons/次 | 次/天@10K | 评价 |
|---|---|---|---|---|---|
| 1 | `@cf/ibm-granite/granite-4.0-h-micro` | 19.5 | 0.88 | 11,317 | 最省，慢 |
| 2 | `@cf/meta/llama-3.1-8b-instruct-fp8` | 13.3 | 2.46 | 4,061 | 慢 |
| 3 | `@cf/meta/llama-3.2-3b-instruct` | 70.0 | 2.67 | 3,739 | 小巧快 |
| 4 | **`@cf/openai/gpt-oss-20b`** | 57.7 | 5.53 | 1,809 | **性价比佳** |
| 5 | **`@cf/google/gemma-4-26b-a4b-it`** | 31.1 | 5.75 | 1,737 | 新模型 |
| 6 | **`@cf/qwen/qwen3-30b-a3b-fp8`** | **97.2** | 6.21 | 1,610 | **最快** |
| 7 | `@cf/mistralai/mistral-small-3.1-24b` | 28.2 | 6.24 | 1,602 | 中规中矩 |
| 8 | `@cf/meta/llama-4-scout-17b-16e` | 26.5 | 6.82 | 1,466 | 中规中矩 |
| 9 | `@cf/zai-org/glm-4.7-flash` | 44.4 | 7.40 | 1,352 | 首字慢 |
| 10 | **`@cf/openai/gpt-oss-120b`** | 54.3 | 11.37 | 879 | **大模型最省** |
| 11 | `@cf/qwen/qwen2.5-coder-32b-instruct` | 24.8 | 12.85 | 778 | 代码向 |
| 12 | `@cf/meta/llama-3.3-70b-instruct-fp8-fast` | 38.3 | 17.74 | 563 | 现有默认 |
| 13 | `@cf/qwen/qwq-32b` | 29.0 | 19.80 | 505 | 推理向 |
| 14 | `@cf/nvidia/nemotron-3-120b-a12b` | 73.6 | 22.02 | 454 | 快但贵 |
| 15 | `@cf/qwen/qwen3.8-27b` | 37.2 | 48.79 | 204 | 首字慢(17s) |
| 16 | `@cf/deepseek-ai/deepseek-r1-distill-qwen-32b` | 24.4 | 89.84 | 111 | **性价比最差** |
| 17 | `@cf/meta/llama-guard-3-8b` | — | — | — | 内容审核专用 |
| 18 | `@cf/meta/llama-3.2-11b-vision-instruct` | — | — | — | 视觉，未测吞吐 |

---

## 四、免费档不可用（403 require paid）

以下模型目录可见但在 Workers Free 档返回 403：

```
@cf/zai-org/glm-5.3
@cf/zai-org/glm-5.3-flash
@cf/zai-org/glm-5.2
@cf/moonshotai/kimi-k2.7-code
@cf/moonshotai/kimi-k2.6
@cf/deepseek-ai/deepseek-v4-pro-0813
@cf/deepseek-ai/deepseek-v4-flash-0731
（另若干图像/嵌入模型亦为付费档）
```

错误原文：`AiError: Model <id> is not available on the Workers Free plan. Upgrade to access...`

> ⚠️ 与 8/28 配置 note 的记载相反：`glm-4.7-flash` 是**免费档可用**（不在 403 名单），而 `glm-5.3-flash` 才需付费。原 note 表述需修正。

---

## 五、建议（待郭老师拍板）

1. **剔除已下架**：`@cf/qwen/qwen2.5-7b-instruct-awq`（调用必 400）。
2. **补入 3 个高价值模型**，替换现有低效配置：
   - `@cf/qwen/qwen3-30b-a3b-fp8`（97 tok/s 最快，1610 次/天）
   - `@cf/openai/gpt-oss-120b`（大模型里最省，879 次/天，替代 llama-3.3-70b）
   - `@cf/openai/gpt-oss-20b`（57.7 tok/s，1809 次/天）
3. **默认模型建议改为** `@cf/qwen/qwen3-30b-a3b-fp8`（速度 2.5 倍于现默认 llama-3.3-70b，neurons 仅 1/3）。
4. **保留** `granite-4.0-h-micro` 作极限省量兜底（0.88 neurons）。
5. 4 个未暴露模型（llama-3.1-8b / llama-3.2-3b / llama-3.2-1b / qwen2.5-7b）要么补进统一模型表，要么从配置删除。

---

## 六、复现脚本

- `data/_cf_channel_probe.py` — 目录拉取 + 配置模型测试
- `data/_cf_channel_probe2.py` — 目录新模型可用性探测
- `data/_cf_speed_test.py` — 吞吐测速（~120-400 token 输出）
- `data/_cf_neurons_test.py` — neurons 计量

端到端复现：
```bash
curl http://127.0.0.1:3100/v1/chat/completions \
  -H "Authorization: Bearer <gw_key>" -H "Content-Type: application/json" \
  -d '{"model":"@cf/qwen/qwen3-30b-a3b-fp8","messages":[{"role":"user","content":"hi"}],"max_tokens":20}'
```

---

*报告生成：2026-09-19，调度大脑。原始测试为一次性探针，未改动网关配置。*