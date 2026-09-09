# R2 Reader and Production Map

R2 is **Run 2** of Peg-Leg Greg.

This directory is the clean reader/publishing surface for the second run. Run 1 remains at the repository root and is intentionally separate.

## Public model

R2 presents one story through three sibling renderings:

1. **Listen**: audio-first narrative, the primary experiential rendering.
2. **Read**: written rendition from the same story truth, not a transcript.
3. **Look**: approved illustrations derived from the same scene/story truth.

Before either Listen or Read becomes a medium-specific artifact, use the shared rendering contract in `PIPELINE.md`.

The default wording path is:

`Story State / Performance → Greg Experience → Shared Greg Surface → Audio Finish / Written Finish`

Audio and written are sibling medium-specific finishes from the same Shared Greg Surface. Do not use written prose as a mandatory source transcript for audio, and do not treat audio wording as a transcript that must later be rewritten back into prose.

The public site may explain the Run 1 → Run 2 lineage and process on the homepage/About page. Chapter pages should stay focused on the story.

## Where to look

```text
r2/
  PIPELINE.md                 # shared Greg surface / medium finishing contract
  IMAGE_SYSTEM.md             # R2 visual authority + production architecture
  IMAGE_WORKER.md             # disposable one-chapter image worker engine
  IMAGE_RELEASES.md           # large ChatGPT Library release packaging
  visual-state/
    R2_VISUAL_CANON.md        # compact current style/identity/location authority
  image-packets/
    TEMPLATE.md               # reusable one-transaction image contract
    PACKET_001.md             # bootstrap Greg/Carrow/Chapter 1 packet

  data/
    project.json              # public project order/current chapter
    rendering-pipeline.json   # machine-readable rendering route
    chapter-registry.json     # production state / unfinished work
    chapters/
      ch001.json              # public presentation manifest
      ch002.json

  assets/
    css/                      # R2-only presentation
    js/                       # manifest-driven site/chapter rendering
    images/
      site/                   # homepage/site mood art
      continuity/             # approved internal visual anchors after repo drop
      chapters/               # approved chapter-specific art after repo drop

  about/                      # public process/lineage explanation
  chapters/                   # public chapter browser
  gallery/                    # approved chapter-art browser
  chapter.html                # reusable chapter reader
  index.html                  # R2 homepage
```

## Authority boundaries

- `data/project.json` answers **what chapters exist publicly and in what order**.
- `data/rendering-pipeline.json` answers **how one Greg-shaped wording surface forks into Listen and Read**.
- `PIPELINE.md` is the human worker contract for that same rendering route.
- `IMAGE_SYSTEM.md` answers **how R2 visual work is claimed, generated, reviewed, staged, released, verified, and integrated**.
- `IMAGE_WORKER.md` answers **how a fresh parallel chapter-image worker executes one transaction and stops**.
- `IMAGE_RELEASES.md` answers **how approved Library binaries become large repo-ready handoff ZIPs**.
- `visual-state/R2_VISUAL_CANON.md` answers **what current R2 image work should not have to rediscover**.
- `data/chapters/chNNN.json` answers **what the public reader should display for that chapter**.
- `data/chapter-registry.json` answers **what production work remains**.
- ChatGPT Library is a shared binary staging warehouse, not story or visual-canon authority.
- Audio, written, and image files are assets referenced by manifests. Folder scanning does not define story order.
- Run 1 prose/art does not automatically become R2 authority.
- Site hero/mood art does not automatically become character or scene canon.

## Stable IDs

Use predictable IDs and do not casually rename them:

```text
r2-ch001
r2-ch001-s01
r2-ch001-img01
```

The presentation filename for a chapter remains `data/chapters/ch001.json`, while its stable ID is `r2-ch001`.

## Add the next chapter

When Chapter N audio or another public rendering becomes real:

