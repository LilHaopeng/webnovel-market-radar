from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = REPO_ROOT / "skills" / "webnovel-market-radar"
SCRIPTS_DIR = SKILL_DIR / "scripts"


class WebnovelMarketRadarTests(unittest.TestCase):
    def test_init_and_validate_across_tracks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for track in ("short", "long", "ai-drama", "both"):
                session_dir = root / "扫榜" / f"20261121_test_{track}_{track}"
                r_init = subprocess.run(
                    [
                        sys.executable,
                        str(SCRIPTS_DIR / "init_scan_session.py"),
                        "--root",
                        str(root),
                        "--platform",
                        f"test_{track}",
                        "--track",
                        track,
                        "--source-mode",
                        "baseline",
                        "--outdir",
                        str(session_dir),
                    ],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                )
                self.assertEqual(r_init.returncode, 0, r_init.stderr)
                report_md = session_dir / "扫榜报告.md"
                brief_md = session_dir / "选题简报.md"
                self.assertTrue(report_md.exists())
                self.assertTrue(brief_md.exists())

                # Fill placeholders in the generated template
                import re
                rep_text = report_md.read_text(encoding="utf-8")
                rep_text = rep_text.replace("有效样本数：0", "有效样本数：5")
                rep_text = re.sub(r"\[待填[^\]]*\]", "内置平台基线参考", rep_text)
                report_md.write_text(rep_text, encoding="utf-8")

                brief_text = brief_md.read_text(encoding="utf-8")
                brief_text = re.sub(r"\[待填[^\]]*\]", "校园微恐与应试反差", brief_text)
                brief_md.write_text(brief_text, encoding="utf-8")

                r_val = subprocess.run(
                    [
                        sys.executable,
                        str(SCRIPTS_DIR / "validate_scan.py"),
                        "--dir",
                        str(session_dir),
                    ],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                )
                self.assertEqual(r_val.returncode, 0, r_val.stdout + "\n" + r_val.stderr)


if __name__ == "__main__":
    unittest.main()
