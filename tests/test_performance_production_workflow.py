import json
import re
import unittest

from scripts import performance_production_funnel as funnel


class PerformanceProductionWorkflowTests(unittest.TestCase):
    def test_push_workflow_runs_compiler_smoke_outside_persistent_state(self):
        workflow = (funnel.ROOT / ".github" / "workflows" / "performance-production-funnel.yml").read_text(encoding="utf-8")
        self.assertIn("--compile-chapter 7", workflow)
        self.assertIn("--output-root /tmp/performance-compiler-smoke", workflow)
        self.assertNotIn("git add /tmp/performance-compiler-smoke", workflow)

    def test_legacy_batch_apply_is_manual_dispatch_only(self):
        workflow = (funnel.ROOT / ".github" / "workflows" / "performance-production-funnel.yml").read_text(encoding="utf-8")
        match = re.search(r"- name: Apply earned PERFORMANCE survivors\n(?P<body>(?:\s+.*\n){1,5})", workflow)
        self.assertIsNotNone(match)
        self.assertIn("github.event_name == 'workflow_dispatch'", match.group("body"))

    def test_generated_prose_em_dash_check_uses_prose_extraction(self):
        workflow = (funnel.ROOT / ".github" / "workflows" / "performance-production-funnel.yml").read_text(encoding="utf-8")
        self.assertIn("extract_paragraphs", workflow)

    def test_replacement_audit_begins_as_evidence_queue_not_cleanup_authority(self):
        path = funnel.ROOT / "state" / "editorial" / "performance-production" / "REPLACEMENT_AUDIT.json"
        self.assertTrue(path.exists())
        audit = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual("performance_replacement_audit/v1", audit["schema"])
        self.assertGreaterEqual(len(audit["candidates"]), 5)
        self.assertTrue(all(candidate["replacement_proven"] is False for candidate in audit["candidates"]))
        self.assertTrue(all("surface" in candidate and "status" in candidate for candidate in audit["candidates"]))


if __name__ == "__main__":
    unittest.main()
