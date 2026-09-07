import json
import unittest
from collections import Counter
from pathlib import Path

from scripts import plg_ai_tools


ROOT = Path(__file__).resolve().parents[1]
TRIAL = ROOT / "state/experiments/dragon-spotter/persistent-act-runtime"


class DragonSpotterPersistentActRuntimeCycle2Tests(unittest.TestCase):
    def _load(self, name):
        return json.loads((TRIAL / name).read_text(encoding="utf-8"))

    def test_cycle_2_closes_evidenced_directional_constraints_without_inventing_story(self):
        state = self._load("runtime-input.json")
        first_bargain = self._load("first-bargain-evidence.json")
        directional = self._load("cycle-2-directional-evidence.json")
        taste = self._load("creator-taste-context.json")

        cycle_1 = plg_ai_tools.run_story_rehearsal_cycle({
            "runtime": state,
            "evidence": first_bargain,
            "creator_taste": taste,
        })
        cycle_2 = plg_ai_tools.run_story_rehearsal_cycle({
            "runtime": cycle_1["evolved_runtime"],
            "evidence": directional,
            "creator_taste": taste,
        })

        self.assertEqual("derived_only_no_canon_mutation", cycle_2["authority_effect"])
        self.assertEqual({"constraint_response"}, {item["type"] for item in cycle_2["applied_deltas"]})
        self.assertEqual(4, len(cycle_2["applied_deltas"]))

        before_temporal = cycle_1["temporal_consistency"]
        after_temporal = cycle_2["temporal_consistency"]
        self.assertEqual(5, before_temporal["unresolved_message_count"])
        self.assertEqual(1, after_temporal["unresolved_message_count"])
        self.assertEqual(1, before_temporal["constraint_collision_count"])
        self.assertEqual(0, after_temporal["constraint_collision_count"])
        self.assertLess(after_temporal["open_pressure_count"], before_temporal["open_pressure_count"])

        # This cycle is directional closure only. It must not prune branches or create discoveries.
        self.assertEqual(0, cycle_2["branch_entropy"]["open_branch_delta"])
        self.assertEqual(
            cycle_1["branch_entropy"]["after"]["open_branch_count"],
            cycle_2["branch_entropy"]["after"]["open_branch_count"],
        )
        self.assertEqual(
            cycle_1["shared_story_sync"]["discovery_levels"],
            cycle_2["shared_story_sync"]["discovery_levels"],
        )
        self.assertEqual([], cycle_2["shared_story_sync"]["story_truths"])

        closure = {item["id"]: item["closure_status"] for item in cycle_2["constraint_closure"]["messages"]}
        for message_id in (
            "a1-to-a3-reciprocity-politics",
            "first-bargain-reciprocity-forward",
            "a4-to-a1-earned-recognition",
            "a4-to-a2-public-risk",
        ):
            self.assertEqual("supported", closure[message_id])
        self.assertEqual("untested", closure["a1-to-a4-earned-recognition"])

        supported_ids = {message_id for message_id, status in closure.items() if status == "supported"}
        still_scheduled = [
            item for item in cycle_2["rehearsal_targets"]
            if item["source_id"] in supported_ids
            and item["experiment_mode"] in {"forward_consequence_test", "backward_prerequisite_test"}
        ]
        modes = Counter(item["experiment_mode"] for item in cycle_2["rehearsal_targets"])

        observation = {
            "public_entry_point": "plg_ai_tools.run_story_rehearsal_cycle",
            "cycle": 2,
            "applied_delta_type_counts": dict(Counter(item["type"] for item in cycle_2["applied_deltas"])),
            "directional_messages_supported": sorted(supported_ids),
            "unresolved_messages_before": before_temporal["unresolved_message_count"],
            "unresolved_messages_after": after_temporal["unresolved_message_count"],
            "constraint_collisions_before": before_temporal["constraint_collision_count"],
            "constraint_collisions_after": after_temporal["constraint_collision_count"],
            "temporal_pressure_before": before_temporal["open_pressure_count"],
            "temporal_pressure_after": after_temporal["open_pressure_count"],
            "branch_open_count": cycle_2["branch_entropy"]["after"]["open_branch_count"],
            "branch_open_delta": cycle_2["branch_entropy"]["open_branch_delta"],
            "branch_pressure_delta": cycle_2["branch_entropy"]["pressure_delta"],
            "boundary_contradiction_count": len(cycle_2["boundary_contradictions"]),
            "strong_threads": sorted(cycle_2["shared_story_sync"]["strong_threads"]),
            "repeated_signals": sorted(cycle_2["shared_story_sync"]["repeated_signals"]),
            "story_truths": sorted(cycle_2["shared_story_sync"]["story_truths"]),
            "target_count": len(cycle_2["rehearsal_targets"]),
            "experiment_mode_counts": dict(sorted(modes.items())),
            "supported_directional_targets_still_scheduled": [item["source_id"] for item in still_scheduled],
            "authority_effect": cycle_2["authority_effect"],
        }
        print("DRAGON_SPOTTER_RUNTIME_CYCLE_2_OBSERVATION=" + json.dumps(observation, sort_keys=True))


if __name__ == "__main__":
    unittest.main()
