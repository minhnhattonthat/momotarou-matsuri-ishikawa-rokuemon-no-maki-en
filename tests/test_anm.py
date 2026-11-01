"""ANM table location and shared HUD sprite rectangles are graphics-editing constraints."""
import struct
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import anm  # noqa: E402
import arc  # noqa: E402
import gen_gfx  # noqa: E402
import gfx  # noqa: E402


def test_table_location_and_signed_offsets():
    # Animated files place their frame table after the sequence section, not always at +20.
    data = bytearray(80)
    data[:4] = b'ANM\0'
    struct.pack_into('<II', data, 4, 1, 40)
    struct.pack_into('<I', data, 40, 48)
    struct.pack_into('<I', data, 48, 1)
    record = (0, 80, 0, 32, 16, 272, 496, 27, -16, -8, 4096, 4096, 0, 0)
    struct.pack_into('<8H2h4H', data, 52, *record)
    assert anm.items(data) == [[record]]
    with pytest.raises(ValueError, match='truncated'):
        anm.items(data[:-1])


@pytest.mark.skipif(not gfx.TREE.exists(), reason='needs work/disc')
def test_shared_hud_words_have_no_partial_sprite_users():
    archive = arc.entries((gfx.TREE / 'M990D.BIN').read_bytes())
    for x0, y0, x1, y1, label, _ in gen_gfx.LABELS['M990D.BIN:0']:
        refs = list(anm.references(archive, 0x1B, (x0, y0, x1, y1)))
        assert refs, label
        # A fragment user would show half an English word after a whole-word redraw.
        assert all(r[1:5] == (x0, y0, x1 - x0, y1 - y0) for _, _, r in refs), label
