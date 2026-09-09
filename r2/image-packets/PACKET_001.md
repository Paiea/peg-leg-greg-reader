# R2 IMAGE PACKET 001

- `packet_id`: `r2-image-packet-001`
- `scope`: early Greg continuity + Carrow continuity + Chapter 1 art
- `authority_checked`: `r2/assets/written/ch001.md` + current R2 manifests
- `visual_canon_checked`: `yes`
- `status`: `planned`
- `next_action`: generate jobs 001–003 first; review continuity anchors before generating jobs 004–005

## Packet strategy

This packet intentionally spends the first three jobs on reusable continuity before publishing more chapter art.

Generation order:

1. Greg face / expression anchor
2. Greg body / posture anchor
3. Carrow environment anchor
4. Chapter 1 mirror anchor, using approved continuity from 1–3
5. Chapter 1 younger-Carrow support, using approved continuity from 1–3

Do not generate 4–5 from rejected or unreviewed continuity anchors.

---

## 001 — Greg face / expression anchor

- `image_id`: `r2-vc-greg-face-001`
- `chapter_id`: `visual-canon`
- `scene_id`: `early-greg-face`
- `role`: `continuity`
- `priority`: `high`
- `purpose`: establish a reusable age-19 Greg face/expression reference without making a polished hero portrait
- `must_show`:
  - clearly nineteen / very young adult
  - lean, slightly underfed face
  - messy dark hair
  - rough practical presentation
  - sharp watchful eyes
  - controlled danger / calculating attention
  - expression can carry faint amused menace but not warmth
- `must_not_show`:
  - middle-aged face
  - heroic grin
  - glossy romance-cover beauty
  - theatrical villain makeup or exaggerated psychosis
  - peg leg / prosthetic / crutches
- `continuity_dependencies`: none; this is a seed anchor
- `hard_references`: current R2 story evidence + approved current R2 site-art identity only when useful
- `soft_references`: prior sketchier PLG visual direction for roughness, never disability state
- `allowed_invention`: minor hair arrangement, cheap-shirt detail, practical background texture
- `style_lane`: `r2_narrative`
- `publish_intent`: `internal`
- `destination_path`: `r2/assets/images/continuity/greg/r2-vc-greg-face-001.webp`
- `status`: `planned`
- `promotion_if_approved`: `greg_face`, `greg_expression`, optional `r2_style`

### Prompt

```text
Create an original continuity-reference illustration for Peg-Leg Greg R2.

SUBJECT
Greg at age nineteen. Clearly young, lean and slightly underfed, messy dark hair, rough practical clothes, sharp watchful eyes. He has lived an entire later life in memory but physically looks nineteen.

EMOTIONAL TARGET
Controlled danger. Calculating attention. A faint possibility of amused menace, but not warmth, friendliness, or theatrical villainy. He should feel like someone easy to underestimate until his attention lands on you.

COMPOSITION
Chest-up or upper-body three-quarter portrait with natural asymmetry, not a clean studio headshot. Let the face and eyes carry the image. Cheap-room or Carrow texture may exist behind him but should stay secondary.

CONTINUITY
Early R2 only. Do not show or imply a peg leg, prosthetic, amputation, or crutches. Do not age him upward.

STYLE
Sketch + ink + paint. Visible drawing structure, pencil/ink edges, painterly wash, rough human texture, restrained sepia/charcoal/dirty-neutral palette, selective detail, illustrated-novel energy. Avoid glossy generic AI-fantasy polish and hyper-clean cinematic concept art.

Do not add text.
```

---

## 002 — Greg body / posture anchor

- `image_id`: `r2-vc-greg-body-001`
- `chapter_id`: `visual-canon`
- `scene_id`: `early-greg-body`
- `role`: `continuity`
- `priority`: `high`
- `purpose`: establish early-R2 body state, clothing scale, and physical posture so later generations do not inherit Run 1 disability continuity
- `must_show`:
  - age-19 Greg
  - lean young body
  - both legs intact
  - two normal boots
  - cheap practical clothing / early low-status gear
  - alert, self-possessed posture rather than heroic posing
- `must_not_show`:
  - peg leg
  - prosthetic
  - crutches
  - amputation
  - middle-aged proportions
  - oversized warrior physique
  - expensive or high-rank equipment
- `continuity_dependencies`: approved `r2-vc-greg-face-001`
- `hard_references`: exact early-R2 leg/body state from Chapter 1
- `soft_references`: approved Greg face anchor
- `allowed_invention`: simple cheap clothing details not contradicted by story
- `style_lane`: `r2_narrative`
- `publish_intent`: `internal`
- `destination_path`: `r2/assets/images/continuity/greg/r2-vc-greg-body-001.webp`
- `status`: `planned`
- `promotion_if_approved`: `greg_body_posture`, optional `greg_clothing`

