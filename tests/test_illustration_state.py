from pathlib import Path
import tempfile
import unittest

from scripts.illustration_state import (
    load_registry,
    load_scene_candidates,
    validate_registry,
    validate_scene_candidates,
)


class SceneCandidateStateTests(unittest.TestCase):
    def valid_candidate(self):
        return {
            "id": "ch090-chair-floor",
            "chapter": 90,
            "chapter_title": "Example",
            "scene_summary": "Greg negotiates around a stubborn piece of furniture.",
            "visual_hook": "Chair, doorway, and bodies angled around a cramped floor.",
            "characters": ["Greg"],
            "location": "shop",
            "mood": "dryly comic",
            "priority": "high",
            "kind": "chapter_illustration",
            "fit_target": "close_enough",
            "spoiler_level": "low",
            "status": "candidate",
        }

    def test_valid_scene_candidate(self):
        validate_scene_candidates([self.valid_candidate()])

    def test_duplicate_scene_candidate_ids_fail(self):
        record = self.valid_candidate()
        with self.assertRaisesRegex(ValueError, "duplicate scene candidate id"):
            validate_scene_candidates([record, dict(record)])

    def test_invalid_scene_candidate_enums_fail(self):
        fields = {
            "priority": "urgent",
            "kind": "wallpaper",
            "fit_target": "perfect",
            "status": "maybe",
            "spoiler_level": "catastrophic",
        }
        for field, value in fields.items():
            with self.subTest(field=field):
                record = self.valid_candidate()
                record[field] = value
                with self.assertRaises(ValueError):
                    validate_scene_candidates([record])

    def test_scene_candidate_requires_summary_and_visual_hook(self):
        for field in ("scene_summary", "visual_hook"):
            with self.subTest(field=field):
                record = self.valid_candidate()
                record[field] = ""
                with self.assertRaisesRegex(ValueError, field):
                    validate_scene_candidates([record])

    def test_load_scene_candidates_requires_json_list(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "candidates.json"
            path.write_text('{"not": "a list"}', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "JSON list"):
                load_scene_candidates(path)


class IllustrationRegistryStateTests(unittest.TestCase):
    def valid_registry_record(self):
        return {
            "id": "art-ch090-chair-floor-v1",
            "candidate_id": "ch090-chair-floor",
            "chapter": 90,
            "kind": "chapter_illustration",
            "status": "queued",
            "style_family": "sketch-ink-paint",
            "source_asset": "",
            "live_asset": "",
            "caption": "",
            "alt_text": "",
            "approved_fit": "close_enough",
            "prompt_pack": "state/visual/prompt-packs/ch090-chair-floor.md",
        }

    def test_valid_queued_registry_record(self):
        validate_registry([self.valid_registry_record()])

    def test_duplicate_registry_ids_fail(self):
        record = self.valid_registry_record()
        with self.assertRaisesRegex(ValueError, "duplicate illustration id"):
            validate_registry([record, dict(record)])

    def test_invalid_registry_status_fails(self):
        record = self.valid_registry_record()
        record["status"] = "candidate"
        with self.assertRaisesRegex(ValueError, "status"):
            validate_registry([record])

    def test_approved_and_live_records_require_alt_text(self):
        for status in ("approved", "live"):
            with self.subTest(status=status):
                record = self.valid_registry_record()
                record["status"] = status
                record["source_asset"] = "visual/chapter_art/090/example.webp"
                record["live_asset"] = "visual/chapter_art/090/example.webp"
                with self.assertRaisesRegex(ValueError, "alt_text"):
                    validate_registry([record])

    def test_live_record_asset_must_exist_when_root_is_supplied(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            record = self.valid_registry_record()
            record["status"] = "live"
            record["alt_text"] = "Greg beside a chair in a cramped shop doorway."
            record["live_asset"] = "visual/chapter_art/090/missing.webp"
            with self.assertRaisesRegex(ValueError, "live_asset"):
                validate_registry([record], root=Path(temp_dir))

    def test_load_registry_requires_json_list(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "registry.json"
            path.write_text('{"not": "a list"}', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "JSON list"):
                load_registry(path)


if __name__ == "__main__":
    unittest.main()
