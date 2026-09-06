from __future__ import annotations

import tempfile
from pathlib import Path
import unittest

from scripts.import_legacy_illustrations import bootstrap_legacy_registry
from scripts.promote_illustrations import promote_html
from scripts.report_illustration_coverage import assert_no_unmanaged_live_art


class LegacyRegistryBootstrapTests(unittest.TestCase):
    def test_empty_registry_bootstraps_existing_live_chapter_art_once(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            chapter_dir = root / "chapters"
            asset = root / "visual" / "chapter_art" / "010" / "old.webp"
            chapter_dir.mkdir(parents=True)
            asset.parent.mkdir(parents=True)
            asset.write_bytes(b"RIFFlegacyWEBP")
            (chapter_dir / "010.html").write_text(
                '<article class="prose"><p>Before.</p><figure class="chapter-art"><img src="../visual/chapter_art/010/old.webp" alt="Greg crossing a yard."/><figcaption>Old accepted art.</figcaption></figure><p>After.</p></article>',
                encoding="utf-8",
            )

            records = bootstrap_legacy_registry(root, chapter_dir, [])
            self.assertEqual(len(records), 1)
            record = records[0]
            self.assertEqual(record["chapter"], 10)
            self.assertEqual(record["status"], "live")
            self.assertEqual(record["live_asset"], "visual/chapter_art/010/old.webp")
            self.assertEqual(record["alt_text"], "Greg crossing a yard.")
            self.assertEqual(record["caption"], "Old accepted art.")
            self.assertEqual(record["style_family"], "legacy-import")

    def test_nonempty_registry_does_not_auto_import_future_unmanaged_art(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            chapter_dir = root / "chapters"
            chapter_dir.mkdir(parents=True)
            (chapter_dir / "011.html").write_text(
                '<figure class="chapter-art"><img src="../visual/chapter_art/011/new.webp" alt="New art."/></figure>',
                encoding="utf-8",
            )
            existing = [{"id": "legacy-existing", "status": "live", "live_asset": "visual/chapter_art/010/old.webp"}]
            self.assertEqual(bootstrap_legacy_registry(root, chapter_dir, existing), existing)


class IllustrationPromotionTests(unittest.TestCase):
    def approved_record(self):
        return {
            "id": "art-ch392-glass-mice-v1",
            "candidate_id": "ch392-glass-mice",
            "chapter": 392,
            "kind": "chapter_illustration",
            "status": "approved",
            "style_family": "sketch-ink-paint",
            "source_asset": "visual/chapter_art/392/Ch392_glass_mice.webp",
            "live_asset": "visual/chapter_art/392/Ch392_glass_mice.webp",
            "caption": "Glass mice test the camp food box.",
            "alt_text": "Three gray glass mice with faint blue-white teeth investigate the camp food box while Greg watches from beside the fire ring.",
            "approved_fit": "exact",
            "prompt_pack": "state/visual/prompt-packs/ch392-glass-mice.md",
            "paragraph_anchor": "Glass mice.",
        }

    def test_promotion_inserts_one_figure_after_exact_anchor_and_preserves_other_html(self):
        source = '<article class="prose"><p>Before.</p>\n<p>Glass mice.</p>\n<p>After.</p></article>'
        updated = promote_html(source, self.approved_record())
        expected_prefix = '<article class="prose"><p>Before.</p>\n<p>Glass mice.</p>'
        self.assertTrue(updated.startswith(expected_prefix))
        self.assertIn('class="chapter-art"', updated)
        self.assertIn('../visual/chapter_art/392/Ch392_glass_mice.webp', updated)
        self.assertIn('alt="Three gray glass mice with faint blue-white teeth investigate the camp food box while Greg watches from beside the fire ring."', updated)
        self.assertTrue(updated.endswith('\n<p>After.</p></article>'))
        self.assertEqual(updated.count('class="chapter-art"'), 1)

    def test_promotion_refuses_ambiguous_anchor(self):
        source = '<article class="prose"><p>Glass mice.</p><p>Other.</p><p>Glass mice.</p></article>'
        with self.assertRaisesRegex(ValueError, "exactly once"):
            promote_html(source, self.approved_record())

    def test_promotion_requires_approved_status(self):
        record = self.approved_record()
        record["status"] = "generated"
        with self.assertRaisesRegex(ValueError, "approved"):
            promote_html('<article class="prose"><p>Glass mice.</p></article>', record)


class RegistryFirstEnforcementTests(unittest.TestCase):
    def test_strict_registry_check_rejects_unmanaged_live_art(self):
        with self.assertRaisesRegex(ValueError, "unmanaged live art"):
            assert_no_unmanaged_live_art(["visual/chapter_art/999/unregistered.webp"])

    def test_strict_registry_check_accepts_clean_reader(self):
        assert_no_unmanaged_live_art([])


if __name__ == "__main__":
    unittest.main()
