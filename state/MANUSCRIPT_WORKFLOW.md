# PEG-LEG GREG — MANUSCRIPT WORKFLOW

This file is a compact routing note for any chat, Codex session, or repository pass touching the active manuscript.

## Permanent files

- Forward manuscript: `state/manuscript/Peg_Leg_Greg_Running_Manuscript.md`
- Manuscript engine method: `state/MANUSCRIPT_ENGINE_PLAYBOOK.md`
- Manuscript state: `state/MANUSCRIPT_STATE.md`
- Project authority / sync rules: `state/PROJECT_STATE.md`
- Chapter index: `state/MANUSCRIPT_CHAPTER_INDEX.md`
- Open threads: `state/OPEN_THREADS.md`
- Economic progression / price calibration: `state/ECONOMY_CONTINUITY.md`

Do not create a new range-stamped running manuscript or chapter-numbered state file for each push. Update these living files in place.

## Authority / merge rule

1. Read current GitHub files first.
2. Newer GitHub-authoritative prose outranks stale overlapping local files.
3. Incoming material may extend the current endpoint, but must not clobber newer edits already present in the repository.
4. Preserve reader UI, artwork, and unrelated repository work unless the task explicitly changes them.
5. Historical range-stamped files may remain as provenance until a deliberate cleanup pass.
6. Exact Chapters 156–219 have been recovered outside GitHub but still require exact-text synchronization into the repository; do not reconstruct them from summaries. Chapter 220 and later are written directly to the permanent file.

## Production model: one chapter, one durable transaction

The WRITING UNIT is one complete chapter.

For normal accepted forward production, the DEFAULT DURABLE SHIPPING UNIT is also one complete chapter.

Do not let several finished chapters accumulate only in chat or other temporary working context. Chapter N is not complete merely because prose was drafted. It is complete when the exact prose, relevant living state, next trailhead, and accepted GitHub authority agree.

A normal chapter transaction looks like:

1. Read current `main`, core manuscript state, and the exact recent prose edge.
2. Read the current executable trailhead from `MANUSCRIPT_STATE.md`.
3. If the chapter contains a meaningful wage, price, purchase, debt movement, bid, fee, or money-driven decision, read `ECONOMY_CONTINUITY.md` and calibrate the amount and Greg's reaction against prior anchors and his current economic stage.
4. Privately identify the light chapter contract and write ONE complete chapter.
5. Give it a LIGHT drafting pass only: clarity, repetition, attribution, paragraph rhythm, continuity, and obvious weak prose.
6. Validate chapter length, title, no-em-dash rule, numerical continuity, protected uncertainty, economic continuity when relevant, and any chapter-specific constraints.
7. Append the exact accepted prose to the SAME permanent running manuscript.
8. Update only the living state/index/open-thread files whose answers materially changed.
9. Put the next executable chapter trailhead in `MANUSCRIPT_STATE.md`.
10. Commit the complete chapter transaction to `main` when the author has authorized normal forward shipping.
11. Re-read current `main` and verify the endpoint before reporting success or drafting the next chapter.

This creates a hard durability boundary between chapters. A chat may continue immediately into Chapter N+1 after Chapter N is verified, but it does so from the new GitHub authority rather than relying on its own memory.

### Money is progression, not purse-state shorthand

When money materially enters a chapter, distinguish cash on hand from earning capacity, assets, debt, and optionality. Greg may be temporarily cash-light without emotionally resetting to early-book poverty.

Economic progression should generally move upward over long spans through better work, stronger access, accumulated assets, greater ability to refuse bad terms, and increasing resilience. Do not create that progression by inflating every ordinary price or multiplying every wage.

A cheap/common price can become less narratively important as Greg progresses. Larger economic stakes should increasingly come from larger or more specialized goods, contracts, travel, tools, materials, magical items, or obligations rather than making bread and ordinary services scale with him.

### Deliberate batches

A multi-chapter batch is an explicit exception, not the default. Use one only when the author asks for it or a specific workflow requires it. Even then, do not leave completed prose vulnerable to chat loss. Use a durable WIP branch/checkpoint between chapters when necessary, preserve chapter boundaries, and do not treat uncommitted chat text as authoritative.

## Chat independence

Previous chat history is optional context, never required authority.

