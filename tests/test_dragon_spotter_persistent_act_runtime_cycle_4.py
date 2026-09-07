import json
import unittest
from pathlib import Path

from scripts import plg_ai_tools

ROOT = Path(__file__).resolve().parents[1]
TRIAL = ROOT / "state/experiments/dragon-spotter/persistent-act-runtime"


class DragonSpotterPersistentActRuntimeCycle4Tests(unittest.TestCase):
    def _load(self, name):
        return json.loads((TRIAL / name).read_text(encoding="utf-8"))

    def test_cycle_4_adversarial_convergence_preserves_honest_uncertainty(self):
        state = self._load("runtime-input.json")
        taste = self._load("creator-taste-context.json")
        evidence_sets = [
            self._load("first-bargain-evidence.json"),
            self._load("cycle-2-directional-evidence.json"),
            self._load("cycle-3-boundary-evidence.json"),
            self._load("cycle-4-adversarial-evidence.json"),
        ]

        cycles = []
        current = state
        for evidence in evidence_sets:
            result = plg_ai_tools.run_story_rehearsal_cycle({
                "runtime": current,
                "evidence": evidence,
                "creator_taste": taste,
            })
            cycles.append(result)
            current = result["evolved_runtime"]

        cycle_3, cycle_4 = cycles[-2:]
        self.assertEqual("derived_only_no_canon_mutation", cycle_4["authority_effect"])
        self.assertEqual(0, len(cycle_4["boundary_contradictions"]))
        self.assertEqual(0, cycle_4["temporal_consistency"]["unresolved_message_count"])
        self.assertEqual(0, cycle_4["temporal_consistency"]["open_pressure_count"])
        self.assertEqual("candidate_passable", cycle_4["temporal_consistency"]["trajectory_status"])

        levels = cycle_4["shared_story_sync"]["discovery_levels"]
        # One support group plus one survived challenge is still one independent support group.
        # Preserve the speculation until another independent positive recurrence exists.
        self.assertEqual("speculation", levels["operational-reliance-before-personal-trust"])
        self.assertEqual("story_truth", levels["mutual-indispensability"])

        relationship_record = next(
            item for item in cycle_4["evolved_runtime"]["shared_story_state"]["sync_state"]["discoveries"]
            if item["id"] == "operational-reliance-before-personal-trust"
        )
        relationship_groups = {item["independent_group"] for item in relationship_record["evidence"]}
        self.assertEqual(2, len(relationship_groups))

        # Cycle 4 is adversarial convergence, not forced branch collapse.
        self.assertEqual(0, cycle_4["branch_entropy"]["open_branch_delta"])
        self.assertIn("first-gift-form", cycle_4["shared_story_sync"]["contradictions_alive"])
        self.assertIn("ending-office-role", cycle_4["shared_story_sync"]["contradictions_alive"])

        observation = {
            "cycle": 4,
            "target_count_before": len(cycle_3["rehearsal_targets"]),
            "target_count_after": len(cycle_4["rehearsal_targets"]),
            "boundary_contradictions": len(cycle_4["boundary_contradictions"]),
            "unresolved_long_range_messages": cycle_4["temporal_consistency"]["unresolved_message_count"],
            "temporal_pressure": cycle_4["temporal_consistency"]["open_pressure_count"],
            "trajectory_status": cycle_4["temporal_consistency"]["trajectory_status"],
            "open_branch_count": cycle_4["branch_entropy"]["after"]["open_branch_count"],
            "open_branch_delta": cycle_4["branch_entropy"]["open_branch_delta"],
            "story_truths": sorted(cycle_4["shared_story_sync"]["story_truths"]),
            "strong_threads": sorted(cycle_4["shared_story_sync"]["strong_threads"]),
            "repeated_signals": sorted(cycle_4["shared_story_sync"]["repeated_signals"]),
            "relationship_third_path_evidence_groups": len(relationship_groups),
            "relationship_third_path_maturity": levels["operational-reliance-before-personal-trust"],
            "unresolved_contradictions": sorted(cycle_4["shared_story_sync"]["contradictions_alive"]),
            "new_forward_consequences": len(cycle_4["evolved_runtime"]["shared_story_state"].get("forward_consequences", [])) - len(cycle_3["evolved_runtime"]["shared_story_state"].get("forward_consequences", [])),
            "new_backward_requirements": len(cycle_4["evolved_runtime"]["shared_story_state"].get("backward_requirements", [])) - len(cycle_3["evolved_runtime"]["shared_story_state"].get("backward_requirements", [])),
            "authority_effect": cycle_4["authority_effect"],
        }
        print("DRAGON_SPOTTER_RUNTIME_CYCLE_4_OBSERVATION=" + json.dumps(observation, sort_keys=True))


if __name__ == "__main__":
    unittest.main()
