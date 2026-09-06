# Dialogue Ownership Pass Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a showcase-aware dialogue-ownership audit and exact-patch workflow, repair visible Chapters 1-491, and prevent new false-attribution regressions from entering published PLG prose.

**Architecture:** Add a conservative candidate scanner over exact chapter prose, using `publishing/showcase_chapters.json` as the only visibility authority. The scanner never rewrites prose. Reviewed candidates become exact paragraph replacements through deterministic patch application, while master prose guidance and publishing validation make speaker ownership a durable invariant.

**Tech Stack:** Python 3.12 standard library, `unittest`, existing PLG HTML chapter surfaces, existing showcase helper and dialogue patch machinery, GitHub Actions.

**Spec:** `state/editorial/DIALOGUE_OWNERSHIP_PASS.md`

## Global Constraints

- Current scope endpoint at branch creation: Chapter 491.
- Repair currently showcased chapters only; hidden canon stays untouched unless later showcased.
- `publishing/showcase_chapters.json` is visibility authority.
- Exact manuscript prose outranks summaries/editorial notes.
- Candidate heuristics never auto-rewrite manuscript prose.
- Preserve spoken dialogue payload unless a separately reviewed edit explicitly changes it.
- Preserve plot, canon, characterization, money, magic, body continuity, chronology, scene outcomes, illustrations, and navigation.
- Prefer simple `said` / `asked` when attribution is the needed repair.
- Do not mechanically split every dialogue line into a separate paragraph.
- NO EM DASHES in manuscript prose.

---

### Task 1: Dialogue ownership candidate detector

**Files:**
- Create: `scripts/dialogue_ownership.py`
- Modify: `tests/test_dialogue_publish_boundary.py`

**Interfaces:**
- Produces: `OwnershipCandidate` dataclass and `scan_paragraphs(paragraphs: list[str]) -> list[OwnershipCandidate]`.
- Candidate fields: `paragraph_index`, `rule`, `confidence`, `previous`, `current`, `following`, `fingerprint`.

- [ ] **Step 1: Write the failing regression tests**

Add tests that import `scan_paragraphs` and prove the detector catches the live Chapter 2 shape while leaving an ordinary same-speaker action beat reviewable rather than rewriting it.

```python
from dialogue_ownership import scan_paragraphs


def test_flags_possible_speaker_switch_inside_one_paragraph(self):
    paragraphs = [
        '"To what?"',
        '"Your age." He smiled. "How old did you expect me to be?"',
        '"Richer."',
    ]
    candidates = scan_paragraphs(paragraphs)
    self.assertTrue(any(
        item.rule == "possible_multi_speaker_paragraph"
        and item.paragraph_index == 1
        for item in candidates
    ))


def test_flags_action_after_untagged_dialogue_for_review(self):
    paragraphs = ['"Doing what?" Rusk pointed at the sack.']
    candidates = scan_paragraphs(paragraphs)
    self.assertTrue(any(
        item.rule == "untagged_dialogue_followed_by_action"
        for item in candidates
    ))
```

- [ ] **Step 2: Run the PR test workflow and verify RED**

Run through the existing `dialogue-attribution-live.yml` PR path by modifying `tests/test_dialogue_publish_boundary.py`.

Expected: workflow fails because `dialogue_ownership` does not exist yet.

- [ ] **Step 3: Implement minimal detector**

Create `scripts/dialogue_ownership.py` with:

```python
@dataclass(frozen=True)
class OwnershipCandidate:
    paragraph_index: int
    rule: str
    confidence: str
    previous: str
    current: str
    following: str
    fingerprint: str


def scan_paragraphs(paragraphs: list[str]) -> list[OwnershipCandidate]:
    ...
```

Detector rules should be intentionally conservative and context-emitting. Do not infer the true speaker or rewrite text.

- [ ] **Step 4: Run tests and verify GREEN**

Run:

`python -m unittest tests.test_dialogue_publish_boundary -v`

Expected: PASS.

- [ ] **Step 5: Commit**

Commit message:

`editor: detect dialogue ownership candidates`

---

### Task 2: Showcase-aware whole-manuscript audit surface

**Files:**
- Create: `scripts/audit_dialogue_ownership.py`
- Create: `tests/test_dialogue_ownership_audit.py`
- Create generated authority directory: `state/editorial/dialogue-ownership-pass/`

**Interfaces:**
- Consumes: `scan_paragraphs`, `scripts/showcase.py`, `publishing/showcase_chapters.json`, `chapters/*.html`.
- Produces: deterministic JSON/Markdown candidate reports.

