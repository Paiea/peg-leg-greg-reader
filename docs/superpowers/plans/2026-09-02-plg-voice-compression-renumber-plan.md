# PLG Voice, Compression, and Renumber Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build durable character-voice authority, audit Chapters 260-299 for compression/merging/cuts, and prepare a safe path for renumbering without canon drift.

**Architecture:** Keep voice authority in focused files under `state/voices/`, keep structural judgments in one recent-run audit, and extend the existing Editor/Prose systems rather than creating a parallel editor. Structural edits happen on `editor/voice-compression-pass`; renumbering happens only after the structural map is frozen.

**Tech Stack:** Markdown state files, GitHub branch workflow, existing Peg-Leg Greg manuscript/editorial authority.

**Spec:** `docs/superpowers/specs/2026-09-02-plg-voice-compression-renumber-design.md`

## Global Constraints

- Exact manuscript prose remains authority for what happened.
- Renumbering is explicitly allowed but must be atomic after structural decisions settle.
- Do not change magic results/counts, money facts, body continuity, relationship status, protected uncertainty, or scene outcomes merely to compress.
- Preserve quiet-life value; cut repetition, not mundanity.
- Use no em dashes in manuscript prose.
- Shared colloquial language is allowed when culturally or relationally consistent.
- Dialogue tags should err toward clarity in group scenes.

---

### Task 1: Create Voice Library Core

**Files:**
- Create: `state/voices/INDEX.md`
- Create: `state/voices/GREG.md`
- Create: `state/voices/LYSSA.md`
- Create: `state/voices/HESSA.md`
- Create: `state/voices/RINNA.md`
- Create: `state/voices/TEREN.md`
- Create: `state/voices/NESSA.md`
- Create: `state/voices/HARA.md`
- Create: `state/voices/MAREK.md`

**Interfaces:**
- Consumes: `state/CHARACTER_BIBLE.md`, `state/PROSE_PLAYBOOK.md`, exact manuscript dialogue.
- Produces: operational voice pages referenced by future 01/04 workers.

- [ ] Write `INDEX.md` with usage rules, evidence hierarchy, canonical-vs-test-line labeling, tagging policy, and priority roster.
- [ ] Write the eight highest-priority voice pages using manuscript-supported cognition/rhythm/relationship evidence.
- [ ] Include short canonical dialogue examples where reliable evidence is available.
- [ ] Include clearly labeled non-canon voice-test lines only where useful for calibration.
- [ ] Verify pages distinguish cognition rather than relying on catchphrases or accents.
- [ ] Commit as a coherent voice-library foundation.

### Task 2: Extend Voice Library to Recurring Work/Household Cast

**Files:**
- Create: `state/voices/JORI.md`
- Create: `state/voices/DAVIN.md`
- Create: `state/voices/CALA.md`
- Create: `state/voices/MARRA.md`
- Create: `state/voices/JESSA.md`
- Create: `state/voices/OLAN.md`
- Create: `state/voices/SERA.md`
- Create: `state/voices/SEVREN.md`

**Interfaces:**
- Consumes: `state/voices/INDEX.md`, exact manuscript/audit evidence.
- Produces: second-tier recurring voice authority.

- [ ] Write each page with core lens, rhythm, humor, disagreement, information behavior, Greg-specific relationship language, overlap allowed, and anti-flattening warnings.
- [ ] Explicitly prevent practical workers from defaulting to Hessa-style evidence rhetoric unless manuscript evidence supports it.
- [ ] Verify no file invents a formal role, relationship, or linguistic gimmick not established by prose.
- [ ] Commit.

### Task 3: Wire Voice Authority into Existing Editorial Systems

**Files:**
- Modify: `state/PROSE_PLAYBOOK.md`
- Modify: `state/EDITOR_STATE.md`
- Modify: `AGENTS.md`

**Interfaces:**
- Consumes: `state/voices/INDEX.md`.
- Produces: boot/routing rules that make the voice library operational rather than optional trivia.

- [ ] Add compact rule to `PROSE_PLAYBOOK.md`: consult the relevant voice page for substantial recurring-character dialogue; do not read the whole folder every chapter.
- [ ] Add explicit tagging guidance: clarity first, especially in 3+ speaker scenes.
- [ ] Add to `EDITOR_STATE.md` a voice-differentiation check using relevant per-character pages.
- [ ] Add structural-compression permission and a rule that whole-chapter cuts/merges require preserving canon outcome and updating the structural map.
- [ ] Add `state/voices/INDEX.md` to the Character/Prose lane routing in `AGENTS.md` as relevant, not mandatory every-chapter boot reading.
- [ ] Re-read all three files for contradictory instructions.
- [ ] Commit.

