# Chapter 19 verification

- Exact spoken source coverage is locked by the successful Chapter 19 take-lock workflow and preserved in `takes/019.json`.
- 36/36 provider artifacts were captured as durable MP3 chunks.
- All chunks passed `ffprobe` during capture.
- The final chapter MP3 was stitched in numeric take order and passed `ffprobe`.
- Final duration: 867.168 seconds.
- Main manifest was fresh-read before publication reconciliation and Chapter 13 plus Chapter 21 newer entries were preserved.
- Chapter 19 route title is `The Maintainer` and points to `../greg-again/audio/assets/chapter-019.mp3`.
- Chapter-specific regression test: `tests/test_greg_again_audio_ch019.py`.
- Temporary generation/capture harnesses were removed after durable artifacts were secured. The verification harness is temporary and should be removed before final merge after it passes.
