"""Letter the ending fans and Kintaro's snow badge without changing their art.

The snow initial crosses the 240-pixel illustration seam. Its two disconnected
ink components are removed in assembled space; the separate oval border is
never part of the mask. Tiny snow placards remain unclassified.
"""
from PIL import Image, ImageFilter


FANS = {
    'EVT620D.BIN:0': [((107, 0, 139, 15), (112, 0), (103, 5)),
                     ((7, 62, 27, 79), (9, 62), (5, 72))],
    'EVT620D.BIN:1': [((43, 127, 76, 157), (51, 132), (39, 140))],
}
KEYS = [*FANS, 'EVT110D.BIN:0', 'EVT110D.BIN:1']
SNOW_RECTS = ((228, 105, 240, 136), (0, 105, 15, 136))


def rectangles(key):
    if key in FANS:
        return [rect for rect, _, _ in FANS[key]] + [
            (x, y, x + 15, y + 15) for _, (x, y), _ in FANS[key]]
    return [SNOW_RECTS[int(key[-1])]] if key.startswith('EVT110D.BIN:') else []


def snow_source():
    import gen_gfx

    im = Image.new('RGBA', (320, 256))
    for entry, width, x in ((0, 240, 0), (1, 80, 240)):
        source = gen_gfx.original(f'EVT110D.BIN:{entry}')[1]
        im.paste(source.crop((0, 0, width, 256)), (x, 0))
    return im


def components(im, region, background, wanted):
    pending = {(x, y) for y in range(region[1], region[3]) for x in range(region[0], region[2])
               if im.getpixel((x, y)) != background}
    mask = Image.new('L', im.size)
    found = set()
    while pending:
        seed = pending.pop()
        group, stack = {seed}, [seed]
        while stack:
            x, y = stack.pop()
            for p in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if p in pending:
                    pending.remove(p)
                    group.add(p)
                    stack.append(p)
        xs, ys = zip(*group)
        box = (min(xs), min(ys), max(xs) + 1, max(ys) + 1)
        if box in wanted:
            assert len(group) == wanted[box], (box, len(group))
            found.add(box)
            for p in group:
                mask.putpixel(p, 255)
    assert found == set(wanted), found
    return mask


def snow_mask(im):
    return components(im, (218, 96, 270, 141), (248, 248, 248, 255),
                      {(229, 105, 255, 128): 288, (228, 126, 249, 136): 125})


def fan_mask(im, rect, background):
    if rect[1] == 62:
        # The lower-right antialias fringe touches the fan ribs. Row bounds
        # stop at the inscription, leaving that connected woodwork intact.
        spans = [(15, 21), (11, 22), (9, 23), (8, 23), (9, 23), (8, 25),
                 (7, 26), (7, 26), (7, 26), (9, 25), (9, 26), (8, 27),
                 (9, 27), (9, 27), (11, 25), (11, 22), (12, 16)]
        mask = Image.new('L', im.size)
        for y, (x0, x1) in enumerate(spans, 62):
            for x in range(x0, x1):
                mask.putpixel((x, y), 255)
        return mask
    region, count = ((104, 0, 143, 18), 300) if rect[1] == 0 else ((40, 124, 80, 161), 661)
    return components(im, region, background, {rect: count})


def draw(im, key, palette):
    import gen_gfx

    if key in FANS:
        for rect, (x, y), sample in FANS[key]:
            # Borrow the untouched orange from this fan, not a global colour:
            # the right-hand fan is brighter than the two on the left atlas.
            background = im.getpixel(sample)
            ink = min(palette, key=lambda c: sum((a - b) ** 2 for a, b in
                                                zip(c[:3], (88, 8, 32))))
            im.paste(background, (0, 0, *im.size), fan_mask(im, rect, background))
            for n, word in enumerate(('FEST', 'IVAL')):
                mask = gen_gfx.mask(word, 7, {'pixel': 'credits7.txt', 'tight': True})
                assert mask.width <= 15 and mask.height == 7
                im.paste(ink, (x, y + 8 * n, x + mask.width, y + 8 * n + 7), mask)
    else:
        assembled = snow_source()
        assembled.paste((248, 248, 248, 255), (0, 0, *assembled.size), snow_mask(assembled))
        letter = gen_gfx.mask('K', 7, {'pixel': True, 'tight': True})
        letter = letter.resize((letter.width * 3, letter.height * 3), Image.Resampling.NEAREST)
        mask = Image.new('L', assembled.size)
        mask.paste(letter, (234, 108))
        assembled.paste((96, 96, 96, 255), (0, 0, *assembled.size), mask.filter(ImageFilter.MaxFilter(3)))
        assembled.paste((208, 232, 248, 255), (0, 0, *assembled.size), mask)
        entry = int(key[-1])
        x0, y0, x1, y1 = SNOW_RECTS[entry]
        offset = 240 * entry
        im.paste(assembled.crop((x0 + offset, y0, x1 + offset, y1)), (x0, y0))
    assert set(im.getdata()) <= palette
