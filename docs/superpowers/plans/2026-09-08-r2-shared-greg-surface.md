# R2 Shared Greg Surface Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the Shared Greg Surface the durable default rendering pipeline for R2 without rewriting existing chapters or redesigning the site.

**Architecture:** R2 uses Story State / Performance to build Greg Experience, then one Shared Greg Surface feeds two light finishes: Audio Finish and Written Finish. A human-readable contract and a small machine-readable routing file become durable repo memory; the public project manifest points at that routing contract, and tests prevent the pipeline from regressing to independent written/audio rewrites.

**Tech Stack:** Markdown, JSON, Python `unittest`, existing static R2 reader/publishing manifests.

**Spec:** `docs/superpowers/specs/2026-09-08-r2-shared-greg-surface-design.md`

## Global Constraints

- Do not rewrite Chapters 1-16 as part of this change.
- Do not regenerate Chapters 1-3 audio.
- Do not redesign the R2 website.
- Do not impose lexical-overlap, pause, fragment, or dialogue quotas.
- Shared Greg Surface contains no provider-specific timing markup, SSML, or hidden acting directions.
- Audio Finish and Written Finish are light transformations of the Shared Greg Surface, not independent rewrites.
- Feedback must be classified as shared/Greg Experience, audio-only, or written-only before revision.
- Existing R2 public manifests and reader behavior remain backward compatible.

---

### Task 1: Add the shared-pipeline regression contract

**Files:**
- Modify: `tests/test_r2_site.py`

**Interfaces:**
- Consumes: `r2/data/project.json`, `r2/data/rendering-pipeline.json`, `r2/PIPELINE.md`, `r2/README.md`
- Produces: regression coverage proving the public R2 project points at a valid shared rendering contract.

- [ ] **Step 1: Add the pipeline assertions**

Require:

```python
project['rendering_pipeline'] == 'data/rendering-pipeline.json'
pipeline['schema'] == 'r2_rendering_pipeline/v1'
pipeline['shared_flow'] == [
    'story_state_or_performance',
    'greg_experience',
    'shared_greg_surface',
]
pipeline['renderers']['audio']['input'] == 'shared_greg_surface'
pipeline['renderers']['written']['input'] == 'shared_greg_surface'
pipeline['feedback_classes'] == [
    'shared_greg_experience',
    'audio_only',
    'written_only',
]
```

Also require `r2/PIPELINE.md` to contain:

- `Clean performance residue. Do not clean away cognition.`
- `Greg may own the linguistic surface.`
- `Audio Finish`
- `Written Finish`

And require `r2/README.md` to point workers at `PIPELINE.md`, `Shared Greg Surface`, and `medium-specific finish`.

- [ ] **Step 2: Run the focused test**

Run:

```bash
python -m unittest tests.test_r2_site.R2SiteTests.test_r2_declares_shared_greg_surface_pipeline -v
```

Expected: PASS once Tasks 2-3 are present.

---

### Task 2: Add durable human and machine pipeline memory

**Files:**
- Create: `r2/PIPELINE.md`
- Create: `r2/data/rendering-pipeline.json`
- Modify: `r2/data/project.json`

**Interfaces:**
- Consumes: approved design spec.
- Produces: human-readable worker contract and machine-readable renderer routing contract.

- [ ] **Step 1: Create `r2/data/rendering-pipeline.json`**

Use:

```json
{
  "schema": "r2_rendering_pipeline/v1",
  "shared_flow": [
    "story_state_or_performance",
    "greg_experience",
    "shared_greg_surface"
  ],
  "renderers": {
    "audio": {
      "input": "shared_greg_surface",
      "output": "audio_finish",
      "role": "light_medium_finish"
    },
    "written": {
      "input": "shared_greg_surface",
      "output": "written_finish",
      "role": "light_medium_finish"
    }
  },
  "feedback_classes": [
    "shared_greg_experience",
    "audio_only",
    "written_only"
  ],
  "rules": {
    "clean_performance_residue_not_cognition": true,
    "greg_owns_pov_not_causal_universe": true,
    "outside_language_may_be_state_changing": true,
    "medium_finishes_may_not_add_story_facts": true,
    "provider_markup_in_shared_surface": false
  },
  "similarity": {
    "heuristic_lexical_overlap_percent": [90, 97],
    "hard_gate": false
  }
}
```

