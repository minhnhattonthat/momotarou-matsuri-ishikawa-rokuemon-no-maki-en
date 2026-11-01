"""Reletter fixed map signs in assembled tile space, preserving their frames.

The field renderer splits a sign into tiles, unlike ANM minigame sprites.
Each piece is (atlas x, y, width, height, assembled x, y). No tile records,
palettes or collision maps change. Cold map captures remain the assembly oracle.
"""
from PIL import Image


SIGNS = {
    'GV02000D.BIN:2': [
        ('contest', [(184, 192, 72, 16, 0, 0), (184, 208, 72, 16, 72, 0)],
         (3, 2, 141, 14), ["World's Greatest Pun Contest"], (120, 112, 80, 255), 'panel'),
    ],
    'GV13000D.BIN:2': [
        ('contest', [(0, 0, 144, 16, 0, 0)], (3, 2, 141, 14),
         ["World's Greatest Pun Contest"], (64, 56, 40, 255), 'panel'),
    ],
    'GV12000D.BIN:1': [
        ('games', [(128, 0, 80, 48, 0, 0)], (23, 16, 69, 31),
         ['Games'], (56, 32, 0, 255), 'wood'),
    ],
    'GV12002D.BIN:1': [
        ('games', [(128, 0, 80, 48, 0, 0)], (23, 16, 69, 31),
         ['Games'], (56, 32, 0, 255), 'wood'),
    ],
    'GV13000D.BIN:1': [
        ('games', [(96, 176, 80, 48, 0, 0)], (23, 16, 69, 31),
         ['Games'], (56, 32, 0, 255), 'wood'),
    ],
    'GV32000D.BIN:1': [
        ('games', [(64, 128, 80, 48, 0, 0)], (23, 16, 69, 31),
         ['Games'], (56, 32, 0, 255), 'wood'),
    ],
    'GV34000D.BIN:1': [
        ('games', [(32, 208, 80, 48, 0, 0)], (23, 16, 69, 31),
         ['Games'], (56, 32, 0, 255), 'wood'),
    ],
    'GV16000D.BIN:3': [
        ('games', [(0, 40, 96, 48, 0, 0)], (23, 16, 73, 31),
         ['Games'], (56, 32, 0, 255), 'wood'),
    ],
    'GV22000D.BIN:1': [
        # The right edge of the board is stored below the main strip.
        ('games', [(128, 48, 64, 32, 0, 0), (176, 96, 32, 32, 64, 0)], (23, 16, 69, 31),
         ['Games'], (56, 32, 0, 255), 'wood'),
    ],
    'GV16090D.BIN:1': [
        ('men', [(0, 0, 56, 32, 0, 0)], (5, 5, 54, 27),
         ["Men's", 'Bath'], (208, 208, 208, 255), 'curtain'),
        ('women', [(64, 0, 56, 32, 0, 0)], (5, 5, 54, 27),
         ["Women's", 'Bath'], (208, 208, 208, 255), 'curtain'),
    ],
}

# The same roof-mounted inn plaque is present in these otherwise different
# atlases. Keep each source explicit; whole-image duplicate expansion alone
# cannot find a sign embedded among different buildings.
INN_ATLASES = {
    'GF10000D': [(225, 49)], 'GF11000D': [(225, 49)], 'GV00000D': [(225, 49)],
    'GV01000D': [(201, 81)], 'GV02000D': [(233, 145)],
    'GV04000D': [(121, 65), (81, 153)], 'GV04002D': [(81, 153)],
    'GV06000D': [(225, 49), (225, 177)], 'GV08000D': [(209, 49)],
    'GV09000D': [(217, 49)], 'GV12000D': [(33, 81)], 'GV12002D': [(33, 81)],
    'GV13000D': [(161, 177), (225, 177)], 'GV16000D': [(81, 81)],
    'GV21000D': [(49, 81)], 'GV22000D': [(33, 81)], 'GV23000D': [(193, 81)],
    'GV20000D': [(1, 81)], 'GV20002D': [(1, 81)], 'GV24000D': [(225, 49), (1, 81)],
    'GV30000D': [(17, 81)], 'GV30002D': [(17, 81)], 'GV31000D': [(225, 49)],
    'GV32000D': [(1, 81), (225, 49)], 'GV38000D': [(225, 49), (1, 81)],
    'GV34000D': [(129, 81)], 'GV36000D': [(49, 81)],
}
for _name, _positions in INN_ATLASES.items():
    SIGNS[f'{_name}.BIN:0'] = []
    for _index, (_x, _y) in enumerate(_positions):
        _left = max(0, _x - 8)
        SIGNS[f'{_name}.BIN:0'].append(
            ('inn' if _index == 0 else f'inn{_index + 1}',
             [(_left, _y - 1, min(32, 256 - _left), 16, 0, 0)],
             (_x - _left, 1, _x - _left + 13, 14), ['Inn'], None, 'plaque'))


