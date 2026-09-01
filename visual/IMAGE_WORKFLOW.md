# PEG-LEG GREG — IMAGE WORKFLOW

Practical storage, curation, promotion, and cleanup policy for visual production.

This file complements:

- `state/VISUAL_BIBLE.md` — visual language and continuity
- `state/IMAGE_PRODUCTION.md` — coverage-first generation loop
- `visual/PRODUCTION_STATUS.md` — current production state

The goal is simple:

**DISCOVER → CURATE → PROMOTE → RECORD → CLEAN**

GitHub is the durable home for accepted visual work. Chat sessions, temporary local folders, and generation workspaces are disposable staging areas.

---

## Why this exists

The historical storage problem was not that the project contained illustrations.

The problem was repeatedly moving a growing repository through full ZIP checkpoints and chat/library handoffs. Each handoff duplicated the same large image payload again.

Normal image production should therefore use GitHub as the handoff instead of moving whole-repository archives between workers.

Preferred:

**CURRENT GITHUB → TEMPORARY DISCOVERY → SELECT WINNERS → PROMOTE TO GITHUB**

Avoid:

**FULL REPO ZIP → NEW CHAT → LARGER FULL REPO ZIP → NEXT CHAT**

Full-project ZIPs are recovery artifacts, not normal image workflow.

---

## Authority split

### GitHub keeps accepted work

Good long-term GitHub material includes:

- promoted chapter art
- approved standalone illustrations
- useful contact sheets
- batch manifests and records
- placement metadata
- alt text and paragraph anchors
- production-status notes
- visual workflow/state files

### Temporary staging keeps exploration bulk

Raw discovery material can remain temporary until selected:

- rejected generations
- near-duplicate candidates
- throwaway variations
- local export folders
- chat/library staging copies
- unselected standalone candidates

Do not preserve material permanently merely because it was generated.

---

## The 25-image discovery model

A 5×5 discovery board is the default high-throughput visual review unit.

There are two valid ways to arrive at one:

### A. One generated 5×5 sheet

Generate one contact/discovery sheet containing approximately 25 independently usable visual cells.

Then:

1. review the sheet
2. mark KEEP / RETRY / IGNORE
3. crop or regenerate selected winners
4. promote only useful standalone outputs
5. keep the sheet if it remains useful production evidence

This is storage-efficient because one sheet can represent a broad search space.

### B. Twenty-five standalone candidates

If the generation system produces separate images instead:

1. keep the 25 raw files in temporary staging
2. assemble one lightweight contact sheet
3. review the board
4. promote only selected winners into GitHub
5. delete temporary losers when no longer useful

Do **not** commit all 25 large standalone candidates merely so they can be reviewed if only a handful are likely to survive.

---

## Important Git-history rule

Deleting a large file from the current Git tree later does not remove the bytes from normal Git history.

Therefore:

**TEMPORARY BULK OUTSIDE GIT → WINNERS INTO GIT**

is better than:

**EVERYTHING INTO GIT → DELETE LOSERS LATER**

Development contact sheets are comparatively cheap and can be worth preserving. Large rejected standalone files usually are not.

This does not mean the repository must stay tiny. Useful accepted art belongs in GitHub. The goal is to avoid permanent storage of low-value exploratory bulk.

---

## Standard workflow

### 1. Choose a bounded target

Examples:

- Chapters 236–250
- one Act
- zero-art chapters
- weak-image replacements
- a character continuity study
- a homepage/map concept pass

The batch should have one clear production purpose.

### 2. Inspect actual reader coverage

Before generating, check the reader and current production records.

Priority remains:

1. zero-art chapters
2. one-image chapters
3. weak or mismatched art
4. second/third-image opportunities
5. replacements only when materially better

See `state/IMAGE_PRODUCTION.md` for the coverage loop.

### 3. Generate discovery material temporarily

Use the manuscript scene, `state/VISUAL_BIBLE.md`, and the production target to build the batch.

Prefer visual variety across:

- camera distance
- camera height
- direction of movement
- interior/exterior
- foreground objects
- quiet/action
- people count
- stage/backstage/audience
- environmental motion

Discovery is allowed to be broad. Permanent storage should be selective.

### 4. Build or keep the contact sheet

Use a numbered board whenever it makes review faster.

A useful board should make it easy to say things like:

