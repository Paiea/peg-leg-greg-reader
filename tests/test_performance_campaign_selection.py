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
            for chapter in (1, 2, 4, 7):
                (chapters / f"{chapter:03d}.html").write_text(
                    f'<article class="prose"><p>Chapter {chapter}.</p></article>', encoding="utf-8"
                )
            result = selected.plan_selected_campaign(
                task="reverse_edit", chapter_ids=[1, 2, 4, 7], source_authority="abc12345",
                chapter_root=chapters, cache_root=root / ".cache" / "plg", profile="eco", executor="manual"
            )
            self.assertEqual(4, result["scenes_considered"])
            campaign = selected.read_campaign(Path(result["campaign_root"]))
            self.assertEqual([1, 2, 4, 7], campaign["scope"]["chapter_ids"])
            self.assertEqual("explicit", campaign["scope"]["selection"])

    def test_plan_rejects_duplicate_or_empty_chapter_ids(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            chapters = root / "chapters"
            chapters.mkdir()
            with self.assertRaisesRegex(ValueError, "chapter_ids"):
                selected.plan_selected_campaign(task="reverse_edit", chapter_ids=[], source_authority="sha", chapter_root=chapters, cache_root=root / ".cache")
            with self.assertRaisesRegex(ValueError, "duplicate"):
                selected.plan_selected_campaign(task="reverse_edit", chapter_ids=[1, 1], source_authority="sha", chapter_root=chapters, cache_root=root / ".cache")

    def test_cli_plans_then_delegates_execution_to_existing_runner(self):
        with mock.patch.object(selected, "plan_selected_campaign", return_value={"campaign_id":"selected","campaign_root":"/tmp/selected","packets_planned":20}) as plan, mock.patch.object(performance_campaign, "run_campaign", return_value={"completed":20,"failures":0}) as run:
            code = selected.main([
                "run", "--task", "reverse-edit",
                "--chapter-ids", "1,2,4,5,7,9,10,11,13,14,15,16,17,18,19,22,23,24,25,26",
                "--source-authority", "sha", "--profile", "eco"
            ])
        self.assertEqual(0, code)
        self.assertEqual([1,2,4,5,7,9,10,11,13,14,15,16,17,18,19,22,23,24,25,26], plan.call_args.kwargs["chapter_ids"])
        run.assert_called_once_with(Path("/tmp/selected"))


if __name__ == "__main__":
    unittest.main()
