#!/usr/bin/env python3
"""Validate market radar outputs (扫榜报告.md & 选题简报.md) for quality gates and downstream handoff."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


PLACEHOLDER_RE = re.compile(r"\[待填[^\]\n]*\]")
SAMPLE_COUNT_RE = re.compile(r"^-\s*有效样本数[：:]\s*(\d+)", re.M)
QUALITY_RE = re.compile(r"^-\s*数据质量[：:]\s*(.+)$", re.M)
DATE_RE = re.compile(r"^-\s*扫榜日期[：:]\s*(\d{4}-\d{2}-\d{2})", re.M)
SOURCE_RE = re.compile(r"^-\s*数据来源[：:]\s*(.+)$", re.M)
RESCAN_RE = re.compile(r"^-\s*建议复扫时间[：:]\s*(\d{4}-\d{2}-\d{2})", re.M)
FEASIBILITY_RE = re.compile(r"^-\s*可行性[：:]\s*([^\s—\-]+)", re.M)

REQUIRED_HANDOFF_KEYS = (
    "推荐写作管线",
    "目标平台",
    "建议体量模板",
    "建议推进叙事类型",
    "核心情绪痛点",
    "差异化原创脑洞切口",
    "可行性",
    "失败风险",
    "最小验证动作",
)


@dataclass
class CheckIssue:
    level: str  # "error" or "warning"
    file: str
    code: str
    message: str


def extract_quality(text: str) -> str:
    m = QUALITY_RE.search(text)
    if not m:
        return ""
    val = m.group(1).strip().strip("[]")
    return val


def validate_session(scan_dir: Path, small_platform: bool = False) -> tuple[list[CheckIssue], dict[str, Any]]:
    issues: list[CheckIssue] = []
    report_path = scan_dir / "扫榜报告.md"
    brief_path = scan_dir / "选题简报.md"

    min_samples = 10 if small_platform else 15
    report_quality = ""
    sample_count: int | None = None

    if not report_path.is_file():
        issues.append(CheckIssue("error", "扫榜报告.md", "missing_report", "缺少 扫榜报告.md。"))
    else:
        r_text = report_path.read_text(encoding="utf-8-sig")
        if PLACEHOLDER_RE.search(r_text):
            issues.append(CheckIssue("error", "扫榜报告.md", "unfilled_placeholder", "仍包含未填写的 [待填...] 占位符。"))
        if not DATE_RE.search(r_text):
            issues.append(CheckIssue("error", "扫榜报告.md", "missing_date", "缺少 YYYY-MM-DD 格式的「扫榜日期」。"))
        if not SOURCE_RE.search(r_text):
            issues.append(CheckIssue("error", "扫榜报告.md", "missing_source", "缺少「数据来源」字段。"))
        if not RESCAN_RE.search(r_text):
            issues.append(CheckIssue("warning", "扫榜报告.md", "missing_rescan_date", "建议填写「建议复扫时间」以防止过时风口误导。"))

        m_cnt = SAMPLE_COUNT_RE.search(r_text)
        if not m_cnt:
            issues.append(CheckIssue("error", "扫榜报告.md", "missing_sample_count", "缺少数字格式的「有效样本数」。"))
        else:
            sample_count = int(m_cnt.group(1))

        report_quality = extract_quality(r_text)
        if not report_quality:
            issues.append(CheckIssue("error", "扫榜报告.md", "missing_quality_tag", "缺少「数据质量」（OK / 数据稀疏 / 内置参考降级）。"))
        elif sample_count is not None:
            if sample_count == 0 and "内置参考降级" not in report_quality:
                issues.append(
                    CheckIssue(
                        "error",
                        "扫榜报告.md",
                        "zero_samples_wrong_quality",
                        "有效样本数为 0 时，数据质量必须标注为「内置参考降级」。",
                    )
                )
            elif 0 < sample_count < min_samples and "数据稀疏" not in report_quality and "内置参考降级" not in report_quality:
                issues.append(
                    CheckIssue(
                        "error",
                        "扫榜报告.md",
                        "sparse_sample_unmarked",
                        f"有效样本数 {sample_count} < {min_samples}，按质量门必须标注「数据稀疏」。",
                    )
                )

    topic_count = 0
    high_feasibility_count = 0
    if not brief_path.is_file():
        issues.append(CheckIssue("error", "选题简报.md", "missing_brief", "缺少 选题简报.md。"))
    else:
        b_text = brief_path.read_text(encoding="utf-8-sig")
        if PLACEHOLDER_RE.search(b_text):
            issues.append(CheckIssue("error", "选题简报.md", "unfilled_placeholder", "仍包含未填写的 [待填...] 占位符。"))

        brief_quality = extract_quality(b_text)
        effective_quality = brief_quality or report_quality
        is_degraded = ("数据稀疏" in effective_quality) or ("内置参考降级" in effective_quality) or (
            sample_count is not None and sample_count < min_samples
        )

        # Split topic sections by "### 选题"
        topic_blocks = re.split(r"(?=^###\s+选题)", b_text, flags=re.M)
        topic_sections = [blk for blk in topic_blocks if re.match(r"^###\s+选题", blk)]
        topic_count = len(topic_sections)
        if topic_count == 0:
            issues.append(CheckIssue("error", "选题简报.md", "no_topics", "未检测到任何「### 选题 N：...」条目。"))

        for idx, blk in enumerate(topic_sections, start=1):
            missing_keys = [
                k for k in REQUIRED_HANDOFF_KEYS if not re.search(rf"^-\s*{re.escape(k)}[：:]", blk, re.M)
            ]
            if missing_keys:
                issues.append(
                    CheckIssue(
                        "error",
                        "选题简报.md",
                        "missing_handoff_fields",
                        f"选题 {idx} 缺少下游交接必填字段：{'、'.join(missing_keys)}。",
                    )
                )

            m_feas = FEASIBILITY_RE.search(blk)
            if m_feas:
                rating = m_feas.group(1).strip("[]`*")
                if rating == "高":
                    high_feasibility_count += 1
                    if is_degraded:
                        degraded_reason = (
                            effective_quality
                            if ("数据稀疏" in effective_quality or "内置参考降级" in effective_quality)
                            else f"有效样本仅 {sample_count} < {min_samples}（样本不足）"
                        )
                        issues.append(
                            CheckIssue(
                                "error",
                                "选题简报.md",
                                "degraded_high_feasibility",
                                f"选题 {idx} 标注了「可行性：高」，但当前为「{degraded_reason}」，按防幻觉规则可行性最高只能给「中」。",
                            )
                        )

    summary = {
        "scan_dir": str(scan_dir),
        "sample_count": sample_count,
        "min_samples_threshold": min_samples,
        "data_quality": report_quality,
        "topics": topic_count,
        "high_feasibility_topics": high_feasibility_count,
        "errors": sum(1 for i in issues if i.level == "error"),
        "warnings": sum(1 for i in issues if i.level == "warning"),
    }
    return issues, summary


def main() -> int:
    parser = argparse.ArgumentParser(
        description="校验网文扫榜目录中的 扫榜报告.md 与 选题简报.md 是否通过质量门与下游交接契约。"
    )
    parser.add_argument("--dir", required=True, type=Path, help="本次扫榜输出目录")
    parser.add_argument(
        "--small-platform",
        action="store_true",
        help="小平台或细分短篇榜模式（有效样本门槛由 15 放宽至 10）",
    )
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    args = parser.parse_args()

    scan_dir = args.dir.expanduser().resolve()
    if not scan_dir.is_dir():
        print(f"ERROR: Scan directory not found: {scan_dir}", file=sys.stderr)
        return 2

    issues, summary = validate_session(scan_dir, small_platform=args.small_platform)
    if args.json:
        print(json.dumps({"summary": summary, "issues": [asdict(i) for i in issues]}, ensure_ascii=False, indent=2))
    else:
        print(f"dir={summary['scan_dir']}")
        print(
            f"samples={summary['sample_count']} quality={summary['data_quality']} "
            f"topics={summary['topics']} errors={summary['errors']} warnings={summary['warnings']}"
        )
        for iss in issues:
            print(f"  [{iss.level.upper()}] {iss.file} ({iss.code}): {iss.message}")
    return 1 if summary["errors"] > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
