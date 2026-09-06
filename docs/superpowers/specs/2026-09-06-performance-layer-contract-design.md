# PERFORMANCE Layer Contract

Status: DESIGN
Date: 2026-09-06
Scope: Smallest implementable PERFORMANCE boundary for Peg-Leg Greg's proposed `BLUEPRINT -> DRAMATIC SCRIPT / IR -> PERFORMANCE -> NOVEL PROSE` architecture

## 1. Architectural position

Lock the pipeline as:

**BLUEPRINT -> DRAMATIC SCRIPT / IR -> PERFORMANCE -> NOVEL PROSE**

The boundaries are:

- **BLUEPRINT:** what must happen and why.
- **DRAMATIC SCRIPT / IR:** what dramatic truth is locked, including required outcomes, required information, required actions/results, state changes, canon constraints, and ownership only where ownership itself matters.
- **PERFORMANCE:** how these specific people actually manage to get through those beats today.
- **NOVEL PROSE:** how Greg experiences, interprets, and narrates the performed scene.

The central rule is:

> **Dramatic Script locks what the scene must accomplish. PERFORMANCE owns how difficult, awkward, efficient, funny, mistimed, evasive, or human the route becomes. Novel Prose owns Greg's narrative expression of that performed scene.**

PERFORMANCE is transformative, not decorative metadata.

## 2. Purpose

The existing dialogue machinery already solves important parts of this problem:

- `state/DIALOGUE_VARIANCE_ENGINE.md` defines `BASE VOICE + RELATIONSHIP + CURRENT STATE + SCENE PRESSURE + SMALL HUMAN VARIANCE`.
- `state/DIALOGUE_VARIANCE_PERFORMANCE_LAYER.md` on `editor/voice-compression-pass` defines comparative performance fingerprints and exchange-level asymmetry.
- `state/voices/EARLY_BOOK_I_PERFORMANCE_MATRIX.md` on `editor/voice-compression-pass` describes Greg, Antonius, Arlo, Hessa, Jorren, and Alden by exchange behavior rather than catchphrases.
- `state/editorial/dialogue-variance-pass/EXCHANGE_RHYTHM_GATE.md` provides exchange-level convergence checks.
- `state/editorial/dialogue-variance-pass/READER_EAR_AUDIT_TEMPLATE.md` provides periodic continuous-read diagnostics.
- `state/editorial/dialogue-variance-pass/PERFORMANCE_CALIBRATION_VISIBLE_001_020.md` establishes Chapters 1-20 as the current calibration set and finds mild remaining cadence convergence rather than a broad attribution failure.

This design does not replace those systems. It promotes their core logic into an explicit generation/editing boundary between Dramatic Script and prose.

The goal is to prevent two common failures:

1. Characters become optimized expressions of their voice fingerprints.
2. Conversations take the cleanest possible route even when the people, state, relationship, and environment would plausibly produce a different route.

## 3. Design principles

The implementation must preserve these principles:

1. **Performance is transformative.** It may reshape local exchange topology rather than merely annotate a finished exchange with mood.
2. **Character fingerprints are tendencies.** Greg does not always extend. Antonius does not always reduce. Hessa does not always impose procedure. Arlo does not always return to the object.
3. **Strengths can fail.** A normal strength may overfire, underfire, arrive too early, or get aimed at the wrong problem.
4. **Variance is causal before random.** Randomness must never be the source of plausibility.
5. **State affects behavior before diction.** Bandwidth, attention, timing, self-presentation, patience, silence, interruption, explanation depth, and conversational control should bend before a character's basic voice identity does.
6. **Internal state and performed stance are distinct.** PERFORMANCE may know a character is worried while the character performs annoyance, neutrality, formality, competence, or silence.
7. **Conversational attempts may fail.** A scene may eventually accomplish a required dramatic job without every individual turn accomplishing it immediately.
8. **Imperfection is available, not mandatory.** Clean efficient exchanges are valid when these people under these conditions would genuinely understand each other.
9. **Operate at exchange/scene level by default.** Do not attach large metadata objects to every line.
10. **Performance state is ephemeral.** Stable character authority and persistent consequences may survive. The temporary performance frame normally does not.

