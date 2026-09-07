import json
import unittest
from pathlib import Path

from scripts import persistent_act_runtime as runtime


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = ROOT / "state" / "experiments"
MANIFEST_SCHEMA = "persistent_story_trial_manifest/v1"


class PersistentStoryProjectFixtureTests(unittest.TestCase):
    def test_declared_project_trials_run_through_generic_runtime(self):
        manifests = sorted(FIXTURE_ROOT.glob("*/persistent-act-runtime/trial-manifest.json"))
        self.assertTrue(manifests, "expected at least one declared persistent story trial")

        for manifest_path in manifests:
            with self.subTest(manifest=manifest_path.as_posix()):
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                self.assertEqual(MANIFEST_SCHEMA, manifest.get("schema"))
                self.assertIsInstance(manifest.get("project"), str)
                fixture_root = manifest_path.parent

                runtime_state = json.loads((fixture_root / manifest["runtime"]).read_text(encoding="utf-8"))
                creator_taste = None
                if manifest.get("creator_taste"):
                    creator_taste = json.loads((fixture_root / manifest["creator_taste"]).read_text(encoding="utf-8"))
                    self.assertEqual(manifest["project"], creator_taste.get("project"))

                expected = manifest.get("expected", {})
                initial_expected = expected.get("initial", {})
                initial = runtime.run_rehearsal_cycle(runtime_state, creator_taste=creator_taste)

                self.assertEqual(expected.get("authority_effect", "derived_only_no_canon_mutation"), initial["authority_effect"])
                self.assertEqual(expected.get("act_count", len(runtime.ACT_IDS)), len(initial["act_packets"]))
                self.assertEqual(set(runtime.ACT_IDS), set(initial["act_packets"]))

                initial_modes = {item["experiment_mode"] for item in initial["rehearsal_targets"]}
                self.assertTrue(set(initial_expected.get("required_experiment_modes", [])).issubset(initial_modes))
                initial_fidelities = {item["fidelity"] for item in initial["rehearsal_targets"]}
                self.assertTrue(set(initial_expected.get("required_fidelities", [])).issubset(initial_fidelities))
                self.assertLessEqual(
                    len(initial["shared_story_sync"].get("story_truths", [])),
                    int(initial_expected.get("max_story_truths", 0)),
                )

                if not manifest.get("evidence"):
                    continue

                evidence = json.loads((fixture_root / manifest["evidence"]).read_text(encoding="utf-8"))
                evolved = runtime.run_rehearsal_cycle(
                    runtime_state,
                    evidence=evidence,
                    creator_taste=creator_taste,
                )
                evolved_expected = expected.get("after_evidence", {})
                self.assertEqual("derived_only_no_canon_mutation", evolved["authority_effect"])
                self.assertLessEqual(
                    len(evolved["shared_story_sync"].get("story_truths", [])),
                    int(evolved_expected.get("max_story_truths", 0)),
                )
                if "max_open_branch_delta" in evolved_expected:
                    self.assertLessEqual(
                        evolved["branch_entropy"]["open_branch_delta"],
                        int(evolved_expected["max_open_branch_delta"]),
                    )
                for discovery_id, expected_level in evolved_expected.get("discovery_levels", {}).items():
                    self.assertEqual(
                        expected_level,
                        evolved["shared_story_sync"]["discovery_levels"].get(discovery_id),
                        discovery_id,
                    )


if __name__ == "__main__":
    unittest.main()
