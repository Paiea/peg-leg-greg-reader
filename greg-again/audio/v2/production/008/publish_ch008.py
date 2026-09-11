import json
import pathlib
import subprocess

ROOT = pathlib.Path.cwd()
BASE_REF = "origin/audio-score/chapters-001-010"
SCORE = ROOT / "r2/assets/audio-score/ch008.md"
CAPTURE = ROOT / "greg-again/audio/v2/takes/008/preview-capture.json"
ASSEMBLY = ROOT / "greg-again/audio/v2/verification/008/assembly.json"
ASSET = ROOT / "greg-again/audio/assets/v2/chapter-008.mp3"
VERIFY_DIR = ROOT / "greg-again/audio/v2/verification/008"
STATUS = ROOT / "greg-again/audio/v2/production/008/STATUS.md"
V2_MANIFEST = ROOT / "greg-again/audio/v2/manifest.json"
PUBLIC_MANIFEST = ROOT / "greg-again/audio/manifest.json"
SOURCE_SHA = "70fb72370291aa2a47b76d383cae9434254305e8"


def run(*args, capture=False):
    return subprocess.run(args, check=True, text=True, capture_output=capture)


def git_show(path):
    cp = run("git", "show", f"{BASE_REF}:{path}", capture=True)
    return cp.stdout


def split_score_body(text, limit=480):
    marker = "\n---\n\n"
    if marker not in text:
        raise SystemExit("Audio Score body marker missing")
    body = text.split(marker, 1)[1].strip("\n")
    paragraphs = body.split("\n\n")
    chunks = []
    current = []
    current_len = 0
    for paragraph in paragraphs:
        add_len = len(paragraph) + (2 if current else 0)
        if current and current_len + add_len > limit:
            chunks.append("\n\n".join(current))
            current = [paragraph]
            current_len = len(paragraph)
        else:
            current.append(paragraph)
            current_len += add_len
    if current:
        chunks.append("\n\n".join(current))
    if "\n\n".join(chunks) != body:
        raise SystemExit("Chunk coverage does not reconstruct Audio Score body exactly")
    return body, chunks


run("git", "fetch", "origin", "audio-score/chapters-001-010")

body, chunks = split_score_body(SCORE.read_text())
capture = json.loads(CAPTURE.read_text())
assembly = json.loads(ASSEMBLY.read_text())

if len(chunks) != 20 or capture.get("chunk_count") != 20 or len(capture.get("chunks", [])) != 20:
    raise SystemExit("Expected exactly 20 chunks")

urls = []
alias_chunks = []
for index, (source_chunk, item) in enumerate(zip(chunks, capture["chunks"]), 1):
    if item.get("chunk") != index:
        raise SystemExit(f"Chunk order mismatch at {index}")
    provider = source_chunk.replace("Mana", "Ma-na").replace("mana", "ma-na")
    if len(provider) > 500:
        raise SystemExit(f"Chunk {index:02d} exceeds preview-safe limit")
    if item.get("char_count") != len(provider):
        raise SystemExit(f"Chunk {index:02d} char count mismatch")
    url = item.get("preview_url", "")
    if not url.startswith("https://storage.googleapis.com/"):
        raise SystemExit(f"Chunk {index:02d} lacks Google Storage preview URL")
    urls.append(url)
    if provider != source_chunk:
        alias_chunks.append(index)

if len(set(urls)) != 20:
    raise SystemExit("Preview URLs are not unique")
if alias_chunks != [10, 17]:
    raise SystemExit(f"Unexpected provider alias chunks: {alias_chunks}")
if not assembly.get("all_chunks_ffprobe_valid"):
    raise SystemExit("Chunk ffprobe verification is not green")
if assembly.get("assembly_order") != list(range(1, 21)):
    raise SystemExit("Assembly order is not 01-20")
if float(assembly.get("settling_tail_seconds_target", 0)) != 2.0:
    raise SystemExit("Settling tail target mismatch")
if not ASSET.exists() or ASSET.stat().st_size <= 0:
    raise SystemExit("Final v2 asset missing")

verification = {
    "chapter": 8,
    "source": "r2/assets/audio-score/ch008.md",
    "source_blob_sha": SOURCE_SHA,
    "chunk_count": 20,
    "source_body_reconstructed_exactly_once": True,
    "all_provider_chunks_preview_safe": True,
    "all_preview_urls_google_storage": True,
    "unique_preview_urls": True,
    "provider_alias_chunks": [10, 17],
    "provider_aliases": ["Mana -> Ma-na", "mana -> ma-na"],
    "all_chunks_ffprobe_valid": True,
    "assembly_order_verified": True,
    "final_asset_exists": True,
    "final_duration_seconds": float(assembly["final_duration_seconds"]),
    "settling_tail_seconds_target": 2.0,
    "human_listen_back_performed": False,
    "subjective_audio_quality_claimed": False,
    "status": "objectively_verified_unlistened",
}
VERIFY_DIR.mkdir(parents=True, exist_ok=True)
(VERIFY_DIR / "source-publication-verification.json").write_text(json.dumps(verification, indent=2) + "\n")

