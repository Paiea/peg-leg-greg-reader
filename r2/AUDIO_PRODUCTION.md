# Greg, Again — Audio Production Protocol

This file owns parallel audio-production coordination for R2 / Greg, Again.

It does **not** replace `r2/PIPELINE.md`. The pipeline owns Shared Greg Surface, Audio Finish, processing space, POV, and medium-specific repair. This file owns worker routing, claiming, provider submission, artifact capture, assembly, verification, publication, and handoff.

Current GitHub authority outranks chat history and stale handoff text.

## Default worker behavior

A fresh audio worker should not ask the human which chapter it owns unless GitHub state is genuinely ambiguous.

If the human did not explicitly assign a chapter, the worker must:

1. inspect current `main`
2. read root `AGENTS.md`
3. read `r2/PIPELINE.md`
4. read this file
5. inspect `greg-again/audio/manifest.json`
6. resolve the current authoritative Greg, Again written ref and enumerate its actual numbered prose files under `state/experiments/greg-again/prose/`
7. read current written state such as `state/experiments/greg-again/written/CURRENT.md` for story context / trailhead, but do not use a stale summary frontier as the numerical audio-eligibility gate
8. inspect live Greg, Again audio branches and open PRs
9. scan the actual written prose-file inventory upward for the earliest chapter that is unpublished and not already durably owned
10. create the single-chapter claim branch
11. refresh ownership evidence and verify the claim still does not overlap newer work
12. only then begin synthesis

Do **not** stop merely because an earlier unpublished chapter is already claimed. Skip occupied chapters and continue scanning upward until the earliest free written chapter is found.

## Written chapter inventory authority

For audio eligibility, the authoritative written inventory is the set of **actual numbered Greg, Again prose files** present on the current authoritative written ref under:

`state/experiments/greg-again/prose/`

Exact prose outranks compact summaries.

Therefore:

- enumerate the directory instead of trusting a cached numerical frontier
- a numbered chapter prose file that actually exists on the authoritative written ref counts as written and may enter the audio availability scan
- `state/experiments/greg-again/written/CURRENT.md` remains important story-state / next-writing context, but its headings or trailhead language do **not** undercount prose files that already exist
- if `CURRENT.md` still says `Frontier after Chapter N` while `N+1` or later numbered prose files already exist on the same authoritative written ref, the actual prose files win for audio inventory
- if a summary, rehearsal, chat handoff, branch name, or state note mentions a chapter but the actual numbered prose file is missing, that chapter is **not** audio-ready
- never reconstruct or synthesize a missing chapter from summaries merely to fill a number
- do not assume `main` itself contains the newest experimental prose when current GitHub routing identifies another written ref as authority

The written inventory may advance faster than a compact state summary is refreshed. That lag must not strand otherwise complete written chapters from audio production.

When current written-ref routing is genuinely ambiguous, resolve that ambiguity from GitHub authority before claiming. Do not guess between competing prose versions.

## Default claim size

The default auto-claim is **1 chapter per worker**.

One worker owns one audio chapter. This is the normal unit of parallel production.

A worker that has explicitly been assigned one different non-overlapping chapter may honor that assignment after checking current GitHub state.

Do not claim a second chapter merely because the current chapter has provider jobs queued, is waiting on artifact retrieval, or is blocked on downstream plumbing. More parallelism should normally come from another worker claiming another free chapter.

This keeps ownership narrow while still allowing roughly a dozen independent take jobs inside one chapter to run or queue aggressively.

## Protocol-native claim branches

New automatic claims use:

`audio/greg-again-chNNN-auto`

Examples:

- `audio/greg-again-ch012-auto`
- `audio/greg-again-ch013-auto`
- `audio/greg-again-ch014-auto`

Creating the branch is the claim operation.

A protocol-native worker must not begin voice synthesis until its claim branch exists.

If branch creation fails because the ref already exists, refresh GitHub state, mark that chapter unavailable, and scan upward for the next free written chapter. Never force-update or overwrite the existing claim.

## What counts as unavailable

A chapter is unavailable when any of the following is true:

