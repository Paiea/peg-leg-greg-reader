from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/dialogue-attribution-live.yml"


class DialoguePublishBoundaryTests(unittest.TestCase):
    def test_live_workflow_publishes_reviewed_range_through_163(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("--min-chapter 100 --max-chapter 155", text)
        self.assertIn("'100-137' --docx state/manuscript/Peg_Leg_Greg_Book2_Manuscript_Ch83-137.docx", text)
        self.assertIn("state/manuscript/Peg_Leg_Greg_Recovered_Ch156-219_EXACT.md", text)
        self.assertIn("156-163", text)
        self.assertIn("generate_light.py 100-163", text)
        self.assertIn("generate_illustrated.py 156-163", text)


if __name__ == "__main__":
    unittest.main()
