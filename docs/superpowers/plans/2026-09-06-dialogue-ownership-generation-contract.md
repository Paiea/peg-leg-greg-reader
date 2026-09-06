# Dialogue Ownership Generation Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prevent new Peg-Leg Greg dialogue-ownership debt by making dramatic ownership part of scene generation and by rejecting clear mixed-owner dialogue paragraphs before a new chapter ships.

**Architecture:** Reuse `scripts/generate_light.py::load_all_sources()` as the canonical chapter resolver. Add a read-only ownership checker that classifies dialogue paragraphs as `error`, `review`, or clean, integrate its latest-chapter summary into `project_check.py manuscript`, and run strict latest-chapter validation early in the existing Light workflow. Graduate the generation rule into the Manuscript Engine and prose authorities so workers build character-owned beats before prose instead of relying on cleanup afterward.

**Tech Stack:** Python 3.12, `unittest`, existing PLG manuscript/source loaders, GitHub Actions YAML, Markdown project authority.

**Spec:** `docs/superpowers/specs/2026-09-06-dialogue-ownership-generation-contract-design.md`

## Global Constraints

- Do not rewrite historical manuscript prose as part of this feature.
- One dramatic owner per dialogue paragraph is the default, not one sentence per paragraph.
- Same-owner dialogue and action may remain together when natural.
- Different-owner action, reaction, interiority, or re-entry normally starts a new paragraph.
- Preserve current dialogue wording by default; paragraph scaffolding is more disposable than spoken content.
- The checker is read-only and must never auto-rewrite canon.
- Ambiguous identity must become `review`, not a guessed speaker.
- Straight and smart double quotes must both be recognized.
- Formatted/quoted documents and malformed quote structures must be protected from hard false positives.
- Reuse existing source authority and project-check architecture; do not create a parallel scene database or manuscript state system.
- No em dashes in newly written manuscript guidance examples.

---

### Task 1: Focused Dialogue Ownership Checker

**Files:**
- Create: `scripts/dialogue_ownership_check.py`
- Create: `tests/test_dialogue_ownership_check.py`

**Interfaces:**
- Consumes: `generate_light.load_all_sources() -> dict[int, Chapter]` and each `Chapter.prose_html`.
- Produces: `Finding` dataclass, `inspect_paragraph(text, chapter, paragraph_index) -> list[Finding]`, `inspect_chapter(chapter) -> list[Finding]`, `check_chapters(chapters, numbers) -> dict`, and CLI flags `--chapter N`, `--latest`, `--range N-N`, `--strict`, `--json`.
- A finding has `severity` (`error` or `review`), `code`, `chapter`, `paragraph`, and `excerpt`.

- [ ] **Step 1: Write failing ownership regressions**

Create `tests/test_dialogue_ownership_check.py` with `unittest` cases covering at minimum:

```python
from scripts.dialogue_ownership_check import inspect_text


def codes(text):
    return [(f.severity, f.code) for f in inspect_text(text, chapter=500)]


class DialogueOwnershipCheckTests(unittest.TestCase):
    def test_same_owner_dialogue_and_action_is_clean(self):
        self.assertEqual(codes('"Fine," Antonius said. He counted the silver.'), [])

    def test_greg_other_greg_is_error(self):
        self.assertIn(("error", "mixed_explicit_owners"), codes('"You," I said. She stared. I smiled.'))

    def test_leave_and_return_is_error(self):
        text = '"How much?" Antonius asked. I named the number. Jorren laughed. Antonius looked at me. "Collateral?"'
        self.assertIn(("error", "mixed_explicit_owners"), codes(text))

    def test_two_named_non_greg_owners_is_error(self):
        self.assertIn(("error", "mixed_explicit_owners"), codes('"Enough," Antonius said. Jorren laughed.'))

    def test_descriptive_actor_is_error(self):
        self.assertIn(("error", "mixed_explicit_owners"), codes('"How much?" Antonius asked. The man with the scar laughed.'))

    def test_smart_quotes_are_detected(self):
        self.assertIn(("error", "mixed_explicit_owners"), codes('Alden said, “You really were bad.” I looked at him.'))

    def test_other_speaker_plus_greg_interior_is_error(self):
        self.assertIn(("error", "mixed_explicit_owners"), codes('“Do I know you?” Sella asked. I knew her future immediately.'))

    def test_ambiguous_pronoun_is_review(self):
        result = codes('"Fine," Antonius said. He looked at him.')
        self.assertIn(("review", "ambiguous_pronoun_owner"), result)

    def test_malformed_quotes_are_review(self):
        self.assertIn(("review", "unbalanced_quotes"), codes('ring the bell and bar the hall...” Different words.'))

    def test_formatted_quoted_block_is_review(self):
        self.assertIn(("review", "formatted_or_embedded_quote"), codes('**The note said, "Again?" He left.**'))

    def test_narration_without_dialogue_is_ignored(self):
        self.assertEqual(codes('Antonius crossed the room. Jorren laughed.'), [])

    def test_separate_rapid_dialogue_paragraphs_are_clean(self):
        text = '"Fine," Antonius said.\n\nI nodded.\n\n"Good," he said.'
        self.assertNotIn(("error", "mixed_explicit_owners"), codes(text))
```

