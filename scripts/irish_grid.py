"""Irish Grid (TM75, Airy 1830 modified ellipsoid) -> WGS84-ish lat/lon.

Solves the blocker OPEN_DATA_SURVEY.md recorded on 2026-08-07: the Heritage
Trees of Ireland dataset (maps.biodiversityireland.ie/Dataset/27) publishes
East/North in Irish Grid metres, and this environment has no pyproj to
reproject them. This is the standard OS "Redfearn" inverse transverse
Mercator formula (the same one used for OSGB36), re-parameterised with the
Irish Grid's own ellipsoid, origin and false origin. It does NOT apply the
extra ~50-150m TM75-to-WGS84 Helmert shift (no dependency exists here to do
it properly), so treat output as approximate: fine for a location this
register itself records at 100m precision, and any tree pinned from this
module ships with location_precision "approximate" until confirmed another
way. Verified against a known landmark (Dublin GPO) and against three
register entries that already matched published, confirmed-pin trees
(Kings Inns' plane = dub_001 to within ~35m; two Trinity New Square planes
matched dub_006 to within ~40m) on 2026-08-08.
"""
import math


def irish_grid_to_latlon(easting, northing):
    a = 6377340.189
    b = 6356034.447
    f0 = 1.000035
    lat0 = math.radians(53.5)
    lon0 = math.radians(-8.0)
    n0 = 250000.0
    e0 = 200000.0
    e2 = 1 - (b * b) / (a * a)
    n = (a - b) / (a + b)
    n2, n3 = n * n, n * n * n

    lat = lat0
    m = 0.0
    for _ in range(50):
        lat = (northing - n0 - m) / (a * f0) + lat
        ma = (1 + n + 1.25 * n2 + 1.25 * n3) * (lat - lat0)
        mb = (3 * n + 3 * n2 + 2.625 * n3) * math.sin(lat - lat0) * math.cos(lat + lat0)
        mc = (1.875 * n2 + 1.875 * n3) * math.sin(2 * (lat - lat0)) * math.cos(2 * (lat + lat0))
        md = (35 / 24) * n3 * math.sin(3 * (lat - lat0)) * math.cos(3 * (lat + lat0))
        m = b * f0 * (ma - mb + mc - md)
        if abs(northing - n0 - m) < 0.00001:
            break

    cos_lat, sin_lat = math.cos(lat), math.sin(lat)
    nu = a * f0 / math.sqrt(1 - e2 * sin_lat * sin_lat)
    rho = a * f0 * (1 - e2) / ((1 - e2 * sin_lat * sin_lat) ** 1.5)
    eta2 = nu / rho - 1

    tan_lat = math.tan(lat)
    tan2, tan4, tan6 = tan_lat ** 2, tan_lat ** 4, tan_lat ** 6
    sec_lat = 1 / cos_lat
    nu3, nu5, nu7 = nu ** 3, nu ** 5, nu ** 7

    vii = tan_lat / (2 * rho * nu)
    viii = tan_lat / (24 * rho * nu3) * (5 + 3 * tan2 + eta2 - 9 * tan2 * eta2)
    ix = tan_lat / (720 * rho * nu5) * (61 + 90 * tan2 + 45 * tan4)
    x = sec_lat / nu
    xi = sec_lat / (6 * nu3) * (nu / rho + 2 * tan2)
    xii = sec_lat / (120 * nu5) * (5 + 28 * tan2 + 24 * tan4)
    xiia = sec_lat / (5040 * nu7) * (61 + 662 * tan2 + 1320 * tan4 + 720 * tan6)

    de = easting - e0
    lat_r = lat - vii * de ** 2 + viii * de ** 4 - ix * de ** 6
    lon_r = lon0 + x * de - xi * de ** 3 + xii * de ** 5 - xiia * de ** 7
    return round(math.degrees(lat_r), 5), round(math.degrees(lon_r), 5)


if __name__ == "__main__":
    print(irish_grid_to_latlon(315656, 234517))  # near Dublin GPO
