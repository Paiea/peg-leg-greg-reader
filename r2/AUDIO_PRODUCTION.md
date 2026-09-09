# Greg, Again — Audio Production Protocol

This file owns parallel audio-production coordination for R2 / Greg, Again.

It does **not** replace `r2/PIPELINE.md`. The pipeline owns Shared Greg Surface, Audio Finish, processing space, POV, and medium-specific repair. This file owns worker routing, claiming, provider submission, artifact capture, assembly, verification, publication, and handoff.

Current GitHub authority outranks chat history and stale handoff text.

## Default worker behavior

A fresh audio worker should not ask the human which chapters it owns unless GitHub state is genuinely ambiguous.

If the human did not explicitly assign a range, the worker must:

1. inspect current `main`
2. read root `AGENTS.md`
3. read `r2/PIPELINE.md`
4. read this file
5. inspect `greg-again/audio/manifest.json`
6. inspect current Greg, Again written authority / written frontier
7. inspect live Greg, Again audio branches and open PRs
8. compute the earliest available contiguous batch
9. create the claim branch
10. verify the claim still does not overlap newer work
11. only then begin synthesis

## Default batch size

The default auto-claimed batch is **3 chapters**.

A worker may claim a smaller tail batch when fewer than 3 written chapters are available before the written frontier.

Do not skip an earlier free chapter merely to create prettier multiples of three.

A worker that has explicitly been assigned a different non-overlapping range may honor that assignment after checking current GitHub state.

The 3-chapter batch is an **ownership envelope**, not a provider-concurrency limit. Keep ownership small and legible while allowing many independent take jobs inside that envelope to run or queue concurrently.

## Protocol-native claim branches

New automatic claims use:

`audio/greg-again-batch-NNN-MMM`

Examples:

- `audio/greg-again-batch-012-014`
- `audio/greg-again-batch-015-017`
- `audio/greg-again-batch-018-020`

Creating the branch is the claim operation.

A protocol-native worker must not begin voice synthesis until its claim branch exists.

If branch creation fails because the ref already exists, refresh GitHub state and compute the next available batch. Never force-update or overwrite the existing claim.

## What counts as unavailable

A chapter is unavailable when any of the following is true:

- it is already published in the current `greg-again/audio/manifest.json`
- it is covered by an existing protocol-native batch claim whose unpublished chapters have not been explicitly released
- a live pre-protocol Greg, Again audio branch clearly owns that chapter
- an open Greg, Again audio PR clearly owns that chapter
- other current durable WIP makes ownership clear

When ownership is genuinely ambiguous, avoid overlap rather than maximizing batch size.

Never claim beyond the current authoritative written frontier.

## Transitional compatibility

Audio workers already running before this protocol remain valid.

Existing per-chapter branches such as:

`audio/greg-again-ch8-evidence-before-certainty`

reserve their exact chapter while that work remains live or unpublished.

Do not rename, restart, absorb, or regenerate those workers merely to normalize branch naming.

At protocol adoption time, Chapters 8–11 already had separate live ownership signals. New workers should respect whatever the newest GitHub state shows rather than assuming those exact chapters remain current forever.

## No automatic stealing

A worker must never:

- delete another worker's claim branch
- force-update another worker's claim branch
- assume an apparently idle branch is abandoned
- steal work because a PR is slow
- regenerate published chapters to normalize production history

An abandoned or mistaken claim requires explicit release or reassignment by the human or a clearly authorized integration worker.

## Working inside a claimed batch

The claim defines ownership, not a requirement to finish all chapters in one giant transaction.

Within a claimed batch, produce and verify chapters sequentially enough that each completed chapter can cross a durable publication boundary. A worker may prepare later chapters while provider jobs for an earlier chapter are processing, but it must not let partial preparation overwrite newer story or audio authority.

For every owned chapter:

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

Do not redesign settled audio philosophy merely because a worker owns several chapters.

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

### Queue across owned chapters

The same rule applies across already-claimed chapters. Once exact transcripts are locked, a worker may queue takes from Chapters N, N+1, and N+2 without waiting for the previous chapter to finish assembly.

This means a 3-chapter worker may legitimately have roughly 30–40 independent provider jobs in flight or queued while still owning only three chapters.

The default strategy is therefore:

**small ownership envelope + high internal take concurrency**

Do not increase chapter claim size merely to increase provider throughput.

If the available account/tool quota stops further generations, preserve the take map, generated provider artifacts, and captured binaries exactly. Do not surrender or duplicate the chapter claim merely because synthesis quota is temporarily exhausted.

## Assembly

The final listener-facing chapter is **one continuous MP3 assembled from the take outputs**.

Assembly must:

1. order takes numerically
2. include every take exactly once
3. preserve intentional end/start silence when it carries useful processing space
4. avoid accidental duplicated phrases at seams
5. avoid accidental missing phrases at seams
6. avoid adding decorative sound design, music, crossfades, or performance effects unless separately authorized
7. produce the established chapter audio artifact path used by the Greg, Again manifest/catalog

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

## Provider queueing across chapters and workers

Voice-generation jobs are independent production work when their transcripts are already locked.

Multiple workers may operate simultaneously when each owns a distinct claimed chapter range. Each worker may aggressively queue its own takes, provided:

- exact transcript-to-take mapping is preserved
- chapter ownership is already claimed
- provider quota / rate limits are respected
- no wording is changed merely to make queueing easier
- generated output remains traceable deterministically to chapter and take
- another worker's claimed chapters are never submitted or regenerated

Provider throttling, serialization, quota exhaustion, or artifact-handoff trouble does not release chapter ownership.

The current short-take / stitched workflow remains valid. Do not pay a regeneration tax merely to make older chapters match a newer provider convenience.

## Producer / finisher separation

R2 may separate expensive synthesis work from cheap deterministic downstream work when that increases throughput.

A **producer** may lock takes, submit voice jobs, and capture durable artifacts.

A **finisher** may consume already-captured artifacts to stitch, verify, reconcile manifests, and publish.

This is an allowed execution topology, not a requirement to create permanent new worker roles. Keep it simple when one worker can finish its own batch cleanly.

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
4. add or change only the current worker's owned chapters

Never restore a stale whole-file copy over newer audio publication.

A worker may merge current `main` into its branch or otherwise reconcile according to repository workflow before publication.

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

When one local take fails, prefer repairing the smallest responsible take rather than regenerating the whole chapter.

## Completion authority

Published entries in `greg-again/audio/manifest.json` are the durable proof that listener-facing audio chapters are complete.

A successful provider render alone is **not** chapter completion.

A historical claim branch may remain after merge. Its existence does not make already-published chapters unfinished.

For any unpublished chapter still covered by an unreleased claim, preserve that ownership until explicit release or completion.

## Handoff

At the end of a batch, report compactly:

- claimed range
- completed / published chapters
- actual take count per completed chapter
- any chapter still in progress
- provider jobs completed / outstanding
- generated takes whose binaries are not yet durably captured
- recovery artifacts or durable provider references that must be preserved
- provider quota / throttling issue, if any
- branch / PR / merge state
- next available range only if current GitHub state makes it clear

Then leave the normal repository handshake.

## Minimal fresh-chat starter

> Continue Greg, Again audio production from current GitHub authority.
>
> Auto-claim the next available audio batch using `r2/AUDIO_PRODUCTION.md`, then produce, capture durable take artifacts, verify, publish, and leave the next handshake.
>
> Preserve newer authority, preserve already-generated provider work, and do not overlap another worker.

A fresh worker should derive its actual chapter range from GitHub rather than asking the human to assign it.
