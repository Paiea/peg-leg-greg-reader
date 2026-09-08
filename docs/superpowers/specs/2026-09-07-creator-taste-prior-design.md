# Creator Taste Prior Design

**Status:** approved architectural direction

**Branch:** `architecture/long-form-story-compiler`

**Purpose:** add a small, evidence-backed creator-taste prior to the generic long-form story compiler so the system can spend search and REHEARSAL budget more intelligently without turning creator preference into story authority or making every project converge on the same narrative shape.

## 1. Core rule

Creator taste is a **search prior**, not canon, not character truth, not audience truth, and not a deterministic branch selector.

The system should use creator taste to answer:

> Which plausible possibilities deserve more exploration?

It must not answer:

> What would Keoni write, therefore write that.

The creator prior is gravitational, not a railroad track.

## 2. Authority order

Creator taste must never override:

1. accepted canon prose / established story truth
2. character truth
3. causal continuity
4. strong repeated REHEARSAL evidence
5. explicit project constraints and audience promise

Creator taste acts only as a search/scheduling signal among still-viable possibilities.

A less creator-likely branch may win when rehearsal, character truth, audience promise, novelty, or downstream consequences are stronger.

## 3. Storage model

Use Git-tracked durable state with three layers:

```text
state/
  long-form/
    creator-taste/
      CONTRACT.md
      CURRENT.json
      evidence.jsonl
      projects/
        <project-slug>.json
```

### 3.1 `evidence.jsonl`

Append-only creator decision evidence.

Each meaningful decision record should preserve enough context to understand what was chosen and why without storing entire conversations.

Suggested fields:

- stable decision id
- timestamp or authority commit when available
- project
- context / decision surface
- candidate options considered when known
- creator choice
- concise creator reason, preferably using explicit language from the decision rather than inferred personality
- signals supported
- signals challenged
- source type, such as human editorial decision, accepted revision, visibility choice, branch selection, or explicit preference
- optional provenance pointer to commit / PR / artifact

Do not log every comment. Preserve consequential decisions and repeated signals.

The ledger is evidence, not a prompt surface for routine generation.

### 3.2 `CURRENT.json`

Small compiled cross-project creator prior.

This is the normal runtime input consumed by the long-form compiler.

It should contain a bounded set of active signals, normally no more than 10–25.

Each signal should include:

- stable signal id
- scope = `cross_project`
- direction, such as prefer / avoid / explore
- confidence
- evidence count
- counterexample count
- concise narrative summary
- optional conditions where the signal applies
- last evidence reference

Example:

```json
{
  "id": "consequence_over_explanation",
  "scope": "cross_project",
  "direction": "prefer",
  "confidence": 0.78,
  "evidence_count": 14,
  "counterexample_count": 3,
  "summary": "Prefer story developments whose mechanics create visible human or social consequences rather than remaining explanatory system detail."
}
```

`CURRENT.json` is derived from evidence and may be rebuilt. It is not durable story authority.

### 3.3 `projects/<project-slug>.json`

Small project-local taste overlay.

This captures demonstrated preferences that are unusually strong or specific within one project without incorrectly promoting them into global creator taste.

Project overlays should normally contain only deviations, stronger local signals, or project-specific creative preferences.

Example:

```json
{
  "project": "dragon-spotter",
  "signals": [
    {
      "id": "competence_as_romantic_pressure",
      "confidence": 0.81,
      "summary": "In this project, competence and professional conflict are especially valuable sources of attraction."
    }
  ]
}
```

## 4. Keep creator taste separate from audience promise

Creator taste and audience promise are different inputs and must remain separately inspectable.

Examples:

- `Creator taste`: repeated demonstrated preference for systems that create human consequences.
- `Audience promise`: Gravity's Embrace is intended to deliver romantasy / progression-fantasy rewards for its target reader.

Do not infer that a project-specific market or genre choice is a permanent creator preference.

The runtime compile packet may therefore receive:

```text
PROJECT SEED
+ AUDIENCE PROMISE
+ CROSS-PROJECT CREATOR PRIOR
+ PROJECT TASTE OVERLAY
+ CURRENT STORY STATE
```

These inputs remain semantically distinct.

## 5. Creator surprise

Every meaningful branch-selection surface should preserve explicit counter-pressure against self-copying.

Add a `creator_surprise` signal alongside `creator_prior_match`.

`creator_surprise` identifies a viable branch that is less obvious from creator history but may produce unusually strong dramatic, emotional, structural, or audience value.

