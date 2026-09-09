# R2 IMAGE PACKET TEMPLATE

Use this for one bounded R2 image transaction.

Do not start generation until current R2 story authority, `../PIPELINE.md`, `../IMAGE_SYSTEM.md`, and `../visual-state/R2_VISUAL_CANON.md` have been checked.

## Packet header

- `packet_id`:
- `transaction_type`: `chapter | visual_canon | site_frontdoor | release`
- `chapter_id`:
- `scope`:
- `authority_checked`:
- `visual_canon_checked`: `yes/no`
- `chapter_source_file`:
- `chapter_read_complete`: `yes/no`
- `claim_branch`:
- `claim_pr`:
- `worker_model_tier`: `instant | higher_thinking`
- `library_stage_root`: `/Peg-Leg Greg Image Integration/R2/`
- `status`: `claimed | reading_source | planning | generating | review | staging | recorded | stopped`
- `next_action`:

## Worker rule

For normal chapter production:

> One fresh worker owns one chapter transaction and then stops.

The worker must read the actual chapter source before scene selection.

The chapter title is metadata only. It may identify the chapter but may not substitute for story evidence or become the image brief.

A routine chapter packet normally resolves **about five source-grounded scene jobs**, then generates up to five images, usually one per selected scene.

If the chapter genuinely contains fewer than five strong visual moments, use fewer. Do not manufacture filler.

Do not claim the next chapter in the same chat after finishing this packet.

Visual-canon/bootstrap packets are explicit exceptions when later chapter workers depend on the new continuity authority.

## Claim check

Before filling the jobs below:

- inspect open image PRs and active `image/r2-*` branches
- skip chapters already owned by another worker
- create the durable claim before generation
- preserve newer `main` authority

## Whole-chapter grounding

Before choosing jobs:

1. locate the exact current chapter source
2. read enough of the whole chapter to understand its movement
3. identify about five visually distinct moments actually present in the source
4. prefer concrete action, work, relationship behavior, objects, setting use, and state changes
5. avoid near-duplicate portraits or title-literal poster concepts

If exact source material cannot be resolved safely, mark `source_authority_gap` and stop or escalate instead of improvising.

## Scene shortlist

Record the chapter-level shortlist before generation.

### SCENE CANDIDATE

- `candidate_id`:
- `source_location`:
- `source_excerpt_or_evidence`:
- `scene_truth`:
- `characters_present`:
- `physical_action`:
- `location_environment`:
- `visual_reason`:
- `selected_for_generation`: `yes/no`

Repeat until the useful chapter shortlist is resolved, normally about five selected scenes.

---

## IMAGE JOB

- `image_id`:
- `chapter_id`:
- `source_file`:
- `source_location`:
- `source_excerpt`:
- `scene_id`:
- `scene_truth`:
- `role`: `cover_frontdoor | anchor | support | texture | continuity`
- `priority`: `high | medium | low`
- `image_reason`:
- `purpose`:
- `characters_present`:
  -
- `physical_action`:
- `location_environment`:
- `must_show`:
  -
- `must_not_show`:
  -
- `continuity_dependencies`:
  -
- `hard_references`:
  -
- `soft_references`:
  -
- `story_brains_consulted`:
  -
- `allowed_invention`:
  -
- `style_lane`: `r2_narrative`
- `publish_intent`: `internal | optional | publish_if_approved | publish`
- `destination_path`:
- `library_incoming_path`:
- `library_approved_path`:
- `status`: `planned | generated | approved | revise | rejected | library_stage_pending | staged_incoming | staged_approved | released | uploaded_unverified | verified | integrated`
- `promotion_if_approved`:
  -
- `failure_tags`:
  -
- `notes`:

### Prompt skeleton

```text
Create an original illustrated-novel image for Peg-Leg Greg R2.

SOURCE AUTHORITY
File: [exact current chapter source file]
Moment: [source location]
Evidence: [brief excerpt or tightly faithful source evidence]

SCENE TRUTH
[what is actually happening in this exact moment]

IMAGE PURPOSE
[why this particular source moment earns an image]

SUBJECT / ACTION
[who is present and what is physically happening]

ENVIRONMENT
[where they are and the material details that matter]

CAMERA / COMPOSITION
[distance, angle, eye path, foreground, movement]

MUST SHOW
[list]

MUST NOT SHOW
[list]

CONTINUITY
Use the relevant approved R2 visual canon, Library continuity references, and only task-relevant story-brain evidence that remains compatible with current R2 authority. Preserve established identity, age, body state, clothing/location evidence, and scene-specific constraints. Change only what this image requires.

STYLE
Sketch + ink + paint. Visible drawing structure, painterly wash, rough human edges, restrained dirty palette, illustrated-novel energy, selective detail. Avoid glossy generic AI-fantasy polish.

ANTI-GENERIC RULE
Do not visualize the chapter title as a poster concept. The exact source scene above controls subject, action, environment, and composition. Reject generic fantasy hero poses, generic job-role symbolism, or scenic filler unsupported by the source.

TONE
[scene-specific emotional target]

ALLOWED INVENTION
[incidental details the model may invent]

OUTPUT ROLE
[anchor/support/continuity/etc.]

Do not add text unless the packet explicitly requires it.
```

### Review

Decision: `approved | revise | rejected`

Source-grounding check:

- clearly depicts selected source moment: `yes/no`
- could this image have been generated from title alone: `yes/no`
- scene-specific physical evidence survived: `yes/no`
- continuity references respected: `yes/no`

Useful evidence to promote:

- face:
- expression:
- body/posture:
- clothing:
- location:
- style:
- composition only:

Failure tags if not approved:

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

### Library staging

- generated file reference available: `yes/no`
- incoming path:
- approval status:
- approved path:
- canon promotion path if applicable:
- release status: `unreleased | released`
- release id:

If safe generated bytes are unavailable, use `library_stage_pending`. Do not claim the binary is staged.

### Transaction finish

- exact chapter source recorded:
- scene shortlist recorded:
- generated scene count:
- GitHub claim/state updated:
- Library staging recorded:
- next-worker handshake left:
- worker stopped without claiming another chapter: `yes/no`
