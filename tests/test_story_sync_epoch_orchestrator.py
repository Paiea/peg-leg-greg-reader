import copy
import unittest

from scripts import story_epoch_orchestrator as epochs


class StoryEpochOrchestratorTests(unittest.TestCase):
    def _task(self, task_id, lane, *, act=None, cost=1, **signals):
        base = {
            "information_gain": 0.4,
            "uncertainty_reduction": 0.4,
            "downstream_reach": 0.4,
            "novelty": 0.4,
            "dramatic_importance": 0.4,
            "render_readiness": 0.0,
            "staleness": 0.0,
        }
        base.update(signals)
        return {
            "id": task_id,
            "lane": lane,
            "target_id": task_id.replace("task:", ""),
            "act": act,
            "expected_cost": cost,
            "priority_signals": base,
            "stop_conditions": ["budget exhausted"],
        }

    def _snapshot(self, phase="explore"):
        return {
            "epoch_number": 12,
            "story_state_version": "story:v21",
            "phase": phase,
            "frontier": [
                self._task("task:a1", "dream", act="act-i", novelty=0.9, information_gain=0.8),
                self._task("task:a2", "rehearsal", act="act-ii", uncertainty_reduction=0.9),
                self._task("task:a3", "performance", act="act-iii", dramatic_importance=0.9),
                self._task("task:a4", "dream", act="act-iv", downstream_reach=0.9, novelty=0.8),
                self._task("task:render-2", "render", render_readiness=1.0, dramatic_importance=0.7),
                self._task("task:stale-7", "stale_repair", staleness=1.0, dramatic_importance=0.8),
            ],
            "renderable_regions": ["chapter-2", "chapter-3"],
            "blocked_regions": ["chapter-4"],
            "stale_candidates": ["chapter-7:candidate-b"],
            "active_render_candidates": ["chapter-2:candidate-a"],
            "performance_queue": ["act-iii:trust"],
            "contradictions": ["ending-office-role"],
            "convergence": {"status": "candidate_passable"},
            "do_not_revisit": ["anomaly-bridge"],
        }

    def test_epoch_plan_respects_budget_and_immutable_snapshot_version(self):
        snapshot = self._snapshot()
        before = copy.deepcopy(snapshot)
        plan = epochs.plan_epoch(snapshot, budget_units=4)
        self.assertEqual(before, snapshot)
        self.assertEqual("story_epoch_plan/v1", plan["schema"])
        self.assertEqual("story:v21", plan["snapshot_version"])
        self.assertLessEqual(plan["allocated_budget"], 4)
        self.assertTrue(plan["tasks"])
        self.assertTrue(all(task["snapshot_version"] == "story:v21" for task in plan["tasks"]))
        self.assertTrue(all(task["budget_cap"] >= task["expected_cost"] for task in plan["tasks"]))
        self.assertEqual("derived_only", plan["authority"])
        self.assertFalse(plan["canon_write_authorized"])

    def test_four_persistent_acts_receive_baseline_opportunity_when_budget_permits(self):
        plan = epochs.plan_epoch(self._snapshot("explore"), budget_units=4)
        acts = {task.get("act") for task in plan["tasks"] if task.get("act")}
        self.assertEqual({"act-i", "act-ii", "act-iii", "act-iv"}, acts)

    def test_phase_changes_compute_allocation_without_changing_task_authority(self):
        explore = epochs.plan_epoch(self._snapshot("explore"), budget_units=5)
        render = epochs.plan_epoch(self._snapshot("render"), budget_units=5)
        explore_lanes = [task["lane"] for task in explore["tasks"]]
        render_lanes = [task["lane"] for task in render["tasks"]]
        self.assertGreaterEqual(explore_lanes.count("dream") + explore_lanes.count("rehearsal"), 2)
        self.assertIn("render", render_lanes)
        self.assertTrue(all(task["authority"] == "derived_work_order" for task in render["tasks"]))

    def test_repair_phase_prioritizes_stale_work_when_baseline_cannot_fit(self):
        plan = epochs.plan_epoch(self._snapshot("repair"), budget_units=1)
        self.assertEqual(1, len(plan["tasks"]))
        self.assertEqual("stale_repair", plan["tasks"][0]["lane"])
        self.assertEqual("task:stale-7", plan["tasks"][0]["id"])

    def test_epoch_reduction_rejects_stale_worker_snapshot(self):
        plan = epochs.plan_epoch(self._snapshot(), budget_units=4)
        with self.assertRaisesRegex(ValueError, "snapshot version"):
            epochs.reduce_epoch_results(plan, [{
                "task_id": plan["tasks"][0]["id"],
                "snapshot_version": "story:v20",
                "status": "completed",
            }])

    def test_epoch_reduction_queues_proposed_deltas_without_mutating_story_state(self):
        plan = epochs.plan_epoch(self._snapshot(), budget_units=4)
        first = plan["tasks"][0]
        reduction = epochs.reduce_epoch_results(plan, [{
            "task_id": first["id"],
            "snapshot_version": "story:v21",
            "status": "completed",
            "proposed_delta": {"kind": "dream_survivors", "payload": ["d1", "d2"]},
            "evidence": [{"kind": "probe", "finding": "survived"}],
            "retire_target": True,
        }])
        self.assertEqual("story_epoch_reduction/v1", reduction["schema"])
        self.assertEqual("story:v21", reduction["snapshot_version"])
        self.assertEqual(2, len(reduction["integration_queue"]))
        self.assertNotIn("story_state", reduction)
        self.assertIn(first["target_id"], reduction["retired_targets"])
        self.assertGreaterEqual(len(reduction["remaining_tasks"]), 1)

    def test_hot_start_packet_survives_partial_epoch_and_points_next_worker(self):
        snapshot = self._snapshot("render")
        plan = epochs.plan_epoch(snapshot, budget_units=5)
        completed = plan["tasks"][0]
        reduction = epochs.reduce_epoch_results(plan, [{
            "task_id": completed["id"],
            "snapshot_version": "story:v21",
            "status": "completed",
            "retire_target": True,
        }])
        packet = epochs.compile_next_epoch_packet(
            snapshot,
            reduction,
            continuation_hint="Continue highest-value render frontier and stale repair; do not reconstruct prior reasoning.",
        )
        self.assertEqual("story_epoch_continuation/v1", packet["schema"])
        self.assertEqual(13, packet["epoch_number"])
        self.assertEqual("story:v21", packet["story_state_version"])
        self.assertEqual("render", packet["phase"])
        self.assertEqual(["chapter-2", "chapter-3"], packet["renderable_regions"])
        self.assertEqual(["chapter-7:candidate-b"], packet["stale_candidates"])
        self.assertIn(completed["target_id"], packet["do_not_revisit"])
        self.assertTrue(packet["highest_value_targets"])
        self.assertIn("do not reconstruct", packet["continuation_hint"])
        self.assertFalse(packet["canon_write_authorized"])


if __name__ == "__main__":
    unittest.main()
