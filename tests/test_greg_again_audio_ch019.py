import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestGregAgainAudioChapter19(unittest.TestCase):
    def test_chapter_19_publication_contract(self):
        takes = json.loads((ROOT / 'greg-again/audio/takes/019.json').read_text(encoding='utf-8'))
        self.assertEqual(takes['take_count'], 36)
        self.assertEqual([t['take'] for t in takes['takes']], list(range(1, 37)))
        self.assertTrue(all(t['status'] == 'artifact_captured' for t in takes['takes']))
        self.assertTrue(all(t['provider_context_id'] for t in takes['takes']))
        self.assertTrue(all(t['provider_preview_url'] for t in takes['takes']))
        self.assertTrue(all(t['durable_audio'] for t in takes['takes']))

        source = (ROOT / 'r2/assets/written/ch019.md').read_text(encoding='utf-8')
        prose = source.split('\n---\n', 1)[1].strip().replace('**', '')
        joined = '\n\n'.join(t['transcript'] for t in takes['takes'])
        self.assertEqual(joined, prose)

        manifest = json.loads((ROOT / 'greg-again/audio/manifest.json').read_text(encoding='utf-8'))
        entry = next(ch for ch in manifest['chapters'] if ch['number'] == 19)
        self.assertEqual(entry['title'], 'The Maintainer')
        self.assertEqual(entry['take_count'], 36)
        self.assertEqual(entry['duration_seconds'], 867.168)
        self.assertEqual(entry['audio_src'], 'assets/chapter-019.mp3')

        route = json.loads((ROOT / 'r2/data/chapters/ch019.json').read_text(encoding='utf-8'))
        self.assertEqual(route['title'], 'The Maintainer')
        self.assertEqual(route['audio']['status'], 'published')
        self.assertEqual(route['audio']['path'], '../greg-again/audio/assets/chapter-019.mp3')

        self.assertTrue((ROOT / 'greg-again/audio/assets/chapter-019.mp3').is_file())
        for n in range(1, 37):
            self.assertTrue((ROOT / f'greg-again/audio/assets/chunks/019/{n:02d}.mp3').is_file())


if __name__ == '__main__':
    unittest.main()
