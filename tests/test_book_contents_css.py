import unittest
from pathlib import Path


class BookContentsCssTests(unittest.TestCase):
    def test_high_res_role_card_scale_and_mobile_stack(self):
        root = Path(__file__).parents[1] / 'assets'
        css = (root / 'book-contents.css').read_text(encoding='utf-8')
        base_css = (root / 'book-contents-base.css').read_text(encoding='utf-8')
        self.assertIn('grid-template-columns: minmax(380px, 420px) minmax(0, 1fr)', css)
        self.assertIn('"plate heading"', css)
        self.assertIn('"plate acts"', css)
        self.assertIn('max-width: 420px', css)
        self.assertIn('width: min(85vw, 340px)', css)
        self.assertIn('grid-template-areas:', css)
        self.assertIn('"heading"', css)
        self.assertIn('"plate"', css)
        self.assertIn('"acts"', css)
        self.assertIn('.reader-book-card-image', css)
        self.assertIn('.toc a.reader-book-card-link', css)
        self.assertIn('grid-template-columns: none', css)
        self.assertIn('padding: 0', css)
        self.assertIn('border-bottom: 0', css)
        self.assertNotIn('grid-template-columns: minmax(240px, 42vw) minmax(0, 1fr)', css)
        self.assertNotIn('width: min(42vw, 280px)', css)
        self.assertNotIn('reader-book-card-art', css + base_css)
        self.assertNotIn('data:image/webp;base64,', css + base_css)
        self.assertNotIn('background-size: 300% 100%', css + base_css)
        self.assertNotIn('animation:', css + base_css)
        self.assertNotIn('transition:', css)
        self.assertNotIn('transform:', css)


if __name__ == '__main__':
    unittest.main()