- it is already published in the current `greg-again/audio/manifest.json`
- a live single-chapter audio branch clearly owns that chapter
- an open audio PR clearly owns that chapter
- a legacy batch branch contains durable chapter-specific production work for that chapter
- other current durable WIP makes chapter ownership clear

A chapter is **not** unavailable merely because an old multi-chapter branch name happens to include its number.

When ownership is genuinely ambiguous, avoid overlap and inspect the branch / PR / status evidence before synthesizing.

Never claim a chapter that lacks an actual numbered prose file on the current authoritative written ref.

## Availability scan

The scan is chapter-by-chapter across the actual written prose-file inventory, not frontier-contiguous and not summary-frontier-driven.

Conceptually:

```text
for chapter in actual numbered prose files on current authoritative written ref, low to high:
    if published:
        continue
    if durably claimed / active:
        continue
    claim this chapter
    stop
```

Therefore:

- Chapter 12 may be unfinished and actively owned
- Chapter 13 may still be free
- a fresh worker should claim Chapter 13 rather than reporting that it cannot proceed because Chapter 12 is unfinished

Holes are allowed during production. Publication may reconcile out-of-order worker completion safely through the shared-file rules below.

## Transitional compatibility with old batch claims

Earlier protocol versions used 3-chapter branches such as:

`audio/greg-again-batch-012-014`

Those historical branches remain durable WIP and must not be deleted, renamed, or force-updated just to normalize naming.

However, after adoption of the single-chapter protocol, **a legacy batch branch is no longer a blanket reservation for every number in its branch name**.

Evaluate each chapter inside that old range separately.

A chapter remains reserved by the legacy worker when current durable evidence shows chapter-specific work such as:

- a locked take map
- submitted provider jobs
- generated provider artifacts
- captured take binaries
- chapter-specific Audio Finish / production files
- a PR or STATUS file explicitly saying that chapter is actively in production

A chapter inside the old range is free for a new single-chapter worker when the only ownership evidence is the legacy range name and current durable state shows that chapter was not actually started.

If a legacy worker already has expensive provider work on more than one chapter, preserve that completed/generated work and let the worker finish those chapters. Do not throw away real synthesis merely to enforce prettier ownership history.

But a legacy worker should **not start new synthesis on an otherwise-unstarted sibling chapter merely because its old branch name covered the range**. That unstarted chapter belongs back in the free chapter scan.

Current GitHub evidence always outranks examples or stale chat memory.

## Pre-protocol per-chapter compatibility

Existing per-chapter branches such as:

`audio/greg-again-ch8-evidence-before-certainty`

remain valid exact-chapter claims while that work is live or unpublished.

Do not rename, restart, absorb, or regenerate those workers merely to normalize branch naming.

## No automatic stealing

A worker must never:

- delete another worker's active claim branch
- force-update another worker's active claim branch
- steal a chapter that has durable chapter-specific WIP
- assume apparently slow provider work is abandoned
- regenerate published chapters to normalize production history

The single-chapter transition releases only **unstarted sibling reservations from old multi-chapter envelopes**. It does not release real chapter-specific work.

An actually abandoned or mistaken single-chapter claim still requires explicit release or reassignment by the human or a clearly authorized integration worker.

## Working inside a claimed chapter

For the owned chapter:

1. resolve the current authoritative Shared Greg Surface / written source
2. apply current `r2/PIPELINE.md` Audio Finish doctrine
3. preserve current narrator / voice / pronunciation authority
4. split into provider-safe performance takes using the established short-take factory below
5. lock a deterministic take map
6. generate each take as its own voice job
7. cross the provider artifact boundary for every successful take
8. assemble the ordered durable take audio into one continuous chapter MP3
9. verify text coverage, take order, seams, playability, title, duration, and route
10. reconcile shared catalog / manifest files against newest GitHub authority
11. publish the verified chapter durably

Do not redesign settled audio philosophy during ordinary production.

## Established short-take voice factory

**Do not default to one giant chapter-long voice generation.**

The proven Greg, Again production method makes the chapter from multiple short provider-safe voice generations and then stitches those outputs into one final chapter MP3.

Published Chapters 1–7 used **11–14 takes per chapter**:

- Chapter 1: 11 takes
- Chapter 2: 12 takes
- Chapter 3: 12 takes
- Chapter 4: 12 takes
- Chapter 5: 14 takes
- Chapter 6: 13 takes
- Chapter 7: 14 takes

