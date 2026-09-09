# R2 IMAGE PACKET 002

- `packet_id`: `r2-image-packet-002`
- `transaction_type`: `chapter`
- `chapter_id`: `r2-ch002`
- `scope`: Chapter 2 only; one continuity-safe training-yard anchor if it earns approval
- `authority_checked`: current `main` at `ca1967823c339a8b2199aff74ce7de80e1c78eec`; `r2/data/chapters/ch002.json`; `r2/assets/written/ch002.md`
- `visual_canon_checked`: `yes`
- `claim_branch`: `image/r2-ch002-novice-yard`
- `claim_pr`: pending creation after claim commit
- `worker_model_tier`: `higher_thinking`
- `library_stage_root`: `/Peg-Leg Greg Image Integration/R2/`
- `status`: `planning`
- `next_action`: generate and review `r2-ch002-img01`; stage only if approved; reconcile newer main and record handshake

## Claim check

- Chapter 1 is actively owned by draft PR #200.
- No other active `image/r2-*` chapter claim was found before this branch was created.
- Chapter 2 is published in both Listen and Read and has no integrated image.
- `00 Canon/` currently exposes no approved R2 continuity binaries, so this routine transaction must not invent Greg's face/body, Sella's identity, or Jorren's identity.

## IMAGE JOB 01

- `image_id`: `r2-ch002-img01`
- `chapter_id`: `r2-ch002`
- `scene_id`: `guild-yard-two-things`
- `role`: `anchor`
- `priority`: `high`
- `purpose`: visualize the chapter's core learning pressure, knowing what good sword work looks like while his present body still has to earn it, without inventing recurring character identity before Chapter 1's continuity bootstrap finishes
- `must_show`:
  - first-person / near-first-person view from Greg's position in the old Carrow Guild training yard
  - a plain wooden practice sword occupying part of the foreground
  - practical sand yard, posts, weapon racks, scuffed gear, wet/darkened patches, working training lanes
  - several anonymous Bronze-level trainees drilling imperfectly in the middle distance
  - one faded-Silver instructor figure moving down the line, not posed as a portrait
  - evidence of repetition and ordinary work rather than heroic combat
- `must_not_show`:
  - Greg's face or durable character identity
  - a peg leg, prosthetic, amputation, crutches, or future disability shorthand
  - a recognizable invented Sella or Jorren identity
  - glossy heroic fantasy-poster staging
  - arena spectacle, magical effects, or elite combat
  - text or labels
- `continuity_dependencies`:
  - current R2 style doctrine only
  - exact Chapter 2 Guild-yard evidence
  - no identity anchor required
- `hard_references`:
  - `r2/assets/written/ch002.md`: three practice lanes, two sparring circles, row of posts, weapon racks, sand dark where people poured water over their heads; Bronze fighters drilling; Silver instructor counting repetitions
  - early R2 rule: Greg is nineteen and physically intact, though this composition intentionally avoids body-state emphasis
- `soft_references`:
  - `r2/visual-state/R2_VISUAL_CANON.md` sketch + ink + paint direction
  - Carrow as a working city/institution rather than scenic fantasy
- `allowed_invention`:
  - incidental anonymous trainees, rack arrangement, wall/door placement, practice-yard clutter consistent with a working guild
- `style_lane`: `r2_narrative`
- `publish_intent`: `publish_if_approved`
- `destination_path`: `r2/assets/images/chapters/ch002/r2-ch002-img01.webp`
- `library_incoming_path`: `/Peg-Leg Greg Image Integration/R2/01 Incoming/ch002/r2-ch002-img01.webp`
- `library_approved_path`: `/Peg-Leg Greg Image Integration/R2/02 Approved/ch002/r2-ch002-img01.webp`
- `status`: `planned`
- `promotion_if_approved`:
  - possible `guild_training_yard` location evidence only
  - possible `r2_style` evidence only if genuinely strong
- `failure_tags`: none yet
- `notes`: Deliberately uses subjective composition to avoid creating a competing Greg identity while Chapter 1 bootstrap claim #200 is active.

### Prompt

Create an original illustrated-novel anchor image for Peg-Leg Greg R2.

SOURCE MOMENT
Chapter 2, inside the old Carrow Guild training yard. Greg can instantly see what every Bronze trainee is doing wrong, but when he picks up a wooden sword his own nineteen-year-old body cannot yet execute what his later-life memory understands. The yard becomes the place where knowledge and embodied skill separate.

IMAGE PURPOSE
Make the reader feel the gap between expert perception and novice execution without inventing Greg's recurring face/body identity before the active Chapter 1 continuity bootstrap is finished.

SUBJECT / ACTION
Use a first-person or near-first-person viewpoint from Greg's position. A plain wooden practice sword and perhaps his hands/forearms occupy part of the foreground. Beyond them, the practical Guild yard is busy with anonymous Bronze trainees drilling badly and repetitively while a faded-Silver instructor moves down the line correcting people. Nobody is posing for the viewer.

CAMERA / COMPOSITION
Eye-level subjective view, slightly off-center, with the wooden practice sword forming a foreground diagonal into the training lanes. Build depth through posts, racks, scuffed sand, moving trainees, and the instructor. Let the scene feel observational and workmanlike, not cinematic spectacle.

MUST SHOW
Three-lane working-yard feeling, practice posts, weapon racks, worn/scuffed sand with darker wet patches, ordinary Bronze trainees repeating basics, plain wooden practice weapon, institutional wear and labor.

MUST NOT SHOW
Do not show Greg's face. Do not establish a recognizable new Sella or Jorren identity. No peg leg, prosthetic, amputation, crutches, magical glow, arena spectacle, elite duel, heroic victory pose, text, signs, labels, or glossy fantasy-poster finish.

CONTINUITY
Early R2 only. Greg is nineteen and physically intact, but lower-body state is not the subject and should remain visually unimportant. Use only current R2 style/location doctrine. Do not borrow Run 1 disability continuity.

STYLE
Sketch + ink + paint. Visible drawing structure, painterly wash, rough human edges, restrained sepia/charcoal/dirty-neutral palette, practical warm light, selective detail, illustrated-novel energy. Avoid glossy generic AI-fantasy polish.

TONE
Hungry, analytical, slightly humiliating, useful. Repetition before mastery.

ALLOWED INVENTION
Only incidental anonymous trainees, practical racks/posts, yard clutter, doors/walls, and mundane training equipment consistent with a busy working guild.

OUTPUT ROLE
Chapter 2 anchor.

Do not add text.

## Transaction finish

- GitHub claim/state updated: in progress
- Library staging recorded: pending generation/review
- next-worker handshake left: pending
- worker stopped without claiming another chapter: pending
