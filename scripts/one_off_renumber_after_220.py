#!/usr/bin/env python3
from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNING = ROOT / "state/manuscript/Peg_Leg_Greg_Running_Manuscript.md"
INDEX = ROOT / "state/MANUSCRIPT_CHAPTER_INDEX.md"
ABC = {
    "220A": (221, "THE SHORTAGE", ROOT / "state/manuscript/Peg_Leg_Greg_Chapter_220A_EXACT.md"),
    "220B": (222, "THE OLD MAN", ROOT / "state/manuscript/Peg_Leg_Greg_Chapter_220B_EXACT.md"),
    "220C": (223, "THE ROUTE", ROOT / "state/manuscript/Peg_Leg_Greg_Chapter_220C_EXACT.md"),
}
RESTORE_COMMIT = "90615b90d1fbddbed632ef18dba8ade64c919af6"
TEXT_SUFFIXES = {".md", ".html", ".json", ".py", ".yml", ".yaml", ".txt", ".js", ".css"}


def run(*args: str) -> str:
    return subprocess.check_output(args, cwd=ROOT, text=True)


def restore_running_if_empty() -> None:
    if RUNNING.exists() and RUNNING.stat().st_size > 100:
        return
    content = run("git", "show", f"{RESTORE_COMMIT}:state/manuscript/Peg_Leg_Greg_Running_Manuscript.md")
    RUNNING.write_text(content, encoding="utf-8")


def shift_number(n: int) -> int:
    return n + 3 if n >= 221 else n


def rewrite_contextual_refs(text: str) -> str:
    # First convert explicit provisional labels. These are not numeric chapters yet.
    text = re.sub(r"\b(?:Chapter|CHAPTER|Ch|ch)[ ]*220A\b", lambda m: m.group(0).replace("220A", "221"), text)
    text = re.sub(r"\b(?:Chapter|CHAPTER|Ch|ch)[ ]*220B\b", lambda m: m.group(0).replace("220B", "222"), text)
    text = re.sub(r"\b(?:Chapter|CHAPTER|Ch|ch)[ ]*220C\b", lambda m: m.group(0).replace("220C", "223"), text)
    text = text.replace("220A.html", "221.html").replace("220B.html", "222.html").replace("220C.html", "223.html")
    text = text.replace("220a.html", "221.html").replace("220b.html", "222.html").replace("220c.html", "223.html")
    text = text.replace("Peg_Leg_Greg_Chapter_220A_EXACT.md", "Peg_Leg_Greg_Chapter_221_EXACT.md")
    text = text.replace("Peg_Leg_Greg_Chapter_220B_EXACT.md", "Peg_Leg_Greg_Chapter_222_EXACT.md")
    text = text.replace("Peg_Leg_Greg_Chapter_220C_EXACT.md", "Peg_Leg_Greg_Chapter_223_EXACT.md")

    def chapter_ref(m: re.Match[str]) -> str:
        prefix, spacing, raw = m.groups()
        return f"{prefix}{spacing}{shift_number(int(raw))}"

    text = re.sub(r"\b(Chapter|CHAPTER|Ch|ch)(\s*)(\d{3})\b", chapter_ref, text)

    def exact_ref(m: re.Match[str]) -> str:
        return f"Peg_Leg_Greg_Chapter_{shift_number(int(m.group(1)))}_EXACT{m.group(2)}"

    text = re.sub(r"Peg_Leg_Greg_Chapter_(\d{3})_EXACT([^\s\"'`]*)", exact_ref, text)

    def query_ref(m: re.Match[str]) -> str:
        return f"chapter={shift_number(int(m.group(1)))}"

    text = re.sub(r"chapter=(\d{3})\b", query_ref, text)

    # Explicit reader/file paths. Limit to chapter-looking path contexts so ordinary numbers in prose do not move.
    def path_ref(m: re.Match[str]) -> str:
        prefix, raw, suffix = m.groups()
        return f"{prefix}{shift_number(int(raw)):03d}{suffix}"

    text = re.sub(r"((?:chapters|light)/)(\d{3})(\.html\b)", path_ref, text)
    return text


def rewrite_text_files_once() -> None:
    skip = {p.resolve() for _, _, p in ABC.values()}
    skip.add(INDEX.resolve())
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if ".git" in path.parts or path.resolve() in skip:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        new = rewrite_contextual_refs(text)
        if new != text:
            path.write_text(new, encoding="utf-8")


