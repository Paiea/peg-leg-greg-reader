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
    card_src: str = ''
    card_alt: str = ''
    card_href: str = ''

    def effective_end(self, latest: int) -> int:
        return latest if self.end is None else min(self.end, latest)

    def range_label(self, latest: int) -> str:
        return f'Chapters {self.start}–{self.effective_end(latest)}'


BOOKS = (
    ReaderBook(
        'BOOK I', 'book-i', 1, 82,
        (
            ReaderAct('ACT I', 'THE SECOND LIFE', 1, 20, 'The impossible morning becomes a second life.'),
            ReaderAct('ACT II', 'MAKING A PLACE', 21, 63, 'Carrow becomes work, people, obligations, and a place to stand.'),
            ReaderAct('ACT III', 'THE NEW BASELINE', 64, 82, 'The terms of Greg’s second life change.'),
        ),
        'assets/book-role-cards/book-i-warrior-005.webp',
        'The Warrior, Chapter 05: young Greg working a sword at the bench, with the chapter quote and peg-leg medallion.',
        'chapters/005.html',
    ),
    ReaderBook(
        'BOOK II', 'book-ii', 83, 180,
        (
            ReaderAct('ACT I', 'A LIFE IN CARROW', 83, 99, 'Work, magic, friendship, Lyssa, and theatre settle into one lived-in life.'),
            ReaderAct('ACT II', 'THE STAGE DOOR', 100, 137, 'The theatre becomes another working doorway into Carrow.'),
            ReaderAct('ACT III', 'THE COMPANY ROAD', 138, 180, 'The company takes its work beyond the familiar rooms of Carrow.'),
        ),
        'assets/book-role-cards/book-ii-stagehand-177.webp',
        'The Stagehand, Chapter 177: young bearded Greg working backstage, framed above the waist with no lower-body or mobility detail visible.',
        'chapters/177.html',
    ),
    ReaderBook(
        'BOOK III', 'book-iii', 181, 320,
        (
            ReaderAct('ACT I', 'THE WORKING COMPANY', 181, 219, 'Company work becomes routine, social, and increasingly interconnected.'),
            ReaderAct('ACT II', 'THE PRICE OF ATTENTION', 220, 280, 'Ordinary work draws new attention, obligations, and pressure.'),
            ReaderAct('ACT III', 'THE WIDER LIFE', 281, 320, 'Work, magic, travel, household life, and the city widen beyond any single lane.'),
        ),
        'assets/book-role-cards/book-iii-magistrate-231.webp',
        'The Magistrate, Chapter 231: young bearded Greg inhabiting the theatrical magistrate role at a petitions desk.',
        'chapters/231.html',
    ),
    ReaderBook(
        'BOOK IV', 'book-iv', 321, 440,
        (
            ReaderAct('ACT I', 'WHAT THINGS COST', 321, 330, 'Money, tools, risk, and opportunity become choices Greg can increasingly make for himself.'),
            ReaderAct('ACT II', 'BEYOND THE DOOR', 331, 388, 'Paid outside-city work becomes repeatable life as Greg’s competence travels through routes, survey, field systems, jobs, and people.'),
            ReaderAct('ACT III', 'THE FARTHER ROAD', 389, 440, 'Greg stops merely taking jobs beyond Carrow and begins inhabiting a genuinely wider regional life.'),
        ),
        'assets/book-role-cards/book-iv-surveyor-331.webp',
        'The Surveyor, Chapter 331: young bearded Greg on two crutches studying an old boundary marker with a field map, Carrow visible beyond the marker field.',
        'chapters/331.html',
    ),
    ReaderBook(
        'BOOK V', 'book-v', 441, None,
        (
            ReaderAct('ACT I', 'THE LONGER REACH', 441, None, 'Greg’s accumulated competence, money, relationships, and freedom of movement begin reaching farther than the structures that first contained his second life.'),
        ),
        'assets/book-role-cards/book-v-investor-446-q80.webp',
        'The Investor, Chapter 446: young bearded Greg at a harbor desk weighing ferry fares, routes, and money against the wider life those choices can buy.',
        'chapters/446.html',
    ),
)

ACTS = tuple(act for book in BOOKS for act in book.acts)


def book_and_act_for_chapter(number: int) -> tuple[ReaderBook, ReaderAct]:
    books = [book for book in BOOKS if book.start <= number and (book.end is None or number <= book.end)]
    if len(books) != 1:
        raise ValueError(f'chapter {number} belongs to {len(books)} Books')
    book = books[0]
    acts = [act for act in book.acts if act.start <= number and (act.end is None or number <= act.end)]
    if len(acts) != 1:
        raise ValueError(f'chapter {number} belongs to {len(acts)} Acts in {book.numeral}')
    return book, acts[0]


