import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))

from generate_light import Chapter, render_chapter, render_index, render_latest


class ReaderLabelTests(unittest.TestCase):
    def test_public_reader_labels_use_one_consistent_vocabulary(self):
        index = Path('index.html').read_text(encoding='utf-8')
        light = Path('light.html').read_text(encoding='utf-8')

        self.assertIn('>Text Reader<', index)
        self.assertIn('>Chapters<', index)
        self.assertNotIn('>Read Light<', index)
        self.assertNotIn('>Chapter List<', index)

        self.assertIn('<title>Text Reader — Peg-Leg Greg</title>', light)
        self.assertIn('>ILLUSTRATED READER<', light)
        self.assertIn('>TEXT READER<', light)
        self.assertIn('TEXT READER</div>', light)
        self.assertIn('Text-only reading with no chapter illustrations.', light)
        self.assertIn('index.html#books', light)
        self.assertNotIn('index.html#chapters', light)
        self.assertNotIn('Light Edition', light)
        self.assertNotIn('LIGHT EDITION', light)
        self.assertNotIn('>LIGHT<', light)

    def test_generated_reader_surfaces_keep_the_same_vocabulary(self):
        chapter = Chapter(220, 'THE TEST', '<p>Body</p>', 'test')
        chapters = {220: chapter}

        rendered_index = render_index(chapters, {220})
        rendered_chapter = render_chapter(chapter, [220], {220})
        rendered_latest = render_latest(chapter, {220})

        for rendered in (rendered_index, rendered_chapter, rendered_latest):
            self.assertIn('TEXT READER', rendered.upper())
            self.assertNotIn('LIGHT EDITION', rendered.upper())
            self.assertNotIn('#chapters', rendered)

        self.assertIn('Illustrated Reader', rendered_index)
        self.assertIn('Text-only Peg-Leg Greg', rendered_index)
        self.assertIn('TEXT READER · CHAPTER 220', rendered_chapter)
        self.assertIn('Text-only reading · no chapter illustrations', rendered_chapter)
        self.assertIn('Browse the Text Reader', rendered_latest)

    def test_reader_label_normalizer_is_retired(self):
        workflow = Path('.github/workflows/light-edition.yml').read_text(encoding='utf-8')
        self.assertFalse(Path('scripts/normalize_reader_labels.py').exists())
        self.assertNotIn('normalize_reader_labels.py', workflow)
        self.assertNotIn('Normalize public reader labels', workflow)
        self.assertIn("! grep -R '#chapters' light/*.html light.html latest.html index.html", workflow)


if __name__ == '__main__':
    unittest.main()
