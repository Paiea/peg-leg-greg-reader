# 3L / The Third Leg - Site Foundation Design

**Status:** Approved visual direction, awaiting written-spec review before implementation.

**Project:** `Paiea/peg-leg-greg-reader`

**Public identity:** **THE THIRD LEG**

**Working shorthand:** **3L**

## 1. Purpose

Build a new reader-facing 3L surface that feels like a story world first and a publishing interface second.

The landing page should place the reader inside the opening dramatic situation: an older Greg has deliberately reached an ancient dragon and is making an impossible claim. The site should make that situation feel materially real without explaining the whole project, spoiling the reset mechanism, or presenting 3L as an experimental dashboard.

The core front-door question is:

> Why is Greg talking to a dragon, and what does he want badly enough to be here?

The second question follows naturally:

> How has he already lived twice?

The third question should remain concealed until the story earns it:

> Does Greg want another reset too?

## 2. Product identity

3L is not "R3" in public presentation.

Use:

- **3L** as the compact project mark
- **THE THIRD LEG** as the public title
- **A Record of Two Lives** as the initial subtitle

Lineage may appear quietly in secondary navigation or the footer:

`PLG -> R2 -> 3L`

The landing page must not lead with the production lineage. A new visitor should be able to enter 3L without understanding Run 1 or R2.

## 3. Formal story model

Reader order remains normal:

`Record 001 -> Record 002 -> ... -> final record`

The opening begins late in Greg's Life Two with the dragon. The account then returns to Greg at nineteen and advances forward through decades of Life Two, with selective returns to the dragon frame.

Two timelines therefore advance at once:

1. **The Account**: Greg's remembered Life Two advances from age nineteen toward the dragon encounter.
2. **The Examination**: the dragon-frame present advances from Greg's arrival toward whatever bargain, expedition, dungeon, and unknown future follow.

Eventually the remembered timeline catches the opening frame. At that point the story moves beyond remembered history into genuinely unknown time.

This structural event should later be visible in the site's temporal presentation. Before catch-up, the interface speaks in archival language such as `RECORD`, `ACCOUNT`, `EVIDENCE`, and `VERIFICATION`. After catch-up, the interface may change to a simpler present-state language such as `NOW` or `AHEAD`.

That transition is a future story-state feature, not required for the first implementation.

## 4. Architectural principle

**Record-first, listen-default.**

R2 foregrounds audio as the defining product experience. 3L should foreground the story situation and record structure, while still making listening the preferred default consumption path.

The hierarchy is:

1. Story / Record authority
2. Listener-facing audio rendition
3. Written rendition
4. Evidence, timeline, atlas, and visual surfaces derived from earned story state

The landing-page primary action is fiction-owned language such as:

**BEGIN THE ACCOUNT**

The UI may route that action to audio-first Record 001 when audio exists, but the button should not read "Start Listening" as the principal project identity.

Secondary medium controls may read:

`LISTEN` and `READ`

or

`Listen by default · Read available`

## 5. Visual direction

The approved mockup establishes the initial visual target:

- near-black base
- cold charcoal, wet stone, muted gray atmosphere
- restrained warm gold as the meaningful accent
- old Greg visually small against an enormous ancient dragon
- dragon partially concealed by geography, shadow, scale, and darkness
- the dragon should feel like a place before it feels like a creature
- Greg should not cower, posture like an action hero, or visually dominate the frame
- Greg should look like someone who came deliberately and prepared to speak
- serif-led book typography with restrained small-cap labels
- very limited ornament
- thin rule lines and low-contrast panels
- no neon fantasy UI
- no streaming-service visual language
- no glowing RPG rarity frames
- no faux parchment
- no generic game HUD

The page should feel cinematic and literary, not like a fantasy dashboard.

### Hero art requirements

Hero art must carry story information rather than generic mood.

It should establish:

- old Greg is here intentionally
- the dragon is vastly beyond Greg in physical scale
- the dragon is allowing the conversation to continue
- Greg has lived enough life to visibly differ from the young Greg of prior projects
- the environment feels ancient and materially real

Do not lock unearned body continuity into the final hero art before the relevant 3L story authority exists. The first implementation may use approved concept art as a visual placeholder, but production art should later source-lock to the actual opening Record.

## 6. Landing-page composition

### 6.1 Global header

Compact, non-sticky by default unless testing proves otherwise.

Left:

- `3L` mark

Primary navigation:

- Story
- Records
- World
- About

Right:

- Listen
- Read

Do not expose production controls, status tools, authoring jargon, or a giant mode switcher.

### 6.2 Hero: The Bargain

Full-width dramatic hero with image and dark overlay.

Primary copy:

**THE THIRD LEG**

*A Record of Two Lives*

Initial hook:

> He came to ask something of a dragon.  
> The price was an explanation.

Primary CTA:

**BEGIN THE ACCOUNT**

