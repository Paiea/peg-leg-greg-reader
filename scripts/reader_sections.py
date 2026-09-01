from __future__ import annotations

from dataclasses import dataclass
from html import escape


@dataclass(frozen=True)
class ReaderAct:
    numeral: str
    title: str
    start: int
    end: int | None
    deck: str

    def effective_end(self, latest: int) -> int:
        return latest if self.end is None else min(self.end, latest)

    def range_label(self, latest: int) -> str:
        return f'Chapters {self.start}–{self.effective_end(latest)}'


@dataclass(frozen=True)
class ReaderBook:
    numeral: str
    slug: str
    start: int
    end: int | None
    acts: tuple[ReaderAct, ...]
    card_src: str
    card_alt: str
    card_href: str
    card_link_label: str

    def effective_end(self, latest: int) -> int:
        return latest if self.end is None else min(self.end, latest)

    def range_label(self, latest: int) -> str:
        return f'Chapters {self.start}–{self.effective_end(latest)}'


BOOKS = (
    ReaderBook(
        'BOOK I',
        'book-i',
        1,
        82,
        (
            ReaderAct('ACT I', 'THE SECOND LIFE', 1, 20, 'The impossible morning becomes a second life.'),
            ReaderAct('ACT II', 'MAKING A PLACE', 21, 63, 'Carrow becomes work, people, obligations, and a place to stand.'),
            ReaderAct('ACT III', 'THE NEW BASELINE', 64, 82, 'The terms of Greg’s second life change.'),
        ),
        'assets/book-role-cards/book-i-warrior-005.webp',
        'The Warrior, Chapter 05: young Greg working a sword at the bench, with the chapter quote and peg-leg medallion.',
        'chapters/005.html',
        'Open Chapter 5, The Warrior',
    ),
    ReaderBook(
        'BOOK II',
        'book-ii',
        83,
        180,
        (
            ReaderAct('ACT I', 'A LIFE IN CARROW', 83, 99, 'Work, magic, friendship, Lyssa, and theatre settle into one lived-in life.'),
            ReaderAct('ACT II', 'THE STAGE DOOR', 100, 137, 'The theatre becomes another working doorway into Carrow.'),
            ReaderAct('ACT III', 'THE COMPANY ROAD', 138, 180, 'The company takes its work beyond the familiar rooms of Carrow.'),
        ),
        'assets/book-role-cards/book-ii-stagehand-177.webp',
        'The Stagehand, Chapter 177: young bearded Greg working backstage, framed above the waist with no lower-body or mobility detail visible.',
        'light/177.html',
        'Open Chapter 177, The Stagehand',
    ),
    ReaderBook(
        'BOOK III',
        'book-iii',
        181,
        None,
        (
            ReaderAct('ACT I', 'THE WORKING COMPANY', 181, 219, 'Company work becomes routine, social, and increasingly interconnected.'),
            ReaderAct('ACT II', 'THE PRICE OF ATTENTION', 220, None, 'Ordinary work draws new attention, obligations, and pressure.'),
        ),
        'assets/book-role-cards/book-iii-magistrate-231.webp',
        'The Magistrate, Chapter 231: young bearded Greg inhabiting the theatrical magistrate role at a petitions desk.',
        'light/231.html',
        'Open Chapter 231, The Magistrate',
    ),
)

ACTS = tuple(act for book in BOOKS for act in book.acts)


def _render_act(
    act: ReaderAct,
    chapter_links: dict[int, str],
    latest: int,
    *,
    open_act: bool,
) -> str:
    end = act.effective_end(latest)
    if end < act.start:
        return ''
    links = [chapter_links[n] for n in range(act.start, end + 1) if n in chapter_links]
    if not links:
        return ''
    open_attr = ' open' if open_act else ''
    links_html = ''.join(links)
    return (
        f'<details class="reader-act"{open_attr}>'
        f'<summary class="reader-act-summary">'
        f'<span class="reader-act-kicker">{escape(act.numeral)} · {escape(act.range_label(latest))}</span>'
        f'<span class="reader-act-title">{escape(act.title)}</span>'
        f'</summary>'
        f'<p class="reader-act-deck">{escape(act.deck)}</p>'
        f'<div class="reader-act-grid">{links_html}</div>'
        f'</details>'
    )


def render_book_sections(
    chapter_links: dict[int, str],
    *,
    illustrated: bool,
    open_first_act: bool = False,
) -> str:
    if not chapter_links:
        return ''

    latest = max(chapter_links)
    rendered: list[str] = []
    first_act_rendered = True

    for book in BOOKS:
        book_end = book.effective_end(latest)
        if book_end < book.start or not any(book.start <= n <= book_end for n in chapter_links):
            continue

        acts: list[str] = []
        for act in book.acts:
            act_html = _render_act(
                act,
                chapter_links,
                latest,
                open_act=open_first_act and first_act_rendered,
            )
            if not act_html:
                continue
            acts.append(act_html)
            first_act_rendered = False

        if not acts:
            continue

        plate = ''
        layout_class = ' reader-book-layout--illustrated' if illustrated else ''
        if illustrated:
            plate = (
                f'<figure class="reader-book-plate">'
                f'<a class="reader-book-card-link" href="{escape(book.card_href)}" '
                f'aria-label="{escape(book.card_link_label)}">'
                f'<img class="reader-book-card-image" src="{escape(book.card_src)}" '
                f'alt="{escape(book.card_alt)}" width="600" height="800" '
                f'loading="lazy" decoding="async">'
                f'</a>'
                f'</figure>'
            )

        acts_html = ''.join(acts)
        rendered.append(
            f'<section class="reader-book" aria-labelledby="{book.slug}-heading">'
            f'<div class="reader-book-layout{layout_class}">'
            f'{plate}'
            f'<div class="reader-book-copy">'
            f'<header class="reader-book-heading">'
            f'<h3 class="reader-book-title" id="{book.slug}-heading">{escape(book.numeral)}</h3>'
            f'<p class="reader-book-range">{escape(book.range_label(latest))}</p>'
            f'</header>'
            f'<div class="reader-book-acts">{acts_html}</div>'
            f'</div>'
            f'</div>'
            f'</section>'
        )

    return ''.join(rendered)


def render_act_details(chapter_links: dict[int, str], *, open_first: bool = False) -> str:
    if not chapter_links:
        return ''
    latest = max(chapter_links)
    rendered: list[str] = []
    first_rendered = True
    for act in ACTS:
        act_html = _render_act(
            act,
            chapter_links,
            latest,
            open_act=open_first and first_rendered,
        )
        if not act_html:
            continue
        rendered.append(act_html)
        first_rendered = False
    return ''.join(rendered)
