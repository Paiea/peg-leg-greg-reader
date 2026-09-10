import hashlib,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
AUDIO=ROOT/'greg-again'/'audio'
R2=ROOT/'r2'
class GregAgainChapter41AudioTest(unittest.TestCase):
    def test_chapter_41_is_durable_verified_and_routed(self):
        manifest=json.loads((AUDIO/'manifest.json').read_text())
        by_id={c['chapter_id']:c for c in manifest['chapters']}
        c=by_id['ga-041']
        self.assertEqual(41,c['number']); self.assertEqual('The Cordon',c['title'])
        self.assertEqual('shared-greg-surface',c['lens']); self.assertEqual('processing-space',c['audio_finish'])
        self.assertEqual(30,c['take_count']); self.assertEqual(785.448,c['duration_seconds'])
        self.assertEqual('assets/chapter-041.mp3',c['audio_src'])
        final=AUDIO/'assets'/'chapter-041.mp3'
        self.assertTrue(final.exists()); self.assertEqual(12567597,final.stat().st_size)
        self.assertEqual('0d7dc39f03031b0836658d23a442fc3d507e1a059668054c9d23c7c0583f4f62',hashlib.sha256(final.read_bytes()).hexdigest())
        m=json.loads((AUDIO/'takes'/'041-short.json').read_text())
        self.assertEqual('ga-041',m['chapter_id']); self.assertEqual('deep',m['voice']); self.assertEqual('verified_playable',m['status'])
        self.assertEqual(30,len(m['takes'])); self.assertEqual(list(range(1,31)),[t['take'] for t in m['takes']])
        self.assertEqual(785.448,m['assembled_duration_seconds'])
        for t in m['takes']:
            self.assertEqual('artifact_captured_verified',t['status'])
            f=ROOT/t['durable_file']; self.assertTrue(f.exists()); self.assertGreater(f.stat().st_size,10000)
            self.assertTrue(t['provider_context_id'])
            self.assertTrue(t['preview_url'].startswith('https://storage.googleapis.com/adm--audio-playback--7d--public/mcp-preview/'))
            self.assertEqual(t['sha256'],hashlib.sha256(f.read_bytes()).hexdigest())
        self.assertEqual('Ma-na',m['takes'][12]['provider_transcript'].split('discharge?')[0].split('\n')[-1].strip('" '))
        v=json.loads((AUDIO/'verification'/'041-short.json').read_text())
        self.assertTrue(v['exact_source_coverage']); self.assertTrue(v['take_order_verified'])
        self.assertTrue(v['individual_mp3s_verified']); self.assertTrue(v['assembled_mp3_verified'])
        self.assertTrue(v['seam_continuity_verified']); self.assertEqual(2.0,v['chapter_tail_silence_seconds_added'])
        self.assertEqual([{'take':13,'written':'Mana','provider':'Ma-na'}],v['pronunciation_substitutions'])
        route=json.loads((R2/'data'/'chapters'/'ch041.json').read_text())
        self.assertEqual('The Cordon',route['title']); self.assertEqual('published',route['audio']['status'])
        self.assertEqual('../greg-again/audio/assets/chapter-041.mp3',route['audio']['path'])
if __name__=='__main__': unittest.main()
