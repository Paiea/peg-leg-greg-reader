# Long-Form Story Compiler — CHARACTER PRESSURE

Status: **active derived contract**

Authority: derived-only. Accepted canon prose remains final story authority.

## Why this exists

If Peg-Leg Greg remains the main long-form vehicle, the cast has to carry far more story weight.

A system can produce competent continuity, useful ideas, and technically good scenes while still generating a weak long-form cast. Common failure modes are:

- recurring characters who mainly ask the protagonist questions
- everyone accepting the protagonist's framing
- the protagonist owning every good idea and solution
- names that sound like variants of the same generated fantasy name
- interchangeable competencies
- dialogue differentiated only by one gimmick
- characters who stop existing when they leave the scene
- relationships that differ in topic but not behavior
- supporting characters who never improve, drift, fail, earn, organize, resent, or solve things off-camera

This layer makes those failures visible before prose repetition turns them into canon texture.

## Core equation

```text
STRONG CAST = DISTINCT PRESSURE + INDEPENDENT MOTION + RELATIONAL SPECIFICITY
```

Characters should not merely be memorable descriptions. They should alter what happens.

## Depth by recurrence

Do not give every named extra a biography.

Use tiers:

- `core` — story-carrying recurring character
- `recurring` — meaningful repeated presence with independent life
- `local` — bounded arc / workplace / institution / scene-cluster character
- `extra` — functional one-scene or background person

The deepest pressure checks apply to `core` and `recurring` characters.

## Required recurring-character pressure

A strong recurring character should normally have:

### 1. A want

Not just a personality trait.

Prefer something that can create behavior, cost, refusal, or initiative.

Weak:

> likes Greg

Stronger:

> wants control of the training schedule because the hall's survival depends on keeping paying students

The want may involve the protagonist. It should not depend entirely on the protagonist's existence.

### 2. Off-camera motion

Ask:

> What is this person doing while Greg is somewhere else?

Examples:

- recruiting
- dating
- healing
- training
- taking other clients
- making money
- losing money
- repairing something
- avoiding someone
- building a friendship Greg is not part of
- changing jobs
- learning a skill
- becoming resentful
- improving a process
- making a bad decision
- solving a problem before Greg arrives

Elapsed time should be able to change supporting characters too.

### 3. Distinguishing competence / leverage

Give the character a real way to matter.

This does not mean combat power.

Possible leverage:

- physical skill
- social access
- procedural knowledge
- money
- labor
- reputation
- beauty/status
- information
- emotional intelligence
- institutional authority
- stubborn endurance
- logistics
- craft knowledge
- willingness to do something Greg will not

### 4. Cost / limit / blind spot

Competence without cost creates helper NPCs.

A useful limit changes what the character will do, not just what they feel.

### 5. Scene agency

A recurring character should sometimes:

- start the scene's real problem
- interrupt Greg's plan
- refuse access
- improve the plan
- solve the problem first
- choose a different win condition
- leave
- spend money without him
- make a promise he cannot control
- bring another relationship into the room
- misunderstand him and act on it
- force him to react

Greg should not own every scene just because he owns the POV.

### 6. Relationship specificity

A character is not one voice delivered to everyone.

Ask how the same person changes around:

- Greg
- a lover
- a rival
- a subordinate
- a parent/child/sibling
- a customer
- somebody they fear
- somebody whose approval they do not need

Relational behavior is more useful than catchphrases.

## Character-driven long form

If PLG is the main vehicle, supporting characters should generate arcs that Greg can enter rather than every arc originating inside Greg.

Healthy examples:

- Greg returns after three weeks and discovers Hessa changed the experiment protocol without him
- a business relationship becomes a friendship while Greg is busy elsewhere
- somebody he helped no longer needs him
- a friend acquires a new obligation that competes with Greg
- two supporting characters develop a relationship Greg only gradually notices
- a character solves something in a way Greg dislikes
- somebody leaves because time made waiting irrational
- a local economic or institutional mechanism grows through people other than Greg

The cast should make time heavier because they continue living through it.

## Name differentiation

Generated fantasy names are especially prone to local similarity.

Before a new recurring/local name settles, compare it against the active roster.

Avoid clusters like:

```text
Jorren
Joran
Torren
```

Even if each name is individually readable, long-form readers must retain dozens of people across hundreds of chapters.

Check:

- spelling silhouette
- opening sounds
- ending sounds
- length
- rhythm / syllable count
- role proximity
- frequency of appearance

Similar names are more dangerous when characters also occupy similar social roles.

The mechanical helper deliberately warns on close spelling similarity. This is an early-review warning, not final naming authority.

## Distinctness is broader than names

Two characters may have different names and still feel cloned.

Check separation across multiple axes:

- what they want
- what they notice first
- what they are good at
- what embarrasses them
- what they spend money on
- how quickly they act
- tolerance for risk
- relationship to authority
- relationship to work
- relationship to Greg
- humor tolerance
- physical habits
- information access
- what they refuse to do
- how they behave when wrong

Do not turn these into a checklist visible in prose. They are generation pressure.

## Greg ownership warning

PLG's analytical POV naturally tempts generation to let Greg:

1. notice the problem
2. understand the mechanism
3. invent the solution
4. convince everybody
5. execute it
6. explain what it meant

Repeated often enough, this makes the whole cast smaller.

Deliberately test variants where:

- Greg notices but someone else solves
- somebody else notices first
- Greg's interpretation is wrong
- the best solution violates Greg's preference
- another character has better domain expertise
- Greg arrives after the important decision
- Greg's contribution is logistical or relational rather than intellectual ownership
- the system grows beyond anybody's control

## Character PERFORMANCE

High-heat PERFORMANCE is especially valuable when the uncertainty is not plot but **who this person becomes under pressure**.

Good targets:

- first meaningful disagreement
- trust rupture
- attraction where both people have independent initiative
- money conflict
- professional jealousy
- somebody succeeding without Greg
- somebody rejecting help
- someone choosing another person over Greg
- old relationship after a long time gap
- behavior after status reversal

Do not predetermine the desired emotional result merely to satisfy the planned arc.

## Operational helper

Use:

`scripts/story_character_pressure.py`

`compile_character_pressure(region)` returns:

- normalized cast tiers
- wants
- off-camera motion
- competence / leverage
- costs / limits
- scene vectors
- relationship-specific behavior
- optional voice/behavior markers
- time changes
- active-roster name comparisons
- warnings for missing recurring-character pressure
- warnings for generated-name similarity
- questions for REHEARSAL / interval design / prose review

It has no canon authority.

## Acceptance questions

For a meaningful long-form region, ask:

1. Who besides the protagonist can move the story?
2. What does each recurring character do off-camera?
3. Who solved or worsened something without Greg?
4. Whose life changed because time passed?
5. Who owns a competence Greg does not?
6. Who can say no and make it stick?
7. Does each major relationship produce distinct behavior rather than generic banter?
8. Are names easy to distinguish after twenty chapters apart?
9. Could two recurring characters swap scenes without much changing? If yes, why do both exist?
10. Did Greg own every good idea again?

## Anti-rules

Do not:

- turn every extra into a protagonist
- force quirky speech patterns for differentiation
- create random tragedy to make a character 'deep'
- make every supporting character secretly exceptional
- remove Greg's competence to make others matter
- require every relationship to become conflict
- confuse name novelty with character distinctness
- let character-card detail substitute for on-page agency

The target is a cast whose independent lives create pressure, opportunity, affection, irritation, surprise, and story even when Greg is not looking.
