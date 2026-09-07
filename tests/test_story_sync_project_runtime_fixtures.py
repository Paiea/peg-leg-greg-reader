import json
import unittest
from collections import Counter
from pathlib import Path

from scripts import persistent_act_runtime as runtime


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = ROOT / "state" / "experiments"
MANIFEST_SCHEMA = "persistent_story_trial_manifest/v1"


def _trial_observation(project, label, result):
    evolved = result["evolved_runtime"]
    sync = result["shared_story_sync"]
    local_branches = []
    unresolved_by_act = {}
    for act_id in runtime.ACT_IDS:
        local = evolved["acts"][act_id]["local_state"]
        unresolved_by_act[act_id] = len(local.get("unresolved_questions", []))
        for possibility in local.get("possibilities", []):
            local_branches.append({
                "act": act_id,
                "id": possibility.get("id"),
                "status": possibility.get("status", "active"),
                "viability": possibility.get("viability", "viable"),
            })

    discovery_evidence = {}
    for discovery in evolved["shared_story_state"]["sync_state"].get("discoveries", []):
        discovery_evidence[discovery["id"]] = len(discovery.get("evidence", []))

    modes = Counter(item["experiment_mode"] for item in result.get("rehearsal_targets", []))
    fidelities = Counter(item["fidelity"] for item in result.get("rehearsal_targets", []))
    closure = result.get("constraint_closure", {})
    messages = closure.get("messages", [])

    return {
        "project": project,
        "label": label,
        "authority_effect": result["authority_effect"],
        "active_local_branches": [item for item in local_branches if item["status"] == "active" and item["viability"] not in {"redundant", "invalidated"}],
        "inactive_or_weakened_local_branches": [item for item in local_branches if item not in [branch for branch in local_branches if branch["status"] == "active" and branch["viability"] not in {"redundant", "invalidated"}]],
        "shared_branches_preserved": sync.get("branches_preserved", []),
        "shared_branches_killed": sync.get("branches_killed", []),
        "unresolved_questions_by_act": unresolved_by_act,
        "shared_unresolved_question_count": len(sync.get("unresolved_questions", [])),
        "boundary_contradiction_count": len(result.get("boundary_contradictions", [])),
        "forward_consequence_count": len(evolved["shared_story_state"].get("forward_consequences", [])),
        "backward_requirement_count": len(evolved["shared_story_state"].get("backward_requirements", [])),
        "constraint_status_counts": dict(Counter(item.get("closure_status", "unknown") for item in messages)),
        "constraint_collision_count": len(closure.get("constraint_collisions", [])),
        "repeated_signals": sync.get("repeated_signals", []),
        "strong_threads": sync.get("strong_threads", []),
        "story_truths": sync.get("story_truths", []),
        "discovery_levels": sync.get("discovery_levels", {}),
        "discovery_evidence_counts": discovery_evidence,
        "rehearsal_experiment_modes": dict(modes),
        "rehearsal_fidelities": dict(fidelities),
        "branch_entropy": result.get("branch_entropy", {}),
        "temporal_consistency": result.get("temporal_consistency", {}),
    }


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
                print("PERSISTENT_STORY_TRIAL_OBSERVATION=" + json.dumps(
                    _trial_observation(manifest["project"], "initial", initial),
                    sort_keys=True,
                ))

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
                print("PERSISTENT_STORY_TRIAL_OBSERVATION=" + json.dumps(
                    _trial_observation(manifest["project"], "after_evidence", evolved),
                    sort_keys=True,
                ))


if __name__ == "__main__":
    unittest.main()
