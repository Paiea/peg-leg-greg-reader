import unittest

from scripts import long_form_rendering_loop as rendering


class LongFormRenderingLoopTests(unittest.TestCase):
    def setUp(self):
        self.interval = {
            "id": "act-i:first-dragon-bargain",
            "act": "act-i",
            "state_in": {"professional_role": "underqualified-official-spotter"},
            "state_out": {"professional_role": "useful-underqualified-negotiator"},
            "required_result": "A real reciprocal bargain becomes possible without making Greg secretly expert.",
            "reader_state": {"knows": ["Greg is underqualified"], "must_not_know": ["ending office role"]},
            "story_truths": ["mutual-indispensability"],
            "strong_threads": ["gift-reciprocity", "improvisation-is-competence-path"],
            "case_law": ["first-bargain high-heat performance"],
            "renderer_choices": ["land-restoration", "relic-restitution"],
        }

    def test_compile_render_packet_is_derived_only_and_keeps_choices_open(self):
        packet = rendering.compile_render_packet(self.interval, rendering_memory=[])
        self.assertEqual("long_form_render_packet/v1", packet["schema"])
        self.assertEqual("derived_candidate_only", packet["authority"])
        self.assertFalse(packet["canon_write_authorized"])
        self.assertEqual(self.interval["state_in"], packet["state_in"])
        self.assertEqual(self.interval["state_out"], packet["state_out"])
        self.assertEqual(["land-restoration", "relic-restitution"], packet["renderer_choices"])

    def test_failure_diagnosis_routes_story_gap_away_from_reprompt(self):
        prose = rendering.diagnose_evaluation({"causal_fidelity": "pass", "prose_quality": "fail", "performance_fidelity": "pass", "continuity": "pass"})
        story = rendering.diagnose_evaluation({"causal_fidelity": "fail", "prose_quality": "pass", "performance_fidelity": "pass", "continuity": "pass"})
        self.assertEqual("prose", prose["failure_class"])
        self.assertEqual("reprompt", prose["route"])
        self.assertEqual("story", story["failure_class"])
        self.assertEqual("story_rehearsal", story["route"])
        with self.assertRaises(ValueError):
            rendering.build_reprompt_packet(self.interval, "candidate", story)

    def test_targeted_reprompt_preserves_story_contract(self):
        diagnosis = {"failure_class": "prose", "route": "reprompt", "feedback": ["dialogue is explanatory"]}
        packet = rendering.build_reprompt_packet(self.interval, "candidate A", diagnosis)
        self.assertEqual(self.interval["state_in"], packet["locked_story_contract"]["state_in"])
        self.assertEqual(self.interval["state_out"], packet["locked_story_contract"]["state_out"])
        self.assertIn("dialogue is explanatory", packet["targeted_feedback"])
        self.assertIn("Do not solve this by changing story facts", packet["instructions"])

    def test_candidate_comparison_retains_best_and_only_renderer_memory(self):
        candidates = [
            {"id": "a", "text": "A", "evaluation": {"causal_fidelity": "pass", "performance_fidelity": "pass", "continuity": "pass", "prose_quality": "pass", "scores": {"voice": 0.6, "readability": 0.7}}},
            {"id": "b", "text": "B", "evaluation": {"causal_fidelity": "pass", "performance_fidelity": "pass", "continuity": "pass", "prose_quality": "pass", "scores": {"voice": 0.9, "readability": 0.8}, "lessons": ["keep negotiation embodied"]}},
        ]
        comparison = rendering.compare_candidates(candidates)
        retained = rendering.retain_candidate(self.interval, candidates, comparison)
        self.assertEqual("b", retained["winner"]["id"])
        self.assertEqual(["keep negotiation embodied"], retained["rendering_memory_delta"])
        self.assertNotIn("story_sync_updates", retained)
        self.assertFalse(retained["canon_write_authorized"])

    def test_forward_motion_budget_advances_acceptable_interval(self):
        run = {"status": "rendering", "attempt_budget_default": 2, "intervals": [self.interval], "cursor": 0, "ledger": [], "rendering_memory": []}
        result = rendering.advance_rendering_run(run, {
            "candidate": {"id": "a", "text": "candidate", "evaluation": {"causal_fidelity": "pass", "performance_fidelity": "pass", "continuity": "pass", "prose_quality": "pass", "scores": {"voice": 0.7}}},
            "attempt_number": 1,
        })
        self.assertEqual("complete", result["status"])
        self.assertEqual(1, result["cursor"])
        self.assertEqual(self.interval["state_out"], result["ledger"][0]["state_out"])

    def test_forward_motion_budget_reprompts_once_then_retains_best_passing_candidate(self):
        run = {"status": "rendering", "attempt_budget_default": 2, "intervals": [self.interval], "cursor": 0, "ledger": [], "rendering_memory": []}
        first = rendering.advance_rendering_run(run, {
            "candidate": {"id": "a", "text": "A", "evaluation": {"causal_fidelity": "pass", "performance_fidelity": "pass", "continuity": "pass", "prose_quality": "fail", "feedback": ["too explanatory"], "scores": {"voice": 0.5}}},
            "attempt_number": 1,
        })
        self.assertEqual("reprompt", first["status"])
        second = rendering.advance_rendering_run(first, {
            "candidate": {"id": "b", "text": "B", "evaluation": {"causal_fidelity": "pass", "performance_fidelity": "pass", "continuity": "pass", "prose_quality": "pass", "scores": {"voice": 0.8}}},
            "attempt_number": 2,
        })
        self.assertEqual("complete", second["status"])
        self.assertEqual("b", second["ledger"][0]["winner"]["id"])

    def test_story_gap_escapes_to_rehearsal_without_advancing(self):
        run = {"status": "rendering", "attempt_budget_default": 2, "intervals": [self.interval], "cursor": 0, "ledger": [], "rendering_memory": []}
        result = rendering.advance_rendering_run(run, {
            "candidate": {"id": "a", "text": "A", "evaluation": {"causal_fidelity": "fail", "performance_fidelity": "pass", "continuity": "pass", "prose_quality": "pass", "feedback": ["dragon demand lacks causal support"]}},
            "attempt_number": 1,
        })
        self.assertEqual("story_rehearsal", result["status"])
        self.assertEqual(0, result["cursor"])
        self.assertEqual("dragon demand lacks causal support", result["rehearsal_request"]["problem"])


if __name__ == "__main__":
    unittest.main()
