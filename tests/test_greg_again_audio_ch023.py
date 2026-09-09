import json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]; A=R/'greg-again'/'audio'
class T(unittest.TestCase):
  def test_ch23(self):
    c={x['chapter_id']:x for x in json.loads((A/'manifest.json').read_text())['chapters']}['ga-023']; self.assertEqual((23,'The Adventurer',46,1020.408),(c['number'],c['title'],c['take_count'],c['duration_seconds'])); self.assertGreater((A/'assets/chapter-023.mp3').stat().st_size,8_000_000)
    m=json.loads((A/'takes/023-short.json').read_text()); self.assertEqual(('ga-023','deep','verified_playable',46,1020.408),(m['chapter_id'],m['voice'],m['status'],len(m['takes']),m['assembled_duration_seconds']))
    for t in m['takes']: self.assertEqual('artifact_captured',t['status']); self.assertGreater((R/t['durable_file']).stat().st_size,10_000)
    self.assertEqual('published',json.loads((R/'r2/data/chapters/ch023.json').read_text())['audio']['status']); self.assertEqual('published',json.loads((R/'r2/data/chapter-registry.json').read_text())['chapters']['r2-ch023']['pipeline']['audio'])
