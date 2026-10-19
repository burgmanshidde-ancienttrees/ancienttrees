#!/usr/bin/env python3
"""Account codes keep the account-deletion promise (privacy audit, 2026-10-19).

The public files hold people.ref(uid) instead of the id. The one thing that
must not break is /terms' promise: when an account is deleted, its photographs
and leads are unlinked within a day. These tests run photo_takedown on a copy
of the files with a made-up account list, so nothing real is touched.

    python3 scripts/test_people.py
"""
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import people  # noqa: E402
import photo_takedown  # noqa: E402

KEY = "test-service-key"
STAYS = "11111111-1111-1111-1111-111111111111"
GOES = "22222222-2222-2222-2222-222222222222"


class Codes(unittest.TestCase):
    def test_code_is_stable_and_hides_the_id(self):
        a, b = people.ref(STAYS, KEY), people.ref(STAYS, KEY)
        self.assertEqual(a, b)
        self.assertTrue(people.is_ref(a))
        self.assertNotIn(STAYS[:8], a)
        self.assertNotEqual(a, people.ref(GOES, KEY))

    def test_a_code_passes_through(self):
        c = people.ref(STAYS, KEY)
        self.assertEqual(people.ref(c, KEY), c)

    def test_a_different_key_gives_a_different_code(self):
        self.assertNotEqual(people.ref(STAYS, KEY), people.ref(STAYS, "another-key"))


class Takedown(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = self.tmp.name
        os.makedirs(os.path.join(root, "data", "cities"))
        os.makedirs(os.path.join(root, "data", "leads"))
        self.stays, self.goes = people.ref(STAYS, KEY), people.ref(GOES, KEY)

        def photo(code):
            return {"url": "https://ancienttrees.app/photos/x.jpg", "source": "contributor",
                    "contributor_user_id": code, "attribution": "Somebody", "status": "approved"}

        city = {"city": "Testtown", "trees": [
            {"id": "tst_001", "name": "Kept", "photo": photo(self.stays)},
            {"id": "tst_002", "name": "Unlinked", "photo": photo(self.goes),
             "photos": [photo(self.stays)]},
        ]}
        with open(os.path.join(root, "data", "cities", "testtown.json"), "w") as fh:
            json.dump(city, fh)
        leads = {"leads": [{"sighting_id": "s1", "user_id": self.goes},
                           {"sighting_id": "s2", "user_id": self.stays}]}
        with open(os.path.join(root, "data", "leads", "_sightings.json"), "w") as fh:
            json.dump(leads, fh)
        self._root, self._key, self._acc = photo_takedown.ROOT, photo_takedown.KEY, people._ACCOUNTS
        photo_takedown.ROOT, photo_takedown.KEY = root, "set"
        # The account list as Supabase would give it: STAYS exists, GOES was deleted.
        people._ACCOUNTS = {self.stays: STAYS}

    def tearDown(self):
        photo_takedown.ROOT, photo_takedown.KEY, people._ACCOUNTS = self._root, self._key, self._acc
        self.tmp.cleanup()

    def run_sweep(self, *args):
        old = sys.argv
        sys.argv = ["photo_takedown.py", *args]
        try:
            return photo_takedown.main()
        finally:
            sys.argv = old

    def read(self, *parts):
        with open(os.path.join(self.tmp.name, *parts)) as fh:
            return json.load(fh)

    def test_check_sees_the_deleted_account(self):
        self.assertEqual(self.run_sweep("--check"), 1)

    def test_sweep_unlinks_only_the_deleted_account(self):
        self.run_sweep()
        trees = {t["id"]: t for t in self.read("data", "cities", "testtown.json")["trees"]}
        gone = trees["tst_002"]["photo"]
        self.assertNotIn("contributor_user_id", gone)
        self.assertTrue(gone.get("unlinked"))
        self.assertEqual(gone["attribution"], photo_takedown.ANON_CREDIT)
        self.assertEqual(trees["tst_001"]["photo"]["contributor_user_id"], self.stays)
        self.assertEqual(trees["tst_002"]["photos"][0]["contributor_user_id"], self.stays)
        leads = {l["sighting_id"]: l for l in self.read("data", "leads", "_sightings.json")["leads"]}
        self.assertNotIn("user_id", leads["s1"])
        self.assertEqual(leads["s2"]["user_id"], self.stays)
        self.assertEqual(self.run_sweep("--check"), 0)

    def test_an_unreadable_account_list_unlinks_nothing(self):
        people._ACCOUNTS = None
        orig = people.accounts
        people.accounts = lambda: None
        try:
            self.run_sweep()
        finally:
            people.accounts = orig
        trees = {t["id"]: t for t in self.read("data", "cities", "testtown.json")["trees"]}
        self.assertEqual(trees["tst_002"]["photo"]["contributor_user_id"], self.goes)


if __name__ == "__main__":
    unittest.main(verbosity=2)
