import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


class ThirdLegSiteTests(unittest.TestCase):
    def test_site_files_and_identity(self):
        home = ROOT / "3l" / "index.html"
        css = ROOT / "3l" / "assets" / "css" / "site.css"
        record = ROOT / "3l" / "records" / "001.html"
        records = ROOT / "3l" / "records" / "index.html"
        audio = ROOT / "3l" / "audio" / "index.html"
        about = ROOT / "3l" / "about" / "index.html"
        for path in (home, css, record, records, audio, about):
            self.assertTrue(path.exists(), path)

        html = home.read_text(encoding="utf-8")
        styles = css.read_text(encoding="utf-8")
        self.assertIn("THE THIRD LEG", html)
        self.assertIn("A Record of Two Lives", html)
        self.assertIn("BEGIN THE ACCOUNT", html)
        self.assertIn("THE BARGAINER", html)
        self.assertIn("He came to ask something of a dragon.", html)
        self.assertIn("The price was an explanation.", html)
        self.assertIn('href="records/001.html"', html)
        self.assertIn('href="audio/"', html)
        self.assertIn('href="records/"', html)
        self.assertIn('href="about/"', html)
        self.assertIn('href="#timeline"', html)
        self.assertIn('class="skip-link"', html)
        self.assertIn("dragon-bargain.png", styles)
        self.assertIn("audio-library.png", styles)
        self.assertIn("@media (max-width: 760px)", styles)
        self.assertIn(":focus-visible", styles)
        self.assertNotIn("R3", html)
        self.assertNotIn("autoplay", html.lower())

    def test_record_and_audio_shells_are_safe_before_content_exists(self):
        record = (ROOT / "3l" / "records" / "001.html").read_text(encoding="utf-8")
        audio = (ROOT / "3l" / "audio" / "index.html").read_text(encoding="utf-8")
        self.assertIn("RECORD 001", record)
        self.assertIn("THE BARGAINER", record)
        self.assertIn("The account is being prepared.", record)
        self.assertIn("LISTENING ARCHIVE", audio)
        self.assertIn("No audio records have been published yet.", audio)


if __name__ == "__main__":
    unittest.main()
