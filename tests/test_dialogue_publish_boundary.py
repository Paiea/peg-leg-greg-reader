from pathlib import Path
import tempfile
import unittest

from scripts.apply_dialogue_attribution_patches import _parse_batch
from scripts.promote_recovered_dialogue import apply_patches_to_recovered


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/dialogue-attribution-live.yml"


class DialoguePublishBoundaryTests(unittest.TestCase):
    def test_live_workflow_publishes_reviewed_range_through_163(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("--min-chapter 100 --max-chapter 155", text)
        self.assertIn("'100-137' --docx state/manuscript/Peg_Leg_Greg_Book2_Manuscript_Ch83-137.docx", text)
        self.assertIn("promote_recovered_dialogue.py", text)
        self.assertIn("156-163", text)
        self.assertIn("generate_light.py 100-163", text)

    def test_parser_accepts_patch_heading_and_blockquote_paragraphs(self):
        batch = '''## Chapter 156 - THE ADVOCATE

### Patch 156-A

Current:

> Lorn said, "Otherwise Orin comes in for no reason."
>
> "To arrest the Chancellor."

Replace only the untagged answer with:

> Lorn said, "Otherwise Orin comes in for no reason."
>
> Lorn said, "To arrest the Chancellor."

Reason:
clear speaker hinge
'''
        patches = _parse_batch(batch, "batch.md", 156, 156)
        self.assertEqual(len(patches), 1)
        self.assertEqual(patches[0].current[-1], '"To arrest the Chancellor."')
        self.assertEqual(patches[0].replacement[-1], 'Lorn said, "To arrest the Chancellor."')

    def test_recovered_promotion_replaces_only_requested_chapter_paragraphs(self):
        source = '''# RECOVERED

# CHAPTER 156
## THE ADVOCATE

Before.

"To arrest the Chancellor."

After.

# CHAPTER 157
## THE TABLE

"To arrest the Chancellor."
'''
        batch = '''## Chapter 156 - THE ADVOCATE

### Patch 156-A

Current:

> "To arrest the Chancellor."

Replace with:

> Lorn said, "To arrest the Chancellor."

Reason:
clear speaker hinge
'''
        patch = _parse_batch(batch, "batch.md", 156, 156)[0]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "recovered.md"
            path.write_text(source, encoding="utf-8")
            changed = apply_patches_to_recovered(path, [patch], 156, 156)
            self.assertTrue(changed)
            text = path.read_text(encoding="utf-8")
            self.assertIn('Lorn said, "To arrest the Chancellor."', text)
            self.assertEqual(text.count('Lorn said, "To arrest the Chancellor."'), 1)
            self.assertEqual(text.count('"To arrest the Chancellor."'), 2)


if __name__ == "__main__":
    unittest.main()
