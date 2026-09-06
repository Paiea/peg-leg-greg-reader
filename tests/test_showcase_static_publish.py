import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))

from showcase import build_showcase_map
from update_showcase_chapter_shells import patch_illustrated_html


class ShowcaseStaticPublishTests(unittest.TestCase):
    def setUp(self):
        self.showcase = build_showcase_map(
            [1, 2, 3, 4],
            {
                'version': 1,
                'mode': 'whole_chapter_only',
                'default': 'visible',
                'chapters': {'2': {'showcase': False, 'reason': 'pacing'}},
            },
        )

    def test_visible_static_page_keeps_prose_and_art_but_skips_hidden_neighbor(self):
        original = '''<!doctype html><html><head><title>Chapter 1: The Boy — Peg-Leg Greg</title></head><body><main class="chapter-shell"><header class="chapter-title"><div class="number">CHAPTER 1</div><h1>THE BOY</h1></header><article class="prose"><p>Exact prose.</p><figure><img src="art.webp"></figure></article></main></body></html>'''
        updated = patch_illustrated_html(original, 1, self.showcase)
        self.assertIn('<article class="prose"><p>Exact prose.</p><figure><img src="art.webp"></figure></article>', updated)
        self.assertIn('<div class="number">CHAPTER 1</div>', updated)
        self.assertIn('rel="next" href="003.html">Chapter 2 →</a>', updated)
        self.assertNotIn('href="002.html"', updated)
        self.assertEqual(updated.count('class="chapter-nav'), 2)

    def test_visible_page_after_hidden_chapter_uses_contiguous_showcase_number(self):
        original = '''<!doctype html><html><head><title>Chapter 3: Three — Peg-Leg Greg</title></head><body><main class="chapter-shell"><nav class="chapter-nav"><a rel="prev" href="002.html">← Chapter 2</a><a href="../index.html#chapters">Chapters</a><a rel="next" href="004.html">Chapter 4 →</a></nav><header class="chapter-title"><div class="number">CHAPTER 3</div><h1>THREE</h1></header><article class="prose"><p>Body.</p></article><nav class="chapter-nav"><a>stale</a></nav></main></body></html>'''
        updated = patch_illustrated_html(original, 3, self.showcase)
        self.assertIn('<title>Chapter 2: Three', updated)
        self.assertIn('<div class="number">CHAPTER 2</div>', updated)
        self.assertIn('rel="prev" href="001.html">← Chapter 1</a>', updated)
        self.assertIn('rel="next" href="004.html">Chapter 3 →</a>', updated)
        self.assertNotIn('#chapters', updated)

    def test_hidden_canonical_page_is_left_as_canon_archive(self):
        original = '<html><body><div class="number">CHAPTER 2</div><article class="prose"><p>Canon only.</p></article></body></html>'
        self.assertEqual(patch_illustrated_html(original, 2, self.showcase), original)


if __name__ == '__main__':
    unittest.main()