Secondary line:

`Listen by default · Read available`

The hero may include one short dragon line or examination fragment if it improves tension. It must not reveal the reset bargain, the catastrophe, Greg's eventual losses, or the dungeon.

### 6.3 Current Record

Immediately below the hero, introduce the record language with a restrained artifact-like panel.

Initial concept:

`CURRENT RECORD`

`001`

`SECOND LIFE · AGE 59 · LOCATION WITHHELD`

**THE BARGAINER**

> Greg remembers forty years that did not happen here.

Possible small fields:

- `CLAIM: Lived once before.`
- `STATUS: Under examination.`
- `EXAMINER: An ancient dragon.`

Possible earned-state marker:

`VERIFICATION 01 · Correct.`

These fields are narrative presentation, not backend status indicators. They should be sparse enough to feel like evidence from the story rather than an admin panel.

When exact Record 001 prose exists, all claims and labels on this card must be reconciled against that authority.

### 6.4 Timeline

A restrained horizontal temporal surface below the Current Record.

Initial conceptual rows:

`FIRST LIFE` with most detail withheld

`SECOND LIFE   19 ---------------- 59`

`THE ACCOUNT` marking the dragon-frame present

`AHEAD ---------------- UNKNOWN`

Rules:

- no spoiler-rich event map on first visit
- reveal only what the reader has earned
- the visual should communicate relationship between remembered time and current examination, not function as a completion meter
- age/date matters more than chapter count
- the timeline must be legible on mobile through stacking or horizontal overflow without microscopic labels

Future state:

When the lived chronology catches the dragon frame, the temporal UI may visibly cross from remembered record into unknown time.

### 6.5 Story surfaces

Below the timeline, allow up to three restrained entry cards that support the fiction rather than market features.

Initial concepts from the approved mockup:

- **A DIFFERENT LIFE**: forty years, countless choices, a future that never was
- **A HIGHER PRICE**: memory is valuable; some things want to buy it
- **WHAT COMES NEXT**: when the past is told, there is nowhere left to hide

These are provisional landing-page copy. They are not canon and should be rewritten when the first 3L records establish better language.

Cards may later route to:

- story/about surface
- earned evidence/record material
- timeline/atlas

Do not create empty lore pages merely to satisfy the mockup.

### 6.6 Footer

Minimal footer:

- 3L mark
- one short project line
- quiet lineage: `PLG -> R2 -> 3L`
- links to prior projects

Avoid fake social icons, fake terms/privacy links, or placeholder commercial furniture that has no real destination.

## 7. Content architecture

Create the new site as an isolated surface under:

`/3l/`

Recommended initial structure:

```text
3l/
  index.html
  assets/
    css/
      site.css
    js/
      site.js
    images/
      hero/
  records/
    index.html
  about/
    index.html
  data/
    site.json
    records.json
    timeline.json
```

This structure is intentionally small. It does not require a framework.

Use static HTML, CSS, and lightweight JavaScript consistent with the existing GitHub Pages repository. Do not introduce React, a build pipeline, a database, or a second hosting stack for the first version.

### Data responsibilities

`site.json`

- public title/subtitle
- current record id
- primary entry route
- medium routes when available

`records.json`

- public record id
- embodied role/title
- age/time metadata
- reveal-safe summary
- audio path when available
- written path when available
- public availability state

`timeline.json`

- reveal-safe temporal anchors only
- state can expand as story authority grows
- no future spoilers in public data

The exact schema may be simplified during implementation if static HTML alone is cleaner for the first page. Do not create JSON merely because the design lists it. The implementation plan should apply YAGNI.

## 8. Record naming

3L should preserve the successful embodied-role naming principle:

**THE BARGAINER**

rather than generic event labels such as "The Dragon Cave" or "A Strange Meeting."

Chapter/Record names should describe a role Greg inhabits in the scene or movement where possible.

This is presentation doctrine, not permission to rename story authority without review.

## 9. Reader behavior

### Primary entry

`BEGIN THE ACCOUNT` opens Record 001.

When audio exists, listening is the default rendition.

When audio does not yet exist, the button should still work and route to the written Record rather than becoming dead UI.

### Continue state

A later implementation may remember local progress and change the primary action to `CONTINUE THE ACCOUNT`, but persistent cross-device sync is out of scope for the foundation.

### Medium switching

Listen and Read should be sibling renditions of the same Record, not different story branches.

Switching medium should preserve the current Record id where possible.

## 10. Responsive behavior

Desktop hero may use a wide cinematic composition similar to the approved mockup.

Mobile must be separately composed rather than merely shrinking the desktop canvas.

Mobile priorities:

1. title
2. hook
3. CTA
4. Greg/dragon power relationship
5. current Record
6. timeline

Allow the hero image crop to shift so Greg and the dragon remain legible.

Timeline may stack vertically on narrow screens.

