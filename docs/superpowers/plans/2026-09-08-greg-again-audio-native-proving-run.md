# Greg, Again Audio-Native Proving Run Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build one repeatable Greg, Again Chapter 1 audio-native proving product: durable Audio Score/state, qualified-renderer boundary, replaceable block takes, deterministic assembly, and a small `/greg-again/audio/` player.

**Architecture:** Keep story authority separate from audio production. A pure-Python Audio OS layer validates score/manifest state, exports renderable blocks, imports only explicitly qualified takes, assembles selected PCM WAV takes, and generates public player metadata. Renderer transport stays behind an adapter boundary so a programmable expressive renderer can be used when it meets the bar, while ChatGPT-quality bootstrap capture remains a valid proof path without leaking browser/recording details into story state.

**Tech Stack:** Python 3 standard library, pytest, JSON/Markdown state, PCM WAV for the first proving master, static HTML/CSS/vanilla JS for GitHub Pages.

**Spec:** `docs/superpowers/specs/2026-09-08-greg-again-audio-native-proving-run-design.md`

## Global Constraints

- This is an audio-native proving run, not generic TTS and not an audiobook conversion pipeline.
- Flat/generic TTS is a failed quality gate, never a silent fallback.
- Renderer quality states are exactly: `qualified`, `experimental`, `failed_quality_gate`, `unrendered`.
- One primary traditional narrator performs narration and characters; no full cast in this build.
- The written Chapter 1 source is evidence, not immutable spoken wording.
- Hidden performance direction must never be emitted as audience speech.
- Stable audio block IDs use `ga-001-bNNN` and survive rerenders.
- A missing or unapproved selected take must block chapter assembly.
- Existing PLG canon, existing reader pages, and original manuscript authority must not be rewritten as a side effect.
- The public proving surface is `/greg-again/audio/` and remains `experimental` until creator listen-back approval.
- Do not build Image OS, a catalog, accounts, waveform editing, soundtrack, dense Foley, or a general multi-book audio platform in this implementation.

---

## File Structure

Create or modify only these focused units:

- `scripts/greg_again_audio.py` — score/manifest validation, selected-take resolution, public metadata generation.
- `scripts/greg_again_audio_render.py` — renderer adapter protocol, bootstrap bundle export, take registration/import.
- `scripts/greg_again_audio_assembly.py` — deterministic PCM WAV compatibility checks and concatenation.
- `scripts/build_greg_again_audio.py` — tiny CLI orchestrator for validate/export/import/assemble/publish commands.
- `tests/test_greg_again_audio.py` — core schema/state tests.
- `tests/test_greg_again_audio_render.py` — adapter/bootstrap/import tests.
- `tests/test_greg_again_audio_assembly.py` — WAV assembly tests.
- `tests/test_greg_again_audio_product.py` — Chapter 1 state and player-product tests.
- `state/experiments/greg-again/audio/narrator.md` — persistent narrator/performance profile.
- `state/experiments/greg-again/audio/pronunciation.json` — pronunciation registry, initially minimal.
- `state/experiments/greg-again/audio/chapters/001/score.json` — complete Chapter 1 Audio Score.
- `state/experiments/greg-again/audio/chapters/001/manifest.json` — selected takes, provenance, quality/approval state.
- `state/experiments/greg-again/audio/chapters/001/listen-back.md` — manual review evidence.
- `state/experiments/greg-again/audio/chapters/001/takes/.gitkeep` — durable take location without fake audio.
- `greg-again/audio/index.html` — minimal audio proving player.
- `greg-again/audio/audio.css` — focused styling; do not append to historical `assets/reader.css`.
- `greg-again/audio/player.js` — load public metadata and wire native audio controls/status.
- `greg-again/audio/manifest.json` — generated public-only metadata.
- `greg-again/audio/assets/.gitkeep` — target for selected assembled chapter master.

Do **not** integrate this first proving subsystem into `scripts/plg_ai_tools.py`; prove the boundary first and add an AI-tool surface only after audio earns promotion.

