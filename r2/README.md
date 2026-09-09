# R2 Reader and Production Map

R2 is **Run 2** of Peg-Leg Greg.

This directory is the clean reader/publishing surface for the second run. Run 1 remains at the repository root and is intentionally separate.

## Public model

R2 presents one story through three sibling renderings:

1. **Listen** — audio-first narrative, the primary experiential rendering.
2. **Read** — written rendition from the same story truth, not a transcript.
3. **Look** — approved illustrations derived from the same scene/story truth.

The public site may explain the Run 1 → Run 2 lineage and process on the homepage/About page. Chapter pages should stay focused on the story.

## Where to look

```text
r2/
  data/
    project.json             # public project order/current chapter
    chapter-registry.json    # production state / unfinished work
    chapters/
      ch001.json             # public presentation manifest
      ch002.json

  assets/
    css/                     # R2-only presentation
    js/                      # manifest-driven site/chapter rendering
    images/                  # site/UI mood art only

  about/                     # public process/lineage explanation
  chapters/                  # public chapter browser
  gallery/                   # approved chapter-art browser
  chapter.html               # reusable chapter reader
  index.html                 # R2 homepage
```

## Authority boundaries

- `data/project.json` answers **what chapters exist publicly and in what order**.
- `data/chapters/chNNN.json` answers **what the public reader should display for that chapter**.
- `data/chapter-registry.json` answers **what production work remains**.
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
2. Create/update `data/chapters/chNNN.json`.
3. Add `r2-chNNN` to `data/project.json` in intended reading order and update `current_chapter` if appropriate.
4. Update previous/next IDs in neighboring chapter manifests.
5. Update `data/chapter-registry.json` with the actual production state.
6. Reference existing audio/written/image assets instead of duplicating them when a stable source already exists.
7. Run `python -m unittest tests.test_r2_site -v`.
8. Do not claim missing written/image output exists. The reader degrades cleanly when optional renderings are unavailable.

## Asset rules

### Audio

Current audio experiments live under `greg-again/audio/assets/` and may be referenced by R2 while that remains the current source. Do not duplicate large MP3 files only to satisfy directory symmetry.

### Written

Only mark `written.status` as `published` once a real R2 written rendition exists at the referenced path.

### Images

Chapter manifests contain only approved R2 chapter images. Mood/site artwork belongs under `r2/assets/images/` and stays separate from chapter visual canon.

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
