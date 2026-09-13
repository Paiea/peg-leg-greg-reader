import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ThreeLFrontierPublishTests(unittest.TestCase):
    def test_reader_pages_cover_written_frontier(self):
        for record in range(1, 11):
            rid = f"{record:03d}"
            manuscript = ROOT / "3l" / "manuscript" / f"record-{rid}.md"
            page = ROOT / "3l" / "records" / f"{rid}.html"
            self.assertTrue(manuscript.exists(), manuscript)
            self.assertTrue(page.exists(), page)
            text = page.read_text(encoding="utf-8")
            self.assertIn(f"../manuscript/record-{rid}.md", text)

        index = (ROOT / "3l" / "records" / "index.html").read_text(encoding="utf-8")
        for record in range(1, 11):
            rid = f"{record:03d}"
            self.assertIn(f'href="{rid}.html"', index)

    def test_audio_plans_cover_002_through_010_with_locked_dragon_routes(self):
        for record in range(2, 11):
            rid = f"{record:03d}"
            plan_path = ROOT / "3l" / "audio" / f"record-{rid}-short-dual-plan.json"
            self.assertTrue(plan_path.exists(), plan_path)
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            self.assertTrue(plan.get("dragon_routing_locked"), rid)
            self.assertTrue(any("normal" in chunk["required_voices"] for chunk in plan["chunks"]), rid)
            self.assertTrue(all(len(chunk["transcript"]) <= 500 for chunk in plan["chunks"]), rid)

    def test_five_worker_frontier_order_covers_every_capture_once(self):
        master_path = ROOT / "3l" / "audio" / "records-002-010-five-worker-work-order.json"
        self.assertTrue(master_path.exists(), master_path)
        master = json.loads(master_path.read_text(encoding="utf-8"))
        self.assertEqual(master["records"], [f"{record:03d}" for record in range(2, 11)])
        self.assertEqual(master["worker_count"], 5)
        self.assertLessEqual(max(master["capture_loads"]) - min(master["capture_loads"]), 1)

        keys = []
        for worker in master["workers"]:
            expected_manifest = f"3l/audio/workers/records-002-010-{worker['worker_id']}-captures.json"
            self.assertEqual(worker["return_manifest"], expected_manifest)
            for capture in worker["captures"]:
                keys.append((capture["record"], capture["chunk_index"], capture["voice"]))
        self.assertEqual(len(keys), len(set(keys)))
        self.assertEqual(len(keys), master["total_captures"])


if __name__ == "__main__":
    unittest.main()
