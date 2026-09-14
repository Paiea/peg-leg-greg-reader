import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "3l" / "manuscript"

CHECKPOINT_MARKERS = {
    "002": "Then the dragon took the floor.",
    "003": "The answer came as a territory, not a word.",
    "004": "You woke with forty years of knowledge and treated the second life as a chance to perform the first more efficiently.",
    "005": "You describe East Four as a detour because that is how you protected the decision from becoming a decision.",
    "006": "You said the contract was four weeks. You remained at East Four for eleven years.",
    "007": "You remember those names because in the first history they died and in the second they did not.",
    "008": "You knew Nessa Vale first as a name on a board of dead people.",
    "009": "You have given me several reasons without giving me the decision beneath them.",
    "010": "You never told Bren. You had information about him and chose not to use it.",
}


class DialogueTerritoryTests(unittest.TestCase):
    def test_every_record_has_its_deliberate_ithar_checkpoint(self):
        for record, marker in CHECKPOINT_MARKERS.items():
            with self.subTest(record=record):
                text = (MANUSCRIPT / f"record-{record}.md").read_text(encoding="utf-8")
                self.assertIn(marker, text)

    def test_records_004_and_005_are_no_longer_dragon_free(self):
        for record in ("004", "005"):
            with self.subTest(record=record):
                text = (MANUSCRIPT / f"record-{record}.md").read_text(encoding="utf-8")
                self.assertIn("Ithar", text)


if __name__ == "__main__":
    unittest.main()
