import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'generate_light.py'

RUNNING = '''# PEG-LEG GREG — RUNNING MANUSCRIPT\n\n# CHAPTER 220\n\n## THE LANDLORD\n\nFirst paragraph.\n\n# CHAPTER 221\n\n## THE PARTICIPANT\n\nRunning manuscript wins here.\n'''
RECOVERED = '''# CHAPTER 156\n\n## THE SAMPLE\n\nRecovered prose.\n'''


class LightCheckpointPublishTests(unittest.TestCase):
    def test_current_extends_with_checkpoint_files_without_overriding_running_manuscript(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            manuscript = root / 'state/manuscript'
            manuscript.mkdir(parents=True)
            (root / 'chapters').mkdir()
            (manuscript / 'Peg_Leg_Greg_Running_Manuscript.md').write_text(RUNNING, encoding='utf-8')
            (manuscript / 'Peg_Leg_Greg_Recovered_Ch156-219_EXACT.md').write_text(RECOVERED, encoding='utf-8')
            (manuscript / 'Peg_Leg_Greg_Chapter_221_EXACT_WIP.md').write_text(
                '# CHAPTER 221\n\n## THE WRONG OVERRIDE\n\nCheckpoint must not replace running prose.\n',
                encoding='utf-8',
            )
            (manuscript / 'Peg_Leg_Greg_Chapter_222_EXACT_WIP.md').write_text(
                '# CHAPTER 222\n\n## THE CHECKPOINT\n\nCheckpoint extension prose.\n',
                encoding='utf-8',
            )

            result = subprocess.run(
                [sys.executable, str(SCRIPT), 'current'],
                cwd=root,
                text=True,
                capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)

            p221 = (root / 'light/221.html').read_text(encoding='utf-8')
            p222 = (root / 'light/222.html').read_text(encoding='utf-8')
            manifest = json.loads((root / 'light/manifest.json').read_text(encoding='utf-8'))

            self.assertIn('Running manuscript wins here.', p221)
            self.assertNotIn('Checkpoint must not replace running prose.', p221)
            self.assertIn('Checkpoint extension prose.', p222)
            self.assertEqual(manifest['latest'], 222)
            self.assertEqual(manifest['chapters'][-1]['source'], 'checkpoint')


if __name__ == '__main__':
    unittest.main()
