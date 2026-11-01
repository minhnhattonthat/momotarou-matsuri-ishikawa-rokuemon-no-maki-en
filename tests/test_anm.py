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
import gfx_racers  # noqa: E402
import gfx_hud  # noqa: E402
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
def test_reused_vram_pages_require_explicit_loaded_textures(tmp_path):
    archive = arc.entries((gfx.TREE / 'M590D.BIN').read_bytes())
    records = [[(r[0] & ~0x7000, *r[1:]) for r in item] for item in anm.items(archive[9][1])]
    with pytest.raises(ValueError, match='ambiguous texture/palette'):
        anm.render(archive, records, tmp_path, strict=True)
    # Story's 8bpp result sprites use entry 0; later modes reuse its page.
    anm.render([archive[0]], records, tmp_path, strict=True)
    assert len(list(tmp_path.glob('*.png'))) == 3


@pytest.mark.skipif(not gfx.TREE.exists(), reason='needs work/disc')
def test_m59_lose_does_not_reuse_actor_pixels():
    from PIL import Image
    archive = arc.entries((gfx.TREE / 'M590D.BIN').read_bytes())
    assert not list(anm.references(archive, 7, (0, 208, 56, 240)))
    before = anm.items(archive[9][1])
    after = anm.items(gfx_layout.patch('M590D.BIN', 9, archive[9][1]))
    assert before[0] == after[0] and before[2] == after[2]
    assert after[1][0][1:5] == (0, 208, 56, 32)
    assert after[1][1][1:5] == (255, 255, 1, 1)
    for old, new in zip(before[1], after[1]):
        assert all(old[i] == new[i] for i in (0, 5, 6, 7, 10, 11, 12, 13))
    original = gen_gfx.original('M590D.BIN:0')[1]
    translated = Image.open(gfx.EN / 'M590D_0.png').convert('RGBA')
    # The old trailing fragment overlaps actor sprites, which must stay intact.
    assert original.crop((64, 120, 80, 152)).tobytes() == translated.crop((64, 120, 80, 152)).tobytes()
    assert translated.getpixel((255, 255))[3] == 0
    corrupt = bytearray(archive[9][1])
    corrupt[-1] ^= 1
    with pytest.raises(ValueError, match='unexpected original'):
        gfx_layout.patch('M590D.BIN', 9, corrupt)


@pytest.mark.skipif(not gfx.TREE.exists(), reason='needs work/disc')
def test_shared_hud_words_have_no_partial_sprite_users():
    archive = arc.entries((gfx.TREE / 'M990D.BIN').read_bytes())
    for x0, y0, x1, y1, label, _ in gen_gfx.LABELS['M990D.BIN:0']:
        refs = list(anm.references(archive, 0x1B, (x0, y0, x1, y1)))
        assert refs, label
        # A fragment user would show half an English word after a whole-word redraw.
        assert all(r[1:5] == (x0, y0, x1 - x0, y1 - y0) for _, _, r in refs), label
    # Shared texture pages can be referenced by ANMs in another archive too.
    for path in gfx.TREE.glob('*.BIN'):
        if path.name == 'M990D.BIN':
            continue
        other = arc.entries(path.read_bytes()) or []
        for x0, y0, x1, y1, label, _ in gen_gfx.LABELS['M990D.BIN:0']:
            assert all(r[1:5] == (x0, y0, x1 - x0, y1 - y0)
                       for _, _, r in anm.references(other, 0x1B, (x0, y0, x1, y1))), (path.name, label)


@pytest.mark.skipif(not gfx.TREE.exists(), reason='needs work/disc')
def test_relocated_hud_preserves_shared_fragments_and_unrelated_fields():
    from PIL import Image
    original = (gfx.TREE / 'M990D.BIN').read_bytes()
    archive = arc.entries(original)
    for path in gfx.TREE.glob('*.BIN'):
        assert not list(anm.references(arc.entries(path.read_bytes()) or [], 27, gfx_hud.RECT)), path.name
    before = anm.items(archive[2][1])
    after = anm.items(gfx_hud.patch(archive[2][1]))
    for item, (old, new) in enumerate(zip(before, after)):
        if item not in gfx_hud.WORDS:
            assert old == new, item
        else:
            assert len(old) == len(new) == 1
            assert new[0][1:5] == gfx_hud.rect(item)
            assert new[0][9] == old[0][9] + 4
            assert all(old[0][i] == new[0][i] for i in (0, 5, 6, 7, 8, 10, 11, 12, 13))
    source = gen_gfx.original('M990D.BIN:0')[1]
    target = Image.open(gfx.EN / 'M990D_0.png').convert('RGBA')
    # Preserve the partial 8x8 user and the announcement tail's 8x24 strip.
    for rect in ((128, 0, 136, 8), (144, 0, 152, 24), (136, 16, 176, 32)):
        assert source.crop(rect).tobytes() == target.crop(rect).tobytes()
    assert verify_build.check_archive('OUTBIN/M990D.BIN', original, gfx.apply('M990D.BIN', original)) == []
    corrupt = bytearray(archive[2][1])
    corrupt[-1] ^= 1
    with pytest.raises(ValueError, match='unexpected original'):
        gfx_hud.patch(corrupt)


