import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import plg_ai_tools


EXPECTED = {
    "brain_for",
    "brain_doctor",
    "audio_next",
    "audio_claim",
    "compile_range",
    "get_scene_view",
    "query_scenes",
    "plan_campaign",
    "run_campaign",
    "get_campaign_result",
    "reduce_campaign",
    "apply_survivors",
}


class PLGAIToolTests(unittest.TestCase):
    def test_tool_registry_is_small_and_stable(self):
        self.assertEqual(EXPECTED, set(plg_ai_tools.TOOLS))

    def test_brain_tools_are_read_only_and_delegate(self):
        self.assertTrue(plg_ai_tools.TOOL_SPECS["brain_for"]["read_only"])
        self.assertTrue(plg_ai_tools.TOOL_SPECS["brain_doctor"]["read_only"])
        with mock.patch.object(plg_ai_tools.brain_compiler, "compile_brain", return_value={"schema":"plg_brain_packet/v1"}) as compile_brain:
            result = plg_ai_tools.brain_for({"task":"dialogue","authority_sha":"sha"})
        self.assertEqual("plg_brain_packet/v1", result["schema"]); compile_brain.assert_called_once()
        with mock.patch.object(plg_ai_tools.brain_doctor_module, "run_doctor", return_value={"schema":"plg_brain_doctor/v1"}) as doctor:
            report = plg_ai_tools.brain_doctor({})
        self.assertEqual("plg_brain_doctor/v1", report["schema"]); doctor.assert_called_once()

    def test_query_scenes_delegates_to_project_index(self):
        with mock.patch.object(plg_ai_tools.performance_index, "query_scenes", return_value=[{"scene_id": "214.s020"}]) as query:
            result = plg_ai_tools.query_scenes({"db_path": "/tmp/index.sqlite", "query": "Greg Antonius"})
        self.assertEqual([{"scene_id": "214.s020"}], result); query.assert_called_once()

    def test_plan_and_run_delegate_to_campaign_runner(self):
        with mock.patch.object(plg_ai_tools.performance_campaign, "plan_campaign", return_value={"campaign_id": "x"}) as plan:
            self.assertEqual({"campaign_id": "x"}, plg_ai_tools.plan_campaign({"task": "reverse_edit", "chapter_start": 1, "chapter_end": 2, "source_authority": "sha"})); plan.assert_called_once()
        with mock.patch.object(plg_ai_tools.performance_campaign, "run_campaign", return_value={"completed": 2}) as run:
            self.assertEqual({"completed": 2}, plg_ai_tools.run_campaign({"campaign_root": "/tmp/campaign"})); run.assert_called_once()

    def test_run_campaign_can_plan_and_execute_from_one_ai_tool_call(self):
        payload = {"task": "reverse_edit", "chapter_start": 1, "chapter_end": 491, "source_authority": "sha", "profile": "eco"}
        with mock.patch.object(plg_ai_tools, "plan_campaign", return_value={"campaign_id": "all", "campaign_root": "/tmp/all", "packets_planned": 300}) as plan, mock.patch.object(plg_ai_tools.performance_campaign, "run_campaign", return_value={"completed": 300, "failures": 0}) as run:
            result = plg_ai_tools.run_campaign(payload)
        plan.assert_called_once_with(payload); run.assert_called_once_with(Path("/tmp/all")); self.assertEqual("all", result["campaign_id"]); self.assertEqual(300, result["run"]["completed"])

    def test_read_scene_view_does_not_mutate_source_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); source = root / "001.html"; source.write_text("canon", encoding="utf-8"); before = source.read_bytes()
            with mock.patch.object(plg_ai_tools.funnel, "load_scene_record", return_value={"scene_id": "001.s010", "source": {"hash": "h"}, "mechanical": {}, "dependencies": {}}), mock.patch.object(plg_ai_tools.funnel, "render_scene_view", return_value={"scene_id": "001.s010"}):
                result = plg_ai_tools.get_scene_view({"scene_id": "001.s010", "view": "dialogue", "compiled_root": root.as_posix()})
            self.assertEqual("001.s010", result["scene_id"]); self.assertEqual(before, source.read_bytes())

    def test_apply_survivors_is_the_only_canon_write_adapter_and_delegates(self):
        canon_write_tools = {name for name, spec in plg_ai_tools.TOOL_SPECS.items() if spec.get("canon_write", False)}
        self.assertEqual({"apply_survivors"}, canon_write_tools)
        self.assertTrue(plg_ai_tools.TOOL_SPECS["audio_claim"]["write"])
        self.assertFalse(plg_ai_tools.TOOL_SPECS["audio_claim"]["canon_write"])
        with mock.patch.object(plg_ai_tools.performance_campaign, "integrate_campaign", return_value={"changed": []}) as integrate:
            result = plg_ai_tools.apply_survivors({"campaign_root": "/tmp/c", "chapter_root": "/tmp/chapters", "current_authority": "sha"})
        self.assertEqual({"changed": []}, result); integrate.assert_called_once()

    def test_tool_metadata_distinguishes_read_only_from_disposable_and_operational_writes(self):
        for name in ("brain_for","brain_doctor","audio_next","get_scene_view","query_scenes","get_campaign_result"):
            self.assertTrue(plg_ai_tools.TOOL_SPECS[name]["read_only"], name)
        for name in ("audio_claim", "compile_range", "plan_campaign", "run_campaign", "reduce_campaign", "apply_survivors"):
            self.assertFalse(plg_ai_tools.TOOL_SPECS[name]["read_only"], name)

    def test_call_dispatches_structured_payload(self):
        with mock.patch.dict(plg_ai_tools.TOOLS, {"query_scenes": lambda payload: {"q": payload["query"]}}):
            self.assertEqual({"q": "silver"}, plg_ai_tools.call_tool("query_scenes", {"query": "silver"}))
        with self.assertRaisesRegex(ValueError, "unknown PLG AI tool"): plg_ai_tools.call_tool("nope", {})


if __name__ == "__main__": unittest.main()
