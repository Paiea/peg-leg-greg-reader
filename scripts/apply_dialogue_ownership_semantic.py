#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

PARA_RE = re.compile(r'<p>(.*?)</p>', re.S)
SPEECH = r'(?:said|asked|answered|replied|added|muttered|continued|told|called|shouted|whispered|yelled|said again|asked again)'
ACTION = r'(?:looked|smiled|laughed|nodded|frowned|shrugged|leaned|stood|sat|turned|stared|watched|pointed|held|took|picked|pushed|pulled|crossed|sighed|blinked|froze|stopped|waited|moved|walked|stepped|glanced|tapped|reached|opened|closed|followed|started|stayed|kept|put|set|folded|unfolded|lifted|lowered|handed|offered|touched|checked|counted|tilted|shook|raised|dropped|waved|grinned|winced|flinched|paused|breathed|exhaled|inhaled|rubbed|scratched|shifted|backed|came|went|left|returned|approached|grabbed|caught|released|gestured|did|named|swore|considered)'

STALE_ARLO_BLOCK_OLD = '<p>"What?" Antonius asked.</p><p>"Nothing," I said.</p><p>"You keep looking at me," Antonius said.</p><p>"I have a memorable-face problem," I said.</p><p>"Your face?" Antonius asked.</p><p>"Other people\'s." Antonius held out his hand.</p><p>"You\'ve been staring at my hands for five minutes," Arlo said.</p>'
STALE_ARLO_BLOCK_NEW = '<p>"What?" Arlo asked.</p><p>"Nothing," I said.</p><p>"You keep looking at me," Arlo said.</p><p>"I have a memorable-face problem," I said.</p><p>"Your face?" Arlo asked.</p><p>"Other people\'s."</p><p>Arlo held out his hand.</p><p>"You\'ve been staring at my hands for five minutes," Arlo said.</p>'


def explicit_speaker(p: str) -> tuple[str | None, int | None]:
    m = re.search(rf'\bI\s+{SPEECH}\b', p, re.I)
    if m:
        return 'GREG', m.start()
    m = re.search(rf'\b(?:he|she|they|[A-Z][a-z]+)\s+{SPEECH}\b', p)
    if m:
        return 'OTHER', m.start()
    return None, None


def begins_dialogue(p: str) -> bool:
    return p.lstrip().startswith('"')


def infer_speakers(paras: list[str]) -> list[tuple[str | None, int | None]]:
    result = []
    last_sp: str | None = None
    last_dialogue = False
    for p in paras:
        has_dialogue = '"' in p
        sp, anchor = explicit_speaker(p) if has_dialogue else (None, None)
        if has_dialogue and sp is None and begins_dialogue(p) and last_dialogue and last_sp:
            sp = 'OTHER' if last_sp == 'GREG' else 'GREG'
            anchor = p.find('"')
        elif has_dialogue and sp is not None:
            first_q = p.find('"')
            if first_q >= 0 and (anchor is None or first_q < anchor):
                anchor = first_q
        result.append((sp, anchor))
        if has_dialogue:
            if sp:
                last_sp = sp
            last_dialogue = True
        else:
            last_dialogue = False
    return result


def quote_map(p: str) -> tuple[list[bool], list[int]]:
    """Return outside-quote flags and positions immediately after closing quotes."""
    outside = [True] * len(p)
    closing_starts: list[int] = []
    inside = False
    for i, ch in enumerate(p):
        if ch == '"':
            if inside:
                closing_starts.append(i + 1)
            inside = not inside
            outside[i] = True
        else:
            outside[i] = not inside
    return outside, closing_starts


def next_nonspace(p: str, pos: int) -> int:
    while pos < len(p) and p[pos].isspace():
        pos += 1
    return pos


def action_events(p: str) -> list[tuple[int, str]]:
    outside, closing_starts = quote_map(p)
    starts = {0}
    for i, ch in enumerate(p):
        if ch in '.!?' and outside[i]:
            starts.add(next_nonspace(p, i + 1))
    for pos in closing_starts:
        starts.add(next_nonspace(p, pos))

    subj_re = re.compile(rf'(I|He|She|They|[A-Z][a-z]+)\s+({ACTION})\b')
    events: list[tuple[int, str]] = []
    for pos in sorted(starts):
        if pos >= len(p) or not outside[pos]:
            continue
        m = subj_re.match(p, pos)
        if not m:
            continue
        if not all(outside[j] for j in range(m.start(), min(m.end(), len(outside)))):
            continue
        owner = 'GREG' if m.group(1) == 'I' else 'OTHER'
        events.append((m.start(), owner))
    return events


def transform_paragraph(p: str, speaker: str | None, anchor: int | None) -> tuple[str, int]:
    if not speaker or '"' not in p or '<' in p or '&' in p:
        return p, 0
    events = action_events(p)
    if anchor is not None:
        events.append((anchor, speaker))
    events = sorted(set(events), key=lambda x: x[0])
    if not events:
        return p, 0

    breaks = []
    current_owner = None
    for pos, owner in events:
        if current_owner is None:
            current_owner = owner
            continue
        if owner != current_owner:
            if 0 < pos < len(p):
                breaks.append(pos)
            current_owner = owner

    if not breaks:
        return p, 0
    new = p
    for pos in sorted(set(breaks), reverse=True):
        new = new[:pos] + '</p><p>' + new[pos:]
    return new, len(set(breaks))


def transform_html(text: str) -> tuple[str, int]:
    article = text.split('<article class="prose">', 1)[1].split('</article>', 1)[0]
    paras = PARA_RE.findall(article)
    inferred = infer_speakers(paras)
    transformed = text
    total = 0
    for p, (sp, anchor) in zip(paras, inferred):
        new, count = transform_paragraph(p, sp, anchor)
        if count:
            transformed = transformed.replace('<p>' + p + '</p>', '<p>' + new + '</p>', 1)
            total += count
    return transformed, total


def self_test() -> None:
    cases = [
        ('"Fine." He counted silver.', 'GREG', 0, '"Fine." </p><p>He counted silver.'),
        ('"Too boring." He stayed in the next hand.', 'GREG', 0, '"Too boring." </p><p>He stayed in the next hand.'),
        ('"Excellent," I said. He looked concerned.', 'GREG', 0, '"Excellent," I said. </p><p>He looked concerned.'),
        ('Jorren said, "Old man." I stared at him. He laughed.', 'OTHER', 0, 'Jorren said, "Old man." </p><p>I stared at him. </p><p>He laughed.'),
        ('Antonius looked at me long enough that I said, "What?"', 'GREG', 36, 'Antonius looked at me long enough that </p><p>I said, "What?"'),
    ]
    for raw, sp, anchor, expected in cases:
        got, _ = transform_paragraph(raw, sp, anchor)
        assert got == expected, (raw, got, expected)
    print('self-test passed')


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--start', type=int, default=1)
    ap.add_argument('--end', type=int, default=20)
    ap.add_argument('--self-test', action='store_true')
    args = ap.parse_args()
    if args.self_test:
        self_test()
        return 0

    total = 0
    touched = []
    for n in range(args.start, args.end + 1):
        path = Path('chapters') / f'{n:03d}.html'
        original = path.read_text(encoding='utf-8')
        text = original
        if n == 3 and STALE_ARLO_BLOCK_OLD in text:
            text = text.replace(STALE_ARLO_BLOCK_OLD, STALE_ARLO_BLOCK_NEW, 1)
        if n == 1:
            old = '<p>I jumped once. That was childish. I did it again. The floorboards creaked. A voice from the other side of the wall shouted, "Some of us are sleeping!" I knew that voice. Or thought I did. I froze.'
            new = '<p>I jumped once. That was childish. I did it again. The floorboards creaked.</p><p>A voice from the other side of the wall shouted, "Some of us are sleeping!"</p><p>I knew that voice. Or thought I did. I froze.'
            if old in text:
                text = text.replace(old, new, 1)
        new_text, count = transform_html(text)
        if new_text != original:
            path.write_text(new_text, encoding='utf-8')
            touched.append((n, count))
            total += count
    print(f'applied {total} semantic paragraph boundaries across {len(touched)} chapters')
    for n, count in touched:
        print(f'  {n:03d}: {count}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
