# R2 Temporal Year Experiment Spec

Status: **EXPERIMENT DESIGN / ZERO AUTHORITY**

Branch: `experiment/r2-temporal-year-043-plus`

Accepted story authority entering the experiment: **Chapter 42**.

Parent quarry: `r2/editorial/character-rebuild/temporal-4x10-043-082/`

This experiment does not replace, edit, or promote the 4x10 rehearsals. It creates a new speculative year that may reuse their discoveries as quarry. No rehearsal prose, event, character, artifact, chapter number, or date becomes canon by existing here.

## 1. Experiment question

Can R2 sustain one full year of continuous speculative story time while preserving the character-first rebuild and adding substantially more conventional fantasy progression, power-fantasy payoff, magic, monsters, artifacts, rank pressure, party competence, travel, ruins, and physical action?

The experiment must answer a harder question than `can we write another 120k words?`:

> Can the reader feel 365 days of change in Greg, his relationships, his body, his money, his rank, his magic, his equipment, his reputation, and the world around him?

The existing 4x10 trial mostly explored four alternate versions of the first one to two weeks after Chapter 42. This experiment turns that horizontal discovery into one continuous speculative year.

## 2. Hard date and destination

The year begins on:

**Firstday of Spring, Year 312**

Internal header notation:

`Y312 / D001 / FIRSTDAY OF SPRING`

The final target is:

**Firstday of Spring, Year 313**

Internal header notation:

`Y313 / D001 / DAY 365 ELAPSED`

On the opening day Greg writes down one concrete intention:

> **One year from today, I am going to stand at the Black Stair.**

The year succeeds temporally only if the final rehearsal reaches that exact date and physically tests whether Greg stands at the Black Stair.

The target is not `become Gold`, `become powerful`, `fix his memory`, or `win Mara`. Those may create pressure, but they are not the clock.

## 3. The Black Stair

The Black Stair is a known western frontier threshold several weeks beyond Carrow by winter expedition pace.

It is an old monumental stair cut into dark stone at the edge of a dangerous frontier corridor. The precise ancient purpose is not known to current Greg and must not be fully explained in the design. It is famous enough that adventurers, freight interests, survey crews, mages, and expedition companies know the name.

The annual **Westreach Expedition** leaves Carrow in late winter and aims to reach the Black Stair on Firstday of Spring. It is not one heroic party. It is a mixed expedition containing some combination of:

- adventuring parties;
- Guild specialists;
- freight and animal crews;
- healers;
- mages and ward workers;
- surveyors;
- merchants or sponsors;
- guards;
- Silver and Gold personnel;
- lower-ranked workers with specific field value.

Greg's year-long problem is therefore not simply `gain a rank`. He must become someone a serious expedition has a reason to take west.

Plausible qualifying paths include Silver rank, an exceptional field waiver, sponsorship, specialist value, a trusted party slot, or a combination. The experiment should discover which path feels earned rather than preselecting one.

The Westreach Expedition must leave Carrow approximately five to six weeks before the deadline, giving the final winter run enough physical travel to make arrival at the Black Stair meaningful.

## 4. Opening image and closing image

### Opening image

Bronze Greg in Carrow on D001 writes the Black Stair date down while his actual life remains small enough to make the promise ridiculous.

At minimum, opening-state pressure includes:

- Bronze rank;
- uneven current magic;
- sword competence that may exceed the tab on his coat but is not yet integrated with current field life;
- no established expedition party;
- no Westreach slot;
- incomplete and unreliable Old Greg memory;
- current Carrow obligations and relationships;
- Mara west in Halden;
- Tavin newly reconnected by letter;
- Jorren and Noll continuing lives that do not wait for Greg;
- real but limited money and equipment;
- desire for the road without proof he will keep choosing it.

### Closing image

On D365 elapsed, Firstday of Spring Year 313, Greg reaches the Black Stair or demonstrably fails at the threshold for an earned reason.

The preferred success image is physical and simple:

Greg puts a hand on the Black Stair after a year the reader can feel in his body, gear, relationships, field judgment, magic, and reputation.

This is not the end of R2. The Black Stair is a threshold, not a final boss.

## 5. Output scale

Target experimental scale:

- 40 chapter-sized rehearsals;
- approximately 2,700 to 3,200 words each;
- approximately 108,000 to 128,000 words total;
- one continuous speculative chronology;
- 365 days elapsed;
- four seasonal ten-chapter runs.

