"""Require complete map-sign assemblies in cold emulator screenshots.

    python tools/debug/field_signs.py RUN --key GV16090D.BIN:1 --original

This checks real screenshots, not static map renders. Every declared sign for
the selected atlas must appear; emulator exit zero alone is not coverage.
"""
import argparse
import csv
from pathlib import Path
import sys

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import gen_gfx  # noqa: E402
import gfx  # noqa: E402
import gfx_signs  # noqa: E402
import tim  # noqa: E402
from announcements_qa import match  # noqa: E402


def check(run, key, original=False, patterns=('*.png',)):
    texture, _ = gen_gfx.original(key)
    if not original:
        name, entry = key.split(':')
        texture = gfx.redraw(texture, gfx.EN / f'{Path(name).stem}_{entry}.png')
    palettes = tim.parse(texture)[2][3]
    paths = sorted({path for pattern in patterns for path in run.glob(pattern)})
    rows = []
    for label, pieces, rect, _, _, _ in gfx_signs.SIGNS[key]:
        templates = [gfx_signs.assemble(tim.image(texture, pal), pieces).crop(rect) for pal in range(palettes)]
        found = None
        for path in paths:
            with Image.open(path) as screen:
                for pal, template in enumerate(templates):
                    position = match(screen.convert('RGB'), template)
                    if position is not None:
                        found = (str(path), position, pal)
                        break
            if found:
                break
        rows.append((key, label, 'ok' if found else 'missing', *(found or ('', '', ''))))
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('run', type=Path)
    ap.add_argument('--key', choices=sorted(gfx_signs.SIGNS), required=True)
    ap.add_argument('--original', action='store_true')
    args = ap.parse_args()
    rows = check(args.run, args.key, args.original)
    with (args.run / 'sign_coverage.tsv').open('w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter='\t', lineterminator='\n')
        writer.writerow(('atlas', 'sign', 'status', 'screenshot', 'position', 'palette'))
        writer.writerows(rows)
    missing = [r[1] for r in rows if r[2] != 'ok']
    print(f'{len(rows) - len(missing)}/{len(rows)} complete signs; missing {missing}')
    return bool(missing)


if __name__ == '__main__':
    raise SystemExit(main())
