"""The saved-name ID mapping, complete glyphs and exact mutation boundaries."""
import struct
import sys
from pathlib import Path

from PIL import Image
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import anm
import arc
import engine
import gfx
import name_entry

pytestmark = pytest.mark.skipif(not gfx.TREE.exists(), reason='needs work/disc (dumpsxiso)')


def test_selection_table_and_guard():
    original = (gfx.TREE / 'OVLXTTL.BIN').read_bytes()
    changed = name_entry.patch(original)
    lo = name_entry.TABLE - name_entry.BASE
    hi = lo + 190 * 4
    assert changed[:lo] == original[:lo] and changed[hi:] == original[hi:]
    words = struct.unpack_from('<190i', changed, lo)
    assert words[:80] == tuple(range(80))
    assert words[80:] == (-1,) * 110
    # All D-pad columns have eight usable entries and a terminating sentinel.
    assert len(set(name_entry.ALPHABET)) == 80
    assert name_entry.ALPHABET[:26] == 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    assert name_entry.ALPHABET[26:52] == 'abcdefghijklmnopqrstuvwxyz'
    assert name_entry.ALPHABET[52:62] == '0123456789'
    assert '@' not in name_entry.ALPHABET  # en12's @ is a dialogue heart icon.
    with pytest.raises(ValueError, match='selection table'):
        name_entry.patch(changed)


def test_font_copies_cells_and_unchanged_art():
    originals = [arc.entries((gfx.TREE / f'{stem}.BIN').read_bytes()) for stem in ('NAME0D', 'PREM0D')]
    assert originals[0][1][1] == originals[1][1][1]
    assert anm.items(originals[0][6][1]) == anm.items(originals[1][12][1])
    paths = [gfx.EN / f'{stem}_1.png' for stem in ('NAME0D', 'PREM0D')]
    assert paths[0].read_bytes() == paths[1].read_bytes()
    original = gfx.unpack(originals[0][1][1])[0]
    changed = gfx.redraw(original, paths[0])
    image = Image.open(paths[0]).convert('RGBA')
    before, after = gfx.indices(original), gfx.indices(changed)
    allowed = set()
    glyphs = engine.glyphs()
    for char, (x, y) in zip(name_entry.ALPHABET, name_entry.cells()):
        allowed.update((y + dy) * image.width + x + dx for dy in range(16) for dx in range(16))
        got = image.crop((x, y, x + 16, y + 16))
        pixels = {(px, py) for py in range(16) for px in range(16) if got.getpixel((px, py))[3]}
        if char == ' ':
            assert not pixels
        else:
            rows = glyphs[char]
            width = max(len(row.rstrip('.')) for row in rows)
            assert pixels == {(dx + (16 - width) // 2, dy + 3) for dy, row in enumerate(rows)
                              for dx, value in enumerate(row) if value == '#'}
    assert all(a == b or i in allowed for i, (a, b) in enumerate(zip(before, after)))
    assert gfx.same_but_pixels(original, changed)
