#!/usr/bin/env python3
"""Initialize a unified short/long webnovel market scan session directory and templates."""

from __future__ import annotations

import argparse
import re
from datetime import date, timedelta
from pathlib import Path


def safe_root(raw: str) -> Path:
    root = Path(raw).expanduser().resolve()
    if root.parent == root:
        raise ValueError("Refusing to initialize a filesystem root.")
    return root


def sanitize_slug(text: str) -> str:
    cleaned = re.sub(r"[\\/:*?\"<>|\s]+", "_", text.strip())
    return cleaned.strip("_") or "multi"


def build_report_template(
    platform: str,
    track: str,
    source_mode: str,
    scan_date: str,
    rescan_date: str,
) -> str:
    quality_default = "内置参考降级" if source_mode == "baseline" else "[待填：OK / 数据稀疏 / 内置参考降级]"
    source_default = (
        "内置历史参考基线（未完成实时榜单校验）"
        if source_mode == "baseline"
        else "[待填：本次实采公开榜单 URL 或用户投喂来源]"
    )

    extra_section = ""
    if track in ("short", "both"):
        extra_section += """
## 短篇专项维度（情绪与传播）

### 情绪热度排行
| 排名 | 情绪类型 | 榜上样本数 | 趋势 | 代表作（仅作样本记录） |
|---|---|---|---|---|
| 1 |  |  | ↑/→/↓ |  |

### 短篇核心特征洞察
- 主力篇幅区间：
- 高频开头 3 句模式：
- 结局偏好（HE / BE / 开放式）：
- 标题与导语/简介规律：
- 高频主角人设：
"""
    if track in ("long", "both"):
        extra_section += """
## 长篇专项维度（题材与追读）

### 题材热度排行
| 排名 | 题材 / 细分标签组合 | 榜上样本数 | 趋势 | 代表作（仅作样本记录） |
|---|---|---|---|---|
| 1 |  |  | ↑/→/↓ |  |

### 新元素三级甄别（跨样本重复才标趋势）
- **新题材信号**：
- **新金手指 / 机制变体**：
- **高频新噱头（警惕同质化）**：
- **主力字数区间与书名热词**：
"""

    if track == "ai-drama":
        extra_section += """
## AI 短剧 / 漫剧专项维度（创作者后台供需 + 红果实采）

### 1. 官方供需与飙升蓝海交叉（来自短剧创作者中心 `shortdramas.com`）
| 题材 | 供需/飙升表现 | 新上作品数 | 官方核心创意标签 | 竞争评估（蓝海/红海） |
|---|---|---|---|---|
|  |  |  |  |  |

### 2. AI 剧 vs 漫剧爆款样本与热评洞察（来自红果 `hongguoduanju.com` + 抖音热播榜）
| 排名 | 剧名 | 形态（AI剧/漫剧/沙雕） | 热度 / 收藏 / 季数集数 | 核心卖点与热评爽点/雷点 |
|---|---|---|---|---|
| 1 |  |  |  |  |

### 3. 平台政策与激励风向
- 最新官方激励计划 / 审稿红线（如 40× 旁白 ≤20% 线、虚拟形象确权等）：
"""

    return f"""# 网文扫榜报告：{platform}（{track}）

- 扫榜日期：{scan_date}
- 赛道类型：{track}
- 采集方式：{source_mode}
- 数据来源：{source_default}
- 有效样本数：0
- 数据质量：{quality_default}
- 建议复扫时间：{rescan_date}
- 问题摘要：无

---

## 市场概况
- 核心发现：[待基于有效样本总结]
{extra_section}
## 风口与饱和预警
- 正在爆发：
- 即将起风：
- 即将饱和 / AI 同质化高危区：

## 清洗后公开样本明细（简介截断 ≤120 字）

| 排名 | 书名 | 题材/标签 | 核心公开指标（在读/热度/收藏/字数） | 截断公开简介 |
|---|---|---|---|---|
"""


