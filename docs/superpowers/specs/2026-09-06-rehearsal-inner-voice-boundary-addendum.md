# REHEARSAL Private Inner Performance Boundary Addendum

Status: approved design clarification

Applies to: `docs/superpowers/specs/2026-09-06-rehearsal-modes-memory-inner-voice-design.md`

This addendum sharpens the actor inner-performance contract. Where wording in the parent spec is ambiguous, this addendum controls.

## Character versus actor authority

PRIVATE INNER VOICE is actor-generated performance state, not literal character truth.

Conceptually:

- **CHARACTER** = durable story identity, canon history, knowledge boundaries, relationships, constraints, and supported tendencies
- **ACTOR** = active inference and performance process for the current scene
- **PRIVATE INNER VOICE** = the actor's current interpretation of what the character may be thinking, wanting, misreading, suppressing, deciding, fearing, hoping, resenting, or strategically withholding
- **CANON INNER STATE** = only established when independently supported by canon, explicitly user-authored, accepted through a prose return, or promoted through existing supported-memory authority rules

Do not model rehearsal output as `character.thinks = X`.

Model it as the actor performing a private interpretation of the character under the current dramatic lock.

Two independent takes may therefore assign different private motives to the same character while still producing the same character-specific observable behavior. Convergence on observable behavior is stronger rehearsal evidence than convergence on a private motive. Private motive convergence remains hypothesis-level unless independently supported.

Greg/Nico follows the same actor-versus-character distinction. Nico's `INNER VOICE` becomes Greg's actual first-person thought only if the resulting prose return survives editorial acceptance.

## Performance channels

Meaningful actors may perform through three channels.

Greg/Nico:

- `BODY`
- `VOICE`
- `INNER VOICE`

Other meaningful actors:

- `BODY`
- `VOICE`
- `PRIVATE INNER VOICE`

The hidden channel exists to improve visible character performance and subtext. It does not grant reader access to non-Greg interiority.

## Hard information boundary

Every actor's private inner performance is private to that actor.

Actor execution may receive only:

- durable character information that actor is entitled to know
- scene-local role packet state
- observable BODY and VOICE outputs from other actors
- other canon-visible facts available to that character

One actor may not receive, inspect, infer from privileged rehearsal metadata, or respond directly to another actor's private inner performance.

A private interpretation may affect another actor only after its owner externalizes something observable through:

- speech
- action
- hesitation
- expression
- posture
- timing
- silence
- interruption
- object handling
- strategic omission
- another physically or socially legible behavior

This is a hard information boundary, not a style preference.

No rehearsal take may accidentally grant telepathic access or unsupported knowledge simply because the engine can see the complete rehearsal state.

## Novelization visibility

Only Greg/Nico's `INNER VOICE` is directly eligible for first-person novelization.

Non-Greg `PRIVATE INNER VOICE` is hidden performance state. It may influence only that actor's outward performance and may not be exposed directly to Greg, another actor, or the reader.

Novelizer and approved critics may inspect Greg's `INNER VOICE`.

For non-Greg actors, critics may inspect `PRIVATE INNER VOICE` only for rehearsal-quality checks such as knowledge leakage, motive over-explanation, duplication of spoken dialogue, ambiguity destruction, or synthetic self-confirmation. The novelizer may consume only the resulting observable BODY/VOICE/subtext consequences, not the hidden thought text itself.

## Inner performance is not sentence-bound

The parent spec describes Greg's `INNER VOICE` as dialogue because it is live, responsive, timed, actor-owned performance.

That does **not** require cognition to arrive as grammatical internal monologue.

> “Dialogue” describes the live, responsive nature of INNER VOICE, not its grammatical form. Nico may perform nonverbal or pre-verbal cognition where appropriate.

Greg's cognition may be performed as:

- image
- memory fragment
- association
- half-word
- impulse
- calculation
- wrong inference
- sensory hook
- unfinished thought
- bodily anticipation
- emotional recoil before naming the emotion
- recognition without immediate verbal explanation
- suppressed joke
- self-correction
- abrupt strategic branching

Non-Greg `PRIVATE INNER VOICE` may use the same broad cognition forms when useful to performance.

A performed thought may contain no complete sentence at all.

The novelizer should preserve the **shape and timing of Greg's cognition** when useful, not automatically convert every internal event into polished internal monologue.

## Relationship-memory authority

Private interpretations discovered in rehearsal may enter relationship-local `HYPOTHESIS` memory.

They remain visibly synthetic unless independently supported.

A synthetic private motive cannot become increasingly true merely because later takes received it in their actor packets. Repeated rehearsal use does not count as independent support.

Only existing independent support classes may move a private interpretation toward supported authority:

- current canon evidence
- accepted prose returns
- explicit user-authored truth
- existing supported-memory promotion rules

## Take variance

Sibling takes share the same frozen memory snapshot and cannot see one another before comparison.

Sibling takes may choose different private interpretations.

Example:

- Hessa FREE A performs responsibility for Greg's safety as the dominant private interpretation
- Hessa FREE B performs suspicion that Greg is hiding something as the dominant private interpretation

If both independently produce similar observable behavior, such as controlling the lesson, refusing deflection, checking Greg's wrist, or waiting him out, the observable convergence is stronger rehearsal evidence.

Do not promote the private motive merely because multiple synthetic takes converge on it.

## Critics

Inner-performance checks must reject or downgrade hidden thoughts that:

- become overly neat explanations of behavior
- duplicate exactly what the actor then says aloud
- invent unsupported knowledge
- solve intentional ambiguity
- become canonical merely through repetition
- leak into another actor's response
- turn a character into a fixed hidden motive rather than an active scene interpretation

## Acceptance additions

The parent spec's implementation acceptance criteria gain these requirements:

1. meaningful non-Greg actors may emit `PRIVATE INNER VOICE`
2. only Greg/Nico's `INNER VOICE` is directly eligible for novelization
3. actor-facing ensemble views never expose another actor's private inner performance
4. private inner performance cannot grant unsupported knowledge
5. private rehearsal interpretations enter hypothesis rather than supported truth by default
6. repeated synthetic use cannot self-promote
7. sibling variance takes preserve frozen-memory independence while allowing different private interpretations
8. convergent observable behavior may become stronger rehearsal evidence without promoting the underlying private motive
9. Greg's `INNER VOICE` and non-Greg private cognition support sentence and non-sentence forms
10. existing BODY/VOICE behavior remains backward-compatible
11. no new unrestricted write path to `main` is introduced
12. the first 001-020 rerun uses high-authority FREE rehearsal for both Greg's live cognition and other actors' hidden subtext
