#!/usr/bin/env python3
"""Assemble a speaker-pure 3L audio plan from public AI Voice preview assets.

Generic assembly layer. Creative/speaker decisions belong in the input plan.
This script never infers speakers or rewrites text.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import urllib.request

BASE_URL = 'https://storage.googleapis.com/adm--audio-playback--7d--public/mcp-preview/'


def run(cmd: list[str], **kwargs):
    return subprocess.run(cmd, check=True, text=True, **kwargs)


def ffprobe_duration(path: Path) -> float:
    out = subprocess.check_output([
        'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1', str(path)
    ], text=True).strip()
    value = float(out)
    if value <= 0:
        raise RuntimeError(f'non-positive audio duration for {path}: {value}')
    return value


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def download_one(item: tuple[int, str, Path]) -> dict:
    idx, asset_id, target = item
    url = BASE_URL + asset_id
    req = urllib.request.Request(url, headers={'User-Agent': '3L-audio-builder/1.0'})
    with urllib.request.urlopen(req, timeout=45) as response, target.open('wb') as out:
        shutil.copyfileobj(response, out)
    size = target.stat().st_size
    if size < 1000:
        raise RuntimeError(f'clip {idx:03d} downloaded only {size} bytes from {url}')
    duration = ffprobe_duration(target)
    return {'id': f'{idx:03d}', 'asset_id': asset_id, 'bytes': size, 'duration_s': duration}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--plan', required=True)
    ap.add_argument('--assets', required=True)
    ap.add_argument('--output', required=True)
    ap.add_argument('--receipt', required=True)
    ap.add_argument('--workdir', default='/tmp/3l-preview-build')
    args = ap.parse_args()

    plan_path = Path(args.plan)
    assets_path = Path(args.assets)
    output_path = Path(args.output)
    receipt_path = Path(args.receipt)
    work = Path(args.workdir)
    raw_dir = work / 'raw'
    wav_dir = work / 'wav'
    silence_dir = work / 'silence'
    for p in (raw_dir, wav_dir, silence_dir):
        p.mkdir(parents=True, exist_ok=True)

    plan = json.loads(plan_path.read_text())
    chunks = plan['chunks']
    asset_ids = [line.strip() for line in assets_path.read_text().splitlines() if line.strip()]
    if len(asset_ids) != len(chunks):
        raise SystemExit(f'asset/plan count mismatch: {len(asset_ids)} assets vs {len(chunks)} chunks')
    if len(asset_ids) != len(set(asset_ids)):
        raise SystemExit('duplicate preview asset IDs detected')

    jobs = [(i, asset_id, raw_dir / f'{i:03d}.mp3') for i, asset_id in enumerate(asset_ids, start=1)]
    downloaded = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
        futures = [pool.submit(download_one, job) for job in jobs]
        for future in concurrent.futures.as_completed(futures):
            downloaded.append(future.result())
    downloaded.sort(key=lambda x: x['id'])
    if len(downloaded) != len(chunks):
        raise SystemExit(f'only verified {len(downloaded)} of {len(chunks)} clips')

    # Normalize every source before concatenation so codec/sample-rate differences cannot leak into seams.
    for i in range(1, len(chunks) + 1):
        run([
            'ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
            '-i', str(raw_dir / f'{i:03d}.mp3'),
            '-ar', '44100', '-ac', '1', '-c:a', 'pcm_s16le',
            str(wav_dir / f'{i:03d}.wav')
        ])

    pause_values = sorted({int(c['pause_after_ms']) for c in chunks} | {int(plan.get('final_tail_ms', 2000))})
    for ms in pause_values:
        if ms <= 0:
            continue
        run([
            'ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
            '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono',
            '-t', f'{ms/1000:.3f}', '-c:a', 'pcm_s16le',
            str(silence_dir / f'{ms}.wav')
        ])

    concat_path = work / 'concat.txt'
    lines = []
    for i, chunk in enumerate(chunks, start=1):
        lines.append(f"file '{(wav_dir / f'{i:03d}.wav').resolve()}'")
        pause = int(chunk.get('pause_after_ms', 0))
        if pause > 0:
            lines.append(f"file '{(silence_dir / f'{pause}.wav').resolve()}'")
    final_tail = int(plan.get('final_tail_ms', 2000))
    if final_tail > 0:
        lines.append(f"file '{(silence_dir / f'{final_tail}.wav').resolve()}'")
    concat_path.write_text('\n'.join(lines) + '\n')

    assembled_wav = work / 'assembled.wav'
    run([
        'ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
        '-f', 'concat', '-safe', '0', '-i', str(concat_path),
        '-c:a', 'pcm_s16le', str(assembled_wav)
    ])

    output_path.parent.mkdir(parents=True, exist_ok=True)
    run([
        'ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
        '-i', str(assembled_wav), '-c:a', 'libmp3lame', '-b:a', '128k',
        str(output_path)
    ])
    final_duration = ffprobe_duration(output_path)
    final_size = output_path.stat().st_size
    final_sha = sha256_file(output_path)

    voice_counts = {}
    for chunk in chunks:
        voice_counts[chunk['voice']] = voice_counts.get(chunk['voice'], 0) + 1

    receipt = {
        'schema_version': 1,
        'record': plan.get('record'),
        'title': plan.get('title'),
        'source_path': plan.get('source_path'),
        'source_sha256': plan.get('source_sha256'),
        'plan_sha256': sha256_file(plan_path),
        'assets_sha256': sha256_file(assets_path),
        'asset_count': len(asset_ids),
        'verified_asset_count': len(downloaded),
        'voice_counts': voice_counts,
        'greg_voice': plan.get('greg_voice'),
        'dragon_voice': plan.get('dragon_voice'),
        'dragon_dsp': plan.get('dragon_dsp'),
        'final_tail_ms': final_tail,
        'source_clip_duration_min_s': min(x['duration_s'] for x in downloaded),
        'source_clip_duration_max_s': max(x['duration_s'] for x in downloaded),
        'output_path': str(output_path),
        'output_duration_s': final_duration,
        'output_bytes': final_size,
        'output_sha256': final_sha,
    }
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
