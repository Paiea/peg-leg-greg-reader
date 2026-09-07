import unittest

from scripts import performance_campaign


class PerformanceSpeakerOwnershipTests(unittest.TestCase):
    def test_reverse_edit_prompt_requires_speaker_ownership_audit(self):
        packet = {
            "scene_id": "001.s010",
            "task": "reverse_edit",
            "view": "comparison",
            "source_hash": "abc",
            "write_authority": "derived_only",
        }
        scene = {
            "scene_id": "001.s010",
            "source": {
                "hash": "abc",
                "paragraphs": [
                    "\u201cYou coming?\u201d",
                    "Greg looked at Sera.",
                    "\u201cMaybe.\u201d",
                ],
            },
            "mechanical": {},
            "dependencies": {},
        }

        prompt = performance_campaign.build_worker_prompt(packet, scene)

        self.assertIn("speaker ownership", prompt.lower())
        self.assertIn("screenplay", prompt.lower())
        self.assertIn("three or more speakers", prompt.lower())
        self.assertIn("another character's action", prompt.lower())
        self.assertIn("said/asked", prompt.lower())
        self.assertIn("preserve clean two-person alternation", prompt.lower())

    def test_non_reverse_edit_prompt_does_not_add_prose_attribution_policy(self):
        packet = {
            "scene_id": "001.s010",
            "task": "performance",
            "view": "performance",
            "source_hash": "abc",
            "write_authority": "derived_only",
        }
        scene = {
            "scene_id": "001.s010",
            "source": {"hash": "abc", "paragraphs": []},
            "mechanical": {},
            "dependencies": {},
        }

        prompt = performance_campaign.build_worker_prompt(packet, scene)

        self.assertNotIn("speaker ownership audit", prompt.lower())
        self.assertNotIn("said/asked", prompt.lower())


if __name__ == "__main__":
    unittest.main()
