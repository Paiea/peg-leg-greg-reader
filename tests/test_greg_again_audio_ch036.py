import hashlib,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
AUDIO=ROOT/"greg-again"/"audio"
R2=ROOT/"r2"
class GregAgainChapter36AudioTest(unittest.TestCase):
    def test_chapter_36_is_durable_verified_and_routed(self):
        manifest=json.loads((AUDIO/"manifest.json").read_text())
        by_id={c["chapter_id"]:c for c in manifest["chapters"]}
        c=by_id["ga-036"]
        self.assertEqual(36,c["number"]); self.assertEqual("Four Nights",c["title"])
        self.assertEqual("shared-greg-surface",c["lens"]); self.assertEqual("processing-space",c["audio_finish"])
        self.assertEqual(33,c["take_count"]); self.assertEqual(662.496,c["duration_seconds"])
        self.assertEqual("assets/chapter-036.mp3",c["audio_src"])
        final=AUDIO/"assets"/"chapter-036.mp3"
        self.assertTrue(final.exists()); self.assertEqual(10600365,final.stat().st_size)
        self.assertEqual("3dc0cec0265257e1f47e05397434515b48e1f6658f01f06703daa5c07e46bba8",hashlib.sha256(final.read_bytes()).hexdigest())
        m=json.loads((AUDIO/"production"/"036"/"takes.json").read_text())
        self.assertEqual("ga-036",m["chapter_id"]); self.assertEqual("deep",m["voice"]); self.assertEqual("verified_playable",m["status"])
        self.assertEqual(33,len(m["takes"])); self.assertEqual(list(range(1,34)),[t["take"] for t in m["takes"]])
        self.assertEqual(662.496,m["assembled_duration_seconds"])
        for t in m["takes"]:
            self.assertEqual("artifact_captured_verified",t["status"])
            f=ROOT/t["durable_path"]; self.assertTrue(f.exists()); self.assertGreater(f.stat().st_size,10000)
            self.assertTrue(t["context_id"])
            self.assertTrue(t["preview_url"].startswith("https://storage.googleapis.com/adm--audio-playback--7d--public/mcp-preview/"))
            self.assertEqual(t["sha256"],hashlib.sha256(f.read_bytes()).hexdigest())
        v=json.loads((AUDIO/"verification"/"036-short.json").read_text())
        self.assertEqual("exact_after_nonspoken_markdown_normalization",v["source_coverage"])
        self.assertTrue(v["take_order_verified"]); self.assertTrue(v["all_takes_playable"])
        self.assertEqual(2.0,v["chapter_tail_silence_seconds"])
        route=json.loads((R2/"data"/"chapters"/"ch036.json").read_text())
        self.assertEqual("Four Nights",route["title"]); self.assertEqual("published",route["audio"]["status"])
        self.assertEqual("../greg-again/audio/assets/chapter-036.mp3",route["audio"]["path"])
        registry=json.loads((R2/"data"/"chapter-registry.json").read_text())
        self.assertEqual("published",registry["chapters"]["r2-ch036"]["pipeline"]["audio"])
if __name__=="__main__": unittest.main()