1. Confirm the newest GitHub authority first.
2. Confirm or create the chapter's Shared Greg Surface before medium-specific finishing unless the chapter is an explicitly documented legacy experiment.
3. Classify listen-back/page-read discoveries before revision: shared Greg Experience, audio-only, or written-only.
4. Create/update `data/chapters/chNNN.json`.
5. Add `r2-chNNN` to `data/project.json` in intended reading order and update `current_chapter` if appropriate.
6. Update previous/next IDs in neighboring chapter manifests.
7. Update `data/chapter-registry.json` with the actual production state.
8. Reference existing audio/written/image assets instead of duplicating them when a stable source already exists.
9. Run `python -m unittest tests.test_r2_site -v`.
10. Do not claim missing written/image output exists. The reader degrades cleanly when optional renderings are unavailable.

## Asset rules

### Audio

Current audio experiments live under `greg-again/audio/assets/` and may be referenced by R2 while that remains the current source. Do not duplicate large MP3 files only to satisfy directory symmetry.

Audio Finish is a light medium-specific finish from the Shared Greg Surface, not an independent rewrite of the chapter.

### Written

Only mark `written.status` as `published` once a real R2 written rendition exists at the referenced path.

Written Finish is a light medium-specific finish from the Shared Greg Surface. Clean performance residue without cleaning away cognition.

### Images

R2 image work must read `IMAGE_SYSTEM.md` and `visual-state/R2_VISUAL_CANON.md` before production.

Routine parallel chapter production should normally use `IMAGE_WORKER.md`:

> one fresh worker = one claimed chapter image transaction = stop

Routine constrained chapter workers may default to Instant. Higher-thinking workers are reserved for visual-canon decisions, new recurring identity/location anchors, repeated drift, ambiguous interpretation, major frontdoor art, or image-system architecture.

This is important because the root Run 1 `VISUAL_BIBLE.md` contains later-story visual continuity that **must not leak backward into early R2**. In particular, until R2 story authority establishes a leg loss, early R2 Greg has both legs intact and must not inherit Run 1 peg-leg/prosthetic/crutch state merely from the project title or old artwork.

Chapter manifests contain only approved **and repository-binary-verified** R2 chapter images. Mood/site artwork stays separate from chapter visual canon.

Preferred repository paths after release/drop:

```text
r2/assets/images/site/
r2/assets/images/continuity/
r2/assets/images/chapters/chNNN/
```

Use bounded image packets under `image-packets/`. Image count is not a quota: a chapter may use zero art, one strong anchor, or additional support images only when they add distinct value.

#### Shared ChatGPT Library staging

Parallel workers stage binaries under the existing persistent Library project shelf:

```text
/Peg-Leg Greg Image Integration/R2/
  00 Canon/
  01 Incoming/
  02 Approved/
  03 Releases/
  04 Released/
```

Workers should not hand Keoni a separate tiny ZIP after every normal chapter. Approved unreleased binaries accumulate in `02 Approved/`.

A separate release worker follows `IMAGE_RELEASES.md` and periodically packages a large repo-mirrored release, normally around 50 to 100 useful images or whenever Keoni asks. The completed release ZIP lives in `03 Releases/`; included source binaries move to `04 Released/` only after the release archive is safely stored.

Generated/edited image binaries still follow `state/IMAGE_BINARY_HANDOFF.md`.

Do not use the AI/GitHub binary-write path as the default transport for approved generated art after the corrupted R2 hero incident. The large release is the preferred human handoff boundary:

1. parallel workers stage approved binaries in ChatGPT Library
2. a release worker packages one repo-mirrored large ZIP
3. Keoni performs one large manual repository drop
4. AI re-reads and opens repository files to verify the actual bytes
5. only then should chapter manifests, gallery state, or live reader references point at the assets
6. highly visible site art should also be checked on the deployed page after merge

If generation does not expose safe bytes/file references for direct Library staging, mark `library_stage_pending` rather than pretending the output is staged.

Site art is `site_mood`, not Greg character canon unless a later explicit visual-authority decision promotes useful evidence from it.

## Reader principles

- Audio first, not audio only.
- Warm, readable, book-like presentation.
- Art supplies atmosphere; UI stays quiet.
- Missing optional media never breaks the chapter.
- Navigation comes from manifests, never filename arithmetic.
- No important production state should live only in chat.
- Prefer deterministic paths and small durable manifests over conversational archaeology.

## Run 1

Run 1 remains the original Peg-Leg Greg reader at the repository root. R2 links to it as lineage, not as a deprecated or failed version.

**R2 remembers Run 1 without being trapped by it.**