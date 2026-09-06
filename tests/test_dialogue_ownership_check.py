import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.dialogue_ownership_check import inspect_text

SCRIPT = ROOT / "scripts" / "dialogue_ownership_check.py"


def finding_pairs(text: str):
    return [(finding.severity, finding.code) for finding in inspect_text(text, chapter=500)]


class DialogueOwnershipCheckTests(unittest.TestCase):
    def test_same_owner_dialogue_and_action_is_clean(self):
        self.assertEqual(finding_pairs('"Fine," Antonius said. He counted the silver.'), [])

    def test_greg_other_greg_is_error(self):
        self.assertIn(
            ("error", "mixed_explicit_owners"),
            finding_pairs('"You," I said. She stared. I smiled.'),
        )

    def test_leave_and_return_is_error(self):
        text = '"How much?" Antonius asked. I named the number. Jorren laughed. Antonius looked at me. "Collateral?"'
        self.assertIn(("error", "mixed_explicit_owners"), finding_pairs(text))

    def test_two_named_non_greg_owners_is_error(self):
        self.assertIn(
            ("error", "mixed_explicit_owners"),
            finding_pairs('"Enough," Antonius said. Jorren laughed.'),
        )

    def test_descriptive_actor_is_error(self):
        self.assertIn(
            ("error", "mixed_explicit_owners"),
            finding_pairs('"How much?" Antonius asked. The man with the scar laughed.'),
        )

    def test_smart_quotes_are_detected(self):
        self.assertIn(
            ("error", "mixed_explicit_owners"),
            finding_pairs('Alden said, “You really were bad.” I looked at him.'),
        )

    def test_other_speaker_plus_greg_interior_is_error(self):
        self.assertIn(
            ("error", "mixed_explicit_owners"),
            finding_pairs('“Do I know you?” Sella asked. I knew her future immediately.'),
        )

    def test_ambiguous_pronoun_is_review(self):
        self.assertIn(
            ("review", "ambiguous_pronoun_owner"),
            finding_pairs('"Fine," Antonius said. He looked at him.'),
        )

    def test_unbalanced_quotes_are_review(self):
        self.assertIn(
            ("review", "unbalanced_quotes"),
            finding_pairs('ring the bell and bar the hall...” Different words.'),
        )

    def test_formatted_quoted_block_is_review(self):
        self.assertIn(
            ("review", "formatted_or_embedded_quote"),
            finding_pairs('**The note said, "Again?" He left.**'),
        )

    def test_narration_without_dialogue_is_ignored(self):
        self.assertEqual(finding_pairs('Antonius crossed the room. Jorren laughed.'), [])

    def test_separate_rapid_dialogue_paragraphs_are_clean(self):
        text = '"Fine," Antonius said.\n\nI nodded.\n\n"Good," he said.'
        self.assertNotIn(("error", "mixed_explicit_owners"), finding_pairs(text))

    def test_strict_cli_fails_on_latest_review_or_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manuscript = root / "state/manuscript/Peg_Leg_Greg_Running_Manuscript.md"
            manuscript.parent.mkdir(parents=True)
            manuscript.write_text(
                '# CHAPTER 500\n\n## THE TEST\n\n"Fine," Antonius said. Jorren laughed.\n',
                encoding="utf-8",
            )
            (root / "state/manuscript/Peg_Leg_Greg_Recovered_Ch156-219_EXACT.md").write_text("", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--latest", "--strict", "--json", "--root", str(root)],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
            self.assertNotEqual(result.returncode, 0)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["chapters"], [500])
            self.assertGreaterEqual(payload["error_count"], 1)


if __name__ == "__main__":
    unittest.main()
