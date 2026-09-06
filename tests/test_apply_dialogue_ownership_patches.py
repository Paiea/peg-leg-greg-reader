from pathlib import Path
import json
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from apply_dialogue_ownership_patches import apply_manifest


class DialogueOwnershipPatchTests(unittest.TestCase):
    def test_exact_patch_can_split_one_paragraph_into_multiple_owner_paragraphs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            chapters = root / "chapters"
            chapters.mkdir()
            (chapters / "002.html").write_text(
                '<html><article class="prose"><p>Before.</p>'
                '<p>"Fine." He counted silver onto the desk. I should have felt relief.</p>'
                '<p>After.</p></article></html>',
                encoding="utf-8",
            )
            manifest = root / "patches.json"
            manifest.write_text(json.dumps({
                "version": 1,
                "patches": [{
                    "chapter": 2,
                    "label": "split Greg from Antonius and Greg reaction",
                    "current": ['"Fine." He counted silver onto the desk. I should have felt relief.'],
                    "replacement": [
                        '"Fine."',
                        'Antonius counted silver onto the desk.',
                        'I should have felt relief.',
                    ],
                }],
            }), encoding="utf-8")

            stats = apply_manifest(manifest, chapters)
            text = (chapters / "002.html").read_text(encoding="utf-8")
            self.assertEqual(stats["applied"], 1)
            self.assertIn('<p>"Fine."</p><p>Antonius counted silver onto the desk.</p><p>I should have felt relief.</p>', text)
            self.assertIn('<p>Before.</p>', text)
            self.assertIn('<p>After.</p>', text)

    def test_exact_patch_is_idempotent_when_replacement_already_present(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            chapters = root / "chapters"
            chapters.mkdir()
            (chapters / "003.html").write_text(
                '<article class="prose"><p>"What?" Arlo asked.</p><p>Arlo held out his hand.</p></article>',
                encoding="utf-8",
            )
            manifest = root / "patches.json"
            manifest.write_text(json.dumps({
                "version": 1,
                "patches": [{
                    "chapter": 3,
                    "label": "stale Arlo attribution",
                    "current": ['"What?" Antonius asked. "Other people\'s." Antonius held out his hand.'],
                    "replacement": ['"What?" Arlo asked.', 'Arlo held out his hand.'],
                }],
            }), encoding="utf-8")

            stats = apply_manifest(manifest, chapters)
            self.assertEqual(stats["already"], 1)
            self.assertEqual(stats["applied"], 0)

    def test_exact_patch_fails_if_current_text_is_not_unique(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            chapters = root / "chapters"
            chapters.mkdir()
            (chapters / "004.html").write_text(
                '<article class="prose"><p>Same.</p><p>Same.</p></article>',
                encoding="utf-8",
            )
            manifest = root / "patches.json"
            manifest.write_text(json.dumps({
                "version": 1,
                "patches": [{
                    "chapter": 4,
                    "label": "ambiguous",
                    "current": ["Same."],
                    "replacement": ["Changed."],
                }],
            }), encoding="utf-8")

            with self.assertRaises(RuntimeError):
                apply_manifest(manifest, chapters)

    def test_only_manifest_chapter_is_modified(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            chapters = root / "chapters"
            chapters.mkdir()
            for number in (1, 2):
                (chapters / f"{number:03d}.html").write_text(
                    '<article class="prose"><p>Keep.</p></article>',
                    encoding="utf-8",
                )
            manifest = root / "patches.json"
            manifest.write_text(json.dumps({
                "version": 1,
                "patches": [{
                    "chapter": 2,
                    "label": "chapter scoped",
                    "current": ["Keep."],
                    "replacement": ["Changed."],
                }],
            }), encoding="utf-8")

            apply_manifest(manifest, chapters)
            self.assertIn('Keep.', (chapters / "001.html").read_text(encoding="utf-8"))
            self.assertIn('Changed.', (chapters / "002.html").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
