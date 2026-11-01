"""Static field-map navigation preview; not emulator QA evidence.

    python tools/fieldmap.py GV1300 --out work/gfx/map.png [--english]

The *0D archive holds TIM pages; *1D holds two u16 tile grids (0x23), an
eight-byte tile record table (0x0322), and animated objects. This preview draws
the static grids back-to-front only: no actors, animation or story-state edits.
Runtime captures must verify the displayed palette, framing and tile assembly.
"""
import argparse
from pathlib import Path
import struct

from PIL import Image

import arc
import gfx
import tim


def render(stem, english=False):
    filename = f'{stem}0D.BIN'
    texture_data = (gfx.TREE / filename).read_bytes()
    if english:
        texture_data = gfx.apply(filename, texture_data)
    textures = arc.entries(texture_data)
    companion = f'{stem}1D.BIN'
    layout = (gfx.TREE / companion).read_bytes()
    if english:
        layout = gfx.apply(companion, layout)
    data = arc.entries(layout)
    pages = {}
    for _, entry in textures:
        if entry[:4] != b'ECD\x01':
            continue
        texture = gfx.unpack(entry)[0]
        _, bpp, clut, image = tim.parse(texture)
        if bpp != 0:
            raise ValueError('preview supports 4bpp field pages only')
        for p in range(clut[3]):
            pages[image[0] // 64 + 16 * (image[1] // 256), ((clut[1] + p) << 6) | (clut[0] // 16)] = \
                tim.image(texture, p)
    grids = [entry for _, entry in data if entry[:4] == b'\x23\0\0\0']
    tiles = next(entry for _, entry in data if entry[:2] == b'\x22\x03')
    count = struct.unpack_from('<H', tiles, 4)[0]
    width, height = grids[0][4:6]
    out = Image.new('RGBA', (width * 16, height * 16))
    for grid in reversed(grids):
        assert grid[4:8] == bytes((width, height, 16, 16))
        values = struct.unpack_from(f'<{width * height}H', grid, 8)
        for i, value in enumerate(values):
            if value >= count:
                raise ValueError(f'tile {value} outside {count} records')
            u, v, clut, flags, page = struct.unpack_from('<BB3H', tiles, 8 + value * 8)
            if flags or page & ~0xC01F:
                raise ValueError(f'unsupported tile flags {flags:04X}/{page:04X}')
            image = pages[page & 31, clut]
            crop = image.crop((u, v, u + 16, v + 16))
            out.alpha_composite(crop, ((i % width) * 16, (i // width) * 16))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('stem')
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--english', action='store_true')
    args = ap.parse_args()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    render(args.stem, args.english).save(args.out)
    print(args.out)


if __name__ == '__main__':
    main()