### Task 4: Audit Chapters 260-299 Before Rewriting

**Files:**
- Create: `state/editorial/RECENT_COMPRESSION_MAP_260_299.md`

**Interfaces:**
- Consumes: exact checkpoint prose for Chapters 260-299 plus adjacent context and current state.
- Produces: disposition and rationale for every chapter in the window.

- [ ] For each Chapter 263-299 record title, unique value, repeated architecture, voice risks, procedural redundancy, and disposition: KEEP / COMPRESS / MERGE CANDIDATE / CUT CANDIDATE.
- [ ] Identify chapter pairs/triples that perform materially duplicated work.
- [ ] Protect distinct hinges such as claim-vs-commitment, leisure/belonging, theatre craft, magic evidence changes, and magical-ecology/world integration.
- [ ] Mark specific recurring narration to trim: lesson-after-lesson paragraphs, repeated scope self-talk, repeated body/protocol logs, and over-qualified conclusions.
- [ ] Estimate compression target by chapter without imposing a universal percentage.
- [ ] Produce a preliminary old->new numbering map only for genuine merge/cut candidates, labeled provisional.
- [ ] Commit.

### Task 5: Pilot Recent Heavy Edit

**Files:**
- Create or update a single branch-scoped recent-edit artifact chosen in the compression map; do not create chapter-per-file sprawl.
- Update: `state/editorial/RECENT_COMPRESSION_MAP_260_299.md`

**Interfaces:**
- Consumes: voice library, compression map, exact source prose.
- Produces: a small edited batch demonstrating target prose before scaling.

- [ ] Select 3-5 adjacent chapters representing different problems: one strong keep, one procedure-heavy compress, one dialogue-heavy chapter, and one possible merge boundary when available.
- [ ] Record source word counts.
- [ ] Heavy-edit while preserving events/outcomes and applying per-character voice rules.
- [ ] Increase dialogue tags where ambiguity remains after voice differentiation.
- [ ] Remove redundant explanation after landed moments.
- [ ] Compress established procedure unless the changed variable is the scene.
- [ ] Record edited word counts and structural result.
- [ ] Re-read the batch continuously for transitions and repeated architecture.
- [ ] Commit.

### Task 6: Freeze Structural Decisions and Renumber if Earned

**Files:**
- Update: `state/editorial/RECENT_COMPRESSION_MAP_260_299.md`
- Modify manuscript/index/state/reader files only after the map is frozen.

**Interfaces:**
- Consumes: completed recent edit and final cut/merge decisions.
- Produces: atomic structural migration if renumbering remains beneficial.

- [ ] Freeze KEEP/COMPRESS/MERGE/CUT decisions.
- [ ] Create exact old->new chapter-number mapping.
- [ ] Search repository for every affected old chapter reference.
- [ ] Apply chapter-heading/title/index changes atomically on the branch.
- [ ] Update state references where chapter numbers are operationally necessary.
- [ ] Update reader navigation/anchors.
- [ ] Preserve historical editorial references as historical where appropriate rather than falsifying their original numbering.
- [ ] Search again for dangling/stale affected references.
- [ ] Verify current endpoint/title/count after renumbering.
- [ ] Commit.

### Task 7: Scale the Heavy Edit Across the Remaining Recent Run

**Files:**
- Continue the single chosen recent heavy-edit artifact and structural map.

**Interfaces:**
- Consumes: frozen voice authority and structural decisions.
- Produces: edited recent run ready for integration review.

- [ ] Edit remaining chapters in small adjacent batches.
- [ ] Re-read neighboring transitions after every batch.
- [ ] Track word-count reduction and any canon-sensitive changes.
- [ ] Run voice audit on scenes with major recurring characters.
- [ ] Run repetition audit across batch boundaries.
- [ ] Verify no em dashes in manuscript prose.
- [ ] Commit each coherent batch.

### Task 8: Final Integration Verification

**Files:**
- Update relevant editor/project trailheads only after durable verification.

**Interfaces:**
- Consumes: completed branch state.
- Produces: merge-ready editorial branch and next executable edge.

- [ ] Compare branch against `main` and inspect every changed file category.
- [ ] Verify manuscript facts, magic counts, money, body continuity, relationships, and endpoint.
- [ ] Verify voice pages are referenced by routing/playbook files.
- [ ] Verify no chapter-number references are stale if renumbering occurred.
- [ ] Update `EDITOR_STATE.md` with the completed structural/voice edge.
- [ ] Leave a compact restart prompt for continuing the larger heavy edit.
- [ ] Commit final state update.