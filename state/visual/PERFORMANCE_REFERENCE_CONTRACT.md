# PERFORMANCE Reference Contract for Illustration

## Authority

Canonical prose remains the visual and story authority.

A successful PERFORMANCE archive under `state/editorial/performance-roundtrip/<chapter>/` is optional **derived visual evidence**. It is never required for illustration generation and never overrides the manuscript, scene-candidate ledger, paragraph-anchor validation, or the visual bible.

The useful distinction is:

- **CANON PROSE** says what is true.
- **SUCCESSFUL SCREENPLAY** may show one especially clear physical performance of that truth.

## Stable read path

Use `scripts.performance_roundtrip_references.load_visual_reference()` or `load_visual_references()`.

Do not read an archive's `visual_reference` directly without freshness validation. The helper returns visual evidence only when the scene-local final-prose anchors still match current canonical prose exactly once.

When a reference is missing or stale, treat it as absent.

## Generation queue

`build_generation_queue.py` may attach a fresh reference as the supplemental field:

```json
{
  "performance_reference": {
    "archive_path": "state/editorial/performance-roundtrip/007",
    "chapter": 7,
    "displayed_showcase_chapter": 5,
    "visual_reference": {
      "characters": ["Greg", "Antonius"],
      "location": "Antonius storeroom",
      "active_task": "...",
      "props": ["..."],
      "physical_beats": ["..."]
    }
  }
}
```

This field is read-only guidance. It must not automatically replace or mutate:

- candidate characters
- candidate location
- paragraph anchor
- candidate status
- generation readiness
- canon facts
- visual-bible constraints

## Useful visual evidence

A fresh successful screenplay may help a worker distinguish a meaningful physical beat from generic dialogue by clarifying:

- who is physically present
- action ownership
- blocking and movement
- active task
- meaningful props
- spatial relationships
- silent reactions
- physical scene endings
- character-specific physical behavior under the archived conditions

Examples from the initial archive include Antonius returning to the broom, Arlo shelving the fixture and protecting the notebook, and Hessa replacing beans and covering the bowl.

## Generation gate

Before generating an image, still read and validate the current canonical prose. PERFORMANCE evidence is supplementary composition/reference material only.