## 4. PERFORMANCE input contract

PERFORMANCE receives four inputs by default.

### 4.1 Dramatic Script / IR

The Dramatic Script supplies the locked dramatic truth for the current scene or exchange.

It may contain:

- required information transfers;
- required actions or physical results;
- required state changes;
- scene entry state;
- scene exit state;
- canon constraints;
- locked ownership where ownership itself is important;
- explicit `MUST NOT DRIFT` constraints.

### 4.2 Ownership locking rule

Do not over-lock ownership.

Lock ownership only when the identity of the owner is itself canonically or dramatically meaningful.

Examples:

```text
LOCKED:
Hessa performs the procedure.
Arlo owns the technical knowledge.
Greg has this realization.
Antonius makes the final decision.
```

For information where only the result matters, prefer result-oriented requirements:

```text
REQUIRED:
Greg understands the room is unsafe before proceeding.
```

Do not automatically convert that into:

```text
Hessa tells Greg the room is unsafe.
```

PERFORMANCE may satisfy the required result through a valid route: speech, action, refusal, demonstration, inference, another authorized speaker, delayed realization, or another route consistent with canon and knowledge ceilings.

### 4.3 Stable character authority

Load only the authority required for materially active recurring characters.

This includes, when relevant:

- stable cognitive lens;
- domain/responsibility;
- established vocabulary/register;
- conversational gravity;
- humor source;
- information habits;
- uncertainty tolerance;
- normal social energy;
- durable relationship history;
- established failure/overapplication tendencies.

For the first lab, reuse the existing voice pages and performance matrix rather than building a new character schema.

### 4.4 Current materially relevant scene state

Supply only state that can plausibly matter to behavior in this scene.

Examples:

- fatigue;
- pain;
- embarrassment;
- concern;
- excitement;
- anger;
- fear;
- distraction;
- money pressure;
- unresolved argument;
- attraction;
- recent success or failure;
- preoccupation with another task or person.

Do not require every known state to appear in the performance.

### 4.5 Scene environment

Supply physical and social conditions that constrain performance, such as:

- current task;
- objects being handled;
- location;
- who is present;
- who can overhear;
- time pressure;
- physical exertion;
- public versus private setting;
- relevant authority/status context.

The environment is behaviorally important. A person carrying a crate, sparring, treating an injury, counting money, or working at a bench does not have the same conversational bandwidth as the same person sitting idle.

## 5. Temporary performance frame

For each materially active character, PERFORMANCE may synthesize one compact temporary frame for the exchange.

Minimum fields:

```text
CHARACTER PERFORMANCE

STATE:
Current materially relevant internal/physical condition.

PERFORMED STANCE:
What the character is presenting socially, which may differ from internal state.

ATTENTION:
What currently has the character's active focus.

BASELINE BEND:
How this moment plausibly bends the stable character baseline.

SHIFT TRIGGER: [optional]
A material condition that would change the performance envelope during the scene.
```

Example:

```text
ANTONIUS PERFORMANCE

STATE:
Preoccupied. Mildly worried about Greg.

PERFORMED STANCE:
Annoyed practicality. Concern is not being offered directly.

ATTENTION:
Immediate risk and finishing the current task.

BASELINE BEND:
Lower patience than usual. More controlling. More likely to interrupt abstraction early.

SHIFT TRIGGER:
If Greg names the concern directly, Antonius may go quiet rather than reduce it.
```

This frame is descriptive, not deterministic.

It must not contain numeric personality scores, per-line tactic assignments, joke probabilities, or mandatory move lists.

## 6. PERFORMANCE freedoms

PERFORMANCE may change local exchange topology while preserving locked dramatic truth.

Allowed freedoms include:

- dialogue wording;
- dialogue length;
- timing;
- silence;
- delayed response;
- partial answers;
- misunderstanding and repair;
- interruption;
- failed interruption;
- hesitation;
- physical response instead of verbal response;
- verbal response instead of physical response when ownership is not locked;
- whether a joke is engaged, ignored, missed, misunderstood, or fails;
- explanation depth;
- whether someone answers the literal or emotional layer first;
- whether someone refuses to engage;
- local ordering of unlocked beats;
- whether one required beat takes one conversational attempt or several;
- whether Greg gets the last word;
- whether a character's normal strength overfires, underfires, arrives late, or targets the wrong issue;
- whether a character temporarily loses conversational control;
- whether a character performs competence while internally uncertain or panicked.

