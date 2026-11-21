# 网文与 AI 短剧市场扫榜雷达 · Webnovel Market Radar

**简体中文** | [English](README_EN.md)

面向短篇网文、长篇连载网文与 AI 短剧/漫剧的三轨独立市场扫榜与选题雷达 Agent Skill。优先调用本机 **Ego Browser（`ego-browser`）** 或**内置可视化浏览器子代理（`browser`）**手动模拟浏览实时公开榜单与创作者后台，执行严格的防幻觉样本质量门，输出标准化 `扫榜报告.md` 与 `选题简报.md`，无缝交接下游写作与编剧工作室。当前版本 **v1.1.0**。

默认采用**简体中文**输出分析报告与选题简报；严格遵守合规边界：**不直接撰写小说或剧本正文，不抓取收费章节全文，不进行洗稿仿写**。

## 三大扫榜赛道

| 赛道 (`--track`) | 覆盖平台 | 核心提取与分析维度 | 下游无缝对接 |
|---|---|---|---|
| **`short`**（短篇网文赛道，0.8–5 万字） | 番茄短故事、知乎盐言、七猫、点众、黑岩 | 情绪痛点热度排行、高频脑洞设定、主力篇幅区间、前 3 句开篇钩子模式、标题与导语公式、风口饱和度预警 | [Webnovel Short Studio](https://github.com/LilHaopeng/webnovel-short-studio) |
| **`long`**（长篇连载赛道，30 万字+） | 番茄男女频榜、起点、七猫、晋江、刺猬猫 | 题材分布与趋势、新题材 / 新金手指 / 新噱头三级甄别、在读/追读/收藏指标、字数与更新节奏、书名与标签热词 | [Story World / Outline / Prose 三件套](https://github.com/LilHaopeng/story-outline-architect) |
| **`ai-drama`**（AI 短剧 / 漫剧 / 沙雕短剧赛道） | 红果短剧官网（`hongguoduanju.com` AI 剧/漫剧榜）、抖音短剧版权中心创作者后台（`shortdramas.com` 供需/飙升/抖音热播榜） | 官方题材供需比（蓝海缺口识别）、2D 漫剧 vs 3D 仿真人 AI 剧 vs 沙雕漫视觉分化、季播集数、高赞热评爽雷点与平台激励公告（如红果 40× vs 10× 规则） | [AI Drama Script Studio](https://github.com/LilHaopeng/ai-drama-script-studio) |
| **`both`**（跨体量/跨媒介联动对比） | 上述全平台 | 观察网文爆款向 AI 短剧/漫剧改编的领先风口与套利窗口 | 全生态任意下游技能 |

## 核心纪律与四级采集策略

1. **浏览器手动模拟优先，告别脆弱爬虫脚本**：
   - **优先级 1（首选）**：本机 `ego-browser` 可视化浏览器（支持直接复用用户已登录的短剧创作者后台或网文榜单会话）。
   - **优先级 2（回退）**：客户端内置 `browser` 子代理手动模拟点击、切换 Tab 与滚动加载。
   - **优先级 3（直读/辅采）**：解析用户投喂的榜单文本、截图或已有扫描记录，配合公开网页检索。
   - **优先级 4（离线兜底）**：读取内置 [platform-baselines.md](skills/webnovel-market-radar/references/platform-baselines.md)，显式标注 `[内置参考降级]`。
2. **防幻觉质量门硬约束**：
   - 单本上榜只记为个例，跨样本/跨榜单复现才标为趋势信号。
   - 常规平台有效样本 `< 15` 条（细分榜 `< 10` 条）强制标注 `[数据稀疏]`；命中 `[数据稀疏]` 或 `[内置参考降级]` 时，选题可行性**最高封顶为「中」**（严禁标「高」），并由 `validate_scan.py` 自动拦截违规虚标。
3. **人机协同与原创底线**：遇登录框、验证码或付费墙立即停手交由用户在可见窗口操作，绝不尝试绕过；仅采公开榜单元数据与 ≤120 字截断简介，下游强制执行原创脑洞置换。

## 配套创作工作流

同系列六大技能既可独立使用，也可串联成“市场雷达 → 选题立项 → 小说/短剧成稿”的完整管线：

1. **网文与短剧市场雷达 · Webnovel Market Radar**：三轨实时扫榜、蓝海缺口分析与标准化 `选题简报.md` 输出。
2. [短篇网文与微短剧爽文创作室 · Webnovel Short Studio](https://github.com/LilHaopeng/webnovel-short-studio)：直读短篇 `选题简报.md`，创作 5 万字以内高概念短篇与微短剧爽文。
3. [AI 短剧与沙雕短剧编剧室 · AI Drama Script Studio](https://github.com/LilHaopeng/ai-drama-script-studio)：直读 AI 短剧 `选题简报.md` 或小说底稿，创作 MiniMax-H3 AI 短剧、漫剧与沙雕短剧剧本。
4. [小说世界观架构师 · Story World Architect](https://github.com/LilHaopeng/story-world-architect) → [小说大纲架构师 · Story Outline Architect](https://github.com/LilHaopeng/story-outline-architect) → [小说正文写作 · Story Prose Writer](https://github.com/LilHaopeng/story-prose-writer)：承接长篇选题简报，完成精品长篇世界构建、六层大纲与正文连载。

## 安装方式

1. **通过 `skill-installer` 安装（Codex 等）**
   ```text
   $skill-installer 请从 https://github.com/LilHaopeng/webnovel-market-radar 安装 skills/webnovel-market-radar
   ```
2. **手动复制到本地技能目录（Antigravity / Claude Code / Codex / Cursor）**
   克隆本仓库，将 `skills/webnovel-market-radar/` 完整复制到对应客户端的技能目录：
   - **Antigravity**：`~/.gemini/config/skills/webnovel-market-radar`
   - **Claude Code**：`~/.claude/skills/webnovel-market-radar`
   - **Codex**：`~/.codex/skills/webnovel-market-radar` 或 `~/.agents/skills/webnovel-market-radar`
   - **Cursor**：`~/.cursor/skills/webnovel-market-radar`

所有辅助脚本仅使用 Python 3.10+ 标准库，无需安装第三方依赖。

## 快速上手

**扫红果短剧 + 抖音短剧创作者后台（AI 短剧 / 漫剧赛道）**：

```text
$webnovel-market-radar
我已经在 Ego 浏览器里打开了红果短剧官网和抖音短剧版权中心后台，帮我扫一下近期 AI 短剧和漫剧的供需榜、飙升榜与热播榜，生成扫榜报告和 3 个蓝海选题简报。
```

**扫番茄短故事 / 知乎盐言（短篇脑洞赛道）**：

```text
$webnovel-market-radar
帮我用浏览器扫描番茄短故事和知乎盐言近期热榜，提取高频情绪痛点、前 3 句钩子模式和标题公式，输出可直接喂给 webnovel-short-studio 的选题简报。
```

## 配套辅助脚本

| 脚本 | 功能说明 |
|---|---|
| `init_scan_session.py` | 初始化标准化扫榜会话目录 `扫榜/{YYYYMMDD}_{平台}_{track}/`，生成 `扫榜报告.md` 与 `选题简报.md` 模板（支持 `--track short\|long\|ai-drama\|both` 与 `--source-mode`）。 |
| `validate_scan.py` | 防幻觉质量门校验器：核对有效样本数、稀疏/降级标记一致性、最高可行性封顶规则（稀疏/降级严禁标「高」）、简介截断长度与下游写作交接块完整性。 |

常用命令示例：

```bash
python skills/webnovel-market-radar/scripts/init_scan_session.py --root <工作区> --platform hongguo_shortdramas --track ai-drama --source-mode ego-browser
python skills/webnovel-market-radar/scripts/validate_scan.py --dir <工作区>/扫榜/20261121_hongguo_shortdramas_ai-drama
```

运行回归测试：

```bash
python -B -m unittest discover -s tests -v
```

## 隐私与许可证

所有辅助脚本均在本地工作区内读写文件，不会上传任何数据。本仓库采用 [MIT License](LICENSE) 开源（Copyright © 2026 LilHaopeng）。
