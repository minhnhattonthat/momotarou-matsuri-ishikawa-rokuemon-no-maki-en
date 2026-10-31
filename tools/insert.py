"""Insert text: script/<FILE>.json -> changed disc files (phase 5+).

    python -X utf8 tools/insert.py stats [--marker]     how many items each mode would write

Modes:
  en      every row with a non-empty `en` (others keep their Japanese), laid out by tools/layout.py (wrap, pages,
          padding); a layout error stops the build
  marker  every row replaced by `<n> filler` (n = row number in work/markers.tsv), lines as wide as the
          Japanese line (12 px per Japanese char), inline {MM}/{R0}.. kept, page and line breaks kept
overrides = {id: text} wins over both (stress lines for the width gate).

Archives: script entries are rebuilt with text.rebuild (jumps move) and the archive repacked (arc.pack).
Code strings (`NAME@ADDR`, kind code) are written in place: encoded bytes + NUL within `max`. Longer text is
relocated in layout.RELOC files (patch_code) and an error elsewhere (EXE, OVLM*: too little slack, and the
"dead" EXE functions from tools/deadcode.py are not dead: 0x80058A98 ran in event00 under tools/lua/deadwatch.lua).
"""
import json
import re
import struct
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import arc  # noqa: E402
import codestr  # noqa: E402
import engine  # noqa: E402
import gfx  # noqa: E402
import text  # noqa: E402

TREE = ROOT / 'work' / 'disc' / 'tree'
SCRIPT = ROOT / 'script'
MARKERS = ROOT / 'work' / 'markers.tsv'
LINE_UNITS = 32          # glyph records per line object (0x10C bytes: 8 + 32 x 8 + 4), text + codes
FILL = 'The quick brown fox jumps over the lazy dog. Pack my box with five dozen liquor jugs. '
CODE = re.compile(r'\{\w+\}')
# Not drawn by build_line: the memory-card save titles, copied (25 bytes, 0x80028048) into the save header that
# the BIOS card manager shows. English must be full-width Shift-JIS (no ASCII), <= 24 bytes. Marker mode skips them.
SJIS_ONLY = {'SLPM_868@80018664': 24, 'SLPM_868@80018680': 24, 'SLPM_868@8001869C': 24}


def rows_by_file():
    return {p.stem: json.loads(p.read_text(encoding='utf-8')) for p in sorted(SCRIPT.glob('*.json'))}


def filler(px, start=0):
    out, w = '', engine.widths()
    i = start
    while engine.width_px(out + FILL[i % len(FILL)], w) <= px:
        out += FILL[i % len(FILL)]
        i += 1
    return out.rstrip()


def marker_line(n, jp_line, first):
    """One marker line for a Japanese line: same 12 px/char width, inline variable codes kept."""
    end = ''
    m = re.search(r'\{(KP|KN|KG)\}$', jp_line)
    if m:
        end, jp_line = m.group(), jp_line[:m.start()]
    keep = ''.join(c for c in CODE.findall(jp_line) if c[1:-1] in ('MM', 'R0', 'R1', 'R2', 'R3'))
    chars = len(CODE.sub('', jp_line).lstrip('　'))
    head = f'<{n}> ' if first else ''   # not [n]: [10] would parse as a raw byte
    body = head + filler(max(12 * chars - engine.width_px(head), 0), n * 7)
    while len(text.encode_text(body + keep)) // 2 + 1 > LINE_UNITS:
        body = body[:-1]
    return (body + keep).rstrip() + end if (body + keep).strip() or end else f'<{n}>'


def marker(n, row):
    if row['kind'] == 'code':
        slots = re.match(r'(?:\[20\])*', row['jp']).group()   # money template: keep put_number's digit slots
        s = slots + 'ryo' if slots else f'<{n}>' + filler(12 * len(row['jp']), n)
        while s and len(text.encode_text(s)) > row['max']:
            s = s[:-1]
        return s
    if row['kind'] != 'msg':
        return marker_line(n, row['jp'], True)
    out, first = [], True
    for line in row['jp'].split('\n'):
        out.append(marker_line(n, line, first))
        first = line.endswith('{KP}')
    return '\n'.join(out)


