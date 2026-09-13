# R2 Audio Score Light Chapters 001-030 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and publish a Light Audio Score generation for Greg, Again Chapters 001-030 that stays anchored to the original written prose, uses only minor speech-generation edits, and replaces public audio chapter-by-chapter only after verified synthesis.

**Architecture:** Add a parallel `audio-score-light` source layer and `audio/light` production registry without deleting or overwriting existing Score 1 or legacy audio. Reuse the proven preview-safe short-take factory, parameterized for the Light source/output paths. Generate all 30 Light text files first or ahead of synthesis, validate the <=15% hard textual-change ceiling, then run bounded audio lanes and independently promote verified Light assets in the public manifest.

**Tech Stack:** Markdown source artifacts, Python 3 standard library validation/planning scripts, JSON manifests, GitHub Actions, AI Voice Generator `deep` voice, ffprobe/ffmpeg, existing Greg Again static audio player.

**Spec:** `docs/superpowers/specs/2026-09-11-audio-score-light-design.md`

## Global Constraints

- Story/written authority remains `r2/assets/written/chNNN.md`.
- Existing heavy Score 1 remains preserved under `r2/assets/audio-score/`.
- Light Score always starts from written prose, never Score 1.
- Expected word-level textual change is roughly 2-8%; 15% is a hard ceiling, not a target.
- Punctuation, whitespace, lineation, and paragraph boundaries do not count toward the word-level textual-change ceiling.
- Zero textual changes are valid.
- No new facts, changed dialogue ownership, invented characterization, or broad paragraph rewriting.
- Invented repetition is rare and must clearly add audible value; reject anything that can sound like a duplicate/stutter.
- Voice is `deep`.
- Provider-safe chunks remain <=500 characters.
- Existing legacy and Score 1 audio/assets/evidence are never overwritten.
- Public routing changes only after full Light verification for that chapter.

---

### Task 1: Add Light doctrine and textual-change validator

**Files:**
- Create: `r2/AUDIO_SCORE_LIGHT.md`
- Create: `scripts/audio_score_light_validate.py`
- Create: `tests/test_audio_score_light.py`

**Interfaces:**
- Consumes: `r2/assets/written/chNNN.md`, `r2/assets/audio-score-light/chNNN.md`
- Produces: CLI `python scripts/audio_score_light_validate.py NNN` returning exit 0 when the Light source header is valid and normalized word-level edit distance is <=0.15.

- [ ] **Step 1: Write the failing validator tests**

```python
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "audio_score_light_validate", ROOT / "scripts" / "audio_score_light_validate.py"
)
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


def test_normalized_words_ignore_punctuation_and_lineation():
    a = "Wait, really?\n\nYes."
    b = "Wait really yes"
    assert mod.normalized_words(a) == mod.normalized_words(b)


def test_change_ratio_allows_small_word_edits():
    source = "one two three four five six seven eight nine ten"
    light = "one two three four five six seven eight nine okay"
    assert mod.word_change_ratio(source, light) <= 0.15


def test_change_ratio_rejects_large_rewrite():
    source = "one two three four five six seven eight nine ten"
    light = "alpha beta gamma delta epsilon zeta eta theta iota kappa"
    assert mod.word_change_ratio(source, light) > 0.15
```

- [ ] **Step 2: Run tests and verify failure**

Run: `python -m pytest tests/test_audio_score_light.py -v`
Expected: FAIL because `scripts/audio_score_light_validate.py` does not exist.

- [ ] **Step 3: Implement the validator**

Use `difflib.SequenceMatcher` over lowercase alphanumeric/apostrophe word tokens so punctuation/lineation are free while inserted/deleted/replaced words count. Core functions:

```python
WORD_RE = re.compile(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)?")


def normalized_words(text: str) -> list[str]:
    return [m.group(0).lower() for m in WORD_RE.finditer(text)]


def word_change_ratio(source: str, light: str) -> float:
    a = normalized_words(source)
    b = normalized_words(light)
    if not a:
        return 0.0 if not b else 1.0
    matcher = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    changed = 0
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag != "equal":
            changed += max(i2 - i1, j2 - j1)
    return changed / len(a)
```

