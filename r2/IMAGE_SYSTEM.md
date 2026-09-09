# R2 IMAGE SYSTEM

R2 has its own visual-production authority.

This file governs Run 2 image work. It may reuse process lessons from Run 1 and the shared Image OS, but **Run 1 visual canon does not automatically apply to R2**.

## Core principle

> Build durable visual understanding once. Reuse it. Change only what the current image requires.

The goal is not to generate attractive one-off pictures. The goal is to produce story-useful images that remain coherent across chapters, survive chat loss, and can be integrated safely.

## Worker execution model

Routine R2 chapter-image production uses **disposable single-transaction workers**.

> ONE FRESH WORKER = ONE CLAIM = ONE CHAPTER IMAGE TRANSACTION = STOP.

A normal chapter worker:

1. fresh-reads current GitHub authority
2. inspects open image PRs / active image branches for ownership
3. claims one eligible unclaimed chapter with a draft PR or equivalent durable branch signal before generating
4. reads the actual current chapter source, not just chapter metadata
5. resolves roughly five visually distinct source moments from that chapter
6. retrieves the relevant visual canon, continuity references, and task-relevant story brains
7. generates up to five scene-specific images, normally one per resolved moment
8. reviews and stages approved outputs
9. leaves durable GitHub state / handshake for the next worker
10. stops after that transaction instead of claiming another chapter in the same chat

Do not optimize for keeping a worker alive. Optimize for making the next fresh worker cheap to start from authority.

### Claim rule

The PR / branch is the claim lock. Do not create a shared mutable claim file merely to coordinate parallel workers.

Before claiming, inspect current open PRs and active `image/r2-*` branches. If another worker owns a chapter, skip it and claim the next eligible chapter. Preserve newer authority and reconcile with current `main` before publication/integration.

### Bootstrap exception

Foundational visual-canon work may use a bounded non-chapter transaction when later workers depend on it, such as the first Greg face/body/style/Carrow anchors in `image-packets/PACKET_001.md`.

Finish that seed deliberately. Do not let every chapter worker independently invent a new Greg or Carrow.

## Hard source-grounding rule

> STORY SOURCE FIRST. TITLE LAST.

Chapter titles, role labels, manifest summaries, and chapter-browser metadata are **not sufficient image source material**.

A chapter worker must not generate from a title such as `The Contractor`, `The Fighter`, `The Investor`, or any equivalent role label as though the title were a visual brief.

For routine chapter art, source priority is:

1. exact current R2 chapter/story source for the claimed chapter
2. scene truth and physical action resolved from that source
3. current R2 visual canon
4. approved R2 continuity references
5. task-relevant character/setting/story brains that remain compatible with current R2 authority
6. chapter manifest and title as weak metadata only

If the exact chapter source cannot be found, is stale, or does not provide enough evidence to resolve a real scene, do not improvise a generic fantasy composition. Record the authority gap and stop or escalate.

### Whole-chapter read requirement

Before choosing images, read enough of the actual chapter to understand its full movement, not merely the opening paragraph or title.

Then identify about five visually distinct moments that are genuinely present in the source.

Prefer moments with:

- physical action or work
- a relationship beat with visible behavior
- a meaningful object or material consequence
- a distinctive location or environmental use
- a state change, realization, arrival, departure, failure, repair, exchange, threat, or other imageable turn

Avoid five near-duplicate portraits, five generic conversation poses, or five visualizations of the chapter title.

If the chapter genuinely contains fewer than five strong moments, use fewer. The target creates useful production volume, not filler.

## Model routing

Routine chapter-image transactions are intentionally narrow enough to **default to Instant** when available.

Instant is acceptable only when the worker actually performs the source-grounding and retrieval steps above. Skipping the source to save context is a production failure, not an optimization.

Escalate to a higher-thinking worker when the job materially depends on judgment that should become durable visual authority, including:

- establishing or replacing a canon identity/style/location anchor
- a new recurring character or location with no trustworthy visual reference
- conflicting visual/story authority
- ambiguous scene selection where the image itself could change interpretation
- repeated identity/style/world drift after a normal retry
- inability to resolve strong source-grounded scene choices without invention
- a major cover/frontdoor image
- image-system, release-system, or integration architecture changes

Do not escalate routine support art merely because a stronger model exists. Spend higher-thinking effort where the project compounds from the decision.

## Authority order

For R2 visual work:

1. current R2 Story Truth / exact scene evidence
2. current R2 visual canon state in `visual-state/R2_VISUAL_CANON.md`
3. approved R2 continuity references
4. current image packet
5. task-relevant R2-compatible story brains
6. shared Image OS process guidance
7. Run 1 visual material as optional evidence only

When Run 1 and R2 conflict, R2 wins.

### Early Greg leg-state rule

Run 1's visual bible contains later-story disability continuity. **Do not inherit it into early R2.**

