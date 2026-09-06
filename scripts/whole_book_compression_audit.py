#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import math
import re
from collections import Counter
from pathlib import Path

AUDIT_VERSION = 1

TAG_RE = re.compile(r"<[^>]+>")
SCRIPT_STYLE_RE = re.compile(r"<(script|style)\b.*?</\1>", re.I | re.S)
WORD_RE = re.compile(r"[A-Za-z][A-Za-z'-]{2,}")
TITLE_RE = re.compile(r"<h2[^>]*>(.*?)</h2>", re.I | re.S)
STOP = {
    "the","and","that","this","with","from","into","was","were","had","have","has","for","but","not","you","his","her","she","him","they","them","their","our","out","about","there","then","when","what","which","would","could","should","been","being","because","just","very","more","some","than","too","one","two","said","greg","chapter"
}


def extract_visible_text(raw: str) -> str:
    raw = SCRIPT_STYLE_RE.sub(" ", raw)
    raw = TAG_RE.sub(" ", raw)
    raw = html.unescape(raw)
    return re.sub(r"\s+", " ", raw).strip()


def extract_title(raw: str, fallback: str) -> str:
    match = TITLE_RE.search(raw)
    if not match:
        return fallback
    return extract_visible_text(match.group(1)).strip() or fallback


def terms(text: str) -> list[str]:
    return [w.lower() for w in WORD_RE.findall(text) if w.lower() not in STOP]


def vector(text: str) -> Counter[str]:
    return Counter(terms(text))


def cosine(a: Counter[str], b: Counter[str]) -> float:
    if not a or not b:
        return 0.0
    dot = sum(v * b.get(k, 0) for k, v in a.items())
    if dot == 0:
        return 0.0
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    return dot / (na * nb)


def jaccard_top(a: Counter[str], b: Counter[str], n: int = 30) -> float:
    sa = {k for k, _ in a.most_common(n)}
    sb = {k for k, _ in b.most_common(n)}
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def sentence_edges(text: str, words: int = 40) -> tuple[str, str]:
    toks = text.split()
    return (" ".join(toks[:words]), " ".join(toks[-words:]))


def phrase_similarity(a: str, b: str) -> float:
    va, vb = vector(a), vector(b)
    return cosine(va, vb)


def load_chapters(root: Path) -> list[dict]:
    rows = []
    for path in sorted((root / "chapters").glob("*.html")):
        if not path.stem.isdigit():
            continue
        n = int(path.stem)
        raw = path.read_text(encoding="utf-8", errors="replace")
        text = extract_visible_text(raw)
        title = extract_title(raw, f"Chapter {n}")
        vec = vector(text)
        opening, closing = sentence_edges(text)
        rows.append({
            "chapter": n,
            "chapter_id": f"plg-ch-{n:06d}",
            "title": title,
            "path": path.as_posix(),
            "text": text,
            "vector": vec,
            "word_count": len(text.split()),
            "opening": opening,
            "closing": closing,
        })
    return rows


def candidate_action(score: float, length_ratio: float) -> str:
    if score >= 0.82:
        return "MERGE_OR_SUMMARIZE_REVIEW"
    if score >= 0.70:
        return "TIGHTEN_OR_MERGE_REVIEW"
    if score >= 0.58 and length_ratio > 1.15:
        return "TIGHTEN_REVIEW"
    return "REVIEW"


