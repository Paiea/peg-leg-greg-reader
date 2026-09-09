# R2 Listening Edition Shelf Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn `/greg-again/audio/` into a light-mode, editorial R2 Listening Edition with a derived availability strip, manifest-driven illustrated chapter cards, and optional stable-ID presentation metadata that never blocks audio playback.

**Architecture:** Keep `greg-again/audio/manifest.json` as the sole authority for chapter number, title, duration, audio source, and publication. Add `greg-again/audio/presentation.json` as optional display metadata keyed only by stable `ga-NNN` identity, then have `player.js` join the sources at runtime. HTML/CSS own the page shell and light-mode visual hierarchy; JavaScript owns derived counts, resilient presentation metadata loading, card rendering, and image fallback behavior.

**Tech Stack:** Static HTML, CSS, vanilla browser JavaScript, JSON manifests, Python `unittest` repository contracts, GitHub Pages.

**Spec:** `docs/superpowers/specs/2026-09-09-r2-listening-edition-shelf-design.md`

## Global Constraints

- Audio remains the primary public R2 experience; written chapters remain a secondary reference surface.
- `greg-again/audio/manifest.json` remains authoritative for stable identity, number, title, duration, audio source, and publication state.
- Presentation metadata is optional and keyed by stable `ga-NNN` identity; it must not duplicate mutable title, duration, publication state, or audio source.
- Audio publication must never depend on art or quote availability.
- The public page must not expose experiment, lab, approved render, take count, lens, provider, or production-note language.
- Default visual mode is warm light mode: cream/paper background, dark ink/brown type, muted maroon accents, restrained borders, art supplying most color.
- Desktop chapter cards use two columns when space permits; mobile uses one column.
- Missing presentation metadata, image, or quote must degrade to a complete playable text-first card.
- A title rename must not break art association because joins happen through stable `ga-NNN` identity.
- Native accessible audio controls remain the playback surface.
- No custom streaming player, account progress, story rewrite, audio regeneration, or requirement to create chapter art before page architecture ships.

---

### Task 1: Lock the new public contracts with failing tests

**Files:**
- Modify: `tests/test_r2_audio_front_door.py`

**Interfaces:**
- Consumes: current static files under `greg-again/audio/` and `r2/index.html`.
- Produces: repository contracts for light-mode presentation, runtime-derived availability, stable-ID presentation metadata, graceful fallback behavior, and existing listen-first homepage routing.

- [ ] **Step 1: Add failing contracts for the new shelf architecture**

Add tests that assert:

```python
import json


def test_audio_page_uses_light_listening_edition_shell(self):
    html = (AUDIO / "index.html").read_text(encoding="utf-8")
    css = (AUDIO / "audio.css").read_text(encoding="utf-8")
    front_css = (AUDIO / "audio-front-door.css").read_text(encoding="utf-8")
    self.assertIn("R2 Listening Edition", html)
    self.assertIn('id="availability-summary"', html)
    self.assertIn('id="chapter-list"', html)
    self.assertNotIn("color-scheme: dark", css + front_css)
    self.assertIn("--paper:", css)
    self.assertIn("--accent:", css + front_css)


def test_presentation_manifest_is_stable_identity_only(self):
    payload = json.loads((AUDIO / "presentation.json").read_text(encoding="utf-8"))
    for stable_id, metadata in payload.get("chapters", {}).items():
        self.assertRegex(stable_id, r"^ga-\\d{3}$")
        self.assertNotIn("title", metadata)
        self.assertNotIn("duration_seconds", metadata)
        self.assertNotIn("audio_src", metadata)
        self.assertNotIn("published", metadata)


def test_player_joins_optional_presentation_metadata_without_blocking_audio(self):
    js = (AUDIO / "player.js").read_text(encoding="utf-8")
    self.assertIn("presentation.json", js)
    self.assertIn("stableId", js)
    self.assertIn("Promise", js)
    self.assertIn("availability-summary", js)
    self.assertIn("chapter-art", js)
    self.assertIn("chapter-quote", js)
    self.assertIn("Audio chapters are temporarily unavailable.", js)
```

Retain the existing assertions that experiment-era wording stays absent and the R2 homepage prominently routes to `../greg-again/audio/`.

