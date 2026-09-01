#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

START = '/* READER ACT CONTENTS + DESKTOP ART CAPS — managed by update_reader_presentation.py */'
END = '/* END READER ACT CONTENTS + DESKTOP ART CAPS */'

BLOCK = f'''{START}
.toc.toc-acts {{
  margin-top:0;
  border-top:0;
}}
.reader-book {{
  margin:42px 0 72px;
}}
.reader-book + .reader-book {{
  margin-top:84px;
  padding-top:46px;
  border-top:1px solid var(--line);
}}
.reader-book-intro {{
  display:grid;
  grid-template-columns:minmax(240px,320px) minmax(0,1fr);
  grid-template-rows:auto auto 1fr;
  column-gap:30px;
  align-items:start;
  margin-bottom:24px;
}}
.reader-book-kicker {{
  grid-column:2;
  grid-row:1;
  display:block;
  margin-bottom:8px;
  color:var(--muted);
  font:700 .7rem/1.35 ui-sans-serif,system-ui,sans-serif;
  letter-spacing:.17em;
  text-transform:uppercase;
}}
.reader-book-title {{
  grid-column:2;
  grid-row:2;
  margin:0;
  font-size:clamp(2rem,4vw,3rem);
  line-height:1;
  letter-spacing:-.035em;
}}
.reader-book-deck {{
  grid-column:2;
  grid-row:3;
  max-width:42rem;
  margin:12px 0 0;
  color:var(--muted);
  font-size:1rem;
  line-height:1.6;
}}
.reader-book-hero {{
  grid-column:1;
  grid-row:1 / span 3;
  width:min(100%,320px);
  aspect-ratio:4 / 5;
  margin:0;
  overflow:hidden;
  border:1px solid var(--line);
  border-radius:6px;
  background:color-mix(in srgb,var(--paper) 86%,var(--ink));
  box-shadow:0 10px 28px color-mix(in srgb,var(--ink) 10%,transparent);
}}
.reader-book-hero img {{
  display:block;
  width:100%;
  height:100%;
  object-fit:cover;
}}
.reader-act {{
  border-top:1px solid var(--line);
}}
.reader-book > .reader-act:last-child {{
  border-bottom:1px solid var(--line);
}}
.reader-act-summary {{
  position:relative;
  display:grid;
  gap:.35rem;
  padding:24px 42px 22px 0;
  cursor:pointer;
  list-style:none;
}}
.reader-act-summary::-webkit-details-marker {{ display:none; }}
.reader-act-summary::after {{
  content:'+';
  position:absolute;
  right:4px;
  top:50%;
  transform:translateY(-50%);
  color:var(--muted);
  font:500 1.35rem/1 ui-sans-serif,system-ui,sans-serif;
}}
.reader-act[open] > .reader-act-summary::after {{ content:'–'; }}
.reader-act-kicker {{
  color:var(--muted);
  font:700 .67rem/1.35 ui-sans-serif,system-ui,sans-serif;
  letter-spacing:.16em;
  text-transform:uppercase;
}}
.reader-act-title {{
  font-size:clamp(1.55rem,3vw,2.2rem);
  line-height:1.05;
  letter-spacing:-.025em;
}}
.reader-act-deck {{
  max-width:35rem;
  margin:-4px 0 20px;
  color:var(--muted);
  font-size:.95rem;
  line-height:1.55;
}}
.reader-act-grid {{
  display:grid;
  grid-template-columns:repeat(2,minmax(0,1fr));
  column-gap:30px;
  padding:0 0 28px;
}}
.toc .reader-act-grid a,
.light-ranges .reader-act-grid a {{
  display:grid;
  grid-template-columns:52px minmax(0,1fr);
  gap:10px;
  min-height:48px;
  align-items:center;
  padding:12px 0;
  border-bottom:1px solid color-mix(in srgb,var(--line) 72%,transparent);
  text-decoration:none;
  color:inherit;
}}
.light-ranges .reader-book {{
  margin-top:36px;
}}
.light-ranges .reader-book + .reader-book {{
  margin-top:60px;
  padding-top:34px;
}}
.light-ranges .reader-book-intro {{
  display:block;
}}
.light-ranges .reader-book-kicker,
.light-ranges .reader-book-title,
.light-ranges .reader-book-deck {{
  display:block;
}}
.light-ranges .reader-act {{
  border-color:var(--line);
}}
.light-ranges .reader-act-summary {{
  padding-left:2px;
}}
.light-ranges .reader-act-grid .num,
.toc .reader-act-grid .num {{
  color:var(--muted);
  font:700 .7rem/1 ui-sans-serif,system-ui,sans-serif;
  letter-spacing:.08em;
}}
.light-ranges .reader-act-grid .title,
.toc .reader-act-grid .title {{
  font-size:.98rem;
}}
.reader-act-summary:focus-visible {{
  outline:3px solid var(--link);
  outline-offset:4px;
}}

@media (max-width:700px) {{
  .reader-book {{ margin:34px 0 54px; }}
  .reader-book + .reader-book {{ margin-top:58px; padding-top:34px; }}
  .reader-book-intro {{ display:flex; flex-direction:column; margin-bottom:18px; }}
  .reader-book-hero {{ order:-1; width:min(82%,320px); aspect-ratio:4 / 5; margin:0 auto 20px; border-radius:5px; }}
  .reader-book-kicker {{ margin-bottom:7px; }}
  .reader-book-title {{ font-size:2rem; }}
  .reader-book-deck {{ font-size:.94rem; }}
  .reader-act-summary {{ padding:20px 38px 18px 0; }}
  .reader-act-title {{ font-size:1.55rem; }}
  .reader-act-deck {{ margin-bottom:14px; font-size:.92rem; }}
  .reader-act-grid {{ grid-template-columns:1fr; column-gap:0; padding-bottom:20px; }}
  .toc .reader-act-grid a,
  .light-ranges .reader-act-grid a {{ grid-template-columns:46px minmax(0,1fr); }}
}}

/* Desktop only: low-fidelity art should never become an IMAX wall. */
@media (min-width:601px) {{
  .chapter-art img {{
    width:auto;
    max-width:min(820px, calc(100vw - 48px));
  }}
  .chapter-art.sketch-beat img {{
    max-width:min(560px, calc(100vw - 48px));
  }}
  .chapter-art.scene-illustration img {{
    width:auto;
    max-width:min(820px, calc(100vw - 48px));
  }}
  .chapter-art.feature-illustration img {{
    width:auto;
    max-width:min(1180px, calc(100vw - 48px));
  }}
  .chapter-art.feature-illustration.feature-portrait img {{
    width:auto;
    max-width:min(720px, calc(100vw - 48px));
  }}
}}
{END}'''


def patch_css(path: Path) -> bool:
    original = path.read_text(encoding='utf-8')
    if START in original and END in original:
        before, rest = original.split(START, 1)
        _, after = rest.split(END, 1)
        updated = before.rstrip() + '\n\n' + BLOCK + after
    else:
        updated = original.rstrip() + '\n\n' + BLOCK + '\n'
    if updated == original:
        return False
    path.write_text(updated, encoding='utf-8')
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description='Materialize shared book/Act styling and desktop illustration caps.')
    parser.add_argument('css', nargs='?', default='assets/reader.css')
    args = parser.parse_args()
    changed = patch_css(Path(args.css))
    print('updated reader presentation css' if changed else 'reader presentation css already current')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
