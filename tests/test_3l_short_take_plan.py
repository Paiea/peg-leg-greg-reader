import unittest

from scripts.plan_3l_short_dual_render import classify_paragraphs, make_chunks


class ShortTakePlanTests(unittest.TestCase):
    def test_classifies_narration_and_cave_turns(self):
        text = '''The dragon did not move.\n\nEventually he said, “Not this time.”\n\n“Yes.”\n\n“You chose those words.”\n\n“I did.”\n\nIthar continued.\n\n“You are not merely carrying information that is old.”\n\nI looked at him.\n\n“That sounds complicated.”'''
        rows = classify_paragraphs(text)
        self.assertEqual(
            [row["role"] for row in rows],
            ["greg", "dragon", "greg", "dragon", "greg", "greg", "dragon", "greg", "greg"],
        )

    def test_chunker_preserves_text_and_limit(self):
        paragraphs = [
            {"role": "greg", "text": "A" * 220},
            {"role": "dragon", "text": "B" * 210},
            {"role": "greg", "text": "C" * 220},
        ]
        chunks = make_chunks(paragraphs, max_chars=500)
        self.assertEqual(len(chunks), 2)
        self.assertTrue(all(len(chunk["transcript"]) <= 500 for chunk in chunks))
        rebuilt = "\n\n".join(chunk["transcript"] for chunk in chunks)
        expected = "\n\n".join(item["text"] for item in paragraphs)
        self.assertEqual(rebuilt, expected)

    def test_chunk_contains_semantic_spans(self):
        paragraphs = [
            {"role": "greg", "text": "Narration."},
            {"role": "dragon", "text": "“No.”"},
            {"role": "greg", "text": "“Right.”"},
        ]
        chunks = make_chunks(paragraphs, max_chars=500)
        self.assertEqual(chunks[0]["roles"], ["greg", "dragon", "greg"])


if __name__ == "__main__":
    unittest.main()
