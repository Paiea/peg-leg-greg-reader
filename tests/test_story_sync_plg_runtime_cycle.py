import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import plg_ai_tools


class PLGPersistentRuntimeCycleTests(unittest.TestCase):
    def test_runtime_cycle_is_exposed_as_derived_only_ai_tool(self):
        self.assertIn("run_story_rehearsal_cycle", plg_ai_tools.TOOLS)
        spec = plg_ai_tools.TOOL_SPECS["run_story_rehearsal_cycle"]
        self.assertFalse(spec["write"])
        self.assertFalse(spec["read_only"])

    def test_runtime_cycle_accepts_object_or_path_and_can_write_derived_output(self):
        state = {"schema": "persistent_act_runtime/v1", "story_id": "test"}
        expected = {"schema": "persistent_rehearsal_cycle/v1", "authority_effect": "derived_only_no_canon_mutation"}
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_path = root / "runtime.json"
            output_path = root / "cycle.json"
            state_path.write_text(json.dumps(state), encoding="utf-8")
            with mock.patch.object(plg_ai_tools.persistent_act_runtime, "run_rehearsal_cycle", return_value=expected) as run:
                result = plg_ai_tools.run_story_rehearsal_cycle({"runtime_path": state_path.as_posix(), "output_path": output_path.as_posix()})
            run.assert_called_once_with(state, evidence=None, creator_taste=None)
            self.assertEqual(expected, result)
            self.assertEqual(expected, json.loads(output_path.read_text(encoding="utf-8")))

    def test_runtime_cycle_passes_evidence_and_creator_taste_without_granting_write_authority(self):
        state = {"schema": "persistent_act_runtime/v1", "story_id": "test"}
        evidence = [{"schema": "persistent_rehearsal_evidence/v1", "id": "e"}]
        creator_taste = {"schema": "creator_taste_context/v1", "project": "test", "cross_project_signals": [], "project_signals": [], "authority_effect": "heuristic_only_no_story_authority"}
        expected = {"schema": "persistent_rehearsal_cycle/v1", "authority_effect": "derived_only_no_canon_mutation"}
        with mock.patch.object(plg_ai_tools.persistent_act_runtime, "run_rehearsal_cycle", return_value=expected) as run:
            result = plg_ai_tools.run_story_rehearsal_cycle({"runtime": state, "evidence": evidence, "creator_taste": creator_taste})
        run.assert_called_once_with(state, evidence=evidence, creator_taste=creator_taste)
        self.assertEqual(expected, result)
        self.assertFalse(plg_ai_tools.TOOL_SPECS["run_story_rehearsal_cycle"]["write"])


if __name__ == "__main__":
    unittest.main()
