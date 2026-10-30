"""PS1 TIM decode (docs/re/graphics.md): magic 0x10 image (+ optional CLUT), magic 0x11 = CLUT-only file.

image(data, pal_index=0) -> PIL RGBA image; 4/8 bpp use CLUT row pal_index (grey ramp when the TIM has none).
"""
import struct


def parse(data):
    magic, flags = struct.unpack_from('<II', data)
    o = 8
    clut = None
    if flags & 8:
        size, x, y, w, h = struct.unpack_from('<IHHHH', data, o)
        clut = (x, y, w, h, data[o + 12:o + size])
        o += size
    img = None
    if magic == 0x10:
        size, x, y, w, h = struct.unpack_from('<IHHHH', data, o)
        raw = data[o + 12:o + size]
        if w * h * 2 != len(raw):
            # some GV*1D images carry 0xCDCD (uninitialised) w/h: assume 256 px wide (64 words in 4bpp)
            w = {0: 64, 1: 128}.get(flags & 7, 256)
            h = len(raw) // (w * 2)
        img = (x, y, w, h, raw)
    return magic, flags & 7, clut, img


def rgba(c):
    r, g, b = (c & 31) << 3, (c >> 5 & 31) << 3, (c >> 10 & 31) << 3
    return (r, g, b, 0 if c == 0 else 255)


def image(data, pal_index=0):
    from PIL import Image
    magic, bpp, clut, img = parse(data)
    x, y, w, h, raw = img
    ncol = {0: 16, 1: 256}.get(bpp)
    if ncol:
        if clut:
            cw = clut[2]
            row = clut[4][pal_index * cw * 2:(pal_index + 1) * cw * 2]
            pal = [rgba(struct.unpack_from('<H', row, i * 2)[0]) for i in range(min(ncol, len(row) // 2))]
            pal += [(0, 0, 0, 255)] * (ncol - len(pal))
        else:
            pal = [(i * 255 // (ncol - 1),) * 3 + (255,) for i in range(ncol)]
    if bpp == 0:
        out = Image.new('RGBA', (w * 4, h))
        px = out.load()
        for yy in range(h):
            for xx in range(w * 2):
                b = raw[yy * w * 2 + xx]
                px[xx * 2, yy] = pal[b & 15]
                px[xx * 2 + 1, yy] = pal[b >> 4]
    elif bpp == 1:
        out = Image.new('RGBA', (w * 2, h))
        out.putdata([pal[b] for b in raw[:w * 2 * h]])
    else:  # 16bpp
        out = Image.new('RGBA', (w, h))
        out.putdata([rgba(c) for c in struct.unpack_from(f'<{w * h}H', raw)])
    return out