A fresh Manuscript Engine chat should be able to begin with:

`Continue Peg-Leg Greg Manuscript Engine from current GitHub authority.`

It must reconstruct the current endpoint, exact edge, constraints, and next job from GitHub. If the same chat remains alive, the user may simply say `Continue` or `Next chapter` after a successful chapter transaction.

## Drafting is not the heavy prose edit

The Manuscript Engine should produce readable, competent prose, but it should NOT simultaneously run the dedicated DEEP PROSE + SOCIAL TEXTURE EDIT PASS while creating new story.

During forward drafting:

- favor clear, natural paragraphs and varied cadence;
- avoid obvious fragment spam and repetitive AI rhythms;
- preserve character voice and existing social memory;
- use nicknames/running jokes only when they arise naturally from established social behavior;
- repair obvious weak lines when noticed;
- then KEEP MOVING.

Do not repeatedly stop forward production to perfect every paragraph, mine dozens of old chapters for callbacks, manufacture new social roles, or perform manuscript-wide cadence surgery.

The dedicated heavy-edit lane exists for that deeper work. It may later reshape sentences/paragraphs, strengthen social memory, and improve prose substantially while preserving the drafted story.

Think:

FORWARD ENGINE = STORY FIRST, CLEAN ENOUGH TO READ.

HEAVY EDIT = PROSE + SOCIAL TEXTURE + LONGITUDINAL POLISH.

Separating these jobs protects both throughput and quality.

## Checkpoint exceptions

Normal forward chapters ship after each chapter. Use a branch or additional checkpoint discipline when:

- work is broad or risky;
- a manuscript synchronization/recovery operation is underway;
- the author explicitly wants several chapters held for inspection as a unit;
- accepted main must not move yet;
- a chapter cannot be fully verified.

Exact numerical continuity, major arc turns, canon changes, or session-end risk are reasons to checkpoint sooner, never reasons to keep completed prose only in chat.

## Verification before a chapter ship

At minimum verify:

- the intended chapter is present and sequential;
- the final chapter/title endpoint is correct;
- target chapter length meets the current writing target unless intentionally changed;
- NO EM DASHES appear in newly drafted manuscript prose;
- numerical/canon continuity reflects what actually happened;
- any meaningful price/wage/reaction fits `ECONOMY_CONTINUITY.md` and does not accidentally reset Greg's economic progression;
- state/index/open-thread changes do not contradict the prose;
- the next executable trailhead is durable in `MANUSCRIPT_STATE.md`;
- no stale source overwrote newer GitHub authority.

After committing, verify the resulting `main` ref and endpoint again before claiming the chapter is shipped.

## Recovery / mismatch rule

If chat history, a prompt, or a user recollection says Chapter N was completed but current GitHub authority ends at N-1, STOP forward numbering.

1. Search durable branches/checkpoints for exact Chapter N prose and state.
2. If exact N exists durably, recover/integrate it before writing N+1.
3. If exact N does not exist durably, report the synchronization gap.
4. Never reconstruct missing exact prose from summaries, state residue, or chat memory and then pretend it was the lost chapter.

Nothing happened durably until it crossed into GitHub.

## Reader synchronization

The reader is downstream from manuscript authority.

Reader updates do not need to interrupt every chapter. Prefer syncing the reader at deliberate reader checkpoints or when a reader-specific fix is already being shipped.

Do not let reader lag become manuscript loss: exact prose must be durable even when illustrated/static pages have not caught up.

## Re-prompt / trailhead behavior

The detailed chapter-specific steering belongs in `MANUSCRIPT_STATE.md`.

After a chapter is shipped, chat should provide a compact production receipt:

1. chapter number/title;
2. verified word count and em-dash status;
3. commit SHA / verified endpoint;
4. one short note about what materially moved;
5. confirmation that the next chapter trailhead is durable.

A giant chapter-specific re-prompt is not required when the durable trailhead already contains the necessary steering. For human convenience, the generic restart prompt is enough:

`Continue Peg-Leg Greg Manuscript Engine from current GitHub authority.`

## Current edge

Do not trust a static chapter number in this workflow file. Read `state/MANUSCRIPT_STATE.md` and the permanent running manuscript on current `main` for the actual endpoint and next trailhead.
