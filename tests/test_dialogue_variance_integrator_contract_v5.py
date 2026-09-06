import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

import apply_dialogue_variance as adv


class DialogueVarianceLedgerSemanticsTests(unittest.TestCase):
    def test_parse_batch_rejects_malformed_chapter_heading(self):
        note = '''## Chapter X — BROKEN
### Patch 3.V1 — example
Current:
`"Old."`
Replace with:
`"New."`
Reason: test
'''
        with self.assertRaisesRegex(AssertionError, 'malformed Chapter heading'):
            adv.parse_batch(note)

    def test_parse_batch_rejects_duplicate_chapter_sections(self):
        note = '''## Chapter 3 — THREE
### Patch 3.V1 — first
Current:
`"Old."`
Replace with:
`"New."`
Reason: first

## Chapter 3 — THREE AGAIN
### Patch 3.V2 — second
Current:
`"Other old."`
Replace with:
`"Other new."`
Reason: second
'''
        with self.assertRaisesRegex(AssertionError, 'duplicate Chapter 3'):
            adv.parse_batch(note)

    def test_parse_batch_requires_nonempty_reason(self):
        cases = (
            '''## Chapter 3 — THREE
### Patch 3.V1 — missing reason
Current:
`"Old."`
Replace with:
`"New."`
''',
            '''## Chapter 3 — THREE
### Patch 3.V1 — empty reason
Current:
`"Old."`
Replace with:
`"New."`
Reason:
''',
        )
        for note in cases:
            with self.subTest(note=note), self.assertRaisesRegex(AssertionError, 'Reason'):
                adv.parse_batch(note)

    def test_parse_batch_rejects_true_noop_patch(self):
        note = '''## Chapter 3 — THREE
### Patch 3.V1 — noop
Current:
`"Same."`
Replace with:
`"Same."`
Reason: should not exist
'''
        with self.assertRaisesRegex(AssertionError, 'no-op'):
            adv.parse_batch(note)

    def test_parse_batch_rejects_replacement_ellipsis_marker(self):
        note = '''## Chapter 3 — THREE
### Patch 3.V1 — ambiguous replacement
Current:
`"Old."`
Replace with:
`"New."`
`...`
Reason: replacement ellipsis is ambiguous
'''
        with self.assertRaisesRegex(AssertionError, 'replacement.*ellipsis'):
            adv.parse_batch(note)


if __name__ == '__main__':
    unittest.main()
