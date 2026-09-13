#!/usr/bin/env python3
"""Download, decode, hash, and receipt reconciled 3L Instant worker captures."""

from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIO = ROOT / "3l" / "audio"
VERIFICATION = AUDIO / "verification"
MASTER = AUDIO / "records-002-010-five-worker-work-order.json"


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def verify() -> dict[str, bool]:
    master = json.loads(MASTER.read_text(encoding="utf-8"))
    VERIFICATION.mkdir(parents=True, exist_ok=True)
    status: dict[str, bool] = {}
    with tempfile.TemporaryDirectory(prefix="3l-worker-verify-") as temp_name:
        temp = Path(temp_name)
        for record in master["records"]:
            plan_path = AUDIO / f"record-{record}-short-dual-plan.json"
            capture_path = AUDIO / f"record-{record}-short-captures-workers.json"
            if not capture_path.exists():
                status[record] = False
                continue
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            manifest = json.loads(capture_path.read_text(encoding="utf-8"))
            if manifest.get("record") != record:
                raise ValueError(f"{capture_path}: record mismatch")
            if manifest.get("plan") != str(plan_path.relative_to(ROOT)):
                raise ValueError(f"{capture_path}: plan mismatch")

            chunks = {int(chunk["index"]): chunk for chunk in plan["chunks"]}
            expected = {
                (int(chunk["index"]), voice)
                for chunk in plan["chunks"]
                for voice in chunk["required_voices"]
            }
            seen = set()
            verified = []
            for item in manifest.get("captures", []):
                chunk_index = int(item["chunk"])
                voice = str(item["voice"])
                key = (chunk_index, voice)
                if key in seen:
                    raise ValueError(f"{record}: duplicate capture {key}")
                seen.add(key)
                chunk = chunks.get(chunk_index)
                if not chunk:
                    raise ValueError(f"{record}: unknown chunk {chunk_index}")
                if voice not in chunk["required_voices"]:
                    raise ValueError(f"{record}: voice {voice} not required for chunk {chunk_index}")
                if item.get("transcript") != chunk["transcript"]:
                    raise ValueError(f"{record}: transcript mismatch for {key}")
                if item.get("status") != "ready":
                    raise ValueError(f"{record}: capture not ready for {key}")
                if not item.get("preview_url"):
                    raise ValueError(f"{record}: capture has no preview URL for {key}")

                out = temp / f"record-{record}-chunk-{chunk_index:03d}-{voice}.mp3"
                run(["curl", "-L", "--fail", "--retry", "3", "--retry-delay", "1", "-o", str(out), item["preview_url"]])
                run(["ffmpeg", "-v", "error", "-i", str(out), "-f", "null", "-"])
                duration = float(
                    subprocess.check_output(
                        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(out)],
                        text=True,
                    ).strip()
                )
                if duration <= 0.5:
                    raise ValueError(f"{record}: suspicious duration {duration} for {key}")
                data = out.read_bytes()
                verified.append(
                    {
                        "chunk": chunk_index,
                        "voice": voice,
                        "context_id": item["context_id"],
                        "preview_url": item["preview_url"],
                        "duration_seconds": round(duration, 6),
                        "byte_size": len(data),
                        "sha256": hashlib.sha256(data).hexdigest(),
                        "status": "verified",
                        "manifest": str(capture_path.relative_to(ROOT)),
                    }
                )

            extra = seen - expected
            if extra:
                raise ValueError(f"{record}: unexpected captures {sorted(extra)}")
            missing = sorted(expected - seen)
            verified.sort(key=lambda item: (item["chunk"], item["voice"]))
            receipt = {
                "record": record,
                "authority": manifest["authority"],
                "plan": manifest["plan"],
                "capture_manifests": [str(capture_path.relative_to(ROOT))],
                "verified_capture_count": len(verified),
                "planned_capture_count": len(expected),
                "complete": not missing,
                "missing": [{"chunk": chunk, "voice": voice} for chunk, voice in missing],
                "captures": verified,
            }
            (VERIFICATION / f"record-{record}-short-captures.json").write_text(
                json.dumps(receipt, indent=2) + "\n", encoding="utf-8"
            )
            status[record] = not missing
            print(record, f"verified={len(verified)}/{len(expected)} complete={not missing}")
    return status


if __name__ == "__main__":
    verify()
