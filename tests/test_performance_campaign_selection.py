import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import performance_campaign
from scripts import performance_selected_campaign as selected


class PerformanceCampaignSelectionTests(unittest.TestCase):
    def test_plan_accepts_noncontiguous_explicit_chapter_ids(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            chapters = root / "chapters"
            chapters.mkdir()
            for chapter in (27, 28, 30, 34):
                (chapters / f"{chapter:03d}.html").write_text(
                    f'<article class="prose"><p>Chapter {chapter}.</p></article>', encoding="utf-8"
                )
            result = selected.plan_selected_campaign(
                task="reverse_edit", chapter_ids=[27, 28, 30, 34], source_authority="abc12345",
                chapter_root=chapters, cache_root=root / ".cache" / "plg", profile="eco", executor="manual"
            )
            self.assertEqual(4, result["scenes_considered"])
            campaign = selected.read_campaign(Path(result["campaign_root"]))
            self.assertEqual([27, 28, 30, 34], campaign["scope"]["chapter_ids"])
            self.assertEqual("explicit", campaign["scope"]["selection"])

    def test_plan_rejects_duplicate_or_empty_chapter_ids(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            chapters = root / "chapters"
            chapters.mkdir()
            with self.assertRaisesRegex(ValueError, "chapter_ids"):
                selected.plan_selected_campaign(task="reverse_edit", chapter_ids=[], source_authority="sha", chapter_root=chapters, cache_root=root / ".cache")
            with self.assertRaisesRegex(ValueError, "duplicate"):
                selected.plan_selected_campaign(task="reverse_edit", chapter_ids=[27, 27], source_authority="sha", chapter_root=chapters, cache_root=root / ".cache")

    def test_cli_plans_then_delegates_execution_to_existing_runner(self):
        chapter_ids = [27,28,29,30,31,32,34,35,36,37,39,40,41,42,44,45,47,50,51,52,53,54,55,56,58,59,60,61,62,63,64,65,67,68,69,70,71,72,74,75,76,77,78,79,80,81,82,83,84,86]
        with mock.patch.object(selected, "plan_selected_campaign", return_value={"campaign_id":"selected","campaign_root":"/tmp/selected","packets_planned":50}) as plan, mock.patch.object(performance_campaign, "run_campaign", return_value={"completed":50,"failures":0}) as run:
            code = selected.main([
                "run", "--task", "reverse-edit",
                "--chapter-ids", ",".join(str(value) for value in chapter_ids),
                "--source-authority", "sha", "--profile", "eco"
            ])
        self.assertEqual(0, code)
        self.assertEqual(chapter_ids, plan.call_args.kwargs["chapter_ids"])
        run.assert_called_once_with(Path("/tmp/selected"))


if __name__ == "__main__":
    unittest.main()
