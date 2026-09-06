import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from whole_book_compression_audit import audit_chapters, extract_visible_text


HTML = """<!doctype html><html><body><main><h1>Chapter {n}</h1><h2>{title}</h2>{body}</main></body></html>"""


class WholeBookCompressionAuditTests(unittest.TestCase):
    def write_chapter(self, root: Path, n: int, title: str, body: str) -> None:
        chapters = root / "chapters"
        chapters.mkdir(parents=True, exist_ok=True)
        (chapters / f"{n:03}.html").write_text(
            HTML.format(n=n, title=title, body=body), encoding="utf-8"
        )

    def test_extract_visible_text_strips_markup(self):
        text = extract_visible_text("<p>Greg <strong>counted</strong> crates.</p>")
        self.assertEqual(text, "Greg counted crates.")

    def test_adjacent_repeated_function_language_ranks_as_candidate(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            repeated = (
                "<p>Greg checked the ledger. He counted the crates, checked the tags, "
                "marked the mismatch, and asked the clerk before changing anything.</p>" * 18
            )
            distinct = (
                "<p>Greg went swimming with Lyssa and argued about oranges while a gull stole lunch.</p>" * 18
            )
            self.write_chapter(root, 1, "THE CHECKER", repeated)
            self.write_chapter(root, 2, "THE COUNTER", repeated.replace("ledger", "manifest"))
            self.write_chapter(root, 3, "THE SWIMMER", distinct)

            report = audit_chapters(root)
            candidates = report["ranked_candidates"]
            self.assertTrue(candidates)
            self.assertEqual(candidates[0]["start_chapter"], 1)
            self.assertEqual(candidates[0]["end_chapter"], 2)
            self.assertGreater(candidates[0]["score"], 0.5)

    def test_distinct_neighboring_chapters_are_not_forced_into_candidate(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.write_chapter(root, 1, "THE COOK", "<p>Soup onions stove supper family laughter.</p>" * 30)
            self.write_chapter(root, 2, "THE FIGHTER", "<p>Hound mud crutch pivot blood ambush road.</p>" * 30)
            self.write_chapter(root, 3, "THE BUYER", "<p>Market copper hinge price merchant repair.</p>" * 30)
            report = audit_chapters(root)
            self.assertEqual(report["ranked_candidates"], [])

    def test_report_includes_keep_signals_for_unique_chapters(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.write_chapter(root, 1, "THE ARRIVAL", "<p>First arrival new town bridge stranger bell.</p>" * 30)
            self.write_chapter(root, 2, "THE LETTER", "<p>Letter from Lyssa changed the promise and route home.</p>" * 30)
            report = audit_chapters(root)
            self.assertEqual(report["chapter_count"], 2)
            self.assertEqual(len(report["chapter_metrics"]), 2)
            self.assertIn("word_count", report["chapter_metrics"][0])


if __name__ == "__main__":
    unittest.main()
