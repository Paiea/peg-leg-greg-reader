#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path

PATHS = {
    183: [Path("chapters/183.html"), Path("light/183.html")],
    184: [Path("chapters/184.html"), Path("light/184.html")],
}
ARTICLE_RE = re.compile(r'(<article class="prose(?: light-prose)?">)(.*?)(</article>)', re.I | re.S)
P_RE = re.compile(r'<p(?:\s[^>]*)?>(.*?)</p>', re.I | re.S)
TAG_RE = re.compile(r'<[^>]+>')


def norm(s):
    return re.sub(r'\s+', ' ', html.unescape(TAG_RE.sub('', re.sub(r'<br\s*/?>', ' ', s, flags=re.I)))).strip()


def wc(ps):
    return sum(len(re.findall(r"\b\w+[’'-]?\w*\b", p)) for p in ps)


def idx(ps, cue):
    matches = [i for i, p in enumerate(ps) if cue in p]
    if len(matches) != 1:
        raise ValueError(f"cue {cue!r}: {len(matches)} matches")
    return matches[0]


def repl(ps, start, end, new):
    i, j = idx(ps, start), idx(ps, end)
    if j <= i:
        raise ValueError(f"bad range {start} -> {end}")
    return ps[:i] + new + ps[j:]


CH183_HOME = [
    "I spent breakfast staring at the corner of the paper under Lyssa's book and not touching it. Lyssa counted that as progress only after telling me to stop staring and go to work.",
    "Three short pieces of blue thread remained tied around folded scraps on the table. Lyssa's explanation was that the rest had gone to people who needed blue thread. Marra had some. Jessa had one. The others were, apparently, people.",
    "The cup and last night's copper were still there too. The copper felt heavier because I had earned it, which was not how weight worked. I took my crutches and went to work before I could investigate the feeling further.",
]

CH183_MAGIC = [
    "At East Market Hall, Pell met me beside the repaired latch and demanded magic. I told him the useful version: I had moved paper under glass while Hessa supervised, and I was not doing it here. He tried to expand that into feathers, string, fake petitions, and finally 'things.' I refused the categories until Nessa found him something real to carry.",
    "Teren asked the questions that mattered to theatre. Could I do it on cue? Here? Without Hessa? On anything larger than paper? No, no, no, and no. He nodded, decided the magic was not his problem, and handed me a rope for the doorframe instead.",
]

CH183_REPAIR = [
    "The red doorframe had split through an old peg hole in one foot. Davin was absent, so Nessa bound a replacement block in place while I kept the frame upright. My shoulder objected to the awkward hold; she told me to sit closer, which irritatingly solved most of it.",
    "By then Pell's version of my magic had reached Sellen, who asked whether I could move the doorframe with it. I could not. This disappointed him and improved nothing. Nessa tightened the repair while I learned that theatre gossip traveled faster than useful information.",
    "The new block held. Another worker and I carried the frame to its mark, and the curtain wheel Davin had fixed opened without its old scrape. Nobody remarked on either repair once it worked. That seemed to be the standard.",
]

CH184_BREAKFAST = [
    "Lyssa asked me for a favor before I had finished chewing and put a gray parcel tied with blue thread on the table. For one stupid second I thought she wanted me to move it with magic. She wanted me to carry it to Marra's.",
    "The instructions were simple in the way other people's errands were always simple: give it to Marra, say the left side was marked, do not untie it, and if Jessa happened to be there tell her narrow, not wide. I did not know what was narrow. Lyssa assured me I did not need to.",
    "My right palm was still tender from calling the show, and the scrap cloth around the crutch grip had bunched again. Lyssa told me to replace it. Then she noticed I was still pleased about moving paper and reduced the achievement to its proper dimensions: a very small amount, under glass, while supervised.",
    "She would be west until at least midday. I had the parcel, three copper, a theatre call before noon, and no reason to go near the Guild. It seemed manageable.",
]

CH184_ERRAND = [
    "Marra's was a few streets out of the way, which remained more meaningful on crutches than it sounded. I delivered the parcel to the green door, repeated Lyssa's message about the marked left side, and learned that Jessa was supposedly at Sen's red door two lanes back.",
    "On the way, Nessa intercepted me and added a paper packet of hooks for the hall. Sen told me Jessa had gone to Marra's. I went back. Jessa was standing exactly where I had left the parcel. 'Narrow, not wide,' I told her. She understood, which made one of us.",
    "I escaped before anyone could hand me a third thing. By then the parcel was gone, the message was delivered, the hooks were under my arm, and the day had quietly converted me from a man going to work into a route.",
]

CH184_HOOKS = [
    "By the time I reached East Market Hall, my palm hurt and I was late enough for Rinna to be waiting in the doorway. I offered the hooks as evidence of productivity. She opened the packet and informed me they were costume hooks, not curtain hooks.",
    "Nessa had given them to me. Nessa was also somewhere else. Rinna sent the packet twelve paces into costumes, where a woman sewing a brown coat pronounced them useful. The wrong hooks had therefore reached the right place by a route nobody had intended.",
]

CH184_SHOW = [
    "The Petition ran that afternoon, and I got my goat back. I waited for the right cue, delivered the familiar argument without adding anything, and the scene worked. Teren said good and immediately gave me set work, which was becoming the more meaningful review.",
    "The repaired red door held. The curtain worked. The fake petition returned to its box. For almost an hour, I forgot I had any magic at all. Then Pell passed with a painted bucket, called me 'Magician,' and accepted 'Props' as my entire answer.",
]


def transform_paragraphs(number, paragraphs):
    out = list(paragraphs)
    if number == 183:
        if any('OLD_HOME_MAGIC_LOOP' in p for p in out):
            out = repl(out, 'I woke up looking at the corner of a piece of paper.', 'At East Market Hall, Pell was waiting for me beside the repaired latch.', CH183_HOME)
        elif not any("last night's copper were still there too" in p for p in out):
            out = repl(out, 'I woke up looking at the corner of a piece of paper.', 'At East Market Hall, Pell was waiting for me beside the repaired latch.', CH183_HOME)

        if any('OLD_MAGIC_QUESTION_LOOP' in p for p in out):
            out = repl(out, 'At East Market Hall, Pell was waiting for me beside the repaired latch.', 'That was how my first established external magical effect entered the theatre.', CH183_MAGIC)
        elif not any('Teren asked the questions that mattered to theatre.' in p for p in out):
            out = repl(out, 'At East Market Hall, Pell was waiting for me beside the repaired latch.', 'That was how my first established external magical effect entered the theatre.', CH183_MAGIC)

        if any('OLD_DOOR_REPAIR_LOOP' in p for p in out):
            out = repl(out, 'That was how my first established external magical effect entered the theatre.', 'The afternoon audience began arriving before we were ready.', ['That was how my first established external magical effect entered the theatre.'] + CH183_REPAIR)
        elif not any('the standard.' in p for p in out):
            out = repl(out, 'The red doorframe had split at the lower joint.', 'The afternoon audience began arriving before we were ready.', CH183_REPAIR)

    elif number == 184:
        if any('OLD_BREAKFAST_AND_PARCEL_LOOP' in p for p in out):
            out = repl(out, 'Lyssa asked me for a favor before I had finished chewing.', 'That was my second warning.', CH184_BREAKFAST)
        elif not any('the day had quietly converted me' in p for p in out) and not any('It seemed manageable.' == p for p in out):
            raise ValueError('chapter 184 authority does not match expected pre-compression opening')
        elif not any('a theatre call before noon' in p for p in out):
            out = repl(out, 'Lyssa asked me for a favor before I had finished chewing.', 'That was my second warning.', CH184_BREAKFAST)

        if any('OLD_MARRA_SEN_MARRA_LOOP' in p for p in out):
            out = repl(out, "Marra's was not on the way to East Market Hall.", 'By the time I reached East Market Hall, my palm hurt', CH184_ERRAND)
        elif not any('converted me from a man going to work into a route.' in p for p in out):
            out = repl(out, "Marra's was not on the way to East Market Hall.", 'By the time I reached East Market Hall, my palm hurt', CH184_ERRAND)

        if any('OLD_WRONG_HOOKS_LOOP' in p for p in out):
            out = repl(out, 'By the time I reached East Market Hall, my palm hurt', 'Teren was onstage.', CH184_HOOKS)
        elif not any('The wrong hooks had therefore reached the right place' in p for p in out):
            out = repl(out, 'By the time I reached East Market Hall, my palm hurt', 'Teren was onstage.', CH184_HOOKS)

        if any('OLD_FAMILIAR_SHOW_LOOP' in p for p in out):
            out = repl(out, 'The Petition ran that afternoon.', 'I left for the south market after my piece.', CH184_SHOW)
        elif not any("accepted 'Props' as my entire answer" in p for p in out):
            out = repl(out, 'The Petition ran that afternoon.', 'I left for the south market after my piece.', CH184_SHOW)
    else:
        raise ValueError(number)
    return out


def transform_html(text, number):
    match = ARTICLE_RE.search(text)
    if not match:
        raise ValueError('article missing')
    body = match.group(2)
    figures = re.findall(r'<figure\b.*?</figure>', body, re.I | re.S)
    before = [norm(x.group(1)) for x in P_RE.finditer(body)]
    after = transform_paragraphs(number, before)
    if after == before:
        return text, before, after
    new_body = ''.join(f'<p>{html.escape(p, quote=False)}</p>' for p in after)
    new_body += ''.join(figures)
    return text[:match.start(2)] + new_body + text[match.end(2):], before, after


def extract_prose(text):
    match = ARTICLE_RE.search(text)
    if not match:
        raise ValueError('article missing')
    return '\n'.join(norm(x.group(1)) for x in P_RE.finditer(match.group(2)))


def verify(root):
    protected = {
        183: [
            'That was how my first established external magical effect entered the theatre.',
            'The afternoon problem was not the children.',
            'The piece ran with a plain lamp.',
            "The Miller's Son was next.",
        ],
        184: [
            'Lyssa asked me for a favor',
            'The Petition ran that afternoon',
            'For almost an hour, I forgot I had any magic at all.',
            'I left for the south market after my piece.',
        ],
    }
    forbidden_duplicates = {
        183: ['That was how my first established external magical effect entered the theatre.'],
        184: ['That was my second warning.'],
    }
    for number, paths in PATHS.items():
        texts = [extract_prose((root / rel).read_text(encoding='utf-8')) for rel in paths]
        for cue in protected[number]:
            if not all(cue in text for text in texts):
                raise AssertionError(f'{number} missing protected cue {cue!r}')
        for cue in forbidden_duplicates[number]:
            if any(text.count(cue) != 1 for text in texts):
                raise AssertionError(f'{number} duplicate boundary cue {cue!r}')
        if texts[0] != texts[1]:
            raise AssertionError(f'{number} illustrated/text prose diverged')
    print('183-184 illustrated/text prose agree and protected beats survive')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path('.'))
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--manifest', type=Path)
    args = parser.parse_args()
    root = args.root.resolve()

    if args.verify:
        verify(root)
        return

    stats = {}
    for number, paths in PATHS.items():
        for rel in paths:
            path = root / rel
            original = path.read_text(encoding='utf-8')
            updated, before, after = transform_html(original, number)
            stats[str(rel)] = {
                'before_words': wc(before),
                'after_words': wc(after),
                'delta_words': wc(after) - wc(before),
            }
            if args.write and updated != original:
                path.write_text(updated, encoding='utf-8')

    if args.write:
        verify(root)

    manifest = {
        'schema_version': 1,
        'batch': '183-184',
        'status': 'applied' if args.write else 'preview',
        'strength': 'aggressive-on-repeated-magic-theatre-and-errand-procedure',
        'source_authority': 'current editor branch reader prose with synchronized text-reader projection',
        'stable_id_actions': {
            'plg-ch-000183': {'status': 'active', 'action': 'tightened_worker_magic-normalization_and_set-procedure'},
            'plg-ch-000184': {'status': 'active', 'action': 'tightened_runner_errand-relay_and_familiar-performance'},
        },
        'illustration_policy': 'advisory_hold; story structure outranks art anchors',
        'stats': stats,
        'protected': {
            '183': [
                'Lyssa boundary and blue-thread domestic texture',
                'theatre learns the bounded truth of Greg magic',
                'first external magic is normalized rather than converted into spectacle',
                'plain-lamp failure still proves performance can sell wonder',
                'new Miller clerk role remains outside compressed setup',
            ],
            '184': [
                'Lyssa entrusts Greg with an outside errand',
                'Marra and Jessa routing comedy survives in compressed form',
                'theatre independently uses Greg as a runner',
                'wrong-hook mistake and practical recovery survive',
                'familiar Third Man performance compresses to normalization rather than another transcript',
                'south-market lamp-oil errand remains intact as next outward work beat',
            ],
        },
    }

    if args.manifest:
        manifest_path = args.manifest if args.manifest.is_absolute() else root / args.manifest
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')

    print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    main()
