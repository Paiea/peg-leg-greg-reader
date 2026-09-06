# PEG-LEG GREG — IMAGE PRODUCTION

Durable coverage-first illustration workflow.

## Goal

Fill the reader first. Upgrade later.

Target roughly **1–3 meaningful illustrations per chapter, ideally 3** over time.

Priority order:
1. chapters with zero art
2. chapters with only one image
3. weak/mismatched art
4. chapters needing a second/third image
5. replacements only when materially better

Generation queues should preserve this coverage order mechanically. When prompt-ready candidates compete, lower current chapter image count outranks candidate priority; candidate priority then breaks ties. This keeps a dramatic newer chapter from repeatedly jumping ahead of an older chapter that still has no art at all.

When the zero-art list is large, backfill it in bounded older-first waves. A useful default is **five older zero-art chapters per iteration**: read the exact chapter prose, nominate one genuinely visual prompt-ready scene per chapter, then let normal queue sorting move those older chapters ahead of newer zero-art work. Do not auto-invent scene briefs from titles alone.

## Manuscript scene-candidate handoff

After a chapter is durably accepted, the Manuscript Engine **may nominate 0–2 genuinely visual moments** for later illustration. This is optional and nonblocking. Do not slow chapter throughput merely to invent an art target.

Write nominations to `state/visual/SCENE_CANDIDATES.json`. **Never insert production tags into canonical manuscript prose.**

A useful candidate records:
- chapter number and exact current chapter title
- short scene summary
- visual hook: what makes the moment worth seeing rather than merely reading
- characters actually required in frame
- location and mood
- optional scene tags such as `workshop`, `backstage`, `street`, or `table_work` when they are genuinely useful for reference selection
- optional camera-angle / pose-family intent when the shot specifically calls for it
- optional framing preference; normal Greg scenes default to `above_waist`
- priority: `high`, `medium`, or `low`
- kind, normally `chapter_illustration`
- fit target: `exact` for iconic/continuity-sensitive scenes or `close_enough` for normal coverage
- spoiler level
- optional natural paragraph anchor for eventual reader placement
- status, initially `candidate`

Prefer moments with physical work, entrances/exits, unusual stage or room geometry, meaningful props, environmental movement, relationship action, comedy/recovery, strong place identity, or an image that would carry a chapter at a glance.

Do **not** mechanically nominate every chapter. Zero good candidates is better than a weak obligatory image brief.

The visual-production lane turns candidates into `ILLUSTRATION_BACKLOG.md` and deterministic prompt packs. Image generation and final approval remain explicit production actions.

## Paragraph-anchor validation gate

`validate_paragraph_anchors.py` checks scene-candidate paragraph anchors against the current generated chapter HTML before a candidate is allowed into the generation queue.

Rules:
- normalize harmless HTML tags/entities/whitespace before matching
- a valid anchor must match exactly once in the current chapter text
- zero matches is `missing`
- more than one match is `ambiguous`
- missing/ambiguous anchors set `anchor_blocked: true` and move a prompt-ready candidate back to `candidate`
- a later unique fix may restore a previously anchor-blocked candidate to `prompt_ready`
- `build_generation_queue.py` also refuses any `anchor_blocked` candidate as defense in depth

Exact-match validation is universal. The active older-backfill lane may additionally set `anchor_quality_enforced: true`. For those candidates, the validator also scores anchor distinctiveness and blocks weak placement text before generation. Current weak signals include very short anchors, short pronoun-led anchors, and anchors with too few distinctive content tokens inside the chapter. A line can therefore be unique but still be too flimsy for durable automated placement.

Use the stricter quality gate on bounded backfill work we control rather than retroactively changing unrelated historical candidate semantics. When the quality gate catches a weak anchor, replace it with stronger nearby manuscript text. Do not lower the threshold merely to restore a packet count.