### Prompt

```text
Create an original full-body continuity-reference illustration for Peg-Leg Greg R2 using the approved young-Greg face reference.

SUBJECT
Greg at nineteen. Lean, young, slightly underfed, rough practical appearance, cheap early-story clothes and boots. He should look capable but not physically perfected.

BODY STATE
Both legs are intact. Show two normal legs and two normal boots clearly enough to lock early-R2 continuity. No peg leg, prosthetic, amputation, crutches, brace, or injury shorthand.

POSTURE
Alert and self-possessed, slightly coiled, weight placed naturally, more calculating than heroic. Avoid a superhero stance or cheerful adventurer pose.

SETTING
Simple cheap-room / working-city context. Background exists only to ground scale and clothing.

STYLE
Sketch + ink + paint. Visible linework and construction, painterly wash, restrained dirty palette, imperfect illustrated-novel finish. Avoid glossy AI concept-art polish.

Do not add text.
```

---

## 003 — Carrow environment anchor

- `image_id`: `r2-vc-carrow-001`
- `chapter_id`: `visual-canon`
- `scene_id`: `younger-carrow-street`
- `role`: `continuity`
- `priority`: `high`
- `purpose`: establish Carrow as a working inland city rather than a generic harbor/fantasy postcard
- `must_show`:
  - narrow practical city route
  - stone / timber / worn plaster
  - mud or rough street surface
  - carts / shop or guild activity / signs of labor
  - dense lived-in architecture
  - ordinary people using the space
  - early / younger Carrow feel
- `must_not_show`:
  - open water
  - docks
  - harbor skyline
  - empty scenic fantasy street
  - pristine medieval theme-park cleanliness
  - giant towers included only to look epic
- `continuity_dependencies`: none beyond R2 style
- `hard_references`: Chapter 1 evidence: red Guild roof, missing later Exchange/apothecary, cart through mud where later paving exists
- `soft_references`: current sketch/ink/paint style direction
- `allowed_invention`: incidental shop fronts, workers, carts, signs, rooflines consistent with a working city
- `style_lane`: `r2_narrative`
- `publish_intent`: `internal_or_optional`
- `destination_path`: `r2/assets/images/continuity/locations/r2-vc-carrow-001.webp`
- `status`: `planned`
- `promotion_if_approved`: `carrow_location`, `r2_style`

### Prompt

```text
Create an original environment continuity illustration for Peg-Leg Greg R2.

SETTING
Carrow in Greg's early life, seen as a working inland fantasy city rather than scenery. Narrow urban route, worn stone and timber buildings, plaster, mud, carts, trade, repairs, shop or guild activity, ordinary people moving through the space. The city should feel used, accumulated, and practical.

STORY EVIDENCE
The Guild roof still has old red tile. A cart can move through mud where Greg later remembers paving. Later landmarks such as the Exchange/apothecary are not yet present.

MUST NOT SHOW
No harbor, no open water, no docks, no scenic port identity, no pristine fantasy-tourism street.

COMPOSITION
Environment-first. Build a strong eye path through the working street using carts, awnings/signs, people, doorways, and vertical architecture. Avoid a centered empty street vanishing-point cliché.

STYLE
Sketch + ink + paint. Visible linework, painterly wash, rough print/illustrated-novel texture, restrained dirty-neutral palette with practical light. Avoid glossy generic AI fantasy.

Do not add title text or labels.
```

---

## 004 — Chapter 1 anchor: the mirror

- `image_id`: `r2-ch001-img01`
- `chapter_id`: `r2-ch001`
- `scene_id`: `mirror-nineteen`
- `role`: `anchor`
- `priority`: `high`
- `purpose`: publish the core opening realization: a fifty-nine-year-old memory looking out through a nineteen-year-old face
- `must_show`:
  - approved young Greg identity
  - cheap room / cracked washbasin / spotted mirror feeling
  - Greg studying his reflection
  - unease + fascination rather than simple joy
  - physical youth without future disability
- `must_not_show`:
  - peg leg / prosthetic / crutches
  - middle-aged reflected face
  - happy heroic rebirth poster
  - luxurious room
  - magical glow explaining the event
- `continuity_dependencies`:
  - approved `r2-vc-greg-face-001`
  - approved `r2-vc-greg-body-001` as body-state authority
  - approved R2 style evidence
