# REHEARSAL Modes, Relationship Memory, and Greg Inner Voice Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend the existing REHEARSAL engine with FAITHFUL/FREE/DIRECTED modes, relationship-local memory, frozen take-variance testing, private Greg INNER VOICE performance, and high-authority FREE prose return, then run a Nico-focused canon 001-020 thought rehearsal.

**Architecture:** Extend `scripts/rehearsal_engine.py` rather than introducing a parallel engine. Keep old overtuned-calibration artifacts readable, promote FREE to the default creative mode, and add strict visibility boundaries so Greg's private cognition is available only to Nico, the novelizer, and approved critics. Use the existing exact-source patching pattern and self-applying workflow for branch prose returns.

**Tech Stack:** Python 3 standard library, `unittest`, JSON state artifacts, GitHub Actions, existing PLG chapter HTML and validation scripts.

**Spec:** `docs/superpowers/specs/2026-09-06-rehearsal-modes-memory-inner-voice-design.md`

**Spec Addendum:** `docs/superpowers/specs/2026-09-06-rehearsal-inner-voice-boundary-addendum.md`

## Global Constraints

- Canonical chapter prose remains the only story authority.
- Preserve canon truth, not canon choreography.
- FREE is the default creative rehearsal mode.
- High actor authority is normal, but no write path has unrestricted authority to `main`.
- Hard story surfaces remain locked: plot, facts, knowledge, causality, chronology, economics, major relationship state, injury/physical state, earned competence, unresolved mystery state.
- Relationship memory has separate `supported` and `hypothesis` lanes.
- Synthetic rehearsal repetition cannot self-promote.
- Variance siblings use one frozen memory snapshot and cannot observe one another before comparison.
- Greg's `INNER VOICE` is private performance state. Non-Greg actors may observe only Greg's `BODY` and `VOICE`.
- `INNER VOICE` may be sentence-shaped or nonverbal/pre-verbal cognition. No schema may require grammatical internal monologue.
- Movement, dialogue, tone, and Greg's live cognition may reshape scene-scale prose on an isolated editorial branch after existing source/lock/reader gates pass.
- Do not use em dashes in generated PLG prose.

---

### Task 1: Add explicit rehearsal modes and production return policy

**Files:**
- Modify: `scripts/rehearsal_engine.py`
- Modify: `tests/test_rehearsal_engine.py`

**Interfaces:**
- Produces: `REHEARSAL_MODES = {"faithful", "free", "directed"}`
- Produces: `build_rehearsal_packet(..., mode="free", direction=None, take_id=None, variance_group_id=None, memory_snapshot_id=None) -> dict`
- Produces: `editorial_return_policy(mode="production") -> dict`
- Preserves: `editorial_return_policy("standard")` and `editorial_return_policy("overtuned_calibration")` for backward compatibility

- [ ] **Step 1: Write failing mode tests**

Add tests equivalent to:

```python
def test_free_is_default_rehearsal_mode(self):
    packet = engine.compile_actor_packet(actor(), scene_id="007.s010", role_context={})
    rehearsal = engine.build_rehearsal_packet({"scene_id": "007.s010"}, {}, [packet])
    self.assertEqual("free", rehearsal["mode"])


def test_directed_requires_explicit_direction(self):
    packet = engine.compile_actor_packet(actor(), scene_id="007.s010", role_context={})
    with self.assertRaisesRegex(ValueError, "direction"):
        engine.build_rehearsal_packet(
            {"scene_id": "007.s010"}, {}, [packet], mode="directed", take_id="take-1"
        )


def test_production_policy_allows_scene_rebuild_on_non_main_branch(self):
    policy = engine.editorial_return_policy("production")
    self.assertTrue(policy["actor_preference_can_trigger_write"])
    self.assertTrue(policy["branch_canon_write_authorized"])
    self.assertEqual("scene_rebuild", policy["max_local_scope"])
    self.assertTrue(policy["production_safe"])
```

- [ ] **Step 2: Run the focused tests and verify RED**

