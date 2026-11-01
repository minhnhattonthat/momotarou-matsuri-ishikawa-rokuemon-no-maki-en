"""Widen selected field plaques with isolated, non-contiguous 16px tiles.

Copy the original three front-layer tiles into unused atlas cells, preserving
their surroundings, then extend the wooden lettering panel. Only the selected
grid cells use the new records. Record count, palette, page, rear layer and all
per-record attribute bytes are preserved. Cold captures are the runtime proof.
"""
import hashlib
import struct
from pathlib import Path


SLOTS = ((128, 64), (144, 208), (144, 240))
RECORDS = (1021, 1022, 1023)
PLANS = {
    'GV06000D.BIN:0': dict(
        label='flowers', word='Flowers', companion='GV06001D.BIN',
        tables=(2, 3), grids=(0,), cell=(20, 39), ids=(197, 200, 199),
        sources=((208, 48), (200, 80), (240, 48)), clut=30784,
        hashes={0: 'a1a87d2b01c680f9828a6f8cc1729f0b379e2abd',
                2: 'feabb8f2692598c99806dd889c349de0c3010606',
                3: 'f91b5eccc3b2063e22ea258cc6a8fd08eab0a61d'}),
    'GV12000D.BIN:0': dict(
        label='items', word='Items', companion='GV12001D.BIN',
        tables=(2,), grids=(0,), cell=(24, 20), ids=(99, 71, 101),
        sources=((208, 48), (16, 80), (144, 48)), clut=31488,
        hashes={0: '670d73b007a51eb338e0dc32c1aae2fe6dc4b0e0',
                2: '0a5c8b92e95390556bec58d8912ce59c94ac25a0'}),
    'GV12002D.BIN:0': dict(
        label='items', word='Items', companion='GV12003D.BIN',
        tables=(2,), grids=(0,), cell=(24, 20), ids=(99, 71, 101),
        sources=((208, 48), (16, 80), (144, 48)), clut=31488,
        hashes={0: 'bb0a4b158e6069cdf06d7b028258d337abd24578',
                2: '80607eacc463f4de186d070b69db6c714962ee68'}),
    'GV22000D.BIN:0': dict(
        label='flowers', word='Flowers', companion='GV22001D.BIN',
        tables=(4,), grids=(0, 2), cell=(70, 26), ids=(742, 75, 744),
        sources=((144, 176), (80, 80), (176, 144)), cluts=(31616, 30784, 31616),
        slots=((176, 240), (192, 240), (208, 240)),
        hashes={0: '9869ce394bf036e51f0581174d2a86bd4a58db0e',
                2: '78a02576562ca3841a76e48ec725b87f4b692cfa',
                4: 'd3d08bec3ed73c61ecf0c94f35f203a75c4dd023'}),
}


def slots(key):
    return PLANS[key].get('slots', SLOTS)


def cluts(plan):
    return plan.get('cluts') or (plan['clut'],) * 3


def pieces(key, original=False):
    return [(u, v, 16, 16, i * 16, 0)
            for i, (u, v) in enumerate(PLANS[key]['sources'] if original else slots(key))]


