"""Latin player-name sprites and the native D-pad selection table.

Names remain four 8-bit sprite IDs, padded to eight bytes with FF in records.
NAME0D:1 and PREM0D:1 share this font. No save-format or executable changes.
The 80 IDs are deliberately stable; changing ALPHABET reinterprets saved names.
"""
import string
import struct

import anm
import arc
import engine
import gfx

ALPHABET = string.ascii_uppercase + string.ascii_lowercase + string.digits + " -.'!?+/():&%=,*#$"
TABLE = 0x800E0D6C
BASE = 0x800CB338
COLS, ROWS = 10, 19
# Original kana columns, terminated by -1; unused rows remain sentinels.
JP_COLUMNS = [list(range(0, 10)), list(range(10, 20)), list(range(20, 30)),
              list(range(30, 40)) + [79], list(range(40, 45)), list(range(45, 60)),
              list(range(60, 65)), list(range(65, 71)), list(range(71, 76)), list(range(76, 79))]


def table_words(english):
    if english:
        return [r * COLS + c if r < 8 else -1 for r in range(ROWS) for c in range(COLS)]
    return [column[r] if r < len(column) else -1 for r in range(ROWS) for column in JP_COLUMNS]


def patch(data):
    """Replace only the checked selection table; the input logic stays native."""
    offset = TABLE - BASE
    original = struct.pack('<190i', *table_words(False))
    if data[offset:offset + len(original)] != original:
        raise ValueError('Name Entry selection table differs from the original revision')
    out = bytearray(data)
    out[offset:offset + len(original)] = struct.pack('<190i', *table_words(True))
    return bytes(out)


def cells():
    archive = arc.entries((gfx.TREE / 'NAME0D.BIN').read_bytes())
    entries = anm.items(archive[6][1])
    assert len(entries) == len(ALPHABET) == 80
    result = []
    for records in entries:
        assert len(records) == 1
        r = records[0]
        assert r[3:5] == (16, 16) and r[7] == 9
        result.append(r[1:3])
    assert len(set(result)) == 80
    return result


def draw(image):
    """Redraw the 80 complete glyph cells, preserving arrows and panel art."""
    glyphs = engine.glyphs()
    for char, (x, y) in zip(ALPHABET, cells()):
        image.paste((0, 0, 0, 0), (x, y, x + 16, y + 16))
        if char == ' ':
            continue
        rows = glyphs[char]
        width = max(len(row.rstrip('.')) for row in rows)
        for dy, row in enumerate(rows):
            for dx, value in enumerate(row):
                if value == '#':
                    image.putpixel((x + (16 - width) // 2 + dx, y + 3 + dy), (248, 208, 0, 255))
