"""Localize the brown marginal dialect captions; illustration SFX are separate.

Uses the committed Fredoka font and each card's original palette. Rectangles
in gfx/card_words.tsv are reviewed in original-card coordinates. Plain paper is
cleared; on illustrated backgrounds, brown lettering and its two-pixel antialias
fringe are filled from nearby unmasked pixels. English runs down the same
margin, clockwise, without resizing the illustration or the prefecture strip.
"""
import csv
from collections import deque

from PIL import Image, ImageFilter

import gen_gfx
import gfx
import gfx_card_art
import gfx_card_props

# Card 69's caption steps diagonally towards the illustrated skirt. A single
# bounding rectangle would erase the skirt's brown outline as well as the ink.
# The stepped bounds on 34/38/49/59 likewise separate caption strokes from
# the monkey, oni, hand and curled staff; whole-card QA checks those edges.
ERASE_RECTS = {
    3: [(179, 9, 203, 98)],
    11: [(181, 3, 204, 92)],
    22: [(179, 10, 201, 33), (182, 33, 201, 62)],
    28: [(172, 6, 202, 64)],
    34: [(181, 1, 205, 75), (187, 75, 205, 82), (188, 82, 205, 90)],
    36: [(180, 2, 203, 106)],
    38: [(190, 2, 208, 77), (193, 77, 208, 85), (192, 85, 208, 86),
         (190, 86, 208, 102)],
    39: [(181, 7, 208, 110), (188, 110, 208, 128)],
    45: [(4, 3, 31, 123)],
    46: [(175, 3, 203, 85)],
    49: [(5, 5, 29, 83), (5, 83, 23, 90)],
    59: [(189, 0, 208, 60), (190, 60, 208, 72), (192, 72, 208, 85), (190, 85, 208, 92),
         (188, 92, 208, 102), (190, 102, 208, 122)],
    69: [(188, 7, 205, 44), (170, 22, 188, 70), (149, 35, 165, 94)],
    76: [(177, 9, 203, 66)],
    77: [(182, 10, 204, 73)],
    78: [(8, 55, 31, 93)],
    80: [(180, 4, 208, 98)],
    81: [(6, 12, 35, 74)],
    84: [(179, 8, 203, 88)],
    86: [(184, 7, 206, 67)],
    99: [(181, 0, 208, 94)],
    100: [(180, 7, 205, 70), (186, 70, 205, 102)],
}
# These caption rectangles contain plain white paper. Clearing them completely
# removes pale, grey antialias remnants which cannot be isolated by hue alone.
PAPER_CARDS = {
    2, 3, 4, 5, 9, 10, 13, 14, 17, 18, 19, 21, 22, 23, 24, 27, 28, 29, 30,
    34, 35, 36, 37, 38, 40, 41, 43, 46, 47, 48, 49, 56, 57, 58, 59, 62, 64, 67, 69,
    72, 74, 76, 77, 78, 81, 83, 84, 88, 89, 90, 91, 92, 96, 97, 99,
}
# Blank-paper subregions inside illustrated margins. The general propagation
# can copy a grey antialias donor into a streak here. Bounds stop before the
# actual grey shoreline (45) and smoke (85); letters are drawn afterward.
PAPER_RECTS = {
    45: [(4, 3, 31, 95), (4, 95, 21, 100)],
    85: [(4, 29, 12, 44)],
}


def rows():
    with (gfx.ROOT / 'gfx' / 'card_words.tsv').open(encoding='utf-8', newline='') as f:
        result = list(csv.DictReader(f, delimiter='\t'))
    for row in result:
        for key in ('card', 'x0', 'y0', 'x1', 'y1'):
            row[key] = int(row[key])
    if [row['card'] for row in result] != list(range(1, 101)):
        raise ValueError('card_words.tsv must contain cards 1-100 in order')
    return result