Until current R2 story authority explicitly establishes Greg's leg loss:

- Greg has both legs intact
- do not show a peg leg, prosthetic, amputation, or crutches as canon
- do not imply the future event merely because the project title is `Peg-Leg Greg`
- when lower-body state is not the point, prefer framing that keeps it visually unimportant

## R2 visual north star

**SKETCH + INK + PAINT, WITH VISIBLE HUMAN ROUGHNESS**

Desired qualities:

- illustrated-novel energy
- visible pencil/ink structure
- painterly wash rather than plastic rendering
- imperfect edges and construction texture
- restrained, dirty palette
- asymmetry and lived-in materials
- expressive faces that do not look cosmetically polished
- strong scene-specific composition
- enough roughness to feel authored, not enough to become muddy

Avoid:

- generic glossy AI-fantasy finish
- hyper-clean cinematic concept art as the default
- cheerful heroic-poster Greg
- anonymous fantasy-city backgrounds
- overdesigned costumes and props unsupported by the story
- attractive outputs that silently invent new visual canon
- chapter-title poster compositions disconnected from actual scenes

## Greg direction

Early R2 Greg is nineteen.

He should read:

- clearly young
- lean / underfed rather than middle-aged or bodybuilder-heavy
- rough, practical, and hard-lived
- intelligent and watchful
- intense, self-possessed, calculating
- capable of amused menace or predatory calm
- morally compromised rather than cleanly heroic

He should not default to:

- warm friendliness
- clean heroism
- glamorous fantasy-protagonist beauty
- exaggerated villain theatrics

The useful emotional target is **controlled danger**: someone easy to underestimate until his attention lands on something.

## Carrow direction

Carrow should feel like a lived-in working city, not a generic scenic fantasy backdrop.

Prefer:

- narrow streets and alleys
- stone, timber, plaster, mud, wet cobble, grime
- signs of trade, labor, hauling, repairs, cheap rooms, carts, shops, guild traffic
- layered vertical architecture
- imperfect practical lighting
- ordinary people using the city rather than posing inside it

Do not make Carrow a harbor by default. Water, docks, and port imagery belong only where current story evidence supports them.

## Visual canon pack

Before scaling chapter generation, maintain a compact anchor set:

1. Greg face / expression anchor
2. Greg body / posture anchor
3. Greg mood anchor
4. Carrow environment anchor
5. R2 style anchor

Not every anchor must be public. These assets exist to reduce rediscovery and drift.

Approval is granular. A useful image may be promoted as:

- face reference
- body/posture reference
- clothing reference
- expression/mood reference
- location reference
- style reference
- composition reference only
- site mood only
- full continuity reference

A beautiful image does not become full canon automatically.

## Image roles

Every planned image gets one primary role:

- `cover_frontdoor`: homepage / section identity
- `anchor`: main chapter illustration
- `support`: secondary story beat
- `texture`: object / place / atmospheric detail
- `continuity`: internal reference that may never publish

## Chapter production vs publishing

Routine production target:

- read one full claimed chapter
- choose about five source-grounded scene moments
- generate up to five images, normally one per moment

Publication remains a **value decision, not a quota**.

The final chapter may publish:

- zero images
- one strong anchor
- several distinct supporting images when they genuinely add value

Generating five candidates does not require publishing five. The worker batch exists to create selection and useful Library accumulation without lowering the bar for the reader.

## Minimal image packet

Before generation, each image job must resolve:

- `image_id`
- `chapter_id`
- `source_file`
- `source_excerpt`
- `scene_id`
- `scene_truth`
- `role`
- `priority`
- `image_reason`
- `purpose`
- `must_show`
- `must_not_show`
- `continuity_dependencies`
- `hard_references`
- `soft_references`
- `allowed_invention`
- `style_lane`
- `publish_intent`
- `destination_path`
- `status`
- `notes`

Use `image-packets/TEMPLATE.md`.

## GPT Library staging

GitHub owns story authority, claims, packets, manifests, and integration state. **ChatGPT Library is the shared binary staging warehouse** for parallel image workers.

R2 uses the existing Library project shelf:

```text
/Peg-Leg Greg Image Integration/R2/
  00 Canon/
  01 Incoming/
  02 Approved/
  03 Releases/
  04 Released/
```

Meaning:

- `00 Canon/`: promoted continuity/reference binaries that future workers may retrieve
- `01 Incoming/`: generated keepers awaiting final approval or routing
- `02 Approved/`: approved, release-ready binaries not yet included in a large handoff release
- `03 Releases/`: packaged release ZIPs and release manifests
- `04 Released/`: approved source binaries already included in a release, retained so they are not accidentally packaged twice

Use deterministic filenames. Chapter workers may create chapter subfolders such as `01 Incoming/ch012/` or `02 Approved/ch012/` when useful.

