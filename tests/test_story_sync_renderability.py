import unittest

from scripts import story_renderability as renderability


class StoryRenderabilityTests(unittest.TestCase):
    def _region(self):
        return {
            "id": "act-i:chapter-002",
            "act": "act-i",
            "state_in": {"role": "underqualified-official"},
            "state_in_stability": 0.82,
            "required_movement": "Greg turns observation into one useful bounded action.",
            "movement_confidence": 0.78,
            "character_state": {"greg": "performing confidence while observing carefully"},
            "character_state_confidence": 0.8,
            "incoming_dependencies": [
                {"id": "professional-role", "version": "v12", "stability": 0.85, "required": True},
                {"id": "reader-knowledge", "version": "v4", "stability": 0.9, "required": True},
            ],
            "unresolved_risks": [],
            "remaining_uncertainty": [
                {"id": "local-realization-form", "safe_to_discover_in_prose": True, "description": "Whether realization lands through task, dialogue, or physical observation."},
            ],
            "global_uncertainty": [
                {"id": "act-iii-romance-architecture", "status": "open", "description": "Later relationship shape remains unresolved."},
            ],
        }

    def test_local_region_can_render_while_unrelated_later_story_is_open(self):
        report = renderability.assess_renderability(self._region())
        self.assertEqual("renderability_report/v1", report["schema"])
        self.assertEqual("derived_only", report["authority"])
        self.assertFalse(report["canon_write_authorized"])
        self.assertTrue(report["renderable"])
        self.assertEqual([], report["blockers"])
        self.assertEqual(["act-iii-romance-architecture"], report["ignored_global_uncertainty"])
        self.assertEqual(["local-realization-form"], report["safe_prose_uncertainty"])

    def test_high_probability_local_invalidation_blocks_rendering(self):
        region = self._region()
        region["unresolved_risks"] = [
            {"id": "first-bargain-motive", "invalidation_probability": 0.72, "description": "Likely to change the required causal action."},
        ]
        report = renderability.assess_renderability(region, invalidation_threshold=0.5)
        self.assertFalse(report["renderable"])
        self.assertIn("risk:first-bargain-motive", report["blockers"])

    def test_low_stability_required_dependency_blocks_but_optional_dependency_does_not(self):
        region = self._region()
        region["incoming_dependencies"].append({"id": "local-weather", "version": "v2", "stability": 0.2, "required": False})
        self.assertTrue(renderability.assess_renderability(region)["renderable"])
        region["incoming_dependencies"].append({"id": "mechanic-model", "version": "v7", "stability": 0.35, "required": True})
        report = renderability.assess_renderability(region, stability_threshold=0.6)
        self.assertFalse(report["renderable"])
        self.assertIn("dependency:mechanic-model", report["blockers"])

    def test_missing_or_weak_local_story_contract_blocks(self):
        region = self._region()
        region["movement_confidence"] = 0.4
        report = renderability.assess_renderability(region, stability_threshold=0.6)
        self.assertFalse(report["renderable"])
        self.assertIn("required_movement", report["blockers"])

    def test_capture_dependencies_records_only_exact_used_versions(self):
        deps = renderability.capture_dependencies(self._region())
        self.assertEqual({"professional-role": "v12", "reader-knowledge": "v4"}, deps)

    def test_unrelated_story_change_does_not_stale_candidate(self):
        dependencies = {"professional-role": "v12", "reader-knowledge": "v4"}
        report = renderability.assess_staleness(
            dependencies,
            {"professional-role": "v12", "reader-knowledge": "v4", "act-iii-romance": "v99"},
        )
        self.assertFalse(report["stale"])
        self.assertEqual([], report["changed_dependencies"])

    def test_changed_used_dependency_stales_candidate_precisely(self):
        report = renderability.assess_staleness(
            {"professional-role": "v12", "reader-knowledge": "v4"},
            {"professional-role": "v13", "reader-knowledge": "v4"},
        )
        self.assertTrue(report["stale"])
        self.assertEqual(
            [{"id": "professional-role", "candidate_version": "v12", "current_version": "v13", "reason": "version_changed"}],
            report["changed_dependencies"],
        )

    def test_missing_current_dependency_stales_candidate(self):
        report = renderability.assess_staleness({"geography": "v3"}, {})
        self.assertTrue(report["stale"])
        self.assertEqual("missing_current_dependency", report["changed_dependencies"][0]["reason"])


if __name__ == "__main__":
    unittest.main()
