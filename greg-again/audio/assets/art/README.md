# R2 Listening Shelf Art Drop

This folder is the stable repository destination for the larger image binaries used by the public Greg, Again listening shelf.

## Naming

- Hero art: `listening-edition-hero.webp`
- Chapter art: `chapter-NNN.webp`, using the zero-padded audio chapter number, for example `chapter-001.webp`.

Keep chapter art associated by stable audio identity (`ga-NNN`), never by mutable chapter title.

## Wiring art into the shelf

The public renderer reads optional metadata from `../../presentation.json`.

Example:

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

The hero entry uses `assets/art/listening-edition-hero.webp`.

Do not duplicate title, duration, publication state, or audio source here. Those stay authoritative in the audio manifest.

## Publication rule

Audio publication never waits on art. A published chapter with no image or presentation entry must remain fully playable as a text-first card.

Large image binaries can be generated, reviewed, converted to WebP, and uploaded manually to this folder. After the binary exists, add only the matching stable-ID metadata to `presentation.json`.
