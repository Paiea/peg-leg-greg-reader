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


class BookOneAuthorityCoverageTests(unittest.TestCase):
    def test_compound_number_words_with_spaces_are_discovered_from_authoritative_docx(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            manuscript = root / "state/manuscript"
            manuscript.mkdir(parents=True)
            write_minimal_docx(
                manuscript / "Peg_Leg_Greg_authoritative_ch82_final_name_map.docx",
                [
                    "CHAPTER SIXTY FIVE",
                    "THE WARD",
                    "CHAPTER EIGHTY TWO",
                    "THE RECONCILER",
                ],
            )

            report = discover_manuscript_chapters(root)
            by_number = {row["chapter_number"]: row for row in report["chapters"]}

            self.assertEqual(by_number[65]["source_kind"], "authoritative_docx")
            self.assertEqual(by_number[65]["title"], "THE WARD")
            self.assertEqual(by_number[82]["source_kind"], "authoritative_docx")
            self.assertEqual(by_number[82]["title"], "THE RECONCILER")

    def test_concatenated_number_and_title_from_real_book1_format_are_split(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            manuscript = root / "state/manuscript"
            manuscript.mkdir(parents=True)
            write_minimal_docx(
                manuscript / "Peg_Leg_Greg_authoritative_ch82_final_name_map.docx",
                [
                    "CHAPTER FIFTY-THREETHE GUEST",
                    "Body prose.",
                    "CHAPTER SIXTY-FIVETHE WARD",
                    "Body prose.",
                    "CHAPTER EIGHTY-TWOTHE RECONCILER",
                    "Body prose.",
                ],
            )

            report = discover_manuscript_chapters(root)
            by_number = {row["chapter_number"]: row for row in report["chapters"]}

            self.assertEqual(by_number[53]["title"], "THE GUEST")
            self.assertEqual(by_number[65]["title"], "THE WARD")
            self.assertEqual(by_number[82]["title"], "THE RECONCILER")
            self.assertTrue(all(row["source_kind"] == "authoritative_docx" for row in by_number.values()))


if __name__ == "__main__":
    unittest.main()
