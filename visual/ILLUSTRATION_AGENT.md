# Peg-Leg Greg Illustration Production Agent

## Mission
Fill the Illustrated Reader from Chapter 156 through Chapter 320 with 1-3 manuscript-grounded illustrations per chapter while preserving the visual identity of the existing book.

## Authority order
1. Exact chapter prose.
2. Durable character and visual continuity notes.
3. Existing promoted chapter art as style reference.
4. Generated-image aesthetics.

Never let a prettier image overrule manuscript continuity.

## Batch size
Work in five-chapter batches. Read all five exact chapters before generating. Normally target two images per chapter. Use one for a quiet/transitional chapter and three only when the prose contains three genuinely distinct visual beats.

## Style target
The target is a higher-quality continuation of the current Illustrated Reader, not a new art direction: hand-drawn storybook / graphic-novel illustration, visible ink or pencil-like linework, sketch texture, restrained painterly or watercolor-like rendering, warm paper/earth atmosphere when appropriate, readable silhouettes, expressive faces, lived-in fantasy environments. Improve anatomy, hands, faces, perspective, lighting, composition, material detail, and environmental clarity without becoming glossy photorealism, polished 3D concept art, anime, or generic digital fantasy splash art.

## Greg continuity gate
Greg is approximately twenty years old in this run. He may have beard/stubble, but his facial structure must remain youthful. Before canon gives him a prosthetic, do not invent a peg leg or prosthetic. Default Greg compositions to chest-up, waist-up, seated/obscured, over-the-shoulder, or environmental framing where his lower-body configuration and amputation side are not readable. Full-body Greg images require an explicit canon check. Crutches may appear when the chapter makes them important, but they do not require exposing his legs.

## Lyssa continuity gate
Lyssa is Black, tall and thin, with Afro-textured / Afro-ish hair. Preserve this unless exact later prose establishes a change in styling or appearance.

## Scene selection
Every image must map to a real chapter beat. Prefer: (a) establishing/world image, (b) strongest character/action/work image, (c) optional payoff/detail image. Do not invent chapter titles, locations, errands, props, relationships, or scenes merely to create visual variety.

## Generation packet
Before generation record: chapter number/title; insertion anchor; exact scene; characters present; appearance state; mobility state; clothing/props; environment; composition; must-not-appear list; style reminder.

## Acceptance gate
Reject or regenerate if any of these fail: wrong chapter event, wrong recurring-character appearance, wrong age, invented prosthetic/peg leg, unsupported amputation side, major prop/location error, style drift, unreadable anatomy, or redundant image with no new visual function.

## Website handoff
Accepted images receive deterministic chapter/slot identities and a placement entry in `visual/ILLUSTRATION_PLACEMENT.md`. Promote production files under `visual/chapter_art/<chapter>/`. The publishing process should consume the placement manifest rather than requiring a human to rediscover where an image belongs. After promotion, regenerate asset/coverage manifests, rebuild the Illustrated Reader, run reference/navigation checks, and publish only when the batch is clean.

## Completion rule
A chapter is visually complete when it has 1-3 accepted, manuscript-grounded images, every image has a placement anchor, continuity checks pass, the reader references promoted assets only, and the live build contains no broken image references.