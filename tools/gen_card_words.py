"""Localize the brown marginal dialect captions; illustration SFX are separate.

Uses the committed Fredoka font and each card's original palette. Rectangles
in gfx/card_words.tsv are reviewed in original-card coordinates. Plain paper is
cleared; on illustrated backgrounds, brown lettering and its antialias fringe
are filled from reviewed background pixels. English runs down the same
margin, clockwise, without resizing the illustration or the prefecture strip.
"""
import csv
from collections import deque

from PIL import Image, ImageDraw, ImageFilter

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
    33: [(177, 1, 204, 75)],
    34: [(181, 1, 205, 75), (187, 75, 205, 82), (188, 82, 205, 90)],
    36: [(180, 2, 203, 106)],
    38: [(190, 2, 208, 77), (193, 77, 208, 85), (192, 85, 208, 86),
         (190, 86, 208, 102)],
    39: [(192, 7, 208, 15), (190, 15, 208, 34), (186, 34, 208, 110),
         (188, 110, 208, 114), (191, 114, 208, 128)],
    45: [(4, 3, 31, 123)],
    46: [(175, 3, 203, 85)],
    49: [(5, 5, 29, 83), (5, 83, 23, 90)],
    59: [(189, 0, 208, 60), (190, 60, 208, 72), (192, 72, 208, 85), (190, 85, 208, 92),
         (188, 92, 208, 102), (190, 102, 208, 122)],
    63: [(178, 3, 208, 128)],
    69: [(188, 7, 205, 44), (170, 22, 188, 70), (149, 35, 165, 94)],
    75: [(6, 5, 31, 94)],
    76: [(177, 9, 203, 66)],
    77: [(182, 10, 204, 73)],
    78: [(8, 55, 31, 93)],
    79: [(179, 3, 204, 84)],
    80: [(180, 4, 208, 98)],
    81: [(6, 12, 35, 74)],
    84: [(179, 8, 203, 88)],
    86: [(184, 7, 206, 67)],
    93: [(5, 20, 28, 72)],
    94: [(5, 2, 30, 78)],
    99: [(181, 0, 208, 94)],
    100: [(180, 7, 205, 70), (186, 70, 205, 102)],
}
# These caption rectangles contain plain white paper. Clearing them completely
# removes pale, grey antialias remnants which cannot be isolated by hue alone.
PAPER_CARDS = {
    2, 3, 4, 5, 9, 10, 13, 14, 17, 18, 19, 21, 22, 23, 24, 27, 28, 29, 30,
    33, 34, 35, 36, 37, 38, 39, 40, 41, 43, 46, 47, 48, 49, 56, 57, 58, 59, 62, 64, 67, 69,
    72, 74, 76, 77, 78, 81, 83, 84, 88, 89, 90, 91, 92, 93, 96, 97, 99,
}
# Blank-paper subregions inside illustrated margins. The general propagation
# can copy a grey antialias donor into a streak here. Bounds stop before the
# actual grey shoreline (45) and smoke (85); letters are drawn afterward.
PAPER_RECTS = {
    45: [(4, 3, 31, 95), (4, 95, 21, 100)],
    63: [(190, 86, 208, 118), (196, 118, 208, 128)],
    79: [(181, 3, 201, 20)],
    85: [(4, 29, 12, 44)],
}

# Illustrated margins whose old breadth-first fill copied grey drawing edges
# across the removed letters. Keep neutral linework and coloured illustration
# pixels; fill caption ink and fringe using nearby light background donors.
SELECTIVE_CARDS = {7, 26, 44, 54, 63, 75, 79, 82, 87, 94, 98}
# Grey ink fringes here can touch a neighbouring drawing through antialias
# pixels. These bounds waive component protection; card087 reconstructs the
# overlapping sky fade separately instead of treating it as blank paper.
CAPTION_FRINGE_RECTS = {
    54: [(177, 23, 185, 36), (196, 33, 202, 48)],
    63: [(186, 18, 205, 34), (194, 85, 205, 116)],
    79: [(179, 3, 204, 23)],
    87: [(183, 1, 208, 48)],
}


