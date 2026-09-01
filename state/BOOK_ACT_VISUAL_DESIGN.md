# PEG-LEG GREG — BOOK & ACT VISUAL DESIGN

Approved reader presentation direction for the Illustrated table of contents.

## Goal

Give the Illustrated contents more visual personality without turning it into a landing page, dashboard, or giant art showcase.

Target:

**A BOOK → WITH NICE ILLUSTRATIONS**

not:

**A WEBSITE → ABOUT A BOOK**

The images should help readers recognize where they are in the story and make each Book feel distinct.

## Shared Book / Act structure

### BOOK I — Chapters 1–82

- Act I — THE SECOND LIFE — 1–20
- Act II — MAKING A PLACE — 21–63
- Act III — THE NEW BASELINE — 64–82

### BOOK II — Chapters 83–current

- Act I — A LIFE IN CARROW — 83–111
- Act II — THE STAGE DOOR — 112–137
- Act III — THE COMPANY ROAD — 138–180
- Act IV — THE WORKING COMPANY — 181–217
- Act V — THE PRICE OF ATTENTION — 218–current

Book and Act boundaries follow story progression/state, not equal chapter counts.

## Book visual

Each Book gets one small high-resolution illustration.

This is not a hero banner. Think:

**illustrated bookplate / miniature cover / visual chapter divider**

rather than:

**cinematic website header**

### Desktop

- target visible width: approximately 260–340 px
- hard maximum around 360 px
- sit beside or immediately above the Book heading
- image should not be wider than the Act contents themselves

### Mobile

- stack naturally above the Book heading
- approximately 70–85% of available content width
- retain a sensible maximum so tablets do not enlarge it excessively

## Image shape

Preferred aspect ratio:

**4:5 or 3:4 portrait**

The goal is a book-cover / plate / frontispiece feeling, not a 16:9 website banner.

## Visual style

Book plates should relate to existing chapter artwork but be cleaner and more resolved because only a few are needed.

Target:

**high-resolution illustrated novel art**

with:

- sketch + ink + painterly texture
- strong environmental storytelling
- slightly handmade quality
- restrained detail
- believable world
- no text baked into the generated image

Do not generate literal fake book covers with AI-generated titles. Book labels/titles remain real HTML text.

## What the Book images should show

Do not make them simple Greg portraits. Each should represent the state of his life during that Book.

### Book I

Communicate:

**arrival → survival → finding footing → bodily transformation → new baseline**

Possible ingredients:

- Greg relatively small within Carrow
- old streets
- work
- roads
- distant buildings
- practical tools/objects
- crutches where appropriate to the represented point
- uncertainty and exploration

Not heroic. Not fantasy-action key art.

### Book II

Communicate:

**ordinary life becoming complicated and interconnected**

Possible ingredients:

- theatre
- company road
- carts / backstage objects
- clothing / work
- people moving through Greg's environment
- Carrow or another inhabited setting
- travel
- increased social pressure

Greg does not need to dominate the composition.

Book I: **finding a life**

Book II: **living inside one**

## Act visuals

Do not generate full illustrations for every Act right now.

If Act visuals are introduced later, prefer tiny 32–56 px vignettes/icons such as:

- road
- window
- crutch
- lantern
- sewing needle/thread
- stage curtain
- theatre mask
- wagon wheel
- door
- glove
- coin
- coat
- prop
- street sign
- architectural silhouette

Typography alone is acceptable for now. The Book plate is the main visual investment.

## Act presentation

Acts remain expandable.

Keep:

- Book label small
- Act name prominent
- chapter range quiet
- chapter list straightforward
- ample whitespace

Avoid:

- progress meters
- status badges
- giant buttons
- statistics
- excessive cards
- glowing UI
- animations
- nested dashboard chrome

## Color and frame

Images should feel physically placed into the page.

Use restrained treatment only:

- subtle warm-gray border
- small radius or square print-like edges
- gentle shadow only if useful
- generous breathing room

Do not use giant glossy cards.

## High-resolution source requirement

Generate Book plates large even though they display small.

Preferred source:

- at least ~1500 px on the long edge
- ideally ~1800–2400 px

High-resolution source does not mean large visible image.

The principle is:

**small on screen, crisp in quality**

## Image loading

Book plates should:

- use normal responsive `<img>`
- have explicit width/height or aspect ratio to prevent layout jump
- use descriptive alt text
- use lazy loading for below-fold Book II where appropriate
- never force-upscale beyond intrinsic dimensions

## Reader difference

### Illustrated

Receives:

- Book plates
- existing chapter illustrations
- potentially tiny Act vignettes later

### Light

Receives:

- same Book hierarchy
- same Act names
- same chapter organization
- no Book images

Light remains intentionally text-first.

## Visual priority

The hierarchy should feel like:

**BOOK** — small image + name

↓

**ACT** — title + range

↓

**CHAPTERS** — simple readable links

The Book image should provide a brief internal-title-page moment, then get out of the way.

## Avoid

Do not introduce:

- giant homepage banners
- full-width cinematic imagery
- fake 3D book mockups
- AI-generated text embedded in pictures
- image backgrounds behind chapter links
- an image for every subdivision
- fantasy-game UI
- streaming-service presentation
- dashboard statistics
- decorative clutter
- oversized branding

## Target feeling

**A nicely illustrated physical novel translated to the web.**

Not a promotional website for a fantasy franchise.

The Book plates should feel like reaching a new internal title page in a printed novel:

**small → crisp → beautiful → back to reading**