---

### Task 1: Core Audio Score and Manifest Contract

**Files:**
- Create: `scripts/greg_again_audio.py`
- Create: `tests/test_greg_again_audio.py`

**Interfaces:**
- Produces: `validate_score(score: dict) -> dict`
- Produces: `validate_manifest(manifest: dict, score: dict) -> dict`
- Produces: `selected_take_paths(manifest: dict, takes_root: Path) -> list[Path]`
- Produces: `build_public_metadata(manifest: dict) -> dict`

- [ ] **Step 1: Write failing schema tests**

```python
from pathlib import Path
import pytest

from scripts.greg_again_audio import (
    build_public_metadata,
    selected_take_paths,
    validate_manifest,
    validate_score,
)


def minimal_score():
    return {
        "schema": "greg_again_audio_score/v1",
        "run_id": "greg-again",
        "chapter_id": "ga-001",
        "title": "The Boy",
        "score_revision": 1,
        "blocks": [
            {
                "id": "ga-001-b001",
                "scene_id": "wake-young-body",
                "spoken_text": "I woke because my back didn't hurt.",
                "direction": {
                    "narrator_mode": "narration",
                    "entering_state": "confused, physically alert",
                    "intention": "notice bodily wrongness before explaining it",
                    "physical_context": "Greg is still in bed",
                    "pace": "unhurried opening, curiosity building",
                    "continuity": "chapter opening",
                    "listener_risks": [],
                },
            }
        ],
    }


def minimal_manifest():
    return {
        "schema": "greg_again_audio_manifest/v1",
        "run_id": "greg-again",
        "chapter_id": "ga-001",
        "title": "The Boy",
        "score_revision": 1,
        "block_order": ["ga-001-b001"],
        "renderer_status": "unrendered",
        "approval_state": "experimental",
        "selected_takes": {},
        "assembled_asset": None,
        "duration_seconds": None,
    }


def test_score_rejects_duplicate_or_unstable_block_ids():
    score = minimal_score()
    score["blocks"].append(dict(score["blocks"][0]))
    with pytest.raises(ValueError, match="duplicate block id"):
        validate_score(score)


def test_manifest_rejects_unknown_quality_state():
    score = minimal_score()
    manifest = minimal_manifest()
    manifest["renderer_status"] = "good_enough_tts"
    with pytest.raises(ValueError, match="renderer_status"):
        validate_manifest(manifest, score)


def test_assembly_inputs_require_one_selected_take_per_block(tmp_path: Path):
    score = minimal_score()
    manifest = minimal_manifest()
    validate_manifest(manifest, score)
    with pytest.raises(ValueError, match="missing selected take"):
        selected_take_paths(manifest, tmp_path)


def test_public_metadata_hides_production_notes():
    score = minimal_score()
    manifest = minimal_manifest()
    manifest["production_notes"] = "private renderer diagnosis"
    public = build_public_metadata(validate_manifest(manifest, score))
    assert "production_notes" not in public
    assert public["status"] == "experimental"
```

- [ ] **Step 2: Run tests and verify failure**

Run: `pytest tests/test_greg_again_audio.py -v`
Expected: import failure because `scripts.greg_again_audio` does not exist.

- [ ] **Step 3: Implement minimal validated contract**

Implement constants and validation with no third-party dependencies:

```python
SCORE_SCHEMA = "greg_again_audio_score/v1"
MANIFEST_SCHEMA = "greg_again_audio_manifest/v1"
RENDERER_STATES = {"qualified", "experimental", "failed_quality_gate", "unrendered"}
APPROVAL_STATES = {"experimental", "approved"}
```

Validation requirements:
- `run_id == "greg-again"`
- chapter ID is nonempty and score/manifest match
- block IDs match `ga-001-bNNN` for this proving chapter and are unique
- every block has nonempty `spoken_text` and a `direction` object
- `block_order` exactly matches score block IDs in intended order
- selected-take keys must be known block IDs
- `renderer_status` and `approval_state` must use the allowed sets
- public metadata exposes only title, chapter ID, status, duration, and assembled asset path.

