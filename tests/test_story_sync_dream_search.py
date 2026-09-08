import unittest

from scripts import dream_search_engine as dream


class DreamSearchEngineTests(unittest.TestCase):
    def _candidate(self, candidate_id, *, concepts, form="causal_graph", surprise=0.7, causality=0.8, reach=0.7, novelty=0.5, form_gain=0.0, causal_status="pass"):
        return dream.build_candidate(
            candidate_id=candidate_id,
            source={"kind": "act", "id": "act-i", "acts": ["act-i"]},
            summary=f"candidate {candidate_id}",
            concept_keys=concepts,
            affected_dimensions=["character", "stakes"],
            representation=form,
            mutation_operator="seed",
            search_lens="strange_but_causal",
            scores={
                "surprise": surprise,
                "causality": causality,
                "reach": reach,
                "novelty_distance": novelty,
                "form_information_gain": form_gain,
            },
            cheap_causal_test={"status": causal_status, "reasons": []},
        )

    def test_dream_candidate_has_no_story_or_canon_authority(self):
        candidate = self._candidate("d1", concepts=["reciprocity", "repair"])
        self.assertEqual("dream_candidate/v1", candidate["schema"])
        self.assertEqual("none", candidate["authority"])
        self.assertFalse(candidate["canon_write_authorized"])
        self.assertEqual([], candidate["parents"])
        self.assertNotIn("story_truth", candidate)
        self.assertNotIn("maturity", candidate)

    def test_surprise_without_causality_gets_killed_cheaply(self):
        plausible = self._candidate("plausible", concepts=["method", "status"], surprise=0.7, causality=0.8, reach=0.8)
        bizarre = self._candidate("bizarre", concepts=["moon", "marriage"], surprise=1.0, causality=1.0, reach=1.0, causal_status="fail")
        self.assertGreater(dream.candidate_value(plausible), 0.0)
        self.assertEqual(0.0, dream.candidate_value(bizarre))
        selected = dream.select_diverse_survivors([bizarre, plausible], limit=2)
        self.assertEqual(["plausible"], [item["id"] for item in selected["survivors"]])
        self.assertEqual("cheap_causal_fail", selected["decisions"]["bizarre"])

    def test_dense_conceptual_cousins_are_suppressed_for_distant_survivors(self):
        cousins = [
            self._candidate("guild-a", concepts=["guild", "recruiter", "talent"], surprise=0.6, causality=0.9, reach=0.5),
            self._candidate("guild-b", concepts=["guild", "recruiter", "talent", "offer"], surprise=0.7, causality=0.9, reach=0.5),
        ]
        distant = self._candidate("method", concepts=["empirical-method", "fatal-risk-data", "social-value"], surprise=0.8, causality=0.8, reach=0.9)
        selected = dream.select_diverse_survivors(cousins + [distant], limit=2, similarity_threshold=0.7)
        ids = {item["id"] for item in selected["survivors"]}
        self.assertIn("method", ids)
        self.assertEqual(2, len(ids))
        self.assertEqual(1, sum(1 for item in selected["survivors"] if "guild" in item["content"]["concept_keys"]))
        self.assertIn("duplicate_cluster", selected["decisions"].values())

    def test_form_shift_can_preserve_content_while_earning_representation_diversity(self):
        base = self._candidate("base", concepts=["trust", "withheld-motive"], form="causal_graph")
        performed = dream.shift_form(
            base,
            candidate_id="performed",
            representation="performance",
            operator="PERFORM",
            form_information_gain=0.8,
        )
        self.assertEqual(["base"], performed["parents"])
        self.assertEqual("performance", performed["representation"])
        self.assertEqual("PERFORM", performed["mutation_operator"])
        self.assertEqual("none", performed["authority"])
        selected = dream.select_diverse_survivors([base, performed], limit=2, similarity_threshold=0.7)
        self.assertEqual({"base", "performed"}, {item["id"] for item in selected["survivors"]})

    def test_mutation_and_crossover_keep_parent_provenance_but_no_authority(self):
        a = self._candidate("a", concepts=["cost", "crown"])
        b = self._candidate("b", concepts=["dragon", "recognition"])
        mutation = dream.mutate_candidate(
            a,
            candidate_id="a-mut",
            summary="Swap who pays the institutional cost",
            concept_keys=["cost", "crown", "swap-payer"],
            operator="swap_cost_payer",
        )
        crossed = dream.cross_candidates(
            a,
            b,
            candidate_id="cross",
            summary="Crown cost collides with dragon recognition",
            concept_keys=["cost", "crown", "dragon", "recognition"],
        )
        self.assertEqual(["a"], mutation["parents"])
        self.assertEqual(["a", "b"], crossed["parents"])
        self.assertEqual("none", mutation["authority"])
        self.assertEqual("none", crossed["authority"])
        self.assertFalse(crossed["canon_write_authorized"])

    def test_rehearsal_bridge_is_a_question_not_a_promotion(self):
        candidate = self._candidate("r", concepts=["method", "social-value"], form="counterfactual_worldline")
        probe = dream.compile_rehearsal_probe(candidate)
        self.assertEqual("dream_rehearsal_probe/v1", probe["schema"])
        self.assertEqual("derived_only_no_story_authority", probe["authority"])
        self.assertEqual("r", probe["source_candidate_id"])
        self.assertIn(probe["experiment_mode"], {
            "plausibility_probe",
            "trajectory_worldline_test",
            "state_transition_test",
            "performance",
        })
        self.assertNotIn("maturity", probe)
        self.assertNotIn("story_truth", probe)

    def test_value_prioritizes_surprise_causality_reach_with_bounded_bonuses(self):
        broad = self._candidate("broad", concepts=["method", "identity", "status"], surprise=0.8, causality=0.8, reach=0.9, novelty=0.7, form_gain=0.4)
        shallow = self._candidate("shallow", concepts=["new-spell"], surprise=0.9, causality=0.9, reach=0.2, novelty=0.9, form_gain=0.0)
        self.assertGreater(dream.candidate_value(broad), dream.candidate_value(shallow))
        self.assertLessEqual(dream.candidate_value(broad), 1.2)


if __name__ == "__main__":
    unittest.main()
