# R2 Website Design

**Status:** Design direction approved; written spec pending user review before implementation planning

## Purpose

R2 is Run 2 of Peg-Leg Greg: the same story lineage, started again with the lessons learned from the first run.

The website must make that lineage legible without turning the reading experience into a development dashboard.

Core reader promise:

> Greg has had two lives so far. So has his story.

Supporting project idea:

> Each run remembers previous lives. It only has to live its own.

R2 is audio-first, with a written rendition and illustrations rendered from the same underlying story state.

The website should explain that process clearly at the project level, then disappear into the background once the reader enters a chapter.

## Product Positioning

### Run 1

Run 1 is the original Peg-Leg Greg project and reader.

It is not deprecated, erased, or treated as a failed version. It is preserved as the first run and as the experiment that taught the project what worked.

The site may describe Run 1 in compact terms such as:

> The first life of the project. Hundreds of chapters, an illustrated reader, and the experiment that taught us what this story wanted to be.

### Run 2

R2 is the active second run.

It keeps the story lineage but is free to diverge from Run 1.

R2 should be described as:

- more tightly centered on Greg's experience
- built for listening first
- rendered into writing and images from the same story state
- informed by Run 1 without being required to repeat it

A compact public-facing explanation:

> Peg-Leg Greg was written once already. R2 starts over with everything that first run taught us, without requiring the new story to follow the same path.
>
> This run is built for listening first, then rendered into writing and images from the same story underneath.

## Architecture Decision

R2 gets its own reader surface and content structure under `/r2/`.

Run 1 remains intact while R2 is built.

Do not replace the established root reader in place during the initial R2 build.

Initial high-level structure:

```text
/r2/
  index.html
  chapters/
  data/
  content/
  assets/
  gallery/
```

R2 owns its own:

- chapter manifests
- audio assets
- written renditions
- image assets
- visual state
- production registry

This avoids coupling the new system to the older reader's accumulated publishing machinery.

## Reader Experience

The visible experience should remain simple:

- Listen
- Read
- Look
- Continue

The backend may be sophisticated. The reader should not feel like an admin tool.

R2 keeps the established project preference for a clean, readable, warm, book-like interface. Art provides atmosphere and personality; UI chrome stays restrained.

Avoid:

- game-wiki styling
- dashboard presentation
- progress-stat clutter
- giant technical labels
- glowing fantasy UI
- backend status language in public chapter pages

## Homepage

### Hero

Primary identity:

```text
R2
RUN 2

Greg has had two lives so far. So has his story.
```

Use strong R2 hero art featuring an early-run Greg who reads clearly young, not middle-aged.

Primary actions:

- Listen
- Read
- Continue

Secondary action:

- Browse Chapters

Optional small flavor line:

> Peg-Leg Greg, again.

### Process Explanation

The homepage should contain a short explanation of the experiment, but not technical implementation details.

Recommended language direction:

> Peg-Leg Greg was written once already. R2 starts over with everything that first run taught us, without requiring the new story to follow the same path.
>
> This run is built for listening first, then rendered into writing and images from the same story underneath.

The goal is transparency and identity, not self-congratulation or engineering exposition.

### Current Story

Show the latest/current chapter with simple Listen and Read entry points.

### Recent Art

Show a restrained strip or grid of 3 to 6 approved R2 images.

### Run Lineage

Include a compact comparison block:

```text
RUN 1
Peg-Leg Greg
The first life of the project.
Explore Run 1

RUN 2
R2
The active second run.
Start R2
```

Run 1 should be visible but subordinate to R2.

## About R2

The About page may explain the process more fully.

It should cover:

- why this is called Run 2
- what Run 1 taught the project
- that R2 is not obligated to recreate Run 1
- audio-first design
- shared story truth underneath audio, written rendition, and images
- why continuity systems exist
- why illustrations are being rebuilt from the beginning

The About page should stay readable for normal readers. Internal schema names and repository mechanics should remain out of public-facing copy unless they genuinely improve understanding.

## Chapter Experience

Once the reader enters a chapter, project/process explanation largely disappears.

Chapter page order:

1. R2 identity / chapter header
2. audio player
3. anchor image when available
4. written rendition
5. support / texture images
6. previous / next / contents navigation

The chapter page should feel like the novel, not an experiment log.

## Audio-First Behavior

Audio is the primary experiential rendering.

The audio player should be visually prominent and easy to use.

Initial controls:

- play / pause
- seek
- current time
- total duration
- playback speed if easy to support

Later enhancements may include persistent playback and saved position, but they are not required for the first build.

If audio is missing, the chapter still renders normally with a quiet fallback message.

## Written Rendition

Written text should remain independent from page markup, preferably stored as Markdown or another simple exact-text source.

The written rendition is a sister rendering of the same story truth, not merely a transcript of audio.

Reader priorities:

- comfortable measure
- strong mobile readability
- clear paragraph rhythm
- restrained styling

## Images

R2 starts a fresh visual layer rather than inheriting Run 1 artwork as visual authority.