Therefore a normal roughly 12–15 minute Greg, Again chapter should usually be expected to require **about a dozen separate voice-generation jobs**, not one long generation. The exact count follows the chapter. Do not force 12 when 11 or 14 creates cleaner provider-safe boundaries.

### Voice generation

Use the current repository renderer / available AI voice-generation tool. When the tool exposes the established voice choice, use:

`deep`

Treat **one take as one voice-generation request**.

For each take:

1. lock the exact spoken transcript for that take
2. submit only that intended spoken material to the voice renderer
3. use the same established `deep` narrator across the chapter
4. record the returned provider artifact identity immediately
5. associate it deterministically with chapter + take number
6. cross the provider artifact boundary before considering the take production-complete
7. do not silently paraphrase the text because a provider call is inconvenient

### Final-take landing

The final take should inherit the authoritative written chapter ending, including the R2 default terminal `...`. Do not create a separate hidden punctuation version merely for the voice provider when the written surface already carries the landing cue.

The purpose is performance: the last spoken thought should settle downward and sound complete rather than rising like a question or sounding as though another sentence is about to follow. If the renderer still gives the authoritative final line a continuation-like cadence, repair or regenerate only the smallest final take that owns that ending. Preserve all acceptable earlier takes.

The written ellipsis and the assembled chapter-tail silence solve different problems. The ellipsis shapes delivery; the roughly 2-second assembly tail gives the listener room after the final spoken word. Keep both rules.

### Pronunciation authority

Written spelling remains authoritative for Read. Provider-facing pronunciation substitutions may be used when needed without changing the displayed prose. `r2/AUDIO_PRONUNCIATION.md` is the durable provider-facing pronunciation authority and instability watchlist. Read it before synthesis and repair work. In particular:

- written `mana` stays `mana`
- provider-facing `mana` should default to `ma-na` / `Ma-na` to preserve the approved Hawaiian-context pronunciation without causing the `deep` voice to audibly pronounce a synthetic H

Record such pronunciation substitutions in production evidence when they differ from the written spelling. Do not flow phonetic provider spellings back into the written chapter unless the prose itself is separately edited.

A useful deterministic naming shape is:

- `ga-012-take-01`
- `ga-012-take-02`
- ...
- `ga-012-take-12`

Follow existing repository file conventions when a current chapter already establishes a more specific path/name.

## Provider artifact boundary

**Provider playback is not durable completion.**

A voice job may succeed at synthesis while downstream binary handoff still fails. Treat these as separate stages:

**LOCKED TAKE → PROVIDER GENERATION → PROVIDER ARTIFACT CAPTURE → DURABLE TAKE → ASSEMBLY → VERIFICATION → PUBLICATION**

A take is production-complete only when at least one of the following exists:

- the actual audio binary is durably available for downstream assembly, or
- a proven durable provider artifact reference exists that can retrieve the already-generated binary later without regenerating the take.

A playable provider page, inline player, temporary client state, blob URL, preview widget, or successful synthesis response by itself does **not** prove that the take has crossed the durable boundary.

### Preserve successful synthesis

If synthesis succeeded but binary extraction, download, transfer, or assembly fails afterward:

- **do not regenerate the take merely to solve plumbing**
- preserve the exact take transcript
- preserve chapter + take identity
- preserve every returned provider artifact ID / URL / filename / resource reference available
- preserve provider-side recovery state when it is the only path to the already-generated audio
- keep the chapter claim
- solve artifact retrieval before paying a regeneration tax

Provider-page archives, client-state archives, exported provider bundles, or similar recovery capsules may be retained when they are the only durable evidence capable of recovering already-generated audio. They are recovery artifacts, not the preferred final production format.

Once the real audio binary has crossed the boundary and is safely associated with the take, prefer the normal durable take file and take map over provider-page archives.

### Never throw away expensive nondeterministic work for a cheap deterministic failure

Voice synthesis is the scarce / nondeterministic stage. File extraction, naming, stitching, manifest reconciliation, and publication are downstream deterministic work.

When the provider already produced an acceptable take, preserve it aggressively. Do not spend synthesis quota again because a downstream worker cannot immediately access the binary.

