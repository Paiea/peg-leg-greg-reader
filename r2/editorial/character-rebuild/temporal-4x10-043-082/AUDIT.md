# R2 Temporal 4×10 Rehearsal Audit

Status: **EXPERIMENT AUDIT / ZERO AUTHORITY**

Branch: `experiment/r2-temporal-4x10-043-082`

Accepted story authority entering the experiment: **Chapter 42**.

Rehearsal set:

- A: 43–52, immediate Carrow / road-choice pressure
- B: 53–62, sustained road pressure
- C: 63–72, Halden / Mara pressure
- D: 73–82, infrastructure / magic / high-action pressure

All forty files are rehearsal only. None may become story authority by copy, rename, numbering, or proximity. Any surviving discovery must later be freshly re-performed from current accepted authority.

## Executive result

The experiment is **promising and worth preserving**, but it did not validate the original 4×10 specification exactly as proposed.

The major success is conceptual: four high-fidelity future lanes discover materially different kinds of story without forcing one speculative future to colonize the others. The rehearsal produces useful character, setting, action, relationship, and world-system discoveries that tiny future notes cannot expose.

The major failures are equally useful:

1. the generator did not hold the intended ~3,000-word chapter target;
2. prose compressed progressively as the run continued;
3. internal routing / horizon-management language leaked into several rehearsal files and required a reader-only scrub;
4. the first thirteen performances were interleaved, but the remaining twenty-seven were completed horizon-by-horizon, so the full run is not a clean test of strict `A → B → C → D` interleaving for all forty turns;
5. a prior D75 draft imported A-horizon characters before being caught and rewritten, proving horizon isolation needs mechanical support rather than memory alone.

The experiment therefore supports **parallel high-fidelity rehearsal as a discovery method**, but not yet a blind fixed 4×10 production protocol.

---

## 1. Word-count / scale audit

### Intended scale

The design target was roughly:

- 10 chapters per horizon
- ~3,000 words per chapter
- ~30,000 words per horizon
- ~120,000 words total

### Observed scale

An exact machine `wc` was not available through the connected GitHub environment during this audit. The repository does expose exact UTF-8 file byte sizes.

A pre-scrub forty-file snapshot measured approximately **358,750 bytes of chapter prose files**, or about **359 KB**. The later reader-only scrub changed only small passages, so the final order of magnitude is effectively unchanged.

Using the observed English prose density of these files as a rough conversion rather than pretending bytes equal words, the forty rehearsals are approximately **62,000–72,000 words total**, with the center of that range around the mid-to-high 60,000s.

That is only roughly **52–60% of the intended 120,000-word experiment**.

The size distribution also shows a clear compression slope. Early files such as A43 were around 16–17 KB, while many later B/C/D files fell into the 5–8 KB range. The instruction to add another lived phase improved embodiment in places, but it did **not** reliably enforce chapter length.

### Conclusion

If ~3,000 words matters, `aim for 3,000` is not a sufficient engine instruction. The process needs a mechanical acceptance gate before advancing:

- actual word count or equivalent reliable token/character measurement;
- minimum number of lived phases;
- aftermath / consequence requirement;
- rejection-and-expand step when the chapter undershoots.

The more important lesson is not that every R2 chapter should be 3,000 words. It is that **a rehearsal system cannot claim a fidelity target it does not mechanically verify**.

---

## 2. How the temporal system behaved

### What worked

The four horizons became genuinely different story engines.

**A** became about Greg choosing motion while Carrow kept being home. The strongest pressure was not whether he could get a road, but whether he could want one without turning it into proof. Ossa, Vell, Jorren's factor work, Noll's ordinary presence, Tavin's arrival, and the second chair all competed with the road rather than serving it.

**B** became the road as an actual social and physical ecology. Moths, camps, a washed road, a night cart accident, an accidental caravan, glasshorn movement, a ford, held pay, wet boots, local road knowledge, and freight paperwork made travel into lived work rather than a fantasy transition between plot points.

**C** became Mara's city rather than Greg's romantic destination. Vey work, Sera, Emmet, Pell, river logistics, a crane failure, a warehouse fire, Guild work, a river rescue, city neighborhoods, and Mara's room made Halden feel like a life Greg was visiting rather than a set waiting for him.

