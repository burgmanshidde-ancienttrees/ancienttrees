"""Minimal pure-stdlib OLE2 Compound File + BIFF8 .xls reader.

Reads old-format (pre-2007) .xls government exports, e.g. MASAF's Italian
national monumental-tree registry (masaf.gov.it), which ship as OLE2
Compound File binaries rather than the newer xlsx (zip+XML) format that
the zipfile/xml stdlib modules can already handle. No third-party
dependency (openpyxl/xlrd aren't installed and don't need to be).

Usage:
    from xls_parser import load_xls, grid_to_rows
    sheets = load_xls("region.xls")          # list of (sheet_name, grid)
    for name, grid in sheets:
        rows = grid_to_rows(grid)            # list of row lists, header first
        ...

Or from the command line: python3 scripts/xls_parser.py path/to/file.xls
prints each sheet's row count and first 3 rows, for a quick sanity check.

Handles LABELSST/LABEL/NUMBER/RK/MULRK cell records and CONTINUE-spliced
SST (shared string table) records. Good enough for reading simple, mostly
numeric/text government data exports; not a general xls library (no
formulas, no rich text runs beyond skipping their bytes, no charts).
"""
import struct


def read_ole_streams(data, wanted_names):
    sig = data[:8]
    assert sig == b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1", "not an OLE2 file"
    sector_shift = struct.unpack_from("<H", data, 30)[0]
    mini_sector_shift = struct.unpack_from("<H", data, 32)[0]
    num_fat_sectors = struct.unpack_from("<I", data, 44)[0]
    first_dir_sector = struct.unpack_from("<I", data, 48)[0]
    mini_cutoff = struct.unpack_from("<I", data, 56)[0]
    first_minifat_sector = struct.unpack_from("<I", data, 60)[0]
    first_difat_sector = struct.unpack_from("<I", data, 68)[0]
    num_difat_sectors = struct.unpack_from("<I", data, 72)[0]

    sec_size = 1 << sector_shift
    mini_size = 1 << mini_sector_shift

    def sector_offset(n):
        return 512 + n * sec_size

    def read_sector(n):
        off = sector_offset(n)
        return data[off:off + sec_size]

    # Build DIFAT (FAT sector list)
    difat = list(struct.unpack_from("<109I", data, 76))
    n = first_difat_sector
    seen = 0
    while n != 0xFFFFFFFE and n != 0xFFFFFFFF and seen < num_difat_sectors:
        sec = read_sector(n)
        entries = struct.unpack_from("<%dI" % (sec_size // 4 - 1), sec, 0)
        difat.extend(entries)
        n = struct.unpack_from("<I", sec, sec_size - 4)[0]
        seen += 1
    difat = [d for d in difat if d != 0xFFFFFFFF]

    # Build FAT
    fat = []
    for fs in difat[:num_fat_sectors] if num_fat_sectors else difat:
        sec = read_sector(fs)
        fat.extend(struct.unpack_from("<%dI" % (sec_size // 4), sec, 0))

    def follow_chain(start, size_hint=None):
        chain = []
        n = start
        guard = 0
        while n != 0xFFFFFFFE and n != 0xFFFFFFFF and n < len(fat):
            chain.append(n)
            n = fat[n]
            guard += 1
            if guard > 2_000_000:
                raise RuntimeError("FAT chain too long / corrupt")
        buf = b"".join(read_sector(s) for s in chain)
        if size_hint is not None:
            buf = buf[:size_hint]
        return buf

    # Directory entries
    dir_bytes = follow_chain(first_dir_sector)
    n_entries = len(dir_bytes) // 128
    entries = []
    for i in range(n_entries):
        e = dir_bytes[i * 128:(i + 1) * 128]
        name_len = struct.unpack_from("<H", e, 64)[0]
        raw_name = e[0:max(name_len - 2, 0)] if name_len >= 2 else b""
        try:
            name = raw_name.decode("utf-16le")
        except Exception:
            name = ""
        obj_type = e[66]
        start_sector = struct.unpack_from("<I", e, 116)[0]
        stream_size = struct.unpack_from("<Q", e, 120)[0]
        entries.append((name, obj_type, start_sector, stream_size))

    root = next((e for e in entries if e[1] == 5), None)
    root_start, root_size = root[2], root[3]
    ministream = follow_chain(root_start, root_size)

    minifat = []
    if first_minifat_sector != 0xFFFFFFFE:
        n = first_minifat_sector
        while n != 0xFFFFFFFE and n != 0xFFFFFFFF:
            sec = read_sector(n)
            minifat.extend(struct.unpack_from("<%dI" % (sec_size // 4), sec, 0))
            n = fat[n]

    def follow_mini_chain(start, size_hint):
        chain = []
        n = start
        while n != 0xFFFFFFFE and n != 0xFFFFFFFF:
            chain.append(n)
            n = minifat[n]
        parts = []
        for s in chain:
            off = s * mini_size
            parts.append(ministream[off:off + mini_size])
        buf = b"".join(parts)
        return buf[:size_hint]

    out = {}
    for name, obj_type, start_sector, stream_size in entries:
        if obj_type != 2:
            continue
        if name not in wanted_names:
            continue
        if stream_size < mini_cutoff:
            out[name] = follow_mini_chain(start_sector, stream_size)
        else:
            out[name] = follow_chain(start_sector, stream_size)
    return out


def parse_rk(rk_bytes):
    raw = struct.unpack("<i", rk_bytes)[0]  # signed 32-bit, includes the 2 flag bits
    is_int = raw & 0x2
    is_100 = raw & 0x1
    if is_int:
        result = float(raw >> 2)  # arithmetic shift, sign-preserving
    else:
        top32 = (raw & ~0x3) & 0xFFFFFFFF  # high 32 bits of the IEEE double, low 2 bits cleared
        packed = b"\x00\x00\x00\x00" + struct.pack("<I", top32)  # low dword=0, high dword=top32 (LE)
        result = struct.unpack("<d", packed)[0]
    if is_100:
        result /= 100.0
    return result


def biff_records(stream):
    """Yield (type, data) merging any CONTINUE records into the preceding one."""
    pos = 0
    n = len(stream)
    pending_type = None
    pending_data = b""
    while pos + 4 <= n:
        rtype, rlen = struct.unpack_from("<HH", stream, pos)
        data = stream[pos + 4: pos + 4 + rlen]
        pos += 4 + rlen
        if rtype == 0x003C:  # CONTINUE
            if pending_type is not None:
                pending_data += data
            continue
        if pending_type is not None:
            yield pending_type, pending_data
        pending_type, pending_data = rtype, data
    if pending_type is not None:
        yield pending_type, pending_data


def parse_sst(data):
    total, unique = struct.unpack_from("<II", data, 0)
    pos = 8
    strings = []
    n = len(data)
    for _ in range(unique):
        if pos + 3 > n:
            break
        cch = struct.unpack_from("<H", data, pos)[0]
        flags = data[pos + 2]
        pos += 3
        compressed = not (flags & 0x1)
        has_rich = bool(flags & 0x8)
        has_asian = bool(flags & 0x4)
        crun = 0
        cb_ext = 0
        if has_rich:
            crun = struct.unpack_from("<H", data, pos)[0]
            pos += 2
        if has_asian:
            cb_ext = struct.unpack_from("<I", data, pos)[0]
            pos += 4
        if compressed:
            raw = data[pos:pos + cch]
            pos += cch
            s = raw.decode("cp1252", errors="replace")
        else:
            raw = data[pos:pos + cch * 2]
            pos += cch * 2
            s = raw.decode("utf-16le", errors="replace")
        pos += crun * 4
        pos += cb_ext
        strings.append(s)
    return strings


def sheets_from_workbook(wb_stream):
    """Scan the whole workbook stream for BOUNDSHEET records (sheet names,
    only present in the globals substream) and BOF record offsets (one per
    substream, globals first). Returns (boundsheets, bof_offsets)."""
    boundsheets = []
    bofs = []
    p = 0
    n = len(wb_stream)
    while p + 4 <= n:
        rtype, rlen = struct.unpack_from("<HH", wb_stream, p)
        data = wb_stream[p + 4:p + 4 + rlen]
        if rtype == 0x0809:  # BOF
            bofs.append(p)
        if rtype == 0x0085:  # BOUNDSHEET
            offset = struct.unpack_from("<I", data, 0)[0]
            cch = data[6]
            grbit_chr = data[7]
            compressed = not (grbit_chr & 0x1)
            name_bytes = data[8:]
            if compressed:
                name = name_bytes[:cch].decode("cp1252", errors="replace")
            else:
                name = name_bytes[:cch * 2].decode("utf-16le", errors="replace")
            boundsheets.append((name, offset))
        p += 4 + rlen
    return boundsheets, bofs


def read_sheet_grid(wb_stream, start_offset):
    """Parse BIFF records for one worksheet substream starting at start_offset
    (a BOF record position) until its matching EOF. Returns
    dict[(row,col)] = (kind, value), kind in {"sst","num","str"}."""
    pos = start_offset
    n = len(wb_stream)
    grid = {}
    depth = 0
    while pos + 4 <= n:
        rtype, rlen = struct.unpack_from("<HH", wb_stream, pos)
        data = wb_stream[pos + 4:pos + 4 + rlen]
        # merge any following CONTINUE records into this one
        npos = pos + 4 + rlen
        while npos + 4 <= n:
            nrtype, nrlen = struct.unpack_from("<HH", wb_stream, npos)
            if nrtype != 0x003C:
                break
            data += wb_stream[npos + 4:npos + 4 + nrlen]
            npos += 4 + nrlen
        pos = npos

        if rtype == 0x0809:  # BOF
            depth += 1
        elif rtype == 0x000A:  # EOF
            depth -= 1
            if depth == 0:
                break
        elif rtype == 0x00FD:  # LABELSST
            row, col, xf, sst_idx = struct.unpack_from("<HHHI", data, 0)
            grid[(row, col)] = ("sst", sst_idx)
        elif rtype == 0x0203:  # NUMBER
            row, col, xf = struct.unpack_from("<HHH", data, 0)
            val = struct.unpack_from("<d", data, 6)[0]
            grid[(row, col)] = ("num", val)
        elif rtype == 0x027E:  # RK
            row, col, xf = struct.unpack_from("<HHH", data, 0)
            val = parse_rk(data[6:10])
            grid[(row, col)] = ("num", val)
        elif rtype == 0x00BD:  # MULRK
            row, first_col = struct.unpack_from("<HH", data, 0)
            rest = data[4:-2]
            last_col = struct.unpack_from("<H", data, len(data) - 2)[0]
            ncols = last_col - first_col + 1
            for i in range(ncols):
                xf, rk = struct.unpack_from("<Hi", rest, i * 6)
                val = parse_rk(struct.pack("<i", rk))
                grid[(row, first_col + i)] = ("num", val)
        elif rtype == 0x0204:  # LABEL (plain, not SST)
            row, col, xf, cch = struct.unpack_from("<HHHH", data, 0)
            flags = data[8]
            compressed = not (flags & 0x1)
            raw = data[9:]
            if compressed:
                s = raw[:cch].decode("cp1252", errors="replace")
            else:
                s = raw[:cch * 2].decode("utf-16le", errors="replace")
            grid[(row, col)] = ("str", s)
    return grid


def load_xls(path_or_bytes):
    """Returns a list of (sheet_name, grid) pairs, grid = dict[(row,col)] -> resolved value."""
    data = path_or_bytes if isinstance(path_or_bytes, (bytes, bytearray)) else open(path_or_bytes, "rb").read()
    streams = read_ole_streams(data, {"Workbook", "Book"})
    wb = streams.get("Workbook") or streams.get("Book")
    if wb is None:
        raise RuntimeError("no Workbook/Book stream found")

    # SST (shared strings) lives in the globals substream, before the first
    # worksheet BOF; scan the whole stream once, merging CONTINUEs.
    sst = []
    for rtype, data_ in biff_records(wb):
        if rtype == 0x00FC:
            sst = parse_sst(data_)
            break

    boundsheets, bofs = sheets_from_workbook(wb)
    result = []
    for (name, _offset), bof_pos in zip(boundsheets, bofs[1:]):
        grid = read_sheet_grid(wb, bof_pos)
        resolved = {}
        for k, (kind, v) in grid.items():
            resolved[k] = sst[v] if kind == "sst" and v < len(sst) else v
        result.append((name, resolved))
    return result


def grid_to_rows(grid):
    """Turn a {(row,col): value} grid into a list of row lists (skipping fully-blank rows)."""
    if not grid:
        return []
    max_row = max(r for r, c in grid)
    max_col = max(c for r, c in grid)
    rows = []
    for r in range(max_row + 1):
        row = [grid.get((r, c), "") for c in range(max_col + 1)]
        if any(v != "" for v in row):
            rows.append(row)
    return rows


def dms_to_decimal(dms):
    """Convert a "43° 49' 14,63''" style string (MASAF's format) to decimal degrees."""
    import re
    m = re.match(r"(\d+)\D+(\d+)\D+([\d,\.]+)", dms.strip())
    if not m:
        return None
    deg, minutes, seconds = m.groups()
    seconds = seconds.replace(",", ".")
    return float(deg) + float(minutes) / 60 + float(seconds) / 3600


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("usage: python3 xls_parser.py path/to/file.xls")
        raise SystemExit(1)
    for name, grid in load_xls(sys.argv[1]):
        rows = grid_to_rows(grid)
        print("===", name, "-", len(rows), "rows")
        for row in rows[:3]:
            print(row)