The 3,000-word target is a fidelity target, not a stylistic law for eventual canon. Unlike the 4x10 trial, the system must mechanically measure length before advancing.

A rehearsal under 2,500 words fails the fidelity gate unless the chapter is intentionally short for a clearly documented structural reason. A rehearsal over 3,500 words should be challenged for bloat unless the action or aftermath genuinely requires it.

## 6. Calendar architecture

Use day-of-year numbers as the internal continuity authority. Season names are reader-facing texture. This avoids inventing a complete canon calendar before the story earns one.

Provisional seasonal ranges:

- Spring: D001-D091
- Summer: D092-D183
- Autumn: D184-D274
- Winter: D275-D365

Each chapter header must contain:

`DATE / DAYS SINCE PRIOR CHAPTER / LOCATION / RANK / MONEY BAND / BODY / MAGIC / ARTIFACT / ACTIVE RELATIONSHIP PRESSURES`

The date header is editorial metadata, not automatically reader-facing prose.

### Gap rule

If more than two days pass between chapters, the opening 500 words must establish at least two concrete consequences of the gap without dumping a summary.

Examples:

- an injury partly healed or still limiting movement;
- money earned or spent;
- weather and daylight changed;
- letters arrived or did not arrive;
- somebody worked shifts Greg did not witness;
- a contract result changed reputation;
- Greg practiced enough for a technique to be different;
- gear wore out or was repaired;
- Mara, Noll, Jorren, Tavin, or another person made an independent choice;
- a business or city location changed;
- a monster route, market price, river level, or road condition changed.

Time skips must create evidence that life occurred off-page.

## 7. Forty temporal checkpoints

These are target dates, not mandatory event locks. They exist to prevent calendar compression.

### Spring, chapters 1-10

1. D001
2. D004
3. D009
4. D017
5. D028
6. D041
7. D055
8. D069
9. D082
10. D091

Spring should feel like roughly three months, not ten consecutive mornings.

### Summer, chapters 11-20

11. D097
12. D105
13. D116
14. D128
15. D140
16. D153
17. D166
18. D176
19. D181
20. D183

Summer may contain short connected runs around major jobs, but must still span the whole season.

### Autumn, chapters 21-30

21. D190
22. D201
23. D214
24. D226
25. D238
26. D249
27. D260
28. D267
29. D272
30. D274

Autumn should show Greg living with midyear consequences rather than resetting after Silver progress or a major fight.

### Winter, chapters 31-40

31. D281
32. D292
33. D304
34. D316
35. D326
36. D336
37. D345
38. D353
39. D360
40. D365

The Westreach departure should occur around D326, leaving roughly thirty-nine elapsed days for the final expedition run.

Dates may shift by a few days during rehearsal only if the year still ends exactly on D365 and the seasonal span remains visible. Any shift must be recorded in `YEAR_CLOCK.md` during implementation.

## 8. Seasonal pressure spine

### Spring: Make the ridiculous goal physically real

Spring pressure question:

> Does Greg actually begin living like a man trying to reach the Black Stair, or does he merely enjoy having a dramatic date written down?

Spring should harvest heavily from 4x10 A and early B without copying their chronology.

High-value spring quarry includes:

- Guild board and ugly physical work;
- ropehouse / hoist / load geometry;
- Greg wanting a road and taking a small one;
- Jorren returning with a life that changed while Greg stayed home;
- Tavin correspondence and eventual current-person arrival;
- Noll's Brass Spoon work and Lower Rook independence;
- Ossa/Beren-style practical road authority;
- wet roads, freight, animals, money, gear, and bodily soreness;
- Greg being useful under pressure rather than merely learning lessons.

Spring fantasy progression should add:

- at least one real monster encounter;
- at least one sword fight or hostile physical confrontation where Greg's existing skill matters;
- at least one magical field problem outside training;
- first meaningful loot or gear improvement;
- the unique artifact seed;
- clear Westreach qualification information, even if the route is still uncertain.

Spring should end with the Black Stair goal looking difficult but no longer imaginary.

### Summer: Roads, Halden, rank pressure, and power beginning to show

Summer pressure question:

> What happens when Greg keeps choosing the road after the novelty is gone, and current capability begins to exceed what Bronze is supposed to look like?

High-value summer quarry includes:

- B's road ecology;
- Kelm and repeat roads as places with recurring people;
- held pay, tolls, weather, animal care, rescue bells, camps, and route economics;
- C's Halden and Mara material distributed across months rather than five consecutive intense days;
- Vey work and Mara's independent city life;
- Guild work in another city;
- crane, river, freight, fire, or equivalent practical action;
- Greg learning that distance changes relationships.

Summer fantasy progression should add:

- a proper ruin, dungeon-like site, or old magical worksite;
- several hostile creature encounters;
- at least one fight Greg wins decisively and is allowed to enjoy;
- at least one party-based tactical sequence;
- meaningful artifact experimentation;
- a first serious Silver evaluation, whether formal exam, field recommendation, or both;
- a first failed or incomplete promotion pressure if that creates better story than immediate success;
- visible gear upgrades purchased or earned from actual work.

Preferred summer endpoint: Greg becomes Silver near the end of the season, or earns an equivalently consequential field status that changes what contracts become available. Silver is a strong target, not a guaranteed author decree.

### Autumn: Prove the new level is real

Autumn pressure question:

> Once Greg has more access, more money, more magic, and more dangerous work, does he become a better field partner or merely a more powerful version of the same difficult man?

Autumn should be the strongest conventional fantasy / power-fantasy quarter before Westreach.

Required territory includes:

- larger Guild contracts;
- stronger monsters;
- ruins or old magic with actual stakes;
- loot and specialized gear;
- Greg's sword skill becoming frighteningly useful in at least one real fight;
- magic integrated with movement and combat rather than demonstrated separately;
- party formation pressure;
- Gold-level workers encountered organically after Greg has enough field experience to understand what they are doing;
- at least one Gold competence sequence where abort judgment matters as much as damage output;
- at least one clean Greg power-fantasy win that does not get immediately undercut by a lecture;
- at least one bad consequence from Greg's curiosity, vanity, or overreach;
- Mara, Tavin, Jorren, Noll, and other recurring people continuing to change outside Greg's progression track.

High-value D quarry may enter here, especially the professional action grammar, infrastructure magic, modified gear, and Gold coordination. The exact warm-wall creature chain is optional and should not be copied merely because it exists.

Autumn should end with Westreach candidacy becoming concrete. Greg should know what he still lacks.

### Winter: Qualify, leave, survive, arrive

Winter pressure question:

> When the date stops being aspirational and becomes a departure schedule, what does Greg actually have to sacrifice, finish, buy, prove, and leave behind?

Winter should have the highest sustained action density.

Required territory includes:

- qualification or sponsor politics;
- expedition money and kit;
- winter roads;
- party / crew role ownership;
- stronger magic and monster encounters;
- at least one substantial team fight;
- at least one severe non-combat hazard such as weather, terrain, structural failure, river/ice, or magical environment;
- equipment damage and repair;
- meaningful injury or bodily cost without forcing the future peg-leg event;
- relationship pressure caused by departure rather than generic goodbye speeches;
- actual late-winter departure around D326;
- approximately five to six weeks of westward expedition movement;
- final approach to the Black Stair;
- D365 arrival test.

The final winter run should feel larger than Spring because Greg is genuinely more capable and the world is genuinely more dangerous, not because prose simply declares escalation.

## 9. Fantasy / isekai / power-fantasy grammar

The experiment should intentionally use more familiar fantasy and isekai pleasures while preserving R2's character-first identity.

Desired genre grammar includes:

- adventurer rank progression;
- Guild boards and better contracts unlocking;
- monster materials and salvage;
- ruins and old magical sites;
- party composition and tactical roles;
- rare equipment;
- magic experimentation;
- visible skill growth;
- status mismatch where Greg performs above his official rank;
- stronger enemies;
- named techniques or repeatable field methods only when the story has earned them;
- specialists recognizing unusual ability;
- money and gear upgrades;
- travel to increasingly dangerous territory;
- occasional decisive victories;
- aspirational high-rank teams;
- the pleasure of Greg becoming dangerous.

Do not import game UI, numerical stat screens, experience points, skill menus, or system notifications unless accepted R2 authority independently establishes them.

Power fantasy is allowed to feel good. The system must not automatically punish every competence beat with humiliation, injury, or a corrective speech.

The balancing rule is:

> Greg may become individually powerful faster than he becomes socially, professionally, or emotionally easy to work with.

## 10. Action floor

The 4x10 experiment proved that R2 improves when Greg thinks while his body is occupied. This experiment pushes that much harder.

