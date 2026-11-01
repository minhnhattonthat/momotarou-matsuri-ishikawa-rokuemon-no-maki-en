"""Reletter fixed map signs in assembled tile space, preserving their frames.

The field renderer splits a sign into tiles, unlike ANM minigame sprites.
Each piece is (atlas x, y, width, height, assembled x, y). Most signs retain
their native tiles; relocated plaques delegate checked grid edits to gfx_field.
Palettes remain unchanged. Cold map captures remain the assembly oracle.
"""
from PIL import Image
import gfx_field


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

# Both engraved Tea patterns, found by their complete index-12/13 masks.
# M220D:0 is an exact image duplicate of GV16000D:0 and is generated too.
TEA_ATLASES = {
    'GF10000D': [(1, 81)], 'GF11000D': [(1, 81)], 'GV00000D': [(1, 81)],
    'GV01000D': [(169, 81)], 'GV02000D': [(233, 129)],
    'GV04000D': [(33, 153)], 'GV04002D': [(33, 153)],
    'GV06000D': [(169, 81)], 'GV08000D': [(33, 81)], 'GV09000D': [(41, 81)],
    'GV12000D': [(49, 81)], 'GV12002D': [(49, 81)], 'GV13000D': [(33, 81)],
    'GV16000D': [(33, 81)], 'GV20000D': [(33, 81)], 'GV20002D': [(33, 81)],
    'GV21000D': [(65, 81)], 'GV22000D': [(17, 81)], 'GV23000D': [(177, 81)],
    'GV24000D': [(33, 81)], 'GV30000D': [(1, 81)], 'GV30002D': [(1, 81)],
    'GV31000D': [(1, 81)], 'GV32000D': [(33, 81)], 'GV34000D': [(97, 81)],
    'GV36000D': [(1, 81)], 'GV38000D': [(33, 81)],
}
for _name, _positions in TEA_ATLASES.items():
    for _x, _y in _positions:
        _left = max(0, _x - 8)
        SIGNS.setdefault(f'{_name}.BIN:0', []).append(
            ('tea', [(_left, _y - 1, min(32, 256 - _left), 16, 0, 0)],
             (_x - _left, 1, _x - _left + 13, 14), ['Tea'], None, 'plaque'))

# と marks the といち屋 (Bank in the glossary). BANK is sixteen pixels wide;
# use a sixteen-pixel source span, whose outer columns are plain wood, rather
# than clipping the word to the Japanese glyph's thirteen-pixel ink bounds.
BANK_ATLASES = {
    'GF10000D': [(81, 81)], 'GF11000D': [(81, 81)], 'GV00000D': [(81, 81)],
    'GV01000D': [(233, 81)], 'GV02000D': [(233, 161)],
    'GV04000D': [(65, 153)], 'GV04002D': [(65, 153)], 'GV06000D': [(105, 65)],
    'GV08000D': [(49, 81)], 'GV09000D': [(73, 81)],
    'GV12000D': [(1, 81)], 'GV12002D': [(1, 81)], 'GV13000D': [(1, 81)],
    'GV16000D': [(65, 81)], 'GV20000D': [(65, 81)], 'GV20002D': [(65, 81)],
    'GV21000D': [(33, 81)], 'GV22000D': [(49, 81)], 'GV23000D': [(145, 81)],
    'GV31000D': [(81, 81)], 'GV34000D': [(81, 81)], 'GV36000D': [(17, 81)],
}
for _name, _positions in BANK_ATLASES.items():
    for _x, _y in _positions:
        _left = max(0, _x - 8)
        SIGNS.setdefault(f'{_name}.BIN:0', []).append(
            ('bank', [(_left, _y - 1, min(32, 256 - _left), 16, 0, 0)],
             (_x - _left - 1, 1, _x - _left + 15, 14), ['Bank'], None, 'plaque'))


# These smaller Games boards use the same engraved ink/highlight indices as
# the roof plaques. Their actual map tiles are contiguous 64x16 strips; the
# unused lookalike tiles elsewhere in these atlases are not the runtime source.
ENGRAVED_GAMES = [
    ('GV02000D.BIN:2', 64, 184), ('GV04000D.BIN:0', 176, 192),
    ('GV04002D.BIN:0', 176, 192), ('GV09000D.BIN:3', 16, 64),
    ('GV21000D.BIN:0', 112, 80), ('GV23000D.BIN:2', 128, 208),
    ('GV36000D.BIN:0', 160, 160),
]
for _key, _u, _v in ENGRAVED_GAMES:
    SIGNS.setdefault(_key, []).append(
        ('games', [(_u, _v, 64, 16, 0, 0)], (9, 0, 53, 14),
         ['Games'], None, 'engraved'))