`state/visual/PARAGRAPH_ANCHOR_REPORT.md` is the compact audit surface. **Fix the candidate anchor rather than weakening the validator.** Generation should not proceed for a scene that cannot be placed safely later.

## Registry-first rule

New illustration work should enter through `state/visual/ILLUSTRATION_REGISTRY.json` before it becomes live reader art. The registry is the durable source of truth for candidate linkage, prompt pack, status, alt text, source asset, live asset, fit quality, and useful visual-continuity metadata.

For newly generated art, preserve generation metadata into the registry when known: required characters, style family, framing preference, camera angle, pose family, and scene tags. This gives accepted art enough structure to become a useful future character reference without reopening the original generation queue.

Accepted legacy art may not have those fields. `tag_registry_characters.py` can infer cataloged character names conservatively from accepted art's alt text/caption/notes. It must not invent characters that are not explicitly named or already carried from generation metadata. Existing explicit character tags and text-derived names are unioned so an older record tagged only `Greg` does not suppress a clearly named `Pell`, `Nessa`, `Marek`, `Serra`, or `Iven` in the same accepted-art metadata.

`backfill_tagged_registry_metadata.py` may then add coarse visual metadata only when accepted-art text metadata contains strong evidence, for example explicit `three-quarter`, `profile`, `working`, `writing`, `seated`, `backstage`, `market`, `mill`, or similar labels. It must preserve existing metadata and skip uncertain view/pose claims instead of guessing.

Existing accepted reader art predates this system. Until it is bootstrap-imported, the coverage report records those images as **unmanaged legacy migration debt**, not as a publishing failure. Do not delete or replace legacy art merely to make the registry cleaner.

Once legacy live art has been imported, CI may tighten from migration reporting to strict reader↔registry parity.

## Generation queue contract

`state/visual/GENERATION_QUEUE.json` is the machine-ready handoff for actual image generation.

Each queue record should be self-sufficient enough that a visual worker does not need to reopen the candidate ledger merely to understand the shot. Carry forward the scene summary, visual hook, required characters, location, mood, scene tags, spoiler level, fit target, paragraph anchor, prompt-pack path, deterministic target asset, current illustration coverage count, style family, framing preference, optional camera/pose intent, selected character reference assets, scored reference records, reference-selection rationale, character appearance notes, and continuity notes.

The queue remains a derivative. Candidate and manuscript authority still outrank it.

## Continuity-aware generation

`state/visual/CHARACTER_VISUAL_REFERENCES.json` is the compact reusable appearance/reference catalog for generation. It is visual-production guidance, not story canon. Manuscript evidence and `VISUAL_BIBLE.md` still outrank it.

For recurring characters:
- reuse accepted live artwork as reference assets when a trustworthy reference exists
- carry written appearance notes even when no single canonical image exists yet
- do not freeze unsupported facial details merely to make generations identical
- promote stronger accepted reference assets into the catalog when they become clearly useful

The catalog may include recurring characters before they have a trustworthy promoted reference asset. In that case, use conservative written continuity notes and let later accepted art earn promotion. **Do not invent a canonical face simply because the production packet wants one.**

For **Greg**, default normal chapter illustrations to **above-waist / chest-up / medium framing** unless lower-body visibility is materially important to the manuscript moment. This reduces unnecessary body-state contradictions and keeps generation focused on the face, hands, work, expression, and relationship action that usually matter more.

Do not solve lower-body continuity by inventing a peg leg, prosthetic, crutch state, injury state, or anatomy detail that the scene does not require. When lower-body state actually matters, read the exact chapter and use the correct period-specific manuscript evidence.

Shared default style remains **SKETCH + INK + PAINT**. Character reference assets should improve continuity without flattening camera, gesture, lighting, expression, or composition variety.

## Reference metadata backfill

Older hand-curated character anchors often predate structured framing/angle/pose/scene metadata. `backfill_character_reference_metadata.py` may attach **conservative, asset-specific metadata** to those known anchors through `reference_metadata` without converting them into fake auto-promoted registry records.

