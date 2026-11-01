"""Reviewed illustration lettering, applied after the card's marginal phrase.

Coordinates in gfx/card_art.tsv are in the original 208x128 illustration.
Separate erase and drawing bounds preserve nearby props and motion lines.
Only declared regions may change; palettes, sprite records and captions do
not change. Fredoka lettering falls back to the MIT pixel font below 9 pixels.
"""
import csv

from collections import deque

from PIL import Image, ImageFilter

import gfx


def boxes(value):
    return [tuple(map(int, rect.split(','))) for rect in value.split(';')]


def rows():
    with (gfx.ROOT / 'gfx/card_art.tsv').open(encoding='utf-8', newline='') as stream:
        result = list(csv.DictReader(stream, delimiter='\t'))
    seen = set()
    for row in result:
        row['card'] = int(row['card'])
        row['erase'] = boxes(row['erase'])
        row['draw'] = boxes(row['draw'])[0]
        row['rotate'] = int(row['rotate'])
        assert row['id'] not in seen, row
        seen.add(row['id'])
        for x0, y0, x1, y1 in [*row['erase'], row['draw']]:
            assert 0 <= x0 < x1 <= 208 and 0 <= y0 < y1 <= 128, row
    return result


def rectangles(card):
    return [rect for row in rows() if row['card'] == card
            for rect in [*row['erase'], row['draw']]]


def allowed_rectangles(card):
    """Fixed reviewed bounds including the small original antialias fringe."""
    return [(max(0, x0 - 3), max(0, y0 - 3), min(208, x1 + 3), min(128, y1 + 3))
            for x0, y0, x1, y1 in rectangles(card)]


def erase_mask(image, row):
    """Pick isolated ink components; never clear part of an actor or prop.

    Bounding boxes are selection windows, not paint buckets. A handwritten
    stroke's antialias pixels can extend past them. Whole connected components
    remove that fringe while rejecting the much larger illustration component.
    """
    candidates = set()
    for y in range(128):
        for x in range(208):
            colour = image.getpixel((x, y))[:3]
            if max(colour) <= 184 and max(colour) - min(colour) <= 32:
                candidates.add((x, y))
    selected = Image.new('L', image.size)
    windows = row['erase']
    while candidates:
        seed = min(candidates, key=lambda point: (point[1], point[0]))
        candidates.remove(seed)
        pending = deque([seed])
        component = [seed]
        while pending:
            x, y = pending.popleft()
            for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1),
                           (-1, -1), (-1, 1), (1, -1), (1, 1)):
                point = x + dx, y + dy
                if point in candidates:
                    candidates.remove(point)
                    pending.append(point)
                    component.append(point)
        inside = sum(any(x0 <= x < x1 and y0 <= y < y1 for x0, y0, x1, y1 in windows)
                     for x, y in component)
        if inside >= len(component) * 0.5 and len(component) <= 1000:
            for point in component:
                selected.putpixel(point, 255)
    selected = selected.filter(ImageFilter.MaxFilter(5))
    if row['id'] == '042_thud_l':
        # The last kana approaches the top door-frame corner. Its final
        # antialias pixels must not eat the frame's horizontal wooden edge.
        selected.paste(0, (60, 29, 100, 50))
    if row['id'] == '033_scratch_l':
        selected.paste(0, (30, 29, 44, 40))  # hand motion, not lettering
    if row['id'] == '091_glub_l':
        selected.paste(0, (10, 31, 26, 42))  # the small underwater bubble
    selected.paste(0, (208, 0, image.width, image.height))
    selected.paste(0, (0, 128, image.width, image.height))
    return selected


def clear_water(image, mask):
    """Extend nearby unlettered pale water into the strokes, retaining colours."""
    x0, y0, x1, y1 = mask.getbbox()
    x0, y0 = max(0, x0 - 4), max(0, y0 - 4)
    x1, y1 = min(208, x1 + 4), min(128, y1 + 4)
    pending, known = deque(), {}
    for y in range(y0, y1):
        for x in range(x0, x1):
            colour = image.getpixel((x, y))
            if not mask.getpixel((x, y)) and min(colour[:3]) >= 224:
                known[x, y] = colour
                pending.append((x, y))
    assert pending, 'no unlettered water surrounding the stroke'
    while pending:
        x, y = pending.popleft()
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if x0 <= nx < x1 and y0 <= ny < y1 and (nx, ny) not in known:
                known[nx, ny] = known[x, y]
                pending.append((nx, ny))
                if mask.getpixel((nx, ny)):
                    image.putpixel((nx, ny), known[x, y])


def draw(image, card, palette):
    import gen_gfx

    paper = (248, 248, 248, 255)
    ink = min((colour for colour in palette if colour[3]),
              key=lambda colour: sum((v - 64) ** 2 for v in colour[:3]))
    original = image.copy()
    for row in rows():
        if row['card'] != card:
            continue
        assert paper in palette, row
        mask = erase_mask(original, row)
        assert mask.getbbox(), row['id']
        if card == 91:
            clear_water(image, mask)
        else:
            image.paste(paper, (0, 0, *image.size), mask)
        x0, y0, x1, y1 = row['draw']
        width, height = x1 - x0, y1 - y0
        if row['rotate'] in (90, 270):
            width, height = height, width
        options = {'size': 14, 'outline': 0, 'wght': 600, 'wdth': 75}
        lettering = gen_gfx.fit(row['en'], width, height, options)
        if lettering.height < 11:
            lettering = gen_gfx.mask(row['en'], 7, {'pixel': 'credits7.txt', 'tight': True})
        assert lettering.width <= width and lettering.height <= height, (row['id'], lettering.size)
        if row['rotate']:
            lettering = lettering.rotate(row['rotate'], expand=True)
        x = x0 + (x1 - x0 - lettering.width) // 2
        y = y0 + (y1 - y0 - lettering.height) // 2
        image.paste(ink, (x, y, x + lettering.width, y + lettering.height), lettering)