def texts(mode, overrides=None):
    """{file stem: {id: text}} for the rows this mode writes."""
    overrides = overrides or {}
    import layout
    import windows
    out, n, mk, var = defaultdict(dict), 0, [], None
    for stem, rows in rows_by_file().items():
        for r in rows:
            n += 1
            t = None
            if mode == 'marker' and r['id'] not in SJIS_ONLY:
                t = marker(n, r)
                mk.append(f"{n}\t{r['id']}\t{r['jp']!r}")
            elif mode != 'marker' and r.get('en'):
                t = r['en']
                if '[20]' not in r['jp'] and r['id'] not in SJIS_ONLY:   # money templates / save titles: as written
                    var = var or windows.variants()
                    t, errs = layout.render(r, var[r['id']])
                    if errs:
                        raise ValueError(f"{r['id']}: {errs}")
            if r['id'] in overrides:
                t = overrides[r['id']]
            if t is not None and r['id'] in SJIS_ONLY:
                if re.search(r'[\x20-\x7e]', CODE.sub('', t)) or len(text.encode_text(t)) > SJIS_ONLY[r['id']]:
                    raise ValueError(f"{r['id']}: save title must be full-width, <= {SJIS_ONLY[r['id']]} bytes")
            if t is not None:
                out[stem][r['id']] = t
    if mode == 'marker':
        MARKERS.parent.mkdir(parents=True, exist_ok=True)
        MARKERS.write_text('n\tid\tjp\n' + '\n'.join(mk) + '\n', encoding='utf-8')
    return out


def build_archive(path, items):
    """Archive bytes with the given {id: text} written into its script entries."""
    d = path.read_bytes()
    ents = [e for _, e in arc.entries(d)]
    per = defaultdict(lambda: defaultdict(dict))        # entry -> op offset -> {item index: text}
    for iid, t in items.items():
        _, i, rest = iid.split('/')
        o, _, k = rest.partition('.')
        per[int(i)][int(o, 16)][int(k or 0)] = t
    for i, ops in per.items():
        e = ents[i]
        old = {o: strs for o, op, n, strs in text.items_of(e)}
        new = {}
        for o, ks in ops.items():
            cur = [s for _, s in old[o]]
            for k, t in ks.items():
                cur[k] = t
            new[o] = cur
        ents[i] = text.rebuild(e, new)
    return arc.pack(ents, struct.unpack_from('<I', d)[0])


def fit(t, n):
    """t cut to at most n encoded bytes."""
    while len(text.encode_text(t)) > n:
        t = t[:-1]
    return t


