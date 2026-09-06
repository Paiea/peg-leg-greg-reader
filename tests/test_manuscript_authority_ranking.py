import tempfile
import unittest
import zipfile
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from manuscript_authority import discover_manuscript_chapters


def write_minimal_docx(path: Path, paragraphs: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    body = "".join(
        f'<w:p><w:r><w:t>{text}</w:t></w:r></w:p>'
        for text in paragraphs
    )
    document = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        f'<w:body>{body}</w:body></w:document>'
    )
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("word/document.xml", document)


class ManuscriptAuthorityRankingTests(unittest.TestCase):
    def test_explicit_authoritative_book2_docx_beats_historical_snapshots(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            manuscript = root / "state/manuscript"
            manuscript.mkdir(parents=True)
            write_minimal_docx(
                manuscript / "Peg_Leg_Greg_Book2_Ch83-105_light_ship_edited.docx",
                ["CHAPTER 83", "THE OLD TITLE"],
            )
            write_minimal_docx(
                manuscript / "Peg_Leg_Greg_Book2_Manuscript_Ch83-137.docx",
                ["CHAPTER 83", "THE LATER SNAPSHOT"],
            )
            write_minimal_docx(
                manuscript / "Peg_Leg_Greg_Book2_Ch83-113_authoritative.docx",
                ["CHAPTER 83", "THE SUITOR"],
            )

            report = discover_manuscript_chapters(root)
            chapter = report["chapters"][0]

            self.assertEqual(chapter["source_kind"], "authoritative_docx")
            self.assertEqual(chapter["title"], "THE SUITOR")
            self.assertEqual(report["authority_conflicts"], [])

    def test_latest_broad_snapshot_wins_when_no_explicit_authority_covers_chapter(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            manuscript = root / "state/manuscript"
            manuscript.mkdir(parents=True)
            write_minimal_docx(
                manuscript / "Peg_Leg_Greg_Book2_Manuscript_Ch83-123.docx",
                ["CHAPTER 120", "THE OLD VERSION"],
            )
            write_minimal_docx(
                manuscript / "Peg_Leg_Greg_Book2_Manuscript_Ch83-137.docx",
                ["CHAPTER 120", "THE REPEATER"],
            )

            report = discover_manuscript_chapters(root)
            chapter = report["chapters"][0]

            self.assertTrue(chapter["path"].endswith("Ch83-137.docx"))
            self.assertEqual(chapter["title"], "THE REPEATER")
            self.assertEqual(report["authority_conflicts"], [])

    def test_docx_prose_is_not_misidentified_as_title(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            manuscript = root / "state/manuscript"
            manuscript.mkdir(parents=True)
            write_minimal_docx(
                manuscript / "Peg_Leg_Greg_authoritative_ch82_final_name_map.docx",
                [
                    "CHAPTER TWELVE",
                    "A spoon is an underrated investigative instrument. It is terrible at cutting.",
                    "CHAPTER THIRTEEN",
                    "THE STUDENT",
                ],
            )

            report = discover_manuscript_chapters(root)
            by_number = {row["chapter_number"]: row for row in report["chapters"]}

            self.assertIsNone(by_number[12]["title"])
            self.assertEqual(by_number[13]["title"], "THE STUDENT")

    def test_case_only_title_differences_do_not_create_index_mismatch(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            manuscript = root / "state/manuscript"
            manuscript.mkdir(parents=True)
            write_minimal_docx(
                manuscript / "Peg_Leg_Greg_authoritative_ch82_final_name_map.docx",
                ["CHAPTER ONE", "The Boy"],
            )
            (root / "state/MANUSCRIPT_CHAPTER_INDEX.md").write_text(
                "1. **THE BOY**\n", encoding="utf-8"
            )

            report = discover_manuscript_chapters(root)

            self.assertEqual(report["chapter_index_title_mismatches"], [])


if __name__ == "__main__":
    unittest.main()
