import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))

from update_home_contents import chapter_href, load_manifest_chapters, parse_chapter_index, patch_home_contents, render_home_contents


class HomeContentsTests(unittest.TestCase):
    def test_parse_chapter_index_and_keep_illustrated_links(self):
        sample = '# INDEX\n\n1. **THE BOY**\n155. **THE LEAK**\n156. **THE ADVOCATE**\n347. **THE GATE HAND**\n'
        chapters = parse_chapter_index(sample)
        self.assertEqual(chapters[1], 'THE BOY')
        self.assertEqual(chapter_href(156), 'chapters/156.html')
        self.assertEqual(chapter_href(347), 'chapters/347.html')

    def test_manifest_can_extend_a_stale_handwritten_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = Path(tmp) / 'manifest.json'
            manifest.write_text(json.dumps({'latest': 347, 'chapters': [{'number': 249, 'title': 'THE NEXT ONE'}, {'number': 347, 'title': 'THE GATE HAND'}]}), encoding='utf-8')
            chapters = {1: 'THE BOY', 248: 'THE CONSTANT'}
            chapters.update(load_manifest_chapters(manifest))
            self.assertEqual(max(chapters), 347)
            self.assertEqual(chapters[347], 'THE GATE HAND')

    def test_patch_is_repeatable_and_migrates_old_chapter_anchor(self):
        source = '<head>x</head><section aria-labelledby="chapters-heading" class="toc toc-acts" id="chapters"><details>old</details></section><footer>keep</footer>'
        body = '<details class="reader-book">BOOK I</details>'
        first = patch_home_contents(source, body)
        second = patch_home_contents(first, body)
        self.assertEqual(first, second)
        self.assertIn('aria-labelledby="books-heading"', first)
        self.assertIn('id="books"', first)
        self.assertIn('<footer>keep</footer>', first)
        self.assertNotIn('<details>old</details>', first)

    def test_home_renderer_reaches_current_book_iv_and_stays_illustrated(self):
        chapters = {n: f'THE CHAPTER {n}' for n in range(1, 348)}
        chapters[347] = 'THE GATE HAND'
        rendered = render_home_contents(chapters, illustrated=True)
        for label in ('BOOK I', 'BOOK II', 'BOOK III', 'BOOK IV'):
            self.assertIn(label, rendered)
        self.assertIn('Chapters 321–347', rendered)
        self.assertIn('BEYOND THE DOOR', rendered)
        self.assertIn('href="chapters/347.html"', rendered)
        self.assertNotIn('href="light/347.html"', rendered)
        self.assertIn('book-iv-surveyor-331.webp', rendered)
        self.assertNotIn('<details class="reader-book" open>', rendered)


if __name__ == '__main__':
    unittest.main()
