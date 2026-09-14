# R2 Temporal Run Template

Status: **TEMPLATE / COPY INTO AN EXPERIMENT AS `TEMPORAL_RUN.md`**

This file is the compact durable contract for one temporal experiment.

Do not use it as story canon. Do not fill every field merely because it exists. Keep only state that materially helps the run continue.

## 1. Authority anchor

```text
ACCEPTED AUTHORITY:
SOURCE COMMIT / CHAPTER / STORY STATE:
EXPERIMENT BRANCH:
EXPERIMENT FOLDER:
```

The run begins from accepted R2 authority. If `main` advances materially while the experiment continues, reconcile before treating older speculative assumptions as current.

## 2. Experiment question

One sentence.

```text
Can R2 ... ?
```

The question should explain why this run exists. Passing time by itself is not enough.

## 3. Clock

```text
CLOCK SOURCE: explicit_user | active_run | inferred_high_confidence | clarified
CLOCK CONFIDENCE: high | resolved
START:
HORIZON / END:
CHECKPOINT STRATEGY:
CURRENT CLOCK POSITION:
STOP CONDITION:
```

Examples:

```text
HORIZON / END: one elapsed year
```

```text
HORIZON / END: through the winter expedition departure
```

```text
HORIZON / END: 30 elapsed days
```

Do not invent a full calendar when relative time is enough.

## 4. Run constraints

Every run needs at least one meaningful item here besides the clock.

### Hard constraints

Pass/fail only.

```text
- 
```

Examples:

```text
- A meaningful Gold-caliber party appears during the run.
- Greg does not become Gold during this run.
- No chosen-one resolution.
```

### Soft nudges

Selection pressure, not quotas.

```text
- 
```

Examples:

```text
- More action.
- A little more recognizable fantasy/isekai trope pleasure.
- More ordinary-life interruption between progression beats.
```

### Explicit non-goals

Protect against accidental scope expansion.

```text
- 
```

## 5. Optional output / fidelity target

Only include what helps this experiment.

```text
CONFIDENCE ZONES:
TARGET CHAPTER / SCENE SHAPE:
WORD-COUNT TARGET:
WORD COUNT HARD?: no
OTHER:
```

Word count is a fidelity target unless the user explicitly makes it hard.

## 6. Current compact state

Track only domains relevant to this run.

```text
GREG:
PEOPLE / RELATIONSHIPS:
BODY:
MONEY / MATERIAL:
WORK / OBLIGATIONS:
GEAR / OBJECTS:
GEOGRAPHY / ROUTES:
MAGIC / CAPABILITY:
RANK / REPUTATION:
WORLD / WEATHER / ECOLOGY:
OPEN PRESSURES:
```

Delete unused categories rather than maintaining empty simulation state.

People who are not relevant to the run do not need clocks.

## 7. Nudge update log

Record only user direction that changes future selection.

Newest explicit user direction outranks older soft nudges.

```text
- [run position] NUDGE: ... -> CONTRACT CHANGE: ...
```

Do not preserve ordinary chat as a transcript.

Examples:

```text
- D001 NUDGE: "Gold party" -> HARD: meaningful Gold-caliber party must appear.
- D001 NUDGE: "more action" -> SOFT: raise embodied hazard/action selection pressure.
- D001 NUDGE: "a little more tropes" -> SOFT: permit more recognizable fantasy progression pleasure.
```

## 8. Temporal residue checkpoint

For each meaningful time jump, keep this compact.

```text
FROM:
TO:
ELAPSED:
OFF-PAGE CHANGES THAT MATTER:
- 
- 
CURRENT CONSEQUENCE:
```

Two concrete consequences are a useful default for meaningful gaps greater than roughly two days, not a prose quota.

Vary which domains carry elapsed time. Do not make every chapter open with the same checklist grammar.

## 9. Planner-only run edge

This is the current next experimental edge, not prose.

```text
CURRENT PRESSURE:
WHAT CHANGED LAST:
WHAT REMAINS UNCERTAIN:
NEXT USEFUL QUESTION:
NEXT CLOCK MOVE:
RELEVANT CONSTRAINTS:
```

Keep this short enough that another worker can reconstruct the edge quickly.

## 10. Reduced Scene Packet

Before generating reader-facing prose, derive a temporary Scene Packet from this run state.

The prose renderer should receive something shaped like:

```text
SCENE TIME:
ELAPSED SINCE LAST LIVED SCENE:
LOCATION / PHYSICAL SITUATION:
PEOPLE PRESENT + WHAT THEY WANT NOW:
CONCRETE CHANGES ALREADY TRUE:
ACTIVE TASK / DESIRE / INTERRUPTION / PRESSURE:
SCENE-RELEVANT RUN PRESSURE:
FACTS THAT MAY NOT BE CONTRADICTED:
CONSEQUENCES THAT SHOULD SURVIVE THIS SCENE:
```

Only include one or two run pressures materially relevant to this scene.

Do **not** copy the full engine, audits, survivor labels, experiment history, alternate versions, or planning vocabulary into the Scene Packet.

### Renderer firewall

The Scene Packet should normally exclude author-side terms such as:

```text
horizon
rehearsal
quarry
canon
story authority
constraint
survivor label
audit verdict
generator/model instruction
```

If a word independently belongs in the fictional scene, that is fine. The rule is against meta leakage.

## 11. Post-render scrub

After prose generation, the scrubber may again read the full engine and run contract.

Check:

- time residue is felt rather than merely announced;
- no planning/audit machinery leaked into prose;
- repeated evaluator fragments are not substituting for cognition;
- the scene does not explain the rule it just successfully demonstrated;
- people act from their own current wants and schedules;
- the relevant constraint affected selection without becoming visible scaffolding;
- word count was not padded with repeated thought;
- action, ordinary life, relationships, work, fantasy pleasure, and messiness appear according to the current run rather than by global quota.

## 12. Resume contract

When a fresh worker receives `continue`:

1. read newest accepted R2 authority;
2. read `TEMPORAL_ENGINE.md`;
3. read this experiment's `TEMPORAL_RUN.md`;
4. read the current experimental edge/prose needed for the next move;
5. reconcile only if newer authority materially conflicts;
6. preserve the existing clock, hard constraints, soft nudges, and stop condition;
7. continue from the current clock position;
8. do not ask the user to repeat durable inputs already stored here.

If no active `TEMPORAL_RUN.md` exists, resolve a new clock and at least one constraint using the engine's inference order.

## 13. Closeout

At the end of the run, record:

```text
FINAL CLOCK POSITION:
STOP CONDITION MET?:
HARD CONSTRAINT RESULTS:
USEFUL SURVIVORS:
FAILED / DEAD MATERIAL:
DISCOVERIES WORTH CARRYING FORWARD:
AUTHORITY STATUS: speculative / zero authority unless separately promoted
```

Then hand useful discoveries to `r2/FUTURE_SURVIVOR_PROTOCOL.md`.

Completion does not equal canon.