def template(texture, key, original=False, vram=None):
    """Assemble each tile under its own native CLUT, including mixed roofs."""
    from PIL import Image
    import tim

    _, _, palette, _ = tim.parse(texture)
    assert palette[2] == 16
    if vram is not None:
        # This Redux build exports a 1024-row GPU backing store; hardware uses
        # the first 512 rows. Also accept hardware-sized dumps.
        if len(vram) not in (1024 * 512 * 2, 1024 * 1024 * 2):
            raise ValueError('expected a complete PS1 VRAM dump')
        # Take only palette rows from the capture. Pixel indices always come
        # from the disc being tested; runtime pixels cannot validate themselves.
        texture = bytearray(texture)
        for row in range(palette[3]):
            at = ((palette[1] + row) * 1024 + palette[0]) * 2
            texture[20 + row * 32:20 + (row + 1) * 32] = vram[at:at + 32]
    base = (palette[1] << 6) | (palette[0] // 16)
    out = Image.new('RGBA', (48, 16))
    for (u, v, w, h, x, y), clut in zip(pieces(key, original), cluts(PLANS[key])):
        assert (clut - base) % 64 == 0
        row = (clut - base) // 64
        if vram is not None:
            import gfx
            colours = gfx.palette(texture, row)
            if not colours[12][3] or any(
                    max(abs(a - b) for a, b in zip(colours[12][:3], colour[:3])) <= 8
                    for colour in colours[7:11]):
                raise ValueError('captured palette cannot distinguish lettering from wood')
        image = tim.image(texture, row)
        out.paste(image.crop((u, v, u + w, v + h)), (x, y))
    return out


def files():
    return {plan['companion'] for plan in PLANS.values()}


def patch(name, entry, data):
    plan = next((p for p in PLANS.values() if p['companion'] == Path(name).name), None)
    if plan is None or entry not in plan['hashes']:
        return None
    if hashlib.sha1(data).hexdigest() != plan['hashes'][entry]:
        raise ValueError(f'{name}/{entry}: unexpected original field layout')
    out = bytearray(data)
    if entry in plan['tables']:
        assert data[:8] == bytes.fromhex('2203008000042020')
        destinations = plan.get('slots', SLOTS)
        for source, target, (u, v), (su, sv), clut in zip(
                plan['ids'], RECORDS, destinations, plan['sources'], cluts(plan)):
            native = struct.unpack_from('<BB3H', data, 8 + source * 8)
            assert native == (su, sv, clut, 0, 5)
            assert struct.unpack_from('<BB3H', data, 8 + target * 8) == (0, 0, 30720, 0, 5)
            struct.pack_into('<BB3H', out, 8 + target * 8, u, v, *native[2:])
            # Preserve the source's trailing attribute (semantics not assumed).
            out[8200 + target] = data[8200 + source]
    else:
        assert data[:4] == b'\x23\0\0\0'
        width, height = data[4:6]
        cells = struct.unpack_from(f'<{width * height}H', data, 8)
        assert not set(RECORDS) & set(cells), 'reserved records already used'
        x, y = plan['cell']
        at = y * width + x - 1
        assert cells[at:at + 3] == plan['ids']
        struct.pack_into('<3H', out, 8 + at * 2, *RECORDS)
    return bytes(out)


def draw(im, key, pal):
    """Generate the three relocated tiles; never alter the native source tiles."""
    import gen_gfx
    import gfx
    import gfx_signs

    plan = PLANS[key]
    texture, original = gen_gfx.original(key)
    colours = gfx.palette(texture, gen_gfx.EDIT_PALETTES.get(key, 0))
    board = gfx_signs.assemble(original, pieces(key, original=True))
    px = board.load()
    # Erase the complete old central glyph, including highlights, first.
    for y in range(1, 15):
        wood = {x: px[x, y] for x in range(16, 32) if px[x, y] in colours[7:11]}
        assert wood, (key, y)
        for x in range(16, 32):
            if px[x, y] in colours[12:14]:
                px[x, y] = wood[min(wood, key=lambda sx: abs(sx - x))]
        # Widen only the panel's middle, preserving roof/edge pixels elsewhere.
        if 3 <= y <= 11:
            for x in range(8, 40):
                px[x, y] = wood[min(wood, key=lambda sx: abs(sx - x))]
    mask = gen_gfx.mask(plan['word'], 7, {'pixel': 'credits7.txt', 'tight': True})
    assert mask.width <= 30
    left = (48 - mask.width) // 2
    board.paste(colours[12], (left, 4, left + mask.width, 11), mask)
    assert set(board.getdata()) <= pal
    for u, v, w, h, x, y in pieces(key):
        assert not im.crop((u, v, u + w, v + h)).getchannel('A').getbbox(), (key, u, v)
        im.paste(board.crop((x, y, x + w, y + h)), (u, v))
