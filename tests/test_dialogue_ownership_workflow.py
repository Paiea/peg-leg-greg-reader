from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/light-edition.yml"


class DialogueOwnershipWorkflowTests(unittest.TestCase):
    def test_strict_latest_check_runs_before_reader_generation(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        step = "- name: Validate latest dialogue ownership\n        run: python scripts/dialogue_ownership_check.py --latest --strict"
        self.assertIn(step, text)
        ownership_index = text.index("Validate latest dialogue ownership")
        test_index = text.index("Test reader tooling")
        illustration_index = text.index("Process illustration production state")
        generation_index = text.index("Generate recovered Light range")
        self.assertGreater(ownership_index, test_index)
        self.assertLess(ownership_index, illustration_index)
        self.assertLess(ownership_index, generation_index)


if __name__ == "__main__":
    unittest.main()
