#!/usr/bin/env python3
"""Minimal pure-stdlib reader for point shapefiles, plus UTM to WGS84.

Spain's regional tree registers ship as shapefiles rather than GeoJSON:
Navarra, Castilla y Leon and Aragon between them, so one reader unlocks three.
No third-party dependency (pyshp, geopandas and pyproj are not installed and
do not need to be), same reasoning as scripts/xls_parser.py.

Handles what a tree register actually contains and nothing else: point
geometry (shape types 1, 11 and 21), the dBase III attribute table beside it,
and the inverse UTM projection those files are usually written in. Lines,
polygons, multipoint and M/Z arrays are refused loudly rather than guessed at.

    from shapefile_reader import read_points, utm_to_wgs84
    rows = read_points("BIODIV.shp", "BIODIV.dbf")   # [{"lat":..,"lng":..,**attrs}]
"""
import math
import struct

POINT_TYPES = {1, 11, 21}


def read_dbf(data):
    """dBase III table to a list of dicts. Field values come back as trimmed
    strings; a register's numbers are small enough that callers can convert
    the two or three they care about."""
    if len(data) < 32:
        return []
    num_records, header_len, record_len = struct.unpack_from("<IHH", data, 4)
    fields = []
    pos = 32
    while pos < header_len - 1 and data[pos] != 0x0D:
        name = data[pos:pos + 11].split(b"\x00")[0].decode("latin-1").strip()
        length = data[pos + 16]
        fields.append((name, length))
        pos += 32
    rows = []
    start = header_len
    for i in range(num_records):
        base = start + i * record_len
        if base + record_len > len(data):
            break
        if data[base:base + 1] == b"*":  # deleted
            continue
        off = base + 1
        row = {}
        for name, length in fields:
            raw = data[off:off + length]
            off += length
            row[name] = raw.decode("latin-1").strip()
        rows.append(row)
    return rows


def read_shp_points(data):
    """Every point record in file order, as (x, y) in the file's own CRS."""
    if len(data) < 100:
        return []
    file_type = struct.unpack_from("<i", data, 32)[0]
    if file_type not in POINT_TYPES:
        raise ValueError(f"shape type {file_type} is not a point layer; "
                         "this reader deliberately does not guess at lines or polygons")
    pts = []
    pos = 100
    n = len(data)
    while pos + 8 <= n:
        _, content_len = struct.unpack_from(">ii", data, pos)
        body = pos + 8
        shape_type = struct.unpack_from("<i", data, body)[0]
        if shape_type != 0:  # 0 is a null shape, which keeps its record slot
            x, y = struct.unpack_from("<dd", data, body + 4)
            pts.append((x, y))
        else:
            pts.append(None)
        pos = body + content_len * 2
    return pts


# Inverse transverse Mercator on the GRS80 ellipsoid. ETRS89 and WGS84 differ
# by centimetres in Europe, which is far below what a register pin means.
_A = 6378137.0
_F = 1 / 298.257222101
_K0 = 0.9996


def utm_to_wgs84(easting, northing, zone, northern=True):
    e2 = _F * (2 - _F)
    ep2 = e2 / (1 - e2)
    x = easting - 500000.0
    y = northing if northern else northing - 10000000.0
    m = y / _K0
    mu = m / (_A * (1 - e2 / 4 - 3 * e2 ** 2 / 64 - 5 * e2 ** 3 / 256))
    e1 = (1 - math.sqrt(1 - e2)) / (1 + math.sqrt(1 - e2))
    phi1 = (mu + (3 * e1 / 2 - 27 * e1 ** 3 / 32) * math.sin(2 * mu)
            + (21 * e1 ** 2 / 16 - 55 * e1 ** 4 / 32) * math.sin(4 * mu)
            + (151 * e1 ** 3 / 96) * math.sin(6 * mu)
            + (1097 * e1 ** 4 / 512) * math.sin(8 * mu))
    c1 = ep2 * math.cos(phi1) ** 2
    t1 = math.tan(phi1) ** 2
    n1 = _A / math.sqrt(1 - e2 * math.sin(phi1) ** 2)
    r1 = _A * (1 - e2) / (1 - e2 * math.sin(phi1) ** 2) ** 1.5
    d = x / (n1 * _K0)
    lat = phi1 - (n1 * math.tan(phi1) / r1) * (
        d ** 2 / 2
        - (5 + 3 * t1 + 10 * c1 - 4 * c1 ** 2 - 9 * ep2) * d ** 4 / 24
        + (61 + 90 * t1 + 298 * c1 + 45 * t1 ** 2 - 252 * ep2 - 3 * c1 ** 2) * d ** 6 / 720)
    lon = (d - (1 + 2 * t1 + c1) * d ** 3 / 6
           + (5 - 2 * c1 + 28 * t1 - 3 * c1 ** 2 + 8 * ep2 + 24 * t1 ** 2) * d ** 5 / 120) / math.cos(phi1)
    return math.degrees(lat), math.degrees(lon) + (zone * 6 - 183)


def zone_from_prj(prj_text):
    """The UTM zone a .prj declares, or None when it is already lat/lon."""
    if "UTM zone" not in prj_text:
        return None
    for part in prj_text.split("UTM zone")[1:]:
        digits = ""
        for ch in part.strip():
            if ch.isdigit():
                digits += ch
            else:
                break
        if digits:
            return int(digits)
    return None


def read_points(shp_bytes, dbf_bytes, prj_text=""):
    """Point records joined to their attributes, projected to WGS84 when the
    .prj says UTM. Records whose geometry is null are dropped."""
    zone = zone_from_prj(prj_text)
    pts = read_shp_points(shp_bytes)
    rows = read_dbf(dbf_bytes)
    out = []
    for i, xy in enumerate(pts):
        if xy is None or i >= len(rows):
            continue
        if zone:
            lat, lng = utm_to_wgs84(xy[0], xy[1], zone)
        else:
            lng, lat = xy
        rec = dict(rows[i])
        rec["lat"], rec["lng"] = round(lat, 6), round(lng, 6)
        out.append(rec)
    return out
