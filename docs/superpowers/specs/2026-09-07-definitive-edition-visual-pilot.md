# Peg-Leg Greg Definitive Edition Visual Pilot

## Status

Approved bounded implementation baseline for the first Definitive Edition image-generation experiment.

Source authority at pilot start: `main` commit `292fe976b8444d9e024305e3523c2886c89ed966`.

## Authority

- Canon prose remains the only story authority.
- PERFORMANCE, dramatic reconstruction, screenplay, visual scene state, shot selection, prompt packs, and image metadata are derived editorial evidence only.
- Existing visual assets are evidence and publication state, not story authority.
- The structural production hold remains active globally.
- This pilot does not authorize broad image generation or broad illustration promotion.

## Goal

Prove that the existing PLG image pipeline can selectively use richer scene evidence without rebuilding the reader or disabling safety around manuscript drift.

The first batch intentionally compares two evidence conditions:

- Chapters 005 x2: prose-led visual selection without a durable PERFORMANCE round-trip archive.
- Chapters 007, 013, and 018: prose plus fresh scene-local PERFORMANCE reference evidence when anchor validation succeeds.

This creates a small real A/B test of whether richer preproduction evidence produces more specific, active, story-identifying images.

## Existing machinery to preserve

Reuse rather than replace:

- `state/visual/SCENE_CANDIDATES.json`
- `state/visual/ILLUSTRATION_REGISTRY.json`
- `state/visual/ILLUSTRATION_APPROVALS.json`
- `state/visual/CHARACTER_VISUAL_REFERENCES.json`
- `state/visual/PRODUCTION_HOLD.json`
- `state/visual/GENERATION_QUEUE.json`
- `scripts/build_generation_queue.py`
- `scripts/build_prompt_packs.py`
- `scripts/intake_generated_illustrations.py`
- `scripts/apply_illustration_approvals.py`
- `scripts/promote_illustrations.py`
- `scripts/performance_roundtrip_references.py`

`ILLUSTRATION_APPROVALS.json` keeps its existing meaning: post-generation approval or rejection of a concrete generated asset. Do not overload it with pre-generation scene approval.

## Bounded generation approval

Add one small machine-readable pilot file that records explicit creator approval for exactly five generation targets while the global production hold remains active.

The normal hold behavior remains unchanged for every other scene.

When the hold is active:

1. the normal global candidate list must not leak into the queue;
2. only explicitly bounded approved pilot candidates may become `generation_ready`;
3. normal registry duplicate checks, anchor checks, character-reference selection, versioning, and fresh PERFORMANCE-reference matching still apply;
4. queued records must identify the bounded batch that authorized them.

When the hold is inactive, existing global queue behavior must remain unchanged.

## Pilot scenes

### 1. `de-ch005-player-reads-greg`

Canon chapter: 005, `THE WARRIOR`.

Anchor: `He knew I was studying him. I did not realize he was studying me.`

Visual truth: Greg thinks he is reading the unnamed player across the table, but the player has recognized Greg's scrutiny and is reading Greg back. The frame should communicate reciprocal observation and Greg's blind spot, not generic gambling competence.

### 2. `de-ch005-jorren-offers-hand`

Canon chapter: 005, `THE WARRIOR`.

Anchor: `Jorren offered a hand.`

Visual truth: Greg's knowledge is ahead of his current conditioning. His foot lags, Jorren drops him, and Jorren offers him a hand while Greg lies in the warm practice-yard sand. This is a body-limit scene, not a victory pose.

### 3. `de-ch007-antonius-reverses-frame`

Canon chapter: 007, `THE BUYER`.

Anchor: `Antonius stopped. Fuck. He came back and picked up the gray frame himself.`

Visual truth: Greg's value claim physically changes Antonius's treatment of the Tere reference from discardable debris to an object worth personally handling. Preserve broom, dirty storeroom work, gray frame, and the reversal of motion.

### 4. `de-ch013-arlo-one-page`

Canon chapter: 013, `THE STUDENT`.

Anchor: `He opened the notebook to a page of readings and turned that page toward me without surrendering the rest of the notes.`

Visual truth: Arlo shares evidence without surrendering process ownership. The notebook remains physically his, one page is turned toward Greg, and the ruined regulator can sit between them as failed work made useful.

### 5. `de-ch018-hessa-covers-bowl`

Canon chapter: 018, `THE EXPERIMENTER`.

Anchor: `Hessa reached across the table and covered the bowl with the cloth.`

Visual truth: Greg wants to continue because he is interested; Hessa ends access after nineteen casts. The covered bowl is procedural authority made physical.

## Temporal continuity rule for the pilot

The current prompt-pack builder contains a legacy default that describes Greg as nineteen with a permanent left BKA and two crutches whenever Greg appears. That is not valid for these early scenes.

For this pilot, explicit scene-level `continuity_notes` override that legacy default. The five scenes are pre-amputation Greg. The Ch005 training scene may deliberately show his lower body because his intact but underconditioned body is the point of the scene.

This override is a narrow safety repair, not the full temporal visual bible. A later Definitive Edition stage should replace static era assumptions with evidence-backed temporal character state.

## Image-generation and promotion boundary

This change authorizes generation targets, not finished images.

After assets are generated and intaked:

- each concrete asset must still pass normal post-generation approval;
- current live art stays live until a replacement is explicitly approved and promoted;
- the five new images are judged against current art for scene specificity, action, blocking, supporting-character autonomy, visible state information, mundane detail, memorability, spoiler cost, and redundancy;
- no mass generation follows automatically from a good result.

## Success criteria

The pilot succeeds architecturally if:

- exactly five bounded candidates can enter the queue while the global hold remains active;
- no unapproved candidate enters the queue during the hold;
- explicit early-era continuity reaches prompt packs without the incorrect BKA/crutch default;
- fresh PERFORMANCE evidence attaches only when the exact current-canon anchor matches;
- normal queue behavior remains unchanged when the hold is inactive;
- tests cover the bounded-hold behavior and continuity override.

The visual experiment succeeds editorially only if the generated Ch007/013/018 images show a meaningful specificity advantage over prose-only selection or current art. If they do not, the system should remain simpler.