"""Graphics text (phase 8, docs/re/graphics.md): English redraws of TIM images inside OUTBIN archives.

    python -X utf8 tools/gfx.py export FILE:ENTRY [--pal N]   original image -> work/gfx/jp/FILE_ENTRY.png
    python -X utf8 tools/gfx.py show                          each redraw's changed-pixel box, per file

A redraw is gfx/en/<FILE>_<ENTRY>[_p<N>].png: the whole image, same size, drawn in the colours of CLUT row N
(default 0). The build (insert.files -> apply) maps each pixel back to a palette index: unchanged pixels keep
their original index (palettes repeat colours), changed ones take the first index of that exact colour, any
other colour is an error. Only the pixel block changes; header and CLUT stay, and the entry is recompressed
(ECD) if it was compressed.
"""
import re
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import arc  # noqa: E402
import ecd  # noqa: E402
import tim  # noqa: E402

TREE = ROOT / 'work' / 'disc' / 'tree' / 'OUTBIN'
EN = ROOT / 'gfx' / 'en'
NAME = re.compile(r'([A-Z0-9_]+)_(\d+)(?:_p(\d+))?\.png$')


def redraws():
    """{FILE.BIN: [(entry, pal, png path)]}"""
    out = {}
    for p in sorted(EN.glob('*.png')):
        m = NAME.match(p.name)
        if not m:
            raise ValueError(f'{p.name}: name it FILE_ENTRY[_pN].png')
        out.setdefault(f'{m[1]}.BIN', []).append((int(m[2]), int(m[3] or 0), p))
    return out


def unpack(entry):
    """(TIM bytes, compressed?)"""
    return (ecd.decompress(entry), True) if entry[:4] == ecd.MAGIC else (entry, False)


def layout(t):
    """(pixel block offset, width px, height, bits per pixel) of a 4/8 bpp TIM."""
    magic, bpp, clut, img = tim.parse(t)
    if magic != 0x10 or bpp not in (0, 1):
        raise ValueError('only 4/8 bpp TIM images')
    o = 8 + (struct.unpack_from('<I', t, 8)[0] if clut else 0) + 12
    x, y, w, h, raw = img
    return o, w * (4 if bpp == 0 else 2), h, 4 if bpp == 0 else 8


def indices(t):
    o, w, h, bits = layout(t)
    if bits == 8:
        return list(t[o:o + w * h])
    return [t[o + i // 2] >> (4 * (i & 1)) & 15 for i in range(w * h)]


def palette(t, pal):
    _, bpp, clut, _ = tim.parse(t)
    row = clut[4][pal * clut[2] * 2:(pal + 1) * clut[2] * 2]
    return [tim.rgba(c) for c in struct.unpack_from(f'<{len(row) // 2}H', row)]


def redraw(t, png, pal=0):
    """TIM bytes with the PNG's pixels (see module doc)."""
    from PIL import Image
    o, w, h, bits = layout(t)
    im = Image.open(png).convert('RGBA')
    if im.size != (w, h):
        raise ValueError(f'{png.name}: {im.size}, image is {(w, h)}')
    pl = palette(t, pal)
    norm = [c if c[3] else (0, 0, 0, 0) for c in pl]
    first = {}
    for i, c in enumerate(norm):
        first.setdefault(c, i)
    old = indices(t)
    new = []
    for i, c in enumerate(im.getdata()):
        c = c if c[3] else (0, 0, 0, 0)
        if old[i] < len(norm) and norm[old[i]] == c:
            new.append(old[i])
        elif c in first:
            new.append(first[c])
        else:
            raise ValueError(f'{png.name}: pixel ({i % w},{i // w}) colour {c} not in CLUT row {pal}')
    out = bytearray(t)
    if bits == 8:
        out[o:o + w * h] = bytes(new)
    else:
        out[o:o + w * h // 2] = bytes(new[k] | new[k + 1] << 4 for k in range(0, w * h, 2))
    return bytes(out)


def apply(name, data):
    """Archive bytes with every redraw of this file written in."""
    hs = struct.unpack_from('<I', data)[0]
    ents = [e for _, e in arc.entries(data)]
    for i, pal, png in redraws().get(name, []):
        t, packed = unpack(ents[i])
        n = redraw(t, png, pal)
        ents[i] = ecd.compress(n, ecd.header(ents[i])[0]) if packed else n
    return arc.pack(ents, hs)


def same_but_pixels(a, b):
    """True if two archive entries hold TIMs that differ only inside the pixel block."""
    ta, tb = unpack(a)[0], unpack(b)[0]
    o, w, h, bits = layout(ta)
    n = o + w * h * bits // 8
    return len(ta) == len(tb) and ta[:o] == tb[:o] and ta[n:] == tb[n:]


def changed_box(t, png, pal=0):
    o, w, h, _ = layout(t)
    a, b = indices(t), indices(redraw(t, png, pal))
    xs = [i % w for i in range(w * h) if a[i] != b[i]]
    ys = [i // w for i in range(w * h) if a[i] != b[i]]
    return (min(xs), min(ys), max(xs) + 1, max(ys) + 1) if xs else None


def main(argv):
    if argv[:1] == ['export']:
        f, _, e = argv[1].partition(':')
        pal = int(argv[argv.index('--pal') + 1]) if '--pal' in argv else 0
        t, _ = unpack(arc.entries((TREE / f).read_bytes())[int(e)][1])
        out = ROOT / 'work' / 'gfx' / 'jp' / f'{Path(f).stem}_{e}{f"_p{pal}" if pal else ""}.png'
        out.parent.mkdir(parents=True, exist_ok=True)
        tim.image(t, pal).save(out)
        print(out)
    elif argv[:1] == ['show']:
        for name, rs in redraws().items():
            ents = arc.entries((TREE / name).read_bytes())
            for i, pal, png in rs:
                print(f'{png.name}: changed box {changed_box(unpack(ents[i][1])[0], png, pal)}')
    else:
        print(__doc__)


if __name__ == '__main__':
    main(sys.argv[1:])
