import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'greg-again'/'audio'
R=ROOT/'r2'
class GregAgainChapter26AudioTest(unittest.TestCase):
    def test_chapter_26_is_durable_and_routed(self):
        m=json.loads((A/'manifest.json').read_text())
        c={x['chapter_id']:x for x in m['chapters']}['ga-026']
        self.assertEqual('The Day Off',c['title'])
        self.assertEqual(38,c['take_count'])
        self.assertEqual('assets/chapter-026.mp3',c['audio_src'])
        self.assertTrue((A/'assets/chapter-026.mp3').stat().st_size>1_000_000)
        t=json.loads((A/'takes/026-short.json').read_text())
        self.assertEqual(38,len(t['takes']))
        self.assertEqual('verified_playable',t['status'])
        for x in t['takes']:
            self.assertEqual('artifact_captured_verified',x['status'])
            self.assertTrue((ROOT/x['durable_file']).stat().st_size>10_000)
            self.assertEqual(64,len(x['sha256']))
        v=json.loads((A/'verification/026-short.json').read_text())
        self.assertTrue(v['exact_source_coverage'])
        self.assertTrue(v['take_order_verified'])
        self.assertTrue(v['individual_mp3s_verified'])
        self.assertTrue(v['assembled_mp3_verified'])
        self.assertEqual(2.0,v['chapter_tail_silence_seconds_added'])
        route=json.loads((R/'data/chapters/ch026.json').read_text())
        self.assertEqual('published',route['audio']['status'])
        reg=json.loads((R/'data/chapter-registry.json').read_text())
        self.assertEqual('published',reg['chapters']['r2-ch026']['pipeline']['audio'])
if __name__=='__main__': unittest.main()