- [ ] **Step 1: Write failing showcase-scope tests**

```python
def test_audit_skips_hidden_canon(tmp_path):
    ...
    self.assertEqual([item["canonical_chapter"] for item in report], [1, 3])


def test_audit_keeps_neighbor_context_and_showcase_number(tmp_path):
    ...
    self.assertEqual(item["showcase_chapter"], 2)
    self.assertIn("previous", item)
    self.assertIn("following", item)
```

- [ ] **Step 2: Verify tests fail because audit module is missing**

Run:

`python -m unittest tests.test_dialogue_ownership_audit -v`

Expected: FAIL on missing module/function.

- [ ] **Step 3: Implement exact HTML prose extraction and manifest scoping**

Provide functions:

```python
def extract_prose_paragraphs(document: str) -> list[str]: ...
def audit_chapters(root: Path, manifest_path: Path) -> dict: ...
def write_reports(report: dict, json_path: Path, md_path: Path) -> None: ...
```

Rules:
- read only `<article class="prose">` paragraphs;
- strip HTML tags and unescape entities;
- use canonical chapter filenames as source identity;
- derive visible order from `build_showcase_map`;
- hidden chapters produce no candidates;
- report metadata records hidden count, visible count, endpoint, scanner version, and candidate totals by rule/confidence.

- [ ] **Step 4: Run audit tests and whole unittest suite**

Run:

`python -m unittest discover -s tests -v`

Expected: PASS.

- [ ] **Step 5: Generate the first durable candidate report**

Run:

`python scripts/audit_dialogue_ownership.py --root . --json state/editorial/dialogue-ownership-pass/CANDIDATES.json --markdown state/editorial/dialogue-ownership-pass/CANDIDATES.md`

- [ ] **Step 6: Commit**

Commit message:

`editor: add showcase dialogue ownership audit`

---

### Task 3: Durable master guidance

**Files:**
- Modify: `state/PROSE_PLAYBOOK.md`
- Modify: `state/EDITOR_STATE.md`
- Modify: `AGENTS.md`

**Interfaces:**
- Consumes: `state/editorial/DIALOGUE_OWNERSHIP_PASS.md`.
- Produces: permanent drafting/editing rule that future workers must follow.

- [ ] **Step 1: Add the hard ownership rule to PROSE_PLAYBOOK**

Add under dialogue/interiority:

```markdown
### Dialogue paragraph ownership

A foreign action beat must never function as attribution for the current speaker. If an untagged spoken line could be read as belonging to the person performing the attached action, tag the actual speaker with `said` / `asked`. If spoken ownership changes, start the new speaker's turn in a new paragraph. Do not mechanically split every line or invent gestures to avoid tags.
```

- [ ] **Step 2: Add the same invariant to editor hard checks**

`EDITOR_STATE.md` should explicitly require checking foreign-action false attribution during prose edits.

- [ ] **Step 3: Add worker-router prevention language**

`AGENTS.md` should route substantial dialogue work through `state/editorial/DIALOGUE_OWNERSHIP_PASS.md` and state that future manuscript production may not use another character's action as false attribution.

- [ ] **Step 4: Verify documentation references and no contradictory guidance**

Search/fetch the three files and ensure the same rule is expressed consistently.

- [ ] **Step 5: Commit**

Commit message:

`docs: make dialogue ownership a manuscript invariant`

---

### Task 4: Publishing regression gate

**Files:**
- Create: `scripts/validate_dialogue_ownership.py`
- Create: `tests/test_dialogue_ownership_validation.py`
- Modify: `.github/workflows/dialogue-attribution-live.yml`
- Modify other forward/publishing workflow(s) only where they can introduce manuscript prose after inspection.

**Interfaces:**
- Consumes: scanner + current reviewed baseline/report.
- Produces: non-mutating validator with nonzero exit on newly introduced unreviewed ownership candidates.

- [ ] **Step 1: Write failing validator tests**

```python
def test_validator_allows_existing_reviewed_fingerprint(...): ...
def test_validator_rejects_new_candidate_fingerprint(...): ...
def test_validator_ignores_hidden_chapter(...): ...
```

- [ ] **Step 2: Verify RED**

Run targeted unittest module and confirm missing validator behavior.

- [ ] **Step 3: Implement baseline comparison**

The validator must compare current visible candidate fingerprints against reviewed baseline fingerprints. It must not require zero candidates before the repair pass is finished. A new candidate must fail unless explicitly reviewed.

