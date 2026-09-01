import unittest
from pathlib import Path


class BookContentsCssTests(unittest.TestCase):
    def test_role_card_caps_sprite_and_mobile_placement(self):
        css = (Path(__file__).parents[1] / 'assets' / 'book-contents.css').read_text(encoding='utf-8')
        self.assertIn('max-width: 200px', css)
        self.assertIn('grid-template-columns: minmax(150px, 200px) minmax(0, 1fr)', css)
        self.assertIn('max-width: 112px', css)
        self.assertIn('aspect-ratio: 1 / 2', css)
        self.assertIn('data:image/webp;base64,', css)
        self.assertIn('background-size: 300% 100%', css)
        self.assertNotIn('animation:', css)


if __name__ == '__main__':
    unittest.main()
