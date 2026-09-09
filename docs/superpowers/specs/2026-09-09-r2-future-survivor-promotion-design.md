# R2 Future Survivor Promotion Design

Status: DESIGN ONLY

Branch: `design/r2-future-survivor-promotion`

## Purpose

R2 now has evidence that speculative future work can remain useful across a long horizon, but the useful resolution falls as temporal distance increases. Near material can survive as prose. Middle material often survives as scene or chapter cores. Far material is most valuable as reconnaissance, pressure, and discovery.

The system needs a durable way to use that future evidence without confusing it with accepted story authority and without lowering final prose quality.

Core rule:

> **Fidelity follows confidence. Future work earns detail by surviving.**

## Current repository reality

As of `main` commit `6524611eeaae6383eeb7ff07ad0c93ee8aae8e93`, PR #252 has already published the Experiment B contiguous written run through Chapter 86.

This design does not retroactively undo that publication. Chapters 49–86 are now accepted written authority and are no longer treated as backlog material. Survivor rules apply only to unaccepted future territory beyond the current accepted frontier, plus any later experimental forks that have not been selected and published.

The publication of 49–86 is therefore historical evidence for why this protocol is needed, not the forward template for promoting speculative territory.

## Authority split

### Main owns doctrine and accepted output

`main` may contain:

- the durable protocol for discovering and using speculative future evidence
- accepted Story State and current R2 written authority
- selected and verified final chapter prose
- normal reader, registry, audio, and publication state

`main` should not carry the live speculative backlog itself by default.

### Experimental branches own future state

Future temporal work remains on experiment branches until it earns re-performance and publication.

Experimental branches may contain:

- A/B/C/D future territory
- first-pass speculative prose
- compressed chapter or scene cores
- far-future reconnaissance
- forks and losing alternatives
- seam reconciliation
- promotion classifications
- survivor receipts
- source pointers and branch-local indexes

None of this is story authority merely because it survived an experiment.

## Confidence and fidelity zones

The temporal field uses four rolling zones. Exact chapter counts may change by experiment, but the fidelity contract stays stable.

### A: Commit Zone

Purpose: next publication territory.

Expected form:

- full Shared Greg Surface
- listening-first prose at normal R2 quality
- complete experiential scenes
- connected rehearsal against newest accepted authority

A material may publish only after fresh performance, evaluation, verification, and normal R2 publication checks.

### B: Hot Speculation

Purpose: high-confidence future candidates close enough to deserve substantial execution.

Expected form:

- full or near-full prose
- embodied scenes
- strong continuity burden
- still challengeable and replaceable

B is not accepted prose authority. When promoted toward A, it must be re-read against current authority and normally re-performed rather than mechanically polished.

### C: Warm Speculation

Purpose: discover likely causal trajectory and durable scene structure without paying full prose cost.

Expected form:

- scene-complete or compressed chapter cores
- decisions, obligations, state changes, relationship motion, objects, money, geography, work, magic, and consequences
- prose only where embodiment materially helps judgment

C may preserve excellent lines and scenes, but its main value is causal and experiential discovery.

### D: Cold Speculation

Purpose: cheap far-future reconnaissance.

Expected form:

- pressures
- possibilities
- consequential scene sketches
- character and world motion
- future constraints and backward obligations
- explicit uncertainty

D should avoid brittle detail when a broader pressure carries the same discovery.

## Promotion ladder

The default rolling motion is:

```text
WRITE / RE-PERFORM A
WRITE B HARD
EXECUTE C SPECULATIVELY
SCOUT D CHEAPLY

RECONCILE

PUBLISH CONTIGUOUS A-SIDE WIN

B -> A
surviving C -> B
surviving D -> C

RE-PERFORM PROMOTED MATERIAL AT ITS NEW FIDELITY
INVALIDATE CONTRADICTED FUTURES
SPAWN NEW D AT THE FAR EDGE
CONTINUE
```

Promotion raises confidence and required fidelity. It does not convert speculative facts into canon automatically.

## Re-performance rule

When future material approaches accepted authority, do not simply expand or polish the old speculative text.

Provide the writer with:

1. newest accepted Story State and exact recent prose
2. surviving future discovery or scene truth
3. old speculative prose as rehearsal evidence and challenger material
4. any later discoveries that remain relevant

Then perform the chapter fresh through the normal R2 path:

```text
CURRENT STORY AUTHORITY
+ SURVIVING FUTURE EVIDENCE
+ OLD SPECULATIVE PROSE AS CHALLENGER
-> WHAT SHOULD ACTUALLY HAPPEN NEXT?
-> PERFORMANCE / STORY SEARCH IF EARNED
-> SHARED GREG SURFACE
-> WRITTEN FINISH
-> CONNECTED REHEARSAL
-> SOURCE WIN / REPERFORM / FORK / DISCOVERY ONLY / KILL
-> SELECT + VERIFY
-> PUBLISH
```