Every chapter must include a meaningful embodied task, movement problem, physical environment, or action consequence. No chapter may consist entirely of conversation, introspection, letters, or institutional explanation.

Across every three consecutive chapters:

- at least two must contain a physical hazard, contest, chase, fight, rescue, dangerous job, difficult travel, or active magical problem;
- at least one must contain lasting bodily, material, financial, or relationship aftermath from action.

Each season must contain at minimum:

- three substantial action sequences;
- one actual combat sequence against a hostile creature or person;
- one non-combat rescue / environmental / work hazard;
- one group tactical sequence where Greg does not own the whole solution.

Across the full year, target:

- 12 to 16 substantial action sequences;
- at least 6 actual fights;
- at least 4 monster encounters with different practical behavior;
- at least 2 ruin / dungeon-like expeditions;
- at least 2 large group or party tactical sequences;
- at least 1 winter action run spanning multiple chapters.

Combat may be short. Aftermath may be long.

Action must change something that survives the scene: injury, route, equipment, money, reputation, relationship, contract, ecology, or next decision.

## 11. Greg progression ledger

Progression must be visible without turning R2 into a stat sheet.

### Rank

Opening: Bronze.

Spring: build real field record.

Summer: pressure Silver eligibility.

Autumn: operate at Silver-scale access if earned.

Winter: become Westreach-credible through rank, sponsor, specialist value, party trust, or a combination.

Gold is not the one-year target. Gold should remain impressive enough that reaching it later matters.

### Sword

Greg may begin the year better with a sword than his Bronze rank suggests.

The year should test:

- current-body endurance;
- friendly sparring versus lethal application;
- monster-specific movement;
- fighting while tired, wet, injured, carrying gear, or protecting someone;
- integration with force / ward magic;
- party spacing;
- when not to draw;
- at least one sequence where Greg is simply excellent.

### Magic

Preferred progression shape:

1. sensing, ward reading, small static force, and bounded current techniques;
2. load geometry and force redirection;
3. shear resistance and moving support;
4. field use under unstable conditions;
5. artifact-assisted redirection or storage;
6. integration with sword, shields, rigging, or party movement;
7. late-year high-load use that would have been impossible on D001.

Old Greg memory may accelerate insight but cannot substitute for current-body capacity, present materials, consent, local expertise, or practice.

### Body

Track:

- calluses;
- blisters;
- sleep debt;
- shoulder / hand / knee strain;
- minor scars;
- endurance;
- seasonal clothing;
- weight carried;
- recovery time;
- cold and wet tolerance;
- injuries that heal over weeks rather than disappearing between chapters.

The year should make Greg's body feel more field-used by winter than spring.

### Money and equipment

Track income and meaningful spending.

Greg should visibly upgrade through work:

- boots;
- oilcloth;
- pack repairs;
- sword maintenance;
- harness or climbing gear;
- ward / magic components;
- winter kit;
- artifact mounting or containment;
- expedition contribution.

Loot does not need to be treasure chests. Salvage, monster materials, contract bonuses, rare components, and favors all count.

## 12. Unique artifact: the Blackglass Anchor

Provisional artifact name: **Blackglass Anchor**.

The name is experimental and does not imply a connection to the Black Stair.

### Core concept

A rare old force / charge-balancing component made from dark glass-like material and metal. Greg first encounters it during an ordinary dangerous job, salvage operation, ruin, or magical infrastructure problem.

Its early function should be understandable through physical behavior before lore:

- it can accept, redirect, equalize, or temporarily store force / mana across a connected structure;
- it interacts with load paths, wards, rigging, armor, or weapon contact;
- it has capacity limits;
- it can heat, fracture, discharge, or destabilize if badly used;
- mounting and connection matter;
- Greg's interest comes partly from his existing obsession with force geometry and practical systems.

### Artifact progression

Spring: discovery and safe containment.

Early summer: small controlled uses and wrong assumptions.

Late summer: first field use that produces a real advantage.

Autumn: modification into equipment or a repeatable field configuration.

Late autumn: a high-load failure or cost that prevents it from becoming a cheat code.

Winter: mature enough to matter during Westreach, but not fully understood.

### Peg-leg rule

Do not design the Blackglass Anchor backward from Greg's future leg loss.

During this year it must earn its place as an artifact Greg would keep even if he never lost a leg.

The leg-loss event is **not required** in this one-year experiment and should not be forced for title fulfillment.

