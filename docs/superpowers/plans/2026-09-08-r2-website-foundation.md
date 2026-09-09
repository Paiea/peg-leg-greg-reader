# R2 Website Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a standalone `/r2/` static reader that explains Run 2, foregrounds the existing Chapter 1 audio experiment, supports written and illustrated chapter renderings, and leaves Run 1 untouched.

**Architecture:** R2 is a manifest-driven static site under `/r2/`. `data/project.json` owns public chapter order and lineage links; one chapter manifest owns presentation metadata for Chapter 1; reusable JavaScript renders the chapter browser, chapter page, and gallery. The existing `greg-again/audio/assets/chapter-001.mp3` stays in place and is referenced rather than duplicated.

**Tech Stack:** GitHub Pages, static HTML/CSS/vanilla JavaScript, JSON manifests, Python `unittest` structural tests.

**Spec:** `docs/superpowers/specs/2026-09-08-r2-website-design.md`

## Global Constraints

- Build on `r2/website-foundation`; do not modify the existing Run 1 root reader.
- Keep R2 audio-first while preserving Read and Look as first-class surfaces.
- Use the public line `Greg has had two lives so far. So has his story.`
- Explain Run 1 as lineage, not as deprecated software.
- Reuse the existing Chapter 1 audio at `greg-again/audio/assets/chapter-001.mp3`.
- Do not invent unpublished R2 prose; missing written or chapter-art media must degrade cleanly.
- Keep the site static, responsive, book-like, restrained, and manifest-driven.
- Use stable chapter IDs such as `r2-ch001`.

---

### Task 1: Lock the manifest contract with failing structural tests

**Files:**
- Create: `tests/test_r2_site.py`
- Create: `r2/data/project.json`
- Create: `r2/data/chapter-registry.json`
- Create: `r2/data/chapters/ch001.json`

**Interfaces:**
- Consumes: existing Run 1 root reader and `greg-again/audio/assets/chapter-001.mp3`.
- Produces: `project.json` with `project_id`, `title`, `subtitle`, `story_title`, `tagline`, `run1_href`, `current_chapter`, and ordered `chapters`; chapter manifest with `audio`, `written`, `images`, and navigation objects.

- [ ] **Step 1: Write the failing manifest tests**

```python
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
R2 = ROOT / "r2"

class R2SiteTests(unittest.TestCase):
    def test_project_manifest_names_run_two_and_preserves_run_one(self):
        project = json.loads((R2 / "data/project.json").read_text(encoding="utf-8"))
        self.assertEqual(project["project_id"], "r2")
        self.assertEqual(project["title"], "R2")
        self.assertIn("two lives", project["tagline"].lower())
        self.assertEqual(project["run1_href"], "../index.html")
        self.assertEqual(project["chapters"], ["r2-ch001"])

    def test_chapter_one_reuses_existing_audio_without_claiming_missing_prose(self):
        chapter = json.loads((R2 / "data/chapters/ch001.json").read_text(encoding="utf-8"))
        self.assertEqual(chapter["chapter_id"], "r2-ch001")
        self.assertEqual(chapter["title"], "The Boy")
        self.assertEqual(chapter["audio"]["status"], "published")
        self.assertEqual(chapter["audio"]["path"], "../../greg-again/audio/assets/chapter-001.mp3")
        self.assertEqual(chapter["written"]["status"], "unavailable")
        self.assertEqual(chapter["images"], [])
```

- [ ] **Step 2: Run the tests and verify RED**

Run: `python -m unittest tests.test_r2_site -v`
Expected: FAIL because `r2/data/project.json` and the chapter manifest do not exist.

- [ ] **Step 3: Add the minimal manifests**

`r2/data/project.json` must identify R2, expose the tagline and Run 1 link, and list only `r2-ch001` initially. `r2/data/chapters/ch001.json` must use title `The Boy`, duration `959.808`, audio status `published`, written status `unavailable`, and an empty images list. `chapter-registry.json` tracks public/production state separately and marks audio published while written/image work remains not started.