Only regenerate when the **audio itself** is bad or unusable, such as bad pronunciation, cadence, truncation, corruption, or an incorrect locked transcript.

## Take map

Before or during generation, preserve an ordered take map containing at minimum:

- chapter number / ID
- take number
- exact transcript or exact source boundaries
- first-word / last-word anchors when useful
- provider job / artifact identity once generated
- durable audio filename or durable retrievable artifact reference once captured
- status such as `locked`, `submitted`, `generated`, `artifact_captured`, `verified`, or `repair_needed`
- any local repair / recovery note

The take map exists so assembly can prove that every spoken segment appears once and in the correct order, and so a later worker can resume without regenerating completed provider work.

## Choosing take boundaries

Take boundaries are **production seams, not story edits**.

Prefer natural boundaries around:

- paragraph / thought movement
- scene movement
- speaker transition
- action transition
- realization
- interruption
- a natural pause that will survive stitching

If a section is too dense or too large for reliable provider generation, split it again without changing story state or meaning. Chapters 6 and 7 already established this precedent with extra provider-safe splits.

Do not shorten Greg's processing space merely to fit a larger chunk.

## Queue the voice jobs

Once take transcripts are locked, the takes are independent provider jobs.

**Submit multiple takes without unnecessarily waiting for each previous take to finish** when the tool/provider permits queued or parallel requests.

For a 12-take chapter, desired behavior is conceptually:

```text
submit take 01
submit take 02
submit take 03
...
submit take 12
collect completed outputs
capture durable artifacts
assemble in take order
```

not:

```text
submit take 01
wait for full downstream assembly work
submit take 02
wait again
...
```

Provider-side serialization or throttling is acceptable. The worker's job is to avoid creating artificial serial waiting when independent jobs can already be queued.

The default strategy is now:

**one-chapter ownership + high internal take concurrency + many parallel workers**

If the available account/tool quota stops further generations, preserve the take map, generated provider artifacts, and captured binaries exactly. Do not surrender or duplicate the chapter claim merely because synthesis quota is temporarily exhausted.

## Assembly

The final listener-facing chapter is **one continuous MP3 assembled from the take outputs**.

Assembly must:

1. order takes numerically
2. include every take exactly once
3. preserve intentional end/start silence when it carries useful processing space
4. end the final listener-facing chapter with about **2.0 seconds of trailing silence after the final spoken word**; an existing natural tail of roughly **1.5–2.5 seconds** is acceptable and does not need normalization
5. apply chapter-tail silence at final chapter assembly only, not by adding extra silence to every take or internal seam
6. avoid accidental duplicated phrases at seams
7. avoid accidental missing phrases at seams
8. avoid adding decorative sound design, music, crossfades, or performance effects unless separately authorized
9. produce the established chapter audio artifact path used by the Greg, Again manifest/catalog

The chapter-tail rule is a **forward-production finishing default**. Do not retroactively regenerate, restitch, or republish already-published chapters solely to normalize their trailing silence. Repair an older chapter only when its listener-facing ending is actually abrupt or a separate audio repair is authorized.

Do not publish the individual provider takes as if they were the audiobook chapter. They are production components.

A separate finisher or integration worker may assemble already-captured takes when ownership and artifact identity are unambiguous. It must not alter story text, steal chapter ownership, or regenerate acceptable provider work merely because it did not create the original takes.

## Repair behavior

If one take has bad pronunciation, cadence, truncation, corruption, or another local synthesis failure, regenerate **that take**, not the whole chapter.

Only widen the repair when the problem crosses a seam or originates in the locked Audio Finish text.

If the failure is only provider-artifact handoff, binary extraction, filename transfer, stitching, or publication plumbing, recover the existing generated take instead of regenerating it.

This replaceable-take property is a major reason the current short-take factory is preserved even though longer paid voice generations may exist.

## Final production record

Before publication, record the actual `take_count` and final chapter duration in the same durable surfaces used by previous chapters.

Do not claim a chapter was produced as a single render when it was assembled from short takes.

## Provider queueing across workers

Voice-generation jobs are independent production work when their transcripts are already locked.

