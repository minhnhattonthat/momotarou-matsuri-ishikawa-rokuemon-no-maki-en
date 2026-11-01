"""English M990D result words and their checked ANM assembly.

The Japanese atlas shares parts of names and ordinal suffixes. English uses
dedicated word rectangles in the same texture page; HUDs, faces and palettes
stay in place. Geometry edits are accepted only against the pinned original
ANM, and preserve every record's flags, CLUT, page and scale.
"""
import hashlib
import struct

ANM_SHA1 = 'f68f9b95c19678d6caaeefd5c3d34e36ccb8616c'
# x, y, width, height. Reuse only the large Japanese-letter regions.
WORDS = {
    'Momotaro': (0, 48, 96, 24),
    'Kintaro': (96, 48, 80, 24),
    'Urashima': (176, 48, 80, 24),
    'Yashahime': (0, 72, 104, 24),
    'Red Oni': (104, 72, 72, 24),
    'Blue Oni': (176, 72, 80, 24),
    'Round': (0, 96, 80, 24),
    'Try': (80, 96, 48, 24),
    'Question': (128, 96, 112, 24),
    '!': (240, 96, 8, 24),
    'wins': (0, 120, 48, 24),
    'win': (64, 120, 40, 24),
    'Win': (120, 120, 48, 24),
    'Lose': (176, 120, 56, 24),
    'and': (128, 144, 40, 32),
}
for _n in range(1, 11):
    WORDS[str(_n)] = ((_n - 1) * 24, 216, 24, 32) if _n <= 6 else ((_n - 7) * 24, 144, 24, 32)

CLEAR_RECTS = [
    (0, 48, 256, 144), (0, 144, 192, 176), (176, 176, 208, 208),
    (0, 216, 144, 248), (240, 160, 248, 192), (152, 32, 184, 48),
]


def line(words, y=-12):
    """Centred sequence; punctuation touches the preceding word's rectangle."""
    width = sum(WORDS[word][2] for word in words)
    x = -(width // 2)
    result = []
    for word in words:
        result.append((word, x, y + (24 - WORDS[word][3]) // 2))
        x += WORDS[word][2]
    return result


LAYOUTS = {}
for _base, _word in ((21, 'Round'), (41, 'Try'), (61, 'Question')):
    for _n in range(1, 11):
        LAYOUTS[_base + _n - 1] = line([_word, str(_n), '!'])
for _item, _name in ((31, 'Momotaro'), (32, 'Kintaro'), (33, 'Urashima'), (34, 'Yashahime')):
    LAYOUTS[_item] = line([_name, 'wins', '!'])
for _item, _first, _second in ((35, 'Momotaro', 'Urashima'), (36, 'Kintaro', 'Yashahime'),
                               (37, 'Momotaro', 'Red Oni'), (51, 'Kintaro', 'Blue Oni')):
    LAYOUTS[_item] = line([_first, 'and', _second], -32) + line(['win', '!'], 8)
LAYOUTS[38] = line(['Win', '!'])
LAYOUTS[39] = line(['Lose', '!'])


def changes(data):
    """(item, sprite, field, before, after), restricted to UV/size/position."""
    if hashlib.sha1(data).hexdigest() != ANM_SHA1:
        raise ValueError('unexpected original M990D result ANM')
    result = []
    for item, layout in LAYOUTS.items():
        start, = struct.unpack_from('<I', data, 20 + item * 4)
        count, = struct.unpack_from('<I', data, start)
        if len(layout) > count:
            raise ValueError(f'result {item}: too few sprite records')
        for sprite in range(count):
            if sprite < len(layout):
                word, x, y = layout[sprite]
                u, v, w, h = WORDS[word]
            else:
                # Retain record count/timing, but sample a transparent texel.
                u, v, w, h, x, y = 255, 255, 1, 1, 0, 0
            for field, after in zip((1, 2, 3, 4, 8, 9), (u, v, w, h, x, y)):
                before, = struct.unpack_from('<H', data, start + 4 + sprite * 28 + field * 2)
                if before != after & 0xFFFF:
                    result.append((item, sprite, field, before, after))
    return result


def draw(image, palette):
    import gen_gfx
    from PIL import Image
    # Borrow the original large-letter gradient, so every runtime CLUT still
    # produces its own colour. The generator imports exact palette indices.
    source = image.crop((0, 48, 96, 80))
    for rect in CLEAR_RECTS:
        image.paste(gen_gfx.CLEAR, rect)
    for word, (x, y, w, h) in WORDS.items():
        patch = source.resize((w, h), Image.Resampling.NEAREST)
        gen_gfx.draw(patch, 0, 0, w, h, word, {'size': 25, 'wdth': 75}, palette)
        image.paste(patch, (x, y))


def generate():
    """Regenerate the unique M990D:0 atlas without rescanning all card art."""
    import gen_gfx
    import gfx
    texture, image = gen_gfx.original('M990D.BIN:0')
    palette = {c if c[3] else gen_gfx.CLEAR for c in gfx.palette(texture, 0)}
    for x0, y0, x1, y1, text, options in gen_gfx.LABELS['M990D.BIN:0']:
        gen_gfx.draw(image, x0, y0, x1, y1, text, options, palette)
    draw(image, palette)
    image.save(gfx.EN / 'M990D_0.png')


if __name__ == '__main__':
    generate()
