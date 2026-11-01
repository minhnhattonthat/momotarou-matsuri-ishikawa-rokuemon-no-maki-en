"""Locate static field-grid and ANM consumers of an original atlas rectangle.

    python tools/debug/field_consumers.py GV02000D.BIN:2 184 192 256 224 --out DIR

Uses the real map table's texture/companion pairs and page/CLUT identity, not
global page-number guesses. Coordinates are 16-pixel tile cells. A reference
is a navigation lead, never proof that the game displays an item at runtime.
Zero references do not establish absence from native-code/story consumers.
"""
import argparse
import csv
from pathlib import Path
import struct
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import anm  # noqa: E402
import arc  # noqa: E402
import fileids  # noqa: E402
import gfx  # noqa: E402
import maps  # noqa: E402
import tim  # noqa: E402


def overlaps(a, b):
    return max(a[0], b[0]) < min(a[2], b[2]) and max(a[1], b[1]) < min(a[3], b[3])


def inspect(key, rectangle):
    name, entry = key.split(':')
    texture = gfx.unpack(arc.entries((gfx.TREE / name).read_bytes())[int(entry)][1])[0]
    _, depth, clut, pixels = tim.parse(texture)
    assert depth == 0, 'only 4bpp field textures are supported'
    assert pixels[0] % 64 == 0 and pixels[1] % 256 == 0, 'atlas must begin at its texture-page origin'
    page = pixels[0] // 64 + (pixels[1] // 256) * 16
    palettes = {((clut[1] + p) << 6) | (clut[0] // 16) for p in range(clut[3])}
    names = fileids.names()
    rows, owners = [], []
    for map_id, record in enumerate(maps.records()):
        texture_id, data_id = struct.unpack_from('<2H', record)
        if fileids.data_name(names, texture_id) != name:
            continue
        companion = fileids.data_name(names, data_id)
        owners.append((map_id, companion))
        entries = arc.entries((gfx.TREE / companion).read_bytes())
        grids = [(n, d) for n, (_, d) in enumerate(entries) if d[:4] == b'\x23\0\0\0']
        for table_entry, (_, data) in enumerate(entries):
            if data[:2] == b'\x22\x03':
                count = struct.unpack_from('<H', data, 4)[0]
                for tile in range(count):
                    u, v, palette, flags, tile_page = struct.unpack_from('<BB3H', data, 8 + tile * 8)
                    if tile_page & 31 != page or palette not in palettes or not overlaps(
                            rectangle, (u, v, u + 16, v + 16)):
                        continue
                    uses = []
                    for grid_entry, grid in grids:
                        width, height = grid[4:6]
                        for cell, value in enumerate(struct.unpack_from(f'<{width * height}H', grid, 8)):
                            if value == tile:
                                uses.append(f'{grid_entry}:{cell % width},{cell // width}')
                    rows.append((map_id, companion, table_entry, 'tile', tile, u, v, 16, 16,
                                 palette, f'{flags:04x}/{tile_page:04x}', ';'.join(uses)))
            elif data[:4] == b'ANM\0':
                for item, sprites in enumerate(anm.items(data)):
                    for sprite, r in enumerate(sprites):
                        _, u, v, width, height, cx, cy, sprite_page, *_ = r
                        palette = (cy << 6) | (cx // 16)
                        if sprite_page != page or palette not in palettes or not overlaps(
                                rectangle, (u, v, u + width, v + height)):
                            continue
                        rows.append((map_id, companion, table_entry, 'anm', f'{item}:{sprite}',
                                     u, v, width, height, palette, f'{r[0]:04x}',
                                     f'offset={r[8]},{r[9]}'))
    return owners, rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('key')
    parser.add_argument('rectangle', type=int, nargs=4)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    owners, rows = inspect(args.key, args.rectangle)
    args.out.mkdir(parents=True, exist_ok=True)
    with (args.out / 'consumers.tsv').open('w', encoding='utf-8', newline='') as stream:
        writer = csv.writer(stream, delimiter='\t', lineterminator='\n')
        writer.writerow(('map', 'companion', 'entry', 'kind', 'item', 'u', 'v', 'w', 'h',
                         'clut', 'flags', 'grid_entry:x,y_or_offset'))
        writer.writerows(rows)
    print(f'{args.key} {args.rectangle}: map-table owners {owners}')
    print(f'{len(rows)} overlapping records; {sum(bool(r[-1]) for r in rows)} with grid/ANM uses')
    print(args.out / 'consumers.tsv')


if __name__ == '__main__':
    main()
