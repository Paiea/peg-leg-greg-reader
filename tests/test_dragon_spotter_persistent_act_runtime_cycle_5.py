import json
import unittest
from pathlib import Path

from scripts import plg_ai_tools

ROOT = Path(__file__).resolve().parents[1]
TRIAL = ROOT / "state/experiments/dragon-spotter/persistent-act-runtime"


class DragonSpotterPersistentActRuntimeCycle5Tests(unittest.TestCase):
    def _load(self, name):
        return json.loads((TRIAL / name).read_text(encoding="utf-8"))

    def test_cycle_5_motivation_explains_remaining_choices_without_reopening_skeleton(self):
        state = self._load("runtime-input.json")
        taste = self._load("creator-taste-context.json")
        evidence_sets = [
            self._load("first-bargain-evidence.json"),
            self._load("cycle-2-directional-evidence.json"),
            self._load("cycle-3-boundary-evidence.json"),
            self._load("cycle-4-adversarial-evidence.json"),
            self._load("cycle-5-motivational-evidence.json"),
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

        cycle_4, cycle_5 = cycles[-2:]
        self.assertEqual("derived_only_no_canon_mutation", cycle_5["authority_effect"])
        self.assertEqual(0, len(cycle_5["boundary_contradictions"]))
        self.assertEqual(0, cycle_5["temporal_consistency"]["unresolved_message_count"])
        self.assertEqual(0, cycle_5["temporal_consistency"]["open_pressure_count"])
        self.assertEqual("candidate_passable", cycle_5["temporal_consistency"]["trajectory_status"])
        self.assertEqual(0, cycle_5["branch_entropy"]["open_branch_delta"])

        levels = cycle_5["shared_story_sync"]["discovery_levels"]
        self.assertEqual("story_truth", levels["mutual-indispensability"])
        self.assertEqual("strong_thread", levels["operational-reliance-before-personal-trust"])
        self.assertEqual("speculation", levels["first-dragon-wants-voluntary-repair"])
        self.assertEqual("speculation", levels["legitimacy-as-usable-authority"])

        # Cycle 5 discovers causal discriminators but does not fake shared branch mutation.
        self.assertIn("first-gift-form", cycle_5["shared_story_sync"]["contradictions_alive"])
        self.assertIn("ending-office-role", cycle_5["shared_story_sync"]["contradictions_alive"])
        self.assertEqual(
            set(cycle_4["shared_story_sync"]["story_truths"]),
            set(cycle_5["shared_story_sync"]["story_truths"]),
        )

        local_act_i = cycle_5["evolved_runtime"]["acts"]["act-i"]["local_state"]["discoveries"]
        local_act_iv = cycle_5["evolved_runtime"]["acts"]["act-iv"]["local_state"]["discoveries"]
        self.assertTrue(any(item.get("id") == "a1.first-dragon-reciprocal-standing" for item in local_act_i))
        self.assertTrue(any(item.get("id") == "a4.legitimacy-as-usable-authority" for item in local_act_iv))
        self.assertTrue(any(item.get("id") == "a4.recognized-cross-polity-mandate" for item in local_act_iv))

        observation = {
            "cycle": 5,
            "target_count_before": len(cycle_4["rehearsal_targets"]),
            "target_count_after": len(cycle_5["rehearsal_targets"]),
            "boundary_contradictions": len(cycle_5["boundary_contradictions"]),
            "unresolved_long_range_messages": cycle_5["temporal_consistency"]["unresolved_message_count"],
            "temporal_pressure": cycle_5["temporal_consistency"]["open_pressure_count"],
            "trajectory_status": cycle_5["temporal_consistency"]["trajectory_status"],
            "open_branch_count": cycle_5["branch_entropy"]["after"]["open_branch_count"],
            "open_branch_delta": cycle_5["branch_entropy"]["open_branch_delta"],
            "story_truths": sorted(cycle_5["shared_story_sync"]["story_truths"]),
            "strong_threads": sorted(cycle_5["shared_story_sync"]["strong_threads"]),
            "repeated_signals": sorted(cycle_5["shared_story_sync"]["repeated_signals"]),
            "motivational_discoveries": {
                "first-dragon-wants-voluntary-repair": levels["first-dragon-wants-voluntary-repair"],
                "legitimacy-as-usable-authority": levels["legitimacy-as-usable-authority"],
            },
            "unresolved_contradictions": sorted(cycle_5["shared_story_sync"]["contradictions_alive"]),
            "new_forward_consequences": len(cycle_5["evolved_runtime"]["shared_story_state"].get("forward_consequences", [])) - len(cycle_4["evolved_runtime"]["shared_story_state"].get("forward_consequences", [])),
            "new_backward_requirements": len(cycle_5["evolved_runtime"]["shared_story_state"].get("backward_requirements", [])) - len(cycle_4["evolved_runtime"]["shared_story_state"].get("backward_requirements", [])),
            "authority_effect": cycle_5["authority_effect"],
        }
        print("DRAGON_SPOTTER_RUNTIME_CYCLE_5_OBSERVATION=" + json.dumps(observation, sort_keys=True))


if __name__ == "__main__":
    unittest.main()
