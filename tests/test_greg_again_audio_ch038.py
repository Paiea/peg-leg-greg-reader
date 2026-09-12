import hashlib,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
AUDIO=ROOT/'greg-again'/'audio'
R2=ROOT/'r2'
class GregAgainChapter38AudioTest(unittest.TestCase):
    def test_chapter_38_is_durable_verified_and_routed(self):
        manifest=json.loads((AUDIO/'manifest.json').read_text())
        by_id={c['chapter_id']:c for c in manifest['chapters']}
        c=by_id['ga-038']
        self.assertEqual(38,c['number']); self.assertEqual('The Host',c['title'])
        self.assertEqual('shared-greg-surface',c['lens']); self.assertEqual('processing-space',c['audio_finish'])
        self.assertEqual(33,c['take_count']); self.assertEqual(771.528,c['duration_seconds'])
        self.assertEqual('assets/chapter-038.mp3',c['audio_src'])
        final=AUDIO/'assets'/'chapter-038.mp3'
        self.assertTrue(final.exists()); self.assertEqual(12344877,final.stat().st_size)
        self.assertEqual('2fc51d5434e4bee6905c133c981128acbfd5598ba367451703ddef70b8d7e0fa',hashlib.sha256(final.read_bytes()).hexdigest())
        m=json.loads((AUDIO/'takes'/'038-short.json').read_text())
        self.assertEqual('ga-038',m['chapter_id']); self.assertEqual('deep',m['voice']); self.assertEqual('verified_playable',m['status'])
        self.assertEqual(33,len(m['takes'])); self.assertEqual(list(range(1,34)),[t['take'] for t in m['takes']])
        self.assertEqual(771.528,m['assembled_duration_seconds'])
        for t in m['takes']:
            self.assertEqual('artifact_captured_verified',t['status'])
            f=ROOT/t['durable_file']; self.assertTrue(f.exists()); self.assertGreater(f.stat().st_size,10000)
            self.assertTrue(t['provider_context_id'])
            self.assertTrue(t['preview_url'].startswith('https://storage.googleapis.com/adm--audio-playback--7d--public/mcp-preview/'))
            self.assertEqual(t['sha256'],hashlib.sha256(f.read_bytes()).hexdigest())
        v=json.loads((AUDIO/'verification'/'038-short.json').read_text())
        self.assertTrue(v['exact_source_coverage']); self.assertTrue(v['take_order_verified'])
        self.assertTrue(v['individual_mp3s_verified']); self.assertTrue(v['assembled_mp3_verified'])
        self.assertTrue(v['seam_continuity_verified']); self.assertEqual(2.0,v['chapter_tail_silence_seconds_added'])
        route=json.loads((R2/'data'/'chapters'/'ch038.json').read_text())
        self.assertEqual('The Host',route['title']); self.assertEqual('published',route['audio']['status'])
        self.assertEqual('../greg-again/audio/assets/chapter-038.mp3',route['audio']['path'])
        registry=json.loads((R2/'data'/'chapter-registry.json').read_text())
        self.assertEqual('published',registry['chapters']['r2-ch038']['pipeline']['audio'])
if __name__=='__main__': unittest.main()