The CLI must:
1. resolve `NNN`
2. read the Light file header and body split at `\n---\n`
3. read the recorded written source path
4. verify the recorded source blob SHA against `git hash-object`
5. calculate the ratio
6. fail above `0.15`
7. print `NNN: X.XX% word-level change`.

- [ ] **Step 4: Add `r2/AUDIO_SCORE_LIGHT.md`**

Durably encode the approved doctrine from the spec, including: original prose first, micro speech-generation tricks only, 2-8% typical, 15% ceiling, punctuation/lineation free, Score 1 preserved, rare repetition, and no broad rewriting.

- [ ] **Step 5: Run tests**

Run: `python -m pytest tests/test_audio_score_light.py -v`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add r2/AUDIO_SCORE_LIGHT.md scripts/audio_score_light_validate.py tests/test_audio_score_light.py
git commit -m "Add Audio Score Light doctrine and validator"
```

---

### Task 2: Parameterize the proven short-take planner for Light generation

**Files:**
- Modify: `scripts/audio_score_capture_plan.py`
- Create: `tests/test_audio_score_capture_plan.py`

**Interfaces:**
- Consumes: generation name `v2` or `light`, chapter number.
- Produces: existing v2 behavior unchanged by default; Light mode reads `r2/assets/audio-score-light/chNNN.md` and writes `greg-again/audio/light/takes/NNN/short-takes.json`.

- [ ] **Step 1: Add failing tests for source/output routing**

Test a pure helper:

```python
def test_generation_paths_preserve_v2_default():
    source, output = mod.generation_paths("v2", "013")
    assert source.as_posix() == "r2/assets/audio-score/ch013.md"
    assert output.as_posix() == "greg-again/audio/v2/takes/013/short-takes.json"


def test_generation_paths_route_light():
    source, output = mod.generation_paths("light", "013")
    assert source.as_posix() == "r2/assets/audio-score-light/ch013.md"
    assert output.as_posix() == "greg-again/audio/light/takes/013/short-takes.json"
```

- [ ] **Step 2: Run test and verify failure**

Run: `python -m pytest tests/test_audio_score_capture_plan.py -v`
Expected: FAIL because `generation_paths` / `--generation` do not exist.

- [ ] **Step 3: Implement minimal generation routing**

Add:

```python
def generation_paths(generation: str, chapter: str) -> tuple[Path, Path]:
    if generation == "v2":
        return (
            Path(f"r2/assets/audio-score/ch{chapter}.md"),
            Path(f"greg-again/audio/v2/takes/{chapter}/short-takes.json"),
        )
    if generation == "light":
        return (
            Path(f"r2/assets/audio-score-light/ch{chapter}.md"),
            Path(f"greg-again/audio/light/takes/{chapter}/short-takes.json"),
        )
    raise SystemExit(f"Unsupported generation: {generation}")
