import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIO = ROOT / 'greg-again' / 'audio'
R2 = ROOT / 'r2'

class GregAgainChapter17AudioTest(unittest.TestCase):
    def test_chapter_17_is_durable_exact_and_published(self):
        manifest = json.loads((AUDIO / 'manifest.json').read_text(encoding='utf-8'))
        by_id = {c['chapter_id']: c for c in manifest['chapters']}
        self.assertIn('ga-017', by_id)
        ch = by_id['ga-017']
        self.assertEqual(17, ch['number'])
        self.assertEqual('The Extra Hand', ch['title'])
        self.assertEqual(42, ch['take_count'])
        self.assertEqual('assets/chapter-017.mp3', ch['audio_src'])

        audio = AUDIO / 'assets' / 'chapter-017.mp3'
        self.assertTrue(audio.exists())
        self.assertGreater(audio.stat().st_size, 1_000_000)

        take_map = json.loads((AUDIO / 'takes' / '017-short.json').read_text(encoding='utf-8'))
        self.assertEqual('ga-017', take_map['chapter_id'])
        self.assertEqual('deep', take_map['voice'])
        self.assertEqual('original_short_take_complete_preview', take_map['production_mode'])
        self.assertEqual('direct_preview_captured', take_map['artifact_boundary'])
        self.assertEqual('verified_playable', take_map['status'])
        self.assertEqual(42, take_map['take_count'])
        self.assertEqual(42, len(take_map['takes']))
        self.assertTrue(take_map['verification']['exact_source_coverage'])
        self.assertEqual(list(range(1,43)), take_map['verification']['take_order'])
        self.assertTrue(all(t['status'] == 'artifact_captured' for t in take_map['takes']))
        self.assertEqual(42, len({t['provider_context_id'] for t in take_map['takes']}))
        self.assertEqual(42, len({t['preview_url'] for t in take_map['takes']}))
        self.assertTrue(all('/mcp-preview/' in t['preview_url'] and t['preview_url'].endswith('.mp3') for t in take_map['takes']))
        for i in range(1, 43):
            take = AUDIO / 'assets' / 'chunks' / '017-short' / f'{i:02d}.mp3'
            self.assertTrue(take.exists())
            self.assertGreater(take.stat().st_size, 10_000)

        route = json.loads((R2 / 'data' / 'chapters' / 'ch017.json').read_text(encoding='utf-8'))
        self.assertEqual('The Extra Hand', route['title'])
        self.assertEqual('published', route['audio']['status'])
        self.assertEqual('../greg-again/audio/assets/chapter-017.mp3', route['audio']['path'])

        registry = json.loads((R2 / 'data' / 'chapter-registry.json').read_text(encoding='utf-8'))
        reg = registry['chapters']['r2-ch017']
        self.assertEqual('The Extra Hand', reg['title'])
        self.assertEqual('published', reg['pipeline']['audio'])

    def test_historical_legacy_map_is_not_reintroduced_on_current_branch(self):
        self.assertFalse((AUDIO / 'takes' / '017.json').exists())

if __name__ == '__main__':
    unittest.main()