def assemble(im, pieces):
    out = Image.new('RGBA', (max(x + w for _, _, w, _, x, _ in pieces),
                             max(y + h for _, _, _, h, _, y in pieces)))
    for u, v, w, h, x, y in pieces:
        out.paste(im.crop((u, v, u + w, v + h)), (x, y))
    return out


def draw(im, key, pal):
    from collections import Counter
    import gen_gfx

    for _, pieces, rect, lines, colour, kind in SIGNS[key]:
        board = assemble(im, pieces)
        px = board.load()
        x0, y0, x1, y1 = rect
        if kind == 'panel':
            background = Counter(board.crop(rect).getdata()).most_common(1)[0][0]
            for y in range(y0, y1):
                for x in range(x0, x1):
                    px[x, y] = background
        elif kind == 'wood':
            # Index 12 is dark in CLUT 0 but cream in the actual roof/sign
            # CLUTs 9-11. Index 1 would become blue/purple at runtime.
            # Borrow clean wood immediately left of the lettering. Narrow
            # boards expose roof pixels in that band, so admit only wood
            # indices 7-11 (expressed in the editing CLUT's colours).
            wood_colours = {(168, 112, 56, 255), (152, 96, 32, 255), (136, 80, 32, 255),
                            (120, 64, 24, 255), (88, 40, 0, 255)}
            for y in range(y0, y1):
                wood = [px[x, y] for x in range(17, x0) if px[x, y] in wood_colours]
                assert wood, (key, y)
                for x in range(x0, x1):
                    px[x, y] = wood[(x - x0) % len(wood)]
        elif kind == 'plaque':
            # Remove both the engraved stroke and its highlight. Sample only
            # wood colours, leaving the carved board edge and roof untouched.
            import gfx
            colours = gfx.palette(gen_gfx.original(key)[0], gen_gfx.EDIT_PALETTES.get(key, 0))
            colour = colours[12]
            ink = set(colours[12:14])
            wood_colours = set(colours[7:11])
            for y in range(y0, y1):
                wood = {x: px[x, y] for x in range(board.width)
                        if px[x, y] in wood_colours and not x0 <= x < x1}
                assert wood, (key, y)
                for x in range(x0, x1):
                    if px[x, y] in ink:
                        px[x, y] = wood[min(wood, key=lambda sx: abs(sx - x))]
        else:
            # The original lettering is grey; keep the coloured cloth and its
            # transparent silhouette. Borrow cloth only from the same row.
            for y in range(y0, y1):
                cloth = {x: px[x, y] for x in range(x0, x1)
                         if px[x, y][3] and max(px[x, y][:3]) - min(px[x, y][:3]) > 24}
                assert cloth, (key, y)
                for x in range(x0, x1):
                    c = px[x, y]
                    if c[3] and max(c[:3]) - min(c[:3]) <= 24:
                        px[x, y] = cloth[min(cloth, key=lambda sx: abs(sx - x))]
        scale = 2 if kind == 'wood' else 1
        height = (len(lines) * 8 - 1) * scale
        assert height <= y1 - y0
        for i, line in enumerate(lines):
            mask = gen_gfx.mask(line, 7, {'pixel': 'credits7.txt', 'tight': True})
            if scale != 1:
                mask = mask.resize((mask.width * scale, mask.height * scale), Image.Resampling.NEAREST)
            assert mask.width <= x1 - x0, (key, line)
            xy = (x0 + (x1 - x0 - mask.width) // 2, y0 + (y1 - y0 - height) // 2 + i * 8 * scale)
            board.paste(colour, (*xy, xy[0] + mask.width, xy[1] + mask.height), mask)
        assert set(board.getdata()) <= pal
        for u, v, w, h, x, y in pieces:
            im.paste(board.crop((x, y, x + w, y + h)), (u, v))