- [ ] **Step 2: Run the focused test and verify RED**

Run:

```bash
python -m unittest tests.test_dialogue_ownership_check -v
```

Expected: import failure because `scripts/dialogue_ownership_check.py` does not exist yet.

- [ ] **Step 3: Implement the minimal read-only checker**

Implement:

```python
@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    chapter: int
    paragraph: int
    excerpt: str
```

Use HTML paragraph extraction for loaded chapters, normalize HTML entities, recognize straight and smart quote pairs, and classify explicit owners using conservative speech/action patterns. Treat `I`/`my` as Greg; named actors and descriptive `the ...` actors as distinct explicit owners. Do not infer ambiguous third-person pronouns across owners. If quote structure is malformed, Markdown-like formatting is embedded, or the paragraph cannot be safely classified, emit `review` rather than `error`.

CLI behavior:

```bash
python scripts/dialogue_ownership_check.py --latest --json
python scripts/dialogue_ownership_check.py --chapter 492 --strict
python scripts/dialogue_ownership_check.py --range 490-492 --json
```

`--strict` exits nonzero for any `error` or `review` in the selected chapter(s), because a forward chapter must be consciously inspected before shipping. Non-strict audit mode returns zero and reports findings.

- [ ] **Step 4: Run focused tests and verify GREEN**

Run:

```bash
python -m unittest tests.test_dialogue_ownership_check -v
```

Expected: all dialogue ownership tests pass.

- [ ] **Step 5: Commit the checker task**

Commit message:

```text
Add forward dialogue ownership checker
```

---

### Task 2: Integrate Ownership Into Project Validation

**Files:**
- Modify: `scripts/project_check.py`
- Test: `tests/test_project_check_dialogue_ownership.py`

**Interfaces:**
- Consumes: `dialogue_ownership_check.check_chapters()` and `generate_light.load_all_sources()`.
- Produces additional `manuscript` payload keys: `latest_canonical_chapter`, `dialogue_ownership.errors`, `dialogue_ownership.reviews`, `dialogue_ownership.findings`.

- [ ] **Step 1: Write failing project-check integration tests**

Create a temporary repository fixture containing a running manuscript with one clean earlier chapter and a latest chapter containing a known mixed-owner paragraph. Assert that `manuscript_check(root)` reports the latest chapter number and ownership counts while preserving existing duplicate/em-dash/stale-name keys.

- [ ] **Step 2: Run the integration test and verify RED**

Run:

```bash
python -m unittest tests.test_project_check_dialogue_ownership -v
```

Expected: missing dialogue-ownership payload.

- [ ] **Step 3: Add latest-chapter ownership reporting to `manuscript_check`**

Load canonical chapters through existing source resolution and inspect only the latest canonical chapter for the normal `manuscript` check. This keeps the routine gate cheap and forward-focused. The dedicated checker retains range/audit support for historical review.

The payload shape must be stable:

```python
"latest_canonical_chapter": latest,
"dialogue_ownership": {
    "errors": error_count,
    "reviews": review_count,
    "findings": [finding.as_dict() for finding in findings],
},
```

The ordinary project check should fail when the latest chapter contains either ownership errors or unresolved reviews.

- [ ] **Step 4: Run focused tests and existing project checks**

Run:

```bash
python -m unittest tests.test_project_check_dialogue_ownership -v
python scripts/project_check.py manuscript
```

Expected: focused tests pass; current repository output is valid JSON. If current latest canon contains a legacy finding, classify it and adjust only detector false positives, never manuscript prose in this feature.

- [ ] **Step 5: Commit the project-check integration**

Commit message:

```text
Gate latest manuscript dialogue ownership
```

---

### Task 3: Graduate the Generation Contract Into Durable Manuscript Authority

**Files:**
- Modify: `state/MANUSCRIPT_ENGINE_PLAYBOOK.md`
- Modify: `state/MANUSCRIPT_WORKFLOW.md`
- Modify: `state/PROSE_PLAYBOOK.md`
- Modify: `state/STORY_ANTI_PATTERNS.md`

**Interfaces:**
- Produces durable forward-generation rules read by fresh Manuscript Engine workers.

- [ ] **Step 1: Update the private chapter contract**

In `MANUSCRIPT_ENGINE_PLAYBOOK.md`, add scene beat ownership to Section 14. Before dialogue-heavy scenes, privately identify owner changes at the level needed to avoid mixed-owner paragraphs. State explicitly that this is disposable steering, not a durable scene outline.