@pytest.mark.skipif(not gfx.TREE.exists(), reason='needs work/disc')
def test_counter_panel_growth_preserves_art_and_only_changes_width():
    from PIL import Image
    original = (gfx.TREE / 'M340D.BIN').read_bytes()
    archive = arc.entries(original)
    assert not list(anm.references(archive, 7, (240, 152, 248, 184)))
    before = anm.items(archive[7][1])
    after = anm.items(gfx_hud.patch_panel(archive[7][1]))
    assert before[:9] == after[:9] and before[10:] == after[10:]
    assert all(a == b for i, (a, b) in enumerate(zip(before[9][0], after[9][0])) if i != 3)
    assert after[9][0][3] == 56
    source = gen_gfx.original('M340D.BIN:1')[1]
    target = Image.open(gfx.EN / 'M340D_1.png').convert('RGBA')
    assert source.crop((192, 152, 224, 184)).tobytes() == target.crop((192, 152, 224, 184)).tobytes()
    assert source.crop((224, 152, 240, 184)).tobytes() == target.crop((232, 152, 248, 184)).tobytes()
    assert verify_build.check_archive('OUTBIN/M340D.BIN', original, gfx.apply('M340D.BIN', original)) == []


@pytest.mark.skipif(not gfx.TREE.exists(), reason='needs work/disc')
def test_minigame_labels_preserve_fragment_users_and_level_numbers():
    from PIL import Image
    import tim
    for key in ('M050D.BIN:2', 'M060D.BIN:2', 'M080D.BIN:6',
                'M180D.BIN:3', 'M230D.BIN:0', 'M500D.BIN:0'):
        texture, _ = gen_gfx.original(key)
        tx, ty, _, _, _ = tim.parse(texture)[3]
        page = tx // 64 + ty // 256 * 16
        archive = arc.entries((gfx.TREE / key.split(':')[0]).read_bytes())
        for x0, y0, x1, y1, label, _ in gen_gfx.LABELS[key]:
            refs = list(anm.references(archive, page, (x0, y0, x1, y1)))
            assert refs, (key, label)
            assert all(r[1] <= x0 and r[2] <= y0 and r[1] + r[3] >= x1 and r[2] + r[4] >= y1
                       for _, _, r in refs), (key, label, refs)
    # Level 1 uses a complete strip, but levels 2/3 append separate number
    # sprites to the shared 40px word. Relettering all 56px corrupts both forms.
    original = gen_gfx.original('M060D.BIN:2')[1]
    translated = Image.open(gfx.EN / 'M060D_2.png').convert('RGBA')
    assert original.crop((208, 0, 256, 24)).tobytes() == translated.crop((208, 0, 256, 24)).tobytes()
    # A speech bubble's rounded tail is artwork, not part of the lettering.
    assert original.crop((220, 24, 224, 120)).tobytes() == translated.crop((220, 24, 224, 120)).tobytes()


@pytest.mark.skipif(not gfx.TREE.exists(), reason='needs work/disc')
def test_race_names_use_free_pixels_and_keep_all_thirty_identities():
    from PIL import Image
    original = (gfx.TREE / 'M230D.BIN').read_bytes()
    archive = arc.entries(original)
    assert not list(anm.references(archive, 11, gfx_racers.RECT))
    assert len(set(row['en'] for row in gfx_racers.rows())) == 30
    before = anm.items(archive[21][1])
    patched = gfx_racers.patch(archive[21][1])
    after = anm.items(patched)
    image = Image.open(gfx.EN / 'M230D_3.png').convert('RGBA')
    assert image.getpixel((255, 255))[3] == 0
    for index, (old, new) in enumerate(zip(before, after)):
        assert len(old) == len(new)
        u, v, w, h = new[0][1:5]
        assert (u, v, w, h) == gfx_racers.rect(index, gfx_racers.rows()[index]['en'])
        assert image.crop((u, v, u + w, v + h)).getchannel('A').getbbox()
        assert new[0][8:10] == (min(r[8] for r in old), min(r[9] for r in old))
        # In the tighter natural standings, names start at x55 and a separator
        # precedes the Lane column at x112. Leave room for that separator too.
        # Seven JP items store a non-leftmost glyph first.
        assert new[0][8] == -24
        assert w <= 50
        for a, b in zip(old, new):
            assert all(a[i] == b[i] for i in (0, 5, 6, 7, 10, 11, 12, 13))
    assert verify_build.check_archive('OUTBIN/M230D.BIN', original, gfx.apply('M230D.BIN', original)) == []
    corrupt = bytearray(archive[21][1])
    corrupt[-1] ^= 1
    with pytest.raises(ValueError, match='unexpected original'):
        gfx_racers.patch(corrupt)


@pytest.mark.skipif(not gfx.TREE.exists(), reason='needs work/disc')
def test_race_units_keep_symbols_palettes_and_rank_punctuation_baseline():
    from PIL import Image
    archive = arc.entries((gfx.TREE / 'M230D.BIN').read_bytes())
    before = anm.items(archive[20][1])
    after = anm.items(gfx_racers.patch_units(archive[20][1]))
    assert before[5:] == after[5:]  # multiplication, equality, dash and colon
    for old, new in zip(before[:5], after[:5]):
        assert len(old) == len(new)
        assert old[0][8:10] == new[0][8:10]
        for a, b in zip(old, new):
            assert all(a[i] == b[i] for i in (0, 5, 6, 7, 10, 11, 12, 13))
    image = Image.open(gfx.EN / 'M230D_3.png').convert('RGBA')
    u, v, w, h = gfx_racers.unit_rect(0)
    assert image.crop((u, v, u + w, v + h)).getchannel('A').getbbox()[1] >= 5
    corrupt = bytearray(archive[20][1])
    corrupt[-1] ^= 1
    with pytest.raises(ValueError, match='unexpected original'):
        gfx_racers.patch_units(corrupt)


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
