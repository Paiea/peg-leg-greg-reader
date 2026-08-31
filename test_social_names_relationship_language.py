import re
import unittest
from pathlib import Path

from docx import Document


ROOT = Path(__file__).resolve().parent
BOOK1 = ROOT / "state/manuscript/Peg_Leg_Greg_authoritative_ch82_final_name_map.docx"
BOOK2 = ROOT / "state/manuscript/Peg_Leg_Greg_Book2_Manuscript_Ch83-137.docx"


def manuscript_text(path):
    return "\n".join(paragraph.text for paragraph in Document(path).paragraphs)


class SocialNamesPassTest(unittest.TestCase):
    def test_relationship_specific_transitions_are_present(self):
        book1 = manuscript_text(BOOK1)
        book2 = manuscript_text(BOOK2)

        self.assertIn("Mr. Vale, your appointment is with Master Crenn.", book1)
        self.assertIn("Just Greg!", book1)
        self.assertEqual(book2.count("Aileen"), 1)
        self.assertIn("Pear thief.", book2)

    def test_private_nickname_does_not_leak_backward(self):
        for chapter in range(1, 123):
            html = (ROOT / f"chapters/{chapter:03d}.html").read_text(encoding="utf-8")
            self.assertNotIn("Aileen", html, f"Aileen leaked into Chapter {chapter}")

        chapter_123 = (ROOT / "chapters/123.html").read_text(encoding="utf-8")
        self.assertEqual(chapter_123.count("Aileen"), 1)

    def test_canonical_spellings_and_reader_structure_remain_intact(self):
        combined = manuscript_text(BOOK1) + "\n" + manuscript_text(BOOK2)
        self.assertIsNone(re.search(r"\bLysa\b", combined))
        self.assertIsNone(re.search(r"\bAntonious\b", combined))
        chapter_files = list((ROOT / "chapters").glob("[0-9][0-9][0-9].html"))
        illustrated = [path for path in chapter_files if 1 <= int(path.stem) <= 155]
        previews = [path for path in chapter_files if int(path.stem) >= 220]
        self.assertEqual(len(illustrated), 155)
        self.assertEqual([path.stem for path in sorted(previews)], ["220", "221"])


if __name__ == "__main__":
    unittest.main()