**D** became a combined infrastructure / ecology / professional-action engine. The warm wall expanded into old municipal systems, occupied buildings, bakery damage, unknown river fauna, Gold-level hazard work, liability, abort decisions, repairs, and invoices rather than becoming a lore dungeon.

This is the central win of the experiment: **future prose can be quarry without becoming railroad when the lanes are kept independent.**

### What did not work cleanly

The process relied too much on the same model instance to be both:

- horizon manager,
- continuity checker,
- prose renderer,
- prose editor.

That caused internal editorial language to leak into reader-facing prose. Examples included explicit references to another rehearsal, horizon facts, drafting alternatives, and comments about whether a scene needed explicit detail. Those were scrubbed, but their presence is a system failure, not merely a typo.

D75 also initially imported A-only rope workers before being rewritten with D-local Ilan and Mett. That is more serious because it demonstrates speculative cross-contamination.

### Required architecture change

A production version needs two distinct passes:

1. **REHEARSE**: generate the high-fidelity scene using only the horizon-local state packet plus accepted authority.
2. **READER SCRUB**: remove routing language, author notes, evaluation scaffolding, and any facts not licensed by that horizon.

Ideally each horizon also owns a small local fact ledger so the renderer cannot silently borrow from another lane.

### Interleaving limitation

The original design wanted every horizon rehearsed simultaneously:

`A43 → B53 → C63 → D73 → A44 → B54 → ...`

The first thirteen performances followed that spirit. The completion pass then finished A, then B, then C, then D.

This preserved factual independence but weakened the test of temporal simultaneity. It may also have contributed to later compression, because long single-horizon runs encourage local momentum and summary behavior.

A future experiment should automate round-robin turn order if strict simultaneity is part of the hypothesis.

---

## 3. Prose audit

### Strongest mode

The prose is strongest when **Greg thinks while his body is occupied**.

Examples of the productive pattern include:

- holding a cart or rope while evaluating whether he wants to prove something;
- walking through mud while Old Greg's route knowledge keeps becoming less useful;
- carrying Vey freight while watching Mara inhabit a work life he does not own;
- descending a drainage shaft while curiosity and physical caution pull in opposite directions;
- cleaning up after danger while the emotional interpretation arrives late.

This lets Greg remain highly analytical without turning the novel into disembodied analysis.

### Repeated weakness

The old R2 rhetorical residue remains visible across the forty rehearsals:

- isolated evaluator words: `Good`, `Correct`, `There`;
- `Not X. Y.` reversals;
- narration explaining what an action already proved;
- Greg catching himself forming a polished conclusion;
- chapter-ending principles that summarize the experience too neatly.

Some of this is Greg's voice. Too much becomes the generator's house voice.

A connected read should therefore challenge **frequency of instrument**, not ban the instrument.

### Dialogue

Dialogue is one of the strongest areas. The better supporting characters have distinct practical rhythms rather than merely different vocabulary.

Especially useful voices from the rehearsal quarry include:

- Ossa: cart-first, unsentimental, dry;
- Beren: road ownership and practical correction;
- Noll: minimal language that often defeats Greg's overthinking;
- Tavin: mocking directness with emotional loyalty underneath;
- Sera: operational aggression and social confidence;
- Vaska: municipal boundaries and refusal to romanticize infrastructure;
- Veyra / Renn / Orra / Nesk: Gold competence expressed through fast disagreement, role ownership, and abort discipline.

These exact people/events are not automatically survivors, but the interaction grammar is valuable.

---

## 4. Character audit

### Greg

The most important character discovery is that **Greg's thoughts and actions should not be forced to agree**.

This produces some of the most alive material in the experiment:

- he wants an independent road, then immediately seeks Jorren's validation;
- he offers to let Mara leave for work, then physically slows his eating to keep her longer;
- he knows curiosity is dangerous and still leans toward an unknown door or creature;
- he claims he does not need reassurance while arranging himself to receive it;
- he can know the right professional boundary and still emotionally resent it.

That is character, not inconsistency.

The action push also corrected an earlier danger: Greg no longer has to be wrong so that a competent local can teach him every chapter.

In the later run he is sometimes simply right:

