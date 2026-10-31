"""Insert text: script/<FILE>.json -> changed disc files (phase 5+).

    python -X utf8 tools/insert.py stats [--marker]     how many items each mode would write

Modes:
  en      every row with a non-empty `en` (others keep their Japanese)
  marker  every row replaced by `<n> filler` (n = row number in work/markers.tsv), lines as wide as the
          Japanese line (12 px per Japanese char), inline {MM}/{R0}.. kept, page and line breaks kept
overrides = {id: text} wins over both (stress lines for the width gate).

Archives: script entries are rebuilt with text.rebuild (jumps move) and the archive repacked (arc.pack).
Code strings (`NAME@ADDR`, kind code) are written in place: encoded bytes + NUL within `max`; longer text is
an error until relocation exists (phase 7).
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
import text  # noqa: E402

TREE = ROOT / 'work' / 'disc' / 'tree'
SCRIPT = ROOT / 'script'
MARKERS = ROOT / 'work' / 'markers.tsv'
LINE_UNITS = 32          # glyph records per line object (0x10C bytes: 8 + 32 x 8 + 4), text + codes
FILL = 'The quick brown fox jumps over the lazy dog. Pack my box with five dozen liquor jugs. '
CODE = re.compile(r'\{\w+\}')


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
        s = f'<{n}>' + filler(12 * len(row['jp']), n)
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
    out, n, mk = defaultdict(dict), 0, []
    for stem, rows in rows_by_file().items():
        for r in rows:
            n += 1
            t = None
            if mode == 'marker':
                t = marker(n, r)
                mk.append(f"{n}\t{r['id']}\t{r['jp']!r}")
            elif r.get('en'):
                t = r['en']
            if r['id'] in overrides:
                t = overrides[r['id']]
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


def patch_code(data, path, items, rows):
    """Code file bytes with strings replaced in place."""
    out = bytearray(data)
    _, base, hdr = codestr.image(path)
    byid = {r['id']: r for r in rows}
    for iid, t in items.items():
        r = byid[iid]
        enc = text.encode_text(t)
        if len(enc) > r['max']:
            raise ValueError(f'{iid}: {len(enc)} bytes > max {r["max"]}: {t!r}')
        o = int(iid.split('@')[1], 16) - base + hdr
        out[o:o + r['max'] + 1] = enc + bytes(r['max'] + 1 - len(enc))
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
    return out


if __name__ == '__main__':
    if sys.argv[1:2] == ['stats']:
        tx = texts('marker' if '--marker' in sys.argv else 'en')
        print(sum(len(v) for v in tx.values()), 'items in', len(tx), 'files')
    else:
        print(__doc__)
