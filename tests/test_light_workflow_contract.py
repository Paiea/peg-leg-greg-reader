from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / '.github' / 'workflows' / 'light-edition.yml'


class LightEditionWorkflowContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = WORKFLOW.read_text(encoding='utf-8')

    def test_uses_current_checkout_action(self):
        self.assertIn('uses: actions/checkout@v7', self.text)
        self.assertNotIn('uses: actions/checkout@v4', self.text)

    def test_uses_current_setup_python_action(self):
        self.assertIn('uses: actions/setup-python@v7', self.text)
        self.assertNotIn('uses: actions/setup-python@v5', self.text)

    def test_reader_build_has_hard_timeout(self):
        self.assertIn('timeout-minutes: 15', self.text)

    def test_generated_commit_uses_canonical_actions_bot_email(self):
        self.assertIn(
            "git config user.email '41898282+github-actions[bot]@users.noreply.github.com'",
            self.text,
        )
        self.assertNotIn(
            "git config user.email '4189826+github-actions[bot]@users.noreply.github.com'",
            self.text,
        )

    def test_generated_push_retries_main_races(self):
        required = (
            'for attempt in 1 2 3; do',
            'git fetch origin main',
            'git rebase origin/main',
            'git push origin HEAD:main && exit 0',
            'git rebase --abort || true',
            'sleep $((attempt * 2))',
        )
        for fragment in required:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, self.text)


if __name__ == '__main__':
    unittest.main()
