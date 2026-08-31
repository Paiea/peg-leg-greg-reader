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

## 5x5 contact-sheet default

One contact sheet = approximately **25 independently usable panels**. Each cell should be conceived as its own illustration, not one continuous 25-panel scene.

Production can run in waves of 3–5 sheets. A longer ambition of roughly 20 sheets / 500 raw panels is acceptable before rejects/dedup, but work in manageable validated batches.

## Batch loop

1. inspect actual current reader image counts
2. identify next 25 highest-value coverage slots
3. read authoritative manuscript scenes
4. select distinct visual moments
5. construct panel prompts using `VISUAL_BIBLE.md`
6. generate 5x5 sheet
7. review cells with loose KEEP/RETRY standard
8. crop KEEP panels deterministically
9. record manifest
10. integration skips RETRY
11. place KEEP art at a natural paragraph break
12. verify chapter path, image path, aspect ratio, continuity, and mobile presentation
13. update coverage state
14. repeat

## Panel selection

Prefer physical action, entering/leaving, work, stagecraft, environmental motion, unusual camera opportunities, relationship action rather than posed conversation, meaningful props, directional magic, comedy/recovery, and strong place identity.

Avoid generating 25 variants of people standing face-to-face.

## Composition diversity

Across a sheet, vary distance, camera height, direction of travel, number of people, foreground presence, interior/exterior, quiet/action, stage/backstage/audience, and lighting/weather where supported.

## Manifest

Retain deterministic mapping between sheet, panel number, chapter, manuscript moment, KEEP/RETRY, output filename, insertion location/paragraph anchor, and useful notes.

Development contact sheets remain DEVELOPMENT until accepted panels are promoted.

## Integration

Preferred art path convention where compatible with current repo:
`visual/chapter_art/CCC/ChCCC_<batch-or-role>_<panel>.jpg`

Do not overwrite unrelated art. Do not delete old art first. Add coverage; replace only clearly wrong or materially inferior work.

## Quality threshold

Production-first. Accept normal variation in facial proportions, rendering detail, clothing folds, lighting, and style texture. Retry major continuity/anatomy/manuscript failures only. See `VISUAL_BIBLE.md`.

## Reader sizing

Low-resolution art should display at sensible intrinsic size. Stronger/high-resolution feature art may display larger. Mixed fidelity is intentional. No universal full bleed.

## After each wave

Report panels generated, KEEP/RETRY, chapters improved, zero/one/two/three+ image counts when available, major continuity problems, and next 25 slots.

Leave a fresh-worker handshake that points back to GitHub state rather than embedding batch history.