- [ ] **Step 4: Run focused tests**

Run: `pytest tests/test_greg_again_audio.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/greg_again_audio.py tests/test_greg_again_audio.py
git commit -m "feat: add Greg Again audio state contract"
```

---

### Task 2: Create the Chapter 1 Audio Score and Narrator State

**Files:**
- Create: `state/experiments/greg-again/audio/narrator.md`
- Create: `state/experiments/greg-again/audio/pronunciation.json`
- Create: `state/experiments/greg-again/audio/chapters/001/score.json`
- Create: `state/experiments/greg-again/audio/chapters/001/manifest.json`
- Create: `state/experiments/greg-again/audio/chapters/001/listen-back.md`
- Create: `state/experiments/greg-again/audio/chapters/001/takes/.gitkeep`
- Create: `tests/test_greg_again_audio_product.py`

**Interfaces:**
- Consumes: `validate_score`, `validate_manifest`
- Produces: a complete renderable Chapter 1 score and valid initial manifest.

- [ ] **Step 1: Write failing repository-state test**

```python
import json
from pathlib import Path

from scripts.greg_again_audio import validate_manifest, validate_score

ROOT = Path(__file__).resolve().parents[1]
AUDIO = ROOT / "state/experiments/greg-again/audio"


def test_chapter_1_audio_state_is_complete_and_unrendered():
    score = json.loads((AUDIO / "chapters/001/score.json").read_text(encoding="utf-8"))
    manifest = json.loads((AUDIO / "chapters/001/manifest.json").read_text(encoding="utf-8"))
    validate_score(score)
    validate_manifest(manifest, score)
    assert score["title"] == "The Boy"
    assert len(score["blocks"]) >= 8
    assert manifest["renderer_status"] == "unrendered"
    assert manifest["approval_state"] == "experimental"
    assert manifest["selected_takes"] == {}
```

Also assert `narrator.md` contains the phrases `one primary narrator`, `dry humor`, `speaker clarity`, and `do not overperform`.

- [ ] **Step 2: Run test and verify failure**

Run: `pytest tests/test_greg_again_audio_product.py::test_chapter_1_audio_state_is_complete_and_unrendered -v`
Expected: FAIL because the audio state files do not exist.

- [ ] **Step 3: Write narrator and pronunciation state**

`narrator.md` must encode:
- one stable traditional narrator
- Greg is dominant POV but not the literal acoustic identity of the whole world
- Greg speeds slightly when overconfident/building a model
- dry humor is underplayed
- grief is not melodramatically signaled before the words earn it
- quoted neighbor dialogue is distinct but not a cartoon character voice
- speaker clarity outranks elegant ambiguity
- do not overperform every joke, profanity, or revelation
- scene direction is preferred over line-by-line emotion tags.

`pronunciation.json` begins as:

```json
{
  "schema": "greg_again_pronunciation/v1",
  "entries": [
    {"term": "Carrow", "status": "confirm_before_render", "note": "Do not guess a pronunciation silently."},
    {"term": "East Verrel", "status": "confirm_before_render", "note": "Do not guess a pronunciation silently."}
  ]
}
```

- [ ] **Step 4: Build the complete Chapter 1 Audio Score**

Use `state/experiments/plg-r2/prose/001-the-boy.md` as source evidence, not locked wording. Cover the full chapter in roughly 8–16 coherent performance blocks. Preserve these story beats in order unless an audio-specific change clearly improves first-listen comprehension:

1. back/body wrongness and young hands
2. mirror/body confirmation and humor
3. cheap sword test and theory-versus-body mismatch
4. magic failure and fear
5. inventory/window/date verification
6. forty-years-back confidence spike
7. parents/grief interruption
8. memory reliability model
9. sword/side-step/basin failure
10. leave for the Guild

