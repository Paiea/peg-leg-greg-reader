from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from dialogue_live_entrypoint import _parse_batch_compat
from promote_recovered_dialogue import apply_patches_to_recovered

WORKFLOW = ROOT / ".github/workflows/dialogue-attribution-live.yml"


class DialoguePublishBoundaryTests(unittest.TestCase):
    def test_live_workflow_publishes_reviewed_range_through_163(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("--min-chapter 100 --max-chapter 155", text)
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
        patches = _parse_batch_compat(batch, "batch.md", 156, 156)
        self.assertEqual(len(patches), 1)
        self.assertEqual(patches[0].current[-1], '"To arrest the Chancellor."')
        self.assertEqual(patches[0].replacement[-1], 'Lorn said, "To arrest the Chancellor."')

    def test_recovered_promotion_is_chapter_scoped(self):
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
        patch = _parse_batch_compat(batch, "batch.md", 156, 156)[0]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "recovered.md"
            path.write_text(source, encoding="utf-8")
            self.assertTrue(apply_patches_to_recovered(path, [patch], 156, 156))
            text = path.read_text(encoding="utf-8")
            self.assertEqual(text.count('Lorn said, "To arrest the Chancellor."'), 1)
            self.assertEqual(text.count('"To arrest the Chancellor."'), 2)


if __name__ == "__main__":
    unittest.main()