- [ ] **Step 2: Run the focused contract test and confirm RED**

Run:

```bash
python -m unittest tests.test_r2_audio_front_door -v
```

Expected: FAIL because light-mode tokens, `presentation.json`, availability summary markup, and the new join/fallback renderer do not exist yet.

- [ ] **Step 3: Commit the failing contracts**

```bash
git add tests/test_r2_audio_front_door.py
git commit -m "test: define R2 listening shelf contracts"
```

---

### Task 2: Add the light-mode Listening Edition shell

**Files:**
- Modify: `greg-again/audio/index.html`
- Modify: `greg-again/audio/audio.css`
- Modify: `greg-again/audio/audio-front-door.css`

**Interfaces:**
- Consumes: existing R2 navigation URLs and existing fallback R2 cover art.
- Produces: semantic hero, stable optional hero-art hook, `#availability-summary`, `#chapter-list`, and responsive light-mode card shell for `player.js`.

- [ ] **Step 1: Rework the HTML shell without hard-coding chapter counts**

Update `index.html` so the main hierarchy is:

```html
<section class="listen-hero" aria-labelledby="listen-title">
  <div class="listen-hero-media" data-hero-art>
    <img
      class="listen-hero-image"
      src="../../r2/assets/images/r2-cover-wide.webp"
      data-custom-src="assets/art/listening-edition-hero.webp"
      alt="Peg-Leg Greg R2 artwork in Carrow."
    >
  </div>
  <div class="listen-hero-copy">
    <p class="eyebrow">R2 Listening Edition</p>
    <h1 id="listen-title">Peg-Leg Greg R2</h1>
    <p class="lede">Built to be heard first. Start with Chapter 1, then use the written chapters whenever you want to check a name, line, or detail.</p>
    <a class="listen-start" href="#chapter-list">Start Listening</a>
  </div>
</section>

<section class="availability-strip" aria-label="Listening edition availability">
  <p id="availability-summary">Loading the listening shelf…</p>
  <a href="../../r2/chapters/">Written reference</a>
</section>

<section class="listen-shelf-heading" aria-labelledby="chapters-title">
  <div>
    <p class="eyebrow">Listening shelf</p>
    <h2 id="chapters-title">Chapters</h2>
  </div>
  <p>Choose a role and press play.</p>
</section>

<section id="chapter-list" class="chapter-list" aria-live="polite" aria-label="Playable audio chapters">
  <p class="render-state">Loading chapters…</p>
</section>
```

Do not write a numeric chapter count into HTML.

- [ ] **Step 2: Convert shared audio variables from dark to warm light mode**

In `audio.css`, replace dark defaults with a light editorial palette while preserving readable contrast and accessible focus treatment. Use explicit tokens such as:

```css
:root {
  color-scheme: light;
  --paper: #f3eddf;
  --paper-soft: #e9dfcd;
  --card: #faf6ed;
  --ink: #29231d;
  --muted: #6f6257;
  --faint: #8a7b6d;
  --line: #cfc0aa;
  --line-soft: #ddd1bf;
  --accent: #7a2f2f;
  --accent-strong: #5f2224;
  --serif: Georgia, 'Times New Roman', serif;
  --ui: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}
```

Update links, focus states, borders, and native player accent usage to use the light palette.

- [ ] **Step 3: Build the editorial hero, availability strip, and responsive two-column card shell**

In `audio-front-door.css`, implement:

```css
.listen-hero {
  display: grid;
  grid-template-columns: minmax(0, 1.35fr) minmax(18rem, .65fr);
  gap: clamp(1.5rem, 4vw, 3.5rem);
  align-items: center;
}

.availability-strip {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  padding: 1rem 0;
  border-block: 1px solid var(--line);
}

.chapter-list {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: clamp(1rem, 2.5vw, 1.5rem);
  border-top: 0;
}

.chapter-card {
  overflow: hidden;
  padding: 0;
  border: 1px solid var(--line);
  background: var(--card);
  border-radius: 2px;
}

@media (max-width: 760px) {
  .listen-hero,
  .chapter-list {
    grid-template-columns: 1fr;
  }
}
```

