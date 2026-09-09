# Greg, Again Audio-Native Proving Run Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build one repeatable Greg, Again Chapter 1 audio-native proving product: durable Audio Score/state, a qualified-renderer boundary, replaceable block takes, deterministic assembly, and a small `/greg-again/audio/` player.

**Architecture:** Story authority stays separate from audio production. A pure-Python Audio OS validates score/manifest state, exports renderable performance blocks, imports only explicit takes, assembles selected qualified PCM WAV takes, and generates public player metadata. Renderer transport stays replaceable so a programmable expressive renderer can be used when it meets the quality bar, while ChatGPT-quality bootstrap capture remains a valid proving path without leaking browser/recording details into story state.

**Tech Stack:** Python 3 standard library, pytest, JSON/Markdown state, 24 kHz mono PCM WAV for the first proving master, static HTML/CSS/vanilla JS for GitHub Pages.

**Spec:** `docs/superpowers/specs/2026-09-08-greg-again-audio-native-proving-run-design.md`

## Global Constraints

- This is audio-native story production, not generic TTS and not audiobook conversion.
- Flat/generic TTS is a failed quality gate, never a silent fallback.
- Renderer states are exactly `qualified`, `experimental`, `failed_quality_gate`, `unrendered`.
- Approval states are exactly `experimental`, `approved`.
- One primary traditional narrator performs narration and characters; no full cast in this build.
- The written Chapter 1 source is evidence, not immutable spoken wording.
- Hidden performance direction must never become audience speech.
- Stable block IDs use `ga-001-bNNN` and survive rerenders.
- Assembly requires exactly one selected take per block, and every selected take must itself be `qualified`.
- Existing PLG canon, manuscript authority, and current root reader must not change as a side effect.
- `/greg-again/audio/` remains experimental until creator listen-back approval.
- Do not build Image OS, a catalog, accounts, waveform editing, soundtrack, dense Foley, or a general audio platform here.

## File Map

- `scripts/greg_again_audio.py` — score/manifest validation, take resolution, public metadata.
- `scripts/greg_again_audio_render.py` — renderer request/result types, bootstrap export, take registration.
- `scripts/greg_again_audio_assembly.py` — PCM WAV compatibility checks and concatenation.
- `scripts/build_greg_again_audio.py` — small CLI composing those modules.
- `tests/test_greg_again_audio.py`
- `tests/test_greg_again_audio_render.py`
- `tests/test_greg_again_audio_assembly.py`
- `tests/test_greg_again_audio_product.py`
- `state/experiments/greg-again/audio/narrator.md`
- `state/experiments/greg-again/audio/pronunciation.json`
- `state/experiments/greg-again/audio/chapters/001/score.json`
- `state/experiments/greg-again/audio/chapters/001/manifest.json`
- `state/experiments/greg-again/audio/chapters/001/listen-back.md`
- `state/experiments/greg-again/audio/chapters/001/takes/.gitkeep`
- `greg-again/audio/index.html`
- `greg-again/audio/audio.css`
- `greg-again/audio/player.js`
- `greg-again/audio/manifest.json`
- `greg-again/audio/assets/.gitkeep`

Do not add this first proof to `scripts/plg_ai_tools.py`; prove the subsystem first.

---

### Task 1: Core Audio State Contract

**Files:**
- Create: `scripts/greg_again_audio.py`
- Create: `tests/test_greg_again_audio.py`

**Interfaces:**
- `validate_score(score: dict) -> dict`
- `validate_manifest(manifest: dict, score: dict) -> dict`
- `selected_take_paths(manifest: dict, takes_root: Path) -> list[Path]`
- `build_public_metadata(manifest: dict) -> dict`

The production manifest take shape is fixed now:

```json
{
  "takes": {
    "ga-001-b001": {
      "take-001": {
        "relative_path": "takes/ga-001-b001-take-001.wav",
        "adapter": "bootstrap_chatgpt",
        "model": null,
        "voice": null,
        "renderer_status": "qualified"
      }
    }
  },
  "selected_takes": {
    "ga-001-b001": "take-001"
  }
}
```

