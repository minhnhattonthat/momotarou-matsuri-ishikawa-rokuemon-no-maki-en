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


def match_remapped(screen, template):
    """Exact opaque pattern with a one-to-one palette mapping for weather.

    Map237 changes the whole CLUT to a dark blue rain palette. This proves
    assembly only, not colour quality; the caller must opt in and review it.
    Every pixel must agree with the mapping, including the wood between glyphs.
    """
    pixels = [(x, y, template.getpixel((x, y))[:3]) for y in range(template.height)
              for x in range(template.width)]
    if any(c[3] != 255 for c in template.getdata()):
        raise ValueError('weather matching requires an opaque rectangle')
    colours = list(dict.fromkeys(c for _, _, c in pixels))
    if len(colours) < 3:
        raise ValueError('weather matching requires at least three colours')
    anchors = [next((x, y, c) for x, y, c in pixels if c == colour) for colour in colours]
    probes = pixels[::max(1, len(pixels) // 24)]
    px = screen.load()
    for dy in range(screen.height - template.height + 1):
        for dx in range(screen.width - template.width + 1):
            mapping = {c: px[dx + x, dy + y][:3] for x, y, c in anchors}
            if len(set(mapping.values())) != len(colours):
                continue
            if all(px[dx + x, dy + y][:3] == mapping[c] for x, y, c in probes):
                if all(px[dx + x, dy + y][:3] == mapping[c] for x, y, c in pixels):
                    return dx, dy
    return None


def check(run, key, original=False, patterns=('*.png',), weather=False):
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
                if found is None and weather:
                    position = match_remapped(screen.convert('RGB'), templates[0])
                    if position is not None:
                        found = (str(path), position, 'weather-remapped')
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