Add `.chapter-art`, `.chapter-card-copy`, `.chapter-quote`, and `.chapter-number` styles that will be consumed by Task 4. Do not require the image block for card layout integrity.

- [ ] **Step 4: Run the focused test**

Run:

```bash
python -m unittest tests.test_r2_audio_front_door -v
```

Expected: still FAIL only on presentation-manifest/player contracts, while the light shell assertions now pass.

- [ ] **Step 5: Commit the shell**

```bash
git add greg-again/audio/index.html greg-again/audio/audio.css greg-again/audio/audio-front-door.css
git commit -m "feat: build light R2 listening edition shell"
```

---

### Task 3: Add optional stable-ID presentation metadata

**Files:**
- Create: `greg-again/audio/presentation.json`

**Interfaces:**
- Consumes: stable audio identities such as `ga-001`.
- Produces: optional `chapters[stable_id] -> {image_src?, alt?, quote?, focal?}` metadata for the public renderer.

- [ ] **Step 1: Create the presentation manifest with no duplicated audio authority**

Create:

```json
{
  "version": 1,
  "hero": {
    "image_src": "assets/art/listening-edition-hero.webp",
    "alt": "Peg-Leg Greg R2 artwork in Carrow."
  },
  "chapters": {}
}
```

The empty `chapters` object is intentional for the first architecture shipment. Approved quotes and art can be added incrementally later. The renderer must not assume all published chapters appear here.

- [ ] **Step 2: Run the presentation contract**

Run:

```bash
python -m unittest tests.test_r2_audio_front_door.R2AudioFrontDoorTests.test_presentation_manifest_is_stable_identity_only -v
```

Expected: PASS.

- [ ] **Step 3: Commit the presentation layer**

```bash
git add greg-again/audio/presentation.json
git commit -m "feat: add optional R2 listening presentation metadata"
```

---

### Task 4: Join manifests and render resilient illustrated audio cards

**Files:**
- Modify: `greg-again/audio/player.js`

**Interfaces:**
- Consumes: `manifest.json` chapters plus optional `presentation.json` metadata keyed by stable identity.
- Produces: `stableId(chapter) -> ga-NNN`, derived availability summary, optional hero replacement, and complete playable `.chapter-card` nodes whether or not presentation metadata exists.

- [ ] **Step 1: Add stable identity and safe optional-presentation loading**

Implement helpers with these exact responsibilities:

```javascript
function stableId(chapter) {
  const explicit = chapter.id || chapter.chapter_id || chapter.audio_id;
  if (typeof explicit === 'string' && /^ga-\d{3}$/.test(explicit)) return explicit;
  return `ga-${String(chapter.number).padStart(3, '0')}`;
}

async function loadOptionalPresentation() {
  try {
    const response = await fetch('presentation.json', { cache: 'no-store' });
    if (!response.ok) return { hero: null, chapters: {} };
    const payload = await response.json();
    return {
      hero: payload.hero || null,
      chapters: payload.chapters || {},
    };
  } catch (error) {
    console.warn('Presentation metadata unavailable.', error);
    return { hero: null, chapters: {} };
  }
}
```

The audio-manifest fetch remains fatal for the shelf; presentation fetch is non-fatal.

- [ ] **Step 2: Render optional art and quote without creating broken frames**

Change `renderChapter` to accept presentation metadata:

```javascript
function renderChapter(chapter, presentation = {}) {
  const card = document.createElement('article');
  card.className = 'player-card chapter-card';

  if (presentation.image_src) {
    const art = document.createElement('img');
    art.className = 'chapter-art';
    art.src = presentation.image_src;
    art.alt = presentation.alt || '';
    art.loading = 'lazy';
    art.addEventListener('error', () => art.remove(), { once: true });
    card.append(art);
  }

  const copy = document.createElement('div');
  copy.className = 'chapter-card-copy';

  const number = document.createElement('p');
  number.className = 'chapter-number';
  number.textContent = `Chapter ${chapter.number}`;

  const heading = document.createElement('h3');
  heading.className = 'chapter';
  heading.textContent = chapter.title;

  copy.append(number, heading);

  if (presentation.quote) {
    const quote = document.createElement('blockquote');
    quote.className = 'chapter-quote';
    quote.textContent = presentation.quote;
    copy.append(quote);
  }

  const meta = document.createElement('p');
  meta.className = 'chapter-meta';
  meta.textContent = formatDuration(chapter.duration_seconds);

  const audio = document.createElement('audio');
  audio.controls = true;
  audio.preload = 'metadata';
  audio.src = chapter.audio_src;
  audio.setAttribute('aria-label', `Play Chapter ${chapter.number}: ${chapter.title}`);

  copy.append(meta, audio);
  card.append(copy);
  return card;
}
```