Public metadata maps private `assembled_asset` to public `audio_src`; it never exposes takes, renderer notes, or hidden direction.

- [ ] **Step 1: Write failing tests**

```python
from pathlib import Path
import pytest

from scripts.greg_again_audio import build_public_metadata, selected_take_paths, validate_manifest, validate_score


def score():
    return {
        "schema": "greg_again_audio_score/v1",
        "run_id": "greg-again",
        "chapter_id": "ga-001",
        "title": "The Boy",
        "score_revision": 1,
        "blocks": [{
            "id": "ga-001-b001",
            "scene_id": "wake-young-body",
            "spoken_text": "I woke because my back didn't hurt.",
            "direction": {"narrator_mode": "narration", "intention": "quiet confusion"},
        }],
    }


def manifest():
    return {
        "schema": "greg_again_audio_manifest/v1",
        "run_id": "greg-again",
        "chapter_id": "ga-001",
        "title": "The Boy",
        "score_revision": 1,
        "block_order": ["ga-001-b001"],
        "renderer_status": "unrendered",
        "approval_state": "experimental",
        "takes": {},
        "selected_takes": {},
        "assembled_asset": None,
        "duration_seconds": None,
    }


def test_rejects_duplicate_block_ids():
    value = score()
    value["blocks"].append(dict(value["blocks"][0]))
    with pytest.raises(ValueError, match="duplicate block id"):
        validate_score(value)


def test_rejects_generic_tts_quality_state():
    value = manifest()
    value["renderer_status"] = "good_enough_tts"
    with pytest.raises(ValueError, match="renderer_status"):
        validate_manifest(value, score())


def test_selected_take_must_exist_and_be_qualified(tmp_path: Path):
    value = manifest()
    value["takes"] = {"ga-001-b001": {"take-001": {
        "relative_path": "takes/a.wav", "adapter": "probe", "model": None,
        "voice": None, "renderer_status": "experimental"
    }}}
    value["selected_takes"] = {"ga-001-b001": "take-001"}
    with pytest.raises(ValueError, match="qualified"):
        selected_take_paths(validate_manifest(value, score()), tmp_path)


def test_public_metadata_maps_asset_without_private_state():
    value = manifest()
    value["assembled_asset"] = "assets/chapter-001.wav"
    value["duration_seconds"] = 123.5
    value["production_notes"] = "private"
    public = build_public_metadata(validate_manifest(value, score()))
    assert public == {
        "chapter_id": "ga-001",
        "title": "The Boy",
        "status": "experimental",
        "duration_seconds": 123.5,
        "audio_src": "assets/chapter-001.wav",
    }
```

- [ ] **Step 2: Run test to verify failure**

Run: `pytest tests/test_greg_again_audio.py -v`
Expected: import failure.

- [ ] **Step 3: Implement minimal contract**

Use:

```python
SCORE_SCHEMA = "greg_again_audio_score/v1"
MANIFEST_SCHEMA = "greg_again_audio_manifest/v1"
RENDERER_STATES = {"qualified", "experimental", "failed_quality_gate", "unrendered"}
APPROVAL_STATES = {"experimental", "approved"}
```

Validation must enforce score/manifest identity match, unique `ga-001-bNNN` block IDs, nonempty spoken text, direction objects, exact block order, known selected-take IDs, and allowed states. `selected_take_paths` resolves the selected take in block order and refuses missing files or any selected take not marked `qualified`.

- [ ] **Step 4: Run focused tests**

Run: `pytest tests/test_greg_again_audio.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/greg_again_audio.py tests/test_greg_again_audio.py
git commit -m "feat: add Greg Again audio state contract"
```

---

### Task 2: Chapter 1 Audio Score and Narrator State