```

Add `--generation choices=("v2", "light") default="v2"`. Preserve the exact existing substitution and chunking behavior.

- [ ] **Step 4: Run planner tests and existing relevant audio tests**

Run: `python -m pytest tests/test_audio_score_capture_plan.py tests/test_greg_again_audio_catalog.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/audio_score_capture_plan.py tests/test_audio_score_capture_plan.py
git commit -m "Reuse short-take planner for Audio Score Light"
```

---

### Task 3: Add Light production routing and manifest scaffold

**Files:**
- Create: `r2/AUDIO_SCORE_LIGHT_PRODUCTION.md`
- Create: `greg-again/audio/light/manifest.json`
- Create: `greg-again/audio/light/ROLLING_POOL.md`
- Modify: `AGENTS.md`

**Interfaces:**
- Consumes: verified Light Score source and short-take plan.
- Produces: durable generation-specific ownership/publication contract for 001-030.

- [ ] **Step 1: Write the production doctrine**

Required rules:
- scope 001-030
- exact spoken source `r2/assets/audio-score-light/chNNN.md`
- Light validation must pass before synthesis
- up to five concurrent synthesis lanes
- one chapter per lane
- short-take factory with `deep`, identical transcript/preview text, durable preview URLs
- Light output paths under `greg-again/audio/light/` and `assets/light/`
- never infer completion from Score 1/v2 completion
- preserve all durable old generations
- publish each chapter independently after verification
- public `audio_finish` becomes `audio-score-light`
- refresh/reconcile newest `greg-again/audio/manifest.json` before each public write.

- [ ] **Step 2: Create empty Light manifest**

```json
{
  "series": "Greg, Again",
  "generation": "audio-score-light",
  "status": "experimental",
  "renderer_adapter": "ai_voice_generator",
  "voice_style": "deep",
  "source_layer": "r2/assets/audio-score-light",
  "chapters": []
}
```

- [ ] **Step 3: Create rolling pool state**

Record 001-030 as eligible once their Light text exists and validates. Keep five-lane concurrency as an execution rule, not thirty branch reservations.

- [ ] **Step 4: Update `AGENTS.md` narrowly**

In the Greg, Again Audio section, route Light-score work to `r2/AUDIO_SCORE_LIGHT_PRODUCTION.md` when the request explicitly names Light / Score 2. Preserve all existing v2 routing.

- [ ] **Step 5: Commit**

```bash
git add r2/AUDIO_SCORE_LIGHT_PRODUCTION.md greg-again/audio/light/manifest.json greg-again/audio/light/ROLLING_POOL.md AGENTS.md
git commit -m "Add Audio Score Light production lane"
```

---

### Task 4: Produce and validate Light Score text for Chapters 001-030

**Files:**
- Create: `r2/assets/audio-score-light/ch001.md` through `ch030.md`

**Interfaces:**
- Consumes: exact current `r2/assets/written/chNNN.md`.
- Produces: validated spoken-source Markdown for every chapter, ready for capture planning.

- [ ] **Step 1: For each chapter, read exact written authority**

Do not use Score 1 as source text. It may be consulted only as negative/positive listening evidence after the written chapter is understood.

- [ ] **Step 2: Create Light header**

Use:

```markdown
# Chapter N: TITLE

Status: **AUDIO SCORE LIGHT / SCORE 2**

Source: `r2/assets/written/chNNN.md`
Source SHA: `<git hash-object of written source>`
Protocol: `r2/AUDIO_SCORE_LIGHT.md`
Voice target: `deep`
Word-level change: `<validator result>`

This is a light speech-generation transcript. The original written prose remains authority. Changes are intentionally minor.

---
```

- [ ] **Step 3: Apply only micro speech-generation edits**

Per chapter, prefer punctuation/lineation first. Add only a few high-value statement/question turns, restatements, self-corrections, or tiny spoken-clarity changes. Do not spend the 15% budget simply because it exists.

- [ ] **Step 4: Validate every chapter**

Run for all chapters:

```bash
for n in $(seq -w 1 30); do
  python scripts/audio_score_light_validate.py "$n" || exit 1
done
```

Expected: all <=15%; normal chapters should usually land roughly 2-8% or lower.

- [ ] **Step 5: Spot-audit for anti-patterns**

Search Light-only additions for suspicious repeated-word clusters and broad rewritten paragraphs. Reject any invented repetition that sounds like a duplicate/stutter without performance context.

- [ ] **Step 6: Commit in reviewable batches**

Commit 001-010, 011-020, 021-030 separately so a bad calibration batch can be reverted without losing the others.

---

### Task 5: Build Light short-take plans for Chapters 001-030

**Files:**
- Create: `greg-again/audio/light/takes/001/short-takes.json` through `030/short-takes.json`

**Interfaces:**
- Consumes: validated Light text.
- Produces: exact provider-facing short-take queue with source identity and pronunciation substitutions.

- [ ] **Step 1: Generate all plans**

```bash
for n in $(seq -w 1 30); do
  python scripts/audio_score_capture_plan.py "$n" --generation light || exit 1
