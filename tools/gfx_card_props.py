"""Card signs and costume initials, with explicit masks in illustration pixels.

The small kana badges are already initials in Japanese: K for Kintaro, P for
Poverty God. Enma's crown uses E. They are emblems, not shortened dialogue names.
Each polygon bounds only the printed face, preserving the surrounding object.
Background and ink use the nearest original palette colours.
"""
from PIL import Image, ImageDraw


# card: [(id, source reading, polygon, background RGB, ink RGB, lines,
#         drawing box, rotation, integer glyph scale)]
PROPS = {
    6: [('crown', '閻', [(122, 23), (126, 23), (128, 29), (121, 29)],
         (80, 72, 72), (208, 88, 64), ['E'], (122, 23, 127, 30), 0, 1)],
    18: [('badge', 'き', [(90, 80), (98, 80), (100, 89), (97, 95), (90, 96), (86, 91)],
          (248, 248, 200), (64, 64, 64), ['K'], (91, 81, 98, 90), 0, 1)],
    19: [('crown', '閻', [(82, 16), (88, 16), (89, 22), (81, 22)],
          (80, 72, 72), (208, 88, 64), ['E'], (82, 16, 89, 23), 0, 1)],
    22: [('cloth', 'び', [(139, 100), (158, 100), (159, 112), (149, 114), (138, 113), (134, 110)],
          (248, 248, 248), (64, 64, 64), ['P'], (143, 101, 153, 109), 0, 1)],
    25: [('crown', '閻', [(73, 20), (80, 20), (80, 27), (73, 26)],
          (80, 72, 72), (208, 88, 64), ['E'], (74, 20, 80, 27), 0, 1)],
    35: [('sake', '酒', [(39, 101), (61, 99), (66, 111), (41, 114)],
          (176, 192, 216), (64, 64, 64), ['Sake'], (42, 102, 62, 110), 0, 1)],
    42: [('cloth', 'び', [(133, 100), (156, 99), (159, 108), (140, 110), (130, 107)],
          (248, 248, 248), (64, 64, 64), ['P'], (139, 100, 153, 108), 0, 1)],
    47: [('crown', '閻', [(122, 19), (128, 19), (129, 26), (122, 26)],
          (80, 72, 72), (208, 88, 64), ['E'], (123, 19, 128, 26), 0, 1)],
    48: [('badge', 'き', [(70, 103), (77, 102), (79, 113), (74, 114), (69, 111)],
          (248, 248, 200), (64, 64, 64), ['K'], (71, 103, 78, 111), 0, 1)],
    61: [('badge', 'き', [(101, 84), (111, 85), (111, 94), (102, 94)],
          (248, 248, 200), (64, 64, 64), ['K'], (103, 85, 110, 93), 0, 1)],
    62: [('price', '千両', [(78, 99), (87, 92), (109, 103), (97, 116)],
          (248, 248, 248), (64, 64, 64), ['1000', 'ryo'], (81, 94, 108, 118), 320, 1)],
    68: [('dumplings', 'だんご', [(42, 0), (71, 0), (79, 34), (75, 49), (58, 49), (53, 29)],
          (248, 248, 248), (64, 64, 64), ['Dumplings'], (55, 5, 70, 44), 270, 1),
         ('cloth', 'び', [(109, 102), (131, 103), (134, 115), (108, 115)],
          (248, 248, 248), (64, 64, 64), ['P'], (115, 104, 127, 113), 0, 1)],
    72: [('cloth', 'び', [(108, 91), (116, 92), (128, 95), (130, 105), (107, 105)],
          (248, 248, 248), (64, 64, 64), ['P'], (114, 96, 125, 104), 0, 1)],
    73: [('puffer', 'ふ', [(85, 17), (115, 17), (115, 44), (85, 44)],
          (248, 248, 248), (64, 64, 64), ['Puffer'], (86, 24, 113, 35), 0, 1),
         ('fish', 'ぐ', [(136, 17), (170, 17), (170, 49), (136, 49)],
          (248, 248, 248), (64, 64, 64), ['fish'], (140, 25, 163, 35), 0, 1)],
    77: [('crown', '閻', [(92, 21), (99, 21), (99, 27), (92, 27)],
          (80, 72, 72), (208, 88, 64), ['E'], (93, 21, 98, 28), 0, 1)],
    85: [('crown', '閻', [(145, 12), (150, 13), (150, 19), (143, 18)],
          (80, 72, 72), (208, 88, 64), ['E'], (144, 12, 150, 19), 0, 1)],
    86: [('cloth', 'び', [(114, 100), (136, 100), (137, 108), (114, 111)],
          (248, 248, 248), (64, 64, 64), ['P'], (120, 102, 131, 110), 0, 1)],
    97: [('badge', 'き', [(145, 85), (153, 84), (159, 99), (159, 102), (148, 104), (143, 100)],
          (248, 248, 200), (64, 64, 64), ['K'], (146, 85, 158, 100), 0, 2)],
}


def rectangles(card):
    result = []
    for name, _, polygon, _, _, _, rect, _, _ in PROPS.get(card, []):
        xs, ys = zip(*polygon)
        pad = 2 if name == 'crown' else 0
        result.extend([(min(xs) - pad, min(ys) - pad, max(xs) + 1 + pad, max(ys) + 1 + pad), rect])
    return result


def draw(image, card, palette):
    import gen_gfx

    for name, _, polygon, background_rgb, rgb, lines, rect, angle, scale in PROPS.get(card, []):
        mask = Image.new('L', image.size)
        ImageDraw.Draw(mask).polygon(polygon, fill=255)
        if name == 'crown':
            xs, ys = zip(*polygon)
            for y in range(min(ys) - 2, max(ys) + 3):
                for x in range(min(xs) - 2, max(xs) + 3):
                    r, g, b, _ = image.getpixel((x, y))
                    if r - g > 40 and r - b > 40 and g < 130:
                        mask.putpixel((x, y), 255)
        if name in ('puffer', 'fish'):
            # Blue wave decoration under the lettering is not part of the ink.
            for y in range(128):
                for x in range(208):
                    r, g, b, _ = image.getpixel((x, y))
                    if b > r + 8:
                        mask.putpixel((x, y), 0)
        background = min((c for c in palette if c[3]),
                         key=lambda c: sum((a - b) ** 2 for a, b in zip(c[:3], background_rgb)))
        image.paste(background, (0, 0, *image.size), mask)
        ink = min((c for c in palette if c[3]),
                  key=lambda c: sum((a - b) ** 2 for a, b in zip(c[:3], rgb)))
        x0, y0, x1, y1 = rect
        width, height = x1 - x0, y1 - y0
        font = True if name in ('badge', 'cloth', 'crown') else 'credits7.txt'
        rendered = [gen_gfx.mask(line, 7, {'pixel': font, 'tight': True}) for line in lines]
        line_height = 8 * scale
        canvas = Image.new('L', (max(m.width for m in rendered) * scale,
                                 len(lines) * line_height - scale))
        for line_number, letters in enumerate(rendered):
            if scale != 1:
                letters = letters.resize((letters.width * scale, letters.height * scale),
                                         Image.Resampling.NEAREST)
            canvas.paste(letters, ((canvas.width - letters.width) // 2, line_number * line_height))
        if angle:
            canvas = canvas.rotate(angle, expand=True)
        assert canvas.width <= width and canvas.height <= height, (card, name, canvas.size, rect)
        x, y = x0 + (width - canvas.width) // 2, y0 + (height - canvas.height) // 2
        image.paste(ink, (x, y, x + canvas.width, y + canvas.height), canvas)
