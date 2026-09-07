# Definitive Edition Visual Pilot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Queue exactly five creator-approved Definitive Edition image targets under the existing structural production hold while preserving the normal PLG illustration pipeline and correct early-story Greg continuity.

**Architecture:** Keep the global hold active and add a tiny bounded-approval input consumed only while that hold is active. Reuse the existing generation-queue record builder, character-reference selection, registry checks, PERFORMANCE-reference matching, and prompt-pack rendering. Explicit scene continuity overrides the current legacy Greg BKA/crutch prompt default for this early-story pilot.

**Tech Stack:** Python 3, JSON state files, existing PLG static illustration pipeline, direct assertion-based regression scripts.

**Spec:** `docs/superpowers/specs/2026-09-07-definitive-edition-visual-pilot.md`

## Global Constraints

- Canon prose remains the only story authority.
- `state/visual/PRODUCTION_HOLD.json` remains active and unchanged.
- Exactly five pilot candidates are authorized while the hold is active.
- `state/visual/ILLUSTRATION_APPROVALS.json` remains reserved for concrete post-generation asset decisions.
- Current live artwork is not deleted or replaced by this change.
- No broad image-generation authorization is introduced.

---

### Task 1: Bounded queue behavior

**Files:**
- Modify: `scripts/build_generation_queue.py`
- Create: `scripts/test_build_generation_queue.py`
- Create: `state/visual/BOUNDED_GENERATION_APPROVALS.json`

**Interfaces:**
- Consumes: normal candidate/registry/hold inputs plus a list of explicitly bounded approved candidate dictionaries.
- Produces: `build_generation_queue(..., bounded_candidates=None, generation_batch_id="") -> list[dict]` with normal queue records plus `generation_approval` and `generation_batch_id` on hold-authorized records.

- [ ] **Step 1: Write the failing regression test**

Create a regression script that proves all three required behaviors:

```python
held = build_generation_queue(
    [global_candidate],
    [],
    production_hold={"active": True},
    bounded_candidates=[approved_candidate],
    generation_batch_id="definitive-pilot-001",
)
assert [item["candidate_id"] for item in held] == [approved_candidate["id"]]
assert held[0]["generation_approval"] == "explicit_bounded"
assert held[0]["generation_batch_id"] == "definitive-pilot-001"

assert build_generation_queue(
    [global_candidate], [], production_hold={"active": True}
) == []

open_queue = build_generation_queue(
    [global_candidate],
    [],
    production_hold={"active": False},
    bounded_candidates=[approved_candidate],
    generation_batch_id="definitive-pilot-001",
)
assert [item["candidate_id"] for item in open_queue] == [global_candidate["id"]]
```

- [ ] **Step 2: Run the test and verify RED**

Run:

```bash
python scripts/test_build_generation_queue.py
```

Expected: failure because `build_generation_queue` does not yet accept `bounded_candidates`.

- [ ] **Step 3: Implement the minimal bounded override**

Add a loader for `state/visual/BOUNDED_GENERATION_APPROVALS.json`. While `edit_hold_active(production_hold)` is true, replace the normal candidate iterable with the approved bounded items. While the hold is false, ignore bounded candidates and preserve current behavior. Add audit metadata only to records queued through the bounded path.

- [ ] **Step 4: Run the regression test and verify GREEN**

Run:

```bash
python scripts/test_build_generation_queue.py
```

Expected: `build generation queue regressions passed`.

- [ ] **Step 5: Record exactly five approved pilot candidates**

Create `state/visual/BOUNDED_GENERATION_APPROVALS.json` with batch id `definitive-pilot-001`, source main SHA `292fe976b8444d9e024305e3523c2886c89ed966`, and exactly these IDs:

```text
de-ch005-player-reads-greg
de-ch005-jorren-offers-hand
de-ch007-antonius-reverses-frame
de-ch013-arlo-one-page
de-ch018-hessa-covers-bowl
```

Every item must use an exact current-canon paragraph anchor and explicit pre-amputation continuity notes.

### Task 2: Prompt-pack continuity override

**Files:**
- Modify: `scripts/build_prompt_packs.py`
- Create: `scripts/test_build_prompt_packs.py`

**Interfaces:**
- Consumes: a candidate dictionary with optional `continuity_notes`.
- Produces: `render_prompt_pack(candidate) -> str` where explicit continuity notes replace the legacy Greg BKA/crutch fallback.

- [ ] **Step 1: Write the failing continuity regression**

```python
candidate = {
    "id": "early-greg",
    "chapter": 5,
    "chapter_title": "THE WARRIOR",
    "kind": "chapter_illustration",
    "fit_target": "exact",
    "spoiler_level": "low",
    "status": "prompt_ready",
    "scene_summary": "Greg trains in the yard.",
    "visual_hook": "Greg down in the sand after his body lags.",
    "characters": ["Greg", "Jorren"],
    "continuity_notes": "Pre-amputation Greg: both legs intact; no crutches or prosthesis.",
}
text = render_prompt_pack(candidate)
assert "Pre-amputation Greg" in text
assert "permanent LEFT BKA" not in text
```

- [ ] **Step 2: Run the test and verify RED**

Run:

```bash
python scripts/test_build_prompt_packs.py
```

Expected: failure because the current renderer ignores `continuity_notes` and emits the legacy BKA/crutch line.

- [ ] **Step 3: Implement explicit continuity precedence**

In `_continuity_lines(candidate)`, if non-empty `continuity_notes` is supplied, emit it as the scene continuity instruction and do not append the static Greg BKA/crutch fallback. If no explicit continuity is supplied, preserve current legacy behavior.

- [ ] **Step 4: Make bounded candidates available to prompt-pack generation**

When the bounded approval file exists, merge its `items` with normal candidates by stable `id` before rendering prompt packs. Bounded records win only on duplicate id. This lets the existing prompt-pack path serve the pilot instead of creating a parallel prompt system.

- [ ] **Step 5: Run the continuity regression and verify GREEN**

Run:

```bash
python scripts/test_build_prompt_packs.py
```

Expected: `build prompt packs regressions passed`.

### Task 3: Generate and verify the five-item batch state

**Files:**
- Generate/update: `state/visual/GENERATION_QUEUE.json`
- Generate/update: `state/visual/GENERATION_PACKET.md`
- Generate/update: `state/visual/prompt-packs/de-ch005-player-reads-greg.md`
- Generate/update: `state/visual/prompt-packs/de-ch005-jorren-offers-hand.md`
- Generate/update: `state/visual/prompt-packs/de-ch007-antonius-reverses-frame.md`
- Generate/update: `state/visual/prompt-packs/de-ch013-arlo-one-page.md`
- Generate/update: `state/visual/prompt-packs/de-ch018-hessa-covers-bowl.md`

**Interfaces:**
- Consumes: bounded approval state, current registry, current character references, current hold, and current fresh PERFORMANCE round-trip references.
- Produces: exactly five `generation_ready` queue records and five prompt packs.

- [ ] **Step 1: Build the queue**

Run:

```bash
python scripts/build_generation_queue.py
```

Expected: hold remains active and exactly 5 explicitly approved records are ready.

- [ ] **Step 2: Build prompt packs**

Run:

```bash
python scripts/build_prompt_packs.py
```

Expected: five `de-` prompt packs exist and none contains the incorrect early-story BKA/crutch instruction.

- [ ] **Step 3: Build the next generation packet**

Run:

```bash
python scripts/build_generation_packet.py --limit 5
```

Expected: packet contains exactly the five pilot candidates.

- [ ] **Step 4: Verify A/B evidence attachment**

Check generated queue state:

```text
Ch005 x2: no durable PERFORMANCE reference required.
Ch007: PERFORMANCE reference present only if exact fresh anchor matches.
Ch013: PERFORMANCE reference present only if exact fresh anchor matches.
Ch018: PERFORMANCE reference present only if exact fresh anchor matches.
```

Do not force a stale or nonmatching PERFORMANCE reference into the queue.

- [ ] **Step 5: Verify hold and asset boundary**

Confirm:

```text
PRODUCTION_HOLD.json remains active.
ILLUSTRATION_APPROVALS.json remains post-generation-only.
No current live asset is removed.
No generated image is falsely marked approved before an asset exists.
```

### Task 4: Branch verification and handoff

**Files:**
- No new production files beyond Tasks 1-3.

**Interfaces:**
- Produces: a reviewable branch/PR that authorizes only the five next-generation image targets.

- [ ] **Step 1: Run focused regressions**

```bash
python scripts/test_build_generation_queue.py
python scripts/test_build_prompt_packs.py
```

Expected: both pass.

- [ ] **Step 2: Run existing project checks available in the checkout**

Run the repository's standard validation command(s) used by CI for visual/state changes. Any failure must be reported rather than ignored.

- [ ] **Step 3: Review the diff**

Verify no canon chapter prose, Showcase selection, live reader output, production hold, or existing live illustration status changed.

- [ ] **Step 4: Commit and open a pull request**

Commit with a bounded visual-pilot message and open a PR to `main` describing the five authorized generation targets and the temporal-continuity fix.