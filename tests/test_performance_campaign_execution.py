import json
import tempfile
import threading
import time
import unittest
from pathlib import Path

from scripts import performance_campaign


class PerformanceCampaignExecutionTests(unittest.TestCase):
    def _campaign(self, root: Path, packet_count: int = 4, profile: str = "eco") -> Path:
        campaign_root = root / "campaign"
        campaign_root.mkdir(parents=True)
        campaign = {
            "schema": "performance_campaign/v1",
            "campaign_id": "test",
            "task": "reverse_edit",
            "source_authority": "abc123",
            "scope": {"chapters": {"start": 1, "end": packet_count}},
            "execution": {"profile": profile, "executor": "fake", "max_worker_retries": 1},
            "paths": {"compiled_root": (root / "compiled").as_posix()},
            "plan": {"scenes_considered": packet_count, "cache_hits": 0, "packets_planned": packet_count},
        }
        (campaign_root / "campaign.json").write_text(json.dumps(campaign), encoding="utf-8")
        packets = [
            {"packet_id": f"{i:03d}.s010:reverse_edit:dep{i}", "scene_id": f"{i:03d}.s010", "task": "reverse_edit", "view": "comparison", "source_hash": f"hash{i}", "dependency_hash": f"dep{i}", "missing_layers": ["comparison"], "creative_authority": False, "write_authority": "derived_only", "output_schema": "performance_scene_result/v1"}
            for i in range(1, packet_count + 1)
        ]
        (campaign_root / "packets.jsonl").write_text("".join(json.dumps(p) + "\n" for p in packets), encoding="utf-8")
        (campaign_root / "results.jsonl").write_text("", encoding="utf-8")
        (campaign_root / "failures.jsonl").write_text("", encoding="utf-8")
        return campaign_root

    def test_eco_profile_bounds_worker_concurrency(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            campaign_root = self._campaign(root, packet_count=5)
            lock = threading.Lock()
            active = 0
            peak = 0

            def fake(packet, prompt, config):
                nonlocal active, peak
                with lock:
                    active += 1
                    peak = max(peak, active)
                time.sleep(0.03)
                with lock:
                    active -= 1
                return {"status": "completed", "comparison": {"verdict": "source_win", "reason": "source"}}

            result = performance_campaign.run_campaign(campaign_root, executor_fn=fake)
            self.assertEqual(5, result["workers_launched"])
            self.assertLessEqual(peak, 2)
            self.assertGreaterEqual(peak, 2)

    def test_resume_skips_completed_packets(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            campaign_root = self._campaign(root, packet_count=2)
            first_packet = json.loads((campaign_root / "packets.jsonl").read_text(encoding="utf-8").splitlines()[0])
            (campaign_root / "results.jsonl").write_text(json.dumps({"packet_id": first_packet["packet_id"], "scene_id": first_packet["scene_id"], "status": "completed", "comparison": {"verdict": "source_win", "reason": "cached run"}}) + "\n", encoding="utf-8")
            calls = []

            def fake(packet, prompt, config):
                calls.append(packet["packet_id"])
                return {"status": "completed", "comparison": {"verdict": "source_win", "reason": "source"}}

            performance_campaign.run_campaign(campaign_root, executor_fn=fake)
            self.assertEqual(1, len(calls))
            self.assertNotEqual(first_packet["packet_id"], calls[0])

    def test_retry_is_bounded_and_failure_is_recorded(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            campaign_root = self._campaign(root, packet_count=1)
            calls = 0

            def always_fail(packet, prompt, config):
                nonlocal calls
                calls += 1
                raise RuntimeError("transient")

            result = performance_campaign.run_campaign(campaign_root, executor_fn=always_fail)
            self.assertEqual(2, calls)
            self.assertEqual(1, result["failures"])
            failures = [json.loads(line) for line in (campaign_root / "failures.jsonl").read_text(encoding="utf-8").splitlines() if line]
            self.assertEqual(1, len(failures))

    def test_telemetry_does_not_invent_usage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            campaign_root = self._campaign(root, packet_count=1)

            def fake(packet, prompt, config):
                return {"status": "completed", "comparison": {"verdict": "source_win", "reason": "source"}}

            performance_campaign.run_campaign(campaign_root, executor_fn=fake)
            events = [json.loads(line) for line in (campaign_root / "telemetry.jsonl").read_text(encoding="utf-8").splitlines() if line]
            completed = [event for event in events if event["event"] == "worker_complete"]
            self.assertEqual(1, len(completed))
            self.assertIsNone(completed[0]["input_tokens"])
            self.assertIsNone(completed[0]["output_tokens"])
            self.assertIsNone(completed[0]["cached_tokens"])

    def test_worker_prompt_is_scope_locked_and_execution_biased(self):
        packet = {"packet_id": "214.s020:reverse_edit:abc", "scene_id": "214.s020", "task": "reverse_edit", "view": "comparison", "source_hash": "hash", "dependency_hash": "abc", "missing_layers": ["comparison"], "creative_authority": False, "write_authority": "derived_only", "output_schema": "performance_scene_result/v1"}
        prompt = performance_campaign.build_worker_prompt(packet, {"scene_id": "214.s020", "source": {"hash": "hash", "paragraphs": ["Exact prose."]}, "mechanical": {}, "dependencies": {}})
        self.assertIn("214.s020", prompt)
        self.assertIn("Do not redesign", prompt)
        self.assertIn("derived_only", prompt)
        self.assertIn("Exact prose.", prompt)
        self.assertNotIn("chapter 215", prompt.lower())


if __name__ == "__main__":
    unittest.main()
