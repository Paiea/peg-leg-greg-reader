import json
import unittest

from scripts.build_3l_parallel_audio_work_order import build_work_order


class ParallelAudioWorkOrderTests(unittest.TestCase):
    def _plan(self, record, weights):
        chunks = []
        for index, weight in enumerate(weights, start=1):
            voices = ["deep"] if weight == 1 else ["deep", "normal"]
            chunks.append(
                {
                    "index": index,
                    "transcript": f"record {record} chunk {index}",
                    "char_count": 20,
                    "semantic_spans": [{"start": 0, "end": 5, "role": "greg", "text": "hello"}],
                    "required_voices": voices,
                }
            )
        return {
            "record": record,
            "title": f"RECORD {record}",
            "dragon_routing_locked": True,
            "chunks": chunks,
        }

    def test_partitions_every_capture_exactly_once_across_five_workers(self):
        plans = [
            self._plan("002", [1, 2, 1, 2, 1, 2, 1, 2, 1, 2]),
            self._plan("003", [2, 1, 2, 1, 2, 1, 2, 1, 2, 1]),
        ]
        order = build_work_order(plans, worker_count=5, branch="test-branch")

        expected = {
            (plan["record"], chunk["index"], voice)
            for plan in plans
            for chunk in plan["chunks"]
            for voice in chunk["required_voices"]
        }
        actual = []
        for worker in order["workers"]:
            for chunk in worker["chunks"]:
                actual.extend(
                    (chunk["record"], chunk["chunk_index"], voice)
                    for voice in chunk["required_voices"]
                )

        self.assertEqual(len(actual), len(set(actual)))
        self.assertEqual(set(actual), expected)

    def test_balance_differs_by_at_most_one_capture(self):
        plans = [
            self._plan("002", [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2]),
            self._plan("003", [2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]),
        ]
        order = build_work_order(plans, worker_count=5, branch="test-branch")
        loads = [worker["capture_count"] for worker in order["workers"]]
        self.assertLessEqual(max(loads) - min(loads), 1)

    def test_workers_own_whole_chunks_and_get_separate_manifest_paths(self):
        plans = [self._plan("002", [2] * 10), self._plan("003", [2] * 10)]
        order = build_work_order(plans, worker_count=5, branch="test-branch")

        seen_chunks = set()
        manifest_paths = set()
        for worker in order["workers"]:
            manifest_paths.add(worker["return_manifest"])
            for chunk in worker["chunks"]:
                key = (chunk["record"], chunk["chunk_index"])
                self.assertNotIn(key, seen_chunks)
                seen_chunks.add(key)
                self.assertEqual(chunk["capture_count"], len(chunk["required_voices"]))

        self.assertEqual(len(manifest_paths), 5)

    def test_rejects_unlocked_dragon_routing(self):
        plan = self._plan("002", [1, 2])
        plan["dragon_routing_locked"] = False
        with self.assertRaisesRegex(ValueError, "dragon routing is not locked"):
            build_work_order([plan], worker_count=5, branch="test-branch")


if __name__ == "__main__":
    unittest.main()