The opening block should remain close to this audible shape because it already performs cleanly:

```text
I woke because my back didn't hurt.

That was wrong.

Not alarming at first. Waking normally involved a short negotiation with several pieces of me that had outlived their warranties. Lower back. Left shoulder. Right knee. The rib that clicked if I slept twisted.

Nothing dramatic. Just attendance.

This morning nobody showed up.
```

Do not optimize the score for page elegance. Use repeated names or explicit orientation only when the ear needs them. Hidden `direction` carries acting context and must not be duplicated into `spoken_text` as stage directions.

Initialize `manifest.json` with every block in `block_order`, no selected takes, `renderer_status: "unrendered"`, `approval_state: "experimental"`, and no assembled asset.

Initialize `listen-back.md` with the review headings: naturalness, acting intelligence, narrator continuity, character distinction, speaker clarity, first-listen comprehension, pacing, joke timing, emotional turn clarity, listening fatigue, desire to continue.

- [ ] **Step 5: Run tests**

Run: `pytest tests/test_greg_again_audio_product.py -v`
Expected: PASS for repository-state validation.

- [ ] **Step 6: Commit**

```bash
git add state/experiments/greg-again/audio tests/test_greg_again_audio_product.py
git commit -m "feat: score Greg Again chapter one for audio"
```

---

### Task 3: Renderer Adapter Boundary and Bootstrap Bundle

**Files:**
- Create: `scripts/greg_again_audio_render.py`
- Create: `tests/test_greg_again_audio_render.py`

**Interfaces:**
- Produces: `RendererRequest` dataclass
- Produces: `RendererResult` dataclass
- Produces: `build_renderer_request(block: dict, narrator_text: str) -> RendererRequest`
- Produces: `export_bootstrap_bundle(score: dict, narrator_text: str, output_dir: Path) -> list[Path]`
- Produces: `register_take(manifest: dict, *, block_id: str, take_id: str, relative_path: str, adapter: str, model: str | None, voice: str | None, renderer_status: str) -> dict`

- [ ] **Step 1: Write failing renderer tests**

```python
from pathlib import Path
import json
import pytest

from scripts.greg_again_audio_render import export_bootstrap_bundle, register_take


def test_bootstrap_bundle_separates_hidden_direction_from_spoken_text(tmp_path: Path):
    score = {
        "chapter_id": "ga-001",
        "score_revision": 1,
        "blocks": [{
            "id": "ga-001-b001",
            "scene_id": "opening",
            "spoken_text": "I woke because my back didn't hurt.",
            "direction": {"intention": "quiet confusion", "pace": "slow"},
        }],
    }
    paths = export_bootstrap_bundle(score, "ONE PRIMARY NARRATOR", tmp_path)
    payload = json.loads(paths[0].read_text(encoding="utf-8"))
    assert payload["spoken_text"] == "I woke because my back didn't hurt."
    assert payload["performance_context"]["intention"] == "quiet confusion"
    assert "quiet confusion" not in payload["spoken_text"]


def test_take_registration_rejects_generic_tts_state():
    with pytest.raises(ValueError, match="renderer_status"):
        register_take({}, block_id="ga-001-b001", take_id="t1", relative_path="takes/t1.wav", adapter="tts", model=None, voice=None, renderer_status="good_enough_tts")
```

- [ ] **Step 2: Run tests and verify failure**

Run: `pytest tests/test_greg_again_audio_render.py -v`
Expected: import failure.

- [ ] **Step 3: Implement the adapter contract**

Use dataclasses only; do not call any external API in this task. `RendererRequest` contains block ID, spoken text, narrator brief, performance context, prior-block continuity text, and pronunciation notes. `RendererResult` contains take ID, relative path, adapter, model, voice, renderer status, and optional generation note.

`export_bootstrap_bundle` writes one JSON request per block plus `index.json`; the bundle is transport-neutral and can be consumed by a future OpenAI Realtime adapter or by a ChatGPT-playback capture worker.