**Files:**
- Create the five state files and `.gitkeep` listed under `state/experiments/greg-again/audio/`.
- Create: `tests/test_greg_again_audio_product.py`

**Interfaces:** consumes Task 1 validators; produces one complete, renderable Chapter 1 score with initial unrendered manifest.

- [ ] **Step 1: Write failing state test**

```python
import json
from pathlib import Path
from scripts.greg_again_audio import validate_manifest, validate_score

ROOT = Path(__file__).resolve().parents[1]
AUDIO = ROOT / "state/experiments/greg-again/audio"


def test_chapter_one_audio_state_is_complete_and_unrendered():
    score = json.loads((AUDIO / "chapters/001/score.json").read_text(encoding="utf-8"))
    manifest = json.loads((AUDIO / "chapters/001/manifest.json").read_text(encoding="utf-8"))
    validate_score(score)
    validate_manifest(manifest, score)
    assert score["title"] == "The Boy"
    assert 8 <= len(score["blocks"]) <= 16
    assert manifest["renderer_status"] == "unrendered"
    assert manifest["approval_state"] == "experimental"
    assert manifest["takes"] == {}
    assert manifest["selected_takes"] == {}
```

Also test `narrator.md` contains `one primary narrator`, `dry humor`, `speaker clarity`, and `do not overperform`.

- [ ] **Step 2: Run test and verify failure**

Run: `pytest tests/test_greg_again_audio_product.py -v`
Expected: missing-file failure.

- [ ] **Step 3: Write narrator and pronunciation state**

`narrator.md` must establish one stable traditional narrator; Greg is dominant POV but not the acoustic identity of the whole world; Greg may accelerate when overconfident; dry humor is underplayed; grief is not pre-signaled melodramatically; speaker clarity outranks elegant ambiguity; neighbor dialogue is distinct but not cartoonish; scene-level direction is preferred over line-level acting tags.

Start `pronunciation.json` exactly as:

```json
{
  "schema": "greg_again_pronunciation/v1",
  "entries": [
    {"term": "Carrow", "status": "confirm_before_render", "note": "Do not guess a pronunciation silently."},
    {"term": "East Verrel", "status": "confirm_before_render", "note": "Do not guess a pronunciation silently."}
  ]
}
```

- [ ] **Step 4: Write the complete Audio Score from Chapter 1 evidence**

Use `state/experiments/plg-r2/prose/001-the-boy.md` as evidence, not locked spoken wording. Cover the full chapter in 8–16 performance blocks preserving these story beats unless audio-specific execution clearly improves them:

1. body wrongness / young hands
2. mirror confirmation / humor
3. sword test / theory-body mismatch
4. magic failure / fear
5. inventory, window, dates
6. forty-years-back confidence spike
7. parents / grief
8. memory reliability model
9. side-step / basin failure
10. leave for the Guild

Opening audible shape should remain close to:

```text
I woke because my back didn't hurt.

That was wrong.

Not alarming at first. Waking normally involved a short negotiation with several pieces of me that had outlived their warranties. Lower back. Left shoulder. Right knee. The rib that clicked if I slept twisted.

Nothing dramatic. Just attendance.

This morning nobody showed up.
```

Every block contains `id`, `scene_id`, `spoken_text`, and `direction`. Direction carries narrator mode, entering state, intention, physical context, pace/energy, previous-block continuity, and listener-orientation risks. Do not place stage directions inside `spoken_text`.

Initialize the manifest with all block IDs in exact order, empty `takes`/`selected_takes`, no asset, no duration, `unrendered`, `experimental`.

Initialize `listen-back.md` with headings for naturalness, acting intelligence, narrator continuity, character distinction, speaker clarity, first-listen comprehension, pacing, joke timing, emotional turn clarity, listening fatigue, and desire to continue.

- [ ] **Step 5: Run tests**

