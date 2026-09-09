# R2 Listening Shelf Art Drop

This folder is the stable repository destination for the larger image binaries used by the public Greg, Again listening shelf.

## Naming

- Hero art: `listening-edition-hero.webp`
- Chapter art: `chapter-NNN.webp`, using the zero-padded audio chapter number, for example `chapter-001.webp`.

Keep chapter art associated by stable audio identity (`ga-NNN`), never by mutable chapter title.

## Fast local workflow

For chapter art, the normal path is deliberately simple:

1. Put approved WebP files in this folder using `chapter-NNN.webp`.
2. From the repository root, run:

```bash
python scripts/sync_r2_listening_art.py
```

The helper reads the current audio manifest, matches each conventional filename to its real `ga-NNN` identity, and updates only the matching `image_src` entry in `../../presentation.json`.

It preserves existing quote and alt metadata, ignores filenames that do not correspond to a current audio chapter, and does not touch the audio manifest or audio binaries. That keeps manual large-file uploads cheap without making the public page probe for nonexistent images.

The hero remains configured by the `hero` entry in `presentation.json`; dropping `listening-edition-hero.webp` at the conventional path satisfies the existing hero mapping.

## Optional presentation metadata

`presentation.json` remains the place for presentation-only details such as a source-grounded alt description or an approved exact chapter quote.

Example after syncing and editorial metadata are both present:

```json
{
  "chapters": {
    "ga-001": {
      "image_src": "assets/art/chapter-001.webp",
      "alt": "Source-grounded description of the Chapter 1 image.",
      "quote": "Optional exact approved quote from the chapter."
    }
  }
}
```

Do not duplicate title, duration, publication state, or audio source here. Those stay authoritative in the audio manifest.

## Publication rule

Audio publication never waits on art. A published chapter with no image or presentation entry must remain fully playable as a text-first card.

Large image binaries can be generated, reviewed, converted to WebP, and uploaded manually to this folder. The sync helper handles conventional chapter image registration afterward.
