import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))

from generate_light import Chapter, render_index


class LightIndexTests(unittest.TestCase):
    def test_light_index_uses_same_book_hierarchy_without_range_duplicates(self):
        chapters = {
            n: Chapter(n, f'THE CHAPTER {n}', '<p>Body</p>', 'test')
            for n in range(1, 243)
        }
        rendered = render_index(chapters, set(chapters))
        self.assertIn('BOOK I', rendered)
        self.assertIn('BOOK II', rendered)
        self.assertIn('BOOK III', rendered)
        self.assertIn('THE STAGE DOOR', rendered)
        self.assertIn('THE WORKING COMPANY', rendered)
        self.assertIn('THE PRICE OF ATTENTION', rendered)
        self.assertIn('Chapters 83–180', rendered)
        self.assertIn('Chapters 181–242', rendered)
        self.assertIn('../assets/book-contents.css', rendered)
        self.assertNotIn('class="light-range"', rendered)
        self.assertNotIn('<img', rendered)
        self.assertEqual(rendered.count('href="220.html"'), 1)


if __name__ == '__main__':
    unittest.main()
