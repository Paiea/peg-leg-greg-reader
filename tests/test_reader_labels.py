import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))

from generate_light import Chapter, render_chapter, render_index, render_latest
from normalize_reader_labels import normalize_text


class ReaderLabelTests(unittest.TestCase):
    def test_public_reader_labels_use_one_consistent_vocabulary(self):
        index = normalize_text(Path('index.html').read_text(encoding='utf-8'))
        light = normalize_text(Path('light.html').read_text(encoding='utf-8'))

        self.assertIn('>Text Reader<', index)
        self.assertIn('>Chapters<', index)
        self.assertNotIn('>Read Light<', index)
        self.assertNotIn('>Chapter List<', index)

        self.assertIn('<title>Text Reader — Peg-Leg Greg</title>', light)
        self.assertIn('>ILLUSTRATED READER<', light)
        self.assertIn('>TEXT READER<', light)
        self.assertIn('TEXT READER</div>', light)
        self.assertIn('Text-only reading with no chapter illustrations.', light)
        self.assertNotIn('Light Edition', light)
        self.assertNotIn('LIGHT EDITION', light)
        self.assertNotIn('>LIGHT<', light)

    def test_generated_reader_surfaces_keep_the_same_vocabulary(self):
        chapter = Chapter(220, 'THE TEST', '<p>Body</p>', 'test')
        chapters = {220: chapter}

        rendered_index = normalize_text(render_index(chapters, {220}))
        rendered_chapter = normalize_text(render_chapter(chapter, [220], {220}))
        rendered_latest = normalize_text(render_latest(chapter, {220}))

        for rendered in (rendered_index, rendered_chapter, rendered_latest):
            self.assertIn('TEXT READER', rendered.upper())
            self.assertNotIn('LIGHT EDITION', rendered.upper())

        self.assertIn('Illustrated Reader', rendered_index)
        self.assertIn('Text-only Peg-Leg Greg', rendered_index)
        self.assertIn('TEXT READER · CHAPTER 220', rendered_chapter)
        self.assertIn('Text-only reading · no chapter illustrations', rendered_chapter)
        self.assertIn('Browse the Text Reader', rendered_latest)


if __name__ == '__main__':
    unittest.main()