- [ ] **Step 2: Create `r2/PIPELINE.md`**

Document:

```text
STORY STATE / PERFORMANCE
        ↓
GREG EXPERIENCE
        ↓
SHARED GREG SURFACE
      ↙       ↘
AUDIO FINISH   WRITTEN FINISH
```

Lock the rules:

- `Clean performance residue. Do not clean away cognition.`
- `Greg may own the linguistic surface. He may not steal another character's thought.`
- Shared Greg Surface is close to publishable prose and speakable audio.
- Audio Finish may split breath units, isolate real cognitive pauses, make one-pass clarity changes, and add only rare cognition-shaped resets.
- Written Finish may recombine excessive breath fragments, normalize punctuation, and improve page rhythm without conventionalizing Greg away.
- Listen-back/page-read feedback is classified as shared Greg Experience, audio-only, or written-only before revision.
- Existing Chapters 1-3 are experimental evidence and are not force-rewritten by this change.

- [ ] **Step 3: Point `r2/data/project.json` at the contract**

Add:

```json
"rendering_pipeline": "data/rendering-pipeline.json"
```

without changing chapter order or the current chapter.

---

### Task 3: Route worker documentation through the shared surface

**Files:**
- Modify: `r2/README.md`

**Interfaces:**
- Consumes: `r2/PIPELINE.md` and `r2/data/rendering-pipeline.json`.
- Produces: a publishing/worker map that tells future chats to use the shared surface before medium finishing.

- [ ] **Step 1: Update the public model section**

Add:

```markdown
Before either Listen or Read becomes a medium-specific artifact, use the shared rendering contract in `PIPELINE.md`.

The default wording path is:

`Story State / Performance → Greg Experience → Shared Greg Surface → Audio Finish / Written Finish`

Audio and written are sibling medium-specific finishes from the same Shared Greg Surface. Do not use written prose as a mandatory source transcript for audio, and do not treat audio wording as a transcript that must later be rewritten back into prose.
```

- [ ] **Step 2: Update the next-chapter worker sequence**

Require workers to:

- confirm or create the chapter's Shared Greg Surface before medium-specific finishing unless it is an explicitly documented legacy experiment
- classify listen-back/page-read discoveries as shared Greg Experience, audio-only, or written-only

Keep the existing manifest and media-publication instructions intact.

---

### Task 4: Verify and publish the architecture change

**Files:**
- Review branch diff against `main`.

**Interfaces:**
- Consumes: Tasks 1-3.
- Produces: clean PR/merge containing only pipeline memory, manifest pointer, and regression coverage.

- [ ] **Step 1: Run the R2 site test suite**

Run:

```bash
python -m unittest tests.test_r2_site -v
```

Expected: PASS, aside from any explicitly identified pre-existing unrelated failure on current `main`.

- [ ] **Step 2: Validate JSON syntax**

Run:

```bash
python - <<'PY'
import json
from pathlib import Path
for path in [Path('r2/data/project.json'), Path('r2/data/rendering-pipeline.json')]:
    json.loads(path.read_text(encoding='utf-8'))
    print('OK', path)
PY
```

Expected: both files print `OK`.

- [ ] **Step 3: Review changed files**

Expected durable scope:

```text
docs/superpowers/specs/2026-09-08-r2-shared-greg-surface-design.md
docs/superpowers/plans/2026-09-08-r2-shared-greg-surface.md
r2/PIPELINE.md
r2/README.md
r2/data/project.json
r2/data/rendering-pipeline.json
tests/test_r2_site.py
```

No chapter prose, audio MP3, chapter manifests, image assets, or root Run 1 reader files should change.

- [ ] **Step 4: Open a PR to `main`**

Title:

```text
Lock R2 shared Greg surface pipeline
```

State clearly that this is a rendering-architecture/memory change only and does not rewrite existing chapters.

- [ ] **Step 5: Merge only after the focused R2 pipeline contract is green**

After merge, verify `main` contains `r2/PIPELINE.md` and `r2/data/rendering-pipeline.json` and that Pages deployment succeeds.
