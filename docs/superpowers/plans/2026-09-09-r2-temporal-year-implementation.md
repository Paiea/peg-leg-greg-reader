# R2 Temporal Year Black Stair Rehearsal Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce one continuous, zero-authority 365-day R2 rehearsal from Chapter 42 to Firstday of Spring Year 313, ending at the Black Stair, using the prior 4x10 experiment as quarry while increasing action, fantasy progression, magic, artifacts, rank pressure, and felt time.

**Architecture:** The rehearsal lives only on `experiment/r2-temporal-year-043-plus`. Four seasonal folders hold ten dated chapter-sized performances each. `YEAR_CLOCK.md`, `PROGRESSION_LEDGER.md`, and `SOURCE_MAP.md` are the continuity interfaces between seasons; every chapter is followed by a reader-only scrub before the next season is treated as stable rehearsal state. Nothing is promoted into accepted R2 authority.

**Tech Stack:** Markdown prose and editorial state in Git; GitHub branch isolation; existing R2 character-rebuild authority through Chapter 42; existing `temporal-4x10-043-082` material as zero-authority quarry.

**Spec:** `r2/editorial/character-rebuild/temporal-year-043-plus/SPEC.md`

## Global Constraints

- Accepted story authority entering the experiment is Chapter 42.
- All year material is `EXPERIMENT / ZERO AUTHORITY`.
- Never copy or rename rehearsal prose into canon. Any eventual survivor must be freshly re-performed from current accepted authority.
- The year begins `Y312 / D001 / FIRSTDAY OF SPRING` and ends exactly `Y313 / D001 / DAY 365 ELAPSED`.
- Greg's opening target is: `One year from today, I am going to stand at the Black Stair.`
- Forty chapter-sized rehearsals must span the target dates in the approved spec.
- Target chapter length is 2,700-3,200 words. Under 2,500 requires a documented structural exception; over 3,500 requires a bloat challenge.
- Every chapter includes a meaningful embodied task, movement problem, physical environment, or action consequence.
- Across every three consecutive chapters, at least two contain a physical hazard, contest, chase, fight, rescue, dangerous job, difficult travel, or active magical problem.
- Across the full year target 12-16 substantial action sequences, at least 6 actual fights, at least 4 distinct monster encounters, at least 2 ruin/dungeon-like expeditions, at least 2 large group tactical sequences, and one multi-chapter winter action run.
- Power fantasy is allowed to feel good. Do not mechanically undercut every Greg competence beat.
- Gold is not the one-year target. Silver is a strong seasonal target if earned.
- The unique artifact must be useful during this year independently of any future peg-leg event.
- The prior 4x10 files are quarry only. Reuse discoveries, not prose or chronology.
- No internal routing language, horizon language, drafting notes, or continuity-manager comments may remain in reader-facing chapter prose.
- No em dashes in prose.

---

### Task 1: Build the year continuity scaffold

**Files:**
- Create: `r2/editorial/character-rebuild/temporal-year-043-plus/README.md`
- Create: `r2/editorial/character-rebuild/temporal-year-043-plus/YEAR_CLOCK.md`
- Create: `r2/editorial/character-rebuild/temporal-year-043-plus/PROGRESSION_LEDGER.md`
- Create: `r2/editorial/character-rebuild/temporal-year-043-plus/SOURCE_MAP.md`
- Create: `r2/editorial/character-rebuild/temporal-year-043-plus/READER_SCRUB.md`

**Interfaces:**
- Consumes: `SPEC.md`, accepted R2 truth through Chapter 42, and `temporal-4x10-043-082/AUDIT.md` plus its A/B/C/D chapter files.
- Produces: the canonical experiment-only date table, progression state schema, quarry mapping, and prose-cleanliness checklist used by Tasks 2-6.

- [ ] **Step 1: Create `YEAR_CLOCK.md` with all forty fixed target dates**

The table must include columns: `Year Chapter`, `Day`, `Season`, `Gap`, `Location Target`, `Temporal Purpose`, `Status`. Seed exact days from the approved spec: 1, 4, 9, 17, 28, 41, 55, 69, 82, 91, 97, 105, 116, 128, 140, 153, 166, 176, 181, 183, 190, 201, 214, 226, 238, 249, 260, 267, 272, 274, 281, 292, 304, 316, 326, 336, 345, 353, 360, 365.