def erase_caption(image, rect, paper=False, pale_fringe=False):
    """Clear reviewed paper, or isolate brown caption ink on illustrated margins."""
    x0, y0, x1, y1 = rect
    patch = image.crop(rect)
    if paper:
        image.paste((248, 248, 248, 255), rect)
        return
    ink = Image.new('L', patch.size)
    for y in range(patch.height):
        for x in range(patch.width):
            r, g, b, _ = patch.getpixel((x, y))
            if r - g >= 12 and g - b >= 4 and r - b >= 24 and g < 216:
                ink.putpixel((x, y), 255)
    if not ink.getbbox():
        raise ValueError(f'no brown lettering in {rect}')
    ink = ink.filter(ImageFilter.MaxFilter(5))
    if pale_fringe:
        # Select additional pale warm pixels without dilating them into the
        # adjacent grey beach/smoke. Expanding those pixels clips the art.
        for y in range(patch.height):
            for x in range(patch.width):
                r, g, b, _ = patch.getpixel((x, y))
                if r > g >= b and r - b >= 8:
                    ink.putpixel((x, y), 255)
    # Propagate the closest clean paper colour into the erased strokes. This
    # preserves coloured backgrounds instead of painting a white rectangle.
    pending = deque()
    known = {}
    for y in range(patch.height):
        for x in range(patch.width):
            if not ink.getpixel((x, y)):
                known[x, y] = patch.getpixel((x, y))
                pending.append((x, y))
    if not pending:
        raise ValueError(f'caption has no surrounding paper in {rect}')
    while pending:
        x, y = pending.popleft()
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= nx < patch.width and 0 <= ny < patch.height and (nx, ny) not in known:
                known[nx, ny] = known[x, y]
                patch.putpixel((nx, ny), known[x, y])
                pending.append((nx, ny))
    image.paste(patch, (x0, y0))


def redraw(image, row, palette):
    rect = tuple(row[k] for k in ('x0', 'y0', 'x1', 'y1'))
    for erase in ERASE_RECTS.get(row['card'], [rect]):
        erase_caption(image, erase, row['card'] in PAPER_CARDS, row['card'] in (45, 85))
    for paper in PAPER_RECTS.get(row['card'], []):
        image.paste((248, 248, 248, 255), paper)
    x0, y0, x1, y1 = rect
    # One style throughout the album, with the same warm brown as the originals.
    opts = {'size': 14, 'wdth': 75, 'wght': 500, 'outline': 0}
    lettering = gen_gfx.fit(row['en'], y1 - y0, x1 - x0, opts).transpose(Image.Transpose.ROTATE_270)
    colour = min(palette, key=lambda c: sum((a - b) ** 2 for a, b in zip(c[:3], (120, 88, 48))))
    x = x0 + (x1 - x0 - lettering.width) // 2
    y = y0 + (y1 - y0 - lettering.height) // 2
    # A one-pixel paper-coloured keyline keeps the English distinct where the
    # original margin crosses straw, water or other illustration linework.
    # mask() already includes an empty pixel of padding, so it stays in rect.
    edge = lettering.filter(ImageFilter.MaxFilter(3))
    paper = (248, 248, 248, 255)
    if paper not in palette:
        raise ValueError(f"card {row['card']}: expected white paper colour")
    image.paste(paper, (x, y, x + lettering.width, y + lettering.height), edge)
    image.paste(colour, (x, y, x + lettering.width, y + lettering.height), lettering)


def render(row):
    """Reconstruct one card from source; also used to reject stale PNGs."""
    i = row['card'] - 1
    key = f'HCARD{i // 10}0D.BIN:{i % 10}'
    texture, image = gen_gfx.original(key)
    palette = gfx.palette(texture, 0)
    for x0, y0, x1, y1, text, opts in gen_gfx.LABELS[key]:
        gen_gfx.draw(image, x0, y0, x1, y1, text, opts, set(palette))
    redraw(image, row, palette)
    gfx_card_art.draw(image, row['card'], palette)
    gfx_card_props.draw(image, row['card'], palette)
    return image


def generate():
    for row in rows():
        i = row['card'] - 1
        path = gfx.EN / f'HCARD{i // 10}0D_{i % 10}.png'
        image = render(row)
        image.save(path)
        print(path.relative_to(gfx.ROOT), row['en'])


if __name__ == '__main__':
    generate()