def normalize_abc_source(path: Path, number: int, title: str) -> str:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n").strip()
    # Remove the provisional heading in either known form, keep body verbatim.
    text = re.sub(r"^#\s*220[A-C]\s*[—–-]\s*[^\n]+\n+", "", text, count=1)
    text = re.sub(r"^#\s*CHAPTER\s*220[A-C]\s*\n+(?:##\s*[^\n]+\n+)?", "", text, count=1, flags=re.I)
    return f"# CHAPTER {number}\n\n## {title}\n\n{text.strip()}\n"


def insert_abc_into_running() -> None:
    text = RUNNING.read_text(encoding="utf-8")
    if "# CHAPTER 221\n\n## THE SHORTAGE" in text:
        return
    marker = re.search(r"(?m)^# CHAPTER 224\s*$", text)
    if not marker:
        raise SystemExit("expected shifted Chapter 224 boundary after old Chapter 221")
    insertion = "\n\n".join(normalize_abc_source(path, number, title).strip() for _, (number, title, path) in ABC.items()) + "\n\n"
    text = text[: marker.start()].rstrip() + "\n\n" + insertion + text[marker.start():]
    RUNNING.write_text(text, encoding="utf-8")


def renumber_checkpoint_filenames() -> None:
    manuscript = ROOT / "state/manuscript"
    matches = []
    for path in manuscript.glob("Peg_Leg_Greg_Chapter_*_EXACT_WIP.md"):
        m = re.fullmatch(r"Peg_Leg_Greg_Chapter_(\d+)_EXACT_WIP\.md", path.name)
        if m and int(m.group(1)) >= 221:
            matches.append((int(m.group(1)), path))
    for old, path in sorted(matches, reverse=True):
        new = old + 3
        target = path.with_name(f"Peg_Leg_Greg_Chapter_{new}_EXACT_WIP.md")
        if target.exists():
            raise SystemExit(f"checkpoint collision: {target}")
        path.rename(target)


def remove_abc_source_files() -> None:
    for _, _, path in ABC.values():
        if path.exists():
            path.unlink()


def parse_sources() -> dict[int, tuple[str, Path]]:
    out: dict[int, tuple[str, Path]] = {}
    boundary = re.compile(r"(?m)^# CHAPTER (\d+)\s*$")

    def scan(path: Path) -> None:
        text = path.read_text(encoding="utf-8")
        matches = list(boundary.finditer(text))
        for idx, m in enumerate(matches):
            n = int(m.group(1))
            end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
            chunk = text[m.end():end]
            tm = re.search(r"(?m)^##\s+(.+?)\s*$", chunk)
            if tm:
                out[n] = (tm.group(1).strip(), path)

    scan(ROOT / "state/manuscript/Peg_Leg_Greg_Recovered_Ch156-219_EXACT.md")
    scan(RUNNING)
    for path in sorted((ROOT / "state/manuscript").glob("Peg_Leg_Greg_Chapter_*_EXACT_WIP.md")):
        scan(path)
    return out


def rebuild_index(sources: dict[int, tuple[str, Path]]) -> None:
    old = INDEX.read_text(encoding="utf-8")
    old_titles: dict[int, str] = {}
    for m in re.finditer(r"(?m)^(\d+)\. \*\*(.+?)\*\*\s*$", old):
        n = int(m.group(1))
        if n <= 220:
            old_titles[n] = m.group(2)
    titles = dict(old_titles)
    titles.update({n: title for n, (title, _) in sources.items() if n >= 221})
    latest = max(titles)
    lines = [f"# PEG-LEG GREG — CHAPTER INDEX — CH{latest}", "", f"**Current endpoint:** Chapter {latest} — {titles[latest]}", ""]
    for n in range(1, latest + 1):
        if n not in titles:
            raise SystemExit(f"index missing chapter {n}")
        lines.append(f"{n}. **{titles[n]}**")
    INDEX.write_text("\n".join(lines) + "\n", encoding="utf-8")


def cleanup_preview_pages() -> None:
    chapter_dir = ROOT / "chapters"
    for path in chapter_dir.glob("*.html"):
        stem = path.stem
        if stem.lower() in {"220a", "220b", "220c"}:
            path.unlink()
            continue
        if stem.isdigit() and int(stem) >= 220:
            path.unlink()


