import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import performance_campaign


class PerformanceCampaignSelectionTests(unittest.TestCase):
    def test_plan_accepts_noncontiguous_explicit_chapter_ids(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            chapters = root / "chapters"
            chapters.mkdir()
            for chapter in (1, 2, 4, 7):
                (chapters / f"{chapter:03d}.html").write_text(
                    f'<article class="prose"><p>Chapter {chapter}.</p></article>',
                    encoding="utf-8",
                )
            result = performance_campaign.plan_campaign(
                task="reverse_edit",
                chapter_ids=[1, 2, 4, 7],
                source_authority="abc12345",
                chapter_root=chapters,
                cache_root=root / ".cache" / "plg",
                profile="eco",
                executor="manual",
            )
            self.assertEqual(4, result["scenes_considered"])
            campaign = (Path(result["campaign_root"]) / "campaign.json").read_text(encoding="utf-8")
            self.assertIn('"ids": [', campaign)
            self.assertIn('7', campaign)

    def test_plan_rejects_duplicate_or_empty_chapter_ids(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            chapters = root / "chapters"
            chapters.mkdir()
            with self.assertRaisesRegex(ValueError, "chapter_ids"):
                performance_campaign.plan_campaign(task="reverse_edit", chapter_ids=[], source_authority="sha", chapter_root=chapters, cache_root=root / ".cache")
            with self.assertRaisesRegex(ValueError, "duplicate"):
                performance_campaign.plan_campaign(task="reverse_edit", chapter_ids=[1, 1], source_authority="sha", chapter_root=chapters, cache_root=root / ".cache")

    def test_run_cli_accepts_comma_separated_chapter_ids(self):
        with mock.patch.object(performance_campaign, "plan_campaign", return_value={"campaign_id":"selected","campaign_root":"/tmp/selected","packets_planned":20}) as plan, mock.patch.object(performance_campaign, "run_campaign", return_value={"completed":20,"failures":0}) as run:
            code = performance_campaign.main([
                "run", "--task", "reverse-edit",
                "--chapter-ids", "1,2,4,5,7,9,10,11,13,14,15,16,17,18,19,22,23,24,25,26",
                "--source-authority", "sha", "--profile", "eco"
            ])
        self.assertEqual(0, code)
        kwargs = plan.call_args.kwargs
        self.assertEqual([1,2,4,5,7,9,10,11,13,14,15,16,17,18,19,22,23,24,25,26], kwargs["chapter_ids"])
        run.assert_called_once_with(Path("/tmp/selected"))


if __name__ == "__main__":
    unittest.main()
