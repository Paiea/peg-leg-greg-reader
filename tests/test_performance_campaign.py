import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import performance_campaign
from scripts import performance_production_funnel as funnel


class PerformanceCampaignTests(unittest.TestCase):
    def _chapters(self, root: Path) -> Path:
        chapters = root / "chapters"
        chapters.mkdir()
        (chapters / "001.html").write_text('<article class="prose"><p>Greg lifted the box.</p></article>', encoding="utf-8")
        (chapters / "002.html").write_text('<article class="prose"><p>Antonius closed the door.</p></article>', encoding="utf-8")
        return chapters

    @staticmethod
    def _survivor(chapter: int, start: str, end: str, replacement: list[str]) -> dict:
        return {
            "chapter": chapter,
            "verdict": "change_survives",
            "screen": {"decision": "deep_review", "signals": ["test"], "reason": "Test survivor."},
            "dramatic": "Locked dramatic truth.",
            "performance": "Performed result.",
            "screenplay": "Performed script.",
            "comparison": "Performance earns this bounded change.",
            "patches": [{"start": start, "end": end, "replacement": replacement, "rationale": "Test patch."}],
        }

    def test_plan_compiles_range_without_mutating_canon_and_creates_scene_packets(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            chapters = self._chapters(root)
            before = {p.name: p.read_text(encoding="utf-8") for p in chapters.glob("*.html")}
            result = performance_campaign.plan_campaign(task="reverse_edit", chapter_start=1, chapter_end=2, source_authority="abc12345", chapter_root=chapters, cache_root=root / ".cache" / "plg", profile="eco", executor="manual")
            self.assertEqual(2, result["scenes_considered"])
            self.assertEqual(2, result["packets_planned"])
            self.assertEqual(0, result["cache_hits"])
            self.assertTrue(Path(result["campaign_root"]).joinpath("campaign.json").exists())
            self.assertTrue((root / ".cache" / "plg" / "project-index.sqlite").exists())
            after = {p.name: p.read_text(encoding="utf-8") for p in chapters.glob("*.html")}
            self.assertEqual(before, after)

    def test_plan_skips_scene_with_cache_valid_comparison(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            chapters = self._chapters(root)
            cache_root = root / ".cache" / "plg"
            compiled = cache_root / "compiler"
            funnel.write_compiled_chapter(1, (chapters / "001.html").read_text(encoding="utf-8"), compiled)
            scene_path = compiled / "001" / "s010.json"
            scene = json.loads(scene_path.read_text(encoding="utf-8"))
            scene["comparison"] = {"verdict": "source_win", "reason": "Already stronger.", "compiler": "comparison/v1", "dependency_hash": "dep"}
            scene["dependencies"]["comparison"] = {"compiler": "comparison/v1", "dependency_hash": "dep"}
            scene_path.write_text(json.dumps(scene), encoding="utf-8")
            result = performance_campaign.plan_campaign(task="reverse_edit", chapter_start=1, chapter_end=2, source_authority="abc12345", chapter_root=chapters, cache_root=cache_root, profile="eco", executor="manual")
            self.assertEqual(1, result["cache_hits"])
            self.assertEqual(1, result["packets_planned"])

    def test_reduce_is_deterministic_and_compact(self):
        with tempfile.TemporaryDirectory() as tmp:
            campaign_root = Path(tmp)
            results = [
                {"packet_id": "001.s010:x", "scene_id": "001.s010", "status": "completed", "comparison": {"verdict": "source_win", "reason": "source"}},
                {"packet_id": "002.s010:x", "scene_id": "002.s010", "status": "completed", "comparison": {"verdict": "performance_candidate", "possible_wins": [{"surface": "dialogue", "problem": "repeat", "performed_advantage": "action", "source_span": ["a", "b"]}]}},
                {"packet_id": "003.s010:x", "scene_id": "003.s010", "status": "completed", "comparison": {"verdict": "ambiguous", "reason": "unclear"}},
            ]
            (campaign_root / "results.jsonl").write_text("".join(json.dumps(r) + "\n" for r in results), encoding="utf-8")
            first = performance_campaign.reduce_campaign(campaign_root)
            second = performance_campaign.reduce_campaign(campaign_root)
            self.assertEqual(first, second)
            self.assertEqual(1, first["source_wins"])
            self.assertEqual(1, first["performance_candidates"])
            self.assertEqual(1, first["ambiguous"])
            self.assertEqual(["002.s010"], first["candidate_scenes"])

    def test_integration_blocks_authority_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            chapters = self._chapters(root)
            campaign_root = root / "campaign"
            campaign_root.mkdir()
            (campaign_root / "campaign.json").write_text(json.dumps({"schema": "performance_campaign/v1", "campaign_id": "x", "task": "reverse_edit", "source_authority": "oldsha", "scope": {"chapters": {"start": 1, "end": 1}}, "execution": {"profile": "eco", "executor": "manual"}}), encoding="utf-8")
            (campaign_root / "results.jsonl").write_text("", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "authority drift"):
                performance_campaign.integrate_campaign(campaign_root, chapters, current_authority="newsha")

    def test_overlapping_survivors_fail_before_canon_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            chapters = root / "chapters"
            chapters.mkdir()
            chapter = chapters / "001.html"
            chapter.write_text('<article class="prose"><p>A.</p><p>B.</p><p>C.</p></article>', encoding="utf-8")
            before = chapter.read_bytes()
            campaign_root = root / "campaign"
            campaign_root.mkdir()
            (campaign_root / "campaign.json").write_text(json.dumps({"schema": "performance_campaign/v1", "campaign_id": "overlap", "task": "reverse_edit", "source_authority": "same-sha", "scope": {"chapters": {"start": 1, "end": 1}}, "execution": {"profile": "eco", "executor": "manual"}}), encoding="utf-8")
            rows = [
                {"packet_id": "001.s010:x", "scene_id": "001.s010", "status": "completed", "record": self._survivor(1, "A.", "B.", ["AB."])},
                {"packet_id": "001.s020:x", "scene_id": "001.s020", "status": "completed", "record": self._survivor(1, "B.", "C.", ["BC."])},
            ]
            (campaign_root / "results.jsonl").write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "overlapping"):
                performance_campaign.integrate_campaign(campaign_root, chapters, current_authority="same-sha")
            self.assertEqual(before, chapter.read_bytes())

    def test_run_cli_can_plan_and_execute_in_one_command(self):
        with mock.patch.object(performance_campaign, "plan_campaign", return_value={"campaign_id": "all", "campaign_root": "/tmp/all", "packets_planned": 300}) as plan, mock.patch.object(performance_campaign, "run_campaign", return_value={"completed": 300, "failures": 0}) as run:
            exit_code = performance_campaign.main(["run", "--task", "reverse-edit", "--chapters", "1:491", "--source-authority", "sha", "--profile", "eco"])
        self.assertEqual(0, exit_code)
        plan.assert_called_once()
        run.assert_called_once_with(Path("/tmp/all"))


if __name__ == "__main__":
    unittest.main()
