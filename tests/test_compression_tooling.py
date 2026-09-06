import json
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))

from chapter_registry import build_registry
from chapter_dependency_scan import scan_dependencies
from compression_migration_preview import build_preview


class CompressionToolingTests(unittest.TestCase):
    def test_registry_assigns_stable_ids_and_art_bindings(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / 'chapters').mkdir()
            (root / 'publishing').mkdir()
            (root / 'chapters/001.html').write_text(
                '<div class="number">CHAPTER 1</div><h1>THE BOY</h1>', encoding='utf-8'
            )
            (root / 'chapters/002.html').write_text(
                '<div class="number">CHAPTER 2</div><h1>THE BORROWER</h1>', encoding='utf-8'
            )
            (root / 'publishing/chapter_art_coverage.json').write_text(json.dumps({
                'chapters': {
                    '001': {'assets': ['visual/chapter_art/001/a.png']},
                    '002': {'assets': []},
                }
            }), encoding='utf-8')
            registry = build_registry(root)
            self.assertEqual(registry['chapters'][0]['chapter_id'], 'plg-ch-000001')
            self.assertEqual(registry['chapters'][0]['current_title'], 'THE BOY')
            self.assertEqual(registry['chapters'][0]['illustration_refs'], ['visual/chapter_art/001/a.png'])
            self.assertEqual(registry['chapters'][1]['public_slug'], 'chapters/002.html')

    def test_dependency_scan_finds_reader_art_and_textual_chapter_references(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / 'state').mkdir()
            (root / 'state/example.md').write_text(
                'See Chapter 17 and chapters/017.html and visual/chapter_art/017/pic.png.',
                encoding='utf-8',
            )
            report = scan_dependencies(root)
            refs = report['by_chapter']['17']
            kinds = {item['kind'] for item in refs}
            self.assertEqual(kinds, {'chapter_text', 'reader_slug', 'chapter_art_path'})

    def test_preview_preserves_stable_identity_and_creates_legacy_aliases(self):
        registry = {
            'chapters': [
                {'chapter_id': 'plg-ch-000001', 'current_display_number': 1, 'current_title': 'A', 'public_slug': 'chapters/001.html', 'illustration_refs': []},
                {'chapter_id': 'plg-ch-000002', 'current_display_number': 2, 'current_title': 'B', 'public_slug': 'chapters/002.html', 'illustration_refs': ['x.png']},
                {'chapter_id': 'plg-ch-000003', 'current_display_number': 3, 'current_title': 'C', 'public_slug': 'chapters/003.html', 'illustration_refs': []},
            ]
        }
        mapping = {
            'plg-ch-000001': {'status': 'active', 'display_number': 1},
            'plg-ch-000002': {'status': 'merged', 'merged_into': 'plg-ch-000001'},
            'plg-ch-000003': {'status': 'active', 'display_number': 2},
        }
        preview = build_preview(registry, mapping)
        self.assertEqual(preview['active_sequence'], ['plg-ch-000001', 'plg-ch-000003'])
        self.assertEqual(preview['aliases']['chapters/002.html'], 'chapters/001.html')
        self.assertEqual(preview['aliases']['chapters/003.html'], 'chapters/002.html')
        self.assertEqual(preview['art_migrations'][0]['asset_path'], 'x.png')
        self.assertEqual(preview['art_migrations'][0]['destination_chapter_id'], 'plg-ch-000001')

    def test_preview_rejects_duplicate_active_numbers(self):
        registry = {'chapters': [
            {'chapter_id': 'a', 'current_display_number': 1, 'current_title': 'A', 'public_slug': 'chapters/001.html', 'illustration_refs': []},
            {'chapter_id': 'b', 'current_display_number': 2, 'current_title': 'B', 'public_slug': 'chapters/002.html', 'illustration_refs': []},
        ]}
        with self.assertRaises(ValueError):
            build_preview(registry, {
                'a': {'status': 'active', 'display_number': 1},
                'b': {'status': 'active', 'display_number': 1},
            })


if __name__ == '__main__':
    unittest.main()
