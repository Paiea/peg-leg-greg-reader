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
→ LOCAL EVALUATION + VERIFICATION
→ ROLE TITLE VALIDATION
→ SELECTED WRITTEN CHAPTER
→ LIVE R2 READER ON MAIN
```

> **SELECTED + VERIFIED WRITTEN CHAPTERS PUBLISH TO THE R2 SITE BY DEFAULT.**

Do not stop at `selected on experiment branch` merely to preserve an extra promotion gate.

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

## Selected chapter title gate

`r2/TITLE_POLICY.md` owns R2 chapter-title semantics.

Working story-search, rehearsal, or development titles may remain provisional. Before a chapter becomes the selected/public written rendition, read the actual chapter and ask:

> **Who is Greg in this chapter?**

The selected heading must name a role, social position, temporary function, relational identity, situational identity, or clean metaphorical role Greg actually inhabits. A title that merely names an object, event, place, time span, abstraction, problem, or chapter topic does not pass selection. A role that materially belongs to somebody else also does not pass.

Duplicate roles are allowed when they are true. Do not invent awkward occupational nouns merely to satisfy the pattern. Do not create a second `role` metadata field that can drift from `title`.

For a selected/public chapter, the first-line heading at `r2/assets/written/chNNN.md` is semantic title authority. Public chapter manifests, production registry metadata, audio title metadata, and future divider-card labels follow that selected heading by stable chapter number.

A title change never changes chapter identity. `r2-chNNN`, `ga-NNN`, and the numeric chapter number remain stable.

Use `python scripts/sync_r2_role_titles.py --check` as the parity guard after the selected chapter and its public metadata are assembled. For a deliberate title-only repair, reconcile newest `main` first, change the selected heading, and use `--apply` only against that current authority so shared manifests are not restored from stale state.

## Publication transaction

After a chapter is selected and verified:

1. Fresh-read newest `main` and preserve newer authority.
2. Publish the exact selected written rendition to `r2/assets/written/chNNN.md`, with a heading that passes `r2/TITLE_POLICY.md`.
3. Create/update `r2/data/chapters/chNNN.json` using the same selected role title.
4. Update neighboring previous/next navigation.
5. Append the stable chapter ID to `r2/data/project.json` and move `current_chapter` when appropriate.
6. Update `r2/data/chapter-registry.json` so written authority, selected title, and production gaps are accurate.
7. Leave unavailable audio/images unavailable. Missing sibling media must not block Read publication.
8. Run `python scripts/sync_r2_role_titles.py --check`, then inspect the R2 reader verification surface. When local tests are available, use `python -m unittest tests.test_r2_site -v`.
9. Re-read newest `main` before integration and reconcile if it moved.
10. Merge the small publication transaction and verify the live reader manifests afterward.

## Concurrency

Audio, image, and story workers may be active simultaneously.

Never restore stale shared manifests over newer work.

If `main` moves while publishing, rebuild/reconcile the publication transaction on the newer head before merge.

Chapter number / stable ID owns identity. Title is mutable metadata, and selected written authority owns its semantic value. A title mismatch is a metadata reconciliation problem, not evidence that existing audio or another published rendering disappeared.

## Local story freedom

Immediate site publication does not change the story engine.

The writer still begins with:

> **WHAT SHOULD ACTUALLY HAPPEN NEXT?**

Do not write toward the website, audio queue, image queue, or publication cadence. Write/select the chapter first. Publication follows selection; publication does not select the story.
