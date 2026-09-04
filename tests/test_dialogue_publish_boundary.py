from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from dialogue_live_entrypoint import _parse_batch_compat
from generate_illustrated import render_chapter as render_illustrated_chapter
from generate_light import Chapter
from promote_recovered_dialogue import apply_patches_to_recovered

WORKFLOW = ROOT / ".github/workflows/dialogue-attribution-live.yml"


class DialoguePublishBoundaryTests(unittest.TestCase):
    def test_live_workflow_publishes_only_verified_reviewed_range_through_201(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("promote_recovered_dialogue.py 164-167", text)
        self.assertIn("promote_recovered_dialogue.py 198-201", text)
        self.assertIn("generate_illustrated.py 156-201", text)
        self.assertNotIn("generate_light.py 164-201", text)
        self.assertNotIn("git add chapters index.html light latest.html", text)
        self.assertIn("git add chapters state/manuscript/Peg_Leg_Greg_Recovered_Ch156-219_EXACT.md", text)
        self.assertNotIn("164-219", text)

    def test_generated_illustrated_chapter_keeps_reader_shell_and_navigation(self):
        chapter = Chapter(177, "THE STAGEHAND", '<p>Backstage work.</p>', "recovered")
        page = render_illustrated_chapter(chapter, [176, 177, 178], [])
        self.assertIn('<article class="prose">', page)
        self.assertIn('Backstage work.', page)
        self.assertIn('href="176.html"', page)
        self.assertIn('href="178.html"', page)
        self.assertIn('href="../light/177.html"', page)
        self.assertNotIn('<figure class="chapter-art', page)

    def test_generated_illustrated_chapter_uses_available_art_without_requiring_it(self):
        chapter = Chapter(177, "THE STAGEHAND", '<p>Before.</p>\n<p>After.</p>', "recovered")
        page = render_illustrated_chapter(chapter, [177], [Path('visual/chapter_art/177/example.webp')])
        self.assertIn('../visual/chapter_art/177/example.webp', page)
        self.assertEqual(page.count('<figure class="chapter-art scene-illustration">'), 1)

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

    def test_parser_folds_wrapped_blockquote_lines_into_one_paragraph(self):
        batch = '''## Chapter 164 - THE PROSPECTOR

### Patch 164-A

Current:

> Greg had money.
>
> That fact was still strange enough that I stood there for a moment
> deciding whether hot food was worth one copper.

Replace with:

> I had money.
>
> That fact was still strange enough that I stood there for a moment
> deciding whether hot food was worth one copper.

Reason:
first-person continuity
'''
        patch = _parse_batch_compat(batch, "batch.md", 164, 164)[0]
        self.assertEqual(patch.current, (
            "Greg had money.",
            "That fact was still strange enough that I stood there for a moment deciding whether hot food was worth one copper.",
        ))
        self.assertEqual(patch.replacement, (
            "I had money.",
            "That fact was still strange enough that I stood there for a moment deciding whether hot food was worth one copper.",
        ))

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
