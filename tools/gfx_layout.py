"""Checked ANM field edits for translated graphics; no animation timing or code edits.

M990D:3: rejoin START's two adjacent atlas fragments, remove its borrowed dash,
and centre GAME START. Centre the level number and ! after removing the Japanese
level suffix. gfx_results also repacks the 40 winner/ordinal layouts into English
word order. All counts, table offsets, palettes, scales and other items remain.
M590D:9 relocates Lose! instead of retaining a Japanese fragment shared with actor art.
M230D:20/21 use whole English race labels/names in previously unused font pixels.
"""
import hashlib
import struct
from pathlib import Path

import gfx_results
import gfx_racers


TARGET = ('M990D.BIN', 3)
# item, sprite, u16 field index, original value, English value.
FIELDS = [
    (13, 0, 8, -104, -92),
    (13, 1, 8, -16, -4),
    (13, 2, 8, 64, 52),
    # Replace the borrowed 24x16 dash with an unused transparent texel.
    (13, 3, 1, 192, 255), (13, 3, 2, 136, 255),
    (13, 3, 3, 24, 1), (13, 3, 4, 16, 1),
    (13, 4, 8, 96, 84),
]
for level in range(1, 10):
    digit, bang = (4, 3) if level <= 2 else (3, 4)
    FIELDS.extend([
        (level, digit, 8, -48 if level == 1 else -40, -28 if level == 1 else -24),
        (level, bang, 8, 32, 12 if level == 1 else 8),
    ])


def patch(name, entry, data):
    """Return exact permitted replacement bytes, or None for an unrelated entry."""
    if (Path(name).name, entry) == ('M230D.BIN', 21):
        return gfx_racers.patch(data)
    if (Path(name).name, entry) == ('M230D.BIN', 20):
        return gfx_racers.patch_units(data)
    if (Path(name).name, entry) == ('M590D.BIN', 9):
        if hashlib.sha1(data).hexdigest() != 'dffaf96bb9ef64da697e51f35b7dbdc80c8adc34':
            raise ValueError('unexpected original M590D result ANM')
        out = bytearray(data)
        table, = struct.unpack_from('<I', data, 8)
        start, = struct.unpack_from('<I', data, table + 4)  # Lose item 1
        for sprite, geometry in enumerate(((0, 208, 56, 32, -28, -16), (255, 255, 1, 1, 0, 0))):
            for field, value in zip((1, 2, 3, 4, 8, 9), geometry):
                struct.pack_into('<H', out, start + 4 + sprite * 28 + field * 2, value & 0xFFFF)
        return bytes(out)
    if (Path(name).name, entry) != TARGET:
        return None
    if data[:4] != b'ANM\0' or struct.unpack_from('<II', data, 4) != (71, 20):
        raise ValueError('unexpected M990D announcement ANM header')
    out = bytearray(data)
    for item, sprite, field, before, after in FIELDS + gfx_results.changes(data):
        start, = struct.unpack_from('<I', data, 20 + item * 4)
        if item not in gfx_results.LAYOUTS and struct.unpack_from('<I', data, start)[0] != 5:
            raise ValueError(f'unexpected announcement {item} sprite count')
        offset = start + 4 + sprite * 28 + field * 2
        actual, = struct.unpack_from('<H', data, offset)
        if actual != before & 0xFFFF:
            raise ValueError(f'announcement {item}/{sprite}/{field}: original field differs')
        struct.pack_into('<H', out, offset, after & 0xFFFF)
    return bytes(out)