def preview_html(n: int, title: str, source: Path, latest: int) -> str:
    rel_source = "../" + source.relative_to(ROOT).as_posix()
    prev_link = f'<a href="{n-1}.html">← Chapter {n-1}</a>' if n > 220 else '<a href="219.html">← Chapter 219</a>'
    next_link = f'<a href="{n+1}.html">Chapter {n+1} →</a>' if n < latest else '<a href="../latest.html">Latest preview index</a>'
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width,initial-scale=1" name="viewport"/>
<title>Chapter {n} — Peg-Leg Greg</title>
<link href="../assets/reader.css" rel="stylesheet"/>
</head>
<body>
<header class="site-head"><a href="../index.html">PEG-LEG GREG</a><nav aria-label="Reader navigation" class="site-nav"><a href="../light.html?chapter={n}">LIGHT</a><a href="../latest.html">LATEST</a><a href="../art.html">ART</a></nav></header>
<main class="chapter-shell">
<header class="chapter-title"><div class="number">CHAPTER {n}</div><h1 data-chapter-title>{title}</h1></header>
<p><strong>Latest manuscript preview.</strong> This page renders Chapter {n} directly from the permanent GitHub manuscript authority.</p>
<article class="prose" data-manuscript-chapter="{n}" data-manuscript-source="{rel_source}"><p>Loading Chapter {n}…</p></article>
<p data-preview-status aria-live="polite"></p>
<nav aria-label="Preview chapter navigation">{prev_link} · <a href="../light.html?chapter={n}">Read in Light Reader</a> · {next_link}</nav>
</main>
<script src="../assets/manuscript-preview.js"></script>
</body>
</html>
'''


def rebuild_preview_pages(sources: dict[int, tuple[str, Path]]) -> None:
    current = {n: v for n, v in sources.items() if n >= 220}
    if not current:
        raise SystemExit("no current chapters found")
    latest = max(current)
    cleanup_preview_pages()
    for n in range(220, latest + 1):
        if n not in current:
            raise SystemExit(f"missing preview source for chapter {n}")
        title, source = current[n]
        (ROOT / "chapters" / f"{n}.html").write_text(preview_html(n, title, source, latest), encoding="utf-8")


def update_book_role_card() -> None:
    old = ROOT / "assets/book-role-cards/book-iii-magistrate-231.webp"
    new = ROOT / "assets/book-role-cards/book-iii-magistrate-234.webp"
    if old.exists() and not new.exists():
        old.rename(new)
    path = ROOT / "scripts/reader_sections.py"
    text = path.read_text(encoding="utf-8")
    text = text.replace("book-iii-magistrate-231.webp", "book-iii-magistrate-234.webp")
    text = text.replace("The Magistrate, Chapter 231:", "The Magistrate, Chapter 234:")
    text = text.replace("light/231.html", "light/234.html")
    path.write_text(text, encoding="utf-8")


def verify_sources(sources: dict[int, tuple[str, Path]]) -> None:
    expected = {
        220: "THE LANDLORD",
        221: "THE SHORTAGE",
        222: "THE OLD MAN",
        223: "THE ROUTE",
        224: "THE PARTICIPANT",
    }
    for n, title in expected.items():
        got = sources.get(n, (None, None))[0]
        if got != title:
            raise SystemExit(f"chapter {n}: expected {title}, got {got}")
    if max(sources) != 304:
        raise SystemExit(f"expected latest 304, got {max(sources)}")
    running = RUNNING.read_text(encoding="utf-8")
    if "# CHAPTER 220A" in running or "# 220A" in running:
        raise SystemExit("provisional 220A label remains in running manuscript")
    for old in ("220A", "220B", "220C"):
        if (ROOT / f"chapters/{old.lower()}.html").exists():
            raise SystemExit(f"provisional reader page remains: {old}")


def main() -> int:
    restore_running_if_empty()
    rewrite_text_files_once()
    insert_abc_into_running()
    renumber_checkpoint_filenames()
    remove_abc_source_files()
    update_book_role_card()
    sources = parse_sources()
    rebuild_index(sources)
    rebuild_preview_pages(sources)
    verify_sources(sources)
    print(f"renumbered canonical sequence through Chapter {max(sources)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