Backfill rules:
- only attach details that are already known from the accepted asset's role/use or a deliberate curated review
- do not infer unsupported facial canon or precise body details
- coarse labels such as `role_card`, `portrait_anchor`, `working`, `backstage`, or `above_waist` are preferred over speculative precision
- manual reference metadata should participate in the same scene-aware/diversity-aware scoring as promoted references
- rerunning the backfill must be idempotent and preserve manually corrected metadata

The current Greg Stagehand anchor is an especially useful normal-generation reference because it is deliberately **above waist** and supports backstage/work scenes without forcing lower-body state into the shot.

## Character-reference promotion and quality

Accepted art can become future continuity guidance, but the catalog must stay selective.

`promote_character_references.py` may nominate `approved` or `live` registry art into the structured reference pool when the asset clearly names/supports a cataloged character and clears the quality threshold. Promotion is additive production metadata; it never changes manuscript canon or approval status. Promoted references should retain framing, camera-angle, pose-family, and scene-tag metadata when the registry knows it.

Reference quality is scored mechanically. Current signals include:
- live art outranks merely approved art
- exact fit outranks close-enough fit
- shared `sketch-ink-paint` style receives a bonus
- hand-curated anchors remain strong baseline references
- strong face/style anchors may receive explicit bonuses
- accepted-art metadata that explicitly names the target character receives an identity-evidence bonus
- a single-character accepted image may receive an additional identity-anchor bonus
- normal Greg generation rewards `above_waist` references
- full-body/lower-body Greg references are penalized when the requested framing is above waist
- scene-tag overlap can reward a useful context match
- non-production statuses are heavily penalized

The identity-evidence bonus is metadata-grounded, not image vision. Automation may know that an accepted illustration explicitly names Pell, Nessa, Marek, Serra, or Iven; it does **not** thereby know that the face is beautifully rendered. `strong_face` remains a curated signal unless actual image review explicitly establishes it.

Automated promotion uses a minimum quality threshold and keeps only a compact top set per character. **Do not automatically accumulate every accepted panel featuring Greg.** A flooded reference pool is worse than a small trustworthy one. The promotion pass may inspect many eligible accepted records, but only the strongest compact retained set per character should feed generation.

`audit_character_references.py` reports stale/bad continuity metadata, including missing assets, duplicate assets, structured references pointing at missing or non-approved/non-live registry records, missing appearance notes, and Greg references explicitly tagged as lower-body-heavy without an above-waist anchor.

The generation queue selects the strongest current references per character rather than copying the whole catalog. Selection is **scene-aware and diversity-aware**: a reference matching useful scene tags may outrank a contextless alternative, while repeated camera angles or pose families receive a selection penalty so a character does not slowly collapse into one canonical portrait pose. Diversity never outranks basic identity/fit quality; it breaks close-enough choices among trustworthy anchors.

The queue stores selected scored records plus a plain-language rationale. Generation packets expose that rationale so a human can see why the continuity anchors won before spending a generation cycle.

Hand-curated references are allowed to remain stronger than mediocre legacy imports. A genuinely better accepted image should be able to outrank them through status, fit, style, scene usefulness, and continuity quality.

## Character-continuity report

`state/visual/CHARACTER_CONTINUITY_REPORT.md` is the compact dashboard for the current character-reference system. It should show each cataloged character's manual/promoted reference counts, tagged camera-angle and pose-family diversity, scene tags, above-waist anchor count, appearance-note coverage, and reference-audit issue count.

The report should also **route metadata repair**, not merely describe it. Count how often characters appear in current scene candidates and registry metadata, identify missing view-angle/pose-family/scene-tag fields, rank the highest-value catalog repair targets, and surface recurring characters that appear in production state but are not cataloged yet.

This report is diagnostic, not canon. A thin reference pool is a prompt to improve future accepted art metadata, not a reason to manufacture fake character details.