- he sees a road crack and calls the stop;
- he recognizes dangerous load / fall geometry;
- he helps organize a night cart rescue;
- he creates a lane for a glasshorn charge rather than trying to defeat it;
- he throws a river rescue line effectively;
- he senses charge in the warehouse fire before the flare;
- he correctly deflects the creature's tail during the seven-second fight.

This matters. If every chapter follows `Greg assumes → local corrects → Greg updates → joke`, the character becomes a pedagogical machine.

### Mara

C is strong evidence that Mara becomes much more convincing when she has a **whole current life that does not organize around Greg**.

Her work schedule, coworkers, landlord, washing-line feud, professional competence, irritation, fatigue, and city knowledge create romantic pressure without manufacturing relationship melodrama.

The portable discovery is not the exact Halden visit. It is:

> Greg should have to love people whose lives continue when he is not present.

### Tavin

A's Tavin material is high-value quarry.

The useful discovery is a present-tense Tavin with:

- freight competence;
- ugly jokes;
- his own current employer / problems;
- memories of young Greg that contradict Greg's worst assumptions;
- independent history with Noll and Jorren;
- willingness to be warm without becoming a therapeutic exposition device.

The exact arrival timing and Venn load remain disposable.

### Supporting-character agency

The experiment is healthiest whenever supporting characters make choices Greg did not request:

- Jorren choosing factor / road work for his own reasons;
- Noll using the second chair and building Brass Spoon competence;
- Mara going back to work;
- Sera controlling her domain;
- Ossa deciding what risk belongs to her cart;
- Beren deciding what belongs to his mule;
- Vaska and city workers treating magic as municipal risk;
- Gold members overruling one another quickly rather than waiting for Greg.

That should remain a hard R2 requirement.

---

## 5. Setting audit

### Road

B is the strongest evidence that the road should be treated as a place rather than connective tissue.

Distinctive texture includes:

- road cooks and farmers;
- recurring drivers;
- tolls and access fees;
- mud and drainage;
- animal behavior;
- blisters and wet socks;
- camp labor;
- load ownership;
- held pay;
- rescue bells;
- bridge / ford authority;
- people who remember whether you paid them last time.

The road becomes socially legible.

### Halden

C makes Halden feel lived because the city is built from **repeated practical locations** rather than tourist exposition:

- Vey yard;
- river stairs;
- crane berth;
- Guild hall;
- steep stair routes;
- market festival;
- Lessa's;
- the Green Finch;
- Mara's room;
- the washing-line thief;
- burned warehouse aftermath.

That is a strong model for new R2 cities.

### Magic / infrastructure

D may be the strongest worldbuilding result.

The unknown magic becomes interesting because it interacts with:

- old heating / return-water infrastructure;
- drainage;
- buildings that have changed ownership and use;
- ecology;
- safety procedure;
- business interruption;
- municipal jurisdiction;
- insurance / reimbursement;
- repairs and material cost.

The portable worldbuilding principle is:

> **Magic gets more believable when ordinary systems have to live around it.**

The exact translucent creatures and warm-return network are zero-authority quarry, not an automatic future arc.

---

## 6. Plot audit

All four horizons created propulsion without requiring a locked master plot.

That supports the core temporal-rehearsal hypothesis.

A pressure became `road versus home versus proof`.

B became `what the road physically/socially teaches when Greg actually stays on it`.

C became `what happens when the relationship enters Mara's independent city life`.

D became `what happens when a mundane infrastructure anomaly widens into a professional hazard without becoming a chosen-one revelation`.

### Strongest plot engine

D has the strongest conventional propulsion. Each consequence creates another practical question:

warm wall → drainage → gate → creature → occupied building → flood → city system → river outlet → Gold survey → abort → release → cleanup / liability.

That chain is satisfying because causality is physical.

It is also the horizon most likely to become a railroad if copied directly. The portable material is the **engine**, not necessarily the event sequence.

### Gold Party

The Gold material worked best when Gold was not treated as a power fantasy or promotion ceremony.

The strongest pieces were:

- arriving with breakfast;
- using local rigger standards instead of overriding them;
- hand signals and role grammar;
- modified gear with replaceable sacrificial components;
- quick abort decisions;
- disagreement without paralysis;
- maintenance after the action;
- charging enough money to make expertise economically real;
- the seven-second fight being surrounded by nine hours of work.

