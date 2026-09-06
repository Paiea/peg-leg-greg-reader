# PEG-LEG GREG — ILLUSTRATION REASSIGNMENT RULES

Purpose: preserve useful art through structural manuscript edits without letting existing illustration investment dictate weak story structure.

## Core rule

**Illustrations belong to story beats and durable chapter identity, not permanently to a display number.**

A chapter being merged, cut, or renumbered does not automatically invalidate its art.

A chapter having art does not automatically protect it from compression.

## Illustration disposition categories

Every structurally affected illustrated chapter should receive one disposition:

### KEEP WITH CHAPTER
The chapter survives and the art still represents a surviving beat. Retain association with the stable chapter id.

### REASSIGN TO MERGED CHAPTER
The source chapter is absorbed, but the pictured beat survives in the merged destination. Move art association to the surviving stable id and preserve original provenance in metadata.

### REASSIGN AS ACT / SECTION ART
The exact chapter disappears but the image still represents a useful arc, location, relationship, or transition. Promote to act/section/interstitial use if composition still fits.

### RETAIN IN GALLERY / ARCHIVE
The image remains good project art but no longer accurately illustrates surviving chapter prose. Keep it discoverable without falsely attaching it to canon scene placement.

### RETIRE
The image depends on removed material, contradicts the surviving scene, or is no longer worth maintaining. Preserve historical record if useful, but do not publish as current chapter art.

## Art is evidence, not immunity

During compression mapping, note whether a chapter has approved/generated art and what scene the art actually depicts.

Do not write `KEEP because illustrated`.

Instead ask:
- Is the pictured beat itself worth preserving?
- If the chapter merges, can that beat survive naturally?
- Does the image represent a broader arc/location rather than a precise moment?
- Would retaining the image misrepresent the new prose?

## Stable identity migration

As the project adopts `state/CHAPTER_IDENTITY_MODEL.md`, illustration manifests should gradually resolve through stable chapter ids.

Preferred future association:

`image_asset -> stable_chapter_id -> current display number`

rather than:

`image_asset -> hard-coded chapter number`

Existing number-based manifests remain valid migration inputs until converted.

## Merge behavior

When Chapters A and B merge:
- identify which exact beats survive;
- list all approved art from both chapters;
- keep the strongest art whose depicted beat survives;
- allow multiple images on one surviving chapter if pacing/layout supports it;
- avoid duplicating near-identical art merely because both source chapters had images;
- preserve original source chapter metadata for audit.

## Cut behavior

Before cutting an illustrated chapter:
1. identify the image's depicted beat;
2. decide whether that beat moves elsewhere;
3. choose REASSIGN / ACT ART / GALLERY / RETIRE;
4. record the decision in the structural migration ledger;
5. do not delete source image files as part of manuscript compression unless a separate asset-cleanup pass authorizes it.

## Reader behavior

The public illustrated reader should eventually consume current chapter-to-art associations from a generated resolver/manifest rather than infer identity solely from file names.

That allows:
- chapter renumbering;
- merged chapter art reuse;
- old asset filenames to remain stable;
- gallery retention;
- redirects/aliases for old chapter URLs.

## Quality rule

A compression pass may reveal that a previously illustrated minor scene no longer deserves chapter-level placement while an unillustrated surviving scene does.

Do not preserve historical coverage ratios at the expense of better visual storytelling.

After structural editing, art coverage should be rebalanced around the surviving manuscript.

## Character-reference protection

Approved character-reference art used by the generation pipeline should not be retired merely because its original chapter is cut or merged.

Character reference utility is independent from publication placement.

If an image is both chapter art and a strong character reference:
- update publication association separately;
- retain reference-registry status unless the image itself is stale/bad/inconsistent.

## Final principle

**The manuscript decides what story survives. The art system decides how good visual work follows it.**