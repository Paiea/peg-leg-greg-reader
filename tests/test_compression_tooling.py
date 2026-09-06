import json
import tempfile
import unittest
import zipfile
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))

from chapter_dependency_scan import scan_dependencies
from chapter_registry import build_registry
from compression_migration_preview import build_preview
from compression_readiness import build_readiness_report
from manuscript_authority import discover_manuscript_chapters


def write_chapter_html(path: Path, number: int, title: str, *, art: str | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image = f'<img src="{art}">' if art else ''
    path.write_text(
        f'<html><head><title>Chapter {number}: {title} — Peg-Leg Greg</title></head>'
        f'<body><div class="number">CHAPTER {number}</div><h1>{title}</h1>{image}</body></html>',
        encoding='utf-8',
    )


def write_minimal_docx(path: Path, paragraphs: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    body = ''.join(
        f'<w:p><w:r><w:t>{text}</w:t></w:r></w:p>'
        for text in paragraphs
    )
    document = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        f'<w:body>{body}</w:body></w:document>'
    )
    with zipfile.ZipFile(path, 'w') as archive:
        archive.writestr('word/document.xml', document)


class CompressionToolingTests(unittest.TestCase):
    def test_full_manuscript_discovery_reconciles_docx_running_checkpoint_and_reader_fallbacks(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            manuscript = root / 'state/manuscript'
            manuscript.mkdir(parents=True)
            write_minimal_docx(
                manuscript / 'Peg_Leg_Greg_authoritative_ch82_final_name_map.docx',
                ['CHAPTER ONE', 'THE BOY', 'CHAPTER TWO', 'THE BORROWER'],
            )
            write_chapter_html(root / 'chapters/003.html', 3, 'THE INVESTOR')
            write_chapter_html(root / 'light/004.html', 4, 'THE EXPERT')
            (manuscript / 'Peg_Leg_Greg_Running_Manuscript.md').write_text(
                '# CHAPTER 5 — THE WARRIOR\n\nRunning prose.\n', encoding='utf-8'
            )
            (manuscript / 'Peg_Leg_Greg_Chapter_6_EXACT_WIP.md').write_text(
                '# Chapter 6 — THE LABORER\n\nCheckpoint prose.\n', encoding='utf-8'
            )
            (root / 'state/MANUSCRIPT_CHAPTER_INDEX.md').write_text(
                '# index\n1. **THE BOY**\n2. **THE BORROWER**\n', encoding='utf-8'
            )

            report = discover_manuscript_chapters(root)
            self.assertEqual(report['endpoint'], 6)
            self.assertEqual(report['gaps'], [])
            self.assertEqual(report['chapter_index_endpoint'], 2)
            self.assertEqual(report['chapter_index_stale_by'], 4)
            by_number = {row['chapter_number']: row for row in report['chapters']}
            self.assertEqual(by_number[1]['source_kind'], 'authoritative_docx')
            self.assertEqual(by_number[3]['source_kind'], 'illustrated_reader_fallback')
            self.assertEqual(by_number[4]['source_kind'], 'light_reader_fallback')
            self.assertEqual(by_number[5]['source_kind'], 'running_manuscript')
            self.assertEqual(by_number[6]['source_kind'], 'exact_checkpoint')

    def test_unified_registry_includes_manuscript_only_reader_and_art_state(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            manuscript = root / 'state/manuscript'
            manuscript.mkdir(parents=True)
            (manuscript / 'Peg_Leg_Greg_Running_Manuscript.md').write_text(
                '# CHAPTER 1 — THE BOY\n\nBody.\n\n# CHAPTER 2 — THE BORROWER\n\nBody.\n',
                encoding='utf-8',
            )
            write_chapter_html(
                root / 'chapters/001.html', 1, 'THE BOY',
                art='../visual/chapter_art/001/a.png',
            )
            art = root / 'visual/chapter_art/001/a.png'
            art.parent.mkdir(parents=True)
            art.write_bytes(b'fake')

            registry = build_registry(root)
            first, second = registry['chapters']
            self.assertEqual(first['chapter_id'], 'plg-ch-000001')
            self.assertEqual(first['current_title'], 'THE BOY')
            self.assertEqual(first['manuscript_source_kind'], 'running_manuscript')
            self.assertEqual(first['reader_pages'], ['chapters/001.html'])
            self.assertEqual(first['illustration_refs'], ['visual/chapter_art/001/a.png'])
            self.assertEqual(second['reader_pages'], [])
            self.assertEqual(registry['diagnostics']['manuscript_only_chapters'], [2])
            self.assertEqual(registry['diagnostics']['reader_only_chapters'], [])

    def test_registry_reports_gaps_stale_index_and_reader_mismatch(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            manuscript = root / 'state/manuscript'
            manuscript.mkdir(parents=True)
            (manuscript / 'Peg_Leg_Greg_Running_Manuscript.md').write_text(
                '# CHAPTER 1 — A\n\nBody.\n\n# CHAPTER 3 — C\n\nBody.\n', encoding='utf-8'
            )
            (root / 'state/MANUSCRIPT_CHAPTER_INDEX.md').write_text('1. **A**\n', encoding='utf-8')
            write_chapter_html(root / 'chapters/001.html', 1, 'A')
            write_chapter_html(root / 'chapters/004.html', 4, 'READER ONLY')

            registry = build_registry(root)
            diagnostics = registry['diagnostics']
            self.assertEqual(diagnostics['manuscript_gaps'], [2])
            self.assertEqual(diagnostics['chapter_index_stale_by'], 2)
            self.assertEqual(diagnostics['reader_only_chapters'], [4])
            self.assertEqual(diagnostics['manuscript_only_chapters'], [3])

    def test_dependency_scan_categorizes_whole_book_number_bindings(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            files = {
                'index.html': 'href="chapters/187.html"',
                'visual/notes.json': 'visual/chapter_art/187/pic.png',
                'state/example.md': 'See Chapter 187.',
                'prompts/edit.md': 'Review Chapter 187.',
                'scripts/example.py': 'url = "light/187.html"',
                'publishing/manifest.json': '{"chapter_number": 187}',
            }
            for relative, text in files.items():
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding='utf-8')

            report = scan_dependencies(root)
            refs = report['by_chapter']['187']
            self.assertGreaterEqual(len(refs), 6)
            self.assertIn('reader', report['counts_by_file_category'])
            self.assertIn('art', report['counts_by_file_category'])
            self.assertIn('state', report['counts_by_file_category'])
            self.assertIn('prompt', report['counts_by_file_category'])
            self.assertIn('script', report['counts_by_file_category'])
            self.assertIn('metadata', report['counts_by_file_category'])
            self.assertIn('reader_slug', report['counts_by_kind'])
            self.assertIn('chapter_art_path', report['counts_by_kind'])
            self.assertIn('chapter_field', report['counts_by_kind'])

    def test_readiness_separates_safe_migration_and_blockers(self):
        registry = {
            'chapters': [
                {'chapter_id': 'plg-ch-000001', 'current_display_number': 1},
                {'chapter_id': 'plg-ch-000003', 'current_display_number': 3},
            ],
            'diagnostics': {
                'manuscript_gaps': [2],
                'authority_conflicts': [],
                'chapter_index_stale_by': 2,
                'reader_only_chapters': [],
                'manuscript_only_chapters': [3],
            },
        }
        dependencies = {
            'reference_count': 2,
            'counts_by_kind': {'reader_slug': 1, 'chapter_art_path': 1},
            'counts_by_file_category': {'reader': 1, 'art': 1},
        }
        report = build_readiness_report(registry, dependencies)
        blocker_codes = {item['code'] for item in report['blocked_before_structural_editing']}
        migration_codes = {item['code'] for item in report['needs_migration']}
        safe_codes = {item['code'] for item in report['safe_now']}
        self.assertIn('manuscript_gaps', blocker_codes)
        self.assertIn('numeric_dependencies', migration_codes)
        self.assertIn('stale_chapter_index', migration_codes)
        self.assertIn('read_only_audit', safe_codes)
        self.assertEqual(report['overall_status'], 'BLOCKED')

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
