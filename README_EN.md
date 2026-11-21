# Webnovel Market Radar · 网文与 AI 短剧市场扫榜雷达

[简体中文](README.md) | **English**

A tri-track market ranking scanner and topic-brief generator Agent Skill covering **Short Webnovels (8k–50k words)**, **Serialized Long Webnovels (300k+ words)**, and **AI Short Dramas / Comic Dramas / Comedy Shorts**. Prioritizes real-time manual browser simulation via **Ego Browser (`ego-browser`)** or the built-in **`browser` subagent**, enforces anti-hallucination sample quality gates, and outputs standardized `扫榜报告.md` (Market Scan Report) and `选题简报.md` (Topic Brief) files that hand off directly to downstream writing and scriptwriting skills. Current version: **v1.1.0**.

## Three Market Tracks

| Track (`--track`) | Target Platforms | Core Analytical Dimensions | Downstream Handoff |
|---|---|---|---|
| **`short`** (Short Webnovels, 8k–50k words) | Fanqie Short Stories, Zhihu Yanyan, Qimao, Dianzhong, Heiyan | Emotional pain-point rankings, high-concept tropes, word-count sweet spots, opening 3-sentence hook patterns, title/blurb formulas | [Webnovel Short Studio](https://github.com/LilHaopeng/webnovel-short-studio) |
| **`long`** (Long Serialized Webnovels, 300k+ words) | Fanqie, Qidian, Qimao, Jinjiang, Ciweimao | Genre distribution, new-genre vs. new-cheat vs. new-gimmick classification, active-reader & retention metrics, serialization cadence | [Story World / Outline / Prose Suite](https://github.com/LilHaopeng/story-outline-architect) |
| **`ai-drama`** (AI Short Dramas / Comic Dramas / Comedy Shorts) | Hongguo Short Drama (`hongguoduanju.com`), Douyin Short Drama Creator Center (`shortdramas.com`) | Official supply-demand ratio (blue-ocean gap detection), 2D comic vs. 3D photoreal AI vs. comedy animation split, episode counts, top viewer comment pain points, platform multiplier policies (`40×` vs `10×`) | [AI Drama Script Studio](https://github.com/LilHaopeng/ai-drama-script-studio) |
| **`both`** (Cross-Track Comparison) | All platforms above | Cross-medium trend arbitrage from webnovel hits to AI short drama adaptations | Any downstream studio skill |

## Anti-Hallucination & Compliance Gates

1. **4-Tier Browser-First Collection**: Prioritizes local `ego-browser` (reusing authenticated creator dashboard sessions) → built-in `browser` subagent → user-supplied text/screenshots + public web search → offline baseline fallback (`[内置参考降级]`).
2. **Sample Quality Gate (`validate_scan.py`)**: Standard platforms with `< 15` valid entries (or niche charts `< 10`) must be tagged `[数据稀疏]` (Sparse Data). Any session marked `[数据稀疏]` or `[内置参考降级]` is strictly capped at **Medium (`中`)** feasibility—`validate_scan.py` automatically blocks inflated High (`高`) feasibility claims.
3. **Human-in-the-Loop & Anti-Plagiarism**: Pauses immediately for user action if a login screen, paywall, or CAPTCHA appears; collects only public chart metadata and truncated synopses (≤120 chars), never full paid chapters.

## Companion Studio Pipeline

1. **Webnovel Market Radar**: Scans live charts across short fiction, long fiction, and AI dramas to produce verified `选题简报.md` briefs.
2. [Webnovel Short Studio](https://github.com/LilHaopeng/webnovel-short-studio): Consumes short-track briefs to write high-concept short webnovels under 50k words.
3. [AI Drama Script Studio](https://github.com/LilHaopeng/ai-drama-script-studio): Consumes `ai-drama` briefs or existing novels to write MiniMax-H3 AI short dramas, comic dramas, and comedy scripts.
4. [Story World Architect](https://github.com/LilHaopeng/story-world-architect) → [Story Outline Architect](https://github.com/LilHaopeng/story-outline-architect) → [Story Prose Writer](https://github.com/LilHaopeng/story-prose-writer): Full long-form novel worldbuilding, outlining, and prose pipeline.

## Installation

1. **Via `skill-installer` (Codex, etc.)**
   ```text
   $skill-installer Install skills/webnovel-market-radar from https://github.com/LilHaopeng/webnovel-market-radar
   ```
2. **Manual Local Installation (Antigravity / Claude Code / Codex / Cursor)**
   Clone this repository and copy `skills/webnovel-market-radar/` into your client's skills directory:
   - **Antigravity**: `~/.gemini/config/skills/webnovel-market-radar`
   - **Claude Code**: `~/.claude/skills/webnovel-market-radar`
   - **Codex**: `~/.codex/skills/webnovel-market-radar` or `~/.agents/skills/webnovel-market-radar`
   - **Cursor**: `~/.cursor/skills/webnovel-market-radar`

All helper scripts use only the Python 3.10+ standard library.

## Helper Scripts

| Script | Purpose |
|---|---|
| `init_scan_session.py` | Scaffolds a timestamped scan session (`扫榜/{YYYYMMDD}_{platform}_{track}/`) with track-specific `扫榜报告.md` and `选题简报.md` templates. |
| `validate_scan.py` | Validates sample counts, sparse/baseline status tags, feasibility cap rules, synopsis length limits, and downstream handoff blocks. |

Run unit tests:

```bash
python -B -m unittest discover -s tests -v
```

## Privacy & License

All helper scripts operate strictly on local workspace files. Released under the [MIT License](LICENSE) (Copyright © 2026 LilHaopeng).
