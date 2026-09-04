# PEG-LEG GREG - REPOSITORY / ASSET AUDIT

Audit date: 2026-08-31  
Audited authority: `main` at `a0f0ce5` after rebasing concurrent manuscript/editorial work  
Generated evidence:

- `publishing/repository_inventory.json`
- `publishing/image_asset_manifest.json`
- `publishing/chapter_art_coverage.json`

This is a non-destructive archaeology pass. Metrics locate review targets. They
are not aesthetic scores and do not authorize deletion.

## Authority map

### Active authority

- Worker routing: `AGENTS.md`
- Project authority: `state/PROJECT_STATE.md`
- Story endpoint and current canon: `state/MANUSCRIPT_STATE.md`
- Forward workflow: `state/MANUSCRIPT_WORKFLOW.md`
- Book 1 exact authority: `state/manuscript/Peg_Leg_Greg_authoritative_ch82_final_name_map.docx`, Chapters 1-82
- Locked Book 2 source: `state/manuscript/Peg_Leg_Greg_Book2_Manuscript_Ch83-137.docx`, Chapters 83-137
- Exact continuation: `state/manuscript/Peg_Leg_Greg_Running_Manuscript_Ch138-155.md`, Chapters 138-155
- Recovered exact block: `state/manuscript/Peg_Leg_Greg_Recovered_Ch156-219_EXACT.md`, Chapters 156-219
- Permanent forward manuscript: `state/manuscript/Peg_Leg_Greg_Running_Manuscript.md`, Chapters 220-231 at audit time
- Writable 04 continuation: `state/editorial/Peg_Leg_Greg_Heavy_Edit_Continuation.md`, completed through Chapter 181 at audit time
- Lane brains and handoffs: `MANUSCRIPT_*`, `WRITERS_ROOM_STATE.md`,
  `STORY_CONTROL_STATE.md`, `EDITOR_STATE.md`, `PROSE_PLAYBOOK.md`,
  bibles, plot/open-thread files, specialist audits, and
  `HANDSHAKE_PROTOCOL.md`

### Active support

- Illustrated reader: `index.html`, `chapters/001.html` through
  `chapters/155.html`, `assets/reader.css`
- Light/current reader: `light.html`, `assets/light-reader.js`
- Forward preview support: `latest.html`, `chapters/220.html`,
  `chapters/224.html`, `assets/manuscript-preview.js`
- Promoted chapter art: `visual/chapter_art/`
- Visual references/maps/homepage: `visual/reference/`, `visual/maps/`,
  `visual/homepage/`
- Publishing manifests and scripts

### Historical - keep pending deliberate cleanup

- Range-stamped manuscript predecessors in `state/manuscript/`
- `state/manuscript/history/`
- Older QA/reconciliation/manuscript manifests
- Development contact sheets and visual-production sources

These files may be superseded operationally while retaining provenance or
unique recovery value. No manuscript material is a deletion candidate in this
pass.

## Can GitHub replace routine ZIP handoffs?

Yes for routine continuation of every active lane.

A fresh worker with repository access, `AGENTS.md`, and current `main` can
reconstruct:

- manuscript authority and exact range boundaries;
- 01 forward production;
- 02 Writers' Room;
- 03 Story Control;
- 04 method, edited Chapter 181, and the next editorial edge;
- reader and Light Reader architecture;
- visual production method and promoted assets;
- character, setting, plot, research, and specialist continuity;
- branch/PR handoff behavior.

Git history preserves accepted code, state, and committed assets across prior
reader generations. A full checkout ZIP adds no routine handoff value when it
contains only a historical Git checkout.

### Remaining archival/editorial gap

`Peg_Leg_Greg_Heavy_Edit.md` remains the frozen external checkpoint containing
completed heavy edits for Chapters 138-180. GitHub now contains the writable
continuation beginning with completed Chapter 181, so 04 can continue from
GitHub alone. GitHub does not yet contain the earlier edited 138-180 prose.

Recommendation: **B, controlled migration to the existing clear GitHub
editorial path.** In a separate change, transfer only the completed edited
Chapters 138-180 into the established 04 editorial stream or a clearly linked
frozen editorial checkpoint. Do not copy the unedited later source chapters
merely because they are present in the Library file.

Keep the Library original until byte count, checksum, chapter headings, current
edge, and editor workflow are verified. Do not merge it casually into the
forward manuscript.

## Manuscript overlap safety

The audit extracts actual chapter headings, including written-number headings
inside DOCX files:

| File | Exact heading range | Role |
| --- | ---: | --- |
| Book 1 final name-map DOCX | 1-82 | Active authority |
| Book 2 light-ship DOCX files | 83-92, 83-97, 83-105 | Historical predecessors |
| Book 2 authoritative DOCX | 83-113 | Historical/locked predecessor |
| Book 2 manuscript DOCX files | 83-123, 83-137 | Ch83-137 file is locked authority |
| Running Markdown predecessors | 138-152, 138-155 | Ch138-155 is exact active continuation |
| Recovered exact Markdown | 156-219 | Active recovery authority |
| Permanent running Markdown | 220-231 | Active forward authority |

