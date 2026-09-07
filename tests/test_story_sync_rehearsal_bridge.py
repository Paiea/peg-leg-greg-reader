import unittest

from scripts import story_sync_engine as sync


class StorySyncRehearsalBridgeTests(unittest.TestCase):
    def test_rehearsal_discovery_becomes_one_support_item_not_story_truth(self):
        rehearsal_discovery = {
            "scene_id": "ds.act-i.first-negotiation",
            "kind": "behavioral_discovery",
            "finding": "The fraud gets more effective when he stops imitating formal dragon protocol.",
            "provenance_class": "rehearsal_hypothesis",
            "dramatic_lock_status": "preserved",
            "support": ["take-1", "take-2"],
        }
        evidence = sync.rehearsal_evidence(
            rehearsal_discovery,
            independent_group="first-negotiation-variance-a",
            dramatic_uses=["character", "plot"],
            regions=["act-i"],
        )
        self.assertEqual("support", evidence["kind"])
        self.assertEqual("first-negotiation-variance-a", evidence["independent_group"])
        discovery = {"id": "fraud-improvisation", "finding": rehearsal_discovery["finding"], "evidence": [evidence]}
        self.assertEqual("speculation", sync.classify_discovery(discovery))

    def test_rehearsal_with_violated_dramatic_lock_enters_as_contradiction_evidence(self):
        rehearsal_discovery = {
            "scene_id": "ds.act-ii.bad-take",
            "kind": "relationship_behavior",
            "finding": "The scholar suddenly trusts him completely.",
            "provenance_class": "rehearsal_hypothesis",
            "dramatic_lock_status": "violated",
            "support": ["take-bad"],
        }
        evidence = sync.rehearsal_evidence(
            rehearsal_discovery,
            independent_group="bad-take",
            dramatic_uses=["relationship"],
            regions=["act-ii"],
        )
        self.assertEqual("contradiction", evidence["kind"])


if __name__ == "__main__":
    unittest.main()
