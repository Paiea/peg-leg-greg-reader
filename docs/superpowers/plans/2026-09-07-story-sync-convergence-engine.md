# STORY SYNC / Convergence Engine Implementation Plan

**Goal:** add the smallest runnable long-form sync layer that preserves competing possibilities, promotes discoveries only through useful evidence, propagates strong discoveries in both temporal directions, triggers book-wide sync on book-shaping discoveries, and supports hidden canon / reader visibility without collapsing them.

**Authority:** build on `architecture/long-form-story-compiler`, which itself begins from PR #160 rehearsal authority. Do not fork the rehearsal engine or create a second manuscript authority.

## Task 1: Write executable sync contracts test-first

Create `tests/test_story_sync_engine.py` covering:

- four discovery confidence levels
- no one-take promotion to story truth
- repetition without multi-dimensional usefulness does not over-promote
- competing branches remain alive when both are viable
- strong discoveries produce forward and backward propagation targets
- book-shaping discoveries request immediate sync
- convergence phase is confidence-driven rather than chapter-number-driven
- hidden canon remains canon while invisible to reader
- reader-state validation detects a visible payoff supported only by hidden canon
- superseded assumptions keep replacement/evidence provenance

Run PR CI and confirm RED because `scripts.story_sync_engine` does not yet exist.

## Task 2: Implement minimal deterministic sync engine

Create `scripts/story_sync_engine.py` with inspectable functions for:

- validation / normalization of project sync state
- discovery scoring and promotion
- useful-evidence support counting
- branch viability and preservation
- contradiction handling
- bidirectional propagation planning
- event-driven sync trigger classification
- convergence-phase policy
- hidden canon / reader-state dependency validation
- sync report construction

Keep semantic quality judgments as explicit input evidence rather than pretending deterministic code can judge literature by itself.

Run focused tests, then full repository tests.

## Task 3: Wire into existing AI tool surface

Extend `scripts/plg_ai_tools.py` with a narrow `sync_story` entry point that:

- accepts an in-memory state or JSON path
- invokes the generalized sync engine
- optionally writes only derived sync output to a requested path
- never writes canon prose

Update tool-registry tests accordingly.

## Task 4: Add bounded Dragon Spotter trial

Add a small project-specific trial under `state/experiments/dragon-spotter/story-sync/` containing:

- sparse four-region possibility field
- several rehearsal-derived discoveries
- deliberate contradiction(s)
- one hidden-canon dependency
- one later payoff requiring earlier setup
- at least one weak branch expected to die

Add a tiny trial runner or fixture test that invokes the generalized sync engine and writes/validates a deterministic sync report.

The trial should demonstrate behavior, not generate a finished novel.

## Task 5: Verify and leave trailhead

Run focused + full tests through GitHub Actions, inspect failures systematically, and update the long-form state/trailhead with:

- current implementation status
- trial findings
- strongest thread(s)
- unresolved contradictions
- next highest-value rehearsal/generation target

Do not merge automatically unless separately authorized.