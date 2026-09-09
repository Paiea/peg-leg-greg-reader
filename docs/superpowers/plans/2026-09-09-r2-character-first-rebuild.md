# R2 Character-First Rebuild Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prove a materially more character-alive R2 trajectory by rebuilding from the Chapter 26 story state without touching public/current R2 chronology on `main`.

**Architecture:** Keep all reconstruction evidence and prose inside branch-only editorial storage under `r2/editorial/character-rebuild/`. Current `r2/assets/written/ch027.md` and later public chapter surfaces remain historical evidence. The experiment consists of a 1-26 diagnosis, a selective 27+ quarry, five reconstructed branch-only chapters, a connected challenger pass, and branch-isolation verification.

**Tech Stack:** Markdown prose/state artifacts, existing R2 manuscript files, Git/GitHub branch isolation.

**Spec:** `r2/editorial/character-rebuild/SPEC.md`

## Global Constraints

- Public/current R2 on `main` remains untouched.
- Chapter 26 is the presumptive chronological rebuild frontier; 27+ is quarry/rehearsal/evidence.
- Do not build a new conveyor, temporal engine, doctrine stack, or large speculative backlog.
- Use exact manuscript prose before summaries when judging continuity.
- Character before system; specificity before thesis; discovery before competence display.
- Preserve real money, work, elapsed time, independent supporting-character clocks, bounded competence, practical magic, material consequence, and off-camera life.
- Do not preserve material because it already exists.
- New reconstructed chapters remain experimental and unpublished until they clearly beat the historical trajectory.
- No public reader, registry, audio, image, or route surface may depend on reconstruction files.

---

### Task 1: Lock the Early-Run Diagnosis

**Files:**
- Create: `r2/editorial/character-rebuild/diagnosis-001-026.md`
- Read: `r2/assets/written/ch001.md` through `r2/assets/written/ch026.md`
- Read: `state/STORY_NORTH_STAR.md`
- Read: `r2/PIPELINE.md`
- Read: `r2/FUTURE_SURVIVOR_PROTOCOL.md`

**Interfaces:**
- Consumes: exact Chapters 1-26 plus durable artistic/pipeline constraints.
- Produces: a compact authority snapshot for Greg, Mara, Jorren, Noll, filtration group, Sella/Guild, body, money, magic, social/emotional range, relationship languages, chapter grammar, alive zones, and procedural onset.

- [ ] **Step 1: Record the exact-read frontier and structural verdict**

State explicitly that Chapters 1-26 were read continuously from the same `main` authority SHA used to create the experiment branch. Record whether Chapter 26 remains the practical frontier and identify any pre-27 material that is strong but structurally repetitive.

- [ ] **Step 2: Record character state, not generic archetypes**

For each recurring person, capture desires, fears, humor, status, money relationship, professional pride, embarrassment patterns, prior choices, independent motion, relationship language with Greg, and live misunderstandings.

- [ ] **Step 3: Record Greg's conflicting desires and attention failures**

Include concrete evidence of pride, competitiveness, curiosity, money stupidity, avoidance, grief, desire for old magic, fear of lost ordinary memory, loss of centrality, desire for adventure, and his tendency to turn truth into proof of correct behavior.

- [ ] **Step 4: Record structural patterns**

Separate strong repeated motifs from repeated chapter machinery. Specifically mark the onset of `problem -> expert correction -> narrow solution -> lesson -> tidy observation` and identify chapters where another scene grammar wins.

- [ ] **Step 5: Fresh-read the completed diagnosis as a story-control artifact**

Delete any advice that merely restates the spec. Keep only findings that materially constrain what reconstructed Chapter 27 can plausibly do next.

- [ ] **Step 6: Commit the diagnosis artifact**

Commit message: `docs(r2): diagnose character rebuild frontier`

---

### Task 2: Build the Later-R2 Quarry Without Rebuilding Chronology

