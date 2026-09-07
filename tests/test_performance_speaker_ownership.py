import json
import tempfile
import unittest
from pathlib import Path

from scripts import performance_campaign
from scripts import performance_production_funnel as funnel
from scripts import performance_selected_campaign


class PerformanceSpeakerOwnershipTests(unittest.TestCase):
    def test_selected_reverse_edit_packet_carries_speaker_ownership_policy_into_prompt(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            chapters = root / "chapters"
            chapters.mkdir()
            (chapters / "001.html").write_text(
                '<article class="prose"><p>“You coming?”</p><p>Greg looked at Sera.</p><p>“Maybe.”</p></article>',
                encoding="utf-8",
            )
            result = performance_selected_campaign.plan_selected_campaign(
                task="reverse_edit",
                chapter_ids=[1],
                source_authority="abc12345",
                chapter_root=chapters,
                cache_root=root / ".cache" / "plg",
                executor="manual",
            )
            campaign_root = Path(result["campaign_root"])
            packet = json.loads((campaign_root / "packets.jsonl").read_text(encoding="utf-8").strip())
            scene = funnel.load_scene_record(root / ".cache" / "plg" / "compiler", "001.s010")

            prompt = performance_campaign.build_worker_prompt(packet, scene)

            self.assertEqual("screenplay_ground_truth", packet["speaker_ownership_policy"]["authority"])
            self.assertIn("speaker ownership", prompt.lower())
            self.assertIn("three or more speakers", prompt.lower())
            self.assertIn("another character's action", prompt.lower())
            self.assertIn("said/asked", prompt.lower())
            self.assertIn("preserve clean two-person alternation", prompt.lower())

    def test_selected_performance_packet_does_not_add_prose_attribution_policy(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            chapters = root / "chapters"
            chapters.mkdir()
            (chapters / "001.html").write_text(
                '<article class="prose"><p>Greg lifted the box.</p></article>',
                encoding="utf-8",
            )
            result = performance_selected_campaign.plan_selected_campaign(
                task="performance",
                chapter_ids=[1],
                source_authority="abc12345",
                chapter_root=chapters,
                cache_root=root / ".cache" / "plg",
                executor="manual",
            )
            campaign_root = Path(result["campaign_root"])
            packet = json.loads((campaign_root / "packets.jsonl").read_text(encoding="utf-8").strip())

            self.assertNotIn("speaker_ownership_policy", packet)


if __name__ == "__main__":
    unittest.main()
