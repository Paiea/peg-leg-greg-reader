import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))

from generate_light import Chapter, chapter_nav, clean_numeric_pages, render_chapter, render_index
from showcase import build_showcase_map


class LightShowcaseTests(unittest.TestCase):
    def setUp(self):
        self.showcase = build_showcase_map([1, 2, 3, 4], {
            'version': 1,
            'mode': 'whole_chapter_only',
            'default': 'visible',
            'chapters': {'3': {'showcase': False, 'reason': 'pacing'}},
        })
        self.chapters = {
            n: Chapter(n, f'THE {n}', '<p>Body.</p>', 'published')
            for n in range(1, 5)
        }

    def test_navigation_skips_hidden_canon_and_labels_showcase_number(self):
        prev_html, next_html = chapter_nav(self.chapters[2], {1, 2, 4}, self.showcase)
        self.assertIn('004.html', next_html)
        self.assertIn('Chapter 3', next_html)
        self.assertNotIn('003.html', next_html)

    def test_rendered_chapter_uses_showcase_heading(self):
        rendered = render_chapter(self.chapters[4], {1, 2, 4}, self.showcase)
        self.assertIn('TEXT READER · CHAPTER 3', rendered)
        self.assertIn('<title>Chapter 3:', rendered)

    def test_index_excludes_hidden_canon_and_uses_canonical_paths(self):
        rendered = render_index(self.chapters, {1, 2, 4}, self.showcase)
        self.assertIn('href="004.html"', rendered)
        self.assertIn('<span class="num">3</span>', rendered)
        self.assertNotIn('href="003.html"', rendered)

    def test_cleanup_removes_hidden_and_unknown_numeric_text_pages(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            for number in (1, 2, 3, 4, 9):
                (directory / f'{number:03d}.html').write_text('page', encoding='utf-8')
            clean_numeric_pages(directory, set(self.chapters), self.showcase)
            self.assertTrue((directory / '001.html').exists())
            self.assertTrue((directory / '002.html').exists())
            self.assertFalse((directory / '003.html').exists())
            self.assertTrue((directory / '004.html').exists())
            self.assertFalse((directory / '009.html').exists())


if __name__ == '__main__':
    unittest.main()