- [ ] **Step 4: Run the tests and verify GREEN**

Run: `python -m unittest tests.test_r2_site -v`
Expected: PASS for manifest tests.

- [ ] **Step 5: Commit**

Commit message: `feat: add R2 manifest foundation`

---

### Task 2: Build the public R2 shell and lineage pages test-first

**Files:**
- Modify: `tests/test_r2_site.py`
- Create: `r2/index.html`
- Create: `r2/about/index.html`
- Create: `r2/chapters/index.html`
- Create: `r2/gallery/index.html`
- Create: `r2/chapter.html`

**Interfaces:**
- Consumes: Task 1 manifests.
- Produces: public routes `/r2/`, `/r2/about/`, `/r2/chapters/`, `/r2/gallery/`, and reusable `/r2/chapter.html?id=r2-ch001`.

- [ ] **Step 1: Add failing shell tests**

```python
    def test_homepage_explains_run_two_and_links_run_one(self):
        html = (R2 / "index.html").read_text(encoding="utf-8")
        self.assertIn("Greg has had two lives so far. So has his story.", html)
        self.assertIn("Peg-Leg Greg was written once already", html)
        self.assertIn('href="../index.html"', html)
        self.assertIn("Listen", html)
        self.assertIn("Read", html)
        self.assertIn("Look", html)

    def test_public_routes_exist(self):
        for path in ["about/index.html", "chapters/index.html", "gallery/index.html", "chapter.html"]:
            self.assertTrue((R2 / path).exists(), path)
```

- [ ] **Step 2: Run and verify RED**

Run: `python -m unittest tests.test_r2_site -v`
Expected: FAIL because public pages do not exist.

- [ ] **Step 3: Create minimal semantic HTML pages**

Each page uses the same compact top navigation: `R2`, `Listen`, `Read`, `Look`, `About`. Homepage contains hero, process explanation, current Chapter 1 card, and Run 1/Run 2 lineage block. About explains the second-run process in reader language. Chapter and gallery pages provide empty render targets for JavaScript without hard-coding chapter data.

- [ ] **Step 4: Run and verify GREEN**

Run: `python -m unittest tests.test_r2_site -v`
Expected: PASS.

- [ ] **Step 5: Commit**

Commit message: `feat: add R2 public reader shell`

---

### Task 3: Add manifest-driven rendering and graceful missing-media behavior test-first

**Files:**
- Modify: `tests/test_r2_site.py`
- Create: `r2/assets/js/site.js`
- Create: `r2/assets/js/chapter.js`

**Interfaces:**
- `site.js`: `loadProject() -> Promise<object>`, `chapterHref(id) -> string`, and page boot logic for chapter list/gallery/home metadata.
- `chapter.js`: loads the requested chapter manifest, renders native `<audio controls>`, hides image containers for an empty image list, and shows the exact fallback `Written rendition coming soon.` when written status is not `published`.

- [ ] **Step 1: Add failing behavior-contract tests**

```python
    def test_chapter_renderer_has_missing_media_fallbacks(self):
        js = (R2 / "assets/js/chapter.js").read_text(encoding="utf-8")
        self.assertIn("Written rendition coming soon.", js)
        self.assertIn("Audio version coming soon.", js)
        self.assertIn("new URLSearchParams", js)
        self.assertIn("document.createElement('audio')", js)
        self.assertIn("chapter.images", js)

    def test_site_renderer_is_manifest_driven(self):
        js = (R2 / "assets/js/site.js").read_text(encoding="utf-8")
        self.assertIn("data/project.json", js)
        self.assertIn("data/chapters/", js)
        self.assertIn("chapter.html?id=", js)
```

- [ ] **Step 2: Run and verify RED**

Run: `python -m unittest tests.test_r2_site -v`
Expected: FAIL because JavaScript files do not exist.

