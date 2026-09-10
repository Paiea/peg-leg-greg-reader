# R2 Temporal Engine Time + Constraint Contract Design

Status: **APPROVED DESIGN / IMPLEMENTATION BRANCH**

Branch: `feature/r2-temporal-engine-time-constraints`

## Problem

The temporal experiments proved that R2 can sustain useful speculative development across substantial fictional time, including a complete one-year run. The reusable engine, however, still treats time mostly as horizon architecture rather than as an explicit run input. It also lacks a compact, durable way to carry user constraints and conversational nudges into future runs.

The year experiment exposed a second failure mode: the planner, critic, and prose renderer saw too much of the same rubric. Over a long run, editorial vocabulary leaked into Greg-facing prose even when the underlying story/event continuity remained coherent.

The next engine should therefore make **time** and **constraint** first-class run inputs while making the prose renderer see less architecture, not more.

## Decision

Promote the temporal engine to active R2 speculative-development doctrine on `main` while keeping all generated future material non-canonical until it passes the normal survivor/re-performance/publication path.

Every temporal run must own a compact **Temporal Run Contract** with:

1. one clock;
2. at least one meaningful run constraint;
3. zero or more soft nudges;
4. an authority anchor;
5. a stop condition.

The contract is planning/state. It is not story prose.

## Clock contract

A clock answers **how much fictional time this run is responsible for exploring**.

Accepted clock shapes include:

- exact elapsed duration, such as `30 days`, `one season`, or `one year`;
- target date or deadline;
- event-relative horizon, such as `until the expedition leaves`;
- bounded chapter/time combination when the user explicitly wants both;
- a high-confidence inferred horizon from the user's nudge and current context.

The clock does not require a fully invented calendar. Day counts, relative dates, seasonal labels, or known in-world dates may be used according to the task.

If the user explicitly gives a time horizon, use it.

If the user does not give one, resolve in this order:

1. explicit current user instruction;
2. already-established active run contract;
3. high-confidence inference from the current nudge and current authority;
4. one concise clarification question only when the ambiguity would materially change the run.

Do not ask the user to restate a horizon that is already obvious from context.

## Time must leave residue

Time is not satisfied by date labels alone.

When a run skips meaningful time, later scenes should contain concrete evidence that life continued off-page. Relevant evidence may include body, weather, money, work, relationships, gear, reputation, geography, household routine, ecology, obligations, correspondence, rank, or magic practice.

For an intentional gap greater than roughly two days, the next lived phase should normally establish at least two concrete consequences of elapsed time before settling fully into the new action. This is a diagnostic default, not a prose quota.

Longer horizons must not collapse into a sequence of consecutive-feeling mornings.

## Constraint contract

Every temporal run must carry at least one meaningful constraint besides the existence of a clock.

Constraints exist to create a useful experimental question. Examples include:

- a Gold-caliber party must appear meaningfully;
- action density should rise;
- remain in one city for the whole run;
- Greg may not gain a rank during the run;
- a relationship must face distance rather than combat pressure;
- preserve ordinary-life texture while fantasy escalation increases;
- no chosen-one resolution;
- a particular artifact remains bounded and costly;
- one expedition, job, social obligation, or route must create the run's spine;
- a specific count or threshold when the user explicitly requests one.

Constraints have two strengths:

### Hard constraints

Pass/fail requirements. Explicit quantities, deadlines, prohibitions, required appearances, and direct `must` / `do not` instructions are hard by default.

### Soft nudges

Taste and pressure adjustments. Phrases such as `more action`, `a little more tropes`, `more romance`, `less work`, or `make it messier` are soft by default unless the user frames them as a requirement.

A soft nudge should change selection pressure, not become a mechanical quota.

## Nudge resolution

Natural-language user nudges are valid engine control.

Examples:

- `do a year` -> set or replace the clock with a one-year horizon;
- `Gold party` -> add a meaningful Gold-party constraint without requiring that party to dominate every chapter;
- `more action` -> raise action-selection pressure;
- `a little more tropes` -> permit more recognizable fantasy/isekai pleasures without replacing R2's character-first identity;
- `don't make Greg Gold yet` -> add a hard negative progression constraint;
- `keep going` -> continue the current run contract if one exists rather than reopening setup questions.

New nudges modify the current run contract unless they clearly start a new experiment.

A nudge does not silently become permanent project canon or global doctrine.

## Word count and output mass

Time and prose mass are separate.

Word count may be used as a fidelity target, especially for experiments that need chapter-sized rehearsal, but it does not prove temporal success or experiential completeness.

Unless the user explicitly makes word count hard:

- under-target prose should be challenged for missing lived phases, aftermath, transitions, relationships, waiting, physical environment, or social texture;
- it should not be padded with repeated explanation;
- a complete shorter scene may survive;
- the engine should prefer more **life per word** over arbitrary mass.

## Planner / renderer firewall

The planner, run-state manager, and scrubber may see the full Temporal Engine, Run Contract, survivor doctrine, anti-patterns, and experimental labels.

The prose renderer should not.

Before prose generation, reduce planning state into a compact **Scene Packet** containing only what the scene needs:

- current fictional time / elapsed gap;
- location and physical situation;
- current concrete state changes;
- people present and what they want now;
- the active task, pressure, or interruption;
- the one or two run constraints materially relevant to this scene;
- facts that may not be contradicted;
- consequences that should survive the scene.

Do not feed the prose renderer architecture vocabulary merely because the planner uses it.

Story prose must not mention experiment machinery such as `horizon`, `rehearsal`, `quarry`, `canon`, `authority`, `constraint`, alternate versions, generator instructions, or audit verdicts unless a word independently belongs naturally in the fictional scene.

The post-render scrubber again sees the full doctrine and removes leakage, repeated evaluator fragments, explanatory thesis lines, and other long-run renderer residue.

## Storage

Keep doctrine compact and reusable:

- `r2/editorial/character-rebuild/TEMPORAL_ENGINE.md` remains the durable engine method;
- `r2/editorial/character-rebuild/TEMPORAL_RUN_TEMPLATE.md` defines the reusable per-run contract and scene-packet handoff;
- each substantial temporal experiment stores its instantiated run contract inside its own branch/folder;
- do not create one permanent simulation ledger for all possible futures;
- `r2/FUTURE_SURVIVOR_PROTOCOL.md` consumes useful temporal output but never treats a speculative contract as canon;
- root `AGENTS.md` routes temporal/year/season/future-rehearsal work to the engine.

## Authority boundary

The Temporal Engine being active on `main` means the **method** is active.

It does not mean speculative future prose is accepted story authority.

Accepted R2 story state and selected prose on current `main` remain authoritative. Temporal runs live on branches or experimental folders until their discoveries are re-performed and selected through normal R2 production.

## Success criteria

The rewrite succeeds when a fresh repository-aware worker can:

1. recognize a temporal/year/season/future-run request from `AGENTS.md`;
2. identify or infer a fictional time horizon without unnecessary questions;
3. record at least one meaningful hard constraint or soft nudge;
4. continue an existing run after a simple `continue` instruction;
5. make elapsed time leave visible residue;
6. keep planning/audit vocabulary out of Greg-facing prose;
7. treat word count as fidelity evidence rather than temporal proof unless explicitly hard;
8. leave an instantiated run contract durable enough that another worker can resume without chat archaeology;
9. preserve the existing Future Survivor authority boundary.

## Non-goals

This change does not:

- canonize the completed one-year Black Stair experiment;
- replace the Manuscript Engine;
- invent a permanent R2 calendar;
- create a global simulation of every character;
- require every future run to last a season or year;
- impose fixed fight, romance, work, or trope quotas unless the user explicitly requests them;
- make temporal branches directly publishable.