Library files do **not** outrank R2 story or visual canon merely because they exist there.

### Generator-to-Library gate

When a generated output is exposed as a usable file reference, route it directly to the correct R2 Library shelf.

If the generation surface does not expose safe bytes / a file reference that Library can store, do not pretend the image is staged. Mark the transaction `library_stage_pending` and preserve the approved output for the narrowest manual deposit possible.

The worker's success criterion is durable staging, not a conversational claim that an image exists.

## Production loop

Default chapter-worker loop:

**FRESH READ → CLAIM → READ CHAPTER → SELECT ~5 SCENES → RETRIEVE BRAINS/REFERENCES → GENERATE → REVIEW → STAGE → RECORD → STOP**

Later release/integration loop:

**COLLECT APPROVED → PACKAGE RELEASE → MANUAL REPO DROP → VERIFY → INTEGRATE**

### PLAN

A normal chapter worker owns one chapter and resolves about five distinct source moments before generation.

Each selected scene must earn its own image. Do not widen into the next chapter merely because generation is cheap.

### RETRIEVE

Use the smallest useful reference neighborhood for each selected scene.

Reference hierarchy:

1. exact chapter scene evidence
2. identity/face anchor when identity matters
3. body/clothing anchor when needed
4. location/object authority when needed
5. task-relevant character/setting/story brain evidence
6. style/mood support

Do not dump every available reference into every generation.

### GENERATE

If an image depends on continuity that does not exist yet, stop the routine chapter transaction and route the missing continuity problem as a higher-judgment visual-canon task.

Generate against the selected scene, not the chapter title. The source scene should determine subject, action, environment, and composition.

Batch multiple images inside the claimed chapter when they share authority and add distinct value. Do not batch unrelated chapters in one worker.

### REVIEW

Every result becomes one of:

- `approved`
- `revise`
- `rejected`

Useful compact failure tags:

- `identity_drift`
- `wrong_age`
- `wrong_leg_state`
- `style_drift`
- `world_drift`
- `tone_mismatch`
- `continuity_break`
- `composition_issue`
- `scene_mismatch`
- `anatomy_issue`
- `too_ai_generic`
- `too_title_literal`
- `insufficient_scene_specificity`
- `not_grounded_in_source`
- `unwanted_text`
- `binary_corruption`

Failure tags exist to improve the next attempt, not to create paperwork.

### PROMOTE USEFUL EVIDENCE

Approved images may teach future work. Promote only the useful part.

Example: a scene may have an excellent Greg face but an invented costume. Promote the face reference, not the costume.

Promoted binaries belong in the Library `00 Canon/` shelf and must be reflected in durable R2 visual-canon state before future workers treat them as authority.

### STAGE / HANDOFF

Normal chapter workers do **not** need to create a tiny ZIP for Keoni after every transaction.

Instead:

- generated candidates go to `01 Incoming/` when safe bytes are available
- approved release-ready keepers go to `02 Approved/`
- record the intended repository path in the packet/claim state
- stop the worker after the chapter transaction

Large handoff packaging is a separate release-worker job governed by `IMAGE_RELEASES.md`.

Generated image binaries still follow `../state/IMAGE_BINARY_HANDOFF.md`: GitHub binary transport is not trusted merely because a write succeeds.

### RELEASE

A separate packager worker periodically gathers approved unreleased Library assets, normally when Keoni asks or when roughly 50 to 100 useful images have accumulated.

The packager creates one repo-mirrored release ZIP, stores it under `03 Releases/`, records membership, then moves included source binaries to `04 Released/` so the Library itself remains an obvious unreleased queue.

See `IMAGE_RELEASES.md`.

### VERIFY

After Keoni performs the large manual repository drop:

- file exists at exact destination
- binary decodes
- pixels match approved output
- dimensions/aspect ratio are plausible
- no stale bad asset remains referenced

### INTEGRATE

Only approved + repository-verified chapter art enters `data/chapters/chNNN.json`.

Preferred chapter-art path:

```text
r2/assets/images/chapters/chNNN/
```

Suggested stable filenames:

```text
r2-ch001-img01.webp
r2-ch001-img02.webp
```

Site/frontdoor art remains under:

```text
r2/assets/images/site/
```

## Resume-first state

A fresh chapter worker should be able to reconstruct its whole job from GitHub plus the R2 Library shelves. It should not need old chat history.

Durable state should make it possible to answer:

- which chapters are already claimed
- what continuity references are approved
- what this worker's one chapter transaction owns
- what exact source chapter was read
- which roughly five scenes were selected and why
- what images are planned/generated/approved
- which binaries are staged in Library and where
- which approved binaries are still unreleased
- what has already been released
- what has been repository-verified and integrated
- what the next fresh worker should claim

Do not make a fresh worker reconstruct those answers from chat.
