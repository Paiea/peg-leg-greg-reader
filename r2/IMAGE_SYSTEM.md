# R2 IMAGE SYSTEM

R2 has its own visual-production authority.

This file governs Run 2 image work. It may reuse process lessons from Run 1 and the shared Image OS, but **Run 1 visual canon does not automatically apply to R2**.

## Core principle

> Build durable visual understanding once. Reuse it. Change only what the current image requires.

The goal is not to generate attractive one-off pictures. The goal is to produce story-useful images that remain coherent across chapters, survive chat loss, and can be integrated safely.

## Authority order

For R2 visual work:

1. current R2 Story Truth / exact scene evidence
2. current R2 visual canon state in `visual-state/R2_VISUAL_CANON.md`
3. approved R2 continuity references
4. current image packet
5. shared Image OS process guidance
6. Run 1 visual material as optional evidence only

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

- `cover_frontdoor` — homepage / section identity
- `anchor` — main chapter illustration
- `support` — secondary story beat
- `texture` — object / place / atmospheric detail
- `continuity` — internal reference that may never publish

## Chapter publishing rule

Image count is a **value decision, not a quota**.

Normal chapter policy:

- 0–1 anchor image
- 0–2 support/texture images
- publish only images that add distinct value

Some chapters should have no art. One strong image is better than three filler images. Do not turn the reader into an AI scrapbook merely to hit coverage numbers.

## Minimal image packet

Before generation, each image job must resolve:

- `image_id`
- `chapter_id`
- `scene_id`
- `role`
- `priority`
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

## Production loop

Default loop:

**PLAN → RETRIEVE → GENERATE → REVIEW → PROMOTE USEFUL EVIDENCE → HANDOFF → VERIFY → INTEGRATE**

### PLAN

Work in bounded packets, usually 3–5 images.

Prioritize jobs that create leverage:

1. missing continuity anchors
2. high-value chapter anchor art
3. support art that adds a distinct visual beat
4. replacements only when materially better

### RETRIEVE

Use the smallest useful reference neighborhood.

Reference hierarchy:

1. identity/face anchor when identity matters
2. body/clothing anchor when needed
3. location/object authority when needed
4. style/mood support

Do not dump every available reference into every generation.

### GENERATE

If an image depends on continuity that does not exist yet, generate the continuity anchor first.

Batch generation is encouraged when the jobs can share authority without flattening composition. Do not batch unrelated scenes simply for throughput.

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
- `unwanted_text`
- `binary_corruption`

Failure tags exist to improve the next attempt, not to create paperwork.

### PROMOTE USEFUL EVIDENCE

Approved images may teach future work. Promote only the useful part.

Example: a scene may have an excellent Greg face but an invented costume. Promote the face reference, not the costume.

### HANDOFF

Generated image binaries follow `../state/IMAGE_BINARY_HANDOFF.md`.

When direct binary transport is unreliable:

- AI owns planning, generation, review support, filenames, destination paths, manifests, code, and verification
- Keoni performs the final approved binary drop
- AI verifies the actual repository file before integration

Prefer clean ZIP handoffs for approved batches when safe bytes are available.

### VERIFY

Before manifest integration:

- file exists at exact destination
- binary decodes
- pixels match approved output
- dimensions/aspect ratio are plausible
- no stale bad asset remains referenced

### INTEGRATE

Only approved + verified chapter art enters `data/chapters/chNNN.json`.

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

The current packet should make it possible for a fresh worker to answer:

- what is planned
- what is generated
- what awaits review
- what is approved
- what awaits handoff
- what has been uploaded but not verified
- what is integrated
- which approved outputs became continuity anchors
- what should happen next

Do not make a fresh worker reconstruct those answers from chat.
