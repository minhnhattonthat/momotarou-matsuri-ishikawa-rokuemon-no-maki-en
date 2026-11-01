"""Credit fragments must form whole lines and may change only their original source rectangles."""
import sys
from pathlib import Path

import pytest
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import anm  # noqa: E402
import arc  # noqa: E402
import engine  # noqa: E402
import gen_credits  # noqa: E402
import gfx  # noqa: E402

pytestmark = pytest.mark.skipif(not gfx.TREE.exists(), reason='needs work/disc')


def test_credits_coverage_and_scattered_pixels():
    archive = arc.entries((gfx.TREE / 'EVT600D.BIN').read_bytes())
    frames = anm.items(archive[37][1])
    assert len(frames) == 22
    words = gen_credits.translations()
    glyphs = engine.glyphs(ROOT / 'fonts' / 'credits7.txt')
    images = {p: Image.open(gfx.EN / f'EVT600D_{e}.png').convert('RGBA')
              for p, e in gen_credits.PAGES.items()}
    actual, owned = set(), set()
    for item, records in enumerate(frames):
        for fragments in gen_credits.lines(records):
            x, y = fragments[0][8:10]
            key = item, x, y
            actual.add(key)
            width = sum(r[3] for r in fragments)
            expected = gen_credits.lettering(words[key], width, glyphs)
            assembled = Image.new('RGBA', (width, 16))
            for r in fragments:
                u, v, w, h, page = r[1], r[2], r[3], r[4], r[7]
                assembled.paste(images[page].crop((u, v, u + w, v + h)), (r[8] - x, 0))
                source = {(page, sx, sy) for sy in range(v, v + h) for sx in range(u, u + w)}
                assert not owned & source, key
                owned.update(source)
            assert assembled.tobytes() == expected.tobytes(), key
    assert len(actual) == 101
    assert actual == words.keys()
    # The final fragment of T's Music comes from a third atlas row. It must be one line.
    joined = next(g for g in gen_credits.lines(frames[14]) if g[0][8:10] == (-128, 52))
    assert len(joined) == 3
    for page, entry in gen_credits.PAGES.items():
        t = gfx.unpack(archive[entry][1])[0]
        out = gfx.EN / f'EVT600D_{entry}.png'
        before, after = gfx.indices(t), gfx.indices(gfx.redraw(t, out))
        width = gfx.layout(t)[1]
        for i, (a, b) in enumerate(zip(before, after)):
            if a != b:
                assert (page, i % width, i // width) in owned


def test_credits_refuse_overflow():
    glyphs = engine.glyphs(ROOT / 'fonts' / 'credits7.txt')
    with pytest.raises(ValueError, match='sprite is'):
        gen_credits.lettering('Full name must not be clipped', 32, glyphs)


def test_credits_redraw_every_ending_reload():
    for entry in (2, 3, 4):
        expected = (gfx.EN / f'EVT600D_{entry}.png').read_bytes()
        for scene in range(60, 66):
            assert (gfx.EN / f'EVT{scene}0D_{entry}.png').read_bytes() == expected
