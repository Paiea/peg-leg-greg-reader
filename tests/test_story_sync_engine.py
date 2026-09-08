import unittest

from scripts import story_sync_engine as sync


class StorySyncEngineTests(unittest.TestCase):
    def test_single_rehearsal_stays_speculation(self):
        discovery = {
            "id": "d1",
            "finding": "The fraud becomes calmer when forced to negotiate concretely.",
            "evidence": [
                {
                    "source_id": "take-a",
                    "independent_group": "scene-1.take-a",
                    "kind": "support",
                    "dramatic_uses": ["character"],
                    "regions": ["act-i"],
                }
            ],
        }
        self.assertEqual("speculation", sync.classify_discovery(discovery))

    def test_repetition_alone_does_not_become_strong_thread(self):
        discovery = {
            "id": "d2",
            "finding": "The dragon calls the spotter a liar.",
            "evidence": [
                {"source_id": f"take-{n}", "independent_group": f"take-{n}", "kind": "support", "dramatic_uses": ["dialogue"], "regions": ["act-i"]}
                for n in range(1, 5)
            ],
        }
        self.assertEqual("repeated_signal", sync.classify_discovery(discovery))

    def test_multi_use_cross_region_discovery_becomes_strong_thread(self):
        discovery = {
            "id": "d3",
            "finding": "Dragon gifts operate as diplomatic obligations, not random loot.",
            "evidence": [
                {"source_id": "negotiation-a", "independent_group": "negotiation-a", "kind": "support", "dramatic_uses": ["plot", "world", "character"], "regions": ["act-i"]},
                {"source_id": "politics-b", "independent_group": "politics-b", "kind": "support", "dramatic_uses": ["plot", "relationship", "setup_payoff"], "regions": ["act-ii", "act-iii"]},
            ],
        }
        self.assertEqual("strong_thread", sync.classify_discovery(discovery))

    def test_story_truth_requires_survived_challenge_not_just_support_volume(self):
        base = {
            "id": "d4",
            "finding": "The scholar and fraud become mutually indispensable.",
            "book_shaping": True,
            "evidence": [
                {"source_id": "a", "independent_group": "a", "kind": "support", "dramatic_uses": ["relationship", "plot", "character"], "regions": ["act-i"]},
                {"source_id": "b", "independent_group": "b", "kind": "support", "dramatic_uses": ["relationship", "setup_payoff", "world"], "regions": ["act-ii"]},
                {"source_id": "c", "independent_group": "c", "kind": "support", "dramatic_uses": ["relationship", "plot", "ending"], "regions": ["act-iv"]},
            ],
        }
        self.assertEqual("strong_thread", sync.classify_discovery(base))
        challenged = dict(base)
        challenged["evidence"] = base["evidence"] + [
            {"source_id": "challenge-1", "independent_group": "challenge-1", "kind": "challenge_survived", "dramatic_uses": ["relationship", "plot"], "regions": ["act-iii"]}
        ]
        self.assertEqual("story_truth", sync.classify_discovery(challenged))

    def test_sync_preserves_two_viable_competing_branches(self):
        state = {
            "schema": sync.SYNC_STATE_SCHEMA,
            "story_confidence": 0.55,
            "possibilities": [
                {"id": "ending-a", "branch_group": "ending", "region": "act-iv", "status": "active", "viability": "viable"},
                {"id": "ending-b", "branch_group": "ending", "region": "act-iv", "status": "active", "viability": "viable"},
            ],
            "discoveries": [],
            "contradictions": [{"id": "c1", "members": ["ending-a", "ending-b"], "status": "unresolved", "severity": "high"}],
            "canon_events": [],
            "reader_requirements": [],
            "assumptions": [],
        }
        report = sync.sync_story(state)
        self.assertEqual("compare", report["phase"])
        self.assertEqual(["ending-a", "ending-b"], report["branches_preserved"])
        self.assertEqual([], report["branches_killed"])
        self.assertEqual(["c1"], report["contradictions_alive"])

    def test_strong_thread_emits_backward_and_forward_propagation(self):
        state = {
            "schema": sync.SYNC_STATE_SCHEMA,
            "story_confidence": 0.6,
            "possibilities": [],
            "discoveries": [
                {
                    "id": "treasure-obligation",
                    "finding": "The first treasure gift creates a reciprocal obligation.",
                    "book_shaping": True,
                    "evidence": [
                        {"source_id": "r1", "independent_group": "r1", "kind": "support", "dramatic_uses": ["plot", "world", "character"], "regions": ["act-i"]},
                        {"source_id": "r2", "independent_group": "r2", "kind": "support", "dramatic_uses": ["plot", "relationship", "setup_payoff"], "regions": ["act-iii"]},
                    ],
                    "propagation": [
                        {"direction": "backward", "target": "act-i", "reason": "seed dragon reciprocity before the gift is interpreted"},
                        {"direction": "forward", "target": "act-iii", "reason": "make human institutions contest the obligation"},
                    ],
                }
            ],
            "contradictions": [],
            "canon_events": [],
            "reader_requirements": [],
            "assumptions": [],
        }
        report = sync.sync_story(state)
        self.assertEqual({"backward", "forward"}, {item["direction"] for item in report["propagation"]})
        self.assertIn("treasure-obligation", report["immediate_sync_discoveries"])

    def test_hidden_canon_remains_canon_but_can_leave_reader_gap(self):
        state = {
            "schema": sync.SYNC_STATE_SCHEMA,
            "story_confidence": 0.4,
            "possibilities": [],
            "discoveries": [],
            "contradictions": [],
            "canon_events": [
                {"id": "training-week", "canon": True, "visibility": "hide"},
                {"id": "public-negotiation", "canon": True, "visibility": "show"},
            ],
            "reader_requirements": [
                {"id": "earned-competence", "payoff_event": "public-negotiation", "required_setup_any": ["training-week"]}
            ],
            "assumptions": [],
        }
        report = sync.sync_story(state)
        self.assertIn("training-week", report["hidden_canon"])
        self.assertEqual(["earned-competence"], [gap["id"] for gap in report["reader_gaps"]])

    def test_visible_setup_satisfies_reader_dependency_without_unhiding_all_canon(self):
        state = {
            "schema": sync.SYNC_STATE_SCHEMA,
            "story_confidence": 0.4,
            "possibilities": [],
            "discoveries": [],
            "contradictions": [],
            "canon_events": [
                {"id": "training-week", "canon": True, "visibility": "hide"},
                {"id": "study-night", "canon": True, "visibility": "show"},
                {"id": "public-negotiation", "canon": True, "visibility": "show"},
            ],
            "reader_requirements": [
                {"id": "earned-competence", "payoff_event": "public-negotiation", "required_setup_any": ["training-week", "study-night"]}
            ],
            "assumptions": [],
        }
        report = sync.sync_story(state)
        self.assertEqual([], report["reader_gaps"])
        self.assertIn("training-week", report["hidden_canon"])

    def test_event_driven_sync_only_fires_when_discovery_is_book_shaping_and_supported(self):
        weak = {"id": "weak", "finding": "A funny hat recurs.", "book_shaping": True, "evidence": [{"source_id": "a", "independent_group": "a", "kind": "support", "dramatic_uses": ["comedy"], "regions": ["act-i"]}]}
        strong = {"id": "strong", "finding": "The presumed central conflict changes.", "book_shaping": True, "evidence": [
            {"source_id": "a", "independent_group": "a", "kind": "support", "dramatic_uses": ["plot", "character", "world"], "regions": ["act-i"]},
            {"source_id": "b", "independent_group": "b", "kind": "support", "dramatic_uses": ["plot", "relationship", "ending"], "regions": ["act-iii"]},
        ]}
        self.assertFalse(sync.should_trigger_immediate_sync(weak, sync.classify_discovery(weak)))
        self.assertTrue(sync.should_trigger_immediate_sync(strong, sync.classify_discovery(strong)))

    def test_convergence_is_confidence_driven_not_chapter_driven(self):
        self.assertEqual("explore", sync.convergence_phase(0.2))
        self.assertEqual("compare", sync.convergence_phase(0.6))
        self.assertEqual("converge", sync.convergence_phase(0.85))

    def test_weak_branch_is_not_killed_early_but_is_killed_late(self):
        possibility = {"id": "branch-x", "branch_group": "conflict", "region": "act-ii", "status": "active", "viability": "weak"}
        self.assertEqual("preserve", sync.branch_sync_action(possibility, phase="explore"))
        self.assertEqual("kill", sync.branch_sync_action(possibility, phase="converge"))

    def test_superseded_assumption_requires_replacement_and_evidence(self):
        good = {
            "id": "old-ending",
            "status": "superseded",
            "replaced_by": "new-ending",
            "why": "late rehearsal produced a more earned emotional ending",
            "evidence": ["ending-rehearsal-3"],
        }
        sync.validate_assumption(good)
        bad = dict(good, evidence=[])
        with self.assertRaisesRegex(ValueError, "evidence"):
            sync.validate_assumption(bad)


if __name__ == "__main__":
    unittest.main()
