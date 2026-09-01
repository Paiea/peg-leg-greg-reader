import unittest
from pathlib import Path


class BookContentsCssTests(unittest.TestCase):
    def test_role_card_caps_sprite_and_mobile_placement(self):
        root = Path(__file__).parents[1] / 'assets'
        css = (root / 'book-contents.css').read_text(encoding='utf-8')
        base_css = (root / 'book-contents-base.css').read_text(encoding='utf-8')
        self.assertIn('max-width: 280px', css)
        self.assertIn('grid-template-columns: minmax(240px, 280px) minmax(0, 1fr)', css)
        self.assertIn('max-width: 210px', css)
        self.assertIn('aspect-ratio: 1 / 2', base_css)
        self.assertIn('data:image/webp;base64,', base_css)
        self.assertIn('background-size: 300% 100%', base_css)
        self.assertNotIn('animation:', css + base_css)


if __name__ == '__main__':
    unittest.main()
