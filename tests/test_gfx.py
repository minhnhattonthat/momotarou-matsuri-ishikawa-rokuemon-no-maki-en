"""Graphics redraws (tools/gfx.py): the original image re-imported gives the original TIM, an edited pixel changes
only that pixel, colours outside the CLUT are refused."""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import arc  # noqa: E402
import gfx  # noqa: E402
import gen_gfx  # noqa: E402
import gen_card_words  # noqa: E402
import gfx_results  # noqa: E402
import gfx_racers  # noqa: E402
import gfx_hud  # noqa: E402
import gfx_signs  # noqa: E402
import gfx_intro  # noqa: E402
import tim  # noqa: E402

pytestmark = pytest.mark.skipif(not gfx.TREE.exists(), reason="needs work/disc (dumpsxiso)")


def test_pixel_labels_have_every_glyph_and_fit():
    for key, labels in gen_gfx.LABELS.items():
        for x0, y0, x1, y1, text, options in labels:
            if options.get('pixel'):
                mask = gen_gfx.fit(text, x1 - x0, y1 - y0, options)
                assert mask.width <= x1 - x0 and mask.height <= y1 - y0, (key, text)


def test_intro_props_preserve_silhouettes_cloth_and_fan_handles():
    from PIL import Image
    for entry in (1, 2):
        key = f'CHR0D.BIN:{entry}'
        _, before = gen_gfx.original(key)
        after = Image.open(gfx.EN / f'CHR0D_{entry}.png').convert('RGBA')
        # Restrict this comparison to portrait pixels; names intentionally
        # change their alpha masks in the lower atlas rows.
        height = 184 if entry == 2 else 208
        assert before.crop((0, 0, 256, height)).getchannel('A').tobytes() == (
            after.crop((0, 0, 256, height)).getchannel('A').tobytes())
        if entry == 2:
            for y in range(184):
                for x in range(256):
                    c = before.getpixel((x, y))
                    if max(c[:3]) - min(c[:3]) > 24:
                        assert after.getpixel((x, y)) == c, (x, y)
        else:
            # Bamboo ribs and handles adjacent to both translated fan faces.
            for rect in ((202, 102, 214, 124), (68, 235, 84, 248)):
                assert before.crop(rect).tobytes() == after.crop(rect).tobytes()


def test_roundtrip_and_one_pixel(tmp_path):
    for name, e in (("CI0D.BIN", 3), ("NAME0D.BIN", 0)):
        t, _ = gfx.unpack(arc.entries((gfx.TREE / name).read_bytes())[e][1])
        im = tim.image(t)
        p = tmp_path / "a.png"
        im.save(p)
        assert gfx.redraw(t, p) == t
        pal = [c for c in gfx.palette(t, 0) if c[3]]
        old = im.getpixel((5, 5))
        im.putpixel((5, 5), next(c for c in pal if c != old))
        im.save(p)
        n = gfx.redraw(t, p)
        assert gfx.changed_box(t, p) == (5, 5, 6, 6)
        assert sum(a != b for a, b in zip(gfx.indices(t), gfx.indices(n))) == 1
        im.putpixel((5, 5), (1, 2, 3, 255))
        im.save(p)
        with pytest.raises(ValueError):
            gfx.redraw(t, p)


def test_redraws_change_only_declared_label_rectangles():
    card_rects = {}
    for row in gen_card_words.rows():
        i = row['card'] - 1
        key = f'HCARD{i // 10}0D.BIN:{i % 10}'
        card_rects[key] = [tuple(row[k] for k in ('x0', 'y0', 'x1', 'y1')),
                           *gen_card_words.ERASE_RECTS.get(i + 1, [])]
    for key, labels in gen_gfx.LABELS.items():
        rects = [(x0, y0, x1, y1) for x0, y0, x1, y1, _, _ in labels]
        rects += card_rects.get(key, [])
        if key == 'M990D.BIN:0':
            rects += gfx_results.CLEAR_RECTS
            rects += [gfx_hud.RECT]
        if key == 'M230D.BIN:3':
            rects += [gfx_racers.RECT]
        if key == 'M340D.BIN:1':
            rects += [gfx_hud.PANEL_RECT]
        for _, pieces, _, _, _, _ in gfx_signs.SIGNS.get(key, []):
            rects += [(u, v, u + w, v + h) for u, v, w, h, _, _ in pieces]
        rects += [(u, v, u + w, v + h) for _, pieces in gen_gfx.COMPOSITES.get(key, [])
                  for u, v, w, h, _, _ in pieces]
        rects += gfx_intro.rectangles(key)
        name, entry = key.split(':')
        t, _ = gen_gfx.original(key)
        png = gfx.EN / f'{Path(name).stem}_{entry}.png'
        before, after = gfx.indices(t), gfx.indices(gfx.redraw(t, png))
        width = gfx.layout(t)[1]
        changed = [i for i, (a, b) in enumerate(zip(before, after)) if a != b]
        assert changed, key
        for i in changed:
            x, y = i % width, i // width
            assert any(x0 <= x < x1 and y0 <= y < y1 for x0, y0, x1, y1 in rects), (key, x, y)
