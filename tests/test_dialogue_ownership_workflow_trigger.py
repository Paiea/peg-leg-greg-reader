from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/light-edition.yml"


class DialogueOwnershipWorkflowTriggerTests(unittest.TestCase):
    def test_light_workflow_watches_dialogue_ownership_checker(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("scripts/dialogue_ownership_check.py", text)


if __name__ == "__main__":
    unittest.main()