def build_brief_template(
    platform: str,
    track: str,
    source_mode: str,
    scan_date: str,
) -> str:
    quality_default = "内置参考降级" if source_mode == "baseline" else "[待填：OK / 数据稀疏 / 内置参考降级]"
    default_pipeline = (
        "`webnovel-short-studio`"
        if track == "short"
        else "`ai-drama-script-studio`"
        if track == "ai-drama"
        else "`story-world-architect` → `story-outline-architect` → `story-prose-writer`（或短篇试水走 `webnovel-short-studio`）"
    )
    default_template = (
        "flash 或 microdrama"
        if track == "short"
        else "ai-drama（MiniMax-H3写实）/ comic-drama（高奇观漫剧）/ shadiao（沙雕短剧）"
        if track == "ai-drama"
        else "long（或先用 flash/microdrama 试水）"
    )
    feasibility_note = (
        "中 — 内置参考降级模式强制封顶「中」，动笔前须实时复扫或小成本试水"
        if source_mode == "baseline"
        else "[高/中/低] — [写清同类样本数、趋势与依据；数据稀疏时不得标高]"
    )

    return f"""# 选题简报：{platform}（{track}）

- 扫榜日期：{scan_date}
- 对应扫榜报告：`扫榜报告.md`
- 赛道类型：{track}
- 采集方式：{source_mode}
- 有效样本数：0
- 数据质量：{quality_default}

> 下游交接说明：本文件可直接喂给 `webnovel-short-studio`（5万字以内短篇/微短剧）、`ai-drama-script-studio`（AI 短剧/漫剧/沙雕短剧完整季播剧本）或传统长篇三件套。下游仅吸收市场情绪骨架与平台特征，**强制置换核心脑洞、规则机制、人物与反转角度**，严禁照抄榜上作品剧情。

---

## 推荐选题（按可行性从高到低排序，2–3 个为宜）

### 选题 1：[待填：一句话选题方向]
- 推荐写作管线：{default_pipeline}
- 目标平台：{platform}
- 建议体量模板：{default_template}
- 建议推进叙事类型：[dialogue / first_person / rules / 传统多维叙事]
- 建议对话引号：[“” / 「」（知乎盐言）]
- 题材与情绪组合：[主题材 + 核心情绪拉扯]
- 核心情绪痛点：[读者最买单的情绪缺口]
- 能爆假设：[跨样本总结的爆点逻辑]（`待试写/市场验证`）
- 市场验证：[同类样本 N 本 + 趋势 ↑/→/↓ + 同质化/反例观察]
- 差异化原创脑洞切口：[强制置换的新规则 / 新身份 / 新反转方向]
- 标题与导语参考方向：[适配目标平台的标题风格与导语字数建议]
- 可行性：{feasibility_note}
- 失败风险：[最容易崩的点]
- 最小验证动作：[如先跑脑洞4问压测并试写前500字定调]
"""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="初始化统一网文扫榜目录，生成标准 扫榜报告.md 与 选题简报.md 模板。"
    )
    parser.add_argument("--root", required=True, help="工作区或项目根目录（将在其下创建 扫榜/...）")
    parser.add_argument("--platform", required=True, help="目标平台名称（如 番茄短故事、知乎盐言、起点、多平台）")
    parser.add_argument(
        "--track",
        choices=("short", "long", "ai-drama", "both"),
        default="short",
        help="扫榜赛道：short（短篇网文）/ long（长篇网文）/ ai-drama（AI短剧与漫剧）/ both（跨体量）",
    )
    parser.add_argument(
        "--source-mode",
        choices=("ego-browser", "builtin-browser", "user-input", "baseline"),
        default="ego-browser",
        help="采集方式标记",
    )
    parser.add_argument("--outdir", default="", help="可选自定义输出目录（默认 <root>/扫榜/<YYYYMMDD>_<平台>_<track>）")
    parser.add_argument("--dry-run", action="store_true", help="仅预览不写入")
    args = parser.parse_args()

    try:
        root = safe_root(args.root)
    except ValueError as exc:
        parser.error(str(exc))

    today = date.today()
    scan_date = today.isoformat()
    rescan_days = 14 if args.track == "ai-drama" else (21 if args.track in ("short", "both") else 45)
    rescan_date = (today + timedelta(days=rescan_days)).isoformat()

    if args.outdir.strip():
        out_dir = Path(args.outdir).expanduser().resolve()
    else:
        slug = sanitize_slug(args.platform)
        out_dir = root / "扫榜" / f"{today.strftime('%Y%m%d')}_{slug}_{args.track}"

    files = {
        "扫榜报告.md": build_report_template(
            platform=args.platform.strip(),
            track=args.track,
            source_mode=args.source_mode,
            scan_date=scan_date,
            rescan_date=rescan_date,
        ),
        "选题简报.md": build_brief_template(
            platform=args.platform.strip(),
            track=args.track,
            source_mode=args.source_mode,
            scan_date=scan_date,
        ),
    }

    if not args.dry_run:
        out_dir.mkdir(parents=True, exist_ok=True)

    created: list[Path] = []
    skipped: list[Path] = []
    for name, content in files.items():
        dest = out_dir / name
        if dest.exists():
            skipped.append(dest)
            continue
        created.append(dest)
        if not args.dry_run:
            dest.write_text(content.rstrip() + "\n", encoding="utf-8")

    print(f"outdir={out_dir}")
    print(f"track={args.track} source_mode={args.source_mode}")
    print(f"created={len(created)}")
    for p in created:
        print(f"  + {p.name}")
    print(f"skipped={len(skipped)}")
    for p in skipped:
        print(f"  = {p.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
