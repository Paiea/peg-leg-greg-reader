# PEG-LEG GREG — MANUSCRIPT WORKFLOW

This file is a compact routing note for any chat, Codex session, or repository pass touching the active manuscript.

## Permanent files

- Forward manuscript: `state/manuscript/Peg_Leg_Greg_Running_Manuscript.md`
- Manuscript engine method: `state/MANUSCRIPT_ENGINE_PLAYBOOK.md`
- Manuscript state: `state/MANUSCRIPT_STATE.md`
- Project authority / sync rules: `state/PROJECT_STATE.md`
- Chapter index: `state/MANUSCRIPT_CHAPTER_INDEX.md`
- Open threads: `state/OPEN_THREADS.md`

Do not create a new range-stamped running manuscript or chapter-numbered state file for each push. Update these living files in place.

## Authority / merge rule

1. Read current GitHub files first.
2. Newer GitHub-authoritative prose outranks stale overlapping local files.
3. Incoming material may extend the current endpoint, but must not clobber newer edits already present in the repository.
4. Preserve reader UI, artwork, and unrelated repository work unless the task explicitly changes them.
5. Historical range-stamped files may remain as provenance until a deliberate cleanup pass.
6. Exact Chapters 156–219 have been recovered outside GitHub but still require exact-text synchronization into the repository; do not reconstruct them from summaries. Chapter 220 and later are written directly to the permanent file.

## Production model: one chapter at a time, ship in small batches

The WRITING UNIT is one chapter.

The DEFAULT SHIPPING UNIT is a small batch, usually 3–5 completed chapters unless the author asks for a different cadence or a chapter contains a reason to checkpoint immediately.

Do not draft five chapters as one undifferentiated block. Complete Chapter N, then Chapter N+1, preserving the ability to stop, inspect, or redirect between chapters.

A normal batch looks like:

1. Read current authority and batch trailhead.
2. Write ONE complete chapter.
3. Give it a LIGHT drafting pass only: clarity, repetition, attribution, paragraph rhythm, continuity, and obvious weak prose.
4. Record compact temporary batch notes so the next chapter inherits what actually happened.
5. Write the next chapter.
6. Repeat until roughly 3–5 chapters are complete or a natural stopping point appears.
7. Before shipping, inspect the batch as a sequence for continuity, repeated openings, accidental resets, title collisions, magic/money/threat facts, and obvious prose problems.
8. Ship the completed batch to the SAME living manuscript and state files.
9. Update durable state from the batch endpoint and important residue, not by writing a full state ceremony for every chapter.
10. Verify the shipped endpoint and leave the next trailhead.

This keeps GitHub durable without forcing the Manuscript Engine to interrupt its story flow after every chapter.

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

## Batch checkpoint exceptions

Ship earlier than 3–5 chapters when:

- canon changes materially;
- exact numerical continuity changes and would be dangerous to lose;
- a major arc turns;
- the author explicitly wants to inspect a chapter;
- the session may end before the batch finishes;
- repository synchronization risk makes an earlier checkpoint safer.

It is also fine to let a batch run a little longer when the story is flowing and the state is stable. The 3–5 chapter cadence is a default, not a rigid quota.

## Verification before a batch ship

At minimum verify:

- every intended chapter is present and sequential;
- the final chapter/title endpoint is correct;
- target chapter lengths meet the current writing target unless intentionally changed;
- NO EM DASHES appear in newly drafted manuscript prose;
- numerical/canon continuity reflects what actually happened;
- state/index/open-thread changes do not contradict the prose;
- no stale source overwrote newer GitHub authority.

## Reader synchronization

The reader is downstream from manuscript authority.

Reader updates do not need to interrupt every chapter. Prefer syncing the reader at batch checkpoints or when a reader-specific fix is already being shipped.

Do not let reader lag become manuscript loss: exact prose must be durable even when illustrated/static pages have not caught up.

## Re-prompt / trailhead behavior

Within a multi-chapter batch, use compact working trailheads rather than a large formal handoff after every chapter.

After the BATCH is shipped, provide:

1. compact production note;
2. chapters completed;
3. verified endpoint;
4. important durable residue;
5. one full copyable next-edge re-prompt.

GitHub provides durable continuity. The re-prompt gives the next writing session an explicit trailhead.

## Current edge

Chapter 235 — **THE TAGALONG**.

See `state/MANUSCRIPT_STATE.md` for current canon and the Chapter 236 edge.