def patch_code(data, path, items, rows):
    """Code file bytes with strings replaced in place. In layout.RELOC files a string longer than its `max` moves
    into a hole that shorter English leaves inside another string's original Japanese bytes (never the zero
    padding after it, which may be a struct field), 4-aligned, and every ref codestr finds (pointer words,
    lui+lo pairs) is repointed; its old place keeps the English cut to fit, for any ref codestr misses."""
    import layout
    out = bytearray(data)
    d, base, hdr = codestr.image(path)
    byid = {r['id']: r for r in rows}
    starts = sorted(int(r['id'].split('@')[1], 16) - base + hdr for r in rows)
    holes, moves = [], []
    for iid, t in items.items():
        r = byid[iid]
        enc = text.encode_text(t)
        o = int(iid.split('@')[1], 16) - base + hdr
        if len(enc) > r['max']:
            if not iid.startswith(layout.RELOC):
                raise ValueError(f'{iid}: {len(enc)} bytes > max {r["max"]}: {t!r}')
            moves.append((iid, o, enc, t))
            enc = text.encode_text(fit(t, r['max']))
        out[o:o + r['max'] + 1] = enc + bytes(r['max'] + 1 - len(enc))
        # free: after this English's NUL up to the original string's 4-aligned end (its NUL + alignment padding,
        # within max) or the next string (a tail ref), whichever first
        nul = d.index(b'\0', o - hdr) + hdr
        end = min([(nul + 4) & ~3, o + r['max'] + 1] + [s for s in starts if s > o])
        lo = (o + len(enc) + 1 + 3) & ~3
        if end > lo:
            holes.append([lo, end])
    if not moves:
        return bytes(out)
    rf = codestr.refs(d, base)
    for iid, o, enc, t in sorted(moves, key=lambda m: -len(m[2])):
        need = len(enc) + 1
        old = base + o - hdr

        def same_hi(a):  # lui halves stay valid (signed for addiu/loads, unsigned for ori)
            return a >> 16 == old >> 16 and (a + 0x8000) >> 16 == (old + 0x8000) >> 16
        h = min((h for h in holes if h[1] - h[0] >= need and same_hi(base + h[0] - hdr) and same_hi(base + h[0] - hdr + need)),
                key=lambda h: h[1] - h[0], default=None)
        if h is None:
            raise ValueError(f'{iid}: no hole for {need} bytes in its lui page: {t!r}')
        new = base + h[0] - hdr
        out[h[0]:h[0] + need] = enc + b'\0'
        h[0] = (h[0] + need + 3) & ~3
        for k in rf.get(old, []):
            if k[0] == 'ptr':
                struct.pack_into('<I', out, hdr + k[1], new)
                continue
            lui_o, lo_o = hdr + k[1], hdr + k[2]
            lw = struct.unpack_from('<I', out, lo_o)[0]
            signed = lw >> 26 != 0x0D
            hi = (new + 0x8000) >> 16 if signed else new >> 16
            ui = struct.unpack_from('<I', out, lui_o)[0]
            if hi != ui & 0xFFFF:
                # a lo can pair with a second lui codestr misses (OVLXTTL 0x800DAF10: one in a branch delay slot)
                raise ValueError(f'{iid}: move to {new:#x} changes the lui half (lui at {k[1]:#x})')
            struct.pack_into('<I', out, lo_o, (lw & 0xFFFF0000) | (new & 0xFFFF))
    return bytes(out)


def files(mode='en', overrides=None):
    """{disc path: bytes} for build.py: engine (EXE hooks, font) + text."""
    tx = texts(mode, overrides)
    rows = rows_by_file()
    exe_path = TREE / 'SLPM_868.88'
    out = {'SLPM_868.88': engine.patch_exe(exe_path.read_bytes()),
           'OUTBIN/FONT0D.BIN': engine.patch_font((TREE / 'OUTBIN' / 'FONT0D.BIN').read_bytes())}
    for stem, items in tx.items():
        if not items:
            continue
        if stem.startswith('SLPM'):
            out['SLPM_868.88'] = patch_code(out['SLPM_868.88'], exe_path, items, rows[stem])
        elif stem.startswith('OVL'):
            p = TREE / 'OUTBIN' / f'{stem}.BIN'
            out[f'OUTBIN/{stem}.BIN'] = patch_code(p.read_bytes(), p, items, rows[stem])
        else:
            out[f'OUTBIN/{stem}.BIN'] = build_archive(TREE / 'OUTBIN' / f'{stem}.BIN', items)
    for name, sites in engine.MONEY_OVL.items():
        key = f'OUTBIN/{name}'
        data = out.get(key) or (TREE / 'OUTBIN' / name).read_bytes()
        out[key] = engine.patch_money(data, sites, codestr.OVL_BASE)
    for name in gfx.redraws():
        key = f'OUTBIN/{name}'
        out[key] = gfx.apply(name, out.get(key) or (TREE / 'OUTBIN' / name).read_bytes())
    return out


if __name__ == '__main__':
    if sys.argv[1:2] == ['stats']:
        tx = texts('marker' if '--marker' in sys.argv else 'en')
        print(sum(len(v) for v in tx.values()), 'items in', len(tx), 'files')
    else:
        print(__doc__)
