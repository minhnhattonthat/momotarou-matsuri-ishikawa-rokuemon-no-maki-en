"""Inspect a plaque's complete native tile neighborhood and unused atlas slots.

    python tools/debug/field_label_plan.py GV06000D.BIN:0 200 80

Static navigation/allocation evidence only; cold captures remain the QA gate.
"""
import argparse
from pathlib import Path
import struct
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import arc
import gfx
import gfx_field
from field_consumers import inspect


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('key')
    parser.add_argument('u', type=int)
    parser.add_argument('v', type=int)
    args = parser.parse_args()
    owners, rows = inspect(args.key, (0, 0, 256, 256))
    targets = {(row[1], row[2], row[4]) for row in rows
               if row[3] == 'tile' and row[5:7] == (args.u, args.v)}
    used = set()
    for row in rows:
        _, _, _, _, _, u, v, w, h, *_ = row
        used.update((x, y) for y in range(v, v + h) for x in range(u, u + w))
    name, entry = args.key.split(':')
    raw = gfx.unpack(arc.entries((gfx.TREE / name).read_bytes())[int(entry)][1])[0]
    assert gfx.layout(raw)[1:3] == (256, 256), 'requires a 256x256 field atlas'
    pixels = gfx.indices(raw)
    slots = [(x, y) for y in range(0, 241, 16) for x in range(0, 209, 16)
             if all((xx, yy) not in used and pixels[yy * 256 + xx] == 0
                    for yy in range(y, y + 16) for xx in range(x, x + 48))]
    print('unreferenced transparent 48x16 slots:', slots)
    allocated = set()
    if args.key in gfx_field.PLANS:
        allocated = {(x, y) for plan in gfx_field.plans(args.key)
                     for u, v in gfx_field.slots(args.key, plan['label'])
                     for y in range(v, v + 16) for x in range(u, u + 16)}
    remaining = [(u, v) for v in range(0, 241, 16) for u in range(0, 241, 16)
                 if all((x, y) not in used and (x, y) not in allocated
                        and pixels[y * 256 + x] == 0
                        for y in range(v, v + 16) for x in range(u, u + 16))]
    print('unreferenced transparent aligned 16x16 slots excluding English allocations:', remaining)
    for companion in sorted({owner[1] for owner in owners}):
        entries = arc.entries((gfx.TREE / companion).read_bytes())
        for entry, (_, table) in enumerate(entries):
            if table[:2] != b'\x22\x03':
                continue
            count = struct.unpack_from('<H', table, 4)[0]
            records = [struct.unpack_from('<BB3H', table, 8 + i * 8) for i in range(count)]
            for index, record in enumerate(records):
                if (companion, entry, index) not in targets:
                    continue
                print(companion, 'table', entry, 'tile', index, 'record', record)
                for grid_entry, (_, grid) in enumerate(entries):
                    if grid[:4] != b'\x23\0\0\0':
                        continue
                    width, height = grid[4:6]
                    cells = struct.unpack_from(f'<{width * height}H', grid, 8)
                    for cell, value in enumerate(cells):
                        if value == index:
                            print(' grid', grid_entry, 'cell', (cell % width, cell // width),
                                  'neighbors', [(v, records[v]) for v in cells[cell - 1:cell + 2]])


if __name__ == '__main__':
    main()
