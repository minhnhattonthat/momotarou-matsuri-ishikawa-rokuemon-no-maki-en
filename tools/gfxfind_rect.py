"""Find complete indexed-pixel rectangles in every original archive texture.

    python tools/gfxfind_rect.py GV01000D.BIN:0 192 80 224 96
    python tools/gfxfind_rect.py GV01000D.BIN:0 201 81 214 94 --indices 12 13

Unlike gfxfind.py's row hints, every row must match at one aligned position.
--indices compares the selected ink indices exactly and treats other indices
as background. Results locate candidates, not proof of runtime use.
"""
import argparse
import struct
import sys

import arc
import gfx


def locations(pixels, width, height, rows):
    """Yield full 2D matches without wrapping a row across a texture edge."""
    start = 0
    while (start := pixels.find(rows[0], start)) >= 0:
        x, y = start % width, start // width
        if x + len(rows[0]) <= width and y + len(rows) <= height and all(
                pixels[start + n * width:start + n * width + len(row)] == row
                for n, row in enumerate(rows)):
            yield x, y
        start += 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('key')
    parser.add_argument('rectangle', nargs=4, type=int)
    parser.add_argument('--indices', nargs='+', type=int)
    args = parser.parse_args()
    name, entry = args.key.split(':')
    texture = gfx.unpack(arc.entries((gfx.TREE / name).read_bytes())[int(entry)][1])[0]
    _, width, height, _ = gfx.layout(texture)
    x0, y0, x1, y1 = args.rectangle
    assert 0 <= x0 < x1 <= width and 0 <= y0 < y1 <= height
    table = bytes(i if args.indices is None or i in args.indices else 255 for i in range(256))
    pixels = bytes(gfx.indices(texture)).translate(table)
    rows = [pixels[y * width + x0:y * width + x1] for y in range(y0, y1)]
    assert len(set(b''.join(rows))) > 1, 'refuse a blank pattern'
    print('atlas\tx\ty')
    for file in sorted(gfx.TREE.glob('*.BIN')):
        for entry, (_, data) in enumerate(arc.entries(file.read_bytes()) or []):
            if data[:4] not in (b'ECD\x01', b'\x10\0\0\0'):
                continue
            try:
                raw = gfx.unpack(data)[0]
                if raw[:4] != b'\x10\0\0\0':
                    continue
                _, w, h, _ = gfx.layout(raw)
            except (ValueError, TypeError, struct.error) as error:
                print(f'skipped {file.name}:{entry}: {error}', file=sys.stderr)
                continue
            pixels = bytes(gfx.indices(raw)).translate(table)
            for x, y in locations(pixels, w, h, rows):
                print(f'{file.name}:{entry}\t{x}\t{y}', flush=True)


if __name__ == '__main__':
    main()