If later canon eventually reaches the peg-leg event, the Anchor may prove unusually suited to a prosthetic interface because readers already understand its relationship to force, load, connection, and body mechanics. That later use should feel like a second life for an established object, not a prophecy hidden in the artifact description.

## 13. Relationship clocks

### Mara

Do not compress Mara into one intense Halden week.

Across the year, test:

- letters and delayed replies;
- missed timing;
- Greg visiting Halden more than once or Mara coming east if earned;
- work seasons;
- jealousy becoming more specific and less adolescent without vanishing;
- physical intimacy and ordinary logistics;
- disagreements that do not resolve in one chapter;
- the effect of Greg taking more dangerous work;
- the effect of Westreach becoming real;
- whether distance produces trust, avoidance, or both.

Mara's life must continue when Greg is absent.

### Tavin

Use A's Tavin as high-value quarry:

- freight competence;
- mocking emotional honesty;
- memories of young Greg that complicate Greg's self-story;
- independent work and travel;
- relationships with Noll and Jorren that do not route through Greg.

Tavin should appear, leave, return, write, or change jobs according to his own clock.

### Jorren

Track whether Jorren becomes road worker, factor specialist, party-capable adventurer, or something the experiment discovers.

Greg should repeatedly face the fact that Jorren can become good at a life Greg did not design.

### Noll

Noll's Brass Spoon / Lower Rook development should accumulate over months.

Greg may leave for weeks and return to find Noll more capable, more connected, busier, or less available.

The second chair remains useful quarry because home should acquire history while Greg keeps leaving it.

### Supporting characters

A one-year experiment must resist disposable-worker syndrome. Reuse practical people when geography and work make recurrence plausible. Let road drivers, clerks, healers, riggers, Guild staff, shop owners, and party members remember prior interactions.

## 14. Quarry rules for the 4x10 experiment

Parent quarry folder:

`r2/editorial/character-rebuild/temporal-4x10-043-082/`

### A quarry

`a-043-052/`

Portable material:

- Guild board / ropehouse action;
- Ossa-style road professionalism;
- small road proving desire physically;
- Tavin current-person material;
- Noll / Jorren / home pressure;
- Gold observed as ordinary professionals rather than destiny.

Do not copy A's ten-day chronology.

### B quarry

`b-053-062/`

Portable material:

- road ecology;
- Beren-style mule / cart ownership;
- Wren Post and recurring road people;
- washed roads, fords, tolls, camps, freight economics;
- rescue bells;
- accidental caravan;
- glasshorn-style nonhuman ecology;
- Greg being right under physical pressure.

Spread these discoveries across multiple trips and seasons rather than one compressed road.

### C quarry

`c-063-072/`

Portable material:

- Halden as repeated practical city;
- Mara's independent work life;
- Sera / Pell / Emmet interaction grammar;
- Guild work in another city;
- crane, fire, freight, river, festival, room, and neighborhood texture;
- Greg's jealousy of current facts rather than generic romantic rivals;
- direct communication versus timetable-monitoring.

Do not preserve the exact sequence or five-day intensity automatically.

### D quarry

`d-073-082/`

Portable material:

- magic embedded in infrastructure and ecology;
- Vaska-style professional boundaries;
- Gold coordination, modified gear, disagreement, and abort judgment;
- action followed by cleanup, liability, and repair;
- Greg's curiosity becoming expensive;
- unknown phenomena that do not instantly become lore answers.

The exact warm-return network, translucent creatures, and Gold party names remain disposable unless the year independently rediscovers them.

## 15. Rehearsal pipeline

The 4x10 trial showed that one pass should not simultaneously manage horizon architecture and pretend that architecture does not exist in prose.

The year uses separate stages.

### Stage 1: date packet

Before each chapter, construct a compact local packet containing:

- accepted authority through Chapter 42;
- year-local facts only;
- exact date;
- days since prior chapter;
- unresolved pressures;
- current rank / money / body / magic / artifact state;
- relationship state;
- source quarry allowed for this chapter;
- action requirement.

### Stage 2: rehearse

Write the chapter at high fidelity from Greg's view.

The prose renderer must not see or mention future chapter outcomes as facts.

### Stage 3: reader scrub

Remove:

- author notes;
- routing language;
- design commentary;
- `this horizon`, `this rehearsal`, or similar scaffolding;
- accidental claims of canon;
- unlicensed facts;
- repeated evaluator language that reads like system residue rather than Greg.

