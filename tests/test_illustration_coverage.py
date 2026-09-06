from pathlib import Path
import tempfile
import unittest

from scripts.report_illustration_coverage import (
    find_unmanaged_live_art,
    summarize_coverage,
    render_coverage_report,
)


class IllustrationCoverageTests(unittest.TestCase):
    def test_coverage_buckets_zero_one_two_three_plus(self):
        summary = summarize_coverage(
            {1: 0, 2: 1, 3: 2, 4: 3, 5: 5},
            candidates=[],
            registry=[],
        )
        self.assertEqual(summary["zero_art"], 1)
        self.assertEqual(summary["one_art"], 1)
        self.assertEqual(summary["two_art"], 1)
        self.assertEqual(summary["three_plus_art"], 2)

    def test_counts_approved_but_unpublished_and_candidate_backlog(self):
        registry = [
            {"status": "approved"},
            {"status": "live"},
            {"status": "generated"},
        ]
        candidates = [
            {"status": "candidate"},
            {"status": "prompt_ready"},
            {"status": "live"},
            {"status": "rejected"},
        ]
        summary = summarize_coverage({1: 0}, candidates, registry)
        self.assertEqual(summary["approved_unpublished"], 1)
        self.assertEqual(summary["queued_candidates"], 2)

    def test_unmanaged_live_art_is_reported_as_migration_debt(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            chapter_dir = Path(temp_dir)
            (chapter_dir / "001.html").write_text(
                '<figure class="chapter-art"><img src="../visual/chapter_art/001/a.png" alt="A"/></figure>',
                encoding="utf-8",
            )
            unmanaged = find_unmanaged_live_art(chapter_dir, registry=[])
            self.assertEqual(unmanaged, ["visual/chapter_art/001/a.png"])

    def test_registered_live_art_is_not_unmanaged(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            chapter_dir = Path(temp_dir)
            (chapter_dir / "001.html").write_text(
                '<figure class="chapter-art"><img src="../visual/chapter_art/001/a.png" alt="A"/></figure>',
                encoding="utf-8",
            )
            registry = [{"status": "live", "live_asset": "visual/chapter_art/001/a.png"}]
            self.assertEqual(find_unmanaged_live_art(chapter_dir, registry), [])

    def test_report_names_unmanaged_legacy_art_without_calling_it_failure(self):
        summary = {
            "frontier": 10,
            "total_chapters": 10,
            "illustrated_chapters": 4,
            "zero_art": 6,
            "one_art": 2,
            "two_art": 1,
            "three_plus_art": 1,
            "approved_unpublished": 2,
            "queued_candidates": 7,
            "registry_live": 3,
            "unmanaged_live_art": 12,
        }
        text = render_coverage_report(summary)
        self.assertIn("Unmanaged legacy live art: 12", text)
        self.assertIn("migration debt", text.lower())
        self.assertIn("Frontier: Chapter 10", text)


if __name__ == "__main__":
    unittest.main()