- `hard_references`: Chapter 1 mirror / cheap room scene
- `soft_references`: approved Carrow/style anchor where useful
- `allowed_invention`: exact mirror frame, minor room clutter, lamp/window placement
- `style_lane`: `r2_narrative`
- `publish_intent`: `publish_if_approved`
- `destination_path`: `r2/assets/images/chapters/ch001/r2-ch001-img01.webp`
- `status`: `planned`
- `promotion_if_approved`: possible `greg_expression`, `cheap_room`, `r2_style` if those parts are strong

### Prompt

```text
Create an original chapter-anchor illustration for Peg-Leg Greg R2 using the approved young-Greg continuity references.

SOURCE MOMENT
Greg has just realized the face in the spotted mirror is his own at nineteen. He has decades of later-life memory, but the body in front of him is young, healthy, and unfamiliar in its ease.

SCENE
A cheap plaster room. Narrow bed, one chair with a coat, cracked washbasin, spotted mirror, cheap sword nearby. Greg leans toward or studies the mirror. His expression mixes disbelief, calculation, fascination, and a dangerous amount of possibility. Do not make it a cheerful rebirth poster.

CONTINUITY
Greg is nineteen. Both legs are intact in early R2. The composition does not need to emphasize the lower body, but it must not show or imply a peg leg, prosthetic, amputation, or crutches.

COMPOSITION
Medium scene with the mirror creating a second eye path rather than a symmetrical portrait. Let room objects establish poverty and history. The reflection should read clearly as the same young Greg, not an older ghost.

STYLE
Sketch + ink + paint. Visible drawing structure, rough human linework, painterly wash, restrained dirty palette, selective detail, illustrated-novel finish. Avoid glossy cinematic AI fantasy and magical explanatory effects.

Do not add text.
```

---

## 005 — Chapter 1 support: younger Carrow at the window

- `image_id`: `r2-ch001-img02`
- `chapter_id`: `r2-ch001`
- `scene_id`: `younger-carrow-window`
- `role`: `support`
- `priority`: `medium`
- `purpose`: show the first external proof that Greg is not only physically young; Carrow itself is earlier
- `must_show`:
  - approved young Greg
  - Greg at or near the cheap-room window
  - younger Carrow outside
  - old red Guild roof
  - mud / cart where later paving exists
  - absence of later-city polish
  - observational/calculating posture
- `must_not_show`:
  - harbor / open water
  - peg leg / prosthetic / crutches
  - grand panoramic fantasy-city hero shot
  - obvious time-travel magic effects
  - happy nostalgia
- `continuity_dependencies`:
  - approved `r2-vc-greg-face-001`
  - approved `r2-vc-greg-body-001`
  - approved `r2-vc-carrow-001`
- `hard_references`: Chapter 1 window / younger Carrow evidence
- `soft_references`: approved style anchor
- `allowed_invention`: incidental street workers, cart type, minor roofs/signage
- `style_lane`: `r2_narrative`
- `publish_intent`: `publish_if_approved`
- `destination_path`: `r2/assets/images/chapters/ch001/r2-ch001-img02.webp`
- `status`: `planned`
- `promotion_if_approved`: possible `carrow_location`, `greg_posture`, `r2_style`

### Prompt

```text
Create an original support illustration for Chapter 1 of Peg-Leg Greg R2 using the approved Greg and Carrow continuity references.

SOURCE MOMENT
Greg goes to the window and realizes Carrow is younger too. The Guild still has its old red roof. Later buildings are missing. A cart rolls through mud where he remembers paving. He distrusts the conclusion and starts treating the future as evidence that the present must prove.

SCENE
Greg at the edge of a cheap-room window, partly foregrounded, studying the working street below. Carrow outside should carry the image: old red Guild roof, worn buildings, mud, cart traffic, ordinary workers and trade. His posture is observational and calculating, not nostalgic.

CONTINUITY
Greg is nineteen and physically intact. No peg leg, prosthetic, crutches, or future-disability leakage. Carrow is inland and working. No harbor or open water.

COMPOSITION
Over-shoulder or three-quarter interior-to-exterior composition. Use the window frame and street movement to carry the eye from Greg into the younger city. Avoid a grand panoramic skyline.

STYLE
Sketch + ink + paint, visible linework, painterly wash, rough print texture, restrained dirty palette, illustrated-novel energy. Avoid glossy generic AI fantasy.

Do not add text.
```

---

## Approval gate

Before Packet 001 is considered complete:

- 001–003 reviewed explicitly
- useful continuity evidence promoted granularly
- 004–005 generated from approved continuity, not from memory alone
- approved outputs assigned exact filenames
- approved binaries handed off through `state/IMAGE_BINARY_HANDOFF.md`
- repository binaries verified before chapter manifests change
- only publish 004/005 if they genuinely improve Chapter 1

Do not open Packet 002 merely because five outputs exist. Open it when Packet 001 leaves a trustworthy visual trailhead.
