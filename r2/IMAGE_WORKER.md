# R2 IMAGE WORKER ENGINE

This is the reusable execution contract for parallel R2 chapter-image workers.

The worker is disposable. GitHub and ChatGPT Library are durable.

## Default user starter

A fresh chat may be started with only:

```text
Continue R2 image production from current GitHub authority.
Auto-claim one eligible unclaimed chapter image transaction. Read the actual chapter source, choose about five visually distinct source-grounded scenes, use the R2 visual/story brains and approved continuity references, generate and review one image per useful scene, stage approved outputs to the R2 ChatGPT Library, leave the next handshake, then stop.
Preserve newer authority, treat chapter titles as metadata rather than image source, and do not overlap another worker.
```

The worker must recover the rest from repository authority rather than asking Keoni to restate the system.

## Read first

Fresh-read:

- root `AGENTS.md`
- `state/PROJECT_STATE.md`
- `r2/README.md`
- `r2/PIPELINE.md`
- `r2/IMAGE_SYSTEM.md`
- `r2/visual-state/R2_VISUAL_CANON.md`
- the exact current chapter source after claiming, normally `r2/assets/written/chNNN.md` when present
- only the task-relevant character/setting/story brain files that materially clarify the chosen scenes and do not conflict with current R2 authority

Do not preload unrelated Run 1 visual state as authority.

## Hard grounding rule

> CHAPTER TITLE IS METADATA, NOT IMAGE SOURCE.

Never generate chapter art from the chapter title, role label, chapter manifest summary, or vague chapter mood alone.

For every generated image, the worker must be able to point to a real moment in the current chapter source and explain what physically happens there. If the exact chapter source cannot be found or is too incomplete to resolve scenes safely, do not improvise a title-poster. Record the authority gap and stop or escalate.

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

### 3. READ THE CHAPTER

Read the exact current chapter source substantially enough to understand the whole chapter, not merely its title or opening paragraph.

The chapter title may help identify the file. It must not determine the composition.

Before generation, produce a compact scene shortlist from the chapter itself. Default target:

- about five visually distinct moments
- each moment must have a concrete action, interaction, object, place, or state change
- avoid five variations of the same pose or conversation beat
- prefer moments that reveal character, work, place, relationship, consequence, or material progression

If the chapter genuinely has fewer than five image-worthy moments, use fewer. Do not manufacture filler.

### 4. RESOLVE FIVE SCENE JOBS

For each selected moment, record:

- exact source file
- source excerpt or tightly faithful source evidence
- concise scene truth
- who is present
- what is physically happening
- location / material environment
- why the image earns a slot
- must-show details
- must-not-show details
- relevant continuity references

Use `image-packets/TEMPLATE.md` as the transaction record.

Normal chapter transaction target:

- up to five scene-specific generated images
- normally one image per selected scene
- one may function as the chapter anchor
- the others are support/texture/story images if approved

The five-image target is a production batch, not a publication quota. The site may ultimately publish fewer.

### 5. RETRIEVE CONTINUITY AND BRAINS

Retrieve the smallest useful reference neighborhood from current R2 visual canon and approved Library canon assets.

Also consult task-relevant story brains when they materially constrain a chosen scene, such as character identity, setting use, recurring objects, or relationship state. Current R2 chapter/story authority remains higher than older Run 1 state.

Do not let Run 1 disability state leak into early R2. Until current R2 authority establishes otherwise, Greg has both legs intact.

If a required identity/location/style anchor does not exist, do not let a routine chapter worker silently invent durable canon. Route that missing anchor as a higher-thinking visual-canon transaction.

### 6. GENERATE AND REVIEW

Generate one image for each resolved scene job using its actual source moment plus the relevant visual canon and continuity references.

Do not prompt primarily with the chapter title. Do not turn role-title language such as `The Contractor`, `The Fighter`, or `The Investor` into literal poster concepts unless the chosen source scene itself supports that composition.

Keep composition varied and scene-specific.

Review each output as:

- approved
- revise
- rejected

Reject or revise outputs that are attractive but not grounded in the selected source moment.

Use failure tags from `IMAGE_SYSTEM.md` when they improve the next attempt.

### 7. STAGE TO CHATGPT LIBRARY

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

### 8. RECORD

Before stopping:

- keep the claim PR/branch truthful
- record the five-scene shortlist and which scenes were actually generated
- record source evidence, image IDs, approval status, Library paths, intended repository paths, and any promoted continuity evidence
- reconcile textual state against newer `main` if it moved
- leave a compact next-worker handshake

The chapter worker does not need to build a user-facing ZIP after every transaction.

### 9. STOP

After the claimed chapter transaction is recorded and staged as far as the available binary route allows, **stop**.

Do not claim another chapter in the same chat.

The next chapter belongs to a fresh worker that reconstructs from current authority.

## Model routing

### Routine default

Routine chapter workers may use **Instant** when available because the transaction is narrow and heavily constrained by durable authority.

Instant is appropriate only when the worker actually performs the grounding steps above. A cheap worker that skips the chapter source is not acceptable production.

### Escalate to higher thinking

Use a higher-thinking worker for:

- new or replacement visual-canon anchors
- new recurring character/location identity decisions
- conflicting authority
- repeated generation drift
- ambiguous visual interpretation
- inability to identify five strong scene moments without inventing meaning
- major cover/frontdoor art
- image-system or release-system architecture

The expensive judgment should improve future workers, not merely make one ordinary support image slightly nicer.

## Handshake

A completed chapter worker should leave a restart instruction that routes to a **fresh chat**, for example:

```text
Start a fresh R2 image worker from current GitHub authority. Auto-claim the next eligible unclaimed chapter image transaction. Read the actual chapter source, choose source-grounded scene moments, preserve current R2 visual canon and Library staging state, and do not overlap active image claims.
```
