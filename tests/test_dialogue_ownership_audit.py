import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from audit_dialogue_ownership import audit_chapters, extract_prose_paragraphs


class DialogueOwnershipAuditTests(unittest.TestCase):
    def test_extract_prose_paragraphs_reads_only_article_prose_and_unescapes_text(self):
        document = (
            '<p>Outside.</p>'
            '<article class="prose">'
            '<p>Before &amp; after.</p>'
            '<figure><img alt="ignored"></figure>'
            '<p>"Doing what?" Rusk pointed.</p>'
            '</article>'
            '<p>Navigation.</p>'
        )
        self.assertEqual(
            extract_prose_paragraphs(document),
            ['Before & after.', '"Doing what?" Rusk pointed.'],
        )

    def test_audit_skips_hidden_canon_and_keeps_showcase_numbers(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            chapters = root / "chapters"
            chapters.mkdir()
            for number, body in (
                (1, '"One?" Rusk pointed.'),
                (2, '"Two?" Rusk pointed.'),
                (3, '"Three?" Rusk pointed.'),
            ):
                (chapters / f"{number:03d}.html").write_text(
                    f'<article class="prose"><p>{body}</p></article>',
                    encoding="utf-8",
                )

            manifest = root / "showcase.json"
            manifest.write_text(
                json.dumps({
                    "version": 1,
                    "mode": "whole_chapter_only",
                    "default": "visible",
                    "chapters": {
                        "2": {"showcase": False, "reason": "pacing"},
                    },
                }),
                encoding="utf-8",
            )

            report = audit_chapters(root, manifest)
            self.assertEqual(report["endpoint"], 3)
            self.assertEqual(report["canonical_chapters"], 3)
            self.assertEqual(report["visible_chapters"], 2)
            self.assertEqual(report["hidden_chapters"], 1)
            self.assertEqual(
                [item["canonical_chapter"] for item in report["candidates"]],
                [1, 3],
            )
            self.assertEqual(
                [item["showcase_chapter"] for item in report["candidates"]],
                [1, 2],
            )

    def test_audit_keeps_neighbor_context_for_cheap_semantic_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            chapters = root / "chapters"
            chapters.mkdir()
            (chapters / "001.html").write_text(
                '<article class="prose">'
                '<p>Previous context.</p>'
                '<p>"Doing what?" Rusk pointed at the sack.</p>'
                '<p>Following context.</p>'
                '</article>',
                encoding="utf-8",
            )
            manifest = root / "showcase.json"
            manifest.write_text(
                json.dumps({
                    "version": 1,
                    "mode": "whole_chapter_only",
                    "default": "visible",
                    "chapters": {},
                }),
                encoding="utf-8",
            )

            report = audit_chapters(root, manifest)
            item = report["candidates"][0]
            self.assertEqual(item["canonical_chapter"], 1)
            self.assertEqual(item["showcase_chapter"], 1)
            self.assertEqual(item["paragraph_index"], 1)
            self.assertEqual(item["previous"], "Previous context.")
            self.assertEqual(item["current"], '"Doing what?" Rusk pointed at the sack.')
            self.assertEqual(item["following"], "Following context.")
            self.assertTrue(item["fingerprint"])


if __name__ == "__main__":
    unittest.main()