- [ ] **Step 2: Create `PROGRESSION_LEDGER.md`**

Track after every chapter: `Rank`, `Guild Record`, `Money Band`, `Sword`, `Magic`, `Blackglass Anchor`, `Body`, `Gear`, `Reputation`, `Mara`, `Noll`, `Jorren`, `Tavin`, `Party/Westreach`, `Open Consequences`. Opening values must come only from accepted Chapter 42 state plus spec-approved experiment assumptions.

- [ ] **Step 3: Create `SOURCE_MAP.md`**

Map reusable discoveries from the prior 4x10 material to seasonal quarry, including exact source paths. High-value mappings must include A road/Tavin/home material, B road ecology and rescue material, C Halden/Mara/Vey material, and D infrastructure/Gold-professional grammar. Explicitly label all mapped events `REPERFORM / DO NOT COPY`.

- [ ] **Step 4: Create `READER_SCRUB.md`**

Checklist each chapter for: no author notes, no experiment-language leaks, no impossible cross-season knowledge, no imported 4x10 chronology, no unsupported calendar claim, no progression jump without elapsed-time evidence, no repeated `Greg wrong -> local corrects -> lesson` dependency, no automatic competence undercut, and no prose em dashes.

- [ ] **Step 5: Verify scaffold**

Read the five files continuously against `SPEC.md`. Confirm all 40 dates exist exactly once, D326 is the planned Westreach departure checkpoint, D365 is the Black Stair arrival test, and the artifact is not predesigned around amputation.

- [ ] **Step 6: Commit**

Commit message: `scaffold temporal year continuity ledgers`.

---

### Task 2: Rehearse Spring, Chapters 1-10, D001-D091

**Files:**
- Create: `r2/editorial/character-rebuild/temporal-year-043-plus/spring/ch01-d001.md`
- Create: `.../spring/ch02-d004.md`
- Create: `.../spring/ch03-d009.md`
- Create: `.../spring/ch04-d017.md`
- Create: `.../spring/ch05-d028.md`
- Create: `.../spring/ch06-d041.md`
- Create: `.../spring/ch07-d055.md`
- Create: `.../spring/ch08-d069.md`
- Create: `.../spring/ch09-d082.md`
- Create: `.../spring/ch10-d091.md`
- Modify: `YEAR_CLOCK.md`
- Modify: `PROGRESSION_LEDGER.md`

**Interfaces:**
- Consumes: Task 1 ledgers and Spring quarry in `SOURCE_MAP.md`.
- Produces: a stable Spring rehearsal state for Summer, including a physically real Black Stair goal, field record, first road repetition, Tavin/Noll/Jorren current-life pressure, first real monster fight, first meaningful gear improvement, and the Blackglass Anchor seed.

- [ ] **Step 1: Write D001 opening chapter**

Greg writes the exact one-year Black Stair promise in Carrow. The chapter must physically move him into a Guild/Westreach information path the same day. Establish how absurd the goal is using concrete qualification facts, not narrator thesis.

- [ ] **Step 2: Write D004 and D009 as an ugly-work/action pair**

Re-perform the ropehouse/load-geometry discovery rather than copying A43. Include a real physical failure or rescue and let Greg be useful. D009 must include either hostile physical conflict or a monster/magical field problem.

- [ ] **Step 3: Write D017 and D028 with the first road and first deliberate time jump**

Use Ossa/Beren-type practical road authority without requiring the exact old cast. D028 opens eleven days later and must show at least two off-page consequences. Greg should still want the road after novelty and soreness.

- [ ] **Step 4: Write D041 and D055 around current people and progression**

Tavin's current-person relationship becomes materially present by this band, whether by arrival or sustained correspondence. Noll and Jorren must have independent changes Greg did not witness. Add a meaningful sword-use sequence where Greg is clearly above ordinary Bronze sword competence.

- [ ] **Step 5: Write D069 artifact seed**

Greg encounters the Blackglass Anchor during salvage, old magic, dangerous infrastructure, or equivalent field work. It is initially a strange load/charge-balancing object, not legendary destiny. He acquires it through work, salvage rules, purchase, or earned claim with a real cost.

- [ ] **Step 6: Write D082 and D091 Spring escalation/end**

