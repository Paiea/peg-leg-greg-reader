import json
import tempfile
import unittest
from pathlib import Path

from scripts import brain_compiler


class BrainCompilerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "state" / "brain").mkdir(parents=True)
        (self.root / "state" / "editorial").mkdir(parents=True)
        for path in [
            "AGENTS.md", "state/PROJECT_STATE.md", "state/HANDSHAKE_PROTOCOL.md",
            "state/MANUSCRIPT_ENGINE_PLAYBOOK.md", "state/MANUSCRIPT_WORKFLOW.md",
            "state/MANUSCRIPT_STATE.md", "state/OPEN_THREADS.md", "state/STORY_NORTH_STAR.md",
            "state/EDITOR_STATE.md", "state/PROSE_PLAYBOOK.md", "state/GENERAL_EDITOR_STATE.md",
            "state/CHARACTER_BIBLE.md", "state/ECONOMY_CONTINUITY.md", "state/VISUAL_BIBLE.md",
            "state/IMAGE_PRODUCTION.md", "state/editorial/CODEX_EXECUTION_POLICY.md",
        ]:
            p = self.root / path
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(f"pointer {path}\n", encoding="utf-8")
        self.registry = self.root / "state" / "brain" / "ROUTING_REGISTRY.json"
        self.registry.write_text(json.dumps({
            "schema": "plg_brain_routing/v1",
            "project": {"authority":"main","canon":"manuscript prose","root_router":"AGENTS.md","project_state":"state/PROJECT_STATE.md","manuscript_owner":"state/MANUSCRIPT_STATE.md","engines":["01","02","03","04"]},
            "tag_aliases": {"whole-manuscript dialogue":["dialogue","editorial"],"continue manuscript":["manuscript"],"illustration":["illustration"]},
            "exclusive_task_tags": ["dialogue-owner"],
            "discovery": {"include_globs":["state/*.md","state/editorial/*.md"],"ignore_globs":[]},
            "documents": [
                {"path":"AGENTS.md","owner":"project","authority_class":"router","default_temperature":"hot","task_tags":[],"reason":"Root router","universal":True},
                {"path":"state/PROJECT_STATE.md","owner":"project","authority_class":"project_state","default_temperature":"hot","task_tags":[],"reason":"Project authority","universal":True},
                {"path":"state/MANUSCRIPT_ENGINE_PLAYBOOK.md","owner":"01","authority_class":"playbook","default_temperature":"conditional","task_tags":["manuscript"],"reason":"Manuscript method"},
                {"path":"state/MANUSCRIPT_STATE.md","owner":"01","authority_class":"state","default_temperature":"conditional","task_tags":["manuscript","illustration"],"reason":"Current manuscript owner"},
                {"path":"state/OPEN_THREADS.md","owner":"01","authority_class":"state","default_temperature":"conditional","task_tags":["manuscript"],"reason":"Open story threads"},
                {"path":"state/STORY_NORTH_STAR.md","owner":"project","authority_class":"direction","default_temperature":"conditional","task_tags":["manuscript","editorial"],"reason":"Story direction"},
                {"path":"state/EDITOR_STATE.md","owner":"04","authority_class":"editorial_state","default_temperature":"conditional","task_tags":["editorial","dialogue"],"reason":"Editor state"},
                {"path":"state/PROSE_PLAYBOOK.md","owner":"04","authority_class":"playbook","default_temperature":"conditional","task_tags":["editorial","dialogue"],"reason":"Prose craft"},
                {"path":"state/GENERAL_EDITOR_STATE.md","owner":"04","authority_class":"case_law","default_temperature":"cold","task_tags":["editorial"],"reason":"Historical editor case law","case_law":True},
                {"path":"state/CHARACTER_BIBLE.md","owner":"character","authority_class":"bible","default_temperature":"conditional","task_tags":["character"],"reason":"Character continuity"},
                {"path":"state/ECONOMY_CONTINUITY.md","owner":"economy","authority_class":"continuity","default_temperature":"conditional","task_tags":["economy"],"reason":"Money continuity"},
                {"path":"state/VISUAL_BIBLE.md","owner":"visual","authority_class":"bible","default_temperature":"conditional","task_tags":["illustration"],"reason":"Visual continuity"},
                {"path":"state/IMAGE_PRODUCTION.md","owner":"visual","authority_class":"workflow","default_temperature":"conditional","task_tags":["illustration"],"reason":"Image production"},
            ],
            "workstreams": [{"id":"dialogue-pass","status":"ACTIVE","task_tags":["dialogue"],"owner_tags":["dialogue-owner"],"owner_path":"state/EDITOR_STATE.md","reason":"Current dialogue owner"}]
        }, indent=2), encoding="utf-8")

    def tearDown(self): self.tmp.cleanup()

    def hot_paths(self, packet): return {row["path"] for row in packet["hot"]}

    def test_dialogue_task_is_narrow(self):
        p = brain_compiler.compile_brain("whole-manuscript dialogue pass", self.root, self.registry, authority_sha="abc")
        self.assertTrue({"state/EDITOR_STATE.md","state/PROSE_PLAYBOOK.md"} <= self.hot_paths(p))
        self.assertNotIn("state/VISUAL_BIBLE.md", self.hot_paths(p))
        self.assertNotIn("state/ECONOMY_CONTINUITY.md", self.hot_paths(p))
        self.assertEqual("high", p["routing"]["confidence"])
        self.assertEqual("dialogue-pass", p["active_wip"][0]["id"])

    def test_manuscript_and_illustration_routing(self):
        m = brain_compiler.compile_brain("continue manuscript", self.root, self.registry)
        self.assertTrue({"state/MANUSCRIPT_ENGINE_PLAYBOOK.md","state/MANUSCRIPT_STATE.md","state/OPEN_THREADS.md"} <= self.hot_paths(m))
        i = brain_compiler.compile_brain("illustration reconciliation", self.root, self.registry)
        self.assertTrue({"state/VISUAL_BIBLE.md","state/IMAGE_PRODUCTION.md","state/MANUSCRIPT_STATE.md"} <= self.hot_paths(i))

    def test_unknown_task_fails_soft(self):
        p = brain_compiler.compile_brain("quantum turnip arbitration", self.root, self.registry)
        self.assertEqual([], p["routing"]["matched_tags"])
        self.assertEqual("low", p["routing"]["confidence"])
        self.assertEqual({"AGENTS.md","state/PROJECT_STATE.md"}, self.hot_paths(p))

    def test_case_law_stays_cold_and_packet_has_no_source_bodies(self):
        p = brain_compiler.compile_brain("editorial", self.root, self.registry)
        self.assertNotIn("state/GENERAL_EDITOR_STATE.md", self.hot_paths(p))
        self.assertIn("state/GENERAL_EDITOR_STATE.md", {r["path"] for r in p["cold_case_law"]})
        self.assertNotIn("pointer state/EDITOR_STATE.md", brain_compiler.canonical_json(p))

    def test_deterministic_and_snapshot_optional(self):
        a = brain_compiler.compile_brain("whole-manuscript dialogue pass", self.root, self.registry, authority_sha="abc")
        b = brain_compiler.compile_brain("whole-manuscript dialogue pass", self.root, self.registry, authority_sha="abc")
        self.assertEqual(brain_compiler.canonical_json(a), brain_compiler.canonical_json(b))
        self.assertEqual("absent", a["routing"]["github_snapshot"])

    def test_snapshot_contradiction_warns(self):
        snap = {"schema":"plg_brain_github_snapshot/v1","authority_sha":"different","branches":[],"pull_requests":[]}
        p = brain_compiler.compile_brain("dialogue", self.root, self.registry, authority_sha="abc", github_snapshot=snap)
        self.assertTrue(any(w["code"] == "authority_sha_conflict" for w in p["warnings"]))

    def test_malformed_registry_and_hot_ceiling_fail_closed(self):
        bad = json.loads(self.registry.read_text())
        bad["schema"] = "wrong"
        self.registry.write_text(json.dumps(bad), encoding="utf-8")
        with self.assertRaises(ValueError): brain_compiler.load_registry(self.registry)

        self.setUp_registry_again = None

    def test_hot_ceiling(self):
        data = json.loads(self.registry.read_text())
        for n in range(20):
            path = f"state/HOT{n}.md"; (self.root/path).write_text("x",encoding="utf-8")
            data["documents"].append({"path":path,"owner":"x","authority_class":"x","default_temperature":"conditional","task_tags":["boom"],"reason":"boom"})
        self.registry.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "HOT"):
            brain_compiler.compile_brain("boom", self.root, self.registry)


if __name__ == "__main__": unittest.main()