- [ ] **Step 3: Implement the minimal renderers**

`site.js` fetches `data/project.json`, resolves chapter manifests by stable ID, and renders chapter cards/gallery items only from manifest data. `chapter.js` reads `?id=`, fetches the chapter manifest, creates a native audio player when published, renders written Markdown as escaped paragraph blocks only when a path is published, and omits broken image frames when images are absent. Any fetch error results in a quiet visible error message rather than a blank page.

- [ ] **Step 4: Run and verify GREEN**

Run: `python -m unittest tests.test_r2_site -v`
Expected: PASS.

- [ ] **Step 5: Commit**

Commit message: `feat: render R2 chapters from manifests`

---

### Task 4: Add the visual system, young-Greg hero, and responsive reading layout test-first

**Files:**
- Modify: `tests/test_r2_site.py`
- Create: `r2/assets/css/r2.css`
- Create: `r2/assets/images/r2-harbor-hero.png`

**Interfaces:**
- CSS provides `.hero`, `.audio-panel`, `.reading-copy`, `.chapter-card`, `.lineage-grid`, `.gallery-grid`, 44px minimum interactive targets, and a mobile breakpoint at 760px.
- Hero image is presentation/mood art only and is not promoted as Greg visual canon.

- [ ] **Step 1: Add failing presentation tests**

```python
    def test_r2_css_is_responsive_and_audio_first(self):
        css = (R2 / "assets/css/r2.css").read_text(encoding="utf-8")
        self.assertIn(".audio-panel", css)
        self.assertIn(".reading-copy", css)
        self.assertIn("min-height: 44px", css)
        self.assertIn("@media (max-width: 760px)", css)
        self.assertNotIn("animation:", css)

    def test_hero_asset_is_referenced_without_becoming_chapter_canon(self):
        html = (R2 / "index.html").read_text(encoding="utf-8")
        self.assertIn("assets/images/r2-harbor-hero.png", html)
        chapter = json.loads((R2 / "data/chapters/ch001.json").read_text(encoding="utf-8"))
        self.assertEqual(chapter["images"], [])
```

- [ ] **Step 2: Run and verify RED**

Run: `python -m unittest tests.test_r2_site -v`
Expected: FAIL because CSS and hero asset/reference are absent.

- [ ] **Step 3: Add styling and the approved young-Greg site hero**

Use the generated young-Greg harbor banner from this design session as `r2/assets/images/r2-harbor-hero.png`. Add a restrained dark/warm palette, serif display typography with readable system serif body fallbacks, generous reading measure, visible native audio controls, responsive cards, and no decorative animation.

- [ ] **Step 4: Run and verify GREEN**

Run: `python -m unittest tests.test_r2_site -v`
Expected: PASS.

- [ ] **Step 5: Commit**

Commit message: `feat: style R2 audio-first reader`

---

### Task 5: Final repository validation and handoff

**Files:**
- Modify only if verification exposes a defect.

**Interfaces:**
- Consumes all previous tasks.
- Produces a branch ready for review/PR without changing Run 1.

- [ ] **Step 1: Run the focused R2 suite**

Run: `python -m unittest tests.test_r2_site -v`
Expected: all tests PASS.

- [ ] **Step 2: Run the repository test suite**

Run: `python -m unittest discover -s tests -p 'test_*.py'`
Expected: PASS, or document any pre-existing unrelated failure with evidence.

- [ ] **Step 3: Verify root reader is unchanged relative to main**

Run: `git diff main...HEAD -- index.html assets/reader.css`
Expected: no R2 implementation changes to Run 1 root reader surfaces.

- [ ] **Step 4: Verify branch diff and links**

Check that `/r2/` paths are self-contained, Chapter 1 audio path resolves to the existing asset, Run 1 link is `../index.html`, and manifests parse.

- [ ] **Step 5: Finish the development branch**

Use the finishing-development workflow after verification and open a PR rather than merging without review.