Multiple workers may operate simultaneously when each owns a distinct chapter. Each worker may aggressively queue its own chapter's takes, provided:

- exact transcript-to-take mapping is preserved
- chapter ownership is already claimed
- provider quota / rate limits are respected
- no wording is changed merely to make queueing easier
- generated output remains traceable deterministically to chapter and take
- another worker's claimed chapter is never submitted or regenerated

Provider throttling, serialization, quota exhaustion, or artifact-handoff trouble does not release chapter ownership.

The current short-take / stitched workflow remains valid. Do not pay a regeneration tax merely to make older chapters match a newer provider convenience.

## Producer / finisher separation

R2 may separate expensive synthesis work from cheap deterministic downstream work when that increases throughput.

A **producer** may lock takes, submit voice jobs, and capture durable artifacts for one claimed chapter.

A **finisher** may consume already-captured artifacts to stitch, verify, reconcile manifests, and publish that same chapter.

This is an allowed execution topology, not a requirement to create permanent new worker roles. Keep it simple when one worker can finish its own chapter cleanly.

When separating roles:

- chapter ownership remains authoritative
- the take map is the handoff contract
- producers must leave durable artifact identities
- finishers must preserve exact take order and transcript coverage
- finishers must not regenerate acceptable takes without a real synthesis defect
- shared publication files must still be reconciled against newest `main`

## Shared-file reconciliation

Parallel workers may all eventually need shared files such as:

- `greg-again/audio/manifest.json`
- R2 audio/catalog routing
- reader chapter audio metadata

Immediately before modifying a shared file:

1. refresh current `main`
2. inspect newer neighboring audio merges
3. preserve every valid newer entry
4. add or change only the current worker's owned chapter

Never restore a stale whole-file copy over newer audio publication.

A worker may merge current `main` into its branch or otherwise reconcile according to repository workflow before publication.

Out-of-order production is acceptable. Shared publication state must preserve already-landed neighboring chapters rather than assuming completion order is contiguous.

## Verification

For every published chapter verify at minimum:

- source text is fully represented with no accidental omission
- no source segment is duplicated at take seams
- take order is correct
- every assembled take crossed the durable provider artifact boundary
- audio is playable
- pronunciation authority is preserved
- chapter number and title match current reader/catalog authority
- duration metadata is recorded when required
- manifest/catalog entries point to the correct artifact
- neighboring workers' chapters were not overwritten
- the final take preserves the authoritative chapter-ending punctuation and lands as a completed, downward final thought rather than an accidental question / continuation
- approved pronunciation substitutions such as written `mana` -> provider `mah-nah` are preserved where relevant
- for chapters produced after adoption of the chapter-tail rule, the final listener-facing file has about **2.0 seconds of silence after the final spoken word**; roughly **1.5–2.5 seconds** is acceptable

When one local take fails, prefer repairing the smallest responsible take rather than regenerating the whole chapter.

## Completion authority

Published entries in `greg-again/audio/manifest.json` are the durable proof that listener-facing audio chapters are complete.

A successful provider render alone is **not** chapter completion.

A historical claim branch may remain after merge. Its existence does not make an already-published chapter unfinished.

For any unpublished chapter with durable chapter-specific WIP, preserve that ownership until explicit release or completion.

## Handoff

At the end of a chapter, report compactly:

- claimed chapter
- completed / published state
- actual take count
- provider jobs completed / outstanding
- generated takes whose binaries are not yet durably captured
- recovery artifacts or durable provider references that must be preserved
- provider quota / throttling issue, if any
- branch / PR / merge state
- next free chapter only if current GitHub state makes it clear

Then leave the normal repository handshake.

## Minimal fresh-chat starter

> Continue Greg, Again audio production from current GitHub authority.
>
> Auto-claim the next available free audio chapter using `r2/AUDIO_PRODUCTION.md`. Derive the written inventory from the actual numbered Greg, Again prose files on the current authoritative written ref, then produce the earliest free written/unpublished chapter with the established short-take voice factory, capture durable take artifacts, verify, publish, and leave the next handshake.
>
> Preserve newer authority, preserve already-generated provider work, skip chapters already durably owned by another worker, and do not overlap.

A fresh worker should derive its actual chapter from GitHub rather than asking the human to assign it.