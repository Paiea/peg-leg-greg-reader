from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / '.github' / 'workflows' / 'light-edition.yml'
SHOWCASE_WORKFLOW = ROOT / '.github' / 'workflows' / 'showcase-canon.yml'


class ShowcasePublishWorkflowTests(unittest.TestCase):
    def test_main_reader_workflow_triggers_on_showcase_curation(self):
        text = WORKFLOW.read_text(encoding='utf-8')
        self.assertIn("- 'publishing/showcase_chapters.json'", text)
        self.assertIn("- 'scripts/update_showcase_chapter_shells.py'", text)
        self.assertIn("- 'scripts/cleanup_showcase_light.py'", text)

    def test_main_reader_workflow_applies_showcase_before_verification(self):
        text = WORKFLOW.read_text(encoding='utf-8')
        self.assertIn('python scripts/cleanup_showcase_light.py', text)
        self.assertIn('python scripts/update_showcase_chapter_shells.py', text)
        self.assertIn('python scripts/project_check.py showcase', text)

    def test_reader_workflow_has_no_canonical_number_assertions_that_break_after_hiding(self):
        text = WORKFLOW.read_text(encoding='utf-8')
        self.assertNotIn("grep -q 'href=\"220.html\"' light/219.html", text)
        self.assertNotIn("grep -q 'href=\"219.html\"' light/220.html", text)
        self.assertNotIn("grep -q 'TEXT READER · CHAPTER 220' light/220.html", text)

    def test_showcase_ci_watches_publish_helpers_and_frontier_verifier(self):
        text = SHOWCASE_WORKFLOW.read_text(encoding='utf-8')
        for path in (
            'scripts/update_showcase_chapter_shells.py',
            'scripts/cleanup_showcase_light.py',
            'scripts/verify_reader_frontier.py',
        ):
            with self.subTest(path=path):
                self.assertIn(path, text)


if __name__ == '__main__':
    unittest.main()