## Prompt-pack metadata contract

Prompt packs should declare useful generation metadata before the prose prompt:
- framing preference
- intended view angle or an explicit non-repetitive-angle instruction
- pose family or physical-action family
- scene tags

These values should flow candidate → prompt pack → generation queue → registry → accepted reference metadata. They exist to improve continuity and composition diversity, not to override the manuscript.

For Greg, prompt packs repeat the above-waist default unless the specific candidate intentionally requires lower-body visibility.

## Generation and approval packets

`state/visual/GENERATION_PACKET.md` is the disposable human-facing view of the next production batch. It is generated from the already coverage-prioritized queue and should normally show the next 25 ready shots with continuity context, selected-reference scores/rationale, and deterministic output paths.

For an active older backfill wave, also generate a **bounded packet** such as `state/visual/GENERATION_PACKET_156_160.md`. A bounded packet deliberately includes only one small chapter band and carries deterministic output targets, paragraph anchors, selected continuity references, reference rationale, and an approval checklist. Finish/review that band before widening the production wave.

The current older-backfill lane also maintains `state/visual/GENERATION_PACKET_161_165.md` as the second bounded handoff. Both bands are generated from the same queue contract, so deterministic targets, selected references, rationale, and approval checks stay consistent rather than being hand-maintained.

`state/visual/BOUNDED_PRODUCTION_REVIEW_156_160.md` is the execution/review router for the first bounded band. It joins candidate, generation-queue, and registry state and reports the real current production state for each candidate: `ready_to_generate`, `generated_awaiting_approval`, `approved_unpublished`, `live`, `rejected_retryable`, `blocked_anchor`, or `not_ready`. A rejected attempt remains retryable when candidate authority still permits another deterministic generation.

The bounded production review must not pretend that a pixel exists merely because a prompt packet exists. `ready_to_generate` means the prompt pack, deterministic target, anchor, and continuity context are ready for an image-generation handoff. It does not mean an image has already been generated or approved.

`state/visual/ILLUSTRATION_APPROVAL_PACKET.md` is the human-facing review surface for assets currently in `generated` status. It provides explicit approve/reject templates without changing approval authority.

These packet files are derivatives. The registry, candidate ledger, prompt packs, manuscript, and visual bible remain the durable authorities beneath them.

## Older backfill wave seeding

`scripts/seed_older_coverage_wave.py` is the deterministic bridge for the currently reviewed older coverage band. It may repair known weak anchors and add manuscript-grounded prompt-ready candidates only after the exact chapter prose has been read.

Current seeded coverage extends through Chapters **166–170**. The five nominated beats are:
- Chapter 166: Nessa repairing the goat-chewed mounting cloth by firelight while Pell helps
- Chapter 167: the Dast harvest-fair traffic/routing problem before the town properly appears
- Chapter 168: a loading cart forcing a lane directly through the north-arcade performance
- Chapter 169: Marek taking a tiny west-platform opening between grain speeches
- Chapter 170: Pell repeatedly moving the rear wagon rope away from a determined goat in the bridge queue

All five preserve the normal Greg `above_waist` framing default because lower-body state is not the point of those scenes.

## 5x5 contact-sheet default

One contact sheet = approximately **25 independently usable panels**. Each cell should be conceived as its own illustration, not one continuous 25-panel scene.

Production can run in waves of 3–5 sheets. A longer ambition of roughly 20 sheets / 500 raw panels is acceptable before rejects/dedup, but work in manageable validated batches.

## Batch loop

