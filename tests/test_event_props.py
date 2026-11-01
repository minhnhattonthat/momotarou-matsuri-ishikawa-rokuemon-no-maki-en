"""Protect the fan ribs and snow badge border around the new lettering."""
import sys
from pathlib import Path

from PIL import Image
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import gen_gfx  # noqa: E402
import gfx  # noqa: E402
import gfx_event_props  # noqa: E402

pytestmark = pytest.mark.skipif(not gfx.TREE.exists(), reason='needs work/disc')


def test_snow_badge_preserves_oval_and_all_other_pixels():
    before = gfx_event_props.snow_source()
    after = before.copy()
    for entry, width, x in ((0, 240, 0), (1, 80, 240)):
        im = Image.open(gen_gfx.png_path(f'EVT110D.BIN:{entry}')).convert('RGBA')
        after.paste(im.crop((0, 0, width, 256)), (x, 0))
    erased = gfx_event_props.snow_mask(before)
    for y in range(256):
        for x in range(320):
            # New K and its outline occupy this interior box; every original
            # oval-border pixel is outside both this box and the old-ink mask.
            if not erased.getpixel((x, y)) and not (233 <= x < 250 and 107 <= y < 130):
                assert before.getpixel((x, y)) == after.getpixel((x, y)), (x, y)
    assert after.getchannel('A').tobytes() == before.getchannel('A').tobytes()
    assert after.crop((218, 96, 270, 141)).tobytes() != before.crop((218, 96, 270, 141)).tobytes()


def test_fans_preserve_ribs_and_redraw_reproducibly():
    for key in gfx_event_props.KEYS:
        texture, before = gen_gfx.original(key)
        after = Image.open(gen_gfx.png_path(key)).convert('RGBA')
        generated = before.copy()
        gfx_event_props.draw(generated, key, set(gfx.palette(texture, 0)))
        assert generated.tobytes() == after.tobytes(), key
        if key not in gfx_event_props.FANS:
            continue
        if key.endswith(':0'):
            # The first fresh cold review exposed these cream antialias
            # pixels beyond the small fan's red glyph body.
            background = before.getpixel((5, 72))
            for point in ((24, 67), (25, 68), (25, 70), (24, 71), (25, 72), (26, 73)):
                assert before.getpixel(point) != background
                assert after.getpixel(point) == background, point
        for rect in ([(131, 15, 150, 25), (12, 79, 32, 91)] if key.endswith(':0') else
                     [(31, 155, 57, 170), (59, 159, 80, 173)]):
            assert before.crop(rect).tobytes() == after.crop(rect).tobytes(), (key, rect)
