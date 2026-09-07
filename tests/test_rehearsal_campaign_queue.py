import tempfile
import unittest
from pathlib import Path

from scripts import rehearsal_campaign_queue as queue


class RehearsalCampaignQueueTests(unittest.TestCase):
    def test_build_batches_covers_061_through_491_serially(self):
        batches = queue.build_batches(61, 491, 10)
        self.assertEqual((61, 70), batches[0])
        self.assertEqual((481, 490), batches[-2])
        self.assertEqual((491, 491), batches[-1])
        self.assertEqual(44, len(batches))

    def test_next_batch_returns_first_pending_only(self):
        state = queue.new_state("editor/rehearsal-simulation-engine", 61, 491, 10)
        self.assertEqual((61, 70), (queue.next_batch(state)["start"], queue.next_batch(state)["end"]))
        queue.claim_next(state, "abc123")
        queue.settle_current(state, "abc123", "def456", "source_win")
        self.assertEqual((71, 80), (queue.next_batch(state)["start"], queue.next_batch(state)["end"]))

    def test_adopt_equivalent_authority_moves_queue_tip_without_changing_result(self):
        state = queue.new_state("editor/rehearsal-simulation-engine", 61, 491, 10)
        queue.claim_next(state, "abc123")
        queue.settle_current(state, "abc123", "def456", "applied")
        adopted = queue.adopt_equivalent_authority(state, "def456", "meta789")
        self.assertEqual("meta789", adopted)
        self.assertEqual("meta789", state["settled_authority"])
        self.assertEqual("meta789", state["batches"][0]["settled_authority"])
        self.assertEqual("applied", state["batches"][0]["status"])
        queue.claim_next(state, "meta789")
        self.assertEqual("meta789", state["batches"][1]["source_authority"])

    def test_adopt_equivalent_authority_requires_current_settled_tip(self):
        state = queue.new_state("editor/rehearsal-simulation-engine", 61, 491, 10)
        queue.claim_next(state, "abc123")
        queue.settle_current(state, "abc123", "def456", "source_win")
        with self.assertRaisesRegex(ValueError, "settled authority"):
            queue.adopt_equivalent_authority(state, "wrong", "meta789")

    def test_blocked_batch_prevents_later_claim(self):
        state = queue.new_state("editor/rehearsal-simulation-engine", 61, 491, 10)
        state["batches"][0]["status"] = "blocked"
        state["batches"][0]["blocking_reason"] = "exact source mismatch"
        self.assertIsNone(queue.next_batch(state))
        with self.assertRaisesRegex(ValueError, "blocked"):
            queue.claim_next(state, "abc123")

    def test_claim_records_source_authority_and_cannot_double_claim(self):
        state = queue.new_state("editor/rehearsal-simulation-engine", 61, 491, 10)
        claimed = queue.claim_next(state, "abc123")
        self.assertEqual("abc123", claimed["source_authority"])
        self.assertEqual("running", claimed["status"])
        with self.assertRaisesRegex(ValueError, "running"):
            queue.claim_next(state, "def456")

    def test_settle_requires_matching_claim_authority_and_valid_result(self):
        state = queue.new_state("editor/rehearsal-simulation-engine", 61, 491, 10)
        queue.claim_next(state, "abc123")
        with self.assertRaisesRegex(ValueError, "source authority"):
            queue.settle_current(state, "wrong", "def456", "source_win")
        with self.assertRaisesRegex(ValueError, "result"):
            queue.settle_current(state, "abc123", "def456", "skipped")
        settled = queue.settle_current(state, "abc123", "def456", "source_win")
        self.assertEqual("source_win", settled["status"])
        self.assertEqual("def456", state["settled_authority"])

    def test_retry_limit_is_one(self):
        state = queue.new_state("editor/rehearsal-simulation-engine", 61, 491, 10)
        queue.claim_next(state, "abc123")
        queue.block_current(state, "worker_failure", retryable=True)
        queue.retry_current(state, "abc123")
        queue.block_current(state, "worker_failure", retryable=True)
        with self.assertRaisesRegex(ValueError, "retry"):
            queue.retry_current(state, "abc123")

    def test_validate_state_rejects_settled_batch_without_authority(self):
        state = queue.new_state("editor/rehearsal-simulation-engine", 61, 491, 10)
        state["batches"][0]["status"] = "applied"
        with self.assertRaises(ValueError):
            queue.validate_state(state)

    def test_save_and_load_state_roundtrip(self):
        state = queue.new_state("editor/rehearsal-simulation-engine", 61, 491, 10)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "queue.json"
            queue.save_state(path, state)
            loaded = queue.load_state(path)
        self.assertEqual(state, loaded)


if __name__ == "__main__":
    unittest.main()
