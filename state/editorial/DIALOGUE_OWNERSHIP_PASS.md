# PEG-LEG GREG — DIALOGUE OWNERSHIP PASS

Branch: `editor/dialogue-ownership-pass`

Status: **ACTIVE / HIGH-PRIORITY READABILITY REPAIR**

## Purpose

Remove a recurring dialogue-readability defect from the currently showcased Peg-Leg Greg manuscript and prevent it from returning.

The defect is not merely low tag density. It is **speaker ownership ambiguity**: a spoken line is left untagged while another character's action is attached closely enough that the action can be read as attribution for the wrong speaker, or two spoken turns are allowed to occupy one paragraph through an ownership switch.

Current known live example from Chapter 2:

`"Your age." He smiled. "How old did you expect me to be?"`

The first spoken turn and the second spoken turn belong to different people. Antonius's action is being used as the hinge between them inside one paragraph. A reader has to backtrack to recover conversational geography.

## Durable invariant

**The reader should never have to infer the speaker by discovering that an attached action actually belongs to somebody else.**

A dialogue paragraph must establish ownership cleanly.

Rules:

1. If a spoken line could be misread as belonging to the character performing the attached action, explicitly tag the actual speaker with a simple attribution such as `said` or `asked`.
2. If spoken ownership changes to another character, start that character's spoken turn in a new paragraph.
3. Another character's reaction may remain near an explicitly owned spoken line when the result is effortless to read, but the reaction must not function as false attribution.
4. In two-person exchanges, untagged alternation is allowed only while sequence is genuinely effortless.
5. After interruption, interiority, movement, subject shift, or any break in conversational rhythm, re-tag sooner.
6. In three-plus-speaker scenes, prefer explicit clarity over line-count bookkeeping.
7. Do not solve attribution by inventing decorative shrugs, looks, nods, or gestures. Prefer `said` / `asked` when a tag is what the sentence needs.
8. Do not mechanically split every dialogue line into its own paragraph. Paragraph breaks are a tool, not the default repair.
9. Do not rewrite dialogue payload, voice, canon, scene outcome, money, magic, body continuity, or relationship state merely to fix attribution.
10. Hard prose rule remains: **NO EM DASHES.**

## Scope

Current manuscript authority on branch creation: Chapter **491**.

Primary repair scope is the **currently showcased manuscript**.

Visibility authority is:

`publishing/showcase_chapters.json`

The manifest is `whole_chapter_only`, defaults to visible, and explicitly marks hidden canon. Hidden chapters remain canon but are skipped by this pass unless they later become showcased.

A chapter that changes from hidden to visible automatically becomes eligible for dialogue-ownership validation.

## Repair hierarchy

Use the smallest change that makes ownership effortless.

### A. Add the real speaker tag

Preferred when an untagged line is being visually attributed to somebody else's action.

Before:

`"Doing what?" Rusk pointed at the sack.`

Preferred shape when Greg is the speaker:

`"Doing what?" I asked. Rusk pointed at the sack.`

The exact final punctuation/paragraphing should follow local prose rhythm.

### B. Separate a true speaker change

Before:

`"Your age." He smiled. "How old did you expect me to be?"`

The Greg turn and Antonius turn should not remain one dialogue paragraph. Give Antonius's action / speech its own ownership surface.

### C. Preserve already-clear prose

Do not add tags to every alternating line. Do not create one-sentence paragraph stacks merely to satisfy a mechanical rule. A clear exchange should remain light.

### D. Escalate semantic ambiguity

If the actual speaker cannot be proven from the local context, do not guess. Record the candidate for review with neighboring paragraphs.

## Detection architecture

The automated layer is a **candidate detector, not a prose author**.

It should scan exact reader/manuscript paragraphs and surface suspicious ownership patterns with:

- canonical chapter number;
- showcase chapter number when visible;
- paragraph index;
- previous paragraph;
- candidate paragraph;
- next paragraph;
- rule/category;
- confidence / review class;
- stable fingerprint derived from exact source text.