done
```

- [ ] **Step 2: Verify each plan**

Every provider-facing `transcript` and `preview_transcript` pair is identical, no take exceeds 500 provider characters, and source reconstruction is exact.

- [ ] **Step 3: Commit plans**

```bash
git add greg-again/audio/light/takes
git commit -m "Plan Audio Score Light takes for Chapters 1-30"
```

---

### Task 6: Synthesize, assemble, verify, and publish Light audio 001-030

**Files:**
- Create per chapter: `greg-again/audio/light/production/NNN/`
- Create per chapter: `greg-again/audio/light/verification/NNN/`
- Create per chapter binary: `greg-again/audio/assets/light/chapter-NNN.mp3`
- Modify incrementally: `greg-again/audio/light/manifest.json`
- Modify incrementally: `greg-again/audio/manifest.json`
- Modify incrementally: `tests/test_greg_again_audio_catalog.py`

**Interfaces:**
- Consumes: Light take plans.
- Produces: verified `deep` MP3s and independent public promotion.

- [ ] **Step 1: Keep at most five live synthesis lanes**

Each lane owns exactly one chapter. When a lane fully publishes, it claims the next earliest unowned Light chapter. Do not pre-claim all thirty.

- [ ] **Step 2: Generate every take using the proven factory**

For every take call the AI Voice Generator with:
- `transcript` = provider-facing take text
- `preview_transcript` = exactly the same provider-facing take text
- `voice_id` = `deep`

Capture returned playable preview URL/context evidence immediately. Never regenerate a take that already has a durable playable artifact.

- [ ] **Step 3: Download and verify chunks in GitHub Actions**

Reuse the current capture-binding/assembly workflow. Every chunk must exist, be nontrivial, and pass `ffprobe` before assembly.

- [ ] **Step 4: Assemble chapter**

Concatenate verified chunks in exact order with ffmpeg, then append approximately two seconds of silence after the final spoken word.

- [ ] **Step 5: Verify chapter**

Record:
- Light source path/blob SHA
- take count/order
- provider contexts/preview URLs
- final duration
- final SHA-256
- ffprobe success
- settling-tail evidence
- listener QA status (`verified_unlistened` unless actually auditioned).

- [ ] **Step 6: Promote independently**

After each chapter verifies, refresh newest public manifest and change only that chapter:

```json
"audio_src": "assets/light/chapter-NNN.mp3",
"audio_finish": "audio-score-light"
```

Preserve chapter ID, number, title, image/lens metadata, unrelated chapter changes, old assets, and old Score 1/v2 manifests.

- [ ] **Step 7: Update catalog contract incrementally**

The catalog test should derive the set of Light-routed chapter numbers from the Light manifest, then assert every published Light route exists and is nontrivial. Do not hard-code a fake 001-030 completion before binaries exist.

- [ ] **Step 8: Continue until all 001-030 are verified and public**

A chapter is not complete merely because synthesis was submitted. Completion requires durable chunks, assembled playable MP3, Light manifest entry, public manifest route, and repository verification.

---

### Task 7: Final 001-030 verification and integration

**Files:**
- Verify: `r2/assets/audio-score-light/ch001.md` ... `ch030.md`
- Verify: `greg-again/audio/light/manifest.json`
- Verify: `greg-again/audio/manifest.json`
- Verify: `greg-again/audio/assets/light/chapter-001.mp3` ... `chapter-030.mp3`
- Verify: all Light production/verification evidence.

**Interfaces:**
- Produces: one auditable integration state proving all thirty Light text/audio chapters are complete without deleting previous generations.

- [ ] **Step 1: Run all Light text validators**

Expected: 30/30 pass <=15%.

- [ ] **Step 2: Run repository audio/catalog tests**

Run: `python -m pytest tests/test_audio_score_light.py tests/test_audio_score_capture_plan.py tests/test_greg_again_audio_catalog.py -v`
Expected: PASS.

- [ ] **Step 3: Verify manifest coverage**

Light manifest contains exactly one verified entry for each ga-001 through ga-030; public manifest routes all 30 to `assets/light/chapter-NNN.mp3`.

- [ ] **Step 4: Verify old generations survive**

Existing `greg-again/audio/assets/v2/` and legacy `greg-again/audio/assets/` files and v2 manifest remain intact.

- [ ] **Step 5: Merge only after green checks**

Open the integration PR from `audio-score-light-001-030` to `main`, run CI, reconcile any concurrent public-manifest movement, rerun checks, then merge.
