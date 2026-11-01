"""Small background labels must erase old ink without cutting adjacent art."""
import sys
from pathlib import Path

from PIL import Image
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import gen_gfx  # noqa: E402
import gfx  # noqa: E402
import gfx_props  # noqa: E402
import tim  # noqa: E402

pytestmark = pytest.mark.skipif(not gfx.TREE.exists(), reason='needs work/disc')


def test_sushi_eraser_removes_brown_antialiasing_and_retains_light_wood():
    _, original = gen_gfx.original('M440D.BIN:0')
    panel = original.crop((72, 48, 88, 76))
    before = list(panel.getdata())
    # Brown edge pixels were missed by the former greyscale-only mask.
    assert any(c[0] < 152 and max(c[:3]) - min(c[:3]) > 24 for c in before)
    gfx_props._clear(panel, 'wood')
    for old, new in zip(before, panel.getdata()):
        assert new[0] >= 152
        if old[0] >= 152:
            assert old == new


def test_prop_redraws_preserve_alpha_and_frames():
    for key in gfx_props.PROPS:
        _, before = gen_gfx.original(key)
        name, entry = key.split(':')
        with Image.open(gfx.EN / f'{Path(name).stem}_{entry}.png') as im:
            after = im.convert('RGBA')
        assert before.getchannel('A').tobytes() == after.getchannel('A').tobytes(), key
        # Bath curtains have their separate declared edits. Only compare the
        # small placard here; the existing signs test checks its neighbours.
        if key.startswith('GV'):
            before, after = before.crop((128, 0, 160, 24)), after.crop((128, 0, 160, 24))
            rects = [(1, 2, 31, 18)]
        else:
            rects = gfx_props.rectangles(key)
        for y in range(before.height):
            for x in range(before.width):
                if not any(x0 <= x < x1 and y0 <= y < y1 for x0, y0, x1, y1 in rects):
                    assert before.getpixel((x, y)) == after.getpixel((x, y)), (key, x, y)


def test_price_labels_use_complete_pixel_glyphs():
    for label in ('100', '200', '300', '400'):
        mask = gen_gfx.mask(label, 7, {'pixel': 'credits7.txt', 'tight': True})
        assert mask.height == 7
        assert mask.width == 11
        assert set(mask.getdata()) <= {0, 255}


def test_sushi_words_fit_above_the_natural_actor_occlusion():
    for key in gfx_props.SUSHI_ERASE:
        _, atlas = gen_gfx.original(key)
        for (x0, y0, x1, y1), lines, direction, _ in gfx_props.PROPS[key]:
            assert 0 <= x0 < x1 <= atlas.width
            assert direction == 'horizontal'
            assert y0 >= 48 and y1 <= 64
            assert len(lines) * 8 <= y1 - y0
            for line in lines:
                mask = gen_gfx.mask(line, 7, {'pixel': 'credits7.txt', 'tight': True})
                assert mask.width <= x1 - x0


def test_bath_placard_both_lines_have_dark_ink_in_runtime_palette():
    texture, _ = gen_gfx.original('GV16090D.BIN:1')
    for filename in ('GV16090D_1.png', 'GV36110D_1.png', 'GV36120D_1.png'):
        changed = gfx.redraw(texture, gfx.EN / filename)
        runtime = tim.image(changed, 2)
        for row, label in enumerate(('Private', 'Today')):
            mask = gen_gfx.mask(label, 7, {'pixel': 'credits7.txt', 'tight': True})
            x0, y0 = 129 + (30 - mask.width) // 2, 2 + row * 8
            for y in range(mask.height):
                for x in range(mask.width):
                    if mask.getpixel((x, y)):
                        assert runtime.getpixel((x0 + x, y0 + y)) == (32, 32, 32, 255)


def test_winning_flag_erases_both_original_kanji():
    _, before = gen_gfx.original('M170D.BIN:20')
    with Image.open(gfx.EN / 'M170D_20.png') as after:
        # The original draft edited only the top-right corner, leaving these
        # three substantial strokes from both characters untouched.
        for point in ((209, 32), (214, 76), (233, 61)):
            assert max(before.getpixel(point)[:3]) < 150
            assert min(after.getpixel(point)[:3]) >= 240