Initial candidate classes:

- `untagged_dialogue_followed_by_action`: quoted speech is followed by a third-person/name action beat before ownership is explicitly established;
- `possible_multi_speaker_paragraph`: multiple quoted turns plus an intervening action/ownership hinge suggest more than one speaker in one paragraph;
- `multi_speaker_scene_retag`: local speaker density / interruption creates an attribution-risk candidate;
- `reader_reported`: exact reader-found defects manually promoted into the audit even if heuristics miss them.

False positives are acceptable in the candidate report. Automatic manuscript rewriting from heuristics is not.

## Cheap-review surface

The audit must consume `publishing/showcase_chapters.json` and emit compact context packets so a worker can review ownership candidates without rereading the entire manuscript.

Default review unit should remain bounded. Prefer batches of approximately 10 canonical chapters or a similarly small candidate count when chapters are dialogue-heavy.

A worker classifies each candidate:

- `FIX_TAG`
- `FIX_PARAGRAPH`
- `FIX_BOTH`
- `CLEAR_ALREADY`
- `NEEDS_CONTEXT`

Only exact reviewed replacements become manuscript patches.

## Patch application

Reuse the repository's deterministic dialogue-patch philosophy:

- exact current text must match uniquely;
- replacement must be explicit;
- no fuzzy prose rewriting;
- stale or multiply matching patches fail;
- spoken payload should remain unchanged unless a separately authorized editorial reason requires dialogue rewriting;
- surrounding markup / illustrations / navigation must remain untouched;
- no em dashes may be introduced.

Approved dialogue-ownership patches live under:

`state/editorial/dialogue-ownership-pass/`

Batch files are durable review authority. They do not outrank newer exact manuscript prose.

## Future prevention

This pass is not complete if the current manuscript is cleaned but forward production can recreate the defect.

The invariant must be represented in:

- `state/PROSE_PLAYBOOK.md`;
- `state/EDITOR_STATE.md`;
- `AGENTS.md` / worker routing where dialogue quality is defined;
- the forward/publishing validation path.

Automated validation should be conservative:

- detect suspicious ownership candidates;
- compare against reviewed current authority / baseline when needed;
- reject newly introduced high-confidence ownership regressions or require explicit review;
- never silently rewrite prose during publishing.

## Separate but related tic

Reaction shorthand such as `considered me`, `studied me`, `looked at me`, and similar face/reaction beats may be audited while reading candidates, but they are **not automatically dialogue-ownership defects**.

Treat repeated vague reaction shorthand as a separate prose-tic finding. Do not use this pass as permission to rewrite every look or reaction.

## Non-goals

This is not:

- a dialogue-variance rewrite;
- a structural compression pass;
- a chapter merge/cut/renumber pass;
- an excuse to sharpen every line;
- an excuse to make everybody sound like Greg;
- a generic body-language purge;
- a reason to edit currently hidden canon merely for completeness.

## Completion definition

The pass is complete only when:

1. durable ownership rules are in master guidance;
2. showcase-aware audit tooling exists and is tested;
3. currently visible Chapters 1-491 have been reviewed against the stronger ownership standard, not merely the older attribution standard;
4. approved exact patches have been applied to current manuscript/reader authority;
5. hidden chapters are recorded as intentionally skipped by showcase state;
6. remaining ambiguous candidates are explicitly dispositioned rather than silently ignored;
7. future publishing/manuscript validation catches new ownership regressions;
8. a final sampled read across early, middle, late, two-speaker, multi-speaker, and dialogue-heavy chapters confirms conversational geography is effortless.

## Restart prompt

`Continue PLG whole-showcase dialogue ownership pass from current GitHub authority on editor/dialogue-ownership-pass. Read state/editorial/DIALOGUE_OWNERSHIP_PASS.md first, consume publishing/showcase_chapters.json for visibility, preserve exact dialogue payload/canon, and continue from the durable candidate/patch edge.`