v2 = json.loads(git_show("greg-again/audio/v2/manifest.json"))
public = json.loads(git_show("greg-again/audio/manifest.json"))

entry = {
    "chapter_id": "ga-008",
    "number": 8,
    "title": "Road Work",
    "status": "verified",
    "source": "r2/assets/audio-score/ch008.md",
    "source_blob_sha": SOURCE_SHA,
    "voice": "deep",
    "capture_factory": "preview-safe-identical-transcript",
    "take_count": 20,
    "duration_seconds": float(assembly["final_duration_seconds"]),
    "audio_src": "assets/v2/chapter-008.mp3",
    "listener_qa": "not_performed",
    "verification": "greg-again/audio/v2/verification/008/",
}
chapters = [chapter for chapter in v2.get("chapters", []) if chapter.get("number") != 8]
chapters.append(entry)
chapters.sort(key=lambda chapter: chapter.get("number", 0))
v2["chapters"] = chapters

public_chapter = None
for chapter in public.get("chapters", []):
    if chapter.get("chapter_id") == "ga-008" or chapter.get("number") == 8:
        public_chapter = chapter
        break
if public_chapter is None:
    raise SystemExit("Stable public Chapter 008 entry missing")

public_chapter["take_count"] = 20
public_chapter["duration_seconds"] = float(assembly["final_duration_seconds"])
public_chapter["audio_src"] = "assets/v2/chapter-008.mp3"
public_chapter["note"] = (
    "Audio Score v2 Chapter 8: twenty preview-safe deep-voice chunks captured from the Audio Score, "
    "objectively verified for exact ordered source coverage, durable Google Storage artifact capture, "
    "ffprobe playability, ordered assembly, and a two-second settling tail. Subjective human listen-back "
    "remains separate QA."
)

V2_MANIFEST.write_text(json.dumps(v2, indent=2) + "\n")
PUBLIC_MANIFEST.write_text(json.dumps(public, indent=2) + "\n")

STATUS.write_text(f"""# Audio Score v2 — Chapter 008 Production Status

Chapter: 008 — Road Work
Claim branch: `audio/v2-greg-again-ch008-auto`
Source: `r2/assets/audio-score/ch008.md`
Audio Score blob SHA: `{SOURCE_SHA}`
Voice: `deep`

## Current state

- 20 preview-safe chunks captured with identical `transcript` + `preview_transcript`
- all 20 returned durable Google Storage preview MP3 URLs
- all 20 downloaded and passed `ffprobe`
- exact Audio Score body reconstructs from the 20 source chunks once and in order
- provider-facing pronunciation aliases only on chunks 10 and 17 (`mana` -> `ma-na`)
- final listener-facing asset exists at `greg-again/audio/assets/v2/chapter-008.mp3`
- final duration: {float(assembly['final_duration_seconds']):.3f} seconds
- approximately 2 seconds of settling tail appended at assembly
- v2 manifest reconciled from newest Audio Score authority
- public manifest Chapter 008 switched to `assets/v2/chapter-008.mp3`

## QA boundary

Objective artifact/source/assembly verification is complete. No claim is made that a human subjective listen-back occurred in this worker. Future listener feedback should repair only the smallest failed chunk or seam if needed.

## Reusable production lesson

Audio Score -> natural preview-safe chunks (about 500 chars max) -> `deep` -> identical `transcript` and `preview_transcript` -> capture returned Google Storage `preview_url` -> Actions download/ffprobe -> ffmpeg stitch -> settling tail -> verify -> v2 asset -> reconcile v2 + public manifests.
""")

run("git", "config", "user.name", "github-actions[bot]")
run("git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")
run("git", "add", str(V2_MANIFEST.relative_to(ROOT)), str(PUBLIC_MANIFEST.relative_to(ROOT)), str((VERIFY_DIR / "source-publication-verification.json").relative_to(ROOT)), str(STATUS.relative_to(ROOT)))
cp = subprocess.run(["git", "diff", "--cached", "--quiet"])
if cp.returncode == 0:
    print("No publication changes to commit")
else:
    run("git", "commit", "-m", "Publish Audio Score v2 Chapter 008")
    run("git", "push")
