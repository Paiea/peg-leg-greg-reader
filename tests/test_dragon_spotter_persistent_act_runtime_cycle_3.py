import json
import unittest
from collections import Counter
from pathlib import Path

from scripts import persistent_act_runtime as runtime
from scripts import plg_ai_tools


ROOT = Path(__file__).resolve().parents[1]
TRIAL = ROOT / "state/experiments/dragon-spotter/persistent-act-runtime"
PERFORMANCE = ROOT / "state/experiments/dragon-spotter/story-sync/cycle-3-romantic-trust-performance.json"


class DragonSpotterPersistentActRuntimeCycle3Tests(unittest.TestCase):
    def _load(self, path):
        return json.loads(path.read_text(encoding="utf-8"))

    def test_cycle_3_boundary_rehearsals_adapt_the_later_state_from_observed_behavior(self):
        state = self._load(TRIAL / "runtime-input.json")
        first_bargain = self._load(TRIAL / "first-bargain-evidence.json")
        cycle_2_evidence = self._load(TRIAL / "cycle-2-directional-evidence.json")
        cycle_3_evidence = self._load(TRIAL / "cycle-3-boundary-evidence.json")
        taste = self._load(TRIAL / "creator-taste-context.json")
        performance = self._load(PERFORMANCE)

        self.assertEqual("derived_experimental_not_story_canon", performance["authority"])
        self.assertEqual("high", performance["heat"])
        self.assertEqual(
            "third_path_operational_reliance_with_guarded_personal_trust",
            performance["comparison"]["observed_relationship_result"],
        )
        self.assertTrue(any(take["outcome_class"] == "deeper_conflict" for take in performance["takes"]))
        self.assertTrue(any(take["outcome_class"] == "asymmetric_reliance" for take in performance["takes"]))
        self.assertTrue(any(take["outcome_class"] == "increased_attraction_persistent_distrust" for take in performance["takes"]))

        cycle_1 = plg_ai_tools.run_story_rehearsal_cycle({
            "runtime": state,
            "evidence": first_bargain,
            "creator_taste": taste,
        })
        cycle_2 = plg_ai_tools.run_story_rehearsal_cycle({
            "runtime": cycle_1["evolved_runtime"],
            "evidence": cycle_2_evidence,
            "creator_taste": taste,
        })
        cycle_3 = plg_ai_tools.run_story_rehearsal_cycle({
            "runtime": cycle_2["evolved_runtime"],
            "evidence": cycle_3_evidence,
            "creator_taste": taste,
        })

        self.assertEqual("derived_only_no_canon_mutation", cycle_3["authority_effect"])

        # PERFORMANCE contradicted the broad Act III relationship hypothesis. Preserve the
        # observed third path by adapting the derived boundary hypothesis rather than forcing
        # the preferred value or mutating canon.
        act_iii_romantic = next(
            item for item in cycle_3["evolved_runtime"]["acts"]["act-iii"]["state_in"]
            if item["id"] == "a3-in-romantic-trust"
        )
        self.assertEqual(
            "mutual-operational-reliance-with-guarded-personal-trust",
            act_iii_romantic["value"],
        )
        self.assertTrue(act_iii_romantic.get("history"))
        self.assertEqual("mutual-reliance", act_iii_romantic["history"][-1]["value"])

        # All three tested temporal boundaries have evidence-backed bridges after the revised
        # relationship state is integrated. Different endpoint values remain valid temporal
        # states and should not be repeatedly scheduled as contradictions once the bridge is supported.
        self.assertEqual(0, len(cycle_3["boundary_contradictions"]))
        boundary_target_ids = {
            item["source_id"]
            for item in cycle_3["rehearsal_targets"]
            if item["source_kind"] == "boundary_contradiction"
        }
        self.assertFalse(boundary_target_ids)

        # The last open long-range recognition consequence is answered by the structural
        # public-identity rehearsal, so temporal pressure can fall without branch pruning.
        closure = {item["id"]: item["closure_status"] for item in cycle_3["constraint_closure"]["messages"]}
        self.assertEqual("supported", closure["a1-to-a4-earned-recognition"])
        self.assertEqual(0, cycle_3["temporal_consistency"]["unresolved_message_count"])
        self.assertEqual(0, cycle_3["temporal_consistency"]["constraint_collision_count"])
        self.assertEqual(0, cycle_3["temporal_consistency"]["open_pressure_count"])
        self.assertEqual("candidate_passable", cycle_3["temporal_consistency"]["trajectory_status"])

        # The high-heat experiment is genuinely independent. Let STORY SYNC classify what
        # that evidence earns instead of freezing Cycle 2 maturity by expectation.
        levels = cycle_3["shared_story_sync"]["discovery_levels"]
        self.assertEqual("story_truth", levels["mutual-indispensability"])
        self.assertEqual("strong_thread", levels["heat-through-competence"])
        self.assertEqual("speculation", levels["operational-reliance-before-personal-trust"])

        # This cycle did not resolve the gift or ending-office branch choices by force.
        self.assertEqual(0, cycle_3["branch_entropy"]["open_branch_delta"])
        self.assertIn("first-gift-form", cycle_3["shared_story_sync"]["contradictions_alive"])
        self.assertIn("ending-office-role", cycle_3["shared_story_sync"]["contradictions_alive"])

        modes = Counter(item["experiment_mode"] for item in cycle_3["rehearsal_targets"])
        observation = {
            "public_entry_point": "plg_ai_tools.run_story_rehearsal_cycle",
            "cycle": 3,
            "performance_result": performance["comparison"]["observed_relationship_result"],
            "act_iii_romantic_trust_after": act_iii_romantic["value"],
            "boundary_contradictions_before": len(cycle_2["boundary_contradictions"]),
            "boundary_contradictions_after": len(cycle_3["boundary_contradictions"]),
            "temporal_pressure_before": cycle_2["temporal_consistency"]["open_pressure_count"],
            "temporal_pressure_after": cycle_3["temporal_consistency"]["open_pressure_count"],
            "unresolved_messages_before": cycle_2["temporal_consistency"]["unresolved_message_count"],
            "unresolved_messages_after": cycle_3["temporal_consistency"]["unresolved_message_count"],
            "target_count_before": len(cycle_2["rehearsal_targets"]),
            "target_count_after": len(cycle_3["rehearsal_targets"]),
            "experiment_mode_counts_after": dict(sorted(modes.items())),
            "open_branch_count_before": cycle_2["branch_entropy"]["after"]["open_branch_count"],
            "open_branch_count_after": cycle_3["branch_entropy"]["after"]["open_branch_count"],
            "open_branch_delta": cycle_3["branch_entropy"]["open_branch_delta"],
            "discovery_levels": {
                key: levels[key]
                for key in (
                    "mutual-indispensability",
                    "heat-through-competence",
                    "operational-reliance-before-personal-trust",
                )
            },
            "story_truths": sorted(cycle_3["shared_story_sync"]["story_truths"]),
            "repeated_signals": sorted(cycle_3["shared_story_sync"]["repeated_signals"]),
            "strong_threads": sorted(cycle_3["shared_story_sync"]["strong_threads"]),
            "unresolved_contradictions": sorted(cycle_3["shared_story_sync"]["contradictions_alive"]),
            "forward_consequence_count": len(cycle_3["evolved_runtime"]["shared_story_state"].get("forward_consequences", [])),
            "backward_requirement_count": len(cycle_3["evolved_runtime"]["shared_story_state"].get("backward_requirements", [])),
            "authority_effect": cycle_3["authority_effect"],
        }
        print("DRAGON_SPOTTER_RUNTIME_CYCLE_3_OBSERVATION=" + json.dumps(observation, sort_keys=True))


if __name__ == "__main__":
    unittest.main()
