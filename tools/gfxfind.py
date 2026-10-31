"""Find every image that holds the same pixels as a rect of another (graphics shipped twice or more).

    python -X utf8 tools/gfxfind.py FILE:ENTRY X0 Y0 X1 Y1
Searches each pixel row of the rect (as packed index bytes; X0 rounded to whole bytes) in every decompressed TIM
of every OUTBIN archive and prints FILE:ENTRY with the number of rows found.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import arc  # noqa: E402
import gfx  # noqa: E402


def rows(t, x0, y0, x1, y1):
    o, w, h, bits = gfx.layout(t)
    bpr = w * bits // 8
    a, b = x0 * bits // 8, (x1 * bits + 7) // 8
    return [t[o + y * bpr + a:o + y * bpr + b] for y in range(y0, y1)]


def main(key, x0, y0, x1, y1):
    name, _, e = key.partition(':')
    t, _ = gfx.unpack(arc.entries((gfx.TREE / name).read_bytes())[int(e)][1])
    want = [r for r in rows(t, x0, y0, x1, y1) if len(set(r)) > 2]   # skip blank rows
    for f in sorted(gfx.TREE.glob('*.BIN')):
        es = arc.entries(f.read_bytes())
        for i, (_, ent) in enumerate(es or []):
            try:
                u, _ = gfx.unpack(ent)
                gfx.layout(u)
            except Exception:
                continue
            n = sum(r in u for r in want)
            if n:
                print(f'{f.name}:{i}\t{n}/{len(want)} rows')


if __name__ == '__main__':
    main(sys.argv[1], *map(int, sys.argv[2:6]))