A missing/broken art image removes itself; missing quote creates no empty quote container.

- [ ] **Step 3: Derive public availability from the loaded audio manifest**

After the manifest resolves, set:

```javascript
const availability = document.getElementById('availability-summary');
const playable = manifest.chapters || [];
availability.textContent = `${playable.length} playable chapter${playable.length === 1 ? '' : 's'} · Written reference available`;
```

Do not hard-code `23` or any other count.

- [ ] **Step 4: Load audio and presentation together without making presentation fatal**

Use a Promise-based flow such as:

```javascript
const [manifestResponse, presentation] = await Promise.all([
  fetch('manifest.json', { cache: 'no-store' }),
  loadOptionalPresentation(),
]);
```

Validate only `manifestResponse.ok` as fatal. Join each chapter using:

```javascript
const id = stableId(chapter);
chapterList.append(renderChapter(chapter, presentation.chapters[id] || {}));
```

If `presentation.hero.image_src` exists, attempt to load it into the hero image and restore the existing cover fallback on error. Do not leave a broken hero image.

- [ ] **Step 5: Run focused tests**

Run:

```bash
python -m unittest tests.test_r2_audio_front_door -v
```

Expected: PASS.

- [ ] **Step 6: Commit the runtime renderer**

```bash
git add greg-again/audio/player.js
git commit -m "feat: render resilient illustrated R2 audio cards"
```

---

### Task 5: Verify integration against current R2 and audio authority

**Files:**
- Modify only if verification exposes a genuine regression: files from Tasks 1-4.

**Interfaces:**
- Consumes: completed listening shelf implementation plus newest `main` authority.
- Produces: a PR-ready branch that preserves newer published audio and passes all existing site/audio contracts.

- [ ] **Step 1: Reconcile the implementation branch with newest `main`**

Run:

```bash
git fetch origin
git rebase origin/main
```

Resolve conflicts by preserving newest audio manifest/chapter publication authority from `main` and the listening-shelf presentation changes from this branch. Never roll back newly published audio.

- [ ] **Step 2: Run focused R2 listening tests**

Run:

```bash
python -m unittest tests.test_r2_audio_front_door -v
```

Expected: PASS.

- [ ] **Step 3: Run Greg Again audio validation**

Run the repository's current audio validation command as defined by current `r2/AUDIO_PRODUCTION.md` / workflow authority. If the repository still uses the existing validation suite directly, run the matching audio test module(s) and ensure the manifest remains valid.

Expected: PASS with no audio identity, route, or manifest regressions.

- [ ] **Step 4: Run the full repository test suite**

Run:

```bash
python -m unittest discover -s tests -p 'test_*.py'
```

Expected: PASS, with only already-authorized skips.

- [ ] **Step 5: Inspect the final diff for product-language regressions**

Confirm the diff does not reintroduce public strings including:

```text
Audio Experiments
Listening lab
Playable experimental render
Approved render
performance takes
provider
```

Also confirm no literal current chapter count was added to `index.html`.

- [ ] **Step 6: Commit any verification-only fixes, then open a PR**

If no fixes were needed, do not create an empty commit. Open a PR titled:

```text
Polish R2 Listening Edition shelf
```

PR body should state that the page now uses the light R2 visual system, derives availability from the audio manifest, supports stable-ID optional art/quote presentation data, and remains fully playable without art.

- [ ] **Step 7: Require green PR-head checks before merge**

Verify fresh PR-head checks for the R2 site, Showcase/full test suite, and Greg Again audio validation. Merge only after the current PR head is green and reconciled with newest `main`.
