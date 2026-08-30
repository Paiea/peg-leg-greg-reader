from pathlib import Path
from bs4 import BeautifulSoup
ROOT = Path(__file__).resolve().parent
expected = {
    "010": ("../visual/chapter_art/010/v28_c10_feature_dead-mans-hand.png", "scene-illustration"),
    "024": ("../visual/chapter_art/024/v28_c24_feature_boat-on-the-road.png", "feature-illustration"),
    "027": ("../visual/chapter_art/027/v28_c27_feature_dyers-lane.png", "feature-illustration"),
}
for ch, (src, role) in expected.items():
    page = ROOT/"chapters"/f"{ch}.html"
    soup = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
    img = soup.find("img", src=src)
    assert img is not None, f"{ch}: missing image reference {src}"
    fig = img.find_parent("figure")
    assert fig and role in fig.get("class", []), f"{ch}: {role} class missing"
    asset = (page.parent/src).resolve()
    assert asset.exists(), f"{ch}: missing asset {asset}"
css=(ROOT/"assets"/"reader.css").read_text(encoding="utf-8")
for cls in ["sketch-beat","scene-illustration","feature-illustration"]:
    assert f".chapter-art.{cls}" in css, f"missing CSS role {cls}"
print("mixed-fidelity reader checks pass")
