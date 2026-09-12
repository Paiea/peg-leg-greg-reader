# R2 Written Production

Status: **ACTIVE FORWARD PUBLICATION POLICY**

R2 is itself a public experiment.

The live R2 reader is the normal human-facing surface for the current selected written experiment. A selected chapter does not need a second canon-promotion ceremony merely because its story search, rehearsal, evaluation, or deeper development memory lives on an experiment branch.

## Default forward route

For a normal Greg, Again written chapter:

```text
CURRENT STORY AUTHORITY
→ WHAT SHOULD ACTUALLY HAPPEN NEXT?
→ STORY SEARCH / PERFORMANCE IF EARNED
→ SHARED GREG SURFACE
→ WRITTEN FINISH
→ LOCAL EVALUATION + A-ZONE VARIANCE CHECK + VERIFICATION
→ SELECTED WRITTEN CHAPTER
→ LIVE R2 READER ON MAIN
```

> **SELECTED + VERIFIED WRITTEN CHAPTERS PUBLISH TO THE R2 SITE BY DEFAULT.**

Do not stop at `selected on experiment branch` merely to preserve an extra promotion gate.

The A-zone variance check is a compact diagnostic from `r2/FUTURE_SURVIVOR_PROTOCOL.md`, not a second selection ceremony. It asks whether familiar successful R2 grammar is still earned by the specific scene. It does not require a rewrite or reward novelty for its own sake.

## Future survivor evidence

When unaccepted temporal-survivor material exists near the current written frontier, consult `r2/FUTURE_SURVIVOR_PROTOCOL.md` before inventing the next run cold.

Future survivor material is rehearsal/challenger evidence, not story authority and not a publication queue. Read newest accepted authority first, inspect only the relevant survivor/reconciliation evidence, then still ask:

> **WHAT SHOULD ACTUALLY HAPPEN NEXT?**

When a speculative unit approaches publication territory, prefer fresh re-performance against current Story State and recent exact prose. Preserve old wording only where it still wins. A missing, stale, conflicting, or inaccessible survivor experiment never blocks normal forward production.

Before publishing prose descended from speculative temporal material, run the `Embodiment challenger` and `Connected-listen challenger` in `r2/FUTURE_SURVIVOR_PROTOCOL.md`. Causal completeness is not enough by itself; speculative-origin prose must still earn normal R2 experiential and listening fidelity.

After a substantial contiguous accepted run, use the cold adversarial run audit defined in `r2/FUTURE_SURVIVOR_PROTOCOL.md` when practical. Roughly 40–50 accepted chapters is a useful default checkpoint, especially before another large forward generation or promotion wave. The audit informs future judgment and targeted revision; it is not an automatic rollback, rewrite quota, or publication blocker.

## What stays experimental

Story-search files, rehearsals, evaluations, long-range maps, Seven Lamps/world-iceberg memory, performance experiments, and other development evidence may remain on their working branch when that is the safest or clearest ownership model.

The public site publishes the selected written rendition, not the development archaeology behind it.

Public R2 publication means:

> **this is the current readable R2 experiment**

It does **not** mean:

- immutable final canon
- Run 1 canon promotion
- all future wording is frozen
- audio or images must already exist
- every theory/rehearsal file should be merged to `main`

Newer explicit author authority or later selected revisions may replace a published R2 written rendition.

## Exact prose rule

Prefer the exact selected written prose rather than maintaining a manually cleaned duplicate.

The R2 chapter renderer strips the internal prelude before the first `---`, so a selected Greg, Again prose file may be reused byte-for-byte at:

`r2/assets/written/chNNN.md`

when its story body is the approved written rendition.

This reduces drift between the selected prose and the public reader.

Do not publish an unselected draft, candidate, theorycraft, story-search file, or rehearsal as chapter prose.

## Publication transaction

After a chapter is selected and verified:

1. Fresh-read newest `main` and preserve newer authority.
2. Publish the exact selected written rendition to `r2/assets/written/chNNN.md`.
3. Before publication, verify the selected title against `TITLE_POLICY.md`: it must name who Greg is being, not merely the object/event/place/topic of the chapter. Then create/update `r2/data/chapters/chNNN.json`.
4. Update neighboring previous/next navigation.
5. Append the stable chapter ID to `r2/data/project.json` and move `current_chapter` when appropriate.
6. Update `r2/data/chapter-registry.json` so written authority, title, and production gaps are accurate.
7. Leave unavailable audio/images unavailable. Missing sibling media must not block Read publication.
8. Run/inspect the R2 reader verification surface available to the worker. When local tests are available, use `python -m unittest tests.test_r2_site -v`.
9. Re-read newest `main` before integration and reconcile if it moved.
10. Merge the small publication transaction and verify the live reader manifests afterward.

## Concurrency

Audio, image, and story workers may be active simultaneously.

Never restore stale shared manifests over newer work.

If `main` moves while publishing, rebuild/reconcile the publication transaction on the newer head before merge.

Chapter number / stable ID owns identity. Title is mutable metadata, but selected/public titles must obey `TITLE_POLICY.md`: ask **Who is Greg in this chapter?** and use an embodied Greg-role title. Downstream site/audio metadata follows that selected title by stable chapter number.

## Local story freedom

Immediate site publication does not change the story engine.

The writer still begins with:

> **WHAT SHOULD ACTUALLY HAPPEN NEXT?**

Do not write toward the website, audio queue, image queue, publication cadence, or a cold-audit score. Write/select the chapter first. Publication follows selection; publication does not select the story.
