# 3L Site Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a new static `/3l/` site that matches the approved dark dragon-first mockup, introduces The Third Leg as its own work, and provides safe Record/Listen/Read entry surfaces before story and audio production are complete.

**Architecture:** Add an isolated static HTML/CSS surface under `/3l/`, borrowing the repository's lightweight GitHub Pages approach without reusing R2's visual identity. V1 uses no framework and no required JavaScript. The generated concept art is referenced through stable CSS background paths so the page remains usable before binary assets are manually uploaded.

**Tech Stack:** Static HTML5, CSS, Python 3 unittest contract tests, GitHub Pages.

**Spec:** `docs/superpowers/specs/2026-09-12-3l-site-foundation-design.md`

## Global Constraints

- Public identity is **THE THIRD LEG**, shorthand **3L**, subtitle **A Record of Two Lives**.
- Story situation outranks format explanation.
- Record-first, listen-default. Do not brand 3L as an audio product first.
- Do not reveal the reset bargain, catastrophe, settled-life tragedy, final dungeon, or Greg's possible desire for a third life.
- Do not modify PLG manuscript prose, PLG reader pages, or R2 reader pages as part of this slice.
- Static page must remain usable with JavaScript disabled.
- No React, build pipeline, database, account system, cloud progress sync, or animation-heavy layer.
- Use near-black, charcoal, muted gray, and restrained warm gold. Avoid neon fantasy UI, faux parchment, RPG HUD styling, and streaming-service framing.
- Mobile composition must preserve title, hook, CTA, Greg/dragon scale relationship, Current Record, and timeline legibility.
- Generated image handoff paths are fixed for V1: `3l/assets/images/hero/dragon-bargain.png` and `3l/assets/images/audio/audio-library.png`.
- Missing image binaries must not break the site. CSS gradients/background colors are the fallback.

---

### Task 1: Add a failing 3L site contract test

**Files:**
- Create: `tests/test_3l_site.py`

**Interfaces:**
- Consumes: repository root path.
- Produces: a static contract for required files, identity copy, navigation targets, accessibility hooks, responsive CSS, and manual image handoff paths.

- [ ] **Step 1: Write the failing test**

```python
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


class ThirdLegSiteTests(unittest.TestCase):
    def test_site_files_and_identity(self):
        home = ROOT / "3l" / "index.html"
        css = ROOT / "3l" / "assets" / "css" / "site.css"
        record = ROOT / "3l" / "records" / "001.html"
        records = ROOT / "3l" / "records" / "index.html"
        audio = ROOT / "3l" / "audio" / "index.html"
        about = ROOT / "3l" / "about" / "index.html"
        for path in (home, css, record, records, audio, about):
            self.assertTrue(path.exists(), path)

        html = home.read_text(encoding="utf-8")
        styles = css.read_text(encoding="utf-8")
        self.assertIn("THE THIRD LEG", html)
        self.assertIn("A Record of Two Lives", html)
        self.assertIn("BEGIN THE ACCOUNT", html)
        self.assertIn("THE BARGAINER", html)
        self.assertIn("He came to ask something of a dragon.", html)
        self.assertIn("The price was an explanation.", html)
        self.assertIn('href="records/001.html"', html)
        self.assertIn('href="audio/"', html)
        self.assertIn('href="records/"', html)
        self.assertIn('href="about/"', html)
        self.assertIn('href="#timeline"', html)
        self.assertIn('class="skip-link"', html)
        self.assertIn("dragon-bargain.png", styles)
        self.assertIn("audio-library.png", styles)
        self.assertIn("@media (max-width: 760px)", styles)
        self.assertIn(":focus-visible", styles)
        self.assertNotIn("R3", html)
        self.assertNotIn("autoplay", html.lower())

    def test_record_and_audio_shells_are_safe_before_content_exists(self):
        record = (ROOT / "3l" / "records" / "001.html").read_text(encoding="utf-8")
        audio = (ROOT / "3l" / "audio" / "index.html").read_text(encoding="utf-8")
        self.assertIn("RECORD 001", record)
        self.assertIn("THE BARGAINER", record)
        self.assertIn("The account is being prepared.", record)
        self.assertIn("LISTENING ARCHIVE", audio)
        self.assertIn("No audio records have been published yet.", audio)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test to verify it fails**

Run:

```bash
python -m unittest tests.test_3l_site -v
```

Expected: FAIL because `/3l/` files do not exist yet.

- [ ] **Step 3: Commit the failing test**

```bash
git add tests/test_3l_site.py
git commit -m "test: define 3L site contract"
```

---

### Task 2: Build the 3L landing page and visual system

**Files:**
- Create: `3l/index.html`
- Create: `3l/assets/css/site.css`

**Interfaces:**
- Consumes: fixed concept-art paths `assets/images/hero/dragon-bargain.png` and `assets/images/audio/audio-library.png`.
- Produces: `/3l/` front door with header, bargain hero, Current Record panel, timeline preview, story surfaces, audio-library visual entry, and lineage footer.

- [ ] **Step 1: Create `3l/index.html` with semantic static structure**

The page must include:

```html
<title>The Third Leg · 3L</title>
<meta name="description" content="The Third Leg. Greg has already lived twice. An ancient dragon wants to know how.">
```

Header links:

```html
<a class="site-mark" href="./">3L</a>
<a href="#story">Story</a>
<a href="records/">Records</a>
<a href="#timeline">World</a>
<a href="about/">About</a>
<a href="audio/">Listen</a>
<a href="records/001.html">Read</a>
```

Hero copy:

```html
<p class="hero-subtitle">A Record of Two Lives</p>
<h1>THE THIRD LEG</h1>
<p class="hero-hook">He came to ask something of a dragon.<br>The price was an explanation.</p>
<a class="button button-primary" href="records/001.html">BEGIN THE ACCOUNT</a>
<p class="medium-note">Listen by default · Read available</p>
```

Current Record copy:

```html
<p class="eyebrow">CURRENT RECORD</p>
<p class="record-number">001</p>
<p class="record-meta">SECOND LIFE · AGE 59 · LOCATION WITHHELD</p>
<h2>THE BARGAINER</h2>
<p>Greg remembers forty years that did not happen here.</p>
<dl class="record-facts">
  <div><dt>CLAIM</dt><dd>Lived once before.</dd></div>
  <div><dt>STATUS</dt><dd>Under examination.</dd></div>
  <div><dt>EXAMINER</dt><dd>An ancient dragon.</dd></div>
