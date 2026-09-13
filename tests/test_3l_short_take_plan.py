import unittest

from scripts.plan_3l_short_dual_render import (
    apply_quote_role_overrides,
    classify_paragraphs,
    extract_quote_inventory,
    make_chunks,
)


class ShortTakePlanTests(unittest.TestCase):
    def test_classifies_narration_and_cave_turns(self):
        text = '''The dragon did not move.\n\nEventually he said, “Not this time.”\n\n“Yes.”\n\n“You chose those words.”\n\n“I did.”\n\nIthar continued.\n\n“You are not merely carrying information that is old.”\n\nI looked at him.\n\n“That sounds complicated.”'''
        rows = classify_paragraphs(text)
        self.assertEqual(
            [row["role"] for row in rows],
            ["greg", "dragon", "greg", "dragon", "greg", "greg", "dragon", "greg", "greg"],
        )

    def test_sustained_dragon_quote_stays_one_contiguous_dragon_territory(self):
        text = '''I looked at him.\n\nThen the dragon took the floor.\n\n“First paragraph of Ithar's examination.\n\n“Second paragraph stays with Ithar.\n\n“Third paragraph closes the examination.”\n\nI rubbed my face.'''
        rows = classify_paragraphs(text)
        self.assertEqual(
            [row["role"] for row in rows],
            ["greg", "greg", "dragon", "dragon", "dragon", "greg"],
        )
        dragon_text = "\n\n".join(row["text"] for row in rows if row["role"] == "dragon")
        self.assertIn("First paragraph", dragon_text)
        self.assertIn("Second paragraph", dragon_text)
        self.assertIn("Third paragraph", dragon_text)

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

    def test_oversize_mixed_paragraph_preserves_semantic_speaker_spans(self):
        narration = "I watched the dragon for a long time. " * 8
        speech = "This is Ithar speaking at length about the shape of the problem. " * 5
        text = f'{narration}Ithar said, “{speech}”'
        rows = classify_paragraphs(text)
        chunks = make_chunks(rows, max_chars=220)
        self.assertTrue(all(chunk["char_count"] <= 220 for chunk in chunks))
        flattened = [span["role"] for chunk in chunks for span in chunk["semantic_spans"]]
        self.assertIn("greg", flattened)
        self.assertIn("dragon", flattened)
        rebuilt = "".join(chunk["transcript"] for chunk in chunks)
        self.assertEqual(rebuilt, text)

    def test_chunk_contains_semantic_spans(self):
        paragraphs = [
            {"role": "greg", "text": "Narration."},
            {"role": "dragon", "text": "“No.”"},
            {"role": "greg", "text": "“Right.”"},
        ]
        chunks = make_chunks(paragraphs, max_chars=500)
        self.assertEqual(chunks[0]["roles"], ["greg", "dragon", "greg"])

    def test_quote_inventory_uses_occurrence_ids(self):
        text = '“Yes.”\n\n“No.”\n\n“Yes.”'
        inventory = extract_quote_inventory(text)
        self.assertEqual([item["id"] for item in inventory], [1, 2, 3])
        self.assertEqual([item["text"] for item in inventory], ['“Yes.”', '“No.”', '“Yes.”'])

    def test_occurrence_override_changes_only_selected_quote(self):
        text = '“Yes.”\n\n“No.”\n\n“Yes.”'
        rows = classify_paragraphs(text)
        adjusted = apply_quote_role_overrides(rows, {1: "greg", 2: "dragon", 3: "dragon"})
        quote_roles = []
        for row in adjusted:
            quote_roles.extend(segment["role"] for segment in row["segments"] if segment["text"].startswith('“'))
        self.assertEqual(quote_roles, ["greg", "dragon", "dragon"])


if __name__ == "__main__":
    unittest.main()
