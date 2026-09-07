# REHEARSAL Greg Inner Voice Boundary Addendum

Status: approved design clarification

Applies to: `docs/superpowers/specs/2026-09-06-rehearsal-modes-memory-inner-voice-design.md`

This addendum sharpens the Greg `INNER VOICE` contract. Where wording in the parent spec is ambiguous, this addendum controls.

## Private performance state

Greg's `INNER VOICE` is private performance state owned by Nico.

Other actors may observe only Greg's externally available performance:

- `BODY`
- `VOICE`

Other actors may not receive, inspect, infer from privileged metadata, or respond directly to Greg's `INNER VOICE` output.

`INNER VOICE` is available to:

- Nico while playing Greg
- the novelizer
- critics that explicitly evaluate Greg's internal performance or the resulting prose

A thought may influence another actor only after Greg externalizes something observable through:

- speech
- action
- hesitation
- expression
- posture
- object handling
- another physically or socially legible behavior

This is a hard information boundary, not a style preference.

The ensemble simulation must therefore distinguish:

- **private actor state**: Greg's `INNER VOICE`
- **observable actor output**: Greg's `BODY` and `VOICE`

No rehearsal take may accidentally grant another actor telepathic access to Greg's internal performance.

## Inner voice is not sentence-bound

The parent spec describes `INNER VOICE` as dialogue because it is live, responsive, timed, character-owned performance.

That does **not** require thought to arrive as grammatical internal monologue.

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

A performed thought may contain no complete sentence at all.

The novelizer should preserve the **shape and timing of cognition** when useful, not automatically convert every internal event into polished internal monologue.

The critic should penalize prose that makes Greg's mind implausibly articulate merely because the rehearsal representation was explicit.

## Novelization consequence

The novelizer may use private `INNER VOICE` to shape:

- paragraph rhythm
- attention order
- sentence length
- omission
- interruption
- associative transitions
- memory intrusion
- sensory emphasis
- spoken dialogue timing
- whether a thought appears explicitly on the page at all

Not every rehearsed thought should survive as text.

The goal is not more thought. The goal is more accurately performed cognition.

## Acceptance additions

The parent spec's implementation acceptance criteria gain these requirements:

1. actor-facing ensemble views never expose Greg's `INNER VOICE` to non-Greg actors
2. novelizer and approved critics can access Greg's `INNER VOICE`
3. Greg's `INNER VOICE` representation supports sentence and non-sentence cognition forms
4. no schema requires every internal event to contain grammatical prose
5. tests prove that another actor cannot respond to private thought unless an observable BODY or VOICE output externalizes it
6. the first Nico campaign samples nonverbal and pre-verbal cognition instead of generating only internal monologue