def _range_label(numbers: list[int], display_numbers: dict[int, int] | None, fallback: str) -> str:
    if not numbers or display_numbers is None:
        return fallback
    first = display_numbers[numbers[0]]
    last = display_numbers[numbers[-1]]
    return f'Chapters {first}–{last}'


def _render_act(
    act: ReaderAct,
    chapter_links: dict[int, str],
    latest: int,
    *,
    open_act: bool,
    display_numbers: dict[int, int] | None = None,
) -> str:
    end = act.effective_end(latest)
    if end < act.start:
        return ''
    visible_numbers = [n for n in range(act.start, end + 1) if n in chapter_links]
    links = [chapter_links[n] for n in visible_numbers]
    if not links:
        return ''
    range_label = _range_label(visible_numbers, display_numbers, act.range_label(latest))
    open_attr = ' open' if open_act else ''
    return (
        f'<details class="reader-act"{open_attr}>'
        f'<summary class="reader-act-summary">'
        f'<span class="reader-act-kicker">{escape(act.numeral)} · {escape(range_label)}</span>'
        f'<span class="reader-act-title">{escape(act.title)}</span>'
        f'</summary>'
        f'<p class="reader-act-deck">{escape(act.deck)}</p>'
        f'<div class="reader-act-grid">{"".join(links)}</div>'
        f'</details>'
    )


def render_book_sections(
    chapter_links: dict[int, str],
    *,
    illustrated: bool,
    open_first_act: bool = False,
    display_numbers: dict[int, int] | None = None,
) -> str:
    if not chapter_links:
        return ''

    latest = max(chapter_links)
    rendered: list[str] = []
    visible_books = [
        book for book in BOOKS
        if book.effective_end(latest) >= book.start
        and any(book.start <= n <= book.effective_end(latest) for n in chapter_links)
    ]

    for book_index, book in enumerate(visible_books):
        is_latest_book = book_index == len(visible_books) - 1
        acts: list[str] = []
        visible_acts = [act for act in book.acts if act.effective_end(latest) >= act.start]
        for act_index, act in enumerate(visible_acts):
            act_html = _render_act(
                act,
                chapter_links,
                latest,
                open_act=(is_latest_book and act_index == len(visible_acts) - 1) or (open_first_act and book_index == 0 and act_index == 0),
                display_numbers=display_numbers,
            )
            if act_html:
                acts.append(act_html)
        if not acts:
            continue

        book_end = book.effective_end(latest)
        book_visible_numbers = [
            n for n in chapter_links
            if book.start <= n <= book_end
        ]
        book_visible_numbers.sort()
        book_range_label = _range_label(book_visible_numbers, display_numbers, book.range_label(latest))

        plate = ''
        layout_class = ' reader-book-layout--illustrated' if illustrated else ''
        if illustrated and book.card_src:
            card_chapter = book.card_href.rsplit('/', 1)[-1].removesuffix('.html')
            plate = (
                f'<figure class="reader-book-plate">'
                f'<a class="reader-book-card-link" href="{escape(book.card_href)}" '
                f'aria-label="Open Chapter {escape(card_chapter)} in the Illustrated Reader">'
                f'<img class="reader-book-card-image" src="{escape(book.card_src)}" alt="{escape(book.card_alt)}" '
                f'width="720" height="960" loading="lazy" decoding="async">'
                f'</a></figure>'
            )

        open_attr = ' open' if is_latest_book else ''
        current_attr = ' aria-current="true"' if is_latest_book else ''
        rendered.append(
            f'<details class="reader-book"{open_attr}>'
            f'<summary class="reader-book-summary" id="{book.slug}-heading"{current_attr}>'
            f'<span class="reader-book-title">{escape(book.numeral)}</span>'
            f'<span class="reader-book-range">{escape(book_range_label)}</span>'
            f'</summary>'
            f'<div class="reader-book-layout{layout_class}">'
            f'{plate}<div class="reader-book-acts">{"".join(acts)}</div>'
            f'</div></details>'
        )

    return ''.join(rendered)


def render_act_details(
    chapter_links: dict[int, str],
    *,
    open_first: bool = False,
    display_numbers: dict[int, int] | None = None,
) -> str:
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
            display_numbers=display_numbers,
        )
        if not act_html:
            continue
        rendered.append(act_html)
        first_rendered = False
    return ''.join(rendered)
