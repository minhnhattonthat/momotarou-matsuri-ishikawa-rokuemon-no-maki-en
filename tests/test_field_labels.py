"""Isolated wider field plaques: allocation, native context and verifier gates."""
from pathlib import Path
import struct
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'tools'), str(ROOT / 'tools/debug')]
import arc  # noqa: E402
import field_consumers  # noqa: E402
import gen_gfx  # noqa: E402
import gfx  # noqa: E402
import gfx_field  # noqa: E402
import tim  # noqa: E402
import verify_build  # noqa: E402

pytestmark = pytest.mark.skipif(not gfx.TREE.exists(), reason='needs work/disc')


@pytest.mark.parametrize('key', gfx_field.PLANS)
def test_new_tiles_have_no_original_consumers_and_old_records_stay_intact(key):
    plan = gfx_field.PLANS[key]
    plans = gfx_field.plans(key)
    destinations = [slot for p in plans for slot in gfx_field.slots(key, p['label'])]
    assert len(destinations) == len(set(destinations)), 'English allocations overlap'
    for u, v in destinations:
        owners, uses = field_consumers.inspect(key, (u, v, u + 16, v + 16))
        assert owners and not uses, (key, u, v, uses)
    records = [record for p in plans for record in gfx_field.records(p)]
    assert len(records) == len(set(records))
    raw = (gfx.TREE / plan['companion']).read_bytes()
    entries = [entry for _, entry in arc.entries(raw)]
    new = gfx.apply(plan['companion'], raw)
    assert not verify_build.check_archive(plan['companion'], raw, new)
    for i, ((_, old), (_, changed)) in enumerate(zip(arc.entries(raw), arc.entries(new))):
        if i in plan['tables']:
            allowed = {at for record in records for at in range(8 + record * 8, 16 + record * 8)}
            allowed.update(8200 + record for record in records)
            assert all(a == b or at in allowed for at, (a, b) in enumerate(zip(old, changed)))
            for p in plans:
                for source, target in zip(p['ids'], gfx_field.records(p)):
                    assert changed[8200 + target] == old[8200 + source]
        elif i in plan['grids']:
            w, h = old[4:6]
            before = struct.unpack_from(f'<{w * h}H', old, 8)
            after = struct.unpack_from(f'<{w * h}H', changed, 8)
            expected = {y * w + x + dx for p in plans for x, y in [p['cell']] for dx in (-1, 0, 1)}
            assert {n for n, pair in enumerate(zip(before, after)) if pair[0] != pair[1]} == expected
        else:
            assert old == changed
        if old[:4] == b'\x23\0\0\0':
            assert not set(records) & set(struct.unpack_from(f'<{old[4] * old[5]}H', old, 8))
    bad = bytearray(entries[plan['tables'][0]])
    bad[9] ^= 1
    with pytest.raises(ValueError, match='unexpected original field layout'):
        gfx_field.patch(plan['companion'], plan['tables'][0], bad)
    # A valid new grid with an unrelated cell modified must fail the verifier.
    damaged = [entry for _, entry in arc.entries(new)]
    grid = bytearray(damaged[plan['grids'][0]])
    grid[8] ^= 1
    damaged[plan['grids'][0]] = bytes(grid)
    assert verify_build.check_archive(plan['companion'], raw, arc.pack(damaged, struct.unpack_from('<I', raw)[0]))


@pytest.mark.parametrize('key,label', [(key, p['label']) for key in gfx_field.PLANS
                                     for p in gfx_field.plans(key)])
def test_widened_label_has_full_word_and_no_old_highlight(key, label):
    plan = gfx_field.plan_for(key, label)
    original = gfx.indices(gen_gfx.original(key)[0])
    revised = gfx.indices(gen_gfx.redrawn(key))
    mask = gen_gfx.mask(plan['word'], 7, {'pixel': 'credits7.txt', 'tight': True})
    left = (48 - mask.width) // 2
    for x in range(48):
        u, v = gfx_field.slots(key, label)[x // 16]
        sx, sy = plan['sources'][x // 16]
        for y in range(16):
            value = revised[(v + y) * 256 + u + x % 16]
            if 8 <= x < 40 and 3 <= y <= 11:
                ink = left <= x < left + mask.width and 4 <= y < 11 and mask.getpixel((x - left, y - 4))
                assert (value == 12) == bool(ink), (key, x, y)
                assert value != 13
            elif not (16 <= x < 32 and 1 <= y < 15):
                assert value == original[(sy + y) * 256 + sx + x % 16], (key, x, y)


def test_capture_supplies_only_palettes_and_rejects_invisible_letters():
    key = 'GV22000D.BIN:0'
    texture = gen_gfx.redrawn(key)
    palette = tim.parse(texture)[2]
    vram = bytearray(1024 * 1024 * 2)
    for row in range(palette[3]):
        at = ((palette[1] + row) * 1024 + palette[0]) * 2
        vram[at:at + 32] = palette[4][row * 32:(row + 1) * 32]
    expected = gfx_field.template(texture, key).tobytes()
    assert gfx_field.template(texture, key, vram=vram).tobytes() == expected
    # Arbitrary captured texture/framebuffer data cannot supply the expected word.
    vram[:10000] = b'\xff' * 10000
    assert gfx_field.template(texture, key, vram=vram).tobytes() == expected
    assert gfx_field.template(texture, key, vram=vram[:1024 * 512 * 2]).tobytes() == expected
    with pytest.raises(ValueError, match='complete PS1 VRAM'):
        gfx_field.template(texture, key, vram=b'bad')
    with pytest.raises(ValueError, match='cannot distinguish'):
        gfx_field.template(texture, key, vram=bytes(len(vram)))
