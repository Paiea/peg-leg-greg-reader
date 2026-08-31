import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'generate_light.py'

RUNNING = '''# PEG-LEG GREG — RUNNING MANUSCRIPT\n\n# CHAPTER 220\n\n## THE LANDLORD\n\nFirst paragraph.\n\nSecond paragraph.\n\n# CHAPTER 221\n\n## THE PARTICIPANT\n\nNext chapter.\n'''
RECOVERED = '''# CHAPTER 156\n\n## THE SAMPLE\n\nRecovered prose.\n'''
PUBLISHED = '''<!doctype html><html><body><header>ignore</header><h1>THE COOK</h1><article class="prose"><p>Published prose.</p><figure><img src="art.png"></figure><p>More prose.</p></article></body></html>'''


def run(*args, cwd):
    return subprocess.run([sys.executable, str(SCRIPT), *args], cwd=cwd, text=True, capture_output=True)


def seed(root):
    (root / 'state/manuscript').mkdir(parents=True)
    (root / 'chapters').mkdir()
    (root / 'state/manuscript/Peg_Leg_Greg_Running_Manuscript.md').write_text(RUNNING, encoding='utf-8')
    (root / 'state/manuscript/Peg_Leg_Greg_Recovered_Ch156-219_EXACT.md').write_text(RECOVERED, encoding='utf-8')
    (root / 'chapters/100.html').write_text(PUBLISHED, encoding='utf-8')


class GenerateLightTests(unittest.TestCase):
    def with_repo(self):
        td = tempfile.TemporaryDirectory()
        root = Path(td.name)
        seed(root)
        self.addCleanup(td.cleanup)
        return root

    def test_current_generates_static_pages_manifest_and_latest(self):
        root = self.with_repo()
        result = run('current', cwd=root)
        self.assertEqual(result.returncode, 0, result.stderr)
        p220 = (root / 'light/220.html').read_text(encoding='utf-8')
        p221 = (root / 'light/221.html').read_text(encoding='utf-8')
        manifest = json.loads((root / 'light/manifest.json').read_text(encoding='utf-8'))
        latest = (root / 'latest.html').read_text(encoding='utf-8')
        self.assertIn('First paragraph.', p220)
        self.assertIn('Second paragraph.', p220)
        self.assertNotIn('<img', p220)
        self.assertIn('THE LANDLORD', p220)
        self.assertIn('href="221.html"', p220)
        self.assertIn('href="220.html"', p221)
        self.assertEqual(manifest['latest'], 221)
        self.assertEqual([c['number'] for c in manifest['chapters']], [220, 221])
        self.assertIn('light/221.html', latest)

    def test_reader_facing_copy_does_not_expose_internal_source_language(self):
        root = self.with_repo()
        result = run('current', cwd=root)
        self.assertEqual(result.returncode, 0, result.stderr)
        page = (root / 'light/220.html').read_text(encoding='utf-8').lower()
        index = (root / 'light/index.html').read_text(encoding='utf-8').lower()
        latest = (root / 'latest.html').read_text(encoding='utf-8').lower()
        self.assertNotIn('exact manuscript prose', page)
        self.assertNotIn('compat', index)
        self.assertNotIn('materialized in github', latest)

    def test_recovered_range_uses_recovered_authority(self):
        root = self.with_repo()
        result = run('156-156', cwd=root)
        self.assertEqual(result.returncode, 0, result.stderr)
        page = (root / 'light/156.html').read_text(encoding='utf-8')
        self.assertIn('Recovered prose.', page)
        self.assertIn('THE SAMPLE', page)

    def test_duplicate_chapter_heading_fails_instead_of_guessing(self):
        root = self.with_repo()
        duplicate = RUNNING + "\n# CHAPTER 221\n\n## THE DUPLICATE\n\nWrong.\n"
        (root / 'state/manuscript/Peg_Leg_Greg_Running_Manuscript.md').write_text(duplicate, encoding='utf-8')
        result = run('current', cwd=root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('duplicate chapter 221', result.stderr.lower())

    def test_published_range_strips_illustrations(self):
        root = self.with_repo()
        result = run('100-100', cwd=root)
        self.assertEqual(result.returncode, 0, result.stderr)
        page = (root / 'light/100.html').read_text(encoding='utf-8')
        self.assertIn('Published prose.', page)
        self.assertIn('More prose.', page)
        self.assertNotIn('<img', page)
        self.assertNotIn('art.png', page)


if __name__ == '__main__':
    unittest.main()
