import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "scripts" / "sync_r2_role_titles.py"


def write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


class R2RoleTitleSyncTests(unittest.TestCase):
    def make_fixture(self, root: Path):
        (root / "r2" / "assets" / "written").mkdir(parents=True, exist_ok=True)
        (root / "r2" / "data" / "chapters").mkdir(parents=True, exist_ok=True)
        (root / "greg-again" / "audio").mkdir(parents=True, exist_ok=True)

        (root / "r2" / "TITLE_ROLE_AUDIT.md").write_text(
            "# Audit\n\n## Approved title map\n\n```text\n001 The Boy\n002 The Novice\n```\n",
            encoding="utf-8",
        )
        (root / "r2" / "assets" / "written" / "ch001.md").write_text(
            "# Chapter 1: Old One\n\nBody one stays exact.\n",
            encoding="utf-8",
        )
        (root / "r2" / "assets" / "written" / "ch002.md").write_text(
            "# Year Chapter 01: Two Things\n\nBody two stays exact.\n",
            encoding="utf-8",
        )
        write_json(
            root / "r2" / "data" / "project.json",
            {"chapters": ["r2-ch001", "r2-ch002"]},
        )
        write_json(
            root / "r2" / "data" / "chapters" / "ch001.json",
            {
                "chapter_id": "r2-ch001",
                "display_number": 1,
                "title": "Old One",
                "route": "chapter.html?ch=1",
                "written": {"path": "assets/written/ch001.md"},
            },
        )
        write_json(
            root / "r2" / "data" / "chapters" / "ch002.json",
            {
                "chapter_id": "r2-ch002",
                "display_number": 2,
                "title": "Two Things",
                "route": "chapter.html?ch=2",
                "written": {"path": "assets/written/ch002.md"},
            },
        )
        # Deliberately partial. Current R2 production registry trails public authority.
        write_json(
            root / "r2" / "data" / "chapter-registry.json",
            {
                "chapters": {
                    "r2-ch001": {"display_number": 1, "title": "Old One", "status": "published"}
                }
            },
        )
        write_json(
            root / "greg-again" / "audio" / "manifest.json",
            {
                "chapters": [
                    {"chapter_id": "ga-001", "number": 1, "title": "Old One", "file": "001.mp3"},
                    {"chapter_id": "ga-002", "number": 2, "title": "Two Things", "file": "002.mp3"},
                ]
            },
        )

    def run_sync(self, root: Path, *args: str):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(root), *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

    def test_promote_audit_preserves_heading_prefixes_and_prose(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_fixture(root)

            result = self.run_sync(root, "--promote-audit")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

            ch1 = (root / "r2" / "assets" / "written" / "ch001.md").read_text(encoding="utf-8")
            ch2 = (root / "r2" / "assets" / "written" / "ch002.md").read_text(encoding="utf-8")
            self.assertEqual(ch1, "# Chapter 1: The Boy\n\nBody one stays exact.\n")
            self.assertEqual(ch2, "# Year Chapter 01: The Novice\n\nBody two stays exact.\n")

    def test_promote_audit_updates_title_surfaces_without_expanding_registry(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_fixture(root)

            before1 = json.loads((root / "r2" / "data" / "chapters" / "ch001.json").read_text())
            before2 = json.loads((root / "r2" / "data" / "chapters" / "ch002.json").read_text())
            result = self.run_sync(root, "--promote-audit")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

            after1 = json.loads((root / "r2" / "data" / "chapters" / "ch001.json").read_text())
            after2 = json.loads((root / "r2" / "data" / "chapters" / "ch002.json").read_text())
            self.assertEqual(after1["title"], "The Boy")
            self.assertEqual(after2["title"], "The Novice")
            self.assertEqual(after1["chapter_id"], before1["chapter_id"])
            self.assertEqual(after2["chapter_id"], before2["chapter_id"])
            self.assertEqual(after1["route"], before1["route"])
            self.assertEqual(after2["route"], before2["route"])

            registry = json.loads((root / "r2" / "data" / "chapter-registry.json").read_text())
            self.assertEqual(set(registry["chapters"]), {"r2-ch001"})
            self.assertEqual(registry["chapters"]["r2-ch001"]["title"], "The Boy")

            audio = json.loads((root / "greg-again" / "audio" / "manifest.json").read_text())
            self.assertEqual([c["title"] for c in audio["chapters"]], ["The Boy", "The Novice"])
            self.assertEqual([c["file"] for c in audio["chapters"]], ["001.mp3", "002.mp3"])

    def test_check_accepts_partial_registry_after_sync(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_fixture(root)
            applied = self.run_sync(root, "--promote-audit")
            self.assertEqual(applied.returncode, 0, applied.stdout + applied.stderr)

            checked = self.run_sync(root, "--check")
            self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
            self.assertIn("synchronized", checked.stdout.lower())


if __name__ == "__main__":
    unittest.main()