</dl>
```

Timeline should contain the reveal-safe labels `FIRST LIFE`, `SECOND LIFE`, `19`, `59`, `THE ACCOUNT`, `AHEAD`, and `UNKNOWN` without future event names.

Story surfaces should include `A DIFFERENT LIFE`, `A HIGHER PRICE`, and `WHAT COMES NEXT`, plus a separate listening-archive card that links to `audio/`.

- [ ] **Step 2: Create `3l/assets/css/site.css`**

Define the visual system with explicit variables:

```css
:root {
  color-scheme: dark;
  --bg: #080908;
  --bg-soft: #0d100f;
  --panel: #101311;
  --ink: #ece7dc;
  --muted: #aaa397;
  --faint: #736d63;
  --line: rgba(236, 231, 220, .14);
  --gold: #b9944c;
  --gold-soft: #806837;
  --serif: Georgia, 'Times New Roman', serif;
  --ui: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}
```

Use the manual image paths only as optional background layers:

```css
.hero {
  background-image:
    linear-gradient(90deg, rgba(5,6,5,.94) 0%, rgba(5,6,5,.68) 44%, rgba(5,6,5,.18) 72%, rgba(5,6,5,.42) 100%),
    url('../images/hero/dragon-bargain.png');
}

.audio-entry-art {
  background-image:
    linear-gradient(180deg, rgba(7,8,7,.12), rgba(7,8,7,.88)),
    url('../images/audio/audio-library.png');
}
```

The elements must still have dark background colors so failed image requests degrade cleanly.

Add accessible focus treatment:

```css
:focus-visible {
  outline: 2px solid var(--gold);
  outline-offset: 4px;
}
```

Add a dedicated phone composition at `@media (max-width: 760px)` that moves the hero focal point rightward, stacks navigation, stacks Current Record facts, and makes the timeline vertical rather than shrinking labels below readability.

- [ ] **Step 3: Run the site contract test**

Run:

```bash
python -m unittest tests.test_3l_site -v
```

Expected: still FAIL only for reader/audio/about files not yet added. Landing-page/CSS assertions should pass.

- [ ] **Step 4: Commit landing-page foundation**

```bash
git add 3l/index.html 3l/assets/css/site.css
git commit -m "feat: build 3L landing page"
```

---

### Task 3: Add Record, audio, and about entry shells

**Files:**
- Create: `3l/records/index.html`
- Create: `3l/records/001.html`
- Create: `3l/audio/index.html`
- Create: `3l/about/index.html`

**Interfaces:**
- Consumes: `../assets/css/site.css` and the navigation language established by Task 2.
- Produces: valid destinations for every primary/secondary landing-page route without inventing story prose or fake audio availability.

- [ ] **Step 1: Create the Records index**

Use the shared header/footer. Display:

```html
<p class="eyebrow">THE ACCOUNT</p>
<h1>Records</h1>
<article class="record-list-item">
  <p>RECORD 001</p>
  <h2><a href="001.html">THE BARGAINER</a></h2>
  <p>Second Life · Age 59 · Location withheld</p>
  <p>Opening record. Publication pending.</p>
