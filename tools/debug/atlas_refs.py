"""Read-only cross-archive ANM leads for a source TIM rectangle.

    python tools/debug/atlas_refs.py HOUGEN0D.BIN:0 196 160 256 184 --contained

Matches texture page, depth and a CLUT row from the source. VRAM is reused:
even an exact record is only a lead, never proof that the source is loaded.
Native-code sprites and runtime UV changes are outside this static scan.
"""
import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import anm  # noqa: E402
import arc  # noqa: E402
import gfx  # noqa: E402
import tim  # noqa: E402


def scan(key, rectangle, contained=False):
    name, entry = key.split(':')
    texture = gfx.unpack(arc.entries((gfx.TREE / name).read_bytes())[int(entry)][1])[0]
    _, depth, clut, pixels = tim.parse(texture)
    if depth not in (0, 1) or clut is None:
        raise ValueError('requires a paletted TIM')
    if pixels[0] % 64 or pixels[1] % 256:
        raise ValueError('source must start at the texture-page origin')
    _, width, height, _ = gfx.layout(texture)
    x0, y0, x1, y1 = rectangle
    if not (0 <= x0 < x1 <= width and 0 <= y0 < y1 <= height):
        raise ValueError('rectangle is outside source TIM')
    page = pixels[0] // 64 + pixels[1] // 256 * 16
    palettes = {(clut[0], clut[1] + p) for p in range(clut[3])}
    rows, archives, tables = [], 0, 0
    for path in sorted(gfx.TREE.glob('*.BIN')):
        entries = arc.entries(path.read_bytes())
        if entries is None:
            continue
        archives += 1
        tables += sum(data[:4] == b'ANM\0' for _, data in entries)
        for table, item, record in anm.references(entries, page, rectangle):
            flags, u, v, w, h, cx, cy, _, dx, dy, *_ = record
            if (flags >> 8) & 1 != depth or (cx, cy) not in palettes:
                continue
            if contained and not (x0 <= u and y0 <= v and u + w <= x1 and v + h <= y1):
                continue
            rows.append((path.name, table, item, u, v, w, h, cx, cy, dx, dy, hex(flags)))
    return rows, archives, tables


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('key')
    parser.add_argument('rectangle', type=int, nargs=4)
    parser.add_argument('--contained', action='store_true', help='require the whole sprite within the rectangle')
    args = parser.parse_args()
    rows, archives, tables = scan(args.key, args.rectangle, args.contained)
    print('archive\tentry\titem\tu\tv\tw\th\tclut_x\tclut_y\tdx\tdy\tflags')
    for row in rows:
        print(*row, sep='\t')
    print(f'{archives} archives, {tables} ANM tables, {len(rows)} candidate records', file=sys.stderr)
    print('Static candidates only; no result establishes runtime use or disuse.', file=sys.stderr)


if __name__ == '__main__':
    main()
