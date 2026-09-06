#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path

PATHS = {
    197: [Path("chapters/197.html"), Path("light/197.html")],
    198: [Path("chapters/198.html"), Path("light/198.html")],
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


CH197_MORNING = [
    "My wrist was stiff in the morning. Not hurt. Stiff. I rotated it until Lyssa told me to stop because four checks had already established the point.",
    "She finally identified the mysterious narrow dark-blue cloth as sleeve binding. Three days of mystery had produced an edge treatment. I was not disappointed, exactly. I had simply expected more object.",
    "The old Hessa note remained under the cup and I left it there. Lyssa noticed, kissed the side of my head, and told me to go to work before I could turn restraint into an argument.",
    "On the way I bought one piece of fried dough folded around greens. It cost enough to regret for one bite and tasted good enough to end the regret. Financially dangerous.",
]

CH197_ROLE = [
    "The board gave me PETITIONER / SET. Marek was still absent, and nobody had marked the space around his missing name as special.",
    "Rinna clarified that I was not Third Man. Today I was the fence petitioner first, then the same man returning with a drainage complaint. Four lines. Teren confirmed the local version, entrance, and count in roughly the time it took Davin to reject a bent hinge pin.",
    "Nessa put me in a short brown coat that smelled faintly of old smoke. Nearby she was still forcing Marek's broader king coat onto Sellen, who regarded every pin as attempted murder. I briefly became responsible for a piece of cord because that was how theatre objects migrated.",
    "Veya and I ran the petitioner once. I arrived furious that a neighbor kept moving a boundary post. She told me to move it back. I returned later because the lane drain was pouring into my yard. She told me the garden was watered and the chair should go inside.",
    "Teren's only useful correction was not to wait for help that the official had no intention of giving. The man's problems were real. The joke was that government remained perfectly calm about them.",
]

CH197_REPAIR = [
    "The rest of the morning was set work. When Davin needed the repaired door held upright, my wrist reminded me about yesterday, so I asked Pell for the heavier side. He took it without requiring an explanation. Davin fitted the new pin, tested the door twice, and dismissed us when it behaved like a door.",
]

CH198_MORNING = [
    "Lyssa was gone before I woke, but she had left me the larger piece of bread. I treated this as suspicious generosity, checked my wrist once, and discovered that once was enough. The wrist and shoulder were nearly boring again.",
    "Nothing new waited under the cup. I left it alone, ate the oversized bread, and went to work. On the way, three people were helping a cart out of a hole while four more explained why they were doing it wrong. Carrow remained fully staffed.",
]

CH198_BOARD = [
    "Inside, Pell and Davin were fixing a wobbling bench. Pell found the missing square nut under it; Davin put it back where it belonged. The repair required less philosophy than my inspection of it.",
    "The board initially gave me SET. Rinna pointed out that I was early only because I had arrived at my old time, which was exactly why she had made third bell official. The new schedule had survived several minutes before theatre began negotiating with it.",
    "Teren came through carrying pages, asked where everyone was, and found me before Rinna could finish proving the system worked.",
]

CH198_GUARD = [
    "The Guard had six lines until I found one about a chicken that no longer existed in the local version. Teren crossed it out. Five. The final line concerned a petitioner's empty basket being called a gift, which did not improve my opinion of the government.",
    "Nessa rejected one coat because it made me look like a clerk and chose a shorter brown one. The left cuff caught against my crutch, so she folded and pinned it until the crossing cleared. Sellen, still wearing Marek's altered king coat, informed me that I now had his government. I told him I guarded the door. He predicted badly.",
    "The repaired stage door had new behavior too. I let it slam once, received Davin's entire review in one word, then learned to close it under my hand. No theory. Just a door that had changed and expected me to notice.",
]


def transform_paragraphs(number, paragraphs):
    out = list(paragraphs)
    if number == 197:
        if any('OLD_MORNING_CHECK_LOOP' in p for p in out):
            out = repl(out, 'My wrist was stiff in the morning.', 'At the hall, Rinna was counting tickets that did not yet belong to anyone.', CH197_MORNING)
        elif not any('Three days of mystery had produced an edge treatment.' in p for p in out):
            out = repl(out, 'My wrist was stiff in the morning.', 'At the hall, Rinna was counting tickets that did not yet belong to anyone.', CH197_MORNING)

        if any('OLD_ROLE_INTERROGATION_LOOP' in p for p in out):
            out = repl(out, 'At the hall, Rinna was counting tickets that did not yet belong to anyone.', 'I liked the petitioner.', ['At the hall, Rinna was counting tickets that did not yet belong to anyone.'] + CH197_ROLE)
        elif not any('The joke was that government remained perfectly calm about them.' in p for p in out):
            out = repl(out, 'The board was short.', 'I liked the petitioner.', CH197_ROLE)

        if any('OLD_REPAIR_AND_LUNCH_LOOP' in p for p in out):
            out = repl(out, 'Nobody respected them.', 'The afternoon changed something.', ['Nobody respected them.'] + CH197_REPAIR)
        elif not any('The repair required less philosophy than my inspection of it.' in p for p in out):
            out = repl(out, 'The rest of the morning was less theatrical.', 'At midday Hara arrived', CH197_REPAIR)

    elif number == 198:
        if any('OLD_MORNING_AND_STREET_LOOP' in p for p in out):
            out = repl(out, 'Lyssa was gone before I woke.', 'Until the Guild sends for you, third bell.', CH198_MORNING + ['Until the Guild sends for you, third bell.'])
        elif not any('Carrow remained fully staffed.' in p for p in out):
            out = repl(out, 'Lyssa was gone before I woke.', 'At the hall, Rinna was standing just inside the front doors', CH198_MORNING + ['At the hall, Rinna was standing just inside the front doors with a small slate in one hand and a piece of chalk in the other.'])

        if any('OLD_BENCH_AND_BOARD_LOOP' in p for p in out):
            out = repl(out, 'I had been scheduled.', 'Teren looked directly at me.', ['I had been scheduled.'] + CH198_BOARD)
        elif not any('The new schedule had survived several minutes' in p for p in out):
            out = repl(out, 'The hall smelled of old cloth', 'Teren looked directly at me.', CH198_BOARD)

        if any('OLD_GUARD_VERSION_AND_COSTUME_LOOP' in p for p in out):
            out = repl(out, 'Good. Guard.', 'Rehearsal took eleven minutes.', ['Good. Guard.'] + CH198_GUARD)
        elif not any('The Guard had six lines until I found one about a chicken' in p for p in out):
            out = repl(out, 'The Guard had six lines.', 'Rehearsal took eleven minutes.', CH198_GUARD)

        if any('OLD_REHEARSAL_PROCEDURE_LOOP' in p for p in out):
            out = repl(out, 'Rehearsal took eleven minutes.', 'The guard worked.', ['Rehearsal took eleven minutes.'])
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
        197: [
            'I liked the petitioner.',
            'Nobody respected them.',
            'At midday Hara arrived',
        ],
        198: [
            'Until the Guild sends for you, third bell.',
            'I had been scheduled.',
            'Good. Guard.',
            'Rehearsal took eleven minutes.',
        ],
    }
    for number, paths in PATHS.items():
        texts = [extract_prose((root / rel).read_text(encoding='utf-8')) for rel in paths]
        for cue in protected[number]:
            if not all(cue in text for text in texts):
                raise AssertionError(f'{number} missing protected cue {cue!r}')
        if texts[0] != texts[1]:
            raise AssertionError(f'{number} illustrated/text prose diverged')
    print('197-198 illustrated/text prose agree and protected beats survive')


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
        'batch': '197-198',
        'status': 'applied' if args.write else 'preview',
        'strength': 'aggressive-on-repeated-theatre-procedure-preserve-distinct-state-changes',
        'source_authority': 'reader chapter prose with synchronized text-reader projection',
        'stable_id_actions': {
            'plg-ch-000197': {'status': 'active', 'action': 'tightened_petitioner_role_flexibility'},
            'plg-ch-000198': {'status': 'active', 'action': 'tightened_regular_schedule_and_guard_adaptation'},
        },
        'illustration_policy': 'advisory hold; art does not protect redundant prose or chapter boundaries',
        'stats': stats,
        'protected': {
            '197': [
                'Lyssa relationship texture',
                'Petitioner role remains a distinct live-performance beat',
                'Greg asks for the correct version instead of assuming',
                'wrist limitation changes how Greg shares set-work load',
                'Hara and Sellen lunch material remains outside the compressed repair block',
            ],
            '198': [
                'Rinna formalizes third-bell regularity',
                'schedule is immediately shown to be adaptable',
                'Guard role remains distinct from Petitioner',
                'obsolete chicken-line version check survives',
                'costume is adapted around Greg crutch use',
                'actual Guard rehearsal remains intact',
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
