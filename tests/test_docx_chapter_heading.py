import unittest

from scripts.docx_chapter_heading import number_from_heading, words_to_number


class DocxChapterHeadingTests(unittest.TestCase):
    def test_numeric_heading(self):
        self.assertEqual(number_from_heading("CHAPTER 102"), 102)

    def test_spelled_hundred_heading(self):
        self.assertEqual(number_from_heading("CHAPTER ONE HUNDRED TWO"), 102)
        self.assertEqual(number_from_heading("CHAPTER ONE HUNDRED TWENTY-SIX"), 126)
        self.assertEqual(number_from_heading("CHAPTER ONE HUNDRED AND THIRTY-SEVEN"), 137)

    def test_combined_heading_ignores_title_line(self):
        self.assertEqual(number_from_heading("CHAPTER SIXTY-SIX\nTHE ABSENT"), 66)

    def test_non_heading(self):
        self.assertIsNone(number_from_heading("THE PIVOT"))
        self.assertIsNone(words_to_number("NOT A NUMBER"))


if __name__ == "__main__":
    unittest.main()