PERFORMANCE is not required to use any specific imperfection.

The required question is:

> **Did this exchange take a route these characters, relationship, state, pressure, and environment would plausibly produce, or did the system merely choose the default optimized conversational path?**

## 7. Forbidden freedoms

PERFORMANCE may not mutate dramatic truth or canon.

It may not:

- change a required scene outcome;
- remove required information;
- alter a locked action/result;
- mutate explicitly locked ownership;
- give a character knowledge they do not yet have;
- move specialist knowledge to a different character merely because the exchange reads better;
- invent persistent consequences outside the Dramatic Script's permission;
- change money facts;
- change magic facts/results;
- change body continuity;
- change object continuity;
- change chronology;
- change relationship status;
- resolve intentionally unresolved questions;
- turn Greg's interpretation into objective truth;
- make another character infer hidden internal state without earned evidence;
- emit non-POV interiority as an observable thought/narration beat without explicit Dramatic Script authorization;
- force internal state to become visible simply because PERFORMANCE has access to it.

PERFORMANCE knows more about internal state than the other characters are automatically allowed to know.

## 8. Performed output contract

PERFORMANCE outputs an explicit **performed script**. It is still not novel prose.

The output should remain script-shaped and ownership-clear.

Minimum beat forms:

```text
CHARACTER [ACTION]
Content.

CHARACTER -> ADDRESSEE [DIALOGUE]
"Content."

POV CHARACTER [THOUGHT]
Content.
```

Use named owners. Avoid ambiguous pronouns when ownership could be unclear.

`[THOUGHT]` is POV-authorized interiority, normally Greg in PLG. A non-POV character's private state may exist in the temporary performance frame and may causally shape visible behavior, but it must not become a thought beat unless the Dramatic Script explicitly authorizes that interior access.

Optional exchange-level markers may be used only when materially useful:

```text
PERFORMANCE SHIFT:
Reason the temporary performance envelope changed.
```

Example:

```text
SCENE: Antonius's storeroom

ANTONIUS [ACTION]
Keeps sweeping.

GREG -> ANTONIUS [DIALOGUE]
"Why are you cleaning?"

ANTONIUS -> GREG [DIALOGUE]
"Because the room needs cleaning."

GREG [THOUGHT]
That cannot be the whole reason.

GREG -> ANTONIUS [DIALOGUE]
"No."

ANTONIUS [ACTION]
Stops with the broom halfway through a stroke.

ANTONIUS -> GREG [DIALOGUE]
"No?"

...

PERFORMANCE SHIFT:
Greg identifies the gauge as potentially extremely valuable. Antonius's attention moves from cleanup and Greg-management to valuation.

ANTONIUS [ACTION]
Sets the broom aside.
```

Novelization must treat the performed script as the behavioral authority for the rendered scene.

If PERFORMANCE decides Antonius keeps sweeping through Greg's question, the prose renderer may choose the wording and cadence of Greg's narration around that action, but it may not silently replace that behavior with Antonius immediately stopping and giving an optimized explanation.

## 9. Behavioral Realization Gate

The PERFORMANCE validator must not require every temporary state to become reader-visible.

Instead:

> **If PERFORMANCE claims that a state materially affected this exchange, the claimed effect must appear in observable performance rather than being explained afterward.**

Observable realization may include:

- timing;
- interruption;
- silence;
- physical action;
- practical redirection;
- missed question;
- partial answer;
- explanation length;
- altered patience;
- control attempt;
- failed joke;
- delayed reaction;
- avoidance;
- retreat into a safer domain;
- unusual willingness to let another person continue.

A frame that says `worried, therefore unusually controlling` fails if the performed script behaves exactly like baseline Antonius and merely adds an explanatory note that he is worried.

Do not require a visible effect when the frame does not claim a material behavioral bend.

Do not generate adjective-only performance.

## 10. Reuse of existing diagnostics

