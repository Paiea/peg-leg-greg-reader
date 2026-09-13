import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


class ThirdLegSiteTests(unittest.TestCase):
    def test_site_files_and_identity(self):
        home = ROOT / "3l" / "index.html"
        css = ROOT / "3l" / "assets" / "css" / "site.css"
        record_css = ROOT / "3l" / "assets" / "css" / "record.css"
        record = ROOT / "3l" / "records" / "001.html"
        records = ROOT / "3l" / "records" / "index.html"
        audio = ROOT / "3l" / "audio" / "index.html"
        about = ROOT / "3l" / "about" / "index.html"
        hero = ROOT / "3l" / "assets" / "images" / "hero" / "dragon-bargain.png"
        audio_art = ROOT / "3l" / "assets" / "images" / "audio" / "audio-library.png"
        manuscript = ROOT / "3l" / "manuscript" / "record-001.md"
        for path in (home, css, record_css, record, records, audio, about, hero, audio_art, manuscript):
            self.assertTrue(path.exists(), path)

        html = home.read_text(encoding="utf-8")
        styles = css.read_text(encoding="utf-8")
        self.assertIn("THE THIRD LEG", html)
        self.assertIn("A Record of Two Lives", html)
        self.assertIn("BEGIN THE ACCOUNT", html)
        self.assertIn("THE PETITIONER", html)
        self.assertIn("He came to ask something of a dragon.", html)
        self.assertIn("The price was an explanation.", html)
        self.assertIn('class="entry-panel"', html)
        self.assertIn('class="listening-feature"', html)
        self.assertIn('class="written-reference"', html)
        self.assertIn('class="lineage-strip"', html)
        self.assertNotIn('class="story-grid"', html)
        self.assertIn('href="records/001.html"', html)
        self.assertIn('href="audio/"', html)
        self.assertIn('href="records/"', html)
        self.assertIn('href="about/"', html)
        self.assertIn('href="#timeline"', html)
        self.assertIn('class="skip-link"', html)
        self.assertIn("dragon-bargain.png", styles)
        self.assertIn("../images/audio/audio-library.png", styles)
        self.assertIn("@media (max-width: 760px)", styles)
        self.assertIn(":focus-visible", styles)
        self.assertNotIn("R3", html)
        self.assertNotIn("autoplay", html.lower())

    def test_r2_routes_forward_to_the_third_leg(self):
        r2_home = (ROOT / "r2" / "index.html").read_text(encoding="utf-8")
        self.assertIn("The Third Leg", r2_home)
        self.assertIn('href="../3l/"', r2_home)
        self.assertNotIn(">R3<", r2_home)

    def test_record_001_is_published_with_prose_and_voice_entry(self):
        record = (ROOT / "3l" / "records" / "001.html").read_text(encoding="utf-8")
        manuscript = (ROOT / "3l" / "manuscript" / "record-001.md").read_text(encoding="utf-8")
        audio = (ROOT / "3l" / "audio" / "index.html").read_text(encoding="utf-8")
        records = (ROOT / "3l" / "records" / "index.html").read_text(encoding="utf-8")

        self.assertIn("RECORD 001", record)
        self.assertIn("THE PETITIONER", record)
        self.assertIn('id="listen"', record)
        self.assertIn('id="read"', record)
        self.assertIn("record-001.md", record)
        self.assertIn("a2af6461-e2f2-48e1-9573-b1c07fff2396.mp3", record)
        self.assertIn("d53f086b9a64427ba8aa22ca77580def", record)
        self.assertNotIn("The account is being prepared.", record)

        self.assertIn("The dragon yawns while I am explaining how many people are going to die.", manuscript)
        self.assertTrue(manuscript.rstrip().endswith("“Not this time.”"))

        self.assertIn("RECORD 001", audio)
        self.assertIn("THE PETITIONER", audio)
        self.assertIn("Play Full Record", audio)
        self.assertNotIn("No audio records have been published yet.", audio)

        self.assertIn("THE PETITIONER", records)
        self.assertNotIn("Publication pending", records)


if __name__ == "__main__":
    unittest.main()
