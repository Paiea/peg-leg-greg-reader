import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from chapter_dependency_scan import scan_dependencies


class DependencyScanScopeTests(unittest.TestCase):
    def test_generated_exports_are_outside_migration_scan_scope(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "state").mkdir()
            (root / "exports").mkdir()
            (root / "state/live.md").write_text("See Chapter 17.", encoding="utf-8")
            (root / "exports/generated.md").write_text("See Chapter 999.", encoding="utf-8")

            report = scan_dependencies(root)

            self.assertIn("17", report["by_chapter"])
            self.assertNotIn("999", report["by_chapter"])


if __name__ == "__main__":
    unittest.main()
