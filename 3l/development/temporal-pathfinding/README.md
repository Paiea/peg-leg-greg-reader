# 3L Temporal Pathfinding

Status: EXPERIMENTAL STORY-DEVELOPMENT EVIDENCE

Accepted canon stops at the manuscript frontier on `main`. This folder cannot directly advance canon.

The purpose of this workspace is to let multiple temporal perspectives search the same forty-year Life-Two story from different distances, then reconcile what actually survives. It is a development surface, not a second story authority.

## Run order

1. Read `PROSE_LOCK.md`.
2. Read `seed.md`.
3. Read `map-300.md` as the map manifest and `map/*.md` as disposable search space.
4. Run A/B/C/D independently from `windows/*.md`.
5. Preserve all four first-pass window outputs unchanged.
6. Reconcile the intentional overlaps through `seams/*.md`.
7. Run the connected life through `rehearsal.md`.
8. Promote only explicit survivors through `story-sync.md`.
9. Resume normal prose from Record 011 only after a near-future runway survives.

## File purposes

| File | Purpose |
| --- | --- |
| `PROSE_LOCK.md` | Locked prose/narrative rules established by Records 001-010. |
| `seed.md` | Compact accepted state at the Record-010 frontier plus open obligations. |
| `map-300.md` | Manifest for the disposable 300-Record search surface. |
| `map/a-001-090.md` | Original map slice used by Window A. |
| `map/b-081-170.md` | Original map slice used by Window B. |
| `map/c-161-250.md` | Original map slice used by Window C. |
| `map/d-241-300.md` | Original map slice used by Window D plus the first obligation pass. |
| `windows/a.md` | High-confidence early temporal work order, Records 011-090. |
| `windows/b.md` | Moderate-confidence accumulation work order, Records 081-170. |
| `windows/c.md` | Low-confidence loss/revenge/rebuilding work order, Records 161-250. |
| `windows/d.md` | Reconnaissance and backward-obligation work order, Records 241-300. |
| `windows/*-first-pass.md` | Immutable first-pass results created by the four workers. |
| `seams/a-b.md` | Reconciliation surface for Records 081-090. |
| `seams/b-c.md` | Reconciliation surface for Records 161-170. |
| `seams/c-d.md` | Reconciliation surface for Records 241-250. |
| `rehearsal.md` | Connected 011-300 life rehearsal after first-pass seams are understood. |
| `story-sync.md` | Explicit promotion boundary from experimental development into accepted story direction. |
| `receipt.md` | Compact evidence of what the run completed, discovered, killed, preserved, and promoted. |

## Authority boundary

Temporal pathfinding workers never directly edit:

- `3l/manuscript/`
- `3l/audio/`
- generated/public reader files
- `3l/STORY_AUTHORITY.md`
- `3l/PROMISE_LEDGER.md`

First-pass work belongs only in this workspace.

Canon manuscript prose outranks the map, every window, every seam, rehearsal output, and Story Sync note. If later prose discovers a better life, the engine recomputes around the prose.

## Independence rule

A, B, C, and D produce their first passes independently. A later window may use the common seed and its own provisional map slice, but it must not quietly consume a completed sibling first pass before producing its own trajectory.

The overlap is intentional. It tests convergence.

A fork is evidence. Do not average it away.

## Four-tab startup

Open four normal ChatGPT tabs. Paste one prompt into each tab. The four tabs may run at the same time.

### Window A prompt

```text
Continue 3L temporal pathfinding in Paiea/peg-leg-greg-reader on branch 3l/temporal-pathfinding-engine.

You are TEMPORAL WINDOW A.

Read and obey:
- 3l/development/temporal-pathfinding/PROSE_LOCK.md
- 3l/development/temporal-pathfinding/seed.md
- 3l/development/temporal-pathfinding/map-300.md
- 3l/development/temporal-pathfinding/map/a-001-090.md
- 3l/development/temporal-pathfinding/windows/a.md
- 3l/STORY_AUTHORITY.md
- 3l/PROMISE_LEDGER.md

Execute Window A exactly as a first-pass pathfinding worker. Do not write manuscript prose. Do not read completed B/C/D first-pass outputs before your first pass is durable. Treat the 300-map as disposable hypotheses. Preserve forks.

Write only the completed Window A first pass to:
3l/development/temporal-pathfinding/windows/a-first-pass.md

Do not modify canon, audio, reader files, Story Authority, Promise Ledger, seams, rehearsal, receipt, or Story Sync.
```

### Window B prompt

