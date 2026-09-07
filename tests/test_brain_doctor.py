import json, tempfile, unittest
from pathlib import Path
from scripts import brain_doctor

class BrainDoctorTests(unittest.TestCase):
    def test_doctor_reports_missing_unregistered_and_is_read_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); (root/'state/brain').mkdir(parents=True); (root/'state').mkdir(exist_ok=True)
            (root/'AGENTS.md').write_text('router',encoding='utf-8'); (root/'state/PROJECT_STATE.md').write_text('project',encoding='utf-8'); (root/'state/MANUSCRIPT_STATE.md').write_text('m',encoding='utf-8'); (root/'state/EXTRA.md').write_text('extra',encoding='utf-8')
            reg={"schema":"plg_brain_routing/v1","project":{"authority":"main","canon":"manuscript prose","root_router":"AGENTS.md","project_state":"state/PROJECT_STATE.md","manuscript_owner":"state/MANUSCRIPT_STATE.md","engines":["01","02","03","04"]},"tag_aliases":{},"exclusive_task_tags":[],"discovery":{"include_globs":["state/*.md"],"ignore_globs":[]},"documents":[{"path":"AGENTS.md","owner":"project","authority_class":"router","default_temperature":"hot","task_tags":[],"reason":"router","universal":True},{"path":"state/PROJECT_STATE.md","owner":"project","authority_class":"state","default_temperature":"hot","task_tags":[],"reason":"project","universal":True},{"path":"state/MISSING.md","owner":"x","authority_class":"x","default_temperature":"conditional","task_tags":["x"],"reason":"missing"}],"workstreams":[]}
            rp=root/'state/brain/ROUTING_REGISTRY.json'; rp.write_text(json.dumps(reg),encoding='utf-8')
            before={p.relative_to(root).as_posix():p.read_bytes() for p in root.rglob('*') if p.is_file()}
            report=brain_doctor.run_doctor(root,rp)
            after={p.relative_to(root).as_posix():p.read_bytes() for p in root.rglob('*') if p.is_file()}
            self.assertEqual(before,after); self.assertTrue(any(x['code']=='missing_registered_path' for x in report['errors'])); self.assertTrue(any(x['code']=='unregistered_brain_file' for x in report['advisories']))

    def test_exclusive_owner_collision_is_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); (root/'state/brain').mkdir(parents=True); (root/'AGENTS.md').write_text('x'); (root/'state/PROJECT_STATE.md').write_text('x'); (root/'state/MANUSCRIPT_STATE.md').write_text('x')
            reg={"schema":"plg_brain_routing/v1","project":{"authority":"main","canon":"manuscript prose","root_router":"AGENTS.md","project_state":"state/PROJECT_STATE.md","manuscript_owner":"state/MANUSCRIPT_STATE.md","engines":["01","02","03","04"]},"tag_aliases":{},"exclusive_task_tags":["dialogue-owner"],"discovery":{"include_globs":[],"ignore_globs":[]},"documents":[{"path":"AGENTS.md","owner":"p","authority_class":"router","default_temperature":"hot","task_tags":[],"reason":"r","universal":True},{"path":"state/PROJECT_STATE.md","owner":"p","authority_class":"state","default_temperature":"hot","task_tags":[],"reason":"p","universal":True}],"workstreams":[{"id":"a","status":"ACTIVE","task_tags":["dialogue"],"owner_tags":["dialogue-owner"],"owner_path":"state/PROJECT_STATE.md","reason":"a"},{"id":"b","status":"ACTIVE","task_tags":["dialogue"],"owner_tags":["dialogue-owner"],"owner_path":"state/PROJECT_STATE.md","reason":"b"}]}
            rp=root/'state/brain/ROUTING_REGISTRY.json'; rp.write_text(json.dumps(reg),encoding='utf-8')
            report=brain_doctor.run_doctor(root,rp); self.assertTrue(any(x['code']=='exclusive_owner_collision' for x in report['errors']))

if __name__=='__main__': unittest.main()
