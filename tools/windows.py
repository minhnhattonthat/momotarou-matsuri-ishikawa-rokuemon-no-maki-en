"""Box variants and line budgets (docs/re/windows.md): the px width each English line must fit.

    python -X utf8 tools/windows.py [ID ...]      variant, budget, tag per id (no ids: counts per variant)

budget(row, variant) -> (px per line, visible lines or None, tag): tag 'measured' (shot in docs/re/windows.md)
or 'guess' (Japanese design width: 12 px per JP char of the item's longest line; measure before cutting text).
Widths are sums of engine.widths() advances (Japanese chars and codes count 12 px).
"""
import json
import re
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))

LINE_UNITS = 32  # records per line object: digraph units + codes (docs/re/engine.md)
VARIANT = {      # px per line, visible lines, tag
    'msg': (228, 3, 'measured'),           # op 02, x=48; frame inner edges x=37..282 (event00, widthgate.json)
    'msg_portrait': (192, 3, 'measured'),  # op 02 with a voice/portrait, x=90; same frame
    'memcard': (180, 3, 'measured'),       # EXE {KK}/{KE} messages, x=72, frame inner right 258; <= 64 bytes/line
}
# code strings measured in-game (widthgate.json shots), else JP width
MEASURED = {
    'OVLXTTL@800CB504': 112, 'OVLXTTL@800CB524': 112,   # main menu, left column x=62, right column starts 184
    'OVLXTTL@800CB514': 92, 'OVLXTTL@800CB534': 92,     # right column x=184, frame 282
}
CHOICE = re.compile(r'SLPM_868@8008C(2[C-F]|3[0-5])')   # EXE choice boxes (0x8002C774..CF34): x=260, frame ~288
CHOICE_W = 26
LAYOUT = {  # one line holding several items at fixed x (cursor positions); keep the Japanese spacing scheme
    'OVLXTTL@800CB4E4': 'title New/Continue: items start at x=108 and x=192 (line x=48; 　 = 12 px, space 4 px)',
}


def jp_width(jp):
    return max((12 * len(re.sub(r'\{\w+\}|\[[0-9A-F]{2}\]', '', ln)) for ln in jp.split('\n')), default=0)


def variants():
    """{id: variant} for every script item: msg / msg_portrait (op 02 voice != 0xFFFF), menu, caption, code."""
    import text
    out = {}
    for p in sorted((ROOT / 'script').glob('*.json')):
        for r in json.loads(p.read_text(encoding='utf-8')):
            out[r['id']] = 'memcard' if r['kind'] == 'code' and r['jp'].endswith('{KE}') else r['kind']
    for f in text.archives():
        for i, e, its in text.script_entries(open(f, 'rb').read()):
            for o, op, n, strs in its:
                if op == 0x02 and struct.unpack_from('<H', e, o + 4)[0] != 0xFFFF:
                    out[text.item_id(text.stem(f), i, o, '')] = 'msg_portrait'
    return out


def budget(row, variant):
    if variant in VARIANT:
        return VARIANT[variant]
    if row['id'] in MEASURED:
        return MEASURED[row['id']], 1, 'measured'
    if CHOICE.match(row['id']):
        return CHOICE_W, 1, 'measured'
    return jp_width(row['jp']), None, 'guess'


if __name__ == '__main__':
    from collections import Counter
    v = variants()
    rows = {r['id']: r for p in (ROOT / 'script').glob('*.json') for r in json.loads(p.read_text(encoding='utf-8'))}
    if sys.argv[1:]:
        for i in sys.argv[1:]:
            print(i, v[i], budget(rows[i], v[i]))
    else:
        print(Counter((v[i], budget(r, v[i])[2]) for i, r in rows.items()))
