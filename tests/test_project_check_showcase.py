import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))

from project_check import showcase_check


class ShowcaseProjectCheckTests(unittest.TestCase):
    def test_valid_manifest_reports_visible_and_hidden_counts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'publishing').mkdir()
            (root / 'state').mkdir()
            (root / 'state' / 'MANUSCRIPT_CHAPTER_INDEX.md').write_text(
                '1. **ONE**\n2. **TWO**\n3. **THREE**\n', encoding='utf-8'
            )
            (root / 'publishing' / 'showcase_chapters.json').write_text(json.dumps({
                'version': 1,
                'mode': 'whole_chapter_only',
                'default': 'visible',
                'chapters': {'2': {'showcase': False, 'reason': 'pacing'}},
            }), encoding='utf-8')
            payload, passed = showcase_check(root)
            self.assertTrue(passed)
            self.assertEqual(payload['canonical_chapters'], 3)
            self.assertEqual(payload['visible_chapters'], 2)
            self.assertEqual(payload['hidden_chapters'], 1)

    def test_unknown_manifest_chapter_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'publishing').mkdir()
            (root / 'state').mkdir()
            (root / 'state' / 'MANUSCRIPT_CHAPTER_INDEX.md').write_text(
                '1. **ONE**\n', encoding='utf-8'
            )
            (root / 'publishing' / 'showcase_chapters.json').write_text(json.dumps({
                'version': 1,
                'mode': 'whole_chapter_only',
                'default': 'visible',
                'chapters': {'9': {'showcase': False, 'reason': 'pacing'}},
            }), encoding='utf-8')
            payload, passed = showcase_check(root)
            self.assertFalse(passed)
            self.assertIn('unknown canonical chapter 9', payload['error'])


if __name__ == '__main__':
    unittest.main()