</article>
```

Do not invent Records 002+.

- [ ] **Step 2: Create the safe Record 001 page**

The page must clearly separate presentation framing from unwritten story text:

```html
<p class="eyebrow">RECORD 001</p>
<h1>THE BARGAINER</h1>
<p class="record-meta">SECOND LIFE · AGE 59 · LOCATION WITHHELD</p>
<section class="pending-record" aria-labelledby="pending-title">
  <h2 id="pending-title">The account is being prepared.</h2>
  <p>This record has a place in the archive, but its authoritative story text has not been published yet.</p>
</section>
```

Link back to `/3l/`, Records, and Listening Archive. Do not write speculative chapter prose.

- [ ] **Step 3: Create the Listening Archive shell**

The page uses the `audio-library.png` background entry art and contains:

```html
<p class="eyebrow">LISTENING ARCHIVE</p>
<h1>The account, heard.</h1>
<p>No audio records have been published yet.</p>
<p>When an audio rendition exists, listening will be the default way into that Record. The written rendition remains alongside it.</p>
<a class="button" href="../records/001.html">Open Record 001</a>
```

No fake player, disabled waveform, or fabricated runtime.

- [ ] **Step 4: Create the About page**

Keep it short and public-facing. Explain only:

- The Third Leg is a distinct work in the Peg-Leg Greg lineage.
- It opens late in Greg's second life with an ancient dragon examining an impossible claim.
- The account moves backward to nineteen, then forward across decades until remembered history catches the present.
- 3L is record-first and listen-default.
- Prior works are optional context.

Add lineage links to `../../index.html` and `../../r2/`.

- [ ] **Step 5: Run the contract test**

Run:

```bash
python -m unittest tests.test_3l_site -v
```

Expected: PASS.

- [ ] **Step 6: Commit the entry surfaces**

```bash
git add 3l/records 3l/audio 3l/about
git commit -m "feat: add 3L record and audio entry surfaces"
```

---

### Task 4: Verify static routing, regressions, and asset handoff

**Files:**
- Test: `tests/test_3l_site.py`
- Verify only: existing PLG/R2 files remain unchanged.

**Interfaces:**
- Consumes: Tasks 1-3.
- Produces: verified branch ready for the user's two manual image uploads and later PR/merge.

- [ ] **Step 1: Run focused tests**

```bash
python -m unittest tests.test_3l_site -v
```

Expected: PASS.

- [ ] **Step 2: Run representative existing UI tests**

```bash
python -m unittest tests.test_book_contents_css tests.test_chapter_role_title_integration -v
```

Expected: PASS.

- [ ] **Step 3: Verify repository diff scope**

Confirm the branch changes only:

```text
3l/**
tests/test_3l_site.py
docs/superpowers/specs/2026-09-12-3l-site-foundation-design.md
docs/superpowers/plans/2026-09-12-3l-site-foundation.md
```

No PLG/R2 source or manuscript files may change.

- [ ] **Step 4: Verify image handoff paths are exactly documented**

The user may upload the generated binaries after site code exists:

```text
3l/assets/images/hero/dragon-bargain.png
3l/assets/images/audio/audio-library.png
```

The site must already render acceptably before those files exist and automatically pick them up once they are added at those exact paths.

- [ ] **Step 5: Final branch commit if verification changes were needed**

```bash
git add tests/test_3l_site.py 3l
git commit -m "test: verify 3L site foundation"
```

If no verification edits were needed, do not create an empty commit.
