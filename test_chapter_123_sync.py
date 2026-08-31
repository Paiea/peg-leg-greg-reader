from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent


class LinkCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.links.append(href)


for chapter in range(106, 138):
    page = ROOT / "chapters" / f"{chapter:03}.html"
    assert page.exists(), f"missing Chapter {chapter} reader page"
    html = page.read_text(encoding="utf-8")
    assert f"CHAPTER {chapter}" in html, f"Chapter {chapter} number missing"

    parser = LinkCollector()
    parser.feed(html)
    assert f"{chapter - 1:03}.html" in parser.links, f"Chapter {chapter} missing previous navigation"
    if chapter < 137:
        assert f"{chapter + 1:03}.html" in parser.links, f"Chapter {chapter} missing next navigation"
    else:
        assert "138.html" not in parser.links, "Chapter 137 must be the published endpoint"

chapter_105 = (ROOT / "chapters" / "105.html").read_text(encoding="utf-8")
assert 'href="106.html"' in chapter_105, "Chapter 105 must link forward to Chapter 106"

print("Chapter 137 synchronization checks pass")