Do not create a parallel diagnostic system.

### 10.1 Exchange Rhythm Gate

Run the existing `EXCHANGE_RHYTHM_GATE.md` logic against the performed script before prose novelization.

Check:

- who initiates the rhythm;
- who extends it;
- who gets the cleanest final button;
- who exits through work, action, silence, uncertainty, misunderstanding, or emotion;
- whether supporting lines could be swapped without changing social texture;
- whether several participants behave like equally optimized versions of Greg.

A flag is not a quota-driven rewrite requirement.

### 10.2 Swap / confusability diagnostics

Use comparative behavior rather than requiring every isolated line to identify its speaker blindly.

High-value failure:

- several turns could be reassigned among Greg, Antonius, Arlo, Hessa, or Jorren without changing the exchange's social behavior.

Expected overlap:

- Greg and Alden may match each other more than other pairs when initiative/competitive chemistry earns it.

### 10.3 Reader-ear audit

Keep the existing 10-20 chapter continuous-read audit as the manuscript-scale check after local lab work eventually reaches prose.

This design does not replace the reader-ear audit with numeric quotas.

## 11. Five-scene Chapters 1-20 laboratory

The first implementation must stop before novelization.

Use current authoritative prose as source material and the existing performance machinery as authority.

Lab scenes:

1. **Chapter 2, Antonius loan negotiation**
   - tests curiosity, commercial evaluation, suspicion, control, and state shift.
2. **Chapter 5, Antonius storeroom**
   - tests mundane work, silence, Greg's theorizing, practical redirection, and a sudden valuation shift.
3. **Chapter 9, Arlo workshop**
   - tests whether object/work exits can replace repeated dry counterpunching without flattening Arlo.
4. **Chapter 12, Jorren + Alden + Greg**
   - tests three competent dry men, intentional Greg/Alden overlap, physical action, and Jorren's distinct exit behavior.
5. **Chapter 14, Hessa beans**
   - tests concern versus performed procedure, Greg's obsessive cognition, stopping conditions, humor restraint, and physical safety.

For each scene, run:

**CURRENT PROSE -> LOCKED DRAMATIC SCRIPT -> TEMPORARY PERFORMANCE FRAMES -> PERFORMED SCRIPT -> COMPARISON WITH SOURCE**

Do not novelize during the first lab.

Do not modify canonical prose.

## 12. Lab comparison questions

Evaluate each performed script against the current source with a small qualitative rubric.

### A. Dramatic truth preservation

- Were all locked outcomes preserved?
- Were knowledge ceilings preserved?
- Did any locked ownership drift?
- Did any persistent consequence appear without permission?

This category must pass.

### B. Character-specific handling

- Does each materially active character remain recognizably themselves?
- Did their current state/stance bend behavior plausibly when it mattered?
- Did a stable strength overfire, underfire, or fail only when causally plausible?

### C. Exchange asymmetry

- Do participants take meaningfully different routes through the exchange?
- Do specialists exit through their own domain when appropriate?
- Does Greg retain appropriate comic/interpretive gravity?
- Is intentional Greg/Alden overlap preserved rather than erased?

### D. Human route quality

- Does the route fit the people and circumstances?
- Did PERFORMANCE avoid defaulting to perfectly relevant immediate answers merely because they were efficient?
- Did PERFORMANCE also avoid inserting misunderstanding, silence, or mess merely to prove it was human?

### E. Behavioral realization

- Where a performance frame claimed a material bend, did the performed script actually realize it behaviorally?
- Did the pass avoid adjective-only performance?

### F. Value over source

Classify each scene:

- **CLEARLY STRONGER**
- **PROMISING BUT MIXED**
- **NO MATERIAL GAIN**
- **WORSE / FLATTENED**

The system earns a novelization experiment only if the five-scene set shows clear value rather than isolated novelty.

Recommended promotion threshold for the first lab:

- zero dramatic-truth failures;
- at least three scenes `CLEARLY STRONGER`;
- no more than one scene `WORSE / FLATTENED`;
- no systematic loss of Greg interiority, mundane texture, or domain-specific character behavior.

This threshold is a decision aid for the lab, not a permanent manuscript quota.

