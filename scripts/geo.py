#!/usr/bin/env python3
"""Great-circle distance between two (lat, lng) points, in kilometres.

The one interface for this in the codebase's Python side. Before this module,
the same haversine formula was pasted independently six times in scripts/
(with three drifted call signatures and two drifted units), plus four more
times on the TypeScript side (see site/src/lib/walks.ts::haversineKm for that
counterpart). Deepening candidate #1 from the 2026-08-13 architecture review:
https://github.com/burgmanshidde-ancienttrees/ancienttrees/issues/1
"""
import math

EARTH_RADIUS_KM = 6371.0


def km(a, b):
    """Distance between two (lat, lng) points, in kilometres."""
    lat1, lat2 = math.radians(a[0]), math.radians(b[0])
    dlat = math.radians(b[0] - a[0])
    dlng = math.radians(b[1] - a[1])
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng / 2) ** 2
    return 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(h))