def erase_warm_caption(image, rect, card):
    x0, y0, x1, y1 = rect
    patch = image.crop(rect)
    seeds = Image.new('L', patch.size)
    for y in range(patch.height):
        for x in range(patch.width):
            r, g, b, _ = patch.getpixel((x, y))
            if r - g >= 12 and g - b >= 4 and r - b >= 24 and g < 216:
                seeds.putpixel((x, y), 255)
    nearby = seeds.filter(ImageFilter.MaxFilter(7))
    # Retain grey drawing components connected to unmasked art. Isolated grey
    # antialias pixels belonging to the removed kana are not artwork donors.
    grey = set()
    protected = set()
    for y in range(patch.height):
        for x in range(patch.width):
            r, g, b, _ = patch.getpixel((x, y))
            if max(r, g, b) - min(r, g, b) <= 16 and max(r, g, b) < 232:
                grey.add((x, y))
                if not nearby.getpixel((x, y)):
                    protected.add((x, y))
    pending = deque(sorted(protected))
    while pending:
        x, y = pending.popleft()
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1),
                       (-1, -1), (-1, 1), (1, -1), (1, 1)):
            point = x + dx, y + dy
            if point in grey and point not in protected:
                protected.add(point)
                pending.append(point)
    for ax0, ay0, ax1, ay1 in CAPTION_FRINGE_RECTS.get(card, []):
        protected.difference_update((x - x0, y - y0)
                                    for y in range(ay0, ay1) for x in range(ax0, ax1))
    removed = set()
    for y in range(patch.height):
        for x in range(patch.width):
            r, g, b, _ = patch.getpixel((x, y))
            blue_art = card in (63, 75, 87) and g - r >= 8 and b >= g
            pink_art = card == 79 and r - g >= 24 and r >= b > g and min(r, g, b) >= 184
            yellow_leaf = card == 63 and r == g and r - b >= 16 and b >= 184
            coloured_art = blue_art or pink_art or yellow_leaf
            if nearby.getpixel((x, y)) and (x, y) not in protected and not coloured_art:
                removed.add((x, y))
    donors = []
    for y in range(patch.height):
        for x in range(patch.width):
            colour = patch.getpixel((x, y))
            r, g, b = colour[:3]
            clean_paper = (r, g, b) == (248, 248, 248)
            pale_sky = card in (63, 75, 87) and g >= 240 and b >= 240 and b - r >= 8
            if not nearby.getpixel((x, y)) and (clean_paper or pale_sky):
                donors.append((x, y, colour))
    if not donors:
        raise ValueError(f'no clean light background in {rect}')
    paper_donors = [p for p in donors if p[2][:3] == (248, 248, 248)]
    colours = sorted(set(image.getdata()))
    for x, y in removed:
        sky = ((card == 63 and y + y0 < 80) or (card == 75 and 42 <= y + y0 < 63)
               or (card == 87 and 50 <= y + y0 < 100))
        candidates = donors if sky else paper_donors
        _, _, colour = min(candidates, key=lambda p: (p[0] - x) ** 2 + (p[1] - y) ** 2)
        if card == 87 and y + y0 < 48:
            # The caption overlaps the grey sky's fade. Interpolate between
            # clean columns at its left and right, retaining native colours;
            # a paper donor here made a conspicuous white notch in the sky.
            left = image.getpixel((183, y + y0))
            right = image.getpixel((207, y + y0))
            weight = (x + x0 - 183) / 24
            target = tuple(round(a + (b - a) * weight) for a, b in zip(left, right))
            colour = min(colours, key=lambda p: sum((a - b) ** 2 for a, b in zip(p, target)))
        patch.putpixel((x, y), colour)
    image.paste(patch, (x0, y0))


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
        if row['card'] in SELECTIVE_CARDS:
            erase_warm_caption(image, erase, row['card'])
        else:
            erase_caption(image, erase, row['card'] in PAPER_CARDS, row['card'] in (45, 85))
    for paper in PAPER_RECTS.get(row['card'], []):
        image.paste((248, 248, 248, 255), paper)
    if row['card'] == 63:
        repair_card63(image, palette)
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


def repair_card63(image, palette):
    """Restore the leaf edge hidden by the first kana; clear isolated fringe.

    These reviewed sky windows contain no illustration. Preserve their blue
    pixels, but remove grey/yellow antialias remnants missed by hue selection.
    The reconstructed lower arc joins the surviving original top/left outline.
    """
    paper = (248, 248, 248, 255)
    for x0, y0, x1, y1 in ((198, 13, 208, 35), (180, 18, 198, 35),
                           (198, 9, 208, 13), (196, 35, 208, 41),
                           (201, 41, 208, 50), (198, 50, 208, 62)):
        for y in range(y0, y1):
            for x in range(x0, x1):
                r, g, b, _ = image.getpixel((x, y))
                if not (g - r >= 8 and b >= g):
                    image.putpixel((x, y), paper)
    def colour(rgb):
        return min(palette, key=lambda p: sum((a - b) ** 2 for a, b in zip(p[:3], rgb)))
    draw = ImageDraw.Draw(image)
    draw.line([(184, 12), (186, 13), (190, 13), (194, 12), (196, 10), (197, 9)],
              fill=colour((224, 224, 216)))
    draw.line([(184, 11), (186, 12), (190, 12), (193, 11), (195, 10), (196, 9)],
              fill=colour((192, 192, 184)))


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
