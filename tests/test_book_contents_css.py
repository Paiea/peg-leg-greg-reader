import unittest
from pathlib import Path


class BookContentsCssTests(unittest.TestCase):
    def test_book_plate_caps_and_mobile_stack(self):
        css = (Path(__file__).parents[1] / 'assets' / 'book-contents.css').read_text(encoding='utf-8')
        self.assertIn('max-width: 340px', css)
        self.assertIn('grid-template-columns: minmax(240px, 320px) minmax(0, 1fr)', css)
        self.assertIn('width: min(82%, 320px)', css)
        self.assertIn('aspect-ratio: 3 / 4', css)
        self.assertNotIn('animation:', css)


if __name__ == '__main__':
    unittest.main()
