# READER / VISUAL STATE

Compact durable state for the public reader, illustration coverage, and presentation work.

## Authority

- Reader/UI work must not overwrite newer manuscript authority.
- Use the newest shipped manuscript/repository state as the base and port forward only compatible reader changes.

## Presentation direction

- preserve chapter URLs, numbering, prose, typography, architecture, and mobile behavior
- keep low-resolution illustrations at sensible intrinsic sizes
- allow genuinely high-resolution art to display larger
- remove obvious accidental seams or edge strips
- use lightweight Act grouping only where story transitions support it
- do not force full-bleed presentation across mixed-resolution art

## Illustration north star

Fill the illustrated reader first. Upgrade it later.

Target: one to three illustrations per chapter, ideally three when the chapter supports it.

Prioritize:
1. zero-image chapters
2. one-image chapters
3. clearly weak or mismatched art
4. second/third images where useful
5. replacement only when materially better

Assume movement unless deliberate stillness is the point. Vary camera angle, distance, direction, foreground, eyelines, environment, and physical action.

Reject only major failures: wrong identity/skin tone, Greg disability contradiction, severe anatomy failure, major scene contradiction, or absurd prop/location substitution.

## Composite workflow

Default fast-production unit: 5 × 5 contact sheet.

Each accepted panel should be independently usable and mapped deterministically through a compact manifest. Keep/retry status should control integration automatically.

## Current repository endpoint

_Update after the active manuscript lane finishes its next ship. Do not hard-code an older endpoint while another lane is advancing the manuscript._

## Current image coverage

_Recalculate from actual current chapter HTML before the next production wave._

## Pending portable work

- light reader/UI sizing and presentation pass
- generic contact-sheet integration scripts/tests, after review
- salvage compatible older art only after checking current chapter state

## Validation

Before publishing reader changes, verify chapter order, endpoint, navigation, image references, relative paths, build integrity, and no accidental manuscript rewrites.