Include a substantial monster or magical-hazard sequence, first real artifact field use, visible money/gear progression, and concrete knowledge of what Westreach requires. Spring ends with the Black Stair goal difficult but operationally imaginable.

- [ ] **Step 7: Measure and scrub all ten Spring chapters**

Each chapter must satisfy the length gate or receive a documented exception. Run the `READER_SCRUB.md` checklist. Remove any author-side commentary and repeated rhetorical residue that makes chapters feel machine-generated.

- [ ] **Step 8: Update ledgers and commit**

Mark Spring dates complete, record state at D091, and commit message: `rehearse temporal year spring`.

---

### Task 3: Rehearse Summer, Chapters 11-20, D097-D183

**Files:**
- Create ten files in `.../summer/` named `ch11-d097.md` through `ch20-d183.md` using the exact day numbers from `YEAR_CLOCK.md`.
- Modify: `YEAR_CLOCK.md`
- Modify: `PROGRESSION_LEDGER.md`

**Interfaces:**
- Consumes: D091 state plus B/C quarry.
- Produces: repeat-road evidence, Halden as a second lived city, deeper Mara relationship over elapsed time, a proper ruin/dungeon-like job, several monster encounters, artifact experimentation, visible gear upgrades, and earned Silver pressure.

- [ ] **Step 1: D097-D116 establish repeat road and summer physicality**

Greg chooses another road after enough time has passed for the first to stop being novelty. Use road ecology, camps, route economics, and at least one rescue or hostile creature event. Greg must make at least one correct fast field call.

- [ ] **Step 2: D128-D140 move through Halden without turning it into a five-day romantic bubble**

Mara's work, coworkers, city routes, and schedule remain independent. Greg has his own Guild or field work. Relationship pressure comes from distance, missed time, and current people knowing Mara, not generic jealousy.

- [ ] **Step 3: D153-D166 run the first ruin/dungeon-like expedition**

Include party roles, an old magical site, at least one real fight, recoverable materials/loot, and Blackglass Anchor experimentation. Greg wins one fight decisively and is allowed to enjoy it.

- [ ] **Step 4: D176-D183 resolve Summer rank pressure**

Run a serious Silver evaluation through field evidence, formal test, recommendation, or a combination. Prefer Silver by D183 if the prior work earns it; if not, record the specific missing gate rather than inventing delay.

- [ ] **Step 5: Measure, scrub, update ledgers, and commit**

Apply all length/action/gap rules. Commit message: `rehearse temporal year summer`.

---

### Task 4: Rehearse Autumn, Chapters 21-30, D190-D274

**Files:**
- Create ten files in `.../autumn/` for D190, D201, D214, D226, D238, D249, D260, D267, D272, D274.
- Modify: `YEAR_CLOCK.md`
- Modify: `PROGRESSION_LEDGER.md`

**Interfaces:**
- Consumes: Summer endpoint and D/Gold quarry grammar.
- Produces: Silver-scale work if earned, stronger monsters, second ruin/old-magic sequence, larger loot/gear progression, integrated sword+magic, Gold-level benchmark encounter, one clean power-fantasy win, one costly overreach, and concrete Westreach candidacy.

- [ ] **Step 1: D190-D214 show new access, not a reset**

New contracts, pay, and expectations must visibly differ from Spring. Greg's official and actual capability mismatch should create opportunity and pressure.

- [ ] **Step 2: D226-D249 run stronger fantasy action**

Include at least two fights across this band, one against a materially stronger monster or hostile magical threat. Let Greg's sword and force magic integrate under movement. Add meaningful loot or specialized gear.

- [ ] **Step 3: D260 introduce Gold-level professional benchmark organically**

Use the 4x10 Gold grammar as quarry: maintained modified gear, fast disagreement, local-professional respect, abort discipline, and teamwork that has been practiced ugly. Do not copy Veyra/Renn/Orra/Nesk unless re-invented and independently justified.

- [ ] **Step 4: D267-D272 power win and overreach consequence**

Give Greg one satisfying, unqualified competence victory. Separately, let curiosity, vanity, or confidence cause a real cost that survives the chapter. Do not make the cost a moralistic punishment for being strong.

- [ ] **Step 5: D274 lock concrete Westreach candidacy**

Greg knows the likely slot/path, missing requirements, costs, winter kit, and social/professional dependencies. Other characters have autumn changes unrelated to his application.

