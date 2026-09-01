# PEG-LEG GREG — LIGHT EDITION STATE

Durable publishing memory for the text-first reader. Exact manuscript authority outranks this file.

## PURPOSE

The public reader has two intentional modes:

- **ILLUSTRATED** — normal book-like static chapter pages with accepted art when available.
- **LIGHT** — fast text-first static publishing derivatives with no chapter illustrations.

Neither reader surface is manuscript authority.

## SOURCE AUTHORITY

Generation preserves the established exact-source split:

- Published Chapters 1–155: exact prose can be extracted from `chapters/NNN.html` for Light backfill, stripping only illustration/presentation markup.
- Chapters 156–219: `state/manuscript/Peg_Leg_Greg_Recovered_Ch156-219_EXACT.md`.
- Chapters 220+: `state/manuscript/Peg_Leg_Greg_Running_Manuscript.md`.

Do not reconstruct missing prose from summaries or compact state.

The publisher supports Chapter 232's exact legacy combined heading form:

`## Chapter 232 — THE COUNTERSIGN`

The manuscript itself does not need to be rewritten to satisfy the reader generator.

## CURRENT ARCHITECTURE

Generator:

`python scripts/generate_light.py <range>`

Supported forms:

- `current` — all Chapter 220+ prose actually present in the permanent running manuscript
- `N-N` — strict bounded exact range, such as `156-219`

Bounded generation fails if a requested source chapter is absent.

Generated namespace:

- `light/index.html` — Book -> Act Light contents
- `light/NNN.html` — static Light chapters
- `light/manifest.json` — generated metadata and exact current endpoint
- `latest.html` — newest exact Light-publishable chapter

Light numeric derivatives whose source chapter disappears are pruned rather than left publicly stale.

`python scripts/verify_light.py <range>` checks title, prose, navigation, manifest coverage, latest routing, absence of images, and source alignment.

Previous/Next navigation is numerically gap-aware and may not silently jump over a missing exact chapter.

Legacy `light.html?chapter=N` remains the compatibility path for old ranges that have not yet been statically backfilled.

## CURRENT VERIFIED COVERAGE

At the current reader checkpoint:

- static Light Chapters 156–219 come from recovered exact authority
- static Light Chapter 220+ follows the permanent running manuscript automatically
- after reconciliation with fresh `main`, the verified Light endpoint is Chapter **238 — THE TAG**
- continuous static Light coverage is **156–238** at this checkpoint
- always re-read current manuscript authority because the forward engine may advance again

The Illustrated normal reader is independently static through Chapter **235 — THE TAGALONG**.

That difference is intentional. Current prose does not wait for Illustrated expansion.

## BOOK -> ACT CONTENTS

Light and Illustrated share the same logical Book/Act structure.

### BOOK I — Chapters 1–82

1. **ACT I — THE SECOND LIFE** — 1–20
2. **ACT II — MAKING A PLACE** — 21–63
3. **ACT III — THE NEW BASELINE** — 64–82

### BOOK II — Chapter 83 onward

1. **ACT I — A LIFE IN CARROW** — 83–111
2. **ACT II — THE STAGE DOOR** — 112–137
3. **ACT III — THE COMPANY ROAD** — 138–180
4. **ACT IV — THE WORKING COMPANY** — 181–217
5. **ACT V — THE PRICE OF ATTENTION** — 218–current

These are content/state boundaries, not equal numeric buckets.

Light renders the same logical hierarchy but intentionally omits the Illustrated reader's Book hero images.

The active Book II and Act V range labels expand automatically as exact forward prose appears.

Do not create a new Act merely because the chapter count grows. New boundaries require actual story progression.

## ILLUSTRATED CROSS-MODE STATE

The normal Illustrated reader now has an approved generated expansion architecture for Chapters 156–235:

- 156–219 from recovered exact authority
- 220–235 from the running manuscript
- static normal-reader pages may exist before art is available
- each generated Illustrated chapter links to its corresponding static Light chapter
- Chapter 155 connects directly to 156
- 219 <-> 220 is a normal direct source seam
- Chapter 235 intentionally has no Illustrated Next link until the bounded Illustrated range is explicitly advanced
- newer Light chapters such as 236+ remain readable without forcing Illustrated production to move in lockstep

Promoted figures on generated Illustrated pages are preserved across regeneration by exact paragraph anchors. If an edit invalidates an anchor, generation fails for deliberate art repositioning rather than silently losing the figure.

## AUTOMATION

`.github/workflows/light-edition.yml` is now the shared reader-editions workflow.

It:

1. materializes managed reader presentation CSS;
2. runs the full reader tooling test suite;
3. generates bounded Illustrated Chapters 156–235;
4. generates recovered Light Chapters 156–219;
5. regenerates current Light Chapter 220+ from exact running authority;
6. updates Book/Act contents and cross-mode navigation;
7. verifies source integrity and the 155 -> 156 and 219 <-> 220 seams;
8. verifies Illustrated does not silently spill into Chapters 236+;
9. verifies Light contains no chapter images or manuscript-path leakage;
10. keeps `latest.html` tied to actual exact current prose;
11. commits generated reader derivatives when needed.

When `main` advances concurrently, preserve the newer main tree, overlay only reader source/tool changes, and rerun this full workflow before review or merge.

## PRESENTATION RULES

Light should feel like a deliberate novel edition, not a manuscript/debug utility.

- no chapter images
- no GitHub/manuscript-authority jargon in reader-facing copy
- clear HOME / ILLUSTRATED / LIGHT / LATEST / ART navigation
- previous / chapters / next on chapter pages
- comfortable text measure and mobile margins
- Book -> Act contents hierarchy
- direct chapter links where static pages exist
- preserve the Illustrated edition rather than replacing it
- no Book hero plates in Light

## REMAINING OLD-RANGE STATIC BACKFILL

Completed static Light coverage:

1. current Chapter 220+ architecture
2. recovered Chapters 156–219

Next useful bounded backfill remains:

3. Chapters 100–155 from exact Illustrated chapter prose

Then, if still worthwhile:

4. Chapters 83–99
5. Chapters 1–82

Current content must never wait for old-range completion.

## SAFETY

- Do not edit manuscript prose from the reader lane.
- Do not make generated HTML a competing manuscript.
- Do not regenerate or destructively alter illustrations as a Light side effect.
- Do not delete the compatibility router until static old-range coverage is sufficient.
- Keep generated chapter number/title/prose aligned to exact source authority.
- Re-render generated neighbors when adding a static range so navigation seams become direct.
- Exact prose outranks this compact endpoint note.
- Do not extend the bounded Illustrated range merely because Light/current advanced.

## RE-PROMPT [READER]

Continue Peg-Leg Greg reader publishing from fresh current GitHub authority. Read `AGENTS.md`, `state/MANUSCRIPT_STATE.md`, `state/LIGHT_EDITION_STATE.md`, `state/READER_DESIGN_LAB.md`, current reader scripts/workflow, and exact prose authority. Preserve the shared Book -> Act contents hierarchy and the intentional split between Light=current and Illustrated=bounded/art-forward. Re-run current Light from the actual running manuscript before trusting a compact endpoint. The approved generated Illustrated range is 156–235 unless explicitly advanced. For the next Light backfill, generate and verify Chapters 100–155 from exact published Illustrated prose, stripping images without rewriting text; pressure-test the 155 -> 156 seam and compatibility responsibility afterward. Do not edit prose or art as a reader side effect.
