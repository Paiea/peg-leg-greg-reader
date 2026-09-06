from __future__ import annotations

import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.generate_light import load_all_sources
from scripts.illustration_state import load_registry, validate_registry

REGISTRY_PATH = ROOT / "state" / "visual" / "ILLUSTRATION_REGISTRY.json"


def figure_markup(record: dict) -> str:
    live_asset = record.get("live_asset") or record.get("source_asset")
    if not isinstance(live_asset, str) or not live_asset.strip():
        raise ValueError(f"illustration {record.get('id', '<unknown>')} requires live_asset")
    alt_text = record.get("alt_text")
    if not isinstance(alt_text, str) or not alt_text.strip():
        raise ValueError(f"illustration {record.get('id', '<unknown>')} requires alt_text")
    caption = record.get("caption", "")
    if not isinstance(caption, str):
        raise ValueError(f"illustration {record.get('id', '<unknown>')} caption must be text")
    src = "../" + live_asset.lstrip("./")
    parts = [
        '<figure class="chapter-art scene-illustration">',
        f'<img src="{html.escape(src, quote=True)}" alt="{html.escape(alt_text.strip(), quote=True)}" loading="lazy"/>',
    ]
    if caption.strip():
        parts.append(f"<figcaption>{html.escape(caption.strip())}</figcaption>")
    parts.append("</figure>")
    return "".join(parts)


def promote_html(source: str, record: dict) -> str:
    if record.get("status") != "approved":
        raise ValueError(f"illustration {record.get('id', '<unknown>')} must be approved before promotion")
    anchor = record.get("paragraph_anchor")
    if not isinstance(anchor, str) or not anchor.strip():
        raise ValueError(f"illustration {record.get('id', '<unknown>')} requires paragraph_anchor")
    target = f"<p>{html.escape(anchor.strip(), quote=False)}</p>"
    count = source.count(target)
    if count != 1:
        raise ValueError(
            f"illustration {record.get('id', '<unknown>')} paragraph anchor must occur exactly once; found {count}: {anchor!r}"
        )
    return source.replace(target, target + "\n" + figure_markup(record), 1)


def promote_approved_records(root: Path, registry: list[dict]) -> tuple[list[dict], int]:
    chapters = load_all_sources()
    updated: list[dict] = []
    promoted = 0
    for original in registry:
        record = dict(original)
        if record.get("status") != "approved":
            updated.append(record)
            continue
        if record.get("kind") != "chapter_illustration":
            raise ValueError(f"automated promotion currently supports chapter_illustration only: {record.get('id')}")
        live_asset = record.get("live_asset") or record.get("source_asset")
        if not isinstance(live_asset, str) or not live_asset.strip() or not (root / live_asset).is_file():
            raise ValueError(f"illustration {record.get('id')} approved asset does not exist: {live_asset}")
        chapter_number = record.get("chapter")
        chapter = chapters.get(chapter_number)
        if chapter is None:
            raise ValueError(f"illustration {record.get('id')} chapter does not exist: {chapter_number}")
        record["live_asset"] = live_asset
        probe = dict(record)
        probe["status"] = "approved"
        promote_html(chapter.prose_html, probe)
        record["status"] = "live"
        updated.append(record)
        promoted += 1
    validate_registry(updated, root=root)
    return updated, promoted


def main() -> None:
    registry = load_registry(REGISTRY_PATH)
    updated, promoted = promote_approved_records(ROOT, registry)
    if not promoted:
        print("no approved chapter illustrations awaiting promotion")
        return
    REGISTRY_PATH.write_text(json.dumps(updated, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"promoted {promoted} approved chapter illustrations to live registry state")


if __name__ == "__main__":
    main()
