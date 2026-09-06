import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import dialogue_variance_integration as dvi


class DialogueVarianceIntegrationTests(unittest.TestCase):
    def test_parses_numbered_chapter_and_v_patch_syntax(self):
        batch = '''## Chapter 3 — THE INVESTOR

### Patch 3.V1 — opening cart exchange

Current:
`"You actually bought it," Arlo said.`
`"I said I would," I told him.`

Replace with:
`"You actually bought it," Arlo said.`
`He looked past me at the cart.`
`"I thought you meant enough to test."`

Reason: preserve Greg's joke ownership.
'''
        patches = dvi._parse_variance_batch(batch, "variance.md", 3, 3)
        self.assertEqual(1, len(patches))
        self.assertEqual(3, patches[0].chapter)
        self.assertEqual('"I thought you meant enough to test."', patches[0].replacement[-1])

    def test_parses_legacy_blockquote_patch_and_folds_wrapped_paragraphs(self):
        batch = '''## Chapter 157 - THE TABLE

### Patch 157.V1 - let the missing object carry the exchange

Current:

> Iven appeared in debtor clothes.
>
> No coat again.
>
> "Don't."

Replace with:

> Iven appeared in debtor clothes.
>
> No coat again.
>
> "The coat is gone."
> "I see that."

Reason:

The coat is visible evidence.

## Chapter 158 - THE RETURNER

### Patch 158.V1 - wrapped paragraph

Current:

> Rinna counted coins into two piles, moved three from one to the other,
> then covered both when Marek came near.
>
> "I wasn't."

Replace with:

> Rinna counted coins into two piles, moved three from one to the other,
> then covered both when Marek came near.
>
> "Do not make me count these again."

Reason:

Keep the work object visible.
'''
        patches = dvi._parse_variance_batch(batch, "variance.md", 157, 158)
        self.assertEqual(2, len(patches))
        self.assertEqual(("Iven appeared in debtor clothes.", "No coat again.", '"Don\'t."'), patches[0].current)
        self.assertEqual('"The coat is gone." "I see that."', patches[0].replacement[-1])
        self.assertEqual(
            "Rinna counted coins into two piles, moved three from one to the other, then covered both when Marek came near.",
            patches[1].current[0],
        )

    def test_injects_metadata_reason_for_approved_legacy_patch_that_omits_it(self):
        batch = '''## 405 THE EARNER

405.V1
Current:
`Sori watched my face.`
`"Don't."`

Replace:
`Sori watched me put the pouch away.`
`"Don't."`

405.V2
Current:
`Dask stopped walking.`
`Sori said, "Don't."`

Replace:
`Dask stopped walking.`
`Sori said, "Walk."`

Keep Greg's later inversion. Greg owns the compressed architecture.
'''
        patches = dvi._parse_variance_batch(batch, "variance.md", 405, 405)
        self.assertEqual(2, len(patches))
        self.assertEqual("405.V1", patches[0].label)
        self.assertEqual(("Sori watched me put the pouch away.", '"Don\'t."'), patches[0].replacement)
        self.assertEqual("405.V2", patches[1].label)
        self.assertEqual(('Dask stopped walking.', 'Sori said, "Walk."'), patches[1].replacement)

    def test_normalizes_inline_slash_current_and_replace_sequences(self):
        batch = '''## 406 THE CONTRACTOR

406.V1
Current: `"You enjoyed that too much." / "No." / "Everyone has face today."`
Replace: `"You enjoyed that too much." / "No." / "That was an enthusiastic good."`
Reason: Nema reacts to Dask's spoken word.
'''
        patches = dvi._parse_variance_batch(batch, "variance.md", 406, 406)
        self.assertEqual(1, len(patches))
        self.assertEqual(
            ('"You enjoyed that too much."', '"No."', '"Everyone has face today."'),
            patches[0].current,
        )
        self.assertEqual(
            ('"You enjoyed that too much."', '"No."', '"That was an enthusiastic good."'),
            patches[0].replacement,
        )

    def test_trailing_editorial_current_line_cannot_become_duplicate_patch_metadata(self):
        batch = '''## 422 THE TEMP

422.V1
Current:
`Trial shell sat there.`
`"Your face did."`

Replace with:
`Trial shell sat there.`
`"No shell today."`

Reason: Masta owns the wear schedule.

## Totals

- Dialogue-variance patches: 1

## Next edge

Current `main` authority: **1-429**.
Next edge: **430**.
'''
        patches = dvi._parse_variance_batch(batch, "variance.md", 422, 422)
        self.assertEqual(1, len(patches))
        self.assertEqual("422.V1", patches[0].label)
        self.assertEqual(('Trial shell sat there.', '"No shell today."'), patches[0].replacement)

    def test_normalizes_late_bare_heading_patch_and_pov_repairs(self):
        batch = '''## 430 THE RECORDER

430.V1
Current:
`Halen inspected.`
`Toll inspected.`
`Second pass?`
`Jorren asked with face only.`
`Enna said, "No."`

Replace with:
`Halen inspected.`
`Toll inspected.`
`Jorren looked from the repaired shoulder to the test wagon.`
`Enna said, "No."`

Reason: visible object-directed gaze is enough.

POV/referent repairs:
- `Did not need Greg wonder.` -> `I did not need to wonder.`
- `Not Greg.` -> `Not me.`
- `No Greg heroics.` -> `No heroics from me.`
'''
        patches = dvi._parse_variance_batch(batch, "variance.md", 430, 430)
        self.assertEqual(4, len(patches))
        self.assertEqual("430.V1", patches[0].label)
        self.assertEqual(("Did not need Greg wonder.",), patches[1].current)
        self.assertEqual(("I did not need to wonder.",), patches[1].replacement)
        self.assertEqual(("No heroics from me.",), patches[-1].replacement)

    def test_merge_order_keeps_attribution_before_variance(self):
        attr = [dvi.IntegrationPatch(3, "Fix 3-A", ("A",), ("B",), "attr.md", kind="attribution")]
        var = [dvi.IntegrationPatch(3, "3.V1", ("B",), ("C",), "variance.md")]
        merged = dvi.merge_patch_sets(attr, var)
        self.assertEqual(["attr.md", "variance.md"], [patch.source_file for patch in merged])

    def test_markdown_authority_gets_exact_patch_without_touching_other_chapter(self):
        source = '''# CHAPTER 220
## THE FIRST

Before.

"Old."

After.

# CHAPTER 221
## THE SECOND

"Old."
'''
        patch = dvi.IntegrationPatch(220, "220.V1", ('"Old."',), ('"New."',), "variance.md")
        stats = {"attribution": dvi.Stats(), "variance": dvi.Stats()}
        conflicts = []
        updated, changed = dvi.apply_patches_to_markdown_chapter(source, 220, [patch], stats, conflicts)
        self.assertTrue(changed)
        self.assertEqual(1, updated.count('"New."'))
        self.assertEqual(1, updated.count('"Old."'))
        self.assertEqual([], conflicts)

    def test_markdown_patch_preserves_unrelated_soft_wraps_byte_for_byte(self):
        source = '''# CHAPTER 220
## THE FIRST

This paragraph is deliberately wrapped across
multiple source lines and must stay that way.

"Old line."

Another wrapped paragraph stays
exactly wrapped too.

# CHAPTER 221
## THE SECOND

Untouched.
'''
        patch = dvi.IntegrationPatch(220, "220.V1", ('"Old line."',), ('"New line."',), "variance.md")
        stats = {"attribution": dvi.Stats(), "variance": dvi.Stats()}
        conflicts = []
        updated, changed = dvi.apply_patches_to_markdown_chapter(source, 220, [patch], stats, conflicts)
        self.assertTrue(changed)
        self.assertIn("This paragraph is deliberately wrapped across\nmultiple source lines and must stay that way.", updated)
        self.assertIn("Another wrapped paragraph stays\nexactly wrapped too.", updated)
        self.assertEqual(source.replace('"Old line."', '"New line."'), updated)

    def test_markdown_match_tolerates_soft_wrap_inside_approved_paragraph(self):
        source = '''# CHAPTER 220
## THE FIRST

Rinna counted coins into two piles, moved three from one to the other,
then covered both when Marek came near.

"I wasn't."
'''
        patch = dvi.IntegrationPatch(
            220,
            "220.V1",
            ("Rinna counted coins into two piles, moved three from one to the other, then covered both when Marek came near.", '"I wasn\'t."'),
            ("Rinna counted coins into two piles, moved three from one to the other, then covered both when Marek came near.", '"Do not make me count these again."'),
            "variance.md",
        )
        stats = {"attribution": dvi.Stats(), "variance": dvi.Stats()}
        conflicts = []
        updated, changed = dvi.apply_patches_to_markdown_chapter(source, 220, [patch], stats, conflicts)
        self.assertTrue(changed)
        self.assertIn('"Do not make me count these again."', updated)
        self.assertNotIn('"I wasn\'t."', updated)
        self.assertEqual([], conflicts)

    def test_stale_patch_is_flagged_and_does_not_overwrite_current_prose(self):
        page = '<article class="prose"><p>Newer manuscript prose.</p></article>'
        patch = dvi.IntegrationPatch(3, "3.V1", ("Old prose.",), ("Approved replacement.",), "variance.md")
        stats = {"attribution": dvi.Stats(), "variance": dvi.Stats()}
        conflicts = []
        updated = dvi.apply_patches_to_html(page, [patch], stats, conflicts)
        self.assertEqual(page, updated)
        self.assertEqual(1, stats["variance"].stale)
        self.assertEqual(1, len(conflicts))
        self.assertNotIn("Approved replacement.", updated)


if __name__ == "__main__":
    unittest.main()