- R2C4 KEEP
- R4C1 RETRY
- 07 promote for Ch241
- 19 useful composition, wrong continuity

The contact sheet is a review surface, not automatically reader art.

### 5. Curate deliberately

Classify candidates loosely:

- **KEEP / PROMOTE** — worth durable standalone use
- **RETRY** — useful scene idea with a major failure
- **DEVELOPMENT ONLY** — useful visual exploration but not reader-ready
- **IGNORE / DISCARD** — no durable value

Do not promote images simply because they exist.

### 6. Promote selected winners

Preferred durable destinations include:

- `visual/chapter_art/`
- `visual/production/standalone/`
- another established production path when appropriate

Use clear filenames and preserve chapter/scene identity.

Where a manifest-backed batch already exists, prefer `scripts/apply_image_batch.py` for copying, paragraph placement, contact-sheet assembly, and usage tracking.

### 7. Record enough provenance

For meaningful batches, preserve a compact manifest or record with useful fields such as:

- batch name
- date
- target chapter range
- purpose
- contact sheet path
- source-generation identifier when available
- panel/candidate number
- chapter
- scene/moment
- KEEP/RETRY decision
- promoted target path
- reader role
- alt text
- paragraph anchor
- continuity notes

The record should allow a future worker to understand the batch without reopening the original chat.

### 8. Integrate approved art

For reader-promoted art:

1. verify the target image exists in its durable path
2. place it at a natural paragraph break
3. preserve intrinsic dimensions
4. add meaningful alt text
5. use lazy loading where appropriate
6. verify desktop and mobile presentation
7. verify continuity against the actual manuscript scene
8. update relevant production status

Do not rewrite manuscript prose to accommodate an illustration.

### 9. Verify before cleanup

Before deleting temporary staging, confirm:

- winner exists in GitHub
- expected filename/path is correct
- reader reference resolves
- manifest/record points to the promoted copy
- contact sheet is retained if desired
- no unique source asset is about to be lost accidentally

### 10. Clean temporary bulk

Once promoted work is durable and verified:

- delete temporary raw candidates if no longer useful
- delete redundant chat/library staging copies when convenient
- delete local throwaway export folders
- do not create a full-repository ZIP merely as a normal handoff

Manual cleanup is acceptable. This workflow does not require elaborate automation for deleting temporary files.

---

## Folder intent

### `visual/chapter_art/`

Promoted chapter illustrations intended for reader use.

### `visual/production/standalone/`

Production-ready standalone outputs that may be promoted or referenced by publishing work.

### `visual/production/development/`

Production exploration worth retaining as development evidence.

### `visual/development/contact_sheets/`

Compact review boards and historical curation surfaces worth keeping.

### `visual/reference/`

Reference/style/continuity material that should not be mistaken for promoted reader art.

### `visual/PRODUCTION_STATUS.md`

Compact running record of current visual production and next coverage priorities.

---

## What is safe to keep

Do not become afraid of repository images merely because historical ZIP handoffs became large.

A useful promoted image in GitHub is doing real work.

The main storage discipline is:

- do not multiply the repository across chat ZIPs
- do not commit large rejected candidate piles by default
- do keep accepted reader art
- do keep compact records/contact sheets when they preserve useful provenance

---

## Human/tool split

Automation is helpful but not mandatory.

Good worker tasks:

- coverage audit
- batch planning
- prompt construction
- contact-sheet review
- filename/manifest preparation
- chapter-anchor selection
- reader integration
- verification

Good small human tasks when tool friction is higher than the value of automation:

- manually move selected winner PNG/JPG files into the requested GitHub folder
- use GitHub Desktop to commit/push those selected files
- delete temporary local/chat generation clutter later

A five-file manual promotion is better than rebuilding a brittle 300 MB ZIP handoff system.

---

## Default fresh-worker instruction

> Use the GitHub-first Peg-Leg Greg image workflow. Treat chat/local generation as temporary staging and GitHub as durable authority for accepted outputs. Prefer bounded 5×5 / ~25-image discovery, selective promotion of winners, manifest-backed placement where useful, and cleanup of temporary bulk after promotion is verified. Do not use full-project ZIPs as routine handoffs.

---

## Short rule

**GENERATE BROADLY. REVIEW CHEAPLY. PROMOTE SELECTIVELY. LET GITHUB REMEMBER THE WINNERS.**
