import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIO_ROOT = ROOT / 'greg-again' / 'audio'
R2_ROOT = ROOT / 'r2'

class GregAgainChapter25AudioTest(unittest.TestCase):
    def test_chapter_25_is_durable_and_routed(self):
        manifest=json.loads((AUDIO_ROOT/'manifest.json').read_text())
        by_id={c['chapter_id']:c for c in manifest['chapters']}
        c=by_id['ga-025']
        self.assertEqual('The Hired Sword',c['title'])
        self.assertEqual('shared-greg-surface',c['lens'])
        self.assertEqual('processing-space',c['audio_finish'])
        self.assertEqual(38,c['take_count'])
        self.assertEqual(931.44,c['duration_seconds'])
        self.assertEqual('assets/chapter-025.mp3',c['audio_src'])

        final_audio=AUDIO_ROOT/'assets'/'chapter-025.mp3'
        self.assertTrue(final_audio.exists())
        self.assertGreater(final_audio.stat().st_size,1_000_000)

        m=json.loads((AUDIO_ROOT/'takes'/'025-short.json').read_text())
        self.assertEqual('ga-025',m['chapter_id'])
        self.assertEqual('The Hired Sword',m['title'])
        self.assertEqual('deep',m['voice'])
        self.assertEqual('verified_playable',m['status'])
        self.assertEqual(38,len(m['takes']))
        self.assertEqual(931.44,m['assembled_duration_seconds'])
        self.assertEqual('98a198d25553f57eb19fd1d0070928eb3336c0d6e71c16eb7ef4f7b25f5ded2d',m['assembled_sha256'])
        for t in m['takes']:
            self.assertEqual('artifact_captured_verified',t['status'])
            f=ROOT/t['durable_file']
            self.assertTrue(f.exists())
            self.assertGreater(f.stat().st_size,10_000)
            self.assertTrue(t['provider_context_id'])
            self.assertTrue(t['preview_url'].startswith('https://storage.googleapis.com/adm--audio-playback--7d--public/mcp-preview/'))
            self.assertEqual(64,len(t['sha256']))

        v=json.loads((AUDIO_ROOT/'verification'/'025-short.json').read_text())
        self.assertTrue(v['exact_source_coverage'])
        self.assertTrue(v['take_order_verified'])
        self.assertTrue(v['individual_mp3s_verified'])
        self.assertTrue(v['assembled_mp3_verified'])
        self.assertEqual(2.0,v['chapter_tail_silence_seconds_added'])

        route=json.loads((R2_ROOT/'data'/'chapters'/'ch025.json').read_text())
        self.assertEqual('The Hired Sword',route['title'])
        self.assertEqual('published',route['audio']['status'])
        self.assertEqual('../greg-again/audio/assets/chapter-025.mp3',route['audio']['path'])

        registry=json.loads((R2_ROOT/'data'/'chapter-registry.json').read_text())
        self.assertEqual('published',registry['chapters']['r2-ch025']['pipeline']['audio'])

if __name__ == '__main__': unittest.main()