Run:

```bash
python -m unittest tests.test_rehearsal_engine -v
```

Expected: failures because `free` is not the default mode, DIRECTED validation does not exist, and `production` policy is unknown.

- [ ] **Step 3: Implement the minimal mode contract**

In `scripts/rehearsal_engine.py`:

```python
REHEARSAL_MODES = {"faithful", "free", "directed"}


def _validate_rehearsal_mode(mode: str, direction: str | None) -> None:
    if mode not in REHEARSAL_MODES:
        raise ValueError(f"invalid rehearsal mode: {mode}")
    if mode == "directed" and not _nonempty(direction):
        raise ValueError("directed rehearsal requires direction")
    if mode != "directed" and direction is not None:
        raise ValueError("direction is only valid for directed rehearsal")
```

Extend `build_rehearsal_packet` to emit `mode`, `direction`, `take_id`, `variance_group_id`, and `memory_snapshot_id`. Use `mode="free"` by default.

Add a `production` policy with the same scene-scale soft-prose authority as the successful overtuned calibration, but mark it `production_safe=True` because it still requires exact-source, reader, lock, soft-surface, and non-main branch gates.

- [ ] **Step 4: Run focused tests and verify GREEN**

Run:

```bash
python -m unittest tests.test_rehearsal_engine -v
```

Expected: all rehearsal engine tests pass.

- [ ] **Step 5: Commit Task 1**

```bash
git add scripts/rehearsal_engine.py tests/test_rehearsal_engine.py
git commit -m "Add REHEARSAL take modes and production policy"
```

---

### Task 2: Add relationship-local performance memory with two trust lanes

**Files:**
- Modify: `scripts/rehearsal_engine.py`
- Modify: `tests/test_rehearsal_engine.py`
- Create: `state/editorial/rehearsal/relationship-memory.json`

**Interfaces:**
- Produces: `RELATIONSHIP_MEMORY_SCHEMA = "rehearsal_relationship_memory/v1"`
- Produces: `relationship_memory_key(role: str, counterpart_role: str) -> str`
- Produces: `validate_relationship_memory_registry(registry: dict) -> None`
- Produces: `relationship_memory_for(registry: dict, role: str, counterpart_roles: list[str]) -> dict`
- Extends: `compile_actor_packet(..., relationship_memory: dict | None = None)`

- [ ] **Step 1: Write failing relationship-memory tests**

Add tests equivalent to:

```python
def test_relationship_memory_is_directional_and_lane_separated(self):
    memory = {
        "schema": engine.RELATIONSHIP_MEMORY_SCHEMA,
        "relationships": {
            "Antonius::Greg": {
                "supported": [{"value": "waits Greg out", "source_type": "canon", "source": "chapters/005.html"}],
                "hypothesis": [{"value": "lets silence defeat the joke", "source_type": "rehearsal", "source": "take-x"}],
            }
        },
    }
    engine.validate_relationship_memory_registry(memory)
    compiled = engine.relationship_memory_for(memory, "Antonius", ["Greg"])
    self.assertEqual("waits Greg out", compiled["supported"][0]["value"])
    self.assertEqual("lets silence defeat the joke", compiled["hypothesis"][0]["value"])
    self.assertEqual({}, engine.relationship_memory_for(memory, "Greg", ["Antonius"]))


def test_rehearsal_hypothesis_does_not_count_as_independent_support(self):
    evidence = [
        {"type": "rehearsal", "source": "take-a"},
        {"type": "rehearsal", "source": "take-b"},
    ]
    self.assertEqual(0, engine.independent_support_count(evidence))
```

- [ ] **Step 2: Run focused tests and verify RED**

```bash
python -m unittest tests.test_rehearsal_engine -v
```

Expected: failures because relationship-memory interfaces do not exist.

- [ ] **Step 3: Implement directional relationship memory**

Use directional keys such as `Antonius::Greg`, because Antonius-opposite-Greg memory is not identical to Greg-opposite-Antonius memory.

Validation rules:

```python
RELATIONSHIP_MEMORY_SCHEMA = "rehearsal_relationship_memory/v1"
VALID_MEMORY_LANES = {"supported", "hypothesis"}
SUPPORTED_MEMORY_SOURCE_TYPES = {"canon", "accepted_prose", "user_anchor", "promoted_tendency"}
HYPOTHESIS_MEMORY_SOURCE_TYPES = {"rehearsal"}
```

Require every entry to include nonempty `value`, `source_type`, and `source`. Reject rehearsal source types in the supported lane.

`relationship_memory_for` returns copies of the relevant lane entries for each requested counterpart without promoting or merging trust levels.

- [ ] **Step 4: Add the initial empty durable registry**

Create:

```json
{
  "schema": "rehearsal_relationship_memory/v1",
  "relationships": {}
}
```

Do not seed synthetic beliefs merely to populate the file. The Nico campaign will add evidence-backed entries.

- [ ] **Step 5: Compile memory into actor packets**

Extend `compile_actor_packet` so packets may contain:

```python
"relationship_memory": {
    "supported": [...],
    "hypothesis": [...],
}
```

Keep the lanes separate in the packet.

- [ ] **Step 6: Run focused tests and verify GREEN**

```bash
python -m unittest tests.test_rehearsal_engine -v
```

Expected: pass.

- [ ] **Step 7: Commit Task 2**

```bash
git add scripts/rehearsal_engine.py tests/test_rehearsal_engine.py state/editorial/rehearsal/relationship-memory.json
git commit -m "Add relationship-local REHEARSAL memory"
```

---

### Task 3: Enforce Greg INNER VOICE privacy and non-sentence cognition

**Files:**
- Modify: `scripts/rehearsal_engine.py`
- Modify: `tests/test_rehearsal_engine.py`

**Interfaces:**
- Produces: `GREG_PERFORMANCE_CHANNELS = ("body", "voice", "inner_voice")`
- Produces: `DEFAULT_PERFORMANCE_CHANNELS = ("body", "voice")`
- Produces: `INNER_VOICE_FORMS`
- Produces: `validate_performance_output(output: dict) -> None`
- Produces: `actor_observable_view(output: dict, *, observer_role: str) -> dict`
- Produces: `novelizer_performance_view(output: dict) -> dict`

- [ ] **Step 1: Write failing channel and privacy tests**

Add tests equivalent to:

```python
def test_greg_packet_has_private_inner_voice_channel(self):
    packet = engine.compile_actor_packet(actor(), scene_id="005.s001", role_context={})
    self.assertEqual(["body", "voice", "inner_voice"], packet["performance_channels"])


def test_non_greg_actor_packet_has_no_inner_voice_channel(self):
    antonius = actor(actor_id="actor.desmond.v1", role="Antonius")
    antonius["actor_name"] = "Desmond"
    packet = engine.compile_actor_packet(antonius, scene_id="005.s001", role_context={})
    self.assertEqual(["body", "voice"], packet["performance_channels"])


def test_other_actor_cannot_observe_greg_inner_voice(self):
    output = {
        "role": "Greg",
        "body": [{"kind": "hesitation", "value": "hand pauses over ledger"}],
        "voice": [{"value": "Same thing."}],
        "inner_voice": [{"form": "wrong_inference", "value": "He bought it."}],
    }
    view = engine.actor_observable_view(output, observer_role="Antonius")
    self.assertIn("body", view)
    self.assertIn("voice", view)
    self.assertNotIn("inner_voice", view)
    self.assertIn("inner_voice", engine.novelizer_performance_view(output))
```

- [ ] **Step 2: Write failing non-sentence cognition tests**

Add:

```python
def test_inner_voice_accepts_preverbal_cognition_forms(self):
    output = {
        "role": "Greg",
        "body": [],
        "voice": [],
        "inner_voice": [
            {"form": "image", "value": "ledger / red numbers"},
            {"form": "memory_fragment", "value": "Senna's hand on the table"},
            {"form": "half_word", "value": "Wait"},
            {"form": "impulse", "value": "leave"},
            {"form": "calculation", "value": "six gold -> four already sunk"},
            {"form": "sensory_hook", "value": "broom bristles stop"},
            {"form": "unfinished_thought", "value": "If he knows..."},
        ],
    }
    engine.validate_performance_output(output)
```

- [ ] **Step 3: Run focused tests and verify RED**

```bash
python -m unittest tests.test_rehearsal_engine -v
```

Expected: failures because channel visibility and cognition-form validation do not exist.

- [ ] **Step 4: Implement channel ownership and cognition forms**

Use:

```python
GREG_PERFORMANCE_CHANNELS = ("body", "voice", "inner_voice")
DEFAULT_PERFORMANCE_CHANNELS = ("body", "voice")
INNER_VOICE_FORMS = {
    "sentence",
    "fragment",
    "image",
    "memory_fragment",
    "association",
    "half_word",
    "impulse",
    "calculation",
    "wrong_inference",
    "sensory_hook",
    "unfinished_thought",
    "bodily_anticipation",
    "emotional_recoil",
    "recognition",
}
```

`compile_actor_packet` assigns three channels only when `role == "Greg"` and `actor_name == "Nico"`. Other actors receive BODY and VOICE only.

`validate_performance_output` requires `inner_voice` only to be a list of typed internal events with a valid `form` and nonempty `value`. It must not require punctuation, complete sentences, or grammatical prose.

`actor_observable_view` must drop `inner_voice` unconditionally when the observed role is Greg and the observer is another actor. It may never infer a private field into actor context.

`novelizer_performance_view` returns BODY, VOICE, and INNER VOICE for Greg.

- [ ] **Step 5: Add a telepathy regression test**

Test that an Antonius take cannot cite `source_channel="inner_voice"` as an observed stimulus. Add validation that rejects actor outputs whose `observed_inputs` contain another actor's private channel.

- [ ] **Step 6: Run focused tests and verify GREEN**

```bash
python -m unittest tests.test_rehearsal_engine -v
```

Expected: pass.

- [ ] **Step 7: Commit Task 3**

```bash
git add scripts/rehearsal_engine.py tests/test_rehearsal_engine.py
git commit -m "Make Greg inner voice private performance state"
```

---

### Task 4: Add frozen take-variance groups

**Files:**
- Modify: `scripts/rehearsal_engine.py`
- Modify: `tests/test_rehearsal_engine.py`

**Interfaces:**
- Produces: `build_take_spec(mode: str, *, take_id: str, memory_snapshot_id: str, direction: str | None = None, variance_group_id: str | None = None) -> dict`
- Produces: `validate_variance_group(takes: list[dict]) -> None`
- Produces: `stable_variance_findings(takes: list[dict]) -> list[dict]`

- [ ] **Step 1: Write failing variance tests**

Add tests equivalent to:

```python
def test_variance_siblings_require_same_frozen_memory_snapshot(self):
    takes = [
        engine.build_take_spec("free", take_id="free-a", memory_snapshot_id="mem-1", variance_group_id="v1"),
        engine.build_take_spec("free", take_id="free-b", memory_snapshot_id="mem-2", variance_group_id="v1"),
    ]
    with self.assertRaisesRegex(ValueError, "memory snapshot"):
        engine.validate_variance_group(takes)


def test_variance_siblings_cannot_carry_sibling_context(self):
    takes = [
        {
            "mode": "free",
            "take_id": "free-a",
            "variance_group_id": "v1",
            "memory_snapshot_id": "mem-1",
            "sibling_take_context": ["free-b"],
        }
    ]
    with self.assertRaisesRegex(ValueError, "sibling"):
        engine.validate_variance_group(takes)
```

- [ ] **Step 2: Run focused tests and verify RED**

```bash
python -m unittest tests.test_rehearsal_engine -v
```

Expected: failures because variance helpers do not exist.

- [ ] **Step 3: Implement frozen variance metadata validation**