- [ ] **Step 4: Wire validator into prose-producing workflows**

Run validation after generation and before commit/push. Do not let the validator modify prose.

- [ ] **Step 5: Run full suite and `git diff --check`**

Expected: all green.

- [ ] **Step 6: Commit**

Commit message:

`ci: guard dialogue ownership regressions`

---

### Task 5: Exact reviewed patch application

**Files:**
- Create: `scripts/apply_dialogue_ownership_patches.py`
- Create: `tests/test_dialogue_ownership_patches.py`
- Add batches under: `state/editorial/dialogue-ownership-pass/BATCH_*.md`

**Interfaces:**
- Consumes: exact reviewed current/replacement paragraph blocks.
- Produces: deterministic chapter HTML edits only when exact current text matches uniquely.

- [ ] **Step 1: Write failing exact-application tests**

Tests must prove:
- unique exact current paragraph is replaced;
- stale current text fails;
- multiply matching current text fails;
- paragraph-count changes cannot cross non-paragraph markup;
- spoken quote payload remains unchanged for attribution-only patches unless patch metadata explicitly marks a broader reviewed edit;
- no em dash may enter prose.

- [ ] **Step 2: Verify RED**

Run targeted unittest module.

- [ ] **Step 3: Implement thin wrapper over existing strict dialogue patch machinery**

Do not create a second fuzzy matcher. Reuse exact paragraph helpers from `apply_dialogue_attribution_patches.py` where safe; scope batch discovery to `state/editorial/dialogue-ownership-pass/`.

- [ ] **Step 4: Verify GREEN and full suite**

Run:

`python -m unittest discover -s tests -v`

- [ ] **Step 5: Commit**

Commit message:

`editor: apply reviewed dialogue ownership patches`

---

### Task 6: Review and repair currently showcased Chapters 1-491

**Files:**
- Update: `state/editorial/dialogue-ownership-pass/CANDIDATES.json`
- Update: `state/editorial/dialogue-ownership-pass/CANDIDATES.md`
- Create/update: `state/editorial/dialogue-ownership-pass/BATCH_*.md`
- Modify: visible `chapters/*.html` only through exact approved replacements
- Update exact manuscript checkpoint surfaces when project authority requires them; never create a divergent second canon.

**Interfaces:**
- Consumes: compact candidate packets with prev/current/next context.
- Produces: reviewed dispositions and exact repairs.

- [ ] **Step 1: Review in bounded chapter/candidate batches**

For each candidate classify exactly one:

`FIX_TAG / FIX_PARAGRAPH / FIX_BOTH / CLEAR_ALREADY / NEEDS_CONTEXT`

- [ ] **Step 2: Read broader chapter context only for NEEDS_CONTEXT**

Do not spend full-manuscript tokens on candidates that are already provable from compact context.

- [ ] **Step 3: Save exact replacement batches**

Each fix records current text, replacement text, and reason. Preserve dialogue payload wherever possible.

- [ ] **Step 4: Apply exact batches and regenerate audit**

A fixed candidate should disappear or move to an explicitly accepted reviewed state.

- [ ] **Step 5: Continue until every currently visible chapter has a deliberate disposition**

Hidden chapters are recorded as showcase-skipped, not silently forgotten.

- [ ] **Step 6: Commit each bounded reviewed batch**

Prefer small commits that identify chapter range.

---

### Task 7: Final verification and merge readiness

**Files:**
- Update: `state/editorial/DIALOGUE_OWNERSHIP_PASS.md`
- Update: final candidate/baseline report

- [ ] **Step 1: Run complete test suite**

`python -m unittest discover -s tests -v`

Expected: PASS.

- [ ] **Step 2: Run ownership audit and validator**

Confirm no new unreviewed visible-canon candidates relative to reviewed authority.

- [ ] **Step 3: Run prose integrity checks**

- no em dashes in changed prose;
- exact chapter/navigation/illustration markup preserved;
- hidden canon untouched by the repair pass;
- no dialogue payload changes without explicit reviewed reason.

- [ ] **Step 4: Sample-read early/middle/late and multi-speaker chapters**

Include Chapter 2 regression plus several dialogue-heavy later chapters. Conversational geography should be effortless without excessive tagging or paragraph fragmentation.

- [ ] **Step 5: Update completion state and restart prompt**

Record reviewed endpoint, candidate totals, remaining accepted exceptions, and future-validator contract.

- [ ] **Step 6: Commit**

Commit message:

`editor: complete showcased dialogue ownership pass`
