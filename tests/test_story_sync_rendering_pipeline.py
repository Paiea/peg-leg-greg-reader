import unittest

from scripts import long_form_rendering_loop as rendering


class StorySyncRenderingPipelineTests(unittest.TestCase):
    def _interval(self, interval_id="act-i:scene-01"):
        return {
            "id": interval_id,
            "act": "act-i",
            "state_in": {"role": "underqualified-official"},
            "state_out": {"role": "useful-negotiator"},
            "required_result": "Observation becomes a bounded useful action.",
            "reader_state": {"must_not_know": ["ending-role"]},
            "dependencies": {"professional-role": "v12", "reader-knowledge": "v4"},
            "story_truths": ["mutual-indispensability"],
        }

    def test_independent_interval_jobs_share_snapshot_without_global_cursor(self):
        first = rendering.compile_interval_job(self._interval("i1"), snapshot_version="story:v21", attempt_budget=2)
        second = rendering.compile_interval_job(self._interval("i2"), snapshot_version="story:v21", attempt_budget=1)
        self.assertEqual("long_form_interval_job/v1", first["schema"])
        self.assertEqual("story:v21", first["snapshot_version"])
        self.assertEqual("story:v21", second["snapshot_version"])
        self.assertNotIn("cursor", first)
        self.assertEqual("derived_candidate_only", first["authority"])
        self.assertFalse(first["canon_write_authorized"])
        self.assertEqual({"professional-role": "v12", "reader-knowledge": "v4"}, first["dependency_snapshot"])

    def test_actionable_evaluation_exposes_survives_fails_and_uncertain(self):
        normalized = rendering.normalize_evaluation({
            "survives": ["dramatic_state_transition", "opening_tension"],
            "fails": [
                {"code": "prose:middle_repetition", "feedback": "The middle repeats the same information."},
            ],
            "uncertain": [
                {"code": "relationship:timing", "feedback": "Attraction may land too early."},
            ],
            "future_repair_obligations": ["preserve the reader-hidden ending role"],
        })
        self.assertEqual("rendering_evaluation/v1", normalized["schema"])
        self.assertEqual(["dramatic_state_transition", "opening_tension"], normalized["survives"])
        self.assertEqual("prose:middle_repetition", normalized["fails"][0]["code"])
        self.assertEqual("relationship:timing", normalized["uncertain"][0]["code"])
        diagnosis = rendering.diagnose_evaluation(normalized)
        self.assertEqual("prose", diagnosis["failure_class"])
        self.assertEqual("reprompt", diagnosis["route"])
        self.assertIn("The middle repeats", diagnosis["feedback"][0])

    def test_directed_reprompt_locks_survivors_and_dependencies(self):
        interval = self._interval()
        diagnosis = rendering.diagnose_evaluation({
            "survives": ["dramatic_state_transition", "character_knowledge"],
            "fails": [{"code": "prose:premature_explanation", "feedback": "Hypothesis is verbalized before evidence."}],
            "uncertain": [],
        })
        packet = rendering.build_reprompt_packet(interval, "candidate A", diagnosis)
        self.assertEqual(interval["dependencies"], packet["locked_story_contract"]["dependencies"])
        self.assertEqual(["dramatic_state_transition", "character_knowledge"], packet["locked_survivors"])
        self.assertIn("Hypothesis is verbalized before evidence.", packet["targeted_feedback"])
        self.assertIn("Do not alter surviving elements", packet["instructions"])

    def test_independent_interval_reducer_reprompts_then_retains_without_global_run(self):
        job = rendering.compile_interval_job(self._interval(), snapshot_version="story:v21", attempt_budget=2)
        first = rendering.reduce_interval_attempt(job, {
            "candidate": {
                "id": "a",
                "text": "A",
                "evaluation": {
                    "survives": ["dramatic_state_transition"],
                    "fails": [{"code": "prose:generic_voice", "feedback": "Voice flattened."}],
                    "uncertain": [],
                },
            },
            "attempt_number": 1,
        })
        self.assertEqual("reprompt", first["status"])
        self.assertEqual("story:v21", first["snapshot_version"])
        second = rendering.reduce_interval_attempt(first, {
            "candidate": {
                "id": "b",
                "text": "B",
                "evaluation": {
                    "survives": ["dramatic_state_transition", "character_knowledge"],
                    "fails": [],
                    "uncertain": [],
                    "comparison_dimensions": {"voice": 0.8, "readability": 0.85},
                },
            },
            "attempt_number": 2,
        })
        self.assertEqual("retained", second["status"])
        self.assertEqual("b", second["retained"]["winner"]["id"])
        self.assertEqual({"professional-role": "v12", "reader-knowledge": "v4"}, second["retained"]["dependency_snapshot"])

    def test_story_failure_escapes_interval_to_rehearsal(self):
        job = rendering.compile_interval_job(self._interval(), snapshot_version="story:v21", attempt_budget=2)
        result = rendering.reduce_interval_attempt(job, {
            "candidate": {
                "id": "a",
                "text": "A",
                "evaluation": {
                    "survives": ["opening_tension"],
                    "fails": [{"code": "story:unsupported_mechanic_knowledge", "feedback": "Mechanic understanding appears before evidence."}],
                    "uncertain": [],
                },
            },
            "attempt_number": 1,
        })
        self.assertEqual("story_rehearsal", result["status"])
        self.assertEqual("Mechanic understanding appears before evidence.", result["rehearsal_request"]["problem"])
        self.assertEqual("story:v21", result["snapshot_version"])

    def test_prose_discoveries_are_proposals_not_story_truth(self):
        candidate = {
            "id": "b",
            "evaluation": {
                "prose_discoveries": [
                    {"claim": "Greg's joke implies prior failed training", "dimensions": ["character", "history"], "evidence": "The line lands naturally under pressure."},
                ],
            },
        }
        discoveries = rendering.extract_prose_discoveries(candidate, interval_id="i1")
        self.assertEqual(1, len(discoveries))
        discovery = discoveries[0]
        self.assertEqual("prose_discovery/v1", discovery["schema"])
        self.assertEqual("speculation_only", discovery["authority"])
        self.assertEqual("proposed_to_story_sync", discovery["status"])
        self.assertFalse(discovery["canon_write_authorized"])
        self.assertNotIn("maturity", discovery)
        self.assertNotIn("story_truth", discovery)

    def test_losing_candidate_can_contribute_useful_evidence_without_becoming_prose_winner(self):
        candidates = [
            {"id": "winner", "evaluation": {"survives": ["dramatic_state_transition"], "fails": [], "uncertain": [], "comparison_dimensions": {"readability": 0.8}}},
            {"id": "loser", "evaluation": {"survives": ["dramatic_state_transition"], "fails": [], "uncertain": [], "comparison_dimensions": {"readability": 0.6}, "useful_evidence": [{"kind": "causal_framing", "content": "The bargain reads more clearly when the cost is physically visible."}]}},
        ]
        comparison = rendering.compare_candidates(candidates)
        self.assertEqual("winner", comparison["winner_id"])
        evidence = rendering.collect_loser_evidence(candidates, comparison["winner_id"], interval_id="i1")
        self.assertEqual(1, len(evidence))
        self.assertEqual("derived_rendering_evidence/v1", evidence[0]["schema"])
        self.assertEqual("loser", evidence[0]["source_candidate_id"])
        self.assertEqual("none", evidence[0]["authority"])
        self.assertFalse(evidence[0]["canon_write_authorized"])


if __name__ == "__main__":
    unittest.main()
