import unittest
from pathlib import Path


class BookContentsCssTests(unittest.TestCase):
    def test_role_card_rail_layout(self):
        root = Path(__file__).parents[1] / 'assets'
        css = (root / 'book-contents.css').read_text(encoding='utf-8')
        base_css = (root / 'book-contents-base.css').read_text(encoding='utf-8')
        self.assertIn('grid-template-columns: minmax(340px, 400px) minmax(0, 1fr)', css)
        self.assertIn('max-width: 400px', css)
        self.assertIn('@media (max-width: 820px)', css)
        self.assertIn('grid-template-columns:1fr', css)
        self.assertIn('grid-template-areas:"plate" "acts"', css)
        self.assertIn('width:min(85vw,340px)', css)
        self.assertIn('max-width:340px', css)
        self.assertIn('.reader-book-card-image', css)
        self.assertIn('.toc a.reader-book-card-link', css)
        self.assertIn('grid-template-columns:none', css)
        self.assertIn('padding:0', css)
        self.assertIn('border-bottom:0', css)
        self.assertNotIn('reader-book-card-art', css + base_css)
        self.assertNotIn('data:image/webp;base64,', css + base_css)
        self.assertNotIn('background-size: 300% 100%', css + base_css)
        self.assertNotIn('animation:', css + base_css)
        self.assertNotIn('transition:', css)
        self.assertNotIn('transform:', css)


if __name__ == '__main__':
    unittest.main()
