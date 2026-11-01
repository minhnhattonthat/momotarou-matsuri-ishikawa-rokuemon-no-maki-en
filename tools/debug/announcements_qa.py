"""Verify that fixture screenshots contain complete, correctly coloured ANM items.

    python -X utf8 tools/debug/announcements_qa.py RUN --out DIR
    ... --file M010D.BIN --entry 18 --items 0,1,2,3,4

The fixture runs the real paused-game renderer. A successful emulator exit is
not coverage: games may ignore Start during dialogue. This gate compares every
opaque sprite pixel, including outlines, against the built image's ANM/TIMs and
requires a match in the named screenshot. Visual review is still required.
"""
import argparse
import csv
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import anm  # noqa: E402
import arc  # noqa: E402
import gfx  # noqa: E402


def match(screen, template):
    pixels = [(x, y, c[:3]) for y in range(template.height) for x in range(template.width)
              if (c := template.getpixel((x, y)))[3]]
    if not pixels:
        return None
    probes = pixels[::max(1, len(pixels) // 16)]
    px = screen.load()

    def close(x, y, colour):
        return max(abs(a - b) for a, b in zip(px[x, y][:3], colour)) <= 8

    for dy in range(screen.height - template.height + 1):
        for dx in range(screen.width - template.width + 1):
            if all(close(dx + x, dy + y, c) for x, y, c in probes):
                if all(close(dx + x, dy + y, c) for x, y, c in pixels):
                    return dx, dy
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('run', type=Path)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--file', default='M990D.BIN')
    ap.add_argument('--entry', type=int, default=3)
    ap.add_argument('--items', default='1,2,3,4,5,6,7,8,9,10,11,13,14,15,16,18')
    ap.add_argument('--original', action='store_true')
    ap.add_argument('--scan', action='store_true', help='search numbered frames from a natural result route')
    args = ap.parse_args()
    wanted = [int(i) for i in args.items.split(',')]
    original = (gfx.TREE / args.file).read_bytes()
    archive = arc.entries(original if args.original else gfx.apply(args.file, original))
    records = anm.items(archive[args.entry][1])
    previews = args.out / 'templates'
    previews.mkdir(parents=True, exist_ok=True)
    # Render only the requested items; names here are positions in this subset.
    # The paused object overrides ANM blend bits (EXE 0x8001B66C..6A4).
    # Compare its opaque output; a different runtime blend will fail the match.
    opaque = [[(r[0] & ~0x7000, *r[1:]) for r in records[i]] for i in wanted]
    anm.render(archive, opaque, previews, strict=True)
    rows = []
    for index, item in enumerate(wanted):
        paths = sorted(args.run.glob('f[0-9]*.png')) if args.scan else [args.run / f'announcement_{item:02d}.png']
        template = previews / f'{index:03d}.png'
        position = None
        matched = ''
        for path in paths:
            if path.exists() and template.exists():
                with Image.open(path) as screen, Image.open(template) as expected:
                    position = match(screen.convert('RGB'), expected.convert('RGBA'))
                if position is not None:
                    matched = str(path)
                    break
        rows.append((item, 'ok' if position is not None else 'missing', matched, position))
    with (args.out / 'coverage.tsv').open('w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter='\t', lineterminator='\n')
        writer.writerow(('item', 'status', 'frame', 'position'))
        writer.writerows(rows)
    missing = [item for item, status, _, _ in rows if status != 'ok']
    print(f'{len(wanted) - len(missing)}/{len(wanted)} complete ANM items; missing {missing}')
    return bool(missing)


if __name__ == '__main__':
    raise SystemExit(main())
