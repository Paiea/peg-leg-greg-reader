# Dialogue Ownership Pass

Purpose: remove cross-character action contamination from dialogue paragraphs without turning the pass into a general prose rewrite.

Authority: exact manuscript prose outranks this ledger. The governing rule lives in `state/editorial/DIALOGUE_ATTRIBUTION_REVIEW_RUBRIC.md`.

## Rule

A dialogue paragraph belongs to its speaker. Independent actions, reactions, expressions, observations, or movement by another character move to that character's paragraph by default.

Preferred repair: **paragraph break first**. Preserve wording unless attribution remains unclear.

Also repair stronger failures exposed during the pass, such as stale/wrong speaker names, impossible character presence, or pronouns resolving to the wrong person.

## Scope

Audit the manuscript from Chapter 1 forward in bounded batches.

Do not use this pass to:
- rewrite dialogue for style;
- compress scenes;
- alter canon;
- improve jokes;
- vary voice merely because a line could be better;
- change paragraphing unrelated to speaker/action ownership.

## Status legend

- `CLEAN` — no ownership violation found.
- `PATCHED` — clear violation found and repaired.
- `REVIEW` — probable issue found but wider context is required before changing prose.

## Batch 001 — Chapters 1-3

### Chapter 1 — THE BOY
Status: `CLEAN` on first ownership read.

No cross-character dialogue/action ownership violation found in the inspected prose. The off-wall neighbor line remains structurally clear because the neighbor's speech is self-contained and Greg's reaction begins after it in narration.

### Chapter 2 — THE BORROWER
Status: `PATCHED` and re-fetched from branch after write.

Repairs shipped to `chapters/002.html`:

1. Greg's `"How much for a cart?"` no longer shares a paragraph with the stall owner's reaction and reply.
2. The stall owner's `"Two silver."` no longer shares a paragraph with Greg's internal reaction.
3. Greg's `"Your age."` no longer carries Antonius's smile and reply.
4. Antonius's `"How much?"` no longer carries Greg naming the number plus the scarred man's reaction.
5. Greg's `"If I had an answer you'd believe..."` no longer carries Antonius denying the loan.
6. Greg's `"Fine."` no longer carries Antonius counting silver.
7. Antonius's `"Eight days, Greg."` no longer carries Greg picking up the coins.
8. Sella's `"Do I know you?"` no longer carries Greg's future-memory narration.
9. Greg's `"You," I said.` no longer carries Sella staring and Greg smiling in one mixed-owner paragraph.

No dialogue wording, canon fact, transaction fact, or scene outcome changed in these repairs.

### Chapter 3 — THE INVESTOR
Status: `REVIEW` with multiple confirmed early hits.

Clear ownership violations already identified in the inspected portion:

1. Arlo says `"For a test? A bucket,"` followed by Greg looking at the cart and the carter looking at Greg in the same paragraph.
2. Greg says `"Possibly," I said.` followed by Arlo setting down the cup in the same paragraph.
3. Greg says `"Everyone guesses. Professionals write the guess down," I said.` followed by Arlo glaring in the same paragraph.
4. Arlo asks `"Where did you get this idea?"` followed by Greg smiling in the same paragraph.
5. Arlo says `"Greg,"` followed by Greg leaning over the bench in the same paragraph.
6. Greg asks `"Cost?"` followed by Arlo naming the number, Greg swearing, and Arlo smiling in the same paragraph.

Stronger attribution failure found in the same Arlo workshop scene:
- several consecutive lines are tagged to **Antonius** even though the scene is with Arlo, followed immediately by an Arlo line about Greg staring at his hands. This appears to be a stale/wrong character-name contamination, not merely paragraph ownership. It must be repaired against full local scene context before shipping the chapter.

## Craft finding

This pass is not cosmetic. A paragraph can be grammatically valid while still lying about conversational ownership. Readers resolve dialogue partly from paragraph boundaries before consciously parsing tags, so wrong-owner action beats create tiny backtracking costs that accumulate across a long manuscript.

## Next edge

Continue full-context repair of Chapter 3, then audit Chapters 4-10.
