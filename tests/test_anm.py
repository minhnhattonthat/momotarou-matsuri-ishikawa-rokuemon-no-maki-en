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
import gfx_layout  # noqa: E402
import gfx_results  # noqa: E402
import verify_build  # noqa: E402


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


@pytest.mark.skipif(not gfx.TREE.exists(), reason='needs work/disc')
def test_english_start_joins_fragments_and_preserves_other_animation_fields():
    from PIL import Image
    original = (gfx.TREE / 'M990D.BIN').read_bytes()
    before = arc.entries(original)[3][1]
    after = gfx_layout.patch('M990D.BIN', 3, before)
    old, new = anm.items(before), anm.items(after)
    assert len(new) == len(old) == 71
    for item in range(71):
        for sprite, (a, b) in enumerate(zip(old[item], new[item])):
            allowed = {f for it, sp, f, _, _ in gfx_layout.FIELDS + gfx_results.changes(before)
                       if (it, sp) == (item, sprite)}
            assert all(x == y for f, (x, y) in enumerate(zip(a, b)) if f not in allowed)
    start = new[13]
    assert start[1][8] + start[1][3] == start[2][8]  # two pieces of START touch
    assert start[2][8] + start[2][3] == start[4][8]  # ! follows START
    assert start[0][8] == -(start[4][8] + start[4][3])  # whole phrase centred
    assert Image.open(gfx.EN / 'M990D_1.png').convert('RGBA').getpixel((255, 255))[3] == 0


@pytest.mark.skipif(not gfx.TREE.exists(), reason='needs work/disc')
def test_verifier_rejects_unapproved_announcement_layout_changes():
    original = (gfx.TREE / 'M990D.BIN').read_bytes()
    built = gfx.apply('M990D.BIN', original)
    assert verify_build.check_archive('OUTBIN/M990D.BIN', original, built) == []
    entry_offset, data = arc.entries(built)[3]
    first, = struct.unpack_from('<I', data, 20)
    start, = struct.unpack_from('<I', data, 20 + 13 * 4)
    # Both an unrelated item and the approved item's CLUT remain protected.
    for position in (first + 4 + 2, start + 4 + 10):
        corrupt = bytearray(built)
        corrupt[entry_offset + position] ^= 1
        assert verify_build.check_archive('OUTBIN/M990D.BIN', original, bytes(corrupt))


@pytest.mark.skipif(not gfx.TREE.exists(), reason='needs work/disc')
def test_results_atlas_does_not_overwrite_other_sprite_users():
    from PIL import Image
    archive = arc.entries((gfx.TREE / 'M990D.BIN').read_bytes())
    # Every original user of reclaimed pixels must be one of the rewritten
    # result items. This protects small HUDs and face icons sharing this page.
    for rect in gfx_results.CLEAR_RECTS:
        for entry, item, _ in anm.references(archive, 0x1B, rect):
            assert entry == 3 and item in gfx_results.LAYOUTS, (entry, item, rect)
    # Page 27 is shared across minigames: a sprite in a different archive must
    # not silently retain an old UV after this atlas is repacked.
    for path in gfx.TREE.glob('*.BIN'):
        if path.name == 'M990D.BIN':
            continue
        other = arc.entries(path.read_bytes()) or []
        for rect in gfx_results.CLEAR_RECTS:
            assert not list(anm.references(other, 0x1B, rect)), (path.name, rect)
    occupied = set()
    for name, (x, y, w, h) in gfx_results.WORDS.items():
        pixels = {(u, v) for v in range(y, y + h) for u in range(x, x + w)}
        assert not pixels & occupied, name
        assert all(any(a <= u < c and b <= v < d for a, b, c, d in gfx_results.CLEAR_RECTS)
                   for u, v in pixels), name
        occupied |= pixels
    assert Image.open(gfx.EN / 'M990D_0.png').convert('RGBA').getpixel((255, 255))[3] == 0


@pytest.mark.skipif(not gfx.TREE.exists(), reason='needs work/disc')
def test_results_layout_keeps_names_whole_and_counters_in_english_order():
    archive = arc.entries((gfx.TREE / 'M990D.BIN').read_bytes())
    records = anm.items(gfx_layout.patch('M990D.BIN', 3, archive[3][1]))
    assert set(gfx_results.LAYOUTS) == set(range(21, 40)) | set(range(41, 52)) | set(range(61, 71))
    for base, word in ((21, 'Round'), (41, 'Try'), (61, 'Question')):
        for n in range(1, 11):
            layout = gfx_results.LAYOUTS[base + n - 1]
            assert [p[0] for p in layout] == [word, str(n), '!']
            assert records[base + n - 1][0][8] < records[base + n - 1][1][8]
    for item, layout in gfx_results.LAYOUTS.items():
        for sprite, (word, x, y) in enumerate(layout):
            r = records[item][sprite]
            assert r[1:5] == gfx_results.WORDS[word]
            assert -160 <= x and x + r[3] <= 160
            assert -104 <= y and y + r[4] <= 104
    corrupt = bytearray(archive[3][1])
    corrupt[-1] ^= 1
    with pytest.raises(ValueError, match='unexpected original'):
        gfx_results.changes(corrupt)