### Stage 4: mechanical gates

Before advancing:

- measure word count;
- verify exact date and elapsed days;
- verify no future date regression;
- verify no 4x10 event was silently promoted as authority;
- verify artifact state;
- verify rank and money continuity;
- verify injuries / gear consequences;
- verify action floor;
- verify reader scrub passed.

### Stage 5: ledger update

Update the year clock and progression ledger only after the scrubbed rehearsal exists.

## 16. Prose rules

Preserve the character-first R2 north star:

> A man who remembers history better than he remembers life is forced to live closely enough that life starts replacing history as his primary source of truth.

The year should not flatten Greg into either a therapy patient or a power-fantasy avatar.

Strong mode:

- Greg thinks while moving, carrying, fighting, working, repairing, traveling, cooking, waiting in weather, or recovering;
- thoughts and actions may disagree;
- Greg can be vain, horny, frightened, petty, generous, curious, selfish, competent, and wrong in the same chapter;
- Old Greg memory is evidence, not narrator authority;
- mundane texture remains valuable when it changes capability or relationship;
- action may reveal character without a concluding lesson.

Challenge repeated house-style residue:

- isolated `Good`, `Correct`, `There` evaluator beats;
- excessive `Not X. Y.` reversals;
- narration explaining what dialogue already proved;
- Greg catching himself producing polished theses every few pages;
- tidy lesson endings.

Do not ban these instruments. Reduce automatic frequency.

## 17. Failure conditions

The year experiment fails if any of the following dominate:

- forty chapters feel like forty consecutive days despite the date headers;
- rank increases without changed work access or social consequence;
- Greg's magic improves mainly through narration rather than repeated use;
- the Blackglass Anchor becomes a cheat code or chosen-one token;
- every fight exists only to prove Greg is special;
- every competence beat is immediately undercut;
- Mara becomes reward, obstacle, or calendar service;
- supporting people stop changing when Greg leaves town;
- Gold becomes merely a bigger damage number;
- the Black Stair becomes a prophecy rather than a destination;
- the final winter run skips travel with a montage;
- 4x10 quarry is copied into chronology rather than re-performed;
- chapter dates advance but body, money, relationships, weather, and institutions do not.

## 18. Audit requirements

After all forty rehearsals, perform a full connected audit covering:

1. exact total word count;
2. exact calendar span and days represented per chapter;
3. whether each season feels different;
4. rank progression;
5. sword progression;
6. magic progression;
7. artifact progression;
8. money / equipment progression;
9. body / injury progression;
10. Mara / Tavin / Jorren / Noll relationship progression;
11. action density and action variety;
12. monster / fantasy trope density;
13. power-fantasy satisfaction;
14. prose quality and repeated rhetorical habits;
15. setting growth;
16. plot causality;
17. supporting-character agency;
18. whether the Black Stair deadline creates useful pressure;
19. which 4x10 discoveries survived months of elapsed time;
20. which events should remain quarry only.

The audit must distinguish:

- portable discovery;
- reusable scene pressure;
- specific event sequence;
- character / location candidate;
- artifact discovery;
- likely canon survivor;
- material that became less convincing when time was added.

No event becomes authority from receiving a positive audit label.

## 19. Success criteria

The experiment is successful if, after approximately 120k rehearsal words, a reader can answer all of these without consulting the ledger:

- What season is it?
- How long has Greg been pursuing the Black Stair goal?
- What can Greg physically do now that he could not do in Spring?
- What can his magic do now that it could not do in Spring?
- What has he earned, bought, broken, repaired, or lost?
- Why is Silver or expedition credibility earned rather than announced?
- How has Mara's relationship with Greg changed over months?
- How have Tavin, Jorren, and Noll changed without waiting for him?
- What does Greg now understand about parties that Spring Greg did not?
- Why does the Blackglass Anchor matter even without a future prosthetic?
- Why is winter more dangerous than spring?
- Why does reaching the Black Stair on D365 mean more than checking off a goal?

The final success standard is simple:

> **The reader should feel that Greg lived a year, not that the outline advanced 365 days.**

## 20. Authority rule

Everything in `temporal-year-043-plus/` remains **zero authority**.

If the experiment discovers an excellent Year-312 future, accepted Chapter 43 must still be freshly written from current accepted authority.

No future chapter may be promoted by copy, rename, renumber, or cleanup.

The year is rehearsal quarry.

Its job is to make the present smarter.