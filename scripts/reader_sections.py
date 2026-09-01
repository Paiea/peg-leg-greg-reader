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


@dataclass(frozen=True)
class ReaderBook:
    numeral: str
    title: str
    start: int
    end: int | None
    deck: str
    hero: str | None
    hero_alt: str | None
    acts: tuple[ReaderAct, ...]


BOOKS = (
    ReaderBook(
        'BOOK I',
        'Book One',
        1,
        82,
        'A second life becomes a place, a body, and a set of obligations Greg can no longer call temporary.',
        'visual/homepage/Book01_Plate.jpg',
        'Greg moving through lived-in Carrow on two crutches, surrounded by the ordinary work and streets that define Book One.',
        (
            ReaderAct('ACT I', 'THE SECOND LIFE', 1, 20, 'The impossible morning becomes a second life.'),
            ReaderAct('ACT II', 'MAKING A PLACE', 21, 63, 'Carrow becomes work, people, obligations, and a place to stand.'),
            ReaderAct('ACT III', 'THE NEW BASELINE', 64, 82, 'The terms of Greg’s second life change, then become ordinary enough to live inside.'),
        ),
    ),
    ReaderBook(
        'BOOK II',
        'Book Two',
        83,
        None,
        'Carrow becomes a life: Lyssa, magic, theatre, company work, roads, money, and the attention that follows accumulated competence.',
        'visual/homepage/Book02_Plate.jpg',
        'Greg just offstage on two crutches amid the working theatre company, with Carrow life continuing beyond the stage door.',
        (
            ReaderAct('ACT I', 'A LIFE IN CARROW', 83, 111, 'Recovery gives way to dating, work, magic questions, errands, and an increasingly ordinary shared life.'),
            ReaderAct('ACT II', 'THE STAGE DOOR', 112, 137, 'Greg enters the theatre as a machine of people and work, then starts finding a place inside it.'),
            ReaderAct('ACT III', 'THE COMPANY ROAD', 138, 180, 'Theatre leaves the familiar room, travel and performance become real work, and Greg accumulates roles by doing them.'),
            ReaderAct('ACT IV', 'THE WORKING COMPANY', 181, 217, 'Calling, backstage labor, performance, customers, debt work, and city routines deepen into a working social world.'),
            ReaderAct('ACT V', 'THE PRICE OF ATTENTION', 218, None, 'Ordinary life keeps accumulating while money, access, reputation, and outside attention begin carrying sharper consequences.'),
        ),
    ),
)


def _in_range(number: int, start: int, end: int | None) -> bool:
    return number >= start and (end is None or number <= end)


def _range_label(numbers: list[int]) -> str:
    if not numbers:
        return ''
    if numbers[0] == numbers[-1]:
        return f'Chapter {numbers[0]}'
    return f'Chapters {numbers[0]}–{numbers[-1]}'


def render_act_details(acts: tuple[ReaderAct, ...], chapter_links: dict[int, str], *, open_first: bool = False) -> str:
    rendered: list[str] = []
    first_rendered = True
    for act in acts:
        numbers = [n for n in sorted(chapter_links) if _in_range(n, act.start, act.end)]
        if not numbers:
            continue
        links = [chapter_links[n] for n in numbers]
        open_attr = ' open' if open_first and first_rendered else ''
        first_rendered = False
        rendered.append(
            f'<details class="reader-act"{open_attr}>'
            f'<summary class="reader-act-summary">'
            f'<span class="reader-act-kicker">{escape(act.numeral)} · {escape(_range_label(numbers))}</span>'
            f'<span class="reader-act-title">{escape(act.title)}</span>'
            f'</summary>'
            f'<p class="reader-act-deck">{escape(act.deck)}</p>'
            f'<div class="reader-act-grid">{"".join(links)}</div>'
            f'</details>'
        )
    return ''.join(rendered)


def render_book_sections(
    chapter_links: dict[int, str],
    *,
    include_heroes: bool,
    hero_prefix: str = '',
    open_first_act: bool = False,
) -> str:
    rendered: list[str] = []
    for book_index, book in enumerate(BOOKS):
        book_numbers = [n for n in sorted(chapter_links) if _in_range(n, book.start, book.end)]
        if not book_numbers:
            continue
        hero = ''
        if include_heroes and book.hero:
            hero_src = f'{hero_prefix}{book.hero}'
            loading = 'eager' if book_index == 0 else 'lazy'
            priority = ' fetchpriority="high"' if book_index == 0 else ''
            hero = (
                '<figure class="reader-book-hero">'
                f'<img src="{escape(hero_src, quote=True)}" alt="{escape(book.hero_alt or "", quote=True)}" '
                f'width="1024" height="1280" loading="{loading}" decoding="async"{priority} '
                'onerror="this.closest(\'figure\').remove()">'
                '</figure>'
            )
        rendered.append(
            '<section class="reader-book">'
            '<header class="reader-book-intro">'
            f'<span class="reader-book-kicker">{escape(book.numeral)} · {escape(_range_label(book_numbers))}</span>'
            f'<h3 class="reader-book-title">{escape(book.title)}</h3>'
            f'<p class="reader-book-deck">{escape(book.deck)}</p>'
            f'{hero}'
            '</header>'
            f'{render_act_details(book.acts, chapter_links, open_first=open_first_act and book is BOOKS[0])}'
            '</section>'
        )
    return ''.join(rendered)
