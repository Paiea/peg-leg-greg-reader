import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIO = ROOT / 'greg-again' / 'audio'
R2 = ROOT / 'r2'


class GregAgainChapter15AudioTest(unittest.TestCase):
    def test_chapter_15_is_durable_and_published(self):
        manifest = json.loads((AUDIO / 'manifest.json').read_text(encoding='utf-8'))
        by_id = {c['chapter_id']: c for c in manifest['chapters']}
        self.assertIn('ga-015', by_id)
        ch = by_id['ga-015']
        self.assertEqual(15, ch['number'])
        self.assertEqual('The Friend', ch['title'])
        self.assertEqual('audio-score-light', ch['audio_finish'])
        self.assertEqual(16, ch['take_count'])
        self.assertEqual(418.488, ch['duration_seconds'])
        self.assertEqual('assets/light/chapter-015.mp3', ch['audio_src'])

        light_audio = AUDIO / 'assets' / 'light' / 'chapter-015.mp3'
        self.assertTrue(light_audio.exists())
        self.assertGreater(light_audio.stat().st_size, 1_000_000)

        # Preserve the previous short-take generation as historical durability evidence.
        legacy_audio = AUDIO / 'assets' / 'chapter-015.mp3'
        self.assertTrue(legacy_audio.exists())
        self.assertGreater(legacy_audio.stat().st_size, 1_000_000)
        take_map = json.loads((AUDIO / 'takes' / '015-short.json').read_text(encoding='utf-8'))
        self.assertEqual('original_short_take_complete_preview', take_map['production_mode'])
        self.assertEqual(27, take_map['take_count'])
        self.assertEqual(27, len(take_map['takes']))
        self.assertTrue(all(t['status'] == 'artifact_captured' for t in take_map['takes']))
        for i in range(1, 28):
            take = AUDIO / 'assets' / 'chunks' / '015-short' / f'{i:02d}.mp3'
            self.assertTrue(take.exists())
            self.assertGreater(take.stat().st_size, 10_000)

        route = json.loads((R2 / 'data' / 'chapters' / 'ch015.json').read_text(encoding='utf-8'))
        self.assertEqual('The Friend', route['title'])
        self.assertEqual('published', route['audio']['status'])
        self.assertEqual('../greg-again/audio/assets/chapter-015.mp3', route['audio']['path'])

        registry = json.loads((R2 / 'data' / 'chapter-registry.json').read_text(encoding='utf-8'))
        reg = registry['chapters']['r2-ch015']
        self.assertEqual('The Friend', reg['title'])
        self.assertEqual('published', reg['pipeline']['audio'])


if __name__ == '__main__':
    unittest.main()
