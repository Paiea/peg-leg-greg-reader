import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))

from update_home_contents import parse_chapter_index, chapter_href, patch_home_contents, render_home_contents


class HomeContentsTests(unittest.TestCase):
    def test_parse_chapter_index_and_route_links(self):
        sample = '''# INDEX\n\n1. **THE BOY**\n155. **THE LEAK**\n156. **THE ADVOCATE**\n242. **THE SPENDER**\n'''
        chapters = parse_chapter_index(sample)
        self.assertEqual(chapters[1], 'THE BOY')
        self.assertEqual(chapters[242], 'THE SPENDER')
        self.assertEqual(chapter_href(155, {156, 242}), 'chapters/155.html')
        self.assertEqual(chapter_href(156, {156, 242}), 'light/156.html')
        self.assertEqual(chapter_href(200, {156, 242}), 'light.html?chapter=200')

    def test_patch_is_repeatable_and_scoped(self):
        source = '<head>x</head><section aria-labelledby="chapters-heading" class="toc toc-acts" id="chapters"><details>old</details></section><footer>keep</footer>'
        body = '<section class="reader-book">BOOK I</section>'
        first = patch_home_contents(source, body)
        second = patch_home_contents(first, body)
        self.assertEqual(first, second)
        self.assertIn('READER BOOK CONTENTS START', first)
        self.assertIn('BOOK I', first)
        self.assertIn('<footer>keep</footer>', first)
        self.assertNotIn('<details>old</details>', first)

    def test_home_renderer_can_defer_book_plates_until_assets_exist(self):
        chapters = {n: f'THE CHAPTER {n}' for n in range(1, 243)}
        rendered = render_home_contents(chapters, set(range(156, 243)), illustrated=False)
        self.assertIn('BOOK I', rendered)
        self.assertIn('BOOK II', rendered)
        self.assertIn('BOOK III', rendered)
        self.assertIn('Chapters 83–180', rendered)
        self.assertIn('Chapters 181–242', rendered)
        self.assertNotIn('<img', rendered)


if __name__ == '__main__':
    unittest.main()
