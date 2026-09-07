import json
import unittest
from collections import Counter
from pathlib import Path

from scripts import persistent_act_runtime as runtime
from scripts import plg_ai_tools


ROOT = Path(__file__).resolve().parents[1]
TRIAL = ROOT / "state/experiments/dragon-spotter/persistent-act-runtime"


class DragonSpotterPersistentActRuntimeTests(unittest.TestCase):
    def _load(self, name):
        return json.loads((TRIAL / name).read_text(encoding="utf-8"))

    def test_existing_first_bargain_evidence_moves_the_four_act_runtime_without_canon_write(self):
        state = self._load("runtime-input.json")
        evidence = self._load("first-bargain-evidence.json")
        taste = self._load("creator-taste-context.json")
        before_sync = runtime.sync_shared_story(state)

        # Prove the project through the same public derived-only seam exposed to AI callers.
        result = plg_ai_tools.run_story_rehearsal_cycle({
            "runtime": state,
            "evidence": evidence,
            "creator_taste": taste,
        })

        self.assertEqual("derived_only_no_canon_mutation", result["authority_effect"])
        self.assertEqual(set(runtime.ACT_IDS), set(result["act_packets"]))
        self.assertEqual(4, len([item for item in result["schedule"] if item["kind"] == "baseline_local_search"]))

        # Act IV is a real temporal perspective: its ending hypothesis sends requirements backward.
        act_i = result["act_packets"]["act-i"]
        self.assertTrue(any(item["source_act"] == "act-iv" for item in act_i["incoming_backward_requirements"]))

        # Act I sends first-bargain consequences forward into later temporal perspectives.
        act_iii = result["act_packets"]["act-iii"]
        self.assertTrue(any(item["source_act"] == "act-i" for item in act_iii["incoming_forward_consequences"]))

        # Acts II/III retain an explicit structural bridge and an embodied relationship bridge.
        targets = result["rehearsal_targets"]
        ii_iii = [item for item in targets if item.get("acts") == ["act-ii", "act-iii"]]
        self.assertTrue(any(item.get("dimension") == "professional_role" and item["experiment_mode"] == "state_transition_test" for item in ii_iii))
        self.assertTrue(any(item.get("dimension") == "romantic_trust" and item["experiment_mode"] == "performance" and item["fidelity"] == "high_heat" for item in ii_iii))

        # Cross-act conflicts and long-range messages become explicit experiment targets.
        self.assertTrue(any(item["source_kind"] == "constraint_collision" for item in targets))
        self.assertTrue(any(item["experiment_mode"] == "backward_prerequisite_test" and item["fidelity"] == "probe" for item in targets))
        self.assertTrue(any(item["experiment_mode"] == "forward_consequence_test" and item["fidelity"] == "probe" for item in targets))

        # Existing high-heat evidence compacts into deltas instead of prose or canon writes.
        delta_types = {item["type"] for item in result["applied_deltas"]}
        self.assertIn("local_discovery", delta_types)
        self.assertIn("forward_consequence", delta_types)
        self.assertIn("local_possibility_update", delta_types)
        self.assertIn("shared_discovery_evidence", delta_types)

        # Repeated cross-act evidence strengthens, but does not jump directly to story truth.
        self.assertEqual("repeated_signal", before_sync["discovery_levels"]["mutual-indispensability"])
        self.assertEqual("strong_thread", result["shared_story_sync"]["discovery_levels"]["mutual-indispensability"])
        self.assertNotIn("mutual-indispensability", result["shared_story_sync"]["story_truths"])

        # Creator taste changes search priority only. Branch survival is identical without it.
        without_taste = runtime.sync_shared_story(result["evolved_runtime"])
        with_taste = result["shared_story_sync"]
        no_taste_branch = next(item for item in without_taste["branch_decisions"] if item["id"] == "gift.scale-token")
        taste_branch = next(item for item in with_taste["branch_decisions"] if item["id"] == "gift.scale-token")
        self.assertEqual(no_taste_branch["action"], taste_branch["action"])
        self.assertEqual("low", no_taste_branch.get("search_priority", "low"))
        self.assertEqual("medium", taste_branch["search_priority"])
        self.assertEqual("heuristic_only_no_story_authority", with_taste["creator_taste"]["authority_effect"])

        # Challenge takes can prune local search without pretending the surviving branch is canon.
        entropy = result["branch_entropy"]
        self.assertLess(entropy["after"]["open_branch_count"], entropy["before"]["open_branch_count"])
        self.assertLess(entropy["open_branch_delta"], 0)

        before_mutual = next(item for item in state["shared_story_state"]["sync_state"]["discoveries"] if item["id"] == "mutual-indispensability")
        after_mutual = next(item for item in result["evolved_runtime"]["shared_story_state"]["sync_state"]["discoveries"] if item["id"] == "mutual-indispensability")
        act_i_possibilities = {
            item["id"]: {"status": item.get("status", "active"), "viability": item.get("viability", "viable")}
            for item in result["evolved_runtime"]["acts"]["act-i"]["local_state"]["possibilities"]
        }
        mode_counts = Counter(item["experiment_mode"] for item in targets)
        fidelity_counts = Counter(item["fidelity"] for item in targets)
        collision_statuses = sorted({item["status"] for item in result["constraint_closure"]["constraint_collisions"]})
        new_third_path_deltas = [
            item for item in result["applied_deltas"]
            if item["type"] in {"local_discovery", "shared_discovery"}
            and "third" in json.dumps(item.get("payload", {}), sort_keys=True).lower()
        ]

        observation = {
            "public_entry_point": "plg_ai_tools.run_story_rehearsal_cycle",
            "target_count": len(targets),
            "experiment_mode_counts": dict(sorted(mode_counts.items())),
            "fidelity_counts": dict(sorted(fidelity_counts.items())),
            "act_iv_backward_requirements": len(act_i["incoming_backward_requirements"]),
            "act_i_forward_consequences_into_act_iii": len([item for item in act_iii["incoming_forward_consequences"] if item["source_act"] == "act-i"]),
            "ii_iii_structural_bridges": len([item for item in ii_iii if item.get("dimension") == "professional_role"]),
            "ii_iii_embodied_performance_bridges": len([item for item in ii_iii if item.get("dimension") == "romantic_trust" and item["experiment_mode"] == "performance"]),
            "constraint_collision_targets": len([item for item in targets if item["source_kind"] == "constraint_collision"]),
            "constraint_collision_statuses": collision_statuses,
            "performance_targets": len([item for item in targets if item["experiment_mode"] == "performance"]),
            "probe_targets": len([item for item in targets if item["fidelity"] == "probe"]),
            "mutual_indispensability_before": before_sync["discovery_levels"]["mutual-indispensability"],
            "mutual_indispensability_after": with_taste["discovery_levels"]["mutual-indispensability"],
            "mutual_indispensability_evidence_before": len(before_mutual["evidence"]),
            "mutual_indispensability_evidence_after": len(after_mutual["evidence"]),
            "gift_scale_priority_without_taste": no_taste_branch.get("search_priority", "low"),
            "gift_scale_priority_with_taste": taste_branch["search_priority"],
            "act_i_branch_state": act_i_possibilities,
            "unresolved_contradictions": sorted(with_taste["contradictions_alive"]),
            "new_third_path_discovery_deltas": len(new_third_path_deltas),
            "open_branch_count_before": entropy["before"]["open_branch_count"],
            "open_branch_count_after": entropy["after"]["open_branch_count"],
            "open_branch_delta": entropy["open_branch_delta"],
            "pressure_before": entropy["before"]["pressure_score"],
            "pressure_after": entropy["after"]["pressure_score"],
            "pressure_delta": entropy["pressure_delta"],
            "authority_effect": result["authority_effect"],
        }
        print("DRAGON_SPOTTER_RUNTIME_OBSERVATION=" + json.dumps(observation, sort_keys=True))


if __name__ == "__main__":
    unittest.main()
