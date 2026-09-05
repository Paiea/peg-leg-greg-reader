import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))

from update_home_contents import (
    chapter_href,
    load_manifest_chapters,
    parse_chapter_index,
    patch_home_contents,
    render_home_contents,
)


class HomeContentsTests(unittest.TestCase):
    def test_parse_chapter_index_and_keep_illustrated_links(self):
        sample = '''# INDEX\n\n1. **THE BOY**\n155. **THE LEAK**\n156. **THE ADVOCATE**\n242. **THE SPENDER**\n'''
        chapters = parse_chapter_index(sample)
        self.assertEqual(chapters[1], 'THE BOY')
        self.assertEqual(chapters[242], 'THE SPENDER')
        self.assertEqual(chapter_href(155), 'chapters/155.html')
        self.assertEqual(chapter_href(156), 'chapters/156.html')
        self.assertEqual(chapter_href(346), 'chapters/346.html')

    def test_manifest_can_extend_a_stale_handwritten_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = Path(tmp) / 'manifest.json'
            manifest.write_text(json.dumps({
                'latest': 346,
                'chapters': [
                    {'number': 249, 'title': 'THE NEXT ONE'},
                    {'number': 346, 'title': 'THE PASSING POINT'},
                ],
            }), encoding='utf-8')
            chapters = {1: 'THE BOY', 248: 'THE CONSTANT'}
            chapters.update(load_manifest_chapters(manifest))
            self.assertEqual(max(chapters), 346)
            self.assertEqual(chapters[346], 'THE PASSING POINT')

    def test_patch_is_repeatable_scoped_and_migrates_to_books(self):
        source = '<head>x</head><section aria-labelledby="chapters-heading" class="toc toc-acts" id="chapters"><details>old</details></section><footer>keep</footer>'
        body = '<section class="reader-book">BOOK I</section>'
        first = patch_home_contents(source, body)
        second = patch_home_contents(first, body)
        self.assertEqual(first, second)
        self.assertIn('READER BOOK CONTENTS START', first)
        self.assertIn('BOOK I', first)
        self.assertIn('<footer>keep</footer>', first)
        self.assertIn('aria-labelledby="books-heading"', first)
        self.assertIn('id="books"', first)
        self.assertNotIn('chapters-heading', first)
        self.assertNotIn('id="chapters"', first)
        self.assertNotIn('<details>old</details>', first)

    def test_home_renderer_reaches_book_iv_and_stays_illustrated(self):
        chapters = {n: f'THE CHAPTER {n}' for n in range(1, 347)}
        chapters[346] = 'THE PASSING POINT'
        rendered = render_home_contents(chapters, illustrated=True)
        self.assertIn('BOOK I', rendered)
        self.assertIn('BOOK II', rendered)
        self.assertIn('BOOK III', rendered)
        self.assertIn('BOOK IV', rendered)
        self.assertIn('Chapters 321–346', rendered)
        self.assertIn('BEYOND THE DOOR', rendered)
        self.assertIn('href="chapters/346.html"', rendered)
        self.assertNotIn('href="light/346.html"', rendered)
        self.assertIn('book-iv-surveyor-331.webp', rendered)


if __name__ == '__main__':
    unittest.main()
