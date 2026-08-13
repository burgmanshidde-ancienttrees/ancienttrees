#!/usr/bin/env python3
"""Unit tests for scripts/geo.py.

    python3 scripts/test_geo.py
    python3 -m unittest scripts.test_geo -v
"""
import math
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import km  # noqa: E402

EARTH_RADIUS_KM = 6371.0


class TestKm(unittest.TestCase):
    def test_same_point_is_zero(self):
        self.assertEqual(km((51.5074, -0.1278), (51.5074, -0.1278)), 0.0)

    def test_quarter_meridian(self):
        # 90 degrees of latitude, same longitude: exactly a quarter of the
        # sphere's circumference. Derived independently of the haversine
        # implementation, so this catches a wrong radius or a wrong angle unit.
        expected = math.pi * EARTH_RADIUS_KM / 2
        got = km((0.0, 0.0), (90.0, 0.0))
        self.assertAlmostEqual(got, expected, places=3)

    def test_antipodal_is_half_circumference(self):
        expected = math.pi * EARTH_RADIUS_KM
        got = km((10.0, 20.0), (-10.0, -160.0))
        self.assertAlmostEqual(got, expected, places=3)

    def test_symmetric(self):
        amsterdam, paris = (52.3676, 4.9041), (48.8566, 2.3522)
        self.assertAlmostEqual(km(amsterdam, paris), km(paris, amsterdam), places=9)

    def test_known_real_world_distance(self):
        # Amsterdam to Paris: commonly cited great-circle distance is ~430 km.
        amsterdam = (52.3676, 4.9041)
        paris = (48.8566, 2.3522)
        got = km(amsterdam, paris)
        self.assertGreater(got, 420)
        self.assertLess(got, 440)


if __name__ == "__main__":
    unittest.main()
