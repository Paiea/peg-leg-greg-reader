from pathlib import Path
import re
from html.parser import HTMLParser

ROOT = Path(__file__).parent
html = (ROOT/'index.html').read_text(encoding='utf-8')
css = (ROOT/'assets/reader.css').read_text(encoding='utf-8')

errors=[]

def expect(cond,msg):
    if not cond: errors.append(msg)

expect('class="home-hero"' in html, 'missing homepage hero')
expect('visual/homepage/peg-leg-greg-homepage-frontispiece.png' in html, 'homepage does not use dedicated high-resolution frontispiece')
expect('He got his life back.' in html, 'missing first-line hook')
expect('The world kept going.' in html, 'missing second-line hook')
expect(re.search(r'class="start[^\"]*" href="chapters/001\.html"', html) is not None, 'Begin Reading must link to chapter 1')
expect('href="#chapters"' in html, 'missing Chapter List jump link')
expect('href="art.html"' in html, 'missing Illustration Gallery link')
expect('id="chapters"' in html, 'chapter list needs an anchor id')
expect(len(re.findall(r'href="chapters/\d{3}\.html"', html)) == 124, 'expected 123 TOC links plus Begin Reading')
expect('href="chapters/123.html"' in html, 'chapter list must reach Chapter 123')
expect('@media (max-width:700px)' in css or '@media (max-width: 700px)' in css, 'missing narrow mobile breakpoint')
expect('min-height:44px' in css.replace(' ', '') or 'min-height:48px' in css.replace(' ', ''), 'homepage controls need phone-sized touch targets')
expect('.home-hero' in css, 'missing homepage hero styles')

if errors:
    print('FAIL')
    for e in errors: print('-', e)
    raise SystemExit(1)
print('PASS')
