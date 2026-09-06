import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))
sys.path.insert(0, str(Path(__file__).parents[1]))

from generate_illustrated import render_chapter
from generate_light import Chapter
from showcase import build_showcase_map


class IllustratedShowcaseTests(unittest.TestCase):
    def test_hidden_canon_is_skipped_but_paths_remain_canonical(self):
        showcase = build_showcase_map([1, 2, 3, 4], {
            'version': 1,
            'mode': 'whole_chapter_only',
            'default': 'visible',
            'chapters': {'3': {'showcase': False, 'reason': 'pacing'}},
        })
        chapter = Chapter(2, 'THE BORROWER', '<p>Body.</p>', 'published')
        rendered = render_chapter(chapter, [], showcase, {})
        self.assertIn('CHAPTER 2', rendered)
        self.assertIn('href="004.html">Chapter 3 →</a>', rendered)
        self.assertNotIn('href="003.html"', rendered)

    def test_later_canon_uses_showcase_number_in_heading_and_metadata(self):
        showcase = build_showcase_map([1, 2, 3, 4], {
            'version': 1,
            'mode': 'whole_chapter_only',
            'default': 'visible',
            'chapters': {'3': {'showcase': False, 'reason': 'pacing'}},
        })
        chapter = Chapter(4, 'THE EXPERT', '<p>Body.</p>', 'published')
        rendered = render_chapter(chapter, [], showcase, {})
        self.assertIn('CHAPTER 3', rendered)
        self.assertIn('Peg-Leg Greg Chapter 3: The Expert.', rendered)
        self.assertIn('href="002.html">← Chapter 2</a>', rendered)
        self.assertNotIn('CHAPTER 4</div>', rendered)


if __name__ == '__main__':
    unittest.main()
