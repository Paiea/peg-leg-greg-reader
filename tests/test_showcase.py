import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))

from showcase import build_showcase_map, load_showcase_manifest


class ShowcaseTests(unittest.TestCase):
    def test_default_visible_is_identity(self):
        mapping = build_showcase_map([1, 2, 3, 4], {
            'version': 1,
            'mode': 'whole_chapter_only',
            'default': 'visible',
            'chapters': {},
        })
        self.assertEqual(mapping.visible_canon, (1, 2, 3, 4))
        self.assertEqual(mapping.showcase_number(4), 4)

    def test_hidden_chapter_is_skipped_and_numbers_remain_contiguous(self):
        mapping = build_showcase_map([1, 2, 3, 4], {
            'version': 1,
            'mode': 'whole_chapter_only',
            'default': 'visible',
            'chapters': {'3': {'showcase': False, 'reason': 'pacing'}},
        })
        self.assertEqual(mapping.visible_canon, (1, 2, 4))
        self.assertIsNone(mapping.showcase_number(3))
        self.assertEqual(mapping.showcase_number(4), 3)
        self.assertEqual(mapping.next_visible(2), 4)
        self.assertEqual(mapping.previous_visible(4), 2)

    def test_invalid_reason_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'unsupported reason'):
            build_showcase_map([1], {
                'version': 1,
                'mode': 'whole_chapter_only',
                'default': 'visible',
                'chapters': {'1': {'showcase': False, 'reason': 'boring'}},
            })

    def test_scene_level_fields_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'whole-chapter only'):
            build_showcase_map([1], {
                'version': 1,
                'mode': 'whole_chapter_only',
                'default': 'visible',
                'chapters': {'1': {'showcase': False, 'reason': 'pacing', 'paragraphs': [1, 2]}},
            })

    def test_unknown_canonical_chapter_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'unknown canonical chapter 9'):
            build_showcase_map([1, 2], {
                'version': 1,
                'mode': 'whole_chapter_only',
                'default': 'visible',
                'chapters': {'9': {'showcase': False, 'reason': 'pacing'}},
            })

    def test_loader_rejects_bad_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'showcase.json'
            path.write_text(json.dumps({
                'version': 1,
                'mode': 'scene_level',
                'default': 'visible',
                'chapters': {},
            }), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'mode'):
                load_showcase_manifest(path)


if __name__ == '__main__':
    unittest.main()
