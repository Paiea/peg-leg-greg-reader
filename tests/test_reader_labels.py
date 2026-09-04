import unittest
from pathlib import Path


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
        self.assertNotIn('Light Edition', light)
        self.assertNotIn('LIGHT EDITION', light)
        self.assertNotIn('>LIGHT<', light)


if __name__ == '__main__':
    unittest.main()
