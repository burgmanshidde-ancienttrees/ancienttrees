#!/usr/bin/env python3
"""Pull readable text out of a PDF with no dependencies and no poppler.

Written 2026-08-18 for Amsterdam's monumental-trees booklet, which arrived by
email with written permission to use it. `pdftotext` is not installed here and
the Read tool needs poppler to render pages, so the file was unreadable by
every route the project had.

The trick that matters: a naive extractor joins every text fragment with a
space and mangles the words, because designed PDFs set type with kerning
adjustments between letters ("monument ale bomen"). The numbers inside a TJ
array say how far to move, so a LARGE negative value is a real space and a
small one is letter-spacing. Reading those instead of guessing turns the same
file from unusable into clean prose.

    python3 scripts/pdf_text.py somefile.pdf > out.txt

What it cannot do: digits set in a subset font with a custom encoding come out
empty, which is how the booklet's planting years and register numbers were
lost. When that happens the numbers usually live in whatever register the
document cites, which is the better source anyway.
"""
import re
import sys
import zlib


def streams(data):
    for m in re.finditer(rb'stream\r?\n', data):
        s = m.end(); e = data.find(b'endstream', s)
        if e < 0: continue
        try: yield zlib.decompress(data[s:e])
        except Exception: continue

def unescape(b):
    out = bytearray(); i = 0
    while i < len(b):
        c = b[i]
        if c == 0x5C and i + 1 < len(b):
            n = b[i+1]
            mp = {0x6E:10, 0x72:13, 0x74:9, 0x62:8, 0x66:12}
            if n in mp: out.append(mp[n]); i += 2; continue
            if 0x30 <= n <= 0x37:
                j = i + 1; oct_ = b''
                while j < len(b) and len(oct_) < 3 and 0x30 <= b[j] <= 0x37:
                    oct_ += bytes([b[j]]); j += 1
                out.append(int(oct_, 8) & 0xFF); i = j; continue
            out.append(n); i += 2; continue
        out.append(c); i += 1
    return bytes(out)

TOKEN = re.compile(rb"""
    \[(?P<arr>(?:[^\[\]\\]|\\.)*)\]\s*TJ
  | \((?P<str>(?:[^()\\]|\\.)*)\)\s*Tj
  | (?P<td>[-\d\.]+\s+[-\d\.]+\s+(?:Td|TD))
  | (?P<tstar>T\*)
  | (?P<tm>[-\d\.]+\s+[-\d\.]+\s+[-\d\.]+\s+[-\d\.]+\s+[-\d\.]+\s+[-\d\.]+\s+Tm)
""", re.X)

ELEM = re.compile(rb'\((?:[^()\\]|\\.)*\)|-?\d+\.?\d*')

def text_of(stream, space_at=180):
    parts = []
    for m in TOKEN.finditer(stream):
        if m.group('arr') is not None:
            buf = []
            for e in ELEM.finditer(m.group('arr')):
                tok = e.group(0)
                if tok.startswith(b'('):
                    buf.append(unescape(tok[1:-1]).decode('latin-1'))
                else:
                    try: kern = float(tok)
                    except ValueError: continue
                    if -kern >= space_at: buf.append(' ')
            parts.append(''.join(buf))
        elif m.group('str') is not None:
            parts.append(unescape(m.group('str')).decode('latin-1'))
        else:
            parts.append('\n')
    return ''.join(parts)

data = open(sys.argv[1], 'rb').read()
chunks = [text_of(s) for s in streams(data) if b'TJ' in s or b'Tj' in s]
txt = '\n'.join(chunks)
txt = re.sub(r'[ \t]+', ' ', txt)
txt = re.sub(r'\n{3,}', '\n\n', txt)
print(txt)
