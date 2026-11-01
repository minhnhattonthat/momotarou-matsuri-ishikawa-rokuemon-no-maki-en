"""Field-sign regression guards: complete assemblies and unchanged surroundings."""
import sys
from pathlib import Path

import pytest
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import gfx  # noqa: E402
import gen_gfx  # noqa: E402
import gfx_signs  # noqa: E402

pytestmark = pytest.mark.skipif(not gfx.TREE.exists(), reason='needs work/disc')


def test_sign_frames_cloth_silhouettes_and_other_tiles_preserved():
    for key, signs in gfx_signs.SIGNS.items():
        _, original = gen_gfx.original(key)
        name, entry = key.split(':')
        revised = Image.open(gfx.EN / f'{Path(name).stem}_{entry}.png').convert('RGBA')
        allowed = set()
        for _, pieces, (x0, y0, x1, y1), _, _, kind in signs:
            for u, v, w, h, x, y in pieces:
                allowed.update((u + dx, v + dy) for dy in range(h) for dx in range(w)
                               if x0 <= x + dx < x1 and y0 <= y + dy < y1)
            if kind == 'curtain':
                assert gfx_signs.assemble(original, pieces).getchannel('A').tobytes() == \
                    gfx_signs.assemble(revised, pieces).getchannel('A').tobytes()
        for y in range(original.height):
            for x in range(original.width):
                if (x, y) not in allowed:
                    assert original.getpixel((x, y)) == revised.getpixel((x, y)), (key, x, y)


def test_curtains_in_every_duplicate_archive():
    original, _ = gen_gfx.original('GV16090D.BIN:1')
    copies = gen_gfx.copies()[original]
    assert set(copies) == {'GV16090D.BIN:1', 'GV36110D.BIN:1', 'GV36120D.BIN:1'}
    expected = (gfx.EN / 'GV16090D_1.png').read_bytes()
    for copy in copies:
        name, entry = copy.split(':')
        assert (gfx.EN / f'{Path(name).stem}_{entry}.png').read_bytes() == expected


def test_full_contest_title_survives_split_atlas_boundary():
    title = "World's Greatest Pun Contest"
    expected = gen_gfx.mask(title, 7, {'pixel': 'credits7.txt', 'tight': True})
    for key in ['GV02000D.BIN:2', 'GV13000D.BIN:2']:
        name, entry = key.split(':')
        im = Image.open(gfx.EN / f'{Path(name).stem}_{entry}.png').convert('RGBA')
        _, pieces, (x0, y0, x1, y1), lines, colour, _ = gfx_signs.SIGNS[key][0]
        assert lines == [title]
        assembled = gfx_signs.assemble(im, pieces)
        left, top = x0 + (x1 - x0 - expected.width) // 2, y0 + (y1 - y0 - 7) // 2
        for y in range(7):
            for x in range(expected.width):
                assert (assembled.getpixel((left + x, top + y)) == colour) == bool(expected.getpixel((x, y)))