Touch targets must remain generous. Decorative labels may shrink, but core reading text should not.

## 11. Accessibility

- semantic heading hierarchy
- visible keyboard focus
- sufficient contrast for all functional text
- decorative art should not carry essential information alone
- hero alt text should describe the relevant scene without exposing unrevealed spoilers
- buttons/links must remain understandable without the background image
- respect reduced-motion preference if any subtle transitions are added later

The first version should not require animation.

## 12. Performance

- static-first implementation
- one optimized hero image, with responsive image sources when practical
- no autoplay media on the landing page
- no heavyweight JS framework
- defer noncritical scripts
- lazy-load below-fold art
- preserve usable text/CTA if JavaScript fails

## 13. Relationship to existing PLG and R2 surfaces

Do not replace or rewrite the existing PLG or R2 sites during the 3L foundation build.

3L is a third distinct presentation lane.

Existing project guidance favors one persistent project URL and static reader surfaces. 3L should therefore initially live inside the current GitHub Pages repository under `/3l/` while presenting as its own work.

Later, if a dedicated domain is desired, it can route to the same static 3L surface without moving story authority.

## 14. Story-authority safeguards

The landing page is not plot authority.

Current brainstormed elements such as:

- exact reset mechanics
- Greg's reason for seeking another reset
- who dies in Life Two
- whether Greg loses a leg
- final catastrophe mechanics
- final dungeon structure
- whether the dragon receives a reset

remain story-development material until established by 3L authority.

The site may imply the opening dramatic situation but must not silently canonize unresolved theory.

Before promoting any detailed landing-page statement, reconcile it against the newest 3L story authority.

## 15. Initial implementation scope

The first implementation should deliver a complete, convincing front door without pretending all downstream systems already exist.

In scope:

- `/3l/` landing page
- approved dark/gold visual language
- header/navigation shell
- bargain hero
- Begin the Account CTA
- Current Record panel
- restrained timeline preview
- up to three story-surface cards
- footer and quiet lineage
- responsive desktop/mobile behavior
- placeholder-safe routing for not-yet-published Records
- foundation CSS and minimal JS only where useful

Out of scope for this first slice:

- full 300-Record reader
- final Record schema
- completed audio pipeline
- full atlas
- interactive spoiler-aware world map
- account login
- server storage
- cloud progress sync
- automatic story-state unlock engine
- animation-heavy transitions
- dedicated new hosting stack
- rewriting PLG or R2 pages

## 16. Validation

Foundation acceptance checks:

1. `/3l/` loads directly on GitHub Pages without requiring JavaScript.
2. Hero clearly reads as **THE THIRD LEG**, not R2/R3.
3. First screen establishes Greg, dragon, bargain, and mystery without explaining the reset plot.
4. Primary CTA has a valid destination or explicit safe placeholder behavior.
5. Desktop and phone layouts preserve the Greg/dragon power relationship.
6. Current Record panel feels narrative, not administrative.
7. Timeline communicates two-life/time structure without exposing unearned spoilers.
8. PLG and R2 links still work and their surfaces are unchanged.
9. No prose authority is edited as a side effect.
10. Page remains usable with JS disabled.
11. Basic keyboard navigation and contrast pass.
12. Hero asset path is valid and missing-art fallback does not break the page.

## 17. Design decisions already approved in conversation

The following are treated as approved direction for the site design:

- public title **THE THIRD LEG** / shorthand **3L**
- dragon scene is the opening landing-page identity
- reader order is normal 1 -> N even though causal design is developed backward
- Greg's account moves from the dragon frame back to age nineteen and then forward through Life Two
- audio remains important but the site is record-first rather than audio-branded
- landing page should feel dark, cinematic, restrained, and materially real
- story situation outranks format explanation
- lineage to PLG/R2 remains secondary
- the approved mockup is the visual reference for the first build

## 18. Open implementation choices

These do not block the foundation build and should be resolved in the implementation plan or by direct inspection during the build:

- whether the hero concept image is temporarily reused, regenerated at exact production dimensions, or replaced with a source-locked Record 001 illustration
- exact `site.json` / `records.json` use versus simpler static HTML for V1
- exact path of the initial Record 001 placeholder/reader surface
- whether World/About links launch with real minimal pages or remain omitted until content exists

Default principle: remove dead or fake UI rather than shipping empty pages.

## 19. Success criterion

A first-time visitor should land on `/3l/` and understand, within seconds:

- this is a distinct fantasy work called **The Third Leg**
- an older Greg has come deliberately to an ancient dragon
- Greg claims knowledge that should be impossible
- the dragon is examining him
- the visitor can begin the account immediately

The visitor should **not** yet know:

- the final reset bargain
- the catastrophe
- the settled-life tragedy
- whether Greg wants a third life
- what waits in the final dungeon

The page succeeds when it creates appetite for Record 001 rather than explaining the architecture behind it.