`register_take` deep-copies the manifest, validates the renderer state against the same four allowed states, records the take under `takes[block_id][take_id]`, and does **not** select it automatically.

- [ ] **Step 4: Run focused tests**

Run: `pytest tests/test_greg_again_audio_render.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/greg_again_audio_render.py tests/test_greg_again_audio_render.py
git commit -m "feat: add replaceable audio renderer boundary"
```

---

### Task 4: Deterministic WAV Assembly and Take Selection

**Files:**
- Create: `scripts/greg_again_audio_assembly.py`
- Create: `tests/test_greg_again_audio_assembly.py`

**Interfaces:**
- Consumes: `selected_take_paths`
- Produces: `inspect_wav(path: Path) -> dict[str, int]`
- Produces: `assemble_pcm_wav(paths: list[Path], output_path: Path) -> float`

- [ ] **Step 1: Write failing WAV tests**

Create tiny WAV fixtures inside the test using Python's `wave` module. Verify two 24 kHz, 16-bit, mono takes concatenate in exact order and incompatible sample rates are rejected.

```python

def test_assemble_pcm_wav_preserves_block_order(tmp_path):
    a = write_silence(tmp_path / "a.wav", frames=2400, rate=24000)
    b = write_silence(tmp_path / "b.wav", frames=4800, rate=24000)
    duration = assemble_pcm_wav([a, b], tmp_path / "chapter.wav")
    assert duration == pytest.approx(0.3)
    with wave.open(str(tmp_path / "chapter.wav"), "rb") as fh:
        assert fh.getnframes() == 7200
        assert fh.getframerate() == 24000
```

- [ ] **Step 2: Run and verify failure**

Run: `pytest tests/test_greg_again_audio_assembly.py -v`
Expected: import failure.

- [ ] **Step 3: Implement minimal assembly**

Use the standard-library `wave` module. Require all selected takes to match channels, sample width, sample rate, and compression type. Write frames sequentially with no automatic trimming, crossfading, gain changes, or normalization in this proving build; those operations risk destroying intentional performance timing and can be added only after listening evidence justifies them.

- [ ] **Step 4: Run tests**

Run: `pytest tests/test_greg_again_audio_assembly.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/greg_again_audio_assembly.py tests/test_greg_again_audio_assembly.py
git commit -m "feat: assemble selected Greg Again audio takes"
```

---

### Task 5: Build CLI and Minimal Public Audio Product

**Files:**
- Create: `scripts/build_greg_again_audio.py`
- Modify: `tests/test_greg_again_audio_product.py`
- Create: `greg-again/audio/index.html`
- Create: `greg-again/audio/audio.css`
- Create: `greg-again/audio/player.js`
- Create: `greg-again/audio/manifest.json`
- Create: `greg-again/audio/assets/.gitkeep`

**Interfaces:**
- Produces CLI commands:
  - `validate`
  - `export-bootstrap`
  - `select-take`
  - `assemble`
  - `publish-metadata`

- [ ] **Step 1: Add failing product tests**

```python

def test_public_audio_page_is_small_and_audio_first():
    html = (ROOT / "greg-again/audio/index.html").read_text(encoding="utf-8")
    assert "GREG, AGAIN" in html
    assert "Audio-Native Proving Run" in html
    assert "The Boy" in html
    assert "<audio" in html
    assert "waveform" not in html.lower()
    assert "dashboard" not in html.lower()


def test_unrendered_public_manifest_has_no_fake_audio_asset():
    public = json.loads((ROOT / "greg-again/audio/manifest.json").read_text(encoding="utf-8"))
    assert public["status"] == "experimental"
    assert public["audio_src"] is None
```

- [ ] **Step 2: Run and verify failure**

Run: `pytest tests/test_greg_again_audio_product.py -v`
Expected: FAIL because the public surface does not exist.

- [ ] **Step 3: Implement CLI orchestration**

The CLI should only compose earlier pure functions. Defaults point at the Chapter 1 paths under `state/experiments/greg-again/audio/chapters/001/` and `greg-again/audio/`.

`select-take` must require an existing registered take and explicit `--block-id` + `--take-id`; it updates `selected_takes` but never marks the chapter approved.

`assemble` must fail unless every block has a selected take and every selected take has `renderer_status == "qualified"`; successful assembly updates `assembled_asset` and `duration_seconds` but leaves `approval_state == "experimental"`.

`publish-metadata` writes only public metadata and sets `audio_src` only when an assembled asset exists.

- [ ] **Step 4: Build the static page**

Use a restrained book-like page, not dashboard chrome. Include:
- `GREG, AGAIN`
- `Audio-Native Proving Run`
- `Chapter 1 · The Boy`
- one native `<audio controls preload="metadata">`
- elapsed/duration supplied by native controls
- visible `Experimental` status
- one short note: `Composed for listening, not converted from a finished audiobook manuscript.`

`player.js` loads `manifest.json`; when `audio_src` is null, disable/hide the active source and show `Audio render not yet qualified.` When present, set the source and allow playback.

- [ ] **Step 5: Run product tests**

Run: `pytest tests/test_greg_again_audio_product.py -v`
Expected: PASS.

- [ ] **Step 6: Run all new audio tests**