**Files:**
- Create: `r2/editorial/character-rebuild/quarry-027-plus.md`
- Read selectively: historical `r2/assets/written/ch027.md` and later chapters where current summaries/search evidence show character, relationship, work, money, body, magic, place, object, or social discoveries worth testing.
- Read selectively: existing `r2/editorial/high-fidelity-*.md` audits for repeated later-run strengths/failures.

**Interfaces:**
- Consumes: Task 1 diagnosis and later historical R2 as non-authoritative evidence.
- Produces: 10-20 portable discoveries worth saving and 10-20 habits explicitly barred from automatic reimport.

- [ ] **Step 1: Read historical Chapter 27-31 first as the nearest challenger**

For each, classify exact material as `portable discovery`, `possible scene`, `line/texture only`, or `chronology-dependent and not protected`.

- [ ] **Step 2: Search later R2 for recurring people and high-value discoveries**

Prioritize Mara, Jorren, Noll, Sella/Guild, Arlo/Ivena/Dena, Kesra, money, housing/home, sex/intimacy if present, friendship, magic/body progression, geographically widening life, independent decisions Greg dislikes, and later objects/places that accumulated real meaning.

- [ ] **Step 3: Sample high-fidelity audits across the later run**

Use the existing cold/high-fidelity audits to locate strong scenes and repeated machinery cheaply. Verify especially important quarry candidates against exact prose before treating them as portable.

- [ ] **Step 4: Write 10-20 `SAVE` entries**

Each entry must say what survives independently of old chronology and why it creates future life per word.

- [ ] **Step 5: Write 10-20 `DO NOT REIMPORT` entries**

Include repeated competence/professional chapter grammar, tidy thesis endings, generic competent-adult voices, excessive future-vs-present specification checks, repeated infrastructure explanations after evidence is clear, and any later-run pattern the selective read proves rather than merely assumes.

- [ ] **Step 6: Commit the quarry artifact**

Commit message: `docs(r2): quarry later run for character rebuild`

---

### Task 3: Choose the Immediate Human Pressure for Reconstructed 27-31

**Files:**
- Create: `r2/editorial/character-rebuild/run-027-031/scene-search.md`
- Read: Task 1 diagnosis, Task 2 quarry, exact Chapters 21-26, and exact earlier material for every recurring person selected.

**Interfaces:**
- Consumes: early authority plus portable later discoveries.
- Produces: a five-chapter search packet that names active wants, unresolved pressures, off-camera clocks, and deliberately varied scene grammars without outlining beyond Chapter 31.

- [ ] **Step 1: List live pressures at the end of Chapter 26**

Include Mara correspondence, Noll/neighborhood life, Jorren absence, filtration venture moving independently, Kesra assessment weeks away, Greg's repaired road body/equipment, field/adventure desire, money reserve, Sella/Guild work access, and any quarry discovery that can arrive now without old chronology.

- [ ] **Step 2: Pick one primary human pressure and no more than two secondary pressures**

The primary pressure must create an interpersonal or emotional problem that cannot be solved solely by Greg performing professional work correctly.

- [ ] **Step 3: Give Greg at least two incompatible wants**

Record both wants in plain language and identify what behavior would expose the conflict without narration explaining it.

- [ ] **Step 4: Give at least two other people independent choices**

At least one choice must inconvenience, hurt, surprise, or frustrate Greg without being a villainous or irrational plot device.

- [ ] **Step 5: Define five different scene grammars**

Do not use the same `problem -> expert -> bounded action -> lesson` structure twice. At least one chapter must be relationship-led, one ordinary-life-led, and one may be work/adventure-led only if the human pressure remains active inside it.

- [ ] **Step 6: Commit the scene-search artifact**

Commit message: `docs(r2): search first character rebuild run`

---

### Task 4: Write Reconstructed Chapters 27-31 Branch-Only

**Files:**
- Create: `r2/editorial/character-rebuild/run-027-031/ch027.md`
- Create: `r2/editorial/character-rebuild/run-027-031/ch028.md`
- Create: `r2/editorial/character-rebuild/run-027-031/ch029.md`
- Create: `r2/editorial/character-rebuild/run-027-031/ch030.md`
- Create: `r2/editorial/character-rebuild/run-027-031/ch031.md`

