# R2 IMAGE WORKER ENGINE

This is the reusable execution contract for parallel R2 chapter-image workers.

The worker is disposable. GitHub and ChatGPT Library are durable.

## Default user starter

A fresh chat may be started with only:

```text
Continue R2 image production from current GitHub authority.
Auto-claim one eligible unclaimed chapter image transaction, use the R2 image-production protocol, stage approved outputs to the R2 ChatGPT Library, leave the next handshake, then stop.
Preserve newer authority and do not overlap another worker.
```

The worker must recover the rest from repository authority rather than asking Keoni to restate the system.

## Read first

Fresh-read:

- root `AGENTS.md`
- `state/PROJECT_STATE.md`
- `r2/README.md`
- `r2/IMAGE_SYSTEM.md`
- `r2/visual-state/R2_VISUAL_CANON.md`
- the current chapter manifest/written/story evidence only after claiming a chapter

Do not preload unrelated Run 1 visual state as authority.

## One-transaction lifecycle

### 1. ORIENT

- read current `main`
- inspect open image PRs and active `image/r2-*` branches
- identify chapters already owned or already adequately illustrated
- identify the next eligible unclaimed chapter

### 2. CLAIM

Create a dedicated branch and draft PR before generation.

Recommended branch shape:

```text
image/r2-chNNN-<short-scene-or-role>
```

The PR body must say clearly that the worker owns **R2 Chapter N images only**.

If the chapter becomes claimed by another worker first, do not overlap it. Refresh authority and take the next eligible chapter.

### 3. RESOLVE THE JOB

Read the exact current chapter/story surface and choose only images that earn their place.

Normal maximum:

- one anchor
- zero to two support/texture images

Zero useful images is allowed. Do not manufacture filler merely to complete a quota.

Use `image-packets/TEMPLATE.md` as the transaction record.

### 4. RETRIEVE CONTINUITY

Retrieve the smallest useful reference neighborhood from current R2 visual canon and approved Library canon assets.

Do not let Run 1 disability state leak into early R2. Until current R2 authority establishes otherwise, Greg has both legs intact.

If a required identity/location/style anchor does not exist, do not let a routine chapter worker silently invent durable canon. Route that missing anchor as a higher-thinking visual-canon transaction.

### 5. GENERATE AND REVIEW

Generate the bounded chapter set. Keep composition varied and scene-specific.

Review each output as:

- approved
- revise
- rejected

Use failure tags from `IMAGE_SYSTEM.md` when they improve the next attempt.

### 6. STAGE TO CHATGPT LIBRARY

Shared R2 image warehouse:

```text
/Peg-Leg Greg Image Integration/R2/
  00 Canon/
  01 Incoming/
  02 Approved/
  03 Releases/
  04 Released/
```

For normal chapter work:

- generated keepers may enter `01 Incoming/chNNN/`
- approved release-ready keepers belong in `02 Approved/chNNN/`
- use deterministic filenames that match intended repository destinations

When a generated result has a safe file reference, route it to Library directly.

If safe bytes are not exposed for Library upload, record `library_stage_pending` and preserve the narrowest manual handoff possible. Never claim the binary is staged without evidence.

### 7. RECORD

Before stopping:

- keep the claim PR/branch truthful
- record image IDs, approval status, Library paths, intended repository paths, and any promoted continuity evidence
- reconcile textual state against newer `main` if it moved
- leave a compact next-worker handshake

The chapter worker does not need to build a user-facing ZIP after every transaction.

### 8. STOP

After the claimed chapter transaction is recorded and staged as far as the available binary route allows, **stop**.

Do not claim another chapter in the same chat.

The next chapter belongs to a fresh worker that reconstructs from current authority.

## Model routing

### Routine default

Routine chapter workers may use **Instant** when available because the transaction is narrow and heavily constrained by durable authority.

### Escalate to higher thinking

Use a higher-thinking worker for:

- new or replacement visual-canon anchors
- new recurring character/location identity decisions
- conflicting authority
- repeated generation drift
- ambiguous visual interpretation
- major cover/frontdoor art
- image-system or release-system architecture

The expensive judgment should improve future workers, not merely make one ordinary support image slightly nicer.

## Handshake

A completed chapter worker should leave a restart instruction that routes to a **fresh chat**, for example:

```text
Start a fresh R2 image worker from current GitHub authority. Auto-claim the next eligible unclaimed chapter image transaction. Preserve current R2 visual canon and Library staging state. Do not overlap active image claims.
```
