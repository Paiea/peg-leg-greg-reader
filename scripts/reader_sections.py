from __future__ import annotations

from dataclasses import dataclass
from html import escape


@dataclass(frozen=True)
class ReaderAct:
    numeral: str
    title: str
    start: int
    end: int
    deck: str

    @property
    def range_label(self) -> str:
        return f'Chapters {self.start}–{self.end}'


ACTS = (
    ReaderAct('ACT I', 'THE SECOND LIFE', 1, 20, 'The impossible morning becomes a second life.'),
    ReaderAct('ACT II', 'MAKING A PLACE', 21, 63, 'Carrow becomes work, people, obligations, and a place to stand.'),
    ReaderAct('ACT III', 'THE NEW BASELINE', 64, 82, 'The terms of Greg’s second life change.'),
    ReaderAct('ACT IV', 'A LIFE IN CARROW', 83, 137, 'Work, magic, friendship, Lyssa, and theatre settle into one lived-in life.'),
    ReaderAct('ACT V', 'THE COMPANY ROAD', 138, 155, 'The company takes its work beyond the familiar rooms of Carrow.'),
)


def render_act_details(chapter_links: dict[int, str], *, open_first: bool = False) -> str:
    rendered: list[str] = []
    first_rendered = True
    for act in ACTS:
        links = [chapter_links[n] for n in range(act.start, act.end + 1) if n in chapter_links]
        if not links:
            continue
        open_attr = ' open' if open_first and first_rendered else ''
        first_rendered = False
        rendered.append(
            f'<details class="reader-act"{open_attr}>'
            f'<summary class="reader-act-summary">'
            f'<span class="reader-act-kicker">{escape(act.numeral)} · {escape(act.range_label)}</span>'
            f'<span class="reader-act-title">{escape(act.title)}</span>'
            f'</summary>'
            f'<p class="reader-act-deck">{escape(act.deck)}</p>'
            f'<div class="reader-act-grid">{"".join(links)}</div>'
            f'</details>'
        )
    return ''.join(rendered)