- [ ] **Step 2: Update drafting and light-pass behavior**

Add the governing rule:

```text
ONE CLEAR DRAMATIC OWNER PER DIALOGUE PARAGRAPH BY DEFAULT.
```

Clarify that same-owner speech/action may stay together, different-owner action/reaction/interiority normally splits, leave-and-return sequences split, and the rule must not create one-sentence paragraph spam.

Add a focused ownership sweep to Section 15 using the five questions from the approved spec.

- [ ] **Step 3: Update verification**

Add:

```bash
python scripts/dialogue_ownership_check.py --latest --strict
```

to the required pre-ship verification contract.

- [ ] **Step 4: Update `MANUSCRIPT_WORKFLOW.md`**

Modify the normal chapter transaction so the light chapter contract includes owner sequence when dialogue-bearing scenes need it, the LIGHT drafting pass includes ownership, and validation invokes the strict latest-chapter checker before commit.

- [ ] **Step 5: Update prose and anti-pattern authority**

In `PROSE_PLAYBOOK.md`, add a `Dialogue paragraph ownership` subsection explaining the one-owner rule, Greg interiority, leave-and-return patterns, crowd handling, and the interaction with voice variance. In `STORY_ANTI_PATTERNS.md`, add `Mixed-owner dialogue paragraphs` as a concise known failure mode.

- [ ] **Step 6: Verify authority language does not contradict paragraph-rhythm guidance**

Confirm the new text explicitly says ownership is not a one-sentence-paragraph rule and preserves fuller natural paragraphs.

- [ ] **Step 7: Commit durable authority**

Commit message:

```text
Make dialogue ownership part of scene generation
```

---

### Task 4: Add the GitHub Actions Backstop

**Files:**
- Modify: `.github/workflows/light-edition.yml`
- Test: `tests/test_dialogue_ownership_workflow.py`

**Interfaces:**
- Consumes: `python scripts/dialogue_ownership_check.py --latest --strict`.
- Produces: a workflow gate before any reader generation/promotion steps.

- [ ] **Step 1: Write a failing workflow contract test**

Assert that `.github/workflows/light-edition.yml` contains a named step such as:

```yaml
- name: Validate latest dialogue ownership
  run: python scripts/dialogue_ownership_check.py --latest --strict
```

and that it occurs after the existing unit-test step but before `Process illustration production state` and all Light/Illustrated generation commands.

- [ ] **Step 2: Run workflow test and verify RED**

Run:

```bash
python -m unittest tests.test_dialogue_ownership_workflow -v
```

Expected: step missing.

- [ ] **Step 3: Add the early workflow gate**

Also add `scripts/dialogue_ownership_check.py` to the workflow path trigger list so checker changes exercise the workflow.

- [ ] **Step 4: Run workflow test and focused checker tests**

Run:

```bash
python -m unittest tests.test_dialogue_ownership_workflow tests.test_dialogue_ownership_check -v
```

Expected: pass.

- [ ] **Step 5: Commit workflow integration**

Commit message:

```text
Backstop reader builds with dialogue ownership
```

---

### Task 5: Full Verification and Safe Integration

**Files:**
- Verify all files above; do not modify manuscript prose.

**Interfaces:**
- Produces a mergeable PR based on current `main` with only generation-contract tooling, authority, tests, docs, and workflow changes.

- [ ] **Step 1: Run the complete repository test suite**

Run:

```bash
python -m unittest discover -s tests -p 'test_*.py'
```

Expected: zero failures.

- [ ] **Step 2: Run focused project checks**

Run:

```bash
python scripts/dialogue_ownership_check.py --latest --strict
python scripts/project_check.py manuscript
python scripts/project_check.py showcase
```

Expected: all pass on the branch. If strict latest validation exposes a true pre-existing current-chapter issue, do not rewrite the chapter in this feature; document the blocker and coordinate with the historical cleanup worker before merge.

- [ ] **Step 3: Verify branch scope**

Compare with current `main`. Allowed paths are the spec/plan, checker/tests, `project_check.py`, the four manuscript/craft authorities, and `light-edition.yml`. Historical chapter prose, running manuscript prose, showcase manifest, art, and reader-generated pages must remain untouched.

- [ ] **Step 4: Reconcile current main if it moved**

If `main` advanced, rebuild/rebase the small feature changes onto current authority rather than merging a stale branch over newer files. Re-run all tests after reconciliation.

- [ ] **Step 5: Open and merge the PR**

PR title:

```text
Prevent new dialogue ownership regressions
```

Merge only after current-main comparison is clean and verification is green.

- [ ] **Step 6: Verify accepted authority**

Fetch `main` after merge and confirm the checker, durable scene-generation rule, and Light workflow backstop are present.
