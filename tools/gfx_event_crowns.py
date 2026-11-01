"""Enma's event-art initials, with row masks that preserve the crown edges."""
from PIL import Image


# (first mask row, half-open spans per row, English initial top-left).
# The native cursive initial meets the triangular rim at a few antialiased
# pixels; a rectangular erase would damage the crown's sloping outline.
CROWNS = {
    'EVT030D.BIN:1': (157, ((171, 173), (169, 179), (168, 180), (167, 180),
                               (169, 177), (169, 180), (168, 180), (169, 175),
                               (170, 174)), (171, 158)),
    'EVT170D.BIN:0': (81, ((203, 206), (202, 212), (201, 212), (201, 212),
                              (202, 210), (201, 211), (201, 211), (201, 211),
                              (202, 208), (203, 206)), (204, 83)),
    'EVT180D.BIN:1': (7, ((131, 133), (129, 138), (130, 138), (130, 136),
                             (129, 136), (129, 137), (130, 134), (131, 132)), (131, 8)),
    'EVT190D.BIN:1': (98, ((147, 148), (145, 151), (144, 152), (143, 152),
                              (144, 151), (144, 150), (143, 151), (143, 152),
                              (143, 149), (144, 148)), (146, 100)),
}


def rectangles(key):
    if key not in CROWNS:
        return []
    y, spans, (x, top) = CROWNS[key]
    return [(left, y + n, right, y + n + 1) for n, (left, right) in enumerate(spans)] + [
        (x, top, x + 4, top + (5 if key == 'EVT180D.BIN:1' else 7))]


def draw(image, key, palette):
    white, ink = (248, 248, 248, 255), (0, 0, 0, 255)
    assert white in palette and ink in palette
    y, spans, (x, top) = CROWNS[key]
    for n, (left, right) in enumerate(spans):
        for column in range(left, right):
            image.putpixel((column, y + n), white)
    rows = ('####', '#...', '###.', '#...', '####') if key == 'EVT180D.BIN:1' else (
        '####', '#...', '#...', '###.', '#...', '#...', '####')
    letter = Image.new('L', (4, len(rows)))
    for yy, row in enumerate(rows):
        for xx, pixel in enumerate(row):
            if pixel == '#':
                letter.putpixel((xx, yy), 255)
    image.paste(ink, (x, top, x + 4, top + len(rows)), letter)