This is good quarry for what upper-rank competence **feels like**.

Important caveat: the user explicitly nudged the experiment toward Gold-party material. Gold appearing in several late rehearsals is therefore **not independent evidence that the story naturally selected Gold as the next plot**. It is evidence that this rendering of Gold has useful texture.

---

## 7. Action audit

The action nudge materially improved the experiment.

The most useful finding is that R2 action does not need to mean combat.

### A action

- ropehouse load failure / rescue;
- dog and mule problem;
- washed road / cart crossing;
- moving-support attempt;
- freight-yard leak;
- physical homecoming / Tavin work arrival.

### B action

- moth swarm and mule panic;
- cart recovery in moving water;
- night passenger-cart overturn rescue;
- glasshorn charge / creating a lane;
- ford crossing;
- repeated load / camp / road labor.

### C action

- unstable freight stack;
- crane failure;
- warehouse fire;
- furniture move and sparring;
- river fall / rope rescue;
- city walking and work aftermath.

### D action

- underground descent;
- bakery flooding;
- unknown creature release;
- Gold survey and abort;
- catwalk collapse / steam escape;
- river outlet hazard;
- a seven-second creature fight;
- cleanup, rerouting, repair, and accounting.

### What action should mean for R2

The strongest sequences share four features:

1. bodies have specific tasks;
2. other people own part of the solution;
3. action changes physical state afterward;
4. cleanup, injury, money, repair, or relationship consequence survives the exciting moment.

This is a better fit for R2 than constant spectacle.

Conventional combat is still under-tested. A future targeted rehearsal could deliberately stage a 2–3 chapter escort / fight sequence where Greg's sword skill is allowed to be genuinely strong without turning the event into a rank-up ceremony.

---

## Portable discoveries versus disposable sequence

### High-value portable discoveries

- Greg genuinely likes the road. It does not need to be destiny or avoidance to matter.
- Greg's mind/body contradiction is core characterization.
- Greg must sometimes be clearly right and useful.
- Current local expertise can outrank future memory without making Greg stupid.
- Action aftermath is part of the action.
- Tavin works well as a current freight professional with mocking emotional honesty.
- Mara is strongest when her independent work/social life is fully present.
- New cities should be built through recurring practical places and people.
- Upper-rank competence should look like coordination, abort judgment, maintained gear, and role ownership.
- Magic becomes richer when ecology, infrastructure, property, money, and maintenance have to coexist with it.

### Disposable / high-risk event sequence

Do not automatically preserve:

- exact West Spur / Ossa sequence;
- exact Beren road / moth / glasshorn chain;
- exact Halden crane, warehouse fire, or river rescue order;
- exact translucent river-creature ecology;
- exact old warm-return municipal network;
- exact timing of a Gold team entering the story;
- Veyra / Renn / Orra / Nesk as canonical people;
- any chapter number assigned in this rehearsal set.

These events did their job even if none survive: they exposed what the story and characters can support.

---

## Recommended next architecture

### Default recommendation: 4×3 + extend

Instead of automatically spending forty high-fidelity chapters every cycle:

1. rehearse A/B/C/D for **three full chapters each**;
2. audit discovery yield and orthogonality;
3. kill or pause lanes that are repeating information;
4. extend only the one or two horizons still producing important new evidence toward 6–10 chapters;
5. harvest portable discoveries;
6. freshly re-perform the next accepted A chapter from authority.

This preserves the anti-railroad advantage of parallel futures while cutting a large amount of forced speculative prose.

### If keeping full 4×10

Then add hard gates:

- strict round-robin scheduler;
- horizon-local fact ledger;
- reader-only scrub after every chapter;
- mechanical word-count / size check;
- minimum embodied phases;
- required aftermath / consequence phase;
- contamination scan before the next turn;
- no promotion by copy.

### Bottom line

The 4×10 trial proves that **high-fidelity temporal rehearsal has substantially more discovery value than tiny speculative notes**.

It does **not** prove that forty long chapters should be the default unit of work.

The best leverage appears to be:

> **Rehearse several futures deeply enough to discover what cannot be found in outline, then spend expensive fidelity only where discovery is still increasing.**

That fits R2's larger rule:

> Keep what is alive. Rewrite what is merely good. Future prose is quarry, not railroad.
