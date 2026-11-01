"""Translate lettering inside the attract portraits, keeping the prop silhouettes.

Only the two fan faces and ten white coat badges are editable. The masks
exclude the coloured fan ribs, badge borders, cloth and transparent pixels.
"""
from PIL import Image


# Atlas bounds include all antialiased Japanese ink; new words use native
# seven-pixel letters, split FEST / IVAL to retain the full word on each fan.
FANS = [
    ((76, 210, 107, 239), (248, 224, 8, 255), (224, 56, 24, 255), (85, 215)),
    ((173, 106, 204, 132), (224, 64, 24, 255), (0, 0, 0, 255), (181, 110)),
]
FAN_HANDLES = ((202, 102, 214, 124), (68, 235, 84, 248))
# Each numeral follows the size/angle of its original badge. Partial badges
# clip the same numeral at the original coat edge, never repainting the cloth.
BADGES = [
    ((124, 32, 138, 41), (130, 36), (6, 11), -48),
    ((170, 32, 188, 43), (179, 37), (7, 12), 48),
    ((123, 62, 134, 80), (128, 71), (5, 10), 0),
    ((171, 62, 185, 82), (178, 72), (7, 11), 8),
    ((112, 99, 123, 115), (117, 107), (7, 12), -15),
    ((132, 101, 140, 120), (138, 110), (7, 12), -6),
    ((168, 109, 176, 121), (169, 115), (7, 12), 22),
    ((183, 101, 199, 118), (191, 110), (8, 12), 40),
    ((111, 130, 122, 147), (116, 138), (7, 12), -9),
    ((190, 134, 204, 149), (198, 142), (8, 12), 28),
]


def rectangles(key):
    return ([row[0] for row in FANS] if key == 'CHR0D.BIN:1' else
            [row[0] for row in BADGES] if key == 'CHR0D.BIN:2' else [])


def masks(im, key):
    """Exact allowed pixel mask; tests also protect every excluded prop pixel."""
    allowed = Image.new('L', im.size)
    px = im.load()
    for rect in rectangles(key):
        x0, y0, x1, y1 = rect
        for y in range(y0, y1):
            for x in range(x0, x1):
                r, g, b, a = px[x, y]
                if key == 'CHR0D.BIN:1':
                    editable = a and not any(
                        left <= x < right and top <= y < bottom
                        for left, top, right, bottom in FAN_HANDLES)
                else:
                    # White/grey/black badge ink, excluding saturated red/green.
                    editable = a and max(r, g, b) - min(r, g, b) <= 24
                if editable:
                    allowed.putpixel((x, y), 255)
    return allowed


def draw(im, key, pal):
    import gen_gfx

    allowed = masks(im, key)
    if key == 'CHR0D.BIN:1':
        for rect, background, ink, (x, y) in FANS:
            assert background in pal and ink in pal
            # Yellow fan: remove only the red/cream ink. Red fan: remove the
            # black/grey lettering. The solid face colour is already present.
            for py in range(rect[1], rect[3]):
                for px in range(rect[0], rect[2]):
                    r, g, b, a = im.getpixel((px, py))
                    erase = (r > 180 and (g < 170 or b > 90)) if x < 100 else (
                        max(r, g, b) - min(r, g, b) <= 40 or b > 60)
                    if allowed.getpixel((px, py)) and erase:
                        im.putpixel((px, py), background)
            for n, word in enumerate(('FEST', 'IVAL')):
                mask = gen_gfx.mask(word, 7, {'pixel': 'credits7.txt', 'tight': True})
                im.paste(ink, (x, y + n * 8, x + mask.width, y + n * 8 + mask.height), mask)
    elif key == 'CHR0D.BIN:2':
        white, black = (240, 232, 232, 255), (0, 0, 0, 255)
        assert white in pal and black in pal
        # Hand-drawn numeral, expanded with nearest-neighbour before rotation.
        six = Image.new('L', (5, 7))
        for y, row in enumerate(('.###.', '#....', '#....', '####.', '#...#', '#...#', '.###.')):
            for x, c in enumerate(row):
                if c == '#':
                    six.putpixel((x, y), 255)
        for rect, (cx, cy), size, angle in BADGES:
            mask = six.resize(size, Image.Resampling.NEAREST).rotate(angle, expand=True)
            layer = Image.new('L', im.size)
            layer.paste(mask, (cx - mask.width // 2, cy - mask.height // 2))
            for y in range(rect[1], rect[3]):
                for x in range(rect[0], rect[2]):
                    if allowed.getpixel((x, y)):
                        im.putpixel((x, y), black if layer.getpixel((x, y)) else white)
    assert set(im.getdata()) <= pal
