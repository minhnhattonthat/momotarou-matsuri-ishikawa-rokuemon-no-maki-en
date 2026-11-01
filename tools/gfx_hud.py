"""Whole English HUD words in unused M990D pixels, preserving shared fragments.

The old Win/Loss and Bonus rectangles have partial users, including an 8x8
piece and announcement items with an external palette. Keep every old pixel;
redirect only the named complete HUD items to transparent, unused space.
"""
import hashlib
import struct

ANM_SHA1 = '1aa343767e38cad3fdb959eb84e8854a0ebf78d6'
RECT = (48, 192, 160, 216)
PANEL_RECT = (192, 152, 248, 184)
PANEL_SHA1 = 'b7588abd46fc698482e28f3e53599fe032b9dda1'
WORDS = {20: 'Total', 31: 'Win', 32: 'Loss', 34: 'Floor',
         49: 'Bonus', 73: 'Match', 85: 'sec', 78: 'items',
         79: 'pieces', 77: 'times', 33: 'min', 48: 'later'}


def mask(text):
    import gen_gfx
    return gen_gfx.fit(text, 28, 8, gen_gfx.HUD_CONDENSED)


def rect(item):
    index = list(WORDS).index(item)
    return 48 + index % 4 * 28, 192 + index // 4 * 8, mask(WORDS[item]).width, 8


def draw(image, palette):
    white = (248, 248, 248, 255)
    if white not in palette or image.crop(RECT).getchannel('A').getbbox():
        raise ValueError('HUD destination must be transparent and support white ink')
    for item, text in WORDS.items():
        u, v, _, _ = rect(item)
        image.paste(white, (u, v), mask(text))


def patch(data):
    if hashlib.sha1(data).hexdigest() != ANM_SHA1:
        raise ValueError('unexpected original M990D HUD ANM')
    out = bytearray(data)
    table, = struct.unpack_from('<I', data, 8)
    for item in WORDS:
        start, = struct.unpack_from('<I', data, table + item * 4)
        if struct.unpack_from('<I', data, start)[0] != 1:
            raise ValueError('HUD word must be a single complete sprite')
        # Keep the original left edge and vertical centre (16px -> 8px).
        top, = struct.unpack_from('<h', data, start + 4 + 18)
        for field, value in zip((1, 2, 3, 4, 9), (*rect(item), top + 4)):
            struct.pack_into('<H', out, start + 4 + field * 2, value & 0xFFFF)
    return bytes(out)


def draw_panel(image):
    """Extend M34's existing 48px counter panel to 56px, preserving its borders."""
    if image.crop((240, 152, 248, 184)).getchannel('A').getbbox():
        raise ValueError('counter panel extension is not transparent')
    panel = image.crop((192, 152, 240, 184))
    image.paste(panel.crop((32, 0, 48, 32)), (232, 152))
    image.paste(panel.crop((24, 0, 32, 32)), (224, 152))


def patch_panel(data):
    if hashlib.sha1(data).hexdigest() != PANEL_SHA1:
        raise ValueError('unexpected original M340D counter ANM')
    out = bytearray(data)
    table, = struct.unpack_from('<I', data, 8)
    start, = struct.unpack_from('<I', data, table + 9 * 4)
    if struct.unpack_from('<I', data, start)[0] != 1 or struct.unpack_from('<H', data, start + 10)[0] != 48:
        raise ValueError('unexpected counter panel geometry')
    struct.pack_into('<H', out, start + 10, 56)
    return bytes(out)
