# R2 DRIVE IMAGE STAGING

This file adds a practical staging layer to the existing image workflow.

It does not change visual canon, manuscript authority, reader placement rules, or the durable GitHub paths for accepted art.

## Default rule

For real R2 image work, use connected Google Drive as the normal human-facing staging surface when available.

Preferred staging path:

`02 PROJECTS / R2 / Images / 00 Inbox`

Optional reviewed holding path:

`02 PROJECTS / R2 / Images / Approved`

Do not hard-code Google Drive file or folder IDs into the repository. Resolve the connected Drive location at runtime.

## Authority split

- ChatGPT generation output is temporary until preserved.
- Drive is the durable review and handoff surface for candidates and approved source files.
- GitHub remains authority for accepted reader art, manifests, chapter placement, alt text, anchors, and production records.
- The public reader should not depend on Google Drive URLs for image delivery.

## Normal flow

**GENERATE -> SAVE TO DRIVE -> REVIEW -> PROMOTE WINNER -> INTEGRATE -> VERIFY**

1. Generate a bounded image or image batch.
2. Preserve project-relevant outputs in Drive instead of relying on chat history or the user's Downloads folder.
3. Give files stable human-readable names in Drive when useful. The user should not need to rename files manually for publication.
4. Keep rejected or exploratory work outside Git unless it has durable development value.
5. When an image is approved, fetch the raw Drive file and promote the exact bytes into the established GitHub visual path, normally `visual/chapter_art/` or another existing production destination.
6. Use the existing manifest-backed placement workflow, including `scripts/apply_image_batch.py`, when chapter insertion or batch placement is required.
7. Verify the promoted image path, chapter reference, intrinsic dimensions, alt text, anchor, desktop/mobile rendering, and production record.
8. After GitHub promotion is verified, Drive may retain the approved master for convenient human access. Temporary losers can be cleaned later.

## Assistant default

When the user asks for an image for an actual R2 chapter, character, location, cover, map, or production batch, treat Drive preservation as part of the job rather than requiring a separate download/rename/upload loop.

Random experiments do not need permanent storage unless the user chooses to keep them.

If the generation system cannot hand the image directly to Drive in the same turn, preserve it at the next available file handoff rather than asking the user to manually repackage it.

## Publication naming

Human-facing Drive names and machine-facing publication names do not need to match.

Drive may use names such as:

`Ch 037 - Greg at the river - approved.png`

GitHub may normalize the promoted asset to a deterministic production path such as:

`visual/chapter_art/ch037-river.png`

The publication system, not the user, should own that normalization.

## Failure fallback

If Drive is unavailable, use the existing temporary staging rule from `visual/IMAGE_WORKFLOW.md` and promote selected winners directly to GitHub when possible.

Do not fall back to full-repository ZIP handoffs for normal image production.

## Short rule

**DRIVE HOLDS THE WORKING IMAGE. GITHUB HOLDS THE ACCEPTED IMAGE. THE WEBSITE SHOWS THE ACCEPTED IMAGE.**