# Complete index-12/13 glyph masks locate these otherwise different atlases.
# The compact seven-pixel lettering retains the full shop names and every
# surrounding board edge. Night artwork uses EDIT_PALETTES as for its Inn.
PRODUCE_ATLASES = {
    'GV01000D': (194, 177), 'GV04000D': (106, 185),
    'GV04002D': (106, 185), 'GV06000D': (18, 81),
    'GV12000D': (186, 145), 'GV12002D': (186, 145),
    'GV13000D': (106, 81), 'GV30000D': (114, 65), 'GV30002D': (114, 65),
}
for _name, (_x, _y) in PRODUCE_ATLASES.items():
    SIGNS.setdefault(f'{_name}.BIN:0', []).append(
        ('produce', [(_x - 9, _y - 1, 64, 16, 0, 0)], (9, 1, 50, 14),
         ['Produce'], None, 'plaque'))

FISH_ATLASES = {
    'GV09000D': (120, 65, 13), 'GV22000D': (168, 81, 13),
    'GV20000D': (152, 81, 14), 'GV20002D': (152, 81, 14),
}
for _name, (_x, _y, _height) in FISH_ATLASES.items():
    SIGNS.setdefault(f'{_name}.BIN:0', []).append(
        ('fish', [(_x - 8, _y - 1, 64, 16, 0, 0)], (8, 1, 40, 1 + _height),
         ['Fish Shop'], None, 'plaque'))


# Map45 draws these as pairs of 16-pixel tiles. Weapons needs the full
# thirty-pixel interior; extend the wood behind it within the existing board.
# The complete index-12/13 masks occur only here in the original archive sweep.
EQUIPMENT_SIGNS = [('weapons', 0, 'Weapons'), ('armor', 32, 'Armor'), ('shoes', 64, 'Shoes')]
for _label, _u, _word in EQUIPMENT_SIGNS:
    SIGNS['GV01000D.BIN:0'].append(
        (_label, [(_u, 80, 32, 16, 0, 0)], (1, 1, 31, 14), [_word], None,
         'wide_plaque' if _label == 'weapons' else 'equipment'))

# The bath-town plaque's right edge is stored separately below the main
# strip. Both layouts assemble the same 48x32 board; keep its edge and posts.
BATH_SIGNS = {
    'GV36000D.BIN:0': [(96, 64, 48, 32, 0, 0)],
    'GV16000D.BIN:3': [(160, 72, 32, 32, 0, 0),
                      (0, 224, 16, 16, 32, 0), (16, 224, 16, 16, 32, 16)],
}
for _key, _pieces in BATH_SIGNS.items():
    SIGNS[_key].append(('bath', _pieces, (9, 8, 39, 28), ['Bath'], None, 'engraved'))

for _key, _plan in gfx_field.PLANS.items():
    SIGNS.setdefault(_key, []).append(
        (_plan['label'], gfx_field.pieces(_key), (0, 0, 48, 16), [_plan['word']], None, 'relocated'))


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
        if kind == 'relocated':
            gfx_field.draw(im, key, pal)
            continue
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
        elif kind in ('plaque', 'engraved', 'wide_plaque', 'equipment'):
            # Remove engraved strokes and highlights using only wood colours.
            # Wide plaques also extend wood within their declared interior.
            import gfx
            colours = gfx.palette(gen_gfx.original(key)[0], gen_gfx.EDIT_PALETTES.get(key, 0))
            colour = colours[12]
            ink = set(colours[12:14])
            wood_colours = set(colours[7:11])
            for y in range(y0, y1):
                # Wide labels can occupy the whole interior: sample untouched
                # wood in the original row before replacing any pixels.
                wood = {x: px[x, y] for x in range(board.width)
                        if px[x, y] in wood_colours and
                        (kind in ('wide_plaque', 'equipment') or not x0 <= x < x1)}
                assert wood, (key, y)
                for x in range(x0, x1):
                    if px[x, y] in ink or (kind == 'wide_plaque' and 3 <= y <= 11):
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
        scale = 2 if kind in ('wood', 'engraved') else 1
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
