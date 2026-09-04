# Website Art Handoff

## Goal
Make each five-chapter illustration batch cheap to ship. Generation and website placement must share one durable manifest so nobody has to rediscover scenes or insertion points later.

## Batch workflow
1. Read exact prose for five chapters.
2. Add 1-3 planned slots per chapter to `visual/ILLUSTRATION_PLACEMENT.md`.
3. Generate single-scene images using `visual/ILLUSTRATION_STYLE.md` and `visual/VISUAL_CONTINUITY.md`.
4. Review each image against the generation packet and exact chapter.
5. Promote accepted assets to `visual/chapter_art/<chapter>/` with deterministic slot-oriented filenames.
6. Replace each slot's TBD asset path and mark it PROMOTED.
7. Run the project's existing asset audit / manifest regeneration process.
8. Rebuild Illustrated Reader chapter pages from current manuscript authority.
9. Verify every image reference resolves, chapter navigation remains intact, no prose was accidentally changed, and no em dash was introduced into manuscript prose.
10. Publish the clean batch and mark its placement slots LIVE.

## Naming
Prefer stable names such as `ch161_a_player_loft.<ext>` and `ch161_b_serra_note_exchange.<ext>` rather than generation IDs. The placement manifest is the semantic authority; generated IDs are disposable.

## Automation direction
The desired endpoint is a small publisher that reads the placement manifest and inserts promoted assets at recorded prose anchors. Until that exists, treat the manifest as machine-readable-enough structured Markdown and keep anchor wording exact. Do not hard-code visual placement only inside generated HTML.

## Safety rails
- Never promote a contact sheet as chapter art.
- Never promote an image solely because it looks good.
- Never overwrite accepted art without preserving the reason/state change.
- Never regenerate chapter prose from memory while adding images.
- Re-read current branch/main before publishing because manuscript and reader work may move in parallel.

## Definition of frictionless
After images are accepted, the website step should be mechanical: copy/promote assets, resolve manifest slots, regenerate, validate, publish. Creative decisions happen before handoff, not while editing HTML.