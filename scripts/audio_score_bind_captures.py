#!/usr/bin/env python3
"""Bind durable voice preview results onto a deterministic Audio Score capture plan."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("chapter")
    args = ap.parse_args()
    chapter = f"{int(args.chapter):03d}"
    plan_path = Path(f"greg-again/audio/v2/takes/{chapter}/short-takes.json")
    results_path = Path(f"greg-again/audio/v2/takes/{chapter}/capture-results.tsv")
    data = json.loads(plan_path.read_text())
    if data.get("status") == "durable_takes_verified_and_assembled":
        print(f"{chapter}: already assembled; capture binder is a no-op")
        return
    rows = []
    with results_path.open(newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            rows.append(row)
    by_order = {}
    for row in rows:
        order = int(row["order"])
        if order in by_order:
            raise SystemExit(f"duplicate capture result for take {order}")
        if not row["context_id"].strip():
            raise SystemExit(f"missing context_id for take {order}")
        url = row["preview_url"].strip()
        if not url.startswith("https://storage.googleapis.com/"):
            raise SystemExit(f"invalid preview_url for take {order}: {url}")
        by_order[order] = {"context_id": row["context_id"].strip(), "preview_url": url}

    expected = data["take_count"]
    if any(order < 1 or order > expected for order in by_order):
        raise SystemExit("capture result order outside planned take range")
    for take in data["takes"]:
        result = by_order.get(take["order"])
        if result:
            take.update(result)

    bound = sum(1 for t in data["takes"] if t.get("context_id") and t.get("preview_url"))
    data["captured_take_count"] = bound
    data["status"] = "capture_ready" if bound == expected else "capture_partial"
    plan_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"{chapter}: bound {bound}/{expected} durable previews; status={data['status']}")


if __name__ == "__main__":
    main()