The ranges are continuous without reconstruction, but they are intentionally
split across formats. Filename overlap does not prove prose equality. Do not
delete any manuscript file until exact text and authority roles are reviewed
separately.

## Repository and image storage

- Working-tree files inventoried: 730
- Working-tree bytes excluding Git metadata and generated audit outputs:
  approximately 352.1 MB decimal, roughly 336 MiB
- Git packed object storage: approximately 287 MiB
- Images: 447 files, approximately 342.5 MB decimal
- Referenced images: 352 files, approximately 212.0 MB
- Images not currently surfaced by code: 95 files, approximately 130.5 MB
- Exact duplicate hash groups: 56 groups across 131 files
- Maximum exact repeated bytes if one copy per hash were retained: about
  44.4 MB. This is an upper bound, not a deletion recommendation.

Most storage is visual. That does not make visual history disposable. The
larger architectural waste is repeated 40-180 MB full-project ZIP uploads
outside Git, which multiply the same repository into several gigabytes.

## Art coverage

- 157 chapter HTML pages inspected
- 150 pages have multiple images
- 5 pages have one image: Chapters 133-137
- 2 pages have no art: preview Chapters 220-221
- Maximum images on one chapter page: 4
- Broken image references: 0
- Reader-referenced nonexistent assets: 0

The zero-art result does not mean missing prose. Chapters 220-221 are forward
preview shells by design. Chapters 156-219 render through the Light Reader and
do not have static illustrated pages.

## Technical image findings

- 195 images trigger a conservative low-resolution flag
- 63 images are at least 3 MB
- 7 images have extreme aspect ratios
- 95 images are unused by current reader/code references

These are technical review flags only. A small sketch can be artistically right.
A 3 MB source can be worth preserving while the reader later serves a generated
derivative.

The largest unused families are:

- `visual/production/`: 72 files, about 70.4 MB
- `visual/development/`: 14 files, about 44.2 MB
- duplicate harvested source files: about 15.0 MB
- two unreferenced files under `visual/chapter_art/`: review required

Many harvested and standalone sources are byte-identical to promoted chapter
art. Those are strong later cleanup candidates, but provenance and generation
workflow should be reviewed before deletion.

## Reader presentation and performance

Current strengths:

- all 348 chapter-image tags have alt text;
- all use lazy loading;
- the final CSS cascade keeps raster art at intrinsic width and prevents small
  images from being stretched to role maximums;
- mobile art uses intrinsic height;
- no broken image path was found.

Current debt:

- 301 chapter images lack explicit width/height attributes, so browsers cannot
  reserve exact aspect-ratio space before metadata arrives;
- 204 lack `decoding="async"`;
- `reader.css` contains several historical image/mobile override layers before
  the final correct cascade;
- the reader downloads original PNG/JPEG sources because no derivative or
  `srcset` pipeline exists;
- 38 referenced images are at least 3 MB and are optimization candidates.

Recommended next performance work is non-destructive:

**SOURCE IMAGE -> GENERATED WEBP/JPEG DERIVATIVES -> WIDTH/HEIGHT + SRCSET ->
READER SELECTS APPROPRIATE FILE**

Do not overwrite the only source image. Build a reproducible derivative command
and apply it in a separate performance PR after this audit.

## Cleanup candidates

### Safe/high confidence after review

- Exact byte duplicates where one copy is promoted chapter art and another is a
  staging/harvest copy, provided no manifest/script requires the staging path.
- Stale tests and documentation that describe the old 155-only file count or
  the former 156-219 gap.

### Probably safe - human review

- Rejected visual-production files explicitly named as rejected/wrong scene.
- Development contact sheets after confirming every accepted crop/source needed
  for future work is preserved.
- Old QA and publishing manifests whose generator and replacement are proven.
- Unreferenced files under `visual/chapter_art/`.

### Keep

- All active manuscript authority and recovered exact prose.
- All durable lane state and specialist audits.
- Reader code and promoted art.
- Visual canon/reference assets.
- Git history.
- Development/source art until provenance is reviewed.

### Unknown/review required

- Whether every `visual/production/` asset is a disposable candidate or a
  unique source generation.
- Whether external visual ZIPs contain high-quality uncommitted source art.
- Whether every historical DOCX is textually contained in stronger authority.

## Art replacement queue

The machine-readable image manifest separates technical flags from artistic
review. It can drive:

- HIGH TECHNICAL PRIORITY: broken references, unreadable dimensions, or severe
  low-resolution display risk;
- OPTIMIZE: referenced files at least 3 MB;
- REPLACE LATER: technically low resolution, subject to human art review;
- UNUSED - REVIEW: no current code reference;
- KEEP: no current technical action.

Mass image generation should remain paused. Existing art already covers every
illustrated chapter, and presentation/performance/provenance work has higher
leverage.
