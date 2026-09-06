import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATE = ROOT / 'scripts' / 'generate_light.py'
VERIFY = ROOT / 'scripts' / 'verify_light.py'

RUNNING = '''# PEG-LEG GREG — RUNNING MANUSCRIPT\n\n# CHAPTER 220\n\n## THE FIRST\n\nFirst.\n\n# CHAPTER 221\n\n## THE HIDDEN\n\nHidden.\n\n# CHAPTER 222\n\n## THE THIRD\n\nThird.\n'''


class VerifyLightShowcaseTests(unittest.TestCase):
    def test_hidden_canonical_chapter_is_not_required_and_navigation_skips_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'state/manuscript').mkdir(parents=True)
            (root / 'publishing').mkdir()
            (root / 'chapters').mkdir()
            (root / 'state/manuscript/Peg_Leg_Greg_Running_Manuscript.md').write_text(RUNNING, encoding='utf-8')
            (root / 'publishing/showcase_chapters.json').write_text(json.dumps({
                'version': 1,
                'mode': 'whole_chapter_only',
                'default': 'visible',
                'chapters': {'221': {'showcase': False, 'reason': 'pacing'}},
            }), encoding='utf-8')

            generated = subprocess.run(
                [sys.executable, str(GENERATE), 'current'], cwd=root, text=True, capture_output=True
            )
            self.assertEqual(generated.returncode, 0, generated.stderr)
            self.assertFalse((root / 'light/221.html').exists())
            p220 = (root / 'light/220.html').read_text(encoding='utf-8')
            self.assertIn('href="222.html">Chapter 2 →</a>', p220)

            verified = subprocess.run(
                [sys.executable, str(VERIFY), 'current'], cwd=root, text=True, capture_output=True
            )
            self.assertEqual(verified.returncode, 0, verified.stderr)


if __name__ == '__main__':
    unittest.main()
