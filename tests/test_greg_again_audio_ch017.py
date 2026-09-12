import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIO = ROOT / 'greg-again' / 'audio'
R2 = ROOT / 'r2'

class GregAgainChapter17AudioTest(unittest.TestCase):
    def test_chapter_17_current_light_audio_is_durable_and_published(self):
        manifest = json.loads((AUDIO / 'manifest.json').read_text(encoding='utf-8'))
        by_id = {c['chapter_id']: c for c in manifest['chapters']}
        self.assertIn('ga-017', by_id)
        ch = by_id['ga-017']
        self.assertEqual(17, ch['number'])
        self.assertEqual('The Extra Hand', ch['title'])
        self.assertEqual('audio-score-light', ch['audio_finish'])
        self.assertEqual(35, ch['take_count'])
        self.assertEqual('assets/light/chapter-017.mp3', ch['audio_src'])

        audio = AUDIO / ch['audio_src']
        self.assertTrue(audio.exists())
        self.assertGreater(audio.stat().st_size, 1_000_000)

        take_map = json.loads((AUDIO / 'light' / 'takes' / '017' / 'short-takes.json').read_text(encoding='utf-8'))
        self.assertEqual('ga-017', take_map['chapter_id'])
        self.assertEqual('light', take_map['generation'])
        self.assertEqual('deep', take_map['voice'])
        self.assertEqual('durable_takes_verified_and_assembled', take_map['status'])
        self.assertEqual(35, take_map['take_count'])
        self.assertEqual(35, len(take_map['takes']))
        self.assertEqual(list(range(1, 36)), [t['order'] for t in take_map['takes']])
        self.assertEqual(35, len({t['context_id'] for t in take_map['takes']}))
        self.assertEqual(35, len({t['preview_url'] for t in take_map['takes']}))
        for take in take_map['takes']:
            durable = ROOT / take['durable_file']
            self.assertTrue(durable.exists())
            self.assertGreater(durable.stat().st_size, 10_000)
            self.assertEqual(64, len(take['audio_sha256']))

        route = json.loads((R2 / 'data' / 'chapters' / 'ch017.json').read_text(encoding='utf-8'))
        self.assertEqual('The Extra Hand', route['title'])
        self.assertEqual('published', route['audio']['status'])

        registry = json.loads((R2 / 'data' / 'chapter-registry.json').read_text(encoding='utf-8'))
        reg = registry['chapters']['r2-ch017']
        self.assertEqual('The Extra Hand', reg['title'])
        self.assertEqual('published', reg['pipeline']['audio'])

    def test_historical_legacy_map_is_not_reintroduced_on_current_branch(self):
        self.assertFalse((AUDIO / 'takes' / '017.json').exists())

if __name__ == '__main__':
    unittest.main()
