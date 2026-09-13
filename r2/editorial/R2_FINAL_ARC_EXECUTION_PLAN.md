# R2 Final Arc Execution Plan

> **For agentic workers:** Execute this plan on `r2/final-arc-completion`. The selected story authority entering the plan is Chapter 164 from the September 13 post-First-Bell re-performance, not the older abandoned high-fidelity 165+ tail.

**Goal:** Finish R2 as a complete iteration with one final fantasy arc, a short ordinary-life landing, a frozen written authority, and a complete R2 → 3L handoff.

**Architecture:** Fresh-write the ending in connected audio-first prose blocks. Use `The Storm Road` as the current challenger, but preserve scene-level veto power: if full prose breaks the cuff logic or the crew becomes thematic machinery, revise locally or fall back before the irreversible choice. The final arc must end the R2 argument without pretending to end Greg's life.

**Spec:** `r2/editorial/R2_COMPLETION_CONTRACT.md`

## Global constraints

- Selected authority entering the arc: Chapter 164.
- Target final frontier: ~180; hard ceiling 184 without explicit user override.
- Full chapters should normally breathe around 2,000–2,500 words, but scene truth outranks quota.
- Audio/listening first: mostly Greg POV; speaker identity and referents must resolve by ear.
- Chapter titles name Greg's embodied role in that chapter.
- Mara keeps an independent Northbank life.
- Greg gets at least one clean win with no immediate punishment.
- The safe option at the climax must be real.
- If Greg uses the setter's cuff, he must understand the tradeoff first.
- The cuff may accelerate an existing narrow family; it may not create a new power.
- The ugly choice must materially work and leave a durable, survivable cost.
- Do not reopen Merek as the main final-arc plot. His successful sponsored contract should remain background evidence in Greg's head.
- No new open-ended arc after the Storm Road resolution.
- Old `high-fidelity-165+` files are historical quarry, not authority for this ending.

---

## Task 1: Write the departure movement, Chapters 165–169

**Deliverable:** Five fresh full chapters that get Greg from ordinary Carrow life onto the Storm Road and prove the road's demand is speed/latency, not raw power.

- 165: ordinary residue after Merek; final-arc contract reaches Greg through normal work channels rather than destiny.
- 166: contract terms, mixed roster, availability defeats Greg's ideal team choices.
- 167: travel west; crew ownership established; weather and road machinery embodied.
- 168: first damaged span / storm-hardware problem; Greg's narrow lane works cleanly.
- 169: first moving danger shows Greg is useful but too slow when several micro-failures arrive together.

**Verification:** Connected listen/read 165–169. Confirm distinct speakers, independent specialist ownership, and no cuff requirement yet.

## Task 2: Write the pressure movement, Chapters 170–174

**Deliverable:** Five chapters that deepen the road, produce fantasy pleasure, and earn the setter's cuff as an informed professional temptation.

- Include camp, bad food, money, repairs, prosthetic maintenance, salvage, weather, and at least one creature/action sequence.
- A specialist refuses one proposed Greg-side experiment because the storm is not a testing ground.
- Another specialist identifies an adaptation Greg missed.
- The setter's cuff becomes available through a plausible professional route. Its cost is demonstrated or documented clearly enough that Greg is not gambling blind.
- End 174 with the crew understanding both the road's remaining risk and the cuff's tradeoff.

**Verification:** Connected listen/read 170–174. Confirm the cuff is optional and the safe route still exists.

## Task 3: Write the commitment movement, Chapters 175–179

**Deliverable:** Five chapters that drive the convoy into the final weather window and climax.

- 175–177 escalate the crossing through actual road/cargo/animal/storm problems rather than repeated consulting puzzles.
- The convoy lead owns the final safe decision: abandon/cut a valuable rear cargo assembly, retreat, accept loss, keep people alive.
- Greg agrees that the safe option works.
- Greg then chooses the cuff because the individual failures are within his skill but arrive too quickly.
- 178–179 perform the cuff-assisted crossing. Other specialists retain ownership of their major actions. Greg becomes fast enough to make those actions available in time.
- The convoy crosses; most cargo survives; people get paid or are clearly going to be paid.
- Give Greg a clean moment of earned admiration before any cost assessment.

**Verification:** Connected listen/read 175–179. Confirm no curse/punishment beat and no false claim that the cuff was necessary to save lives.

## Task 4: Write the landing, Chapters 180–182

**Deliverable:** 1–3 ordinary-life chapters that convert consequence into daily life and end R2.

- Greg removes/returns the cuff.
- His narrow routing family remains faster and more reflexive.
- A broad structural family he previously performed competently is now slower/farther away, not gone.
- Greg's first reaction is practical rather than horrified.
- Mara learns what happened after the fact and reacts as an independent partner, not moral authority.
- The world begins pricing Greg for narrower moving-load/failure-routing work.
- Include money, food, leg/gear maintenance, correspondence, and at least one person choosing a life/job that is not Greg-centered.
- Final image shows who Greg has become without explaining the theme.

**Verification:** The ending must carry the feeling: `This works. Greg can keep making it work. That may be the problem.`

## Task 5: Cold connected read, 165–final

**Deliverable:** `r2/editorial/R2_FINAL_CONNECTED_READ.md`.

Audit:
- audio clarity and speaker ownership;
- repetitive `Good / Different / Useful` evaluator cadence;
- repetitive `Not X. Y.` reversals;
- chapter-role title correctness;
- whether every specialist became too neatly right;
- whether Mara retained independent life;
- whether the safe option was genuinely viable;
- whether the cuff choice was informed and voluntary;
- whether the consequence is durable but survivable;
- whether any chapter exists only to explain the theme.

Apply only earned light finishes. Reperform any chapter whose scene is structurally wrong.

## Task 6: Select and publish the ending

**Deliverable:** selected public R2 written frontier at the final chapter.

- Copy/finalize surviving prose under `r2/assets/written/chNNN.md`.
- Create/update `r2/data/chapters/chNNN.json` manifests.
- Extend navigation from 164 through the final chapter.
- Update `r2/data/project.json` current chapter and authority note.
- Preserve audio as `not_started` unless matching final prose exists.
- Verify the reader strips internal editorial preludes if any remain.

**Verification:** R2-specific site validation passes and final navigation is contiguous.

## Task 7: Freeze R2

**Deliverables:**
- `r2/editorial/R2_POSTMORTEM.md`
- completed `r2/editorial/R2_TO_3L_HANDOFF.md`
- `r2/editorial/R2_COMPLETE.md`
- durable completion marker branch/tag equivalent if tooling permits.

Record:
- final chapter/title/SHA;
- final Greg/Mara states;
- surviving relationship and magic/prosthetic state;
- top 10 scenes to self-plagiarize;
- top 10 mistakes 3L should avoid;
- exact production conventions 3L inherits;
- continuity 3L is explicitly free to discard.

After this task, no new R2 story arc may be added without explicit user override.

## Task 8: Production handoff

**Deliverable:** a concise R2 production status noting that written story development is frozen while selective audio/art can continue.

Do not require full audio/art completion before 3L begins.
