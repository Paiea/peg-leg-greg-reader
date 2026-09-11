import json
import pathlib
import subprocess

ROOT = pathlib.Path.cwd()
SOURCE_BRANCH = "origin/audio/v2-greg-again-ch008-integrate"
AUTHORITY_BRANCH = "origin/audio-score/chapters-001-010"


def git_show(ref, path):
    result = subprocess.run(
        ["git", "show", f"{ref}:{path}"],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout

# Confirm the Audio Score source has not changed under the moving authority.
score_sha = subprocess.run(
    ["git", "rev-parse", f"{AUTHORITY_BRANCH}:r2/assets/audio-score/ch008.md"],
    check=True,
    capture_output=True,
    text=True,
).stdout.strip()
if score_sha != "70fb72370291aa2a47b76d383cae9434254305e8":
    raise SystemExit(f"Chapter 008 Audio Score changed: {score_sha}")

# Reconcile Chapter 008 into the newest v2 registry without replacing siblings.
v2_path = ROOT / "greg-again/audio/v2/manifest.json"
v2 = json.loads(v2_path.read_text())
source_v2 = json.loads(git_show(SOURCE_BRANCH, "greg-again/audio/v2/manifest.json"))
source_entry = next((c for c in source_v2.get("chapters", []) if c.get("number") == 8), None)
if source_entry is None:
    raise SystemExit("Source integration branch lacks Chapter 008 v2 entry")
v2["chapters"] = [c for c in v2.get("chapters", []) if c.get("number") != 8]
v2["chapters"].append(source_entry)
v2["chapters"].sort(key=lambda c: c.get("number", 0))
v2_path.write_text(json.dumps(v2, indent=2) + "\n")

# Reconcile only the Chapter 008 public route/production metadata.
public_path = ROOT / "greg-again/audio/manifest.json"
public = json.loads(public_path.read_text())
source_public = json.loads(git_show(SOURCE_BRANCH, "greg-again/audio/manifest.json"))
source_public_8 = next((c for c in source_public.get("chapters", []) if c.get("number") == 8), None)
public_8 = next((c for c in public.get("chapters", []) if c.get("number") == 8), None)
if source_public_8 is None or public_8 is None:
    raise SystemExit("Chapter 008 public manifest entry missing")
for key in ("take_count", "duration_seconds", "audio_src", "note"):
    public_8[key] = source_public_8[key]
public_path.write_text(json.dumps(public, indent=2) + "\n")

# Assertions for the exact intended route and objective production state.
if public_8["audio_src"] != "assets/v2/chapter-008.mp3":
    raise SystemExit("Chapter 008 public route is not v2")
if public_8["take_count"] != 20:
    raise SystemExit("Chapter 008 take count is not 20")
if float(public_8["duration_seconds"]) != 535.8:
    raise SystemExit("Chapter 008 duration is not 535.8")
asset = ROOT / "greg-again/audio/assets/v2/chapter-008.mp3"
if not asset.exists() or asset.stat().st_size <= 1_000_000:
    raise SystemExit("Chapter 008 v2 asset missing or implausibly small")
verification = json.loads((ROOT / "greg-again/audio/v2/verification/008/source-publication-verification.json").read_text())
if verification.get("source_blob_sha") != score_sha:
    raise SystemExit("Verification source SHA mismatch")
if not verification.get("source_body_reconstructed_exactly_once"):
    raise SystemExit("Exact source coverage verification missing")
if not verification.get("all_chunks_ffprobe_valid"):
    raise SystemExit("Chunk ffprobe verification missing")
if verification.get("human_listen_back_performed") is not False:
    raise SystemExit("Human listen-back boundary changed unexpectedly")