- [ ] **Step 6: Measure, scrub, update ledgers, and commit**

Commit message: `rehearse temporal year autumn`.

---

### Task 5: Rehearse Winter and Westreach, Chapters 31-40, D281-D365

**Files:**
- Create ten files in `.../winter/` for D281, D292, D304, D316, D326, D336, D345, D353, D360, D365.
- Modify: `YEAR_CLOCK.md`
- Modify: `PROGRESSION_LEDGER.md`

**Interfaces:**
- Consumes: Autumn candidacy and every accumulated consequence.
- Produces: qualification, winter preparation, actual D326 departure, roughly 39 days of Westreach travel, strongest sustained action run, party/crew role ownership, artifact maturation, and the D365 Black Stair arrival test.

- [ ] **Step 1: D281-D316 finish qualification and departure costs**

Resolve sponsor/slot/rank/specialist requirements. Make Greg buy, repair, borrow, or earn winter kit. Relationships feel the approaching departure through behavior and scheduling, not speeches alone.

- [ ] **Step 2: D326 departure chapter**

Westreach physically leaves Carrow. The expedition is a mixed logistics organism, not four heroes walking west. Greg has a specific role and someone else owns overall command.

- [ ] **Step 3: D336-D345 first expedition escalation**

Use winter road, animals, logistics, stronger monsters, and one team fight. The Blackglass Anchor should solve a problem it could not have solved in Spring because Greg has changed.

- [ ] **Step 4: D353-D360 severe approach sequence**

Run the experiment's strongest multi-chapter action: combine terrain/weather/old magic with hostile ecology or enemies. Damage equipment. Hurt bodies. Force abort/route choices. Let Greg be highly capable without becoming sole savior.

- [ ] **Step 5: D365 Black Stair**

Reach Firstday of Spring Year 313 exactly. Physically test the opening promise. Preferred result: Greg touches the Black Stair. Do not make it a final boss or close every relationship/progression thread.

- [ ] **Step 6: Measure, scrub, update ledgers, and commit**

Commit message: `rehearse temporal year winter and Black Stair`.

---

### Task 6: Full-year verification and comparative audit

**Files:**
- Create: `r2/editorial/character-rebuild/temporal-year-043-plus/AUDIT.md`
- Modify if needed after scrub: any year rehearsal chapter, `YEAR_CLOCK.md`, `PROGRESSION_LEDGER.md`, `SOURCE_MAP.md`

**Interfaces:**
- Consumes: all forty chapters and ledgers.
- Produces: evidence-based judgment on whether the one-year engine should influence future R2 production.

- [ ] **Step 1: Verify exact temporal coverage**

Confirm 40 chapter files, all target days exactly once, D001 opening promise, D326 departure, D365 Black Stair test, and no chronology regression.

- [ ] **Step 2: Verify length and action metrics**

Record exact or best-available mechanical word counts. Count substantial action sequences, fights, monster encounters, ruin/dungeon-like expeditions, large-team sequences, and chapters lacking meaningful embodiment.

- [ ] **Step 3: Read continuously for time feel**

Audit whether Spring, Summer, Autumn, and Winter feel materially different; whether gaps show off-page life; whether injuries, money, relationships, gear, rank, and magic actually age rather than teleport.

- [ ] **Step 4: Audit progression and power fantasy**

Judge rank progression, sword growth, magic growth, artifact growth, loot/gear pleasure, status mismatch, and whether competence wins are allowed to land without reflexive undercutting.

- [ ] **Step 5: Audit character and relationship continuity**

Check Greg thought/action contradiction, supporting-character agency, Mara distance/time, Tavin/Jorren/Noll independent lives, and whether progression plot swallowed ordinary life.

- [ ] **Step 6: Audit prose and contamination**

Remove remaining routing language, author notes, horizon references, repeated evaluator words, and accidental old-4x10 chronology imports. Preserve Greg voice without letting house-rhetoric dominate.

- [ ] **Step 7: Identify survivors as discoveries, not canon scenes**

Classify the year's outputs into `PORTABLE DISCOVERY`, `REPERFORM`, `DISCOVERY ONLY`, and `KILL`. Do not promote prose.

- [ ] **Step 8: Commit final audit**

Commit message: `audit temporal year Black Stair experiment`.