Run: `pytest tests/test_greg_again_audio.py tests/test_greg_again_audio_render.py tests/test_greg_again_audio_assembly.py tests/test_greg_again_audio_product.py -v`
Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add scripts/build_greg_again_audio.py greg-again/audio tests/test_greg_again_audio_product.py
git commit -m "feat: add Greg Again audio proving player"
```

---

### Task 6: Renderer Qualification, Chapter 1 Sample, and Listen-Back Gate

**Files:**
- Modify: `state/experiments/greg-again/audio/chapters/001/manifest.json`
- Modify: `state/experiments/greg-again/audio/chapters/001/listen-back.md`
- Add qualified WAV takes under: `state/experiments/greg-again/audio/chapters/001/takes/`
- Add assembled sample under: `greg-again/audio/assets/chapter-001.wav`
- Regenerate: `greg-again/audio/manifest.json`

**Interfaces:**
- Consumes the bootstrap bundle or a future programmable expressive renderer implementing the adapter contract.
- Produces the actual heard Chapter 1 proving sample.

- [ ] **Step 1: Export the Chapter 1 renderer bundle**

Run:

```bash
python scripts/build_greg_again_audio.py export-bootstrap
```

Expected: one renderer request per `ga-001-bNNN` plus an index under a temporary/cache output path, with spoken text and hidden context separated.

- [ ] **Step 2: Qualify renderer candidates by ear before bulk rendering**

Render the same 60–90 second difficult excerpt through available expressive paths. The primary programmable candidates should use current OpenAI native audio/Realtme-capable models rather than legacy TTS; as of the design date, official OpenAI docs expose Realtime models with text input, audio output, response-level instructions, and 24 kHz PCM output. The known-good ChatGPT playback remains the reference path if programmable output is materially worse.

Record each candidate in `listen-back.md` under:
- naturalness
- acting intelligence
- narrator continuity
- character distinction
- speaker clarity
- first-listen comprehension
- pacing
- joke timing
- listening fatigue
- desire to continue

Mark only a candidate that meets the creator's quality bar as `qualified`. Do not proceed with a generic/flat candidate for convenience.

- [ ] **Step 3: Render/import one complete take per block using the qualified path**

For a programmable adapter, save output as 24 kHz mono PCM WAV before registration. For the bootstrap path, capture ChatGPT-quality playback through loopback/system-audio tooling outside the Audio OS, save each block as WAV, then import/register the files. Browser automation and loopback-recording implementation details remain outside score/manifest state.

Register each take with adapter/model/voice provenance and `renderer_status: "qualified"`.

- [ ] **Step 4: Listen to seams and rerender only failed blocks**

Do not inspect only the score. Listen to transitions between adjacent blocks. If a seam resets cadence, emotion, or speaker identity, first try a longer continuity context or move the block boundary; rerender only affected blocks.

- [ ] **Step 5: Explicitly select takes and assemble**

For every block:

```bash
python scripts/build_greg_again_audio.py select-take --block-id ga-001-bNNN --take-id TAKE_ID
```

Then:

```bash
python scripts/build_greg_again_audio.py assemble
python scripts/build_greg_again_audio.py publish-metadata
```

Expected: `greg-again/audio/assets/chapter-001.wav` exists and the public manifest references it, while status remains `experimental`.

- [ ] **Step 6: Perform the actual quality gate**

Listen without reading the score. Chapter 1 only becomes `approved` if both are true:
1. narrator quality is acceptable against the known-good ChatGPT playback reference;
2. the creator voluntarily wants to continue listening for roughly 10 consecutive minutes or the full sample if shorter.

If not, classify failure as renderer, voice, performance context, wording, scene construction, story beat, or seam/assembly. Revise the cheapest correct layer and rerender. If the expressive renderer itself cannot meet the bar after the bounded proving effort, leave the chapter `experimental`/`failed_quality_gate` and return Greg, Again to prose-first rendering.

- [ ] **Step 7: Record approval or failure and commit only truthful state**

If approved, update `approval_state` to `approved` and preserve listen-back evidence. If not approved, do not publish a fake success state.

```bash
git add state/experiments/greg-again/audio greg-again/audio
git commit -m "feat: publish Greg Again chapter one audio proof"
```

---

### Task 7: Verification and Durable Handoff

**Files:**
- Modify only if needed: `state/READER_DESIGN_LAB.md`
- Modify only if the experiment earns promotion: relevant Greg, Again durable state/trailhead

- [ ] **Step 1: Run the focused suite**

```bash
pytest tests/test_greg_again_audio.py tests/test_greg_again_audio_render.py tests/test_greg_again_audio_assembly.py tests/test_greg_again_audio_product.py -v
```

Expected: PASS.

- [ ] **Step 2: Run the repository test suite**

```bash
pytest -q
```

Expected: PASS; if unrelated pre-existing failures exist, record exact failures rather than claiming green.

- [ ] **Step 3: Verify publication boundaries**

Confirm:
- no original `chapters/*.html` prose changed
- no PLG manuscript authority changed
- no existing root reader route was replaced
- `/greg-again/audio/` is isolated
- no generic TTS fallback exists
- public manifest contains no production-only notes
- score and manifest remain durable under `state/experiments/greg-again/audio/`.

- [ ] **Step 4: Update durable reader guidance only if evidence earned it**

If Chapter 1 is approved, add a compact principle to `state/READER_DESIGN_LAB.md`: Greg, Again may support an audio-native renderer whose heard performance, not page prose, is the audience-quality authority; renderer quality remains gated. If the experiment fails, do not promote the rule; keep the evidence local to the experiment.

- [ ] **Step 5: Commit verification/handoff changes**

```bash
git add state/READER_DESIGN_LAB.md state/experiments/greg-again/audio
git commit -m "docs: record Greg Again audio proving result"
```

Only include files that actually changed.

## Plan Self-Review

- **Spec coverage:** score/hidden direction, narrator model, renderer quality gate, bootstrap path, stable block IDs, take provenance, speaker clarity, listen-back categories, deterministic assembly, minimal player, truthful unrendered/failure behavior, and prose fallback are all mapped to tasks.
- **Placeholder scan:** no `TBD`, `TODO`, `implement later`, or unspecified edge-handling steps remain.
- **Type consistency:** score/manifest schemas, `renderer_status`, `approval_state`, block IDs, selected-take map, and generated public metadata use the same names across tasks.
- **Scope:** first build remains one Chapter 1 proof. No Image OS, full-cast drama, catalog, or broad reader migration is included.
