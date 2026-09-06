import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/project_check.py"


class ProjectCheckDialogueOwnershipTests(unittest.TestCase):
    def seed(self, root: Path, latest_paragraph: str) -> None:
        manuscript = root / "state/manuscript/Peg_Leg_Greg_Running_Manuscript.md"
        manuscript.parent.mkdir(parents=True)
        manuscript.write_text(
            '# CHAPTER 500\n\n## THE CLEAN\n\n"Fine," Antonius said. He counted the silver.\n\n'
            '# CHAPTER 501\n\n## THE LATEST\n\n'
            + latest_paragraph
            + "\n",
            encoding="utf-8",
        )
        (root / "state/manuscript/Peg_Leg_Greg_Recovered_Ch156-219_EXACT.md").write_text("", encoding="utf-8")

    def run_check(self, root: Path):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "manuscript", "--root", str(root)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

    def test_manuscript_check_reports_latest_dialogue_ownership_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.seed(root, '"Enough," Antonius said. Jorren laughed.')
            result = self.run_check(root)
            self.assertNotEqual(result.returncode, 0)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["latest_canonical_chapter"], 501)
            self.assertEqual(payload["dialogue_ownership"]["errors"], 1)
            self.assertEqual(payload["dialogue_ownership"]["reviews"], 0)
            self.assertEqual(payload["dialogue_ownership"]["findings"][0]["chapter"], 501)
            self.assertIn("duplicate_chapters", payload["errors"])
            self.assertIn("em_dash_count", payload["errors"])
            self.assertIn("stale_lysa_files", payload["errors"])

    def test_manuscript_check_passes_clean_latest_chapter(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.seed(root, '"Enough," Antonius said. He counted the silver.')
            result = self.run_check(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["latest_canonical_chapter"], 501)
            self.assertEqual(payload["dialogue_ownership"]["errors"], 0)
            self.assertEqual(payload["dialogue_ownership"]["reviews"], 0)


if __name__ == "__main__":
    unittest.main()