Run: `pytest tests/test_greg_again_audio_product.py -v`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add state/experiments/greg-again/audio tests/test_greg_again_audio_product.py
git commit -m "feat: score Greg Again chapter one for audio"
```

---

### Task 3: Renderer Boundary and Bootstrap Export/Import

**Files:**
- Create: `scripts/greg_again_audio_render.py`
- Create: `tests/test_greg_again_audio_render.py`

**Interfaces:**
- `RendererRequest` dataclass: block ID, spoken text, narrator brief, performance context, continuity context, pronunciation notes.
- `RendererResult` dataclass: take ID, relative path, adapter, model, voice, renderer status, generation note.
- `export_bootstrap_bundle(score: dict, narrator_text: str, pronunciation: dict, output_dir: Path) -> list[Path]`
- `register_take(manifest: dict, result: RendererResult) -> dict`

- [ ] **Step 1: Write failing renderer tests**

```python
import json
from pathlib import Path
import pytest
from scripts.greg_again_audio_render import RendererResult, export_bootstrap_bundle, register_take


def test_export_keeps_direction_hidden(tmp_path: Path):
    score = {"chapter_id": "ga-001", "score_revision": 1, "blocks": [{
        "id": "ga-001-b001", "scene_id": "opening",
        "spoken_text": "I woke because my back didn't hurt.",
        "direction": {"intention": "quiet confusion"},
    }]}
    paths = export_bootstrap_bundle(score, "ONE PRIMARY NARRATOR", {"entries": []}, tmp_path)
    payload = json.loads(paths[0].read_text(encoding="utf-8"))
    assert payload["spoken_text"] == "I woke because my back didn't hurt."
    assert payload["performance_context"]["intention"] == "quiet confusion"
    assert "quiet confusion" not in payload["spoken_text"]


def test_register_take_does_not_auto_select_it():
    manifest = {"takes": {}, "selected_takes": {}}
    result = RendererResult("ga-001-b001", "take-001", "takes/a.wav", "bootstrap_chatgpt", None, None, "qualified", None)
    updated = register_take(manifest, result)
    assert "take-001" in updated["takes"]["ga-001-b001"]
    assert updated["selected_takes"] == {}
```

- [ ] **Step 2: Run and verify failure**

Run: `pytest tests/test_greg_again_audio_render.py -v`
Expected: import failure.

- [ ] **Step 3: Implement the transport-neutral boundary**

Use dataclasses and JSON only. Bootstrap export writes one request JSON per block plus `index.json`. It is usable by a future programmable OpenAI native-audio worker or a ChatGPT-playback capture worker. `register_take` records provenance under the fixed manifest shape and never auto-selects or auto-approves.

Do not add a legacy TTS adapter.

- [ ] **Step 4: Run tests**

Run: `pytest tests/test_greg_again_audio_render.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/greg_again_audio_render.py tests/test_greg_again_audio_render.py
git commit -m "feat: add replaceable Greg Again audio renderer boundary"
```

---

### Task 4: Deterministic PCM WAV Assembly

**Files:**
- Create: `scripts/greg_again_audio_assembly.py`
- Create: `tests/test_greg_again_audio_assembly.py`

**Interfaces:**
- `inspect_wav(path: Path) -> dict[str, int]`
- `assemble_pcm_wav(paths: list[Path], output_path: Path) -> float`

- [ ] **Step 1: Write failing WAV tests**

Use Python `wave` to create tiny 24 kHz mono 16-bit fixtures. Assert 2400 + 4800 frames produces 7200 frames and 0.3 seconds; assert incompatible sample rates raise `ValueError`.

- [ ] **Step 2: Run and verify failure**

Run: `pytest tests/test_greg_again_audio_assembly.py -v`
Expected: import failure.

- [ ] **Step 3: Implement standard-library assembly**

Require identical channel count, sample width, sample rate, and compression type. Write frames in selected block order. Do not trim silence, crossfade, normalize gain, or otherwise alter timing in the first proof.

- [ ] **Step 4: Run tests**

Run: `pytest tests/test_greg_again_audio_assembly.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/greg_again_audio_assembly.py tests/test_greg_again_audio_assembly.py
git commit -m "feat: assemble qualified Greg Again audio takes"
```

---

### Task 5: CLI and Minimal Public Player

**Files:**
- Create: `scripts/build_greg_again_audio.py`
- Modify: `tests/test_greg_again_audio_product.py`
- Create: `greg-again/audio/index.html`
- Create: `greg-again/audio/audio.css`
- Create: `greg-again/audio/player.js`
- Create: `greg-again/audio/manifest.json`
- Create: `greg-again/audio/assets/.gitkeep`

**CLI commands:** `validate`, `export-bootstrap`, `register-take`, `select-take`, `assemble`, `publish-metadata`.

- [ ] **Step 1: Add failing player tests**

```python

