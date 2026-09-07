# REHEARSAL Scene Pressure and Behavioral Evidence Addendum

Status: approved design clarification

Applies to: `docs/superpowers/specs/2026-09-06-rehearsal-modes-memory-inner-voice-design.md`

This is a lightweight extension of the existing REHEARSAL architecture. It does not introduce an automatic routing subsystem.

## Core rule

> Do not store character traits when behavior under conditions can be stored instead.

Character packets remain durable identity and authority inputs. Rehearsal scenes act as tests that place actors under specific pressures and observe how they solve the scene in character.

The engine should prefer evidence such as:

> Under physical-safety pressure, especially with Greg, Hessa tends to reduce ambiguity by taking direct control of the task or body before explaining herself.

instead of:

> Hessa is controlling.

## Scene pressure model

Every meaningful actor in a rehearsal scene may receive a compact scene-pressure context. Keep it small, normally 3 to 6 populated fields:

- `goal`: what the character wants right now
- `concealment`: what the actor is trying not to reveal or externalize
- `belief`: what the actor currently interprets as happening
- `pressure`: the active pressure on the character
- `resources`: tools, authority, relationships, information, or practical leverage available
- `observable_access`: what the character can actually observe

These are scene-local performance inputs, not durable personality labels.

`belief` and `concealment` may include actor-generated interpretation. When synthetic, they remain `performed_interpretation`, not canon truth.

The scene-pressure model must respect existing knowledge boundaries and private-channel visibility.

## Behavioral discovery extraction

After rehearsal, accepted or useful takes may produce small behavioral-discovery records.

A behavioral discovery describes what the actor did under stated conditions, not a broad trait claim.

Minimum useful metadata:

- source scene or probe
- actor and character role
- relationship context
- pressure tags
- observed behavior
- evidence source/take
- support count
- authority status: `hypothesis` or `supported`

Private motive may be preserved as separate hypothesis provenance when useful, but the observable behavior is the primary evidence surface.

Synthetic rehearsal cannot self-promote. Existing independent-support rules continue to control promotion.

## Character probes

REHEARSAL may create optional, short, synthetic character probes whose purpose is differentiation rather than story generation.

A probe:

- is explicitly `authoritative: false`
- is not a story event
- does not update canon facts or chronology
- uses the existing actor, pressure, visibility, knowledge, variance, and critic machinery
- may generate behavioral hypotheses
- may not create supported truth without independent evidence

Example probe condition:

> Greg makes an obviously dangerous but technically clever suggestion.

Different actors may then solve the same pressure independently. The useful evidence is whether their observable solutions differentiate.

## Survival outcome logging

Every rehearsal-derived prose decision should log why it survived or did not survive.

Use a compact reason vocabulary that may include:

- `behavioral_specificity`
- `dialogue_voice`
- `subtext`
- `physical_ownership`
- `inner_voice`
- `timing`
- `no_change`
- `rejected_overperformance`

Outcome records should connect a discovery or take to the editorial result without changing story authority.

This data is evidence for a future routing layer, but no automatic router is implemented by this addendum.

## Performance freedom versus prose retention

Rehearsal freedom and prose-retention authority are separate knobs.

Actors may overperform internally and explore strong private interpretations when useful for character excavation.

Final prose retains only what survives existing editorial, dramatic-lock, reader, source-freshness, and authority checks.

The fact that rehearsal material is later discarded is not evidence that the rehearsal was wasted.

## Acceptance additions

1. actor packets can carry compact scene-pressure context without replacing existing role context
2. pressure context respects character knowledge and observable-access boundaries
3. behavioral discoveries record conditions and observed behavior rather than trait-only labels
4. synthetic behavioral discoveries enter hypothesis authority by default
5. character probes are explicitly non-authoritative and reuse existing rehearsal machinery
6. probe output cannot mutate canon truth merely because a probe was run repeatedly
7. survival outcomes log why rehearsal discoveries did or did not reach prose
8. no automatic scene router is introduced
9. existing actor, relationship-memory, variance, evidence, and write-authority behavior remains backward-compatible
10. the 001-020 campaign begins collecting pressure tags, behavioral discoveries, probe evidence where useful, and survival outcomes