## 13. Cost discipline

The implementation should remain cheap enough to use on a large manuscript.

Rules:

- operate at exchange/scene level, not per-line metadata;
- load only relevant recurring-character authority;
- synthesize one temporary performance frame per materially active character per exchange;
- reuse the frame until a material `SHIFT TRIGGER` occurs;
- do not persist temporary frames as a manuscript database;
- run expensive continuous reader-ear review only after a useful span, not every scene;
- first lab stops before prose generation;
- no manuscript-wide migration or regeneration is authorized by this design.

## 14. Data lifecycle and authority

### Persistent

May persist:

- stable character/voice authority;
- durable relationship history;
- canonical state changes caused by the scene;
- approved improvements to existing performance guidance after evidence warrants them.

### Ephemeral

Normally discard after the performed script is evaluated:

- temporary performance frames;
- inferred current stance;
- baseline bend;
- shift triggers that did not produce lasting canon;
- temporary diagnostic labels.

### Authority sources for the first lab

- Current manuscript/source prose: current `main` authority.
- Core variance engine: current `main` `state/DIALOGUE_VARIANCE_ENGINE.md`.
- Approved newer performance guidance: `editor/voice-compression-pass` versions of `state/DIALOGUE_VARIANCE_PERFORMANCE_LAYER.md`, `state/voices/EARLY_BOOK_I_PERFORMANCE_MATRIX.md`, relevant recurring voice pages, `EXCHANGE_RHYTHM_GATE.md`, `READER_EAR_AUDIT_TEMPLATE.md`, and `PERFORMANCE_CALIBRATION_VISIBLE_001_020.md`.

Do not create a second permanent performance bible for the experiment.

The implementation plan must define one explicit way to consume the approved WIP performance files in the experiment branch without silently treating stale copies as newer manuscript authority.

## 15. Non-goals

This first implementation does not:

- build the full Blueprint layer;
- build the full Dramatic Script authoring system for new chapters;
- novelize the five lab scenes;
- rewrite Chapters 1-20;
- modify canonical prose;
- merge or reorder chapters;
- create a permanent performance database;
- create numeric personality/state models;
- require conversational imperfection;
- require every state to become visible;
- replace the dialogue-variance engine;
- replace voice pages;
- replace the existing reader-ear audit;
- automatically approve performed scripts for canon.

## 16. Minimal implementation surface

The first implementation should add only what is required to run and inspect the five-scene lab.

Expected conceptual components:

1. **Dramatic Script fixture format** for the five scenes.
2. **Performance-frame synthesis contract** using existing voice/performance authority.
3. **Performed-script format** with explicit action/dialogue/thought ownership.
4. **Behavioral Realization check** for claimed material bends.
5. **Adapter/checklist for the existing exchange-rhythm diagnostics** against performed scripts.
6. **Lab comparison report** recording source-vs-performed findings and the six rubric categories above.

Do not integrate this into forward Manuscript Engine generation or publication yet.

## 17. Acceptance criteria for the first implementation

The experiment is complete when:

1. All five selected current scenes have a compact Dramatic Script fixture.
2. Ownership is locked only where ownership itself matters.
3. Each scene receives temporary performance frames only for materially active characters.
4. Each scene produces an explicit performed script with clear dialogue/action/POV-thought ownership.
5. The performed script preserves all locked dramatic truth.
6. Claimed material state bends pass the Behavioral Realization Gate.
7. Existing exchange-rhythm/swap logic can be applied to the performed script without converting it back into prose.
8. The lab report compares each performed script to current source prose and classifies the result.
9. Canonical manuscript prose remains untouched.
10. The result supports a clear decision: proceed to five-scene novelization comparison, revise the PERFORMANCE contract, or stop the experiment.

## 18. Decision after the lab

Only if the performed scripts are clearly stronger should the project proceed to:

**PERFORMED SCRIPT -> NOVEL PROSE -> ownership/canon validation -> side-by-side prose comparison**

That is a separate implementation/design step.

The first lab exists to answer one question:

> **Does a first-class PERFORMANCE transformation produce more human, asymmetric, character-specific scene behavior than the current prose while preserving dramatic truth?**