1. inspect actual current reader image counts
2. identify next 25 highest-value coverage slots from the generated backlog
3. read authoritative manuscript scenes and candidate briefs
4. validate paragraph anchors before generation readiness
5. select distinct visual moments
6. construct panel prompts using `VISUAL_BIBLE.md`, scored character visual references, and generated prompt packs
7. generate 5x5 sheet
8. review cells with loose KEEP/RETRY standard
9. crop KEEP panels deterministically
10. record/update registry mapping and known visual metadata
11. integration skips RETRY
12. place KEEP art at a natural paragraph break
13. verify chapter path, image path, aspect ratio, continuity, alt text, and mobile presentation
14. update coverage, character-reference, audit, anchor, and continuity-report state
15. repeat

## Panel selection

Prefer physical action, entering/leaving, work, stagecraft, environmental motion, unusual camera opportunities, relationship action rather than posed conversation, meaningful props, directional magic, comedy/recovery, and strong place identity.

Avoid generating 25 variants of people standing face-to-face.

## Composition diversity

Across a sheet, vary distance, camera height, direction of travel, number of people, foreground presence, interior/exterior, quiet/action, stage/backstage/audience, and lighting/weather where supported.

The Greg above-waist default is a continuity safeguard, not an excuse for repeated passport-photo composition. Use over-shoulder, profile, three-quarter, foreground obstruction, hands/work surfaces, high/low camera, entering/leaving frame, and environmental staging while keeping unnecessary lower-body state out of frame.

Reference selection should reinforce the same principle. Prefer a small set that stabilizes identity while spanning useful angles/poses rather than three nearly identical face references.

## Manifest / registry

Retain deterministic mapping between candidate, prompt pack, sheet, panel number, chapter, manuscript moment, KEEP/RETRY, output filename, insertion location/paragraph anchor, and useful notes.

Development contact sheets remain DEVELOPMENT until accepted panels are promoted.

## Approval ledger

Generated assets do not become live merely because the file exists.

`state/visual/ILLUSTRATION_APPROVALS.json` records an explicit decision for the generated asset:
- `decision: approve` requires the normal fit judgment, alt text, and optional caption
- `decision: reject` requires a short reason and marks that generation attempt rejected without publishing it

Rejected attempts remain useful production history. A rejection must not block a later deterministic version of the same scene candidate. Candidate-status synchronization therefore records the rejected attempt while leaving that prompt-ready scene retryable.

## Integration

Preferred art path convention where compatible with current repo:
`visual/chapter_art/CCC/ChCCC_<batch-or-role>_<panel>.jpg`

Do not overwrite unrelated art. Do not delete old art first. Add coverage; replace only clearly wrong or materially inferior work.

Paragraph anchors remain safety boundaries. Automated placement may tolerate harmless HTML whitespace around the exact anchor, but it must still refuse missing or ambiguous anchors rather than guessing where art belongs or rewriting prose.

## Quality threshold

Production-first. Accept normal variation in facial proportions, rendering detail, clothing folds, lighting, and style texture. Retry major continuity/anatomy/manuscript failures only. See `VISUAL_BIBLE.md`.

## Reader sizing

Low-resolution art should display at sensible intrinsic size. Stronger/high-resolution feature art may display larger. Mixed fidelity is intentional. No universal full bleed.

## Coverage report

Coverage should expose not only image counts but production state. Distinguish:
- candidate exists but still needs a prompt pack
- prompt ready / generation ready
- generated and awaiting approval
- approved but unpublished
- rejected generation attempts
- zero-art chapters with no active candidate at all

Also expose short actionable chapter previews for:
- zero-art chapters that still need scene discovery
- prompt-ready chapters ready for generation
- chapters with generated assets waiting for approval

That last view converts the report from a scoreboard into a routing surface: the next worker can immediately tell whether to discover scenes, generate, review, or integrate.

## After each wave

Report panels generated, KEEP/RETRY, chapters improved, zero/one/two/three+ image counts when available, approved-but-unpublished count, unmanaged legacy migration debt, character-reference audit issues, paragraph-anchor issues, character-continuity diversity gaps, major continuity problems, and next 25 slots.

Leave a fresh-worker handshake that points back to GitHub state rather than embedding batch history.
