import json
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
R2 = ROOT / 'r2'


class R2SiteTests(unittest.TestCase):
    def test_project_manifest_names_run_two_and_preserves_run_one(self):
        project = json.loads((R2 / 'data/project.json').read_text(encoding='utf-8'))
        self.assertEqual(project['project_id'], 'r2')
        self.assertEqual(project['title'], 'R2')
        self.assertIn('two lives', project['tagline'].lower())
        self.assertEqual(project['run1_href'], '../index.html')
        self.assertEqual(project['chapters'], ['r2-ch001'])

    def test_chapter_one_reuses_existing_audio_without_claiming_missing_prose(self):
        chapter = json.loads((R2 / 'data/chapters/ch001.json').read_text(encoding='utf-8'))
        self.assertEqual(chapter['chapter_id'], 'r2-ch001')
        self.assertEqual(chapter['title'], 'The Boy')
        self.assertEqual(chapter['audio']['status'], 'published')
        self.assertEqual(chapter['audio']['path'], '../../greg-again/audio/assets/chapter-001.mp3')
        self.assertEqual(chapter['written']['status'], 'unavailable')
        self.assertEqual(chapter['images'], [])


if __name__ == '__main__':
    unittest.main()