def audit_chapters(root: Path) -> dict:
    chapters = load_chapters(root)
    metrics = [
        {
            "chapter": row["chapter"],
            "chapter_id": row["chapter_id"],
            "title": row["title"],
            "word_count": row["word_count"],
        }
        for row in chapters
    ]
    if not chapters:
        return {"schema_version": 1, "audit_version": AUDIT_VERSION, "chapter_count": 0, "chapter_metrics": [], "ranked_candidates": [], "repeated_titles": []}

    median_wc = sorted(row["word_count"] for row in chapters)[len(chapters)//2] or 1
    pair_candidates = []
    for left, right in zip(chapters, chapters[1:]):
        if right["chapter"] != left["chapter"] + 1:
            continue
        lexical = cosine(left["vector"], right["vector"])
        top_overlap = jaccard_top(left["vector"], right["vector"])
        edge_repeat = max(
            phrase_similarity(left["closing"], right["opening"]),
            phrase_similarity(left["opening"], right["opening"]),
            phrase_similarity(left["closing"], right["closing"]),
        )
        title_same = 1.0 if left["title"].strip().lower() == right["title"].strip().lower() else 0.0
        score = 0.58 * lexical + 0.24 * top_overlap + 0.13 * edge_repeat + 0.05 * title_same
        length_ratio = ((left["word_count"] + right["word_count"]) / 2) / median_wc
        if score >= 0.56:
            pair_candidates.append({
                "start_chapter": left["chapter"],
                "end_chapter": right["chapter"],
                "chapter_ids": [left["chapter_id"], right["chapter_id"]],
                "titles": [left["title"], right["title"]],
                "score": round(score, 4),
                "lexical_similarity": round(lexical, 4),
                "top_term_overlap": round(top_overlap, 4),
                "edge_similarity": round(edge_repeat, 4),
                "mean_length_vs_median": round(length_ratio, 3),
                "suggested_action": candidate_action(score, length_ratio),
                "reason": "Adjacent chapters share unusually similar vocabulary/scene-language. Human review must determine whether they repeat dramatic function or merely share setting/arc texture.",
            })

    pair_candidates.sort(key=lambda x: x["start_chapter"])
    clusters = []
    current = None
    for pair in pair_candidates:
        if current and pair["start_chapter"] == current["end_chapter"]:
            current["end_chapter"] = pair["end_chapter"]
            current["chapter_ids"].append(pair["chapter_ids"][-1])
            current["titles"].append(pair["titles"][-1])
            current["pair_scores"].append(pair["score"])
            current["score"] = round(sum(current["pair_scores"]) / len(current["pair_scores"]), 4)
            current["suggested_action"] = candidate_action(current["score"], current["mean_length_vs_median"])
        else:
            if current:
                clusters.append(current)
            current = {
                "start_chapter": pair["start_chapter"],
                "end_chapter": pair["end_chapter"],
                "chapter_ids": list(pair["chapter_ids"]),
                "titles": list(pair["titles"]),
                "pair_scores": [pair["score"]],
                "score": pair["score"],
                "mean_length_vs_median": pair["mean_length_vs_median"],
                "suggested_action": pair["suggested_action"],
                "reason": pair["reason"],
            }
    if current:
        clusters.append(current)

    title_groups: dict[str, list[int]] = {}
    for row in chapters:
        key = row["title"].strip().lower()
        title_groups.setdefault(key, []).append(row["chapter"])
    repeated_titles = [
        {"title": title, "chapters": nums}
        for title, nums in title_groups.items() if len(nums) >= 3
    ]
    repeated_titles.sort(key=lambda x: (-len(x["chapters"]), x["title"]))

    ranked = sorted(clusters, key=lambda x: (-x["score"], -(x["end_chapter"]-x["start_chapter"]), x["start_chapter"]))
    for rank, row in enumerate(ranked, 1):
        row["rank"] = rank
        row["confidence"] = "HIGH" if row["score"] >= 0.78 else "MEDIUM" if row["score"] >= 0.66 else "LOW"
        row.pop("pair_scores", None)

    return {
        "schema_version": 1,
        "audit_version": AUDIT_VERSION,
        "chapter_count": len(chapters),
        "median_word_count": median_wc,
        "chapter_metrics": metrics,
        "ranked_candidates": ranked,
        "repeated_titles": repeated_titles,
        "method_note": "Automated ranking detects textual/scene-language repetition only. It is a triage layer for human structural review, not authority to cut, merge, or renumber.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--output", default="publishing/whole_book_compression_audit.json")
    args = parser.parse_args()
    root = Path(args.root)
    report = audit_chapters(root)
    out = root / args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {len(report['ranked_candidates'])} compression candidates across {report['chapter_count']} chapters to {out}")


if __name__ == "__main__":
    main()
