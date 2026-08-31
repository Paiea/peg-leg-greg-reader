import json
import struct
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CHECK = ROOT / "scripts/project_check.py"


def run_check(project: Path, command: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["python", str(CHECK), command, "--root", str(project)],
        text=True,
        capture_output=True,
        check=False,
    )


class ProjectCheckTests(unittest.TestCase):
    def test_manuscript_check_rejects_em_dash_and_duplicate_headings(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "state/manuscript/Peg_Leg_Greg_Running_Manuscript.md"
            path.parent.mkdir(parents=True)
            path.write_text(
                "# PEG-LEG GREG — RUNNING MANUSCRIPT\n"
                "# CHAPTER 220\nText — bad.\n# CHAPTER 220\nDuplicate.",
                encoding="utf-8",
            )
            result = run_check(root, "manuscript")
            payload = json.loads(result.stdout)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(payload["errors"]["em_dash_count"], 1)
            self.assertEqual(payload["errors"]["duplicate_chapters"], [220])

    def test_reader_check_reports_broken_local_image_reference(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            page = root / "chapters/001.html"
            page.parent.mkdir(parents=True)
            page.write_text('<img src="../visual/missing.png">', encoding="utf-8")
            result = run_check(root, "reader")
            payload = json.loads(result.stdout)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(
                payload["errors"]["broken_image_references"],
                [{"chapter": 1, "asset_path": "visual/missing.png"}],
            )

    def test_assets_check_warns_without_failing_for_unused_low_resolution_image(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "visual/development/small.png"
            path.parent.mkdir(parents=True)
            path.write_bytes(
                b"\x89PNG\r\n\x1a\n"
                + struct.pack(">I", 13)
                + b"IHDR"
                + struct.pack(">II", 200, 100)
                + b"\x08\x02\x00\x00\x00"
            )
            result = run_check(root, "assets")
            payload = json.loads(result.stdout)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(payload["warnings"]["unused_assets"], 1)
            self.assertEqual(payload["warnings"]["low_resolution_assets"], 1)

    def test_all_combines_check_results(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manuscript = root / "state/manuscript/Peg_Leg_Greg_Running_Manuscript.md"
            manuscript.parent.mkdir(parents=True)
            manuscript.write_text("# CHAPTER 220\nText.", encoding="utf-8")
            chapter_root = root / "chapters"
            chapter_root.mkdir(parents=True)
            for number in range(1, 156):
                (chapter_root / f"{number:03d}.html").write_text(
                    "<p>Text</p>", encoding="utf-8"
                )
            result = run_check(root, "all")
            payload = json.loads(result.stdout)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(set(payload["checks"]), {"assets", "manuscript", "reader"})


if __name__ == "__main__":
    unittest.main()
