import hashlib
import json
import struct
import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.project_audit import (
    chapter_art_coverage,
    detect_manuscript_ranges,
    inventory_images,
    inventory_repository,
)


def write_png(path: Path, width: int, height: int, payload: bytes = b"") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + struct.pack(">I", 13)
        + b"IHDR"
        + struct.pack(">II", width, height)
        + b"\x08\x02\x00\x00\x00"
        + payload
    )


class RepositoryInventoryTests(unittest.TestCase):
    def test_inventory_records_paths_sizes_hashes_references_and_categories(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "AGENTS.md").write_text("Read state/PROJECT_STATE.md", encoding="utf-8")
            (root / "state").mkdir()
            (root / "state" / "PROJECT_STATE.md").write_text("authority", encoding="utf-8")
            (root / "chapters").mkdir()
            (root / "chapters" / "001.html").write_text(
                '<img src="../visual/chapter_art/001/a.png">', encoding="utf-8"
            )
            write_png(root / "visual/chapter_art/001/a.png", 800, 600)
            rows = inventory_repository(root)
            by_path = {row["path"]: row for row in rows["files"]}
            self.assertEqual(by_path["AGENTS.md"]["category"], "ACTIVE_AUTHORITY")
            self.assertEqual(by_path["chapters/001.html"]["category"], "GENERATED")
            self.assertIn("chapters/001.html", by_path["visual/chapter_art/001/a.png"]["referenced_by"])
            self.assertEqual(
                by_path["state/PROJECT_STATE.md"]["sha256"],
                hashlib.sha256(b"authority").hexdigest(),
            )

    def test_inventory_excludes_its_generated_outputs_for_determinism(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("reader", encoding="utf-8")
            first = inventory_repository(root)
            output = root / "publishing/repository_inventory.json"
            output.parent.mkdir()
            output.write_text(json.dumps(first), encoding="utf-8")
            self.assertEqual(first, inventory_repository(root))

    def test_manuscript_ranges_come_from_headings_not_filenames(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manuscript = root / "state/manuscript/Peg_Leg_Greg_Running_Manuscript.md"
            manuscript.parent.mkdir(parents=True)
            manuscript.write_text(
                "# CHAPTER 220\n## ONE\ntext\n# CHAPTER 222\n## THREE\ntext",
                encoding="utf-8",
            )
            rows = detect_manuscript_ranges(root)
            self.assertEqual(rows[0]["chapters"], [220, 222])
            self.assertEqual(rows[0]["missing_within_range"], [221])
            self.assertEqual(rows[0]["range"], "220-222")

    def test_manuscript_ranges_are_extracted_from_docx_xml(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manuscript = root / "state/manuscript/Book.docx"
            manuscript.parent.mkdir(parents=True)
            document_xml = (
                '<?xml version="1.0" encoding="UTF-8"?>'
                '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
                '<w:body><w:p><w:r><w:t>CHAPTER EIGHTY-THREE</w:t></w:r><w:r><w:t>THE ARRIVAL</w:t></w:r></w:p>'
                '<w:p><w:r><w:t>Text</w:t></w:r></w:p>'
                '<w:p><w:r><w:t>CHAPTER 84</w:t></w:r></w:p></w:body></w:document>'
            )
            with zipfile.ZipFile(manuscript, "w") as archive:
                archive.writestr("word/document.xml", document_xml)
            rows = detect_manuscript_ranges(root)
            self.assertEqual(rows[0]["chapters"], [83, 84])
            self.assertEqual(rows[0]["range"], "83-84")


class ImageInventoryTests(unittest.TestCase):
    def test_images_include_dimensions_references_duplicate_and_quality_flags(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            chapter = root / "chapters/001.html"
            chapter.parent.mkdir(parents=True)
            chapter.write_text(
                '<figure><img src="../visual/chapter_art/001/a.png" alt="A" loading="lazy">'
                '<img src="../visual/chapter_art/001/missing.png"></figure>',
                encoding="utf-8",
            )
            write_png(root / "visual/chapter_art/001/a.png", 320, 200, b"same")
            write_png(root / "visual/development/a-copy.png", 320, 200, b"same")
            images = inventory_images(root)
            by_path = {row["asset_path"]: row for row in images}
            self.assertEqual(by_path["visual/chapter_art/001/a.png"]["width"], 320)
            self.assertEqual(by_path["visual/chapter_art/001/a.png"]["chapter"], 1)
            self.assertEqual(by_path["visual/chapter_art/001/a.png"]["status"], "REFERENCED")
            self.assertIn("LOW_RESOLUTION", by_path["visual/chapter_art/001/a.png"]["quality_flags"])
            self.assertEqual(
                by_path["visual/chapter_art/001/a.png"]["duplicate_group"],
                by_path["visual/development/a-copy.png"]["duplicate_group"],
            )
            self.assertEqual(by_path["visual/development/a-copy.png"]["status"], "UNUSED_REVIEW")

    def test_coverage_reports_zero_one_multiple_and_broken_references(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            chapters = root / "chapters"
            chapters.mkdir()
            (chapters / "001.html").write_text(
                '<img src="../visual/chapter_art/001/a.png">', encoding="utf-8"
            )
            (chapters / "002.html").write_text("<p>No art</p>", encoding="utf-8")
            (chapters / "003.html").write_text(
                '<img src="../visual/chapter_art/003/a.png">'
                '<img src="../visual/chapter_art/003/b.png">'
                '<img src="../visual/chapter_art/003/missing.png">',
                encoding="utf-8",
            )
            write_png(root / "visual/chapter_art/001/a.png", 800, 600)
            write_png(root / "visual/chapter_art/003/a.png", 800, 600)
            write_png(root / "visual/chapter_art/003/b.png", 800, 600)
            images = inventory_images(root)
            coverage = chapter_art_coverage(root, images)
            self.assertEqual(coverage["chapters"]["001"]["image_count"], 1)
            self.assertEqual(coverage["chapters"]["002"]["image_count"], 0)
            self.assertEqual(coverage["chapters"]["003"]["image_count"], 2)
            self.assertEqual(coverage["summary"]["no_art"], [2])
            self.assertEqual(
                coverage["broken_references"],
                [{"chapter": 3, "asset_path": "visual/chapter_art/003/missing.png"}],
            )


if __name__ == "__main__":
    unittest.main()