`validate_variance_group` must enforce:

- all takes share one nonempty `variance_group_id`
- all takes share one nonempty `memory_snapshot_id`
- every `take_id` is unique
- no take contains sibling outputs, sibling context, or sibling findings
- DIRECTED takes contain their explicit direction

`stable_variance_findings` may count repeated finding IDs/categories across independently generated takes but must label the result `rehearsal_evidence`, never `canon_support`.

- [ ] **Step 4: Run focused tests and verify GREEN**

```bash
python -m unittest tests.test_rehearsal_engine -v
```

Expected: pass.

- [ ] **Step 5: Commit Task 4**

```bash
git add scripts/rehearsal_engine.py tests/test_rehearsal_engine.py
git commit -m "Add frozen REHEARSAL take variance"
```

---

### Task 5: Generalize exact-source prose return for normal FREE production

**Files:**
- Create: `scripts/apply_rehearsal_returns.py`
- Create: `tests/test_apply_rehearsal_returns.py`
- Preserve unchanged: `scripts/apply_rehearsal_overtuned_calibration.py`
- Create: `.github/workflows/rehearsal-free-returns-001-020.yml`

**Interfaces:**
- Produces: `apply_patch_to_text(text: str, patch: dict, *, target_branch: str, policy_mode: str = "production") -> tuple[str, dict]`
- Produces: `apply_manifest(root: str | Path, manifest: dict, *, write: bool = False) -> dict`
- Manifest mode for normal campaign: `free_production`

- [ ] **Step 1: Write failing generic return tests**

Create tests proving:

```python
def test_free_production_manifest_accepts_inner_voice_prose_surface(self):
    # candidate is actor-preferred, lock-preserved, reader-pass, exact-source matched,
    # target branch is editor/rehearsal-simulation-engine, and changed surfaces are soft.
    ...


def test_free_production_manifest_rejects_main_target(self):
    ...


def test_free_production_manifest_rejects_hard_story_surface(self):
    ...
```

Use a temporary root with `chapters/005.html` so the test proves exact one-match replacement and report provenance.

- [ ] **Step 2: Run generic return tests and verify RED**

```bash
python -m unittest tests.test_apply_rehearsal_returns -v
```

Expected: import failure because `scripts/apply_rehearsal_returns.py` does not exist.

- [ ] **Step 3: Implement the generic return runner by extracting the proven pattern**

Copy only the general exact-source behavior from `scripts/apply_rehearsal_overtuned_calibration.py`:

- exact `before` match count must equal one
- production policy must approve the candidate
- patch report records `actor`, `role`, `take_id`, `variance_group_id`, `changed_surfaces`, `reason`, lock status, reader status, source match, and policy scope
- `--write` is explicit
- dry-run writes a report but does not modify chapter HTML

Do not delete or reinterpret historical overtuned artifacts.

- [ ] **Step 4: Extend soft prose surfaces for Greg cognition returns**

Add only prose-level surfaces, not private state itself:

```python
"internal_dialogue",
"narration_rhythm",
"attention_order",
"sensory_emphasis",
"memory_intrusion",
```

Private `inner_voice` rehearsal state may justify those prose changes but is not itself a canon surface.

- [ ] **Step 5: Run return tests and verify GREEN**

```bash
python -m unittest tests.test_apply_rehearsal_returns -v
python -m unittest tests.test_rehearsal_engine -v
```

Expected: pass.

- [ ] **Step 6: Create the branch self-applying workflow**

Base `.github/workflows/rehearsal-free-returns-001-020.yml` on `.github/workflows/rehearsal-overtuned-calibration-001-020.yml` but invoke `scripts/apply_rehearsal_returns.py` and the Nico campaign manifest.

The workflow must:

1. verify the branch is `editor/rehearsal-simulation-engine`
2. dry-run the entire manifest
3. derive expected patch count from the manifest rather than hardcoding it
4. apply all exact-source patches
5. reject changed chapter files outside the manifest's declared chapter set
6. reject hard-surface leakage
7. reject em dashes in changed prose
8. run `python -m unittest discover -s tests -p 'test_*.py'`
9. run `python scripts/performance_roundtrip_references.py --check`
10. run `python scripts/project_check.py showcase`
11. commit generated chapter prose and the final report only when every gate passes

- [ ] **Step 7: Commit Task 5**

```bash
git add scripts/apply_rehearsal_returns.py tests/test_apply_rehearsal_returns.py .github/workflows/rehearsal-free-returns-001-020.yml scripts/rehearsal_engine.py
git commit -m "Add production REHEARSAL prose return path"
```

---

### Task 6: Run Nico's canon 001-020 INNER VOICE rehearsal campaign

**Files:**
- Read: `chapters/001.html` through `chapters/020.html`
- Read/reuse: `state/editorial/rehearsal/campaigns/canon-001-020.json`
- Read/reuse: `state/editorial/rehearsal/campaigns/canon-001-020-overtuned-report.json`
- Create: `state/editorial/rehearsal/campaigns/canon-001-020-nico-inner-voice.json`
- Create: `state/editorial/rehearsal/campaigns/canon-001-020-nico-inner-voice.md`
- Create: `state/editorial/rehearsal/campaigns/canon-001-020-nico-inner-voice-returns.json`
- Modify after accepted evidence only: `state/editorial/rehearsal/relationship-memory.json`

**Interfaces:**
- Campaign uses FAITHFUL control and FREE take for Greg-heavy scenes.
- Disputed/high-leverage scenes use one frozen variance group.
- DIRECTED is used only for a named question such as `inner_voice`, `minimal`, `pressure`, or `voice_collision`.
- Every Greg performance records BODY, VOICE, and private INNER VOICE.

- [ ] **Step 1: Select Greg-heavy scenes from actual canon 001-020**

Use current branch prose, not stale campaign quotes. Prioritize scenes where Greg's thought rhythm materially affects reading:

- Antonius debt/ledger exchanges
- sword training and Jorren instruction
- Arlo workshop/system-recognition scenes
- Hessa training/procedure scenes
- Alden investigation scenes
- moments where Greg's analysis outruns the immediate social situation

Do not force every chapter to receive a rewrite.

- [ ] **Step 2: Freeze the relationship-memory snapshot for each variance group**

Persist a `memory_snapshot_id` before generating sibling takes. FREE A and FREE B receive identical supported/hypothesis memory and cannot see each other's output.

- [ ] **Step 3: Perform Nico through BODY / VOICE / INNER VOICE**

INNER VOICE must deliberately sample both verbal and nonverbal forms from the approved set. A scene may include items such as:

```json
{"form":"sensory_hook","value":"broom bristles stop"}
{"form":"calculation","value":"today's debt != total debt"}
{"form":"wrong_inference","value":"He bought the bluff."}
{"form":"memory_fragment","value":"Senna: learn quieter"}
{"form":"impulse","value":"push"}
{"form":"unfinished_thought","value":"If Antonius already knows..."}
```

These are performance state, not required final prose sentences.

- [ ] **Step 4: Enforce the private-state boundary during ensemble takes**

Before another actor responds, supply that actor only observable BODY/VOICE views. Record any Greg thought that affects another actor only after Nico externalizes it through speech, action, hesitation, expression, posture, object use, or another observable behavior.

Reject any take that allows a non-Greg actor to respond directly to private cognition.

- [ ] **Step 5: Run critics on each candidate**

At minimum record:

- dramatic lock
- reader/speaker legibility
- motif recursion
- stage-direction density
- inner-voice quality
- thought-density/scene-smothering check
- retrospective-analysis-vs-live-cognition check
- source win vs candidate win

- [ ] **Step 6: Build exact-source prose returns only for clear wins**

Allow thought performance to reshape:

- paragraph rhythm
- attention order
- sentence length
- omission
- interruption
- memory intrusion
- sensory emphasis
- spoken dialogue timing
- explicit internal dialogue where useful

