"""Small fixed signs whose English lettering needs vertical or multiline layout.

Each entry is (rectangle, lines, direction, background). Vertical labels are
lettered as horizontal lines in rotated space, then rotated back; multiple
lines become Japanese-style right-to-left columns. Only lettering interiors
are cleared, preserving wood grain, paper, flag borders and all other art.
"""

from PIL import Image


PROPS = {
    'M170D.BIN:20': [
        ((206, 24, 238, 80), ['First'], 'vertical', 'flag'),
    ],
    'M440D.BIN:0': [
        # Cats/other actors cover the original board below y=64. Keep every
        # English letter above them, with horizontal names over their prices.
        ((72, 48, 112, 64), ['Fatty Tuna', '400'], 'horizontal', 'wood'),
        ((116, 48, 158, 64), ['Sea Urchin', '300'], 'horizontal', 'wood'),
        ((160, 48, 202, 64), ['Salmon Roe', '200'], 'horizontal', 'wood'),
        ((204, 48, 232, 64), ['Shrimp', '200'], 'horizontal', 'wood'),
    ],
    'M440D.BIN:1': [
        # This texture starts at screen x=240, not 256. Keep the entire egg
        # label here; an atlas-0 rectangle crossing x=240 is silently clipped.
        ((0, 48, 24, 64), ['Egg', '100'], 'horizontal', 'wood'),
    ],
    'GV16090D.BIN:1': [
        # 予約 / 本日 / 貸切: the bath is privately booked today.
        ((129, 2, 159, 18), ['Private', 'Today'], 'horizontal', 'placard'),
    ],
}

# All original ink, including the egg label's tail across the atlas seam.
SUSHI_ERASE = {
    'M440D.BIN:0': [(72, 48, 104, 76), (120, 48, 152, 76),
                    (168, 48, 216, 76), (232, 48, 240, 76)],
    'M440D.BIN:1': [(0, 48, 24, 76)],
}


def rectangles(key):
    return [entry[0] for entry in PROPS.get(key, [])] + SUSHI_ERASE.get(key, [])


def _clear(panel, kind):
    import gen_gfx

    px = panel.load()
    width, height = panel.size
    for y in range(height):
        if kind == 'flag':
            paper = max((px[x, y] for x in range(width) if px[x, y][3]), key=gen_gfx.luma)
            for x in range(width):
                if px[x, y][3]:
                    px[x, y] = paper
        elif kind == 'placard':
            # This sprite uses CLUT 2, where CLUT 0's purple indices 1/2/3
            # are dark ink and 4/5 are pale paper. Brightness in CLUT 0 is
            # therefore the wrong erasure criterion for this one sprite.
            paper = {(40, 24, 120, 255), (24, 8, 96, 255),
                     (232, 168, 104, 255), (184, 120, 64, 255)}
            lettering = {(104, 72, 176, 255), (72, 56, 160, 255), (48, 40, 136, 255)}
            background = {x: px[x, y] for x in range(width) if px[x, y] in paper}
            assert background, (panel.size, y, kind)
            for x in range(width):
                if px[x, y] in lettering:
                    px[x, y] = background[min(background, key=lambda sx: abs(sx - x))]
        elif kind == 'wood':
            # The original antialiasing includes dark brown, not only grey.
            # Keeping those pixels leaves Japanese strokes behind the English.
            # Borrow the unlettered wood colours from the same scanline.
            background = {x: px[x, y] for x in range(width)
                          if px[x, y][3] and px[x, y][0] >= 152}
            assert background, (panel.size, y, kind)
            for x in range(width):
                colour = px[x, y]
                if colour[0] < 152:
                    px[x, y] = background[min(background, key=lambda sx: abs(sx - x))]
        else:
            lumas = [gen_gfx.luma(px[x, y]) for x in range(width) if px[x, y][3]]
            if not lumas:
                continue
            threshold = (min(lumas) + max(lumas)) // 2
            background = {x: px[x, y] for x in range(width)
                          if px[x, y][3] and gen_gfx.luma(px[x, y]) >= threshold}
            assert background, (panel.size, y, kind)
            for x in range(width):
                if gen_gfx.luma(px[x, y]) < threshold:
                    px[x, y] = background[min(background, key=lambda sx: abs(sx - x))]


def draw(im, key, pal):
    import gen_gfx

    ink = min((c for rect, _, _, _ in PROPS[key] for c in im.crop(rect).getdata() if c[3]),
              key=gen_gfx.luma)
    for rect in SUSHI_ERASE.get(key, []):
        panel = im.crop(rect)
        _clear(panel, 'wood')
        im.paste(panel, rect[:2])
    for rect, lines, direction, background in PROPS[key]:
        panel = im.crop(rect)
        silhouette = panel.getchannel('A')
        if key not in SUSHI_ERASE:
            _clear(panel, background)
        if background == 'placard':
            ink = (48, 40, 136, 255)  # CLUT 2 index 3: (32,32,32)
        if direction == 'vertical':
            panel = panel.transpose(Image.Transpose.ROTATE_90)
        width, height = panel.size
        line_height = 16 if background == 'flag' else 8
        top = (height - len(lines) * line_height) // 2
        for i, line in enumerate(lines):
            options = {'pixel': 'credits7.txt', 'tight': True}
            mask = gen_gfx.mask(line, 7, options)
            if background == 'flag':
                mask = mask.resize((mask.width * 2, mask.height * 2), Image.Resampling.NEAREST)
            assert mask.width <= width and mask.height <= line_height, (key, line, mask.size)
            x = (width - mask.width) // 2
            y = top + i * line_height + (line_height - mask.height) // 2
            panel.paste(ink, (x, y, x + mask.width, y + mask.height), mask)
        if direction == 'vertical':
            panel = panel.transpose(Image.Transpose.ROTATE_270)
        panel.putalpha(silhouette)
        panel.putdata([c if c[3] else gen_gfx.CLEAR for c in panel.getdata()])
        assert set(panel.getdata()) <= pal, key
        im.paste(panel, rect[:2])