**Interfaces:**
- Consumes: Task 3 search packet and exact referenced continuity.
- Produces: one connected five-chapter experimental Shared Greg Surface run with no publication wiring.

- [ ] **Step 1: Write Chapter 27 from current people, not historical Chapter 27**

Slow the camera at consequential moments. Let wants and misunderstandings determine attention. Preserve only historical material that wins fresh.

- [ ] **Step 2: Read Chapter 27 before writing Chapter 28**

Carry physical residue, money, awkwardness, relationship state, object positions, and another person's independent choice forward.

- [ ] **Step 3: Write Chapter 28 with a materially different scene grammar**

Do not answer every pressure introduced in Chapter 27.

- [ ] **Step 4: Write Chapter 29 and force the anonymous challenger mid-draft**

If names can be stripped and the scene becomes generic competent-fantasy prose, change wants, misunderstandings, refusals, or choices before finishing.

- [ ] **Step 5: Write Chapter 30 with Old Greg affecting emotion or social judgment**

Do not use old memory only as technical specification. It must distort, tempt, grieve, embarrass, comfort, frighten, or otherwise complicate present attention.

- [ ] **Step 6: Write Chapter 31 without manufacturing closure**

Leave earned residue. Do not explain the five-chapter run's lesson.

- [ ] **Step 7: Commit the connected run**

Commit message: `feat(r2): draft character rebuild 027-031`

---

### Task 5: Run Character, Anonymous, Repetition, and Reader Challengers

**Files:**
- Create: `r2/editorial/character-rebuild/run-027-031/evaluation.md`
- Modify only clear losers among: `r2/editorial/character-rebuild/run-027-031/ch027.md` through `ch031.md`

**Interfaces:**
- Consumes: the connected reconstructed run.
- Produces: an explicit quality verdict plus targeted revisions only where challenger evidence beats source.

- [ ] **Step 1: Read 27-31 continuously without editing**

Judge reader desire to continue because of people, not because another system exists.

- [ ] **Step 2: Answer every quality-test question from the spec with evidence**

Mark each `PASS`, `MIXED`, or `FAIL` and cite the exact chapter/scene internally.

- [ ] **Step 3: Run the anonymous challenger on every major scene**

Record which scenes remain unmistakably Greg/Mara/Jorren/Noll/etc after names and surface biography are mentally removed.

- [ ] **Step 4: Run the repetition challenger across all five chapters**

Search for repeated evaluator fragments, rhetorical reversals, expert-correction machinery, tidy endings, uniform competence, repeated joke placement, and identical paragraph cadence.

- [ ] **Step 5: Revise only clear losers**

Do not polish SOURCE WINs merely because revision is available. Re-read the full connected run after any revision.

- [ ] **Step 6: Commit evaluation and surviving revisions**

Commit message: `edit(r2): challenge character rebuild 027-031`

---

### Task 6: Verify Isolation and Stop at the Proven Run

**Files:**
- Read/compare branch versus `main`.
- No publication files should be modified.

**Interfaces:**
- Consumes: completed branch artifacts.
- Produces: verified experiment state ready for a later 3-5 chapter continuation decision.

- [ ] **Step 1: Compare `experiment/r2-character-rebuild` against current `main`**

Expected changed paths are limited to `r2/editorial/character-rebuild/**` and this plan file. No `r2/assets/written/ch027.md`, `r2/data/chapters/**`, reader route, audio, image, manifest, or public registry file may change.

- [ ] **Step 2: Re-fetch all five reconstructed chapter files from the branch**

Confirm they exist only in experimental storage and remain readable in order.

- [ ] **Step 3: Confirm current `main` historical Chapter 27 remains unchanged**

Fetch `r2/assets/written/ch027.md` from `main` and compare its blob SHA against the branch path of the same public file. They must match because the experiment does not rewrite public R2.

- [ ] **Step 4: Stop**

Do not continue to Chapter 32 in this execution. The next run must begin by fresh-reading the reconstructed 27-31 and its evaluation, then deciding whether the experiment earned continuation.
