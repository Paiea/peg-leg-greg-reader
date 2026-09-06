from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.build_character_continuity_report import summarize_character_continuity, render_character_continuity_report
from scripts.intake_generated_illustrations import intake_generated_assets
from scripts.score_character_references import select_character_references
from scripts.tag_registry_characters import tag_registry_characters


class RegistryCharacterTaggingTests(unittest.TestCase):
    def test_tags_accepted_art_from_alt_text_using_known_character_catalog(self):
        catalog = {
            "Greg": {"appearance_notes": "Young Greg."},
            "Lyssa": {"appearance_notes": "Black woman with natural Afro-textured hair."},
            "Nessa": {"appearance_notes": "Nessa."},
        }
        registry = [
            {
                "id": "art-v1",
                "status": "live",
                "alt_text": "Greg and Lyssa lean over the work table.",
                "caption": "",
                "notes": "",
            }
        ]
        tagged, changed = tag_registry_characters(registry, catalog)
        self.assertEqual(changed, 1)
        self.assertEqual(tagged[0]["characters"], ["Greg", "Lyssa"])
        self.assertEqual(tagged[0]["character_tag_source"], "text_metadata")

    def test_does_not_invent_characters_when_text_has_no_known_name(self):
        catalog = {"Greg": {"appearance_notes": "Young Greg."}}
        registry = [{"id": "art-v1", "status": "approved", "alt_text": "A cart under rain."}]
        tagged, changed = tag_registry_characters(registry, catalog)
        self.assertEqual(changed, 0)
        self.assertNotIn("characters", tagged[0])


class RegistryMetadataIntakeTests(unittest.TestCase):
    def test_intake_carries_generation_continuity_metadata_into_registry(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            target = "visual/chapter_art/020/ch020-work-v1.webp"
            path = root / target
            path.parent.mkdir(parents=True)
            path.write_bytes(b"image")
            queue = [
                {
                    "candidate_id": "ch020-work",
                    "chapter": 20,
                    "kind": "chapter_illustration",
                    "fit_target": "exact",
                    "prompt_pack": "state/visual/prompt-packs/ch020-work.md",
                    "paragraph_anchor": "Anchor.",
                    "target_asset": target,
                    "characters": ["Greg", "Lyssa"],
                    "style_family": "sketch-ink-paint",
                    "framing_preference": "above_waist",
                    "camera_angle": "three_quarter",
                    "pose_family": "working_hands",
                    "scene_tags": ["workshop", "table_work"],
                }
            ]
            updated, changed = intake_generated_assets(root, queue, [])
        self.assertEqual(changed, 1)
        record = updated[0]
        self.assertEqual(record["characters"], ["Greg", "Lyssa"])
        self.assertEqual(record["framing_preference"], "above_waist")
        self.assertEqual(record["style_family"], "sketch-ink-paint")
        self.assertEqual(record["camera_angle"], "three_quarter")
        self.assertEqual(record["pose_family"], "working_hands")
        self.assertEqual(record["scene_tags"], ["workshop", "table_work"])


class ReferenceDiversityTests(unittest.TestCase):
    def test_selector_prefers_visual_diversity_over_repeating_same_angle(self):
        catalog = {
            "Greg": {
                "appearance_notes": "Young Greg.",
                "references": [
                    {"asset": "visual/front-a.webp", "status": "live", "approved_fit": "exact", "style_family": "sketch-ink-paint", "tags": ["above_waist"], "view_angle": "front", "pose_family": "portrait"},
                    {"asset": "visual/front-b.webp", "status": "live", "approved_fit": "exact", "style_family": "sketch-ink-paint", "tags": ["above_waist", "strong_face"], "view_angle": "front", "pose_family": "portrait"},
                    {"asset": "visual/three-quarter.webp", "status": "approved", "approved_fit": "exact", "style_family": "sketch-ink-paint", "tags": ["above_waist"], "view_angle": "three_quarter", "pose_family": "working_hands"},
                ],
            }
        }
        selected = select_character_references(
            catalog,
            ["Greg"],
            framing_preference="above_waist",
            limit_per_character=2,
            diversity_aware=True,
        )
        assets = [record["asset"] for record in selected]
        self.assertIn("visual/front-b.webp", assets)
        self.assertIn("visual/three-quarter.webp", assets)
        self.assertEqual(len({record.get("view_angle") for record in selected}), 2)


class SceneAwareReferenceTests(unittest.TestCase):
    def test_selector_rewards_reference_matching_scene_tags(self):
        catalog = {
            "Greg": {
                "appearance_notes": "Young Greg.",
                "references": [
                    {"asset": "visual/theatre.webp", "status": "live", "approved_fit": "exact", "style_family": "sketch-ink-paint", "tags": ["above_waist"], "scene_tags": ["theatre", "backstage"]},
                    {"asset": "visual/workshop.webp", "status": "approved", "approved_fit": "exact", "style_family": "sketch-ink-paint", "tags": ["above_waist"], "scene_tags": ["workshop", "table_work"]},
                ],
            }
        }
        selected = select_character_references(
            catalog,
            ["Greg"],
            framing_preference="above_waist",
            limit_per_character=1,
            scene_context={"scene_tags": ["workshop", "table_work"]},
        )
        self.assertEqual(selected[0]["asset"], "visual/workshop.webp")
        self.assertIn("scene context match", selected[0]["reasons"])


class CharacterContinuityReportTests(unittest.TestCase):
    def test_report_summarizes_reference_strength_diversity_and_greg_framing(self):
        catalog = {
            "Greg": {
                "appearance_notes": "Young Greg.",
                "reference_assets": ["visual/manual.webp"],
                "references": [
                    {"asset": "visual/greg-live.webp", "status": "live", "tags": ["above_waist"], "view_angle": "three_quarter", "pose_family": "working_hands"}
                ],
            },
            "Lyssa": {"appearance_notes": "Lyssa.", "reference_assets": [], "references": []},
        }
        audit_issues = [{"character": "Lyssa", "code": "missing_asset", "asset": "visual/nope.webp"}]
        summary = summarize_character_continuity(catalog, audit_issues)
        self.assertEqual(summary["characters"]["Greg"]["total_references"], 2)
        self.assertEqual(summary["characters"]["Greg"]["above_waist_references"], 1)
        self.assertEqual(summary["characters"]["Greg"]["view_angles"], ["three_quarter"])
        self.assertEqual(summary["characters"]["Lyssa"]["audit_issues"], 1)
        report = render_character_continuity_report(summary)
        self.assertIn("# PEG-LEG GREG — CHARACTER CONTINUITY", report)
        self.assertIn("Greg", report)
        self.assertIn("Above-waist anchors: 1", report)
        self.assertIn("Lyssa", report)


if __name__ == "__main__":
    unittest.main()