def test_public_page_is_small_and_audio_first():
    html = (ROOT / "greg-again/audio/index.html").read_text(encoding="utf-8")
    assert "GREG, AGAIN" in html
    assert "Audio-Native Proving Run" in html
    assert "The Boy" in html
    assert "<audio" in html
    assert "waveform" not in html.lower()
    assert "dashboard" not in html.lower()


def test_unrendered_public_manifest_has_no_fake_audio():
    public = json.loads((ROOT / "greg-again/audio/manifest.json").read_text(encoding="utf-8"))
    assert public["status"] == "experimental"
    assert public["audio_src"] is None
```

- [ ] **Step 2: Run and verify failure**

Run: `pytest tests/test_greg_again_audio_product.py -v`
Expected: player files missing.

- [ ] **Step 3: Implement CLI orchestration**

Defaults target Chapter 1 state paths. `register-take` only registers. `select-take` requires known block/take IDs. `assemble` calls Task 1 resolution, so every block must have a selected `qualified` take; successful assembly writes `greg-again/audio/assets/chapter-001.wav`, updates `assembled_asset`, `duration_seconds`, and chapter `renderer_status` to `qualified`, but leaves `approval_state` as `experimental`. `publish-metadata` writes only the five public fields from `build_public_metadata`.

- [ ] **Step 4: Build the static page**

Use a restrained book-like surface with:
- `GREG, AGAIN`
- `Audio-Native Proving Run`
- `Chapter 1 · The Boy`
- one native `<audio controls preload="metadata">`
- visible Experimental status
- note: `Composed for listening, not converted from a finished audiobook manuscript.`

`player.js` loads `manifest.json`. If `audio_src` is null, it shows `Audio render not yet qualified.` and does not invent a source. If present, it assigns the source and lets native controls handle playback.

- [ ] **Step 5: Run all new tests**

```bash
pytest tests/test_greg_again_audio.py tests/test_greg_again_audio_render.py tests/test_greg_again_audio_assembly.py tests/test_greg_again_audio_product.py -v
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add scripts/build_greg_again_audio.py greg-again/audio tests/test_greg_again_audio_product.py
git commit -m "feat: add Greg Again audio proving player"
```

---

### Task 6: Renderer Qualification and Actual Chapter 1 Sample

**Files:**
- Modify: `state/experiments/greg-again/audio/chapters/001/manifest.json`
- Modify: `state/experiments/greg-again/audio/chapters/001/listen-back.md`
- Add qualified takes under: `state/experiments/greg-again/audio/chapters/001/takes/`
- Add assembled sample: `greg-again/audio/assets/chapter-001.wav`
- Regenerate: `greg-again/audio/manifest.json`

- [ ] **Step 1: Export render requests**

Run:

```bash
python scripts/build_greg_again_audio.py export-bootstrap
```

Expected: one request per block plus an index, with spoken text and performance context separated.

- [ ] **Step 2: Qualify the renderer before bulk production**

Render the same difficult 60–90 second excerpt through available expressive paths. Prefer current native-audio/Realtime-capable OpenAI models rather than legacy TTS. Current official OpenAI API documentation exposes Realtime models with text input, audio output, response-level instructions, and 24 kHz PCM output. Compare programmable output against the creator's known-good ChatGPT playback reference.

Record naturalness, acting intelligence, narrator continuity, character distinction, speaker clarity, first-listen comprehension, pacing, joke timing, listening fatigue, and desire to continue. Only a path that meets the creator's bar is marked `qualified`. If no programmable path qualifies, the bootstrap path may use ChatGPT-quality playback plus loopback/system-audio capture.

- [ ] **Step 3: Render/import one complete qualified take per block**

Save/import each selected candidate as 24 kHz mono PCM WAV. Register adapter/model/voice provenance and its renderer state. Browser automation and recording transport details must remain outside score/story state.

- [ ] **Step 4: Listen to block seams and rerender only failures**

If a seam resets cadence, emotional state, or speaker ownership, first increase continuity context or move the block boundary; rerender affected blocks only.

- [ ] **Step 5: Select and assemble**

For each block:

```bash
python scripts/build_greg_again_audio.py select-take --block-id ga-001-bNNN --take-id TAKE_ID
```

Then:

```bash
python scripts/build_greg_again_audio.py assemble
python scripts/build_greg_again_audio.py publish-metadata
```

Expected: `greg-again/audio/assets/chapter-001.wav` exists, public metadata references it, renderer status is `qualified`, approval remains `experimental`.

- [ ] **Step 6: Apply the actual quality gate**

Listen without reading the score. Approve only when narrator quality is acceptable against the ChatGPT playback reference **and** the creator voluntarily wants to continue listening for roughly 10 consecutive minutes or the full sample if shorter.

If it fails, classify the failure as renderer, narrator/voice, performance context, spoken wording, scene construction, story beat, or block seam. Revise the cheapest correct layer. If the expressive renderer cannot meet the bar after the bounded proof, keep truthful failure state and return Greg, Again to prose-first rendering.

- [ ] **Step 7: Record truthful outcome and commit**

If approved, set `approval_state` to `approved` and preserve listen-back evidence. Otherwise leave it experimental/failed; never publish a fake success.

```bash
git add state/experiments/greg-again/audio greg-again/audio
git commit -m "feat: publish Greg Again chapter one audio proof"
```

---

### Task 7: Verification and Handoff

- [ ] **Step 1: Run focused suite**

```bash
pytest tests/test_greg_again_audio.py tests/test_greg_again_audio_render.py tests/test_greg_again_audio_assembly.py tests/test_greg_again_audio_product.py -v
```

Expected: PASS.

- [ ] **Step 2: Run repository suite**

Run: `pytest -q`
Expected: PASS, or record exact pre-existing unrelated failures without claiming green.

- [ ] **Step 3: Verify boundaries**

Confirm no original `chapters/*.html`, manuscript authority, or root reader route changed; `/greg-again/audio/` is isolated; no generic TTS fallback exists; public metadata has no production notes; score/manifest remain under experimental state.

- [ ] **Step 4: Promote guidance only if earned**

If Chapter 1 is approved, add a compact evidence-backed audio-native principle to `state/READER_DESIGN_LAB.md`. If it fails, keep evidence local and do not promote the rule.

- [ ] **Step 5: Commit only actual handoff changes**

```bash
git add state/READER_DESIGN_LAB.md state/experiments/greg-again/audio
git commit -m "docs: record Greg Again audio proving result"
```

Only add files that actually changed.

## Self-Review

- **Spec coverage:** narrator model, score/hidden direction, quality gate, bootstrap path, block IDs, take provenance, speaker clarity, listen-back, deterministic assembly, minimal player, truthful failure, and prose fallback are mapped.
- **No placeholders:** no TBD/TODO/"implement later" steps remain.
- **Type consistency:** production `takes`, `selected_takes`, `assembled_asset`, public `audio_src`, renderer status, approval status, and block IDs use one fixed shape across tasks.
- **Scope:** one Chapter 1 proof only; no Image OS, full cast, broad reader migration, or generic platform work.