```text
Continue 3L temporal pathfinding in Paiea/peg-leg-greg-reader on branch 3l/temporal-pathfinding-engine.

You are TEMPORAL WINDOW B.

Read and obey:
- 3l/development/temporal-pathfinding/PROSE_LOCK.md
- 3l/development/temporal-pathfinding/seed.md
- 3l/development/temporal-pathfinding/map-300.md
- 3l/development/temporal-pathfinding/map/b-081-170.md
- 3l/development/temporal-pathfinding/windows/b.md
- 3l/STORY_AUTHORITY.md
- 3l/PROMISE_LEDGER.md

Execute Window B exactly as a first-pass pathfinding worker. Do not write manuscript prose. Do not read completed A/C/D first-pass outputs before your first pass is durable. Treat the 300-map as disposable hypotheses. Preserve forks.

Write only the completed Window B first pass to:
3l/development/temporal-pathfinding/windows/b-first-pass.md

Do not modify canon, audio, reader files, Story Authority, Promise Ledger, seams, rehearsal, receipt, or Story Sync.
```

### Window C prompt

```text
Continue 3L temporal pathfinding in Paiea/peg-leg-greg-reader on branch 3l/temporal-pathfinding-engine.

You are TEMPORAL WINDOW C.

Read and obey:
- 3l/development/temporal-pathfinding/PROSE_LOCK.md
- 3l/development/temporal-pathfinding/seed.md
- 3l/development/temporal-pathfinding/map-300.md
- 3l/development/temporal-pathfinding/map/c-161-250.md
- 3l/development/temporal-pathfinding/windows/c.md
- 3l/STORY_AUTHORITY.md
- 3l/PROMISE_LEDGER.md

Execute Window C exactly as a first-pass pathfinding worker. Do not write manuscript prose. Do not read completed A/B/D first-pass outputs before your first pass is durable. Treat the 300-map as disposable hypotheses. Preserve forks.

Write only the completed Window C first pass to:
3l/development/temporal-pathfinding/windows/c-first-pass.md

Do not modify canon, audio, reader files, Story Authority, Promise Ledger, seams, rehearsal, receipt, or Story Sync.
```

### Window D prompt

```text
Continue 3L temporal pathfinding in Paiea/peg-leg-greg-reader on branch 3l/temporal-pathfinding-engine.

You are TEMPORAL WINDOW D.

Read and obey:
- 3l/development/temporal-pathfinding/PROSE_LOCK.md
- 3l/development/temporal-pathfinding/seed.md
- 3l/development/temporal-pathfinding/map-300.md
- 3l/development/temporal-pathfinding/map/d-241-300.md
- 3l/development/temporal-pathfinding/windows/d.md
- 3l/STORY_AUTHORITY.md
- 3l/PROMISE_LEDGER.md

Execute Window D exactly as a first-pass pathfinding worker. Do not write manuscript prose. Do not read completed A/B/C first-pass outputs before your first pass is durable. Treat the 300-map as disposable hypotheses. Preserve forks. Separate backward requirements from possible earlier events.

Write only the completed Window D first pass to:
3l/development/temporal-pathfinding/windows/d-first-pass.md

Do not modify canon, audio, reader files, Story Authority, Promise Ledger, seams, rehearsal, receipt, or Story Sync.
```

## Reconciliation startup

Do not launch reconciliation until all four first-pass output files exist.

```text
Continue 3L temporal pathfinding in Paiea/peg-leg-greg-reader on branch 3l/temporal-pathfinding-engine.

Do not begin until all four files exist:
- 3l/development/temporal-pathfinding/windows/a-first-pass.md
- 3l/development/temporal-pathfinding/windows/b-first-pass.md
- 3l/development/temporal-pathfinding/windows/c-first-pass.md
- 3l/development/temporal-pathfinding/windows/d-first-pass.md

Read PROSE_LOCK.md, seed.md, all four immutable first passes, the three seam templates, rehearsal.md, STORY_AUTHORITY.md, and PROMISE_LEDGER.md.

Preserve all four first-pass files unchanged.

Reconcile:
- A/B at Records 081-090
- B/C at Records 161-170
- C/D at Records 241-250

Use only CONVERGED, MINOR DIVERGENCE, MAJOR DIVERGENCE, or FORK for each seam. Do not average genuine forks.

Then perform the connected rehearsal in rehearsal.md. Do not modify canon prose.

When the connected life is coherent enough, update story-sync.md only with pressures, directions, institutions, obligations, or short near-future runs that genuinely survived. Leave uncertain material explicitly unpromoted.

Update receipt.md with what actually completed and whether the project is ready to resume Record 011 prose.
```

## Recovery rule

Apply `3l/WORK_RECOVERY_AUTHORITY.md`.

If one temporal window stalls:

1. do not restart completed siblings;
2. retry the stalled worker once;
3. if the same mechanism fails again for the same reason, preserve every completed first pass and rerun only the missing window from its frozen work order through the simplest available path;
4. do not begin seam reconciliation until all four first passes exist.

A temporal-engine failure never blocks readable prose or audio production.
