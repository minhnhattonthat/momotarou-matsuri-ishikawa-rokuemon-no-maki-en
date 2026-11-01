"""Read the game's ANM sprite-rectangle tables for graphics QA (no disc edits).

    python -X utf8 tools/anm.py FILE.BIN ENTRY [--render DIR]
    python -X utf8 tools/anm.py FILE.BIN TIM_ENTRY --labels

The ANM header holds a count at +4 and the relative-offset table location at +8. Each item
is a u32 sprite count followed by 28-byte records. UV, size, CLUT and tpage are
u16s at record +2..14; signed offsets at +16/+18 and 12-bit scales at +20/+22.
Rendering supports unscaled 4bpp/8bpp sprites in the original archive; external
pages/palettes are explicitly skipped. Conflicting TIMs on the same page/palette
are rejected: callers must select the images actually loaded in that mode.
--labels lists candidate references to
redraw rectangles from gen_gfx.py. Archives can reuse VRAM pages between modes,
so a candidate is not by itself proof that the same texture is loaded.
"""
import argparse
import struct
from pathlib import Path

import arc
import gfx
import tim


def items(data):
    if data[:4] != b'ANM\0':
        raise ValueError('not an ANM sprite table')
    count, table = struct.unpack_from('<II', data, 4)
    offsets = struct.unpack_from(f'<{count}I', data, table)
    result = []
    for offset in offsets:
        n, = struct.unpack_from('<I', data, offset)
        if offset + 4 + n * 28 > len(data):
            raise ValueError('truncated ANM item')
        records = [struct.unpack_from('<8H2h4H', data, offset + 4 + j * 28) for j in range(n)]
        result.append(records)
    return result


def references(archive, page, rect):
    """All ANM records on this texture page intersecting a rectangle."""
    x0, y0, x1, y1 = rect
    for entry, (_, data) in enumerate(archive):
        if data[:4] != b'ANM\0':
            continue
        for frame, records in enumerate(items(data)):
            for r in records:
                u, v, w, h = r[1:5]
                if r[7] == page and max(x0, u) < min(x1, u + w) and max(y0, v) < min(y1, v + h):
                    yield entry, frame, r


def render(archive, entries, out, strict=False):
    from PIL import Image
    pages = {}
    for _, entry in archive:
        if entry[:4] not in (b'ECD\x01', b'\x10\0\0\0'):
            continue
        t, _ = gfx.unpack(entry)
        magic, bpp, clut, img = tim.parse(t)
        if magic != 16 or bpp not in (0, 1):
            continue
        x, y, _, _, _ = img
        for pal in range(clut[3]):
            key = (x // 64 + (y // 256) * 16, clut[0], clut[1] + pal)
            decoded = tim.image(t, pal)
            if key in pages and (pages[key][0] != bpp or pages[key][1].size != decoded.size
                                 or pages[key][1].tobytes() != decoded.tobytes()):
                raise ValueError(f'ambiguous texture/palette {key}; select the TIM entries loaded in this mode')
            pages[key] = (bpp, decoded)
    out.mkdir(parents=True, exist_ok=True)
    for i, records in enumerate(entries):
        x0 = min(r[8] for r in records)
        y0 = min(r[9] for r in records)
        x1 = max(r[8] + r[3] for r in records)
        y1 = max(r[9] + r[4] for r in records)
        image = Image.new('RGBA', (max(1, x1 - x0), max(1, y1 - y0)))
        for r in records:
            flags, u, v, w, h, cx, cy, page, dx, dy, sx, sy, _, _ = r
            if flags & ~0x100 or sx != 4096 or sy != 4096:
                raise ValueError(f'item {i}: unsupported flags/scale {r}')
            if (page, cx, cy) not in pages:
                if strict:
                    raise ValueError(f'item {i}: external palette/page {(page, cx, cy)}')
                print(f'skip item {i}: external palette/page {(page, cx, cy)}')
                break
            bpp, source = pages[(page, cx, cy)]
            if (flags >> 8) != bpp:
                raise ValueError(f'item {i}: texture depth differs from sprite flag')
            image.alpha_composite(source.crop((u, v, u + w, v + h)), (dx - x0, dy - y0))
        else:
            image.save(out / f'{i:03}.png')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('file')
    ap.add_argument('entry', type=int)
    ap.add_argument('--render', type=Path)
    ap.add_argument('--labels', action='store_true')
    args = ap.parse_args()
    archive = arc.entries((gfx.TREE / args.file).read_bytes())
    if args.labels:
        import gen_gfx
        key = f'{args.file}:{args.entry}'
        texture, _ = gen_gfx.original(key)
        tx, ty, _, _, _ = tim.parse(texture)[3]
        page = tx // 64 + ty // 256 * 16
        for x0, y0, x1, y1, label, _ in gen_gfx.LABELS[key]:
            refs = references(archive, page, (x0, y0, x1, y1))
            print(repr(label), sorted({r[1:5] for _, _, r in refs}))
        return
    entries = items(archive[args.entry][1])
    for i, records in enumerate(entries):
        print(i, '; '.join(f'page={r[7]:02x} uv={r[1]},{r[2]} size={r[3]}x{r[4]} '
                          f'offset={r[8]},{r[9]} clut={r[5]},{r[6]}' for r in records))
    if args.render:
        render(archive, entries, args.render)


if __name__ == '__main__':
    main()
