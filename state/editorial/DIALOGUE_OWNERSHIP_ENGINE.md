# Dialogue Ownership Engine

Status: ACTIVE EDITORIAL AUTHORITY
Scope: whole Peg-Leg Greg canon

## Purpose

Dialogue readability is governed by dramatic ownership, not merely grammatical correctness.

The core rule is simple:

> A paragraph containing spoken dialogue should have one clear dramatic owner.

A reader should not have to reassign the paragraph from one character to another in the middle of a spoken exchange.

## Governing rule

Treat spoken dialogue as the anchor. Attribution, action, reaction, interior response, and nearby connective scaffolding may move, split, or be lightly rebuilt when needed to make ownership immediately legible.

This pass is deliberately more aggressive than the earlier attribution cleanup.

### Keep together

Keep dialogue and action together when they clearly belong to the same character.

Example:

`"Fine," Antonius said. He counted the silver.`

This may remain one paragraph when `He` is unambiguously Antonius.

### Split different owners

When another character acts, reacts, thinks, or speaks, give that owner a new paragraph.

Bad:

`"You," I said. She stared. I smiled.`

Preferred:

`"You," I said.`

`She stared.`

`I smiled.`

### Split leave-and-return paragraphs

A paragraph must not leave one dramatic owner, visit another, then return to the first.

Bad:

`"How much?" Antonius asked. I named the number. Jorren laughed. Antonius looked at me. "Collateral?"`

Preferred ownership sequence:

1. Antonius
2. Greg
3. Jorren
4. Antonius

### Distinguish actual characters

The engine must not reduce ownership to `Greg` versus `everyone else`.

Named and descriptive actors are distinct when the prose identifies them:

- Greg
- Antonius
- Jorren
- Sella
- Hessa
- `the man with the scar`
- `the clerk`
- other explicit actors

If Antonius speaks and Jorren reacts, that is an ownership change even though neither is Greg.

### Greg interior narration

Greg's first-person interior narration normally receives its own paragraph when it follows another character's spoken line and functions as Greg's reaction or interpretation.

Do not attach Greg's interior response to another character's dialogue merely because the prose is first person.

### Pronouns and ambiguity

Do not invent identity.

When a pronoun is safely tied to the current explicit owner, same-owner dialogue and action may stay together. When identity is ambiguous, prefer a conservative paragraph split or flag the paragraph for review rather than assigning the action to the wrong speaker.

### Attribution fallback

Paragraph breaks are preferred over rewriting.

If paragraph breaks still leave the speaker genuinely ambiguous, a minimal attribution may be added or rebuilt. Do not add decorative tags just to satisfy a detector.

## What may change

This pass may change:

- paragraph boundaries
- placement of action and reaction beats
- dialogue tags and nearby attribution scaffolding when clarity requires it
- short connective prose immediately surrounding dialogue when needed to restore readable ownership

## What must not change

This pass must preserve:

- canon events
- causality
- scene outcomes
- world facts
- relationship progression
- character voice
- the substance and intent of spoken dialogue
- distinctive comedy and mundane texture

Spoken wording is presumptively protected. Automated whole-novel work should preserve quoted dialogue exactly unless a specific reviewed repair requires otherwise.

## Anti-patterns

Do not:

- merge separately owned beats into one dialogue paragraph
- let another character's reaction ride inside the speaker's paragraph for convenience
- treat all non-Greg characters as one owner
- add `said` everywhere when a paragraph break solves the problem
- rewrite good dialogue merely because the surrounding attribution is weak
- preserve a confusing paragraph solely because it already exists in canon

## Whole-novel execution model

1. Work from current canon authority.
2. Use identity-aware ownership detection.
3. Apply deterministic paragraph-boundary repairs first.
4. Use bounded semantic fallbacks only where deterministic ownership is insufficient.
5. Preserve quoted dialogue spans during automated passes.
6. Validate source authority as well as reader derivatives.
7. Report unresolved mixed-owner candidates instead of silently guessing.
8. Commit in bounded chapter batches so any bad region is easy to inspect or revert.

## Source authority

Permanent edits must follow the current publishing authority map:

- Chapters 1-155: published canon chapter prose is the active reader source. Chapters 1-82 must also be promoted into the canonical Book 1 DOCX after approval.
- Chapters 156-219: `state/manuscript/Peg_Leg_Greg_Recovered_Ch156-219_EXACT.md` is source authority.
- Chapters 220-current: the running manuscript and active exact chapter checkpoint Markdown files are source authority according to `scripts/generate_light.py` precedence.

Do not ship a reader-only whole-novel cleanup that can be overwritten by source regeneration.

## Success standard

The pass does not need to prove that every paragraph in a 491-chapter novel is semantically perfect.

It does need to make the common ownership failure substantially rarer, catch explicit multi-character collisions, preserve dialogue/canon, surface unresolved cases, and leave behind an engine that can be rerun safely as the manuscript grows.
