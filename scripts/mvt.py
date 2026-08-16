"""Minimal Mapbox Vector Tile reader, standard library only.

Wire format: Tile { repeated Layer layers = 3 }
Layer { name=1 str, features=2 msg, keys=3 str, values=4 msg, extent=5 varint }
Feature { id=1, tags=2 packed, type=3, geometry=4 packed }
Value { string=1, float=2, double=3, int=4, uint=5, sint=6, bool=7 }
"""
import gzip
import struct


def varint(b, i):
    r = s = 0
    while True:
        x = b[i]; i += 1
        r |= (x & 0x7F) << s
        if not x & 0x80:
            return r, i
        s += 7


def fields(b):
    """Yield (field_number, wire_type, payload) for one message."""
    i = 0
    while i < len(b):
        key, i = varint(b, i)
        fn, wt = key >> 3, key & 7
        if wt == 0:
            v, i = varint(b, i); yield fn, wt, v
        elif wt == 1:
            yield fn, wt, b[i:i + 8]; i += 8
        elif wt == 2:
            n, i = varint(b, i); yield fn, wt, b[i:i + n]; i += n
        elif wt == 5:
            yield fn, wt, b[i:i + 4]; i += 4
        else:
            raise ValueError("wire type %d" % wt)


def value(b):
    for fn, wt, p in fields(b):
        if fn == 1: return p.decode("utf-8", "replace")
        if fn == 2: return struct.unpack("<f", p)[0]
        if fn == 3: return struct.unpack("<d", p)[0]
        if fn in (4, 5): return p
        if fn == 6: return (p >> 1) ^ -(p & 1)
        if fn == 7: return bool(p)
    return None


def packed(b):
    out, i = [], 0
    while i < len(b):
        v, i = varint(b, i); out.append(v)
    return out


def points(geom, extent, x, y, z):
    """Decode geometry commands to lon/lat. Only the first point is kept."""
    i = cx = cy = 0
    while i < len(geom):
        cmd = geom[i]; i += 1
        op, count = cmd & 7, cmd >> 3
        if op in (1, 2):
            for _ in range(count):
                dx = (geom[i] >> 1) ^ -(geom[i] & 1); i += 1
                dy = (geom[i] >> 1) ^ -(geom[i] & 1); i += 1
                cx += dx; cy += dy
                n = 1 << z
                lon = (x + cx / extent) / n * 360.0 - 180.0
                import math
                lat = math.degrees(math.atan(math.sinh(
                    math.pi * (1 - 2 * (y + cy / extent) / n))))
                return lon, lat
        else:
            i += count
    return None


def read(raw, x, y, z):
    if raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
    layers = {}
    for fn, wt, p in fields(raw):
        if fn != 3:
            continue
        name, keys, vals, feats, extent = None, [], [], [], 4096
        for f2, w2, p2 in fields(p):
            if f2 == 1: name = p2.decode("utf-8", "replace")
            elif f2 == 3: keys.append(p2.decode("utf-8", "replace"))
            elif f2 == 4: vals.append(value(p2))
            elif f2 == 5: extent = p2
            elif f2 == 2: feats.append(p2)
        rows = []
        for f in feats:
            tags, geom, gtype = [], [], 0
            for f3, w3, p3 in fields(f):
                if f3 == 2: tags = packed(p3)
                elif f3 == 4: geom = packed(p3)
                elif f3 == 3: gtype = p3
            props = {}
            for a in range(0, len(tags) - 1, 2):
                if tags[a] < len(keys) and tags[a + 1] < len(vals):
                    props[keys[tags[a]]] = vals[tags[a + 1]]
            pt = points(geom, extent, x, y, z) if geom else None
            rows.append({"props": props, "lonlat": pt, "gtype": gtype})
        layers[name] = rows
    return layers