Old speculative wording survives only where it still wins.

## Survivor classification

Every future unit should be classifiable as one of:

- `SOURCE WIN`: existing speculative rendering still wins after current rehearsal
- `REPERFORM`: causal core survives but current scene/prose should be freshly rendered
- `FORK`: two or more viable trajectories remain materially distinct
- `DISCOVERY ONLY`: exact event or prose dies, but pressure, constraint, relationship motion, or other discovery remains useful
- `KILL`: no material value remains

Do not preserve speculative material because work was already spent on it.

## Backlog behavior

The backlog is a rehearsal and discovery bank, not a publication queue.

A future position may preserve:

- exact event identity
- only a causal pressure
- only a relationship or professional movement
- one strong scene
- an object or resource consequence
- a warning about a likely future failure

Chapter numbers inside far speculative territory are provisional. If an old speculative Chapter 103 naturally becomes Chapter 107 after current authority evolves, preserve the discovery rather than the old number.

## Discovery contract for fresh writers

The normal R2 writer should not invent forward material cold when relevant survivor evidence already exists, but it also should not treat that evidence as an outline.

Before substantial forward writing near a speculative frontier:

1. read newest accepted R2 authority
2. discover active temporal-survivor experiment branches using the repository's normal branch/WIP discovery rules
3. inspect only the survivor/reconciliation material relevant to the immediate horizon
4. treat it as challenger evidence, not story truth
5. ask `WHAT SHOULD ACTUALLY HAPPEN NEXT?` from current authority
6. preserve SOURCE when speculative material loses

A missing, stale, conflicting, or inaccessible survivor branch must never block normal forward writing.

## Main versus experiment data

Forward default:

- **protocol/doctrine** may graduate to `main`
- **live future backlog** remains experimental
- **accepted prose** graduates to `main` only through normal written production

Do not copy hundreds of speculative chapter files or live C/D queues into `main` merely for discoverability.

If later experiments prove branch discovery too fragile, a compact non-canon pointer/index on `main` may be designed separately. It is not required by this first implementation.

## Prose quality contract

A large future backlog is not permission to lower publication quality.

Promotion toward A should shift saved creative effort toward:

- listening clarity
- rhythmic variation
- physical and social embodiment
- dialogue ownership
- emotional messiness and human irrationality
- removal of redundant evaluative fragments
- deletion of principles already demonstrated by the scene
- preservation of Greg's specific voice without repetitive classification cadence

Final chapters should be judged against strong recent R2 prose, not against the quality of the speculative source they inherited.

## Relationship to Experiments A through D

- **Experiment A:** single-writer temporal horizon. Tests whether looking farther ahead improves immediate story selection and restraint.
- **Experiment B:** distributed temporal prose. Tests how much independently extrapolated future material survives reconciliation and reveals the natural fidelity gradient.
- **Experiment C:** multithreaded temporal cognition. Tests whether independent future perspectives improve NOW without requiring full far-future prose.
- **Experiment D:** hybrid rolling speculative execution. Uses confidence-weighted fidelity, promotion, re-performance, reconciliation, and far-edge respawn.

This protocol is designed so Experiment D can be tested without prematurely turning its live future field into accepted R2 authority.

## Minimal implementation scope

The first implementation should be intentionally small:

1. add a durable future-survivor protocol under `r2/`
2. add a short routing note to `r2/WRITTEN_PRODUCTION.md`
3. add a short worker-router note to `AGENTS.md` so fresh R2 narrative workers know future survivor evidence may exist
4. leave all current live speculative backlog files on experiment branches
5. do not add databases, scripts, queue managers, automatic promotion, or new root lanes

## Verification

Implementation verification should confirm:

- normal R2 writing still works when no survivor experiment exists
- speculative evidence is explicitly non-authoritative
- a fresh worker can discover how to use survivor evidence from main documentation
- publication still requires selected written prose through the existing normal route
- no reader, registry, audio, or image surface depends directly on experiment-branch paths
- no automatic promotion from C/D to accepted prose exists

## Success criteria

The design succeeds if R2 can maintain a deep speculative future while preserving these invariants:

1. accepted story authority remains clear
2. far future can be cheap and disposable
3. surviving material becomes more detailed only as confidence rises
4. old speculative prose is challenger evidence, not a fossilized draft
5. final listening prose can continue improving even if hundreds of future positions are queued
6. workers can benefit from future discoveries without being railroaded toward them
