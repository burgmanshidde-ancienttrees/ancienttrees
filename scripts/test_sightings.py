#!/usr/bin/env python3
"""Unit tests for the reader-photograph loop: matching and the photo block.

    python3 scripts/test_sightings.py
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sightings_inbox as inbox  # noqa: E402
import sightings_publish as pub  # noqa: E402

INDEX = {
    "ams_001": {"slug": "amsterdam", "city": "Amsterdam", "name": "The Wertheimpark Wingnut",
                "lat": 52.3670, "lng": 4.9050, "photo_status": "none", "photo_source": None, "path": ""},
    "ams_002": {"slug": "amsterdam", "city": "Amsterdam", "name": "Another tree",
                "lat": 52.3700, "lng": 4.9100, "photo_status": "approved", "photo_source": None, "path": ""},
}


class TestMatch(unittest.TestCase):
    def test_app_tree_id_wins_even_when_gps_is_off(self):
        tid, how, d = inbox.match({"tree_id": "ams_002", "lat": 52.3670, "lng": 4.9050}, INDEX)
        self.assertEqual((tid, how), ("ams_002", "app"))
        self.assertGreater(d, 100)

    def test_unknown_tree_id_falls_through_to_distance(self):
        tid, how, d = inbox.match({"tree_id": "gone_999", "lat": 52.36701, "lng": 4.90501}, INDEX)
        self.assertEqual((tid, how), ("ams_001", "distance"))
        self.assertLessEqual(d, inbox.MATCH_M)

    def test_nearest_within_threshold(self):
        tid, how, d = inbox.match({"tree_id": None, "lat": 52.36715, "lng": 4.90510}, INDEX)
        self.assertEqual((tid, how), ("ams_001", "distance"))

    def test_too_far_is_a_lead_not_a_guess(self):
        tid, how, d = inbox.match({"tree_id": None, "lat": 52.3690, "lng": 4.9050}, INDEX)
        self.assertEqual((tid, how), (None, "none"))
        self.assertGreater(d, inbox.MATCH_M)

    def test_no_coordinates(self):
        self.assertEqual(inbox.match({"tree_id": None, "lat": None, "lng": None}, INDEX), (None, "none", None))


class TestPhotoBlock(unittest.TestCase):
    ENTRY = {"sighting_id": "abc-123", "user_id": "u-1", "display_name": "Katy",
             "tree_id": "ams_001", "tree_name": "The Wertheimpark Wingnut",
             "city_slug": "amsterdam", "city": "Amsterdam", "taken_at": "2026-09-03T10:00:00Z"}

    def test_block_carries_both_takedown_fields(self):
        b = pub.photo_block(self.ENTRY, 1200, 1600, "good frame", "2026-09-04")
        self.assertEqual(b["source"], "contributor")
        self.assertEqual(b["contributor_user_id"], "u-1")
        self.assertEqual(b["status"], "approved")
        self.assertEqual((b["width"], b["height"]), (1200, 1600))

    def test_an_extras_url_follows_its_own_file(self):
        """An `add` verdict writes the file under a name carrying the sighting
        id so it cannot overwrite the lead; the url has to point at THAT file.
        It used to point at the lead's, apply_to_city's duplicate check dropped
        the extra, and the orphaned file failed QA and was deleted: the Paris
        Turkey Oak close-up a reader sent on 2026-10-01 was lost that way."""
        lead = pub.photo_block(self.ENTRY, 1, 1, "", "2026-10-02")
        extra = pub.photo_block(self.ENTRY, 1, 1, "", "2026-10-02",
                                fname="ams_001-the-wertheimpark-wingnut-abc-123.jpg")
        self.assertTrue(extra["url"].endswith("/photos/ams_001-the-wertheimpark-wingnut-abc-123.jpg"))
        self.assertNotEqual(extra["url"], lead["url"])

    def test_no_name_is_printed_beside_a_readers_photograph(self):
        """Hidde, 2026-09-04: "laten we niet mensen hun naam noemen, laten we
        alleen hun fotos gebruiken als ze goed zijn, het kan mensen afschrikken
        als hun naam erbij staat."

        These two tests asserted the OPPOSITE until 2026-09-08, because they
        were written the day before that ruling and nothing failed loudly
        enough to get them read: they had been red for four days. A red test
        nobody fixes is a gate nobody has, which is the same lesson this
        project already recorded about ios.yml.
        """
        b = pub.photo_block(self.ENTRY, 1, 1, "", "2026-09-04")
        self.assertIsNone(b["attribution"])
        self.assertTrue(b["license"].lower().startswith("provided by"))
        self.assertNotIn("Katy", json_dump(b))
        self.assertNotIn("@", json_dump(b))

    def test_the_account_id_travels_even_though_the_name_does_not(self):
        """The id is the whole of the deletion promise in /terms: a published
        photograph is a copy no database cascade reaches, so photo_takedown.py
        needs something to ask Supabase about. Preflight refuses one without
        the other in either direction."""
        b = pub.photo_block(dict(self.ENTRY, display_name=""), 1, 1, "", "2026-09-04")
        self.assertEqual(b["source"], "contributor")
        self.assertTrue(b["contributor_user_id"])
        self.assertIsNone(b["attribution"])

    def test_url_is_ours_and_named_after_the_tree(self):
        b = pub.photo_block(self.ENTRY, 1, 1, "", "2026-09-04")
        self.assertEqual(b["url"], "https://ancienttrees.app/photos/ams_001-the-wertheimpark-wingnut.jpg")


def json_dump(o):
    import json
    return json.dumps(o)


class TestReaderPin(unittest.TestCase):
    """A reader's accepted fix replaces an approximate pin, never a confirmed one."""

    def tree(self, precision="approximate", lat=64.1474, lon=-21.9418):
        return {"id": "rey_001", "location_precision": precision,
                "location": {"latitude": lat, "longitude": lon}}

    def test_approximate_moves_and_becomes_confirmed(self):
        t = self.tree()
        line = pub.move_pin(t, 64.1474222, -21.9420133, "sid", "2026-09-04T15:45:35Z", "2026-10-05")
        self.assertTrue(line.startswith("PIN "))
        self.assertEqual(t["location"]["latitude"], 64.147422)
        self.assertEqual(t["location_precision"], "confirmed")
        self.assertEqual(t["pin_source"]["sighting_id"], "sid")
        self.assertEqual(t["pin_source"]["moved_m"], 11)

    def test_confirmed_is_never_touched(self):
        t = self.tree("confirmed")
        self.assertIsNone(pub.move_pin(t, 64.1475, -21.9420, "sid", None, "2026-10-05"))
        self.assertEqual(t["location"]["latitude"], 64.1474)
        self.assertNotIn("pin_source", t)

    def test_too_far_is_reported_not_applied(self):
        t = self.tree()
        line = pub.move_pin(t, 64.1600, -21.9418, "sid", None, "2026-10-05")
        self.assertTrue(line.startswith("NOT MOVED"))
        self.assertEqual(t["location_precision"], "approximate")
        self.assertEqual(t["location"]["latitude"], 64.1474)

    def test_no_fix_no_change(self):
        t = self.tree()
        self.assertIsNone(pub.move_pin(t, None, None, "sid", None, "2026-10-05"))


if __name__ == "__main__":
    unittest.main()
