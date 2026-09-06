from __future__ import annotations

import hashlib
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.report_illustration_coverage import _normalize_live_src

CHAPTER_DIR = ROOT / "chapters"
REGISTRY_PATH = ROOT / "state" / "visual" / "ILLUSTRATION_REGISTRY.json"

FIGURE_RE = re.compile(
    r'<figure\b[^>]*class=["\'][^"\']*\bchapter-art\b[^"\']*["\'][^>]*>(.*?)</figure>',
    re.I | re.S,
)
IMG_RE = re.compile(r'<img\b([^>]*)>', re.I | re.S)
ATTR_RE = re.compile(r'\b(?P<name>src|alt)=["\'](?P<value>.*?)["\']', re.I | re.S)
CAPTION_RE = re.compile(r'<figcaption\b[^>]*>(.*?)</figcaption>', re.I | re.S)
TAG_RE = re.compile(r'<[^>]+>')


def _plain_text(value: str) -> str:
    return html.unescape(TAG_RE.sub("", value)).strip()


def _legacy_id(chapter: int, live_asset: str) -> str:
    digest = hashlib.sha1(live_asset.encode("utf-8")).hexdigest()[:10]
    return f"legacy-ch{chapter:03d}-{digest}"


def discover_legacy_records(root: Path, chapter_dir: Path) -> list[dict]:
    records: list[dict] = []
    seen_assets: set[str] = set()
    for chapter_path in sorted(chapter_dir.glob("[0-9][0-9][0-9].html")):
        chapter = int(chapter_path.stem)
        text = chapter_path.read_text(encoding="utf-8")
        for figure in FIGURE_RE.findall(text):
            img_match = IMG_RE.search(figure)
            if not img_match:
                continue
            attrs = {match.group("name").lower(): match.group("value") for match in ATTR_RE.finditer(img_match.group(1))}
            src = attrs.get("src", "")
            live_asset = _normalize_live_src(src)
            if not live_asset or live_asset in seen_assets:
                continue
            seen_assets.add(live_asset)
            caption_match = CAPTION_RE.search(figure)
            caption = _plain_text(caption_match.group(1)) if caption_match else ""
            alt_text = html.unescape(attrs.get("alt", "")).strip() or caption or f"Legacy illustration for Chapter {chapter}."
            art_id = _legacy_id(chapter, live_asset)
            records.append(
                {
                    "id": art_id,
                    "candidate_id": f"legacy-import-{art_id}",
                    "chapter": chapter,
                    "kind": "chapter_illustration",
                    "status": "live",
                    "style_family": "legacy-import",
                    "source_asset": live_asset,
                    "live_asset": live_asset,
                    "caption": caption,
                    "alt_text": alt_text,
                    "approved_fit": "close_enough",
                    "prompt_pack": "legacy/imported",
                    "notes": "Imported from pre-registry live reader markup. Existing placement remains generator-managed.",
                }
            )
    return sorted(records, key=lambda record: (record["chapter"], record["live_asset"], record["id"]))


def bootstrap_legacy_registry(root: Path, chapter_dir: Path, registry: list[dict]) -> list[dict]:
    if registry:
        return registry
    return discover_legacy_records(root, chapter_dir)


def main() -> None:
    existing = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    if existing:
        print(f"legacy illustration bootstrap already complete: {len(existing)} registry records")
        return
    records = bootstrap_legacy_registry(ROOT, CHAPTER_DIR, existing)
    REGISTRY_PATH.write_text(json.dumps(records, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"bootstrapped {len(records)} legacy live illustrations into registry")


if __name__ == "__main__":
    main()