Run 1 artwork may remain reference evidence when genuinely useful, but R2 visual continuity is built from R2-approved assets.

Default chapter image policy:

- minimum: 1
- normal target: 2
- optional third when it adds distinct value

Roles:

- anchor
- support
- texture

Do not create redundant images of the same beat merely to hit a count.

The image system should prioritize continuity across Greg, recurring characters, locations, props, and project style.

## Visual Style

R2 may use realistic, semi-realistic, painterly, or illustrated rendering if that best serves the book.

Style should be chosen because it fits R2, not mainly because it hides generation errors.

The current direction is grounded, mature, atmospheric, readable, lived-in, and restrained.

Early Greg should read visibly young even when weathered or physically burdened.

Hero/site mood art is not automatically character canon.

## Data Model

The site should be manifest-driven rather than discovering structure by scanning folders.

Recommended responsibilities:

```text
production registry
  -> what work remains

chapter manifest
  -> what the public site should display

content files
  -> audio, written rendition, images

visual state
  -> continuity evidence for future image generation
```

Production state and published presentation state must remain separate.

## Suggested R2 Structure

```text
r2/
  data/
    project.json
    chapter-registry.json
    chapters/
      ch001.json
      ch002.json

  content/
    written/
      ch001.md
      ch002.md

    audio/
      ch001.mp3
      ch002.mp3

    images/
      ch001/
      ch002/

  visual-state/
    characters/
    locations/
    objects/
    style/

  image-plans/
  image-batches/

  assets/
    css/
    js/
    ui/

  gallery/
  chapters/
  index.html
```

Exact paths may adapt to current repository constraints, but responsibility boundaries should remain stable.

## Chapter Manifest

Each published chapter should have one authoritative presentation manifest containing at minimum:

- chapter ID
- display number
- title
- publication status
- written path/status
- audio path/status
- ordered images with roles
- previous / next navigation IDs

Stable IDs should follow predictable conventions such as:

```text
r2-ch001
r2-ch001-s01
r2-ch001-img01
```

Do not casually rename stable IDs.

## Navigation

Navigation order comes from structured chapter data, not filename arithmetic.

This allows chapters to be inserted, hidden, reordered, or grouped into Books/Acts later without breaking navigation.

## Gallery

Gallery v1 remains simple:

- chronological grid
- optional chapter grouping

Do not build character/location filtering until enough approved R2 visual metadata exists to justify it.

## Run 1 Access

Run 1 remains available throughout the R2 build.

Initial implementation should link back to the existing reader rather than migrate Run 1 into the R2 structure.

If R2 later becomes the primary public entry point, the repository root may become a small project landing page that strongly favors R2 while preserving a quieter route to Run 1.

That migration is a later decision, not part of the initial R2 site build.

## Backend / Worker Ergonomics

R2 should be easier for future workers and tools to inspect than the legacy reader.

Rules:

- one obvious location for each asset type
- deterministic paths
- manifest-first structure
- no important state living only in chat
- no hand-maintained unique HTML per chapter if one reusable renderer/template can serve the same purpose
- preserve simple static hosting unless complexity is clearly earned

The site should remain simpler than the system underneath it.

## Error / Missing-Asset Behavior

A missing optional rendering must not break a chapter.

Examples:

- no audio -> show written rendition and quiet audio-unavailable text
- no image -> render chapter without an empty broken-image frame
- no support image -> anchor image only

Invalid required chapter metadata should fail visibly during validation rather than silently producing incorrect navigation.

## Testing

Initial implementation should verify:

- project manifest parses
- all published chapter manifests parse
- referenced written/audio/image paths resolve when marked published
- previous / next navigation matches structured order
- chapter pages render with audio missing
- chapter pages render with images missing
- chapter pages render on narrow/mobile layouts
- Run 1 links remain intact
- existing root reader remains unchanged during initial R2 build

## Initial Build Scope

Build now:

- `/r2/` foundation
- R2 naming and lineage language
- homepage
- About page
- project manifest
- chapter registry
- chapter manifest format
- reusable chapter reader
- audio-first chapter UI
- written rendition support
- image support
- chapter browser
- simple gallery
- responsive styling

Do not build yet:

- accounts
- comments
- database
- social features
- lore wiki
- complex search
- giant filters
- custom streaming backend
- heavy client framework
- root-site migration from Run 1 to R2

## Definition of Done

R2 site v1 is complete when:

1. `/r2/` clearly presents Run 2 and its relationship to Run 1.
2. A reader understands the audio-first / written / illustrated process without reading technical documentation.
3. A reader can enter the current story quickly through Listen or Read.
4. Chapter pages work with audio, writing, and one to three images.
5. Missing optional media degrades cleanly.
6. Navigation is manifest-driven and deterministic.
7. New chapters can be added primarily by adding content and updating structured data.
8. Future workers can locate production state and assets without reverse-engineering HTML.
9. The old Run 1 reader remains intact.
10. The public reading experience feels like a deliberate book, not a development interface.

## Core Principle

R2 remembers Run 1 without being trapped by it.

The reader sees a story.

The project quietly carries the lessons underneath.
