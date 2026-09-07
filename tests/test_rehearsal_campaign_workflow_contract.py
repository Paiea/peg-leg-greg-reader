import unittest
from pathlib import Path


class RehearsalCampaignWorkflowContractTests(unittest.TestCase):
    def test_queue_workflow_is_serial_and_uses_existing_return_gate(self):
        path = Path(__file__).resolve().parents[1] / ".github" / "workflows" / "rehearsal-campaign-queue.yml"
        text = path.read_text(encoding="utf-8")
        self.assertIn("concurrency:", text)
        self.assertIn("cancel-in-progress: false", text)
        self.assertIn("scripts/compile_rehearsal_campaign_returns.py", text)
        self.assertIn("scripts/apply_rehearsal_returns.py", text)
        self.assertIn("scripts/rehearsal_campaign_queue.py", text)
        self.assertIn("performance_roundtrip_references.py --check", text)
        self.assertIn("project_check.py showcase", text)
        self.assertIn("git diff --check", text)

    def test_queue_workflow_never_skips_failed_validation(self):
        path = Path(__file__).resolve().parents[1] / ".github" / "workflows" / "rehearsal-campaign-queue.yml"
        text = path.read_text(encoding="utf-8")
        self.assertNotIn("continue-on-error: true", text)
        self.assertIn("Settle queue only after validation", text)
        self.assertIn("Block queue on failure", text)


if __name__ == "__main__":
    unittest.main()