The system should preserve at least one creator-surprise branch during meaningful early/mid exploration when such a branch exists.

Creator surprise must still respect canon, character truth, causal continuity, and project constraints.

The purpose is not random novelty. It is productive deviation from the creator prior.

## 6. Branch evaluation

Where the existing compiler compares viable branches, allow lightweight evaluation signals such as:

- continuity / causal strength
- character truth
- repeated REHEARSAL support
- audience promise
- creator prior match
- creator surprise
- novelty
- downstream consequences

Do not require a rigid universal numeric formula if qualitative levels fit the current implementation better.

Creator-prior match is a scheduling/search signal, not an authority score.

## 7. Learning from disagreement

When the creator chooses a branch that contradicts the current prior, preserve that as evidence rather than silently replacing an old preference.

Record the conditions that made the unexpected branch win.

Example:

> Creator usually prefers immediate exploitation of a discovered mechanic, but selected delayed disclosure because secrecy produced a stronger relationship arc.

This becomes a contextual refinement and counterexample, not a new absolute rule.

## 8. Runtime behavior

Creator taste should primarily influence **what gets generated / compared / rehearsed**, not dictate REHEARSAL outcomes.

Preferred flow:

```text
POSSIBILITIES
-> creator prior nudges exploration
-> creator surprise preserves non-obvious alternatives
-> REHEARSAL tests behavior
-> story / character / audience evidence competes
-> STORY SYNC promotes earned discoveries
-> prose renders the resulting story
```

### Early exploration

- use creator taste lightly
- preserve multiple viable possibilities
- intentionally keep creator-surprise branches alive

### Middle comparison

- creator prior may help allocate rehearsal/search budget
- repeated rehearsal evidence should increasingly dominate
- preserve counterexamples and branch disagreement

### Late convergence

- do not increase creator-taste authority merely because the run is converging
- established truth, causal closure, character truth, audience promise, and repeated rehearsal evidence dominate
- creator taste acts only as a tie-breaker / search heuristic

## 9. Evidence capture policy

Do not build a giant personality profile.

Capture only narrative/editorial decisions with reusable search value.

Good evidence examples:

- repeated approval or rejection of a dramatic solution
- creator choosing consequence over exposition
- preserving/hiding/compressing a chapter for a clear narrative reason
- choosing one relationship trajectory over another
- rejecting generic or mechanically repetitive fantasy material
- choosing a surprising branch over a creator-likely branch and explaining why

Bad evidence examples:

- temporary mood
- unrelated personal facts
- isolated wording preferences unless they materially affect story architecture
- arbitrary inferred personality traits
- every conversational reaction

## 10. Boundedness and maintenance

Keep the active cross-project prior small.

Target: 10–25 active signals maximum.

When several signals overlap, merge or simplify them. Preserve historical evidence in `evidence.jsonl` rather than keeping every micro-preference active.

Weak or stale signals may decay in confidence while remaining auditable in the evidence ledger.

Project-local signals should not automatically graduate into cross-project taste. Graduation should require repeated evidence across multiple projects or explicit creator approval.

## 11. Rebuildability

`CURRENT.json` and project overlays are derived editorial state.

If inference quality becomes bad, they must be rebuildable from the evidence ledger and explicit project decisions.

The evidence ledger itself remains non-canon editorial provenance.

No creator-taste artifact may modify canon prose directly.

## 12. Minimal first implementation

The first implementation should add only:

1. storage contract and schema validation
2. empty / seeded `CURRENT.json`
3. append-only evidence record support
4. one Dragon Spotter project overlay
5. compile-packet support for creator prior + project overlay
6. branch metadata for `creator_prior_match` and `creator_surprise`
7. tests proving creator taste cannot override canon / character truth / strong rehearsal evidence
8. tests proving a creator-surprise branch remains eligible for rehearsal
9. lightweight prior rebuild/update function from explicit evidence

Do not build embeddings, a learned ML taste model, vector storage, or a generalized personality engine in the first slice.

## 13. Success criteria

The feature is successful when:

- the compiler can load a small cross-project creator prior and project overlay
- those inputs change exploration priority without becoming story authority
- a non-obvious but strong creator-surprise branch can survive and win
- creator disagreement becomes contextual evidence rather than rule replacement
- project-specific preferences do not silently become global preferences
- normal generation does not need to load the full historical evidence ledger
- the feature remains inspectable, reversible, and cheap enough to use continuously during overnight long-form runs

## Core principle

**Use the creator's demonstrated taste to search more intelligently while retaining enough independence for the story to surprise him.**
