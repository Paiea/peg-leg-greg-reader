# Experiment B — Distributed Temporal Prose

Status: ACTIVE EXPERIMENTAL EVIDENCE ONLY

Branch: `experiment/r2-temporal-b-distributed-prose`

Accepted base: `main` at `41792464ef312963eca0f0fae7cc0a521b66f767`

Accepted written frontier at freeze: **Chapter 48 — The Member**

Experiment A is frozen and separate. Its branch, prose, state, PR #248, and publication candidate are not inputs to B.

## Question

Can several temporal regions actually write future chapters independently, then reconcile enough speculative prose to materially increase accepted R2 chapter throughput?

## Window ownership

- A: Chapters 49–62 — high speculative confidence
- B: Chapters 61–74 — moderate speculative confidence
- C: Chapters 73–86 — low speculative confidence
- D: Chapters 85–98 — reconnaissance prose

Intentional seam overlaps:

- A/B: 61–62
- B/C: 73–74
- C/D: 85–86

## Execution contract

1. Freeze common seed from accepted authority.
2. Write all four first-pass windows as chapter-complete prose.
3. Preserve window independence: no later window may consume another window's first-pass prose before completing its own first pass.
4. Do not publish anything while first-pass windows are being produced.
5. Preserve original first-pass window prose unchanged.
6. Reconcile only after A–D exist.
7. Classify seam behavior and every speculative chapter.
8. Build the strongest contiguous candidate from Chapter 49 onward.
9. Rehearse the connected candidate run and repair only what clearly loses.
10. Publish only the maximum contiguous survivor through the normal R2 written-production route against newest `main`.
11. Keep all B evidence experimental. Public reader must never depend on B paths.
12. Record compact receipt and stop.

## Independence discipline for this execution surface

True concurrent creative subagents are not available in this chat surface. Preserve the experiment's independence semantics by treating each window as a sealed writer session:

- each window sees only accepted authority + `seed.md` + its own projected entry condition + normal R2 artistic guidance;
- the model does not inspect previously written B window prose while composing a later window's first pass;
- each first pass is committed durably before moving to the next sealed window;
- cross-window comparison begins only after all four are durable.

This is weaker wall-clock parallelism than four simultaneous agents and must be reported honestly in `receipt.md`, but it still tests the core reconciliation question: whether independently extrapolated future prose survives when brought back together.
