from pathlib import Path
from html.parser import HTMLParser


class ImageCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.figures = []
        self.current_figure_classes = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "figure":
            self.current_figure_classes = attrs.get("class", "").split()
        elif tag == "img":
            self.figures.append((attrs.get("src"), list(self.current_figure_classes)))

    def handle_endtag(self, tag):
        if tag == "figure":
            self.current_figure_classes = []


ROOT = Path(__file__).resolve().parent
expected = {
    "010": ("../visual/chapter_art/010/v28_c10_feature_dead-mans-hand.png", "scene-illustration"),
    "024": ("../visual/chapter_art/024/v28_c24_feature_boat-on-the-road.png", "feature-illustration"),
    "027": ("../visual/chapter_art/027/v28_c27_feature_dyers-lane.png", "feature-illustration"),
}
for ch, (src, role) in expected.items():
    page = ROOT/"chapters"/f"{ch}.html"
    parser = ImageCollector()
    parser.feed(page.read_text(encoding="utf-8"))
    match = next((classes for image_src, classes in parser.figures if image_src == src), None)
    assert match is not None, f"{ch}: missing image reference {src}"
    assert role in match, f"{ch}: {role} class missing"
    asset = (page.parent/src).resolve()
    assert asset.exists(), f"{ch}: missing asset {asset}"
css=(ROOT/"assets"/"reader.css").read_text(encoding="utf-8")
for cls in ["sketch-beat","scene-illustration","feature-illustration"]:
    assert f".chapter-art.{cls}" in css, f"missing CSS role {cls}"
print("mixed-fidelity reader checks pass")