Do not add a thought merely because Nico generated one. The final prose should preserve cognition shape, not prove the rehearsal contained an INNER VOICE track.

- [ ] **Step 7: Update relationship memory with correct trust lanes**

Accepted prose returns may add supported relationship memory with `source_type="accepted_prose"`.

Rehearsal-only recurring discoveries go to the `hypothesis` lane with `source_type="rehearsal"`.

Do not count sibling variance takes as independent canon support.

- [ ] **Step 8: Commit campaign evidence and return manifest**

```bash
git add state/editorial/rehearsal/campaigns/canon-001-020-nico-inner-voice.json \
        state/editorial/rehearsal/campaigns/canon-001-020-nico-inner-voice.md \
        state/editorial/rehearsal/campaigns/canon-001-020-nico-inner-voice-returns.json \
        state/editorial/rehearsal/relationship-memory.json
git commit -m "Rehearse Greg inner voice through canon 20"
```

---

### Task 7: Apply, verify, and document the Nico prose returns

**Files:**
- Generated modifications: only chapter files declared in `canon-001-020-nico-inner-voice-returns.json`
- Generated: campaign return report
- Modify: PR #160 body
- Create or update: `state/editorial/rehearsal/campaigns/canon-001-020-nico-inner-voice-calibration.md`

**Interfaces:**
- Consumes: generic production return runner from Task 5
- Consumes: Nico return manifest from Task 6
- Produces: validated branch prose and campaign calibration record

- [ ] **Step 1: Dry-run the entire Nico return manifest**

Run:

```bash
python scripts/apply_rehearsal_returns.py \
  --manifest state/editorial/rehearsal/campaigns/canon-001-020-nico-inner-voice-returns.json
```

Expected: every exact source anchor matches once; no chapter is modified without `--write`.

- [ ] **Step 2: Trigger the self-applying FREE returns workflow**

The workflow must apply all approved patches, run full project validation, and create a bot commit only when every gate passes.

- [ ] **Step 3: Independently validate the resulting branch head**

Run or confirm the normal PR workflow executes:

```bash
python -m unittest discover -s tests -p 'test_*.py'
python scripts/performance_roundtrip_references.py --check
python scripts/project_check.py showcase
```

Expected: all green.

- [ ] **Step 4: Audit private-state leakage in persisted take evidence**

Confirm actor-facing views do not contain another actor's private `inner_voice`. Full private cognition may exist only in Nico take evidence and novelizer/critic records.

- [ ] **Step 5: Read the changed scenes cold**

Calibrate for the new failure mode: too much beautifully written internal monologue. Specifically check whether nonverbal cognition survives as rhythm/attention/omission instead of being converted into extra sentences.

Also retain the prior overtune calibration checks:

- no repeated signature prop as emotional subtitle
- no stage-direction transcription
- no voice collision
- no new speaker-ownership bugs

- [ ] **Step 6: Record calibration findings**

Write `canon-001-020-nico-inner-voice-calibration.md` with:

- chapters/scenes changed
- number and type of prose returns
- source wins
- candidate wins
- variance findings
- supported vs hypothesis memory updates
- examples where private cognition improved prose without becoming explicit sentences
- examples where Nico generated thought that the novelizer correctly omitted
- any overthinking/over-monologue failure signals

- [ ] **Step 7: Update PR #160 and keep it draft**

Document the new architecture and Nico campaign. Explicitly state that `main` remains untouched unless a later merge decision is made.

- [ ] **Step 8: Final verification before claiming completion**

Confirm:

```bash
python -m unittest discover -s tests -p 'test_*.py'
python scripts/performance_roundtrip_references.py --check
python scripts/project_check.py showcase
```

Then inspect the PR changed-file list and confirm all chapter edits are within the declared Nico campaign return set.

- [ ] **Step 9: Commit final calibration documentation**

```bash
git add state/editorial/rehearsal/campaigns/canon-001-020-nico-inner-voice-calibration.md
git commit -m "Document Nico inner voice calibration"
```
