import html
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent


class Chapter152SyncTests(unittest.TestCase):
    def test_reader_publishes_complete_supplied_forward_range(self):
        expected = {
            138: "THE SHOPKEEPER",
            139: "THE BASELINE",
            140: "THE TRAVELER",
            141: "THE PACKER",
            142: "THE PASSENGER",
            143: "THE STOP",
            144: "THE STABLE",
            145: "THE ARRIVAL",
            146: "THE HAND",
            147: "THE REHEARSAL",
            148: "THE ROOF",
            149: "THE AUDIENCE",
            150: "THE WORK",
            151: "THE SHOW",
            152: "THE SECOND SHOW",
        }
        for number, title in expected.items():
            page = ROOT / "chapters" / f"{number:03}.html"
            self.assertTrue(page.is_file(), page)
            document = page.read_text(encoding="utf-8")
            self.assertIn(f"CHAPTER {number}", document)
            self.assertIn(f"<h1>{title}</h1>", document)
            self.assertIn(f'href="{number - 1:03}.html"', document)
            if number < 152:
                self.assertIn(f'href="{number + 1:03}.html"', document)
            else:
                self.assertNotIn("Next Chapter", document)

    def test_reader_preserves_forward_prose_without_editing(self):
        source = (ROOT / "state" / "manuscript" / "Peg_Leg_Greg_Running_Manuscript_Ch138-152.md").read_text(encoding="utf-8")
        for number in range(138, 153):
            start = source.index(f"# CHAPTER {number}")
            end = source.find(f"# CHAPTER {number + 1}", start)
            block = source[start : end if end >= 0 else None]
            source_paragraphs = []
            for paragraph in re.split(r"\n\s*\n", block):
                text = " ".join(line.strip() for line in paragraph.splitlines()).strip()
                if not text or text.startswith("#") or set(text) == {"-"}:
                    continue
                source_paragraphs.append(text)
            document = (ROOT / "chapters" / f"{number:03}.html").read_text(encoding="utf-8")
            for paragraph in source_paragraphs:
                self.assertIn(f"<p>{html.escape(paragraph, quote=False)}</p>", document)

    def test_index_and_endpoint_metadata_reach_147(self):
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="chapters/152.html"', index)
        self.assertIn('<span class="title">The Second Show</span>', index)
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Chapters 1–152", readme)
        self.assertIn("Chapter 152 — THE SECOND SHOW", readme)


if __name__ == "__main__":
    unittest.main()
