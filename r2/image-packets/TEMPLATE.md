# R2 IMAGE PACKET TEMPLATE

Use this for bounded R2 image production.

Do not start a generation batch until current R2 story authority and `../visual-state/R2_VISUAL_CANON.md` have been checked.

## Packet header

- `packet_id`:
- `scope`:
- `authority_checked`:
- `visual_canon_checked`: `yes/no`
- `status`: `planned | generating | review | handoff | verifying | integrated`
- `next_action`:

## Batch rule

Default to 3–5 jobs.

Do not widen the batch merely because generation is cheap. Finish the current packet through review/promotion/handoff before opening the next one unless there is a clear parallelization benefit.

---

## IMAGE JOB

- `image_id`:
- `chapter_id`:
- `scene_id`:
- `role`: `cover_frontdoor | anchor | support | texture | continuity`
- `priority`: `high | medium | low`
- `purpose`:
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
- `allowed_invention`:
  -
- `style_lane`: `r2_narrative`
- `publish_intent`: `internal | optional | publish_if_approved | publish`
- `destination_path`:
- `status`: `planned | generated | approved | revise | rejected | handoff_ready | uploaded_unverified | verified | integrated`
- `promotion_if_approved`:
  -
- `failure_tags`:
  -
- `notes`:

### Prompt skeleton

```text
Create an original illustrated-novel image for Peg-Leg Greg R2.

SOURCE MOMENT
[exact scene / concise scene truth]

IMAGE PURPOSE
[what this image must add that prose alone does not]

SUBJECT / ACTION
[who is present and what is physically happening]

CAMERA / COMPOSITION
[distance, angle, eye path, foreground, movement]

MUST SHOW
[list]

MUST NOT SHOW
[list]

CONTINUITY
Use only the relevant approved R2 references. Preserve established identity, age, body state, clothing/location evidence, and scene-specific constraints. Change only what this image requires.

STYLE
Sketch + ink + paint. Visible drawing structure, painterly wash, rough human edges, restrained dirty palette, illustrated-novel energy, selective detail. Avoid glossy generic AI-fantasy polish.

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
- `unwanted_text`

### Handoff

- approved filename:
- exact destination:
- ZIP/package:
- uploaded:
- repository binary verified:
- chapter manifest updated:
- deployed page checked:
