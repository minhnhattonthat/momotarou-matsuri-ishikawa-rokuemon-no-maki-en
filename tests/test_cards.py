"""Card redraws preserve undeclared artwork; runtime coverage rejects stale art."""
import sys
from pathlib import Path

import pytest
from PIL import Image, ImageChops, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(ROOT / 'tools' / 'debug'))
import cards_qa  # noqa: E402
import gen_gfx  # noqa: E402
import gen_card_words  # noqa: E402
import gfx  # noqa: E402

pytestmark = pytest.mark.skipif(not gfx.TREE.exists(), reason='needs work/disc')


def test_all_card_captions_preserve_numbers_and_art():
    names = [name for name, count in gen_gfx.PREFECTURES for _ in range(count)]
    assert len(names) == 100
    assert len(cards_qa.meanings()) == 100
    words = gen_card_words.rows()
    for i in range(100):
        key = f'HCARD{i // 10}0D.BIN:{i % 10}'
        _, original = gen_gfx.original(key)
        with Image.open(gfx.EN / f'HCARD{i // 10}0D_{i % 10}.png') as translated:
            row = words[i]
            rect = tuple(row[k] for k in ('x0', 'y0', 'x1', 'y1'))
            allowed = Image.new('L', original.size)
            draw = ImageDraw.Draw(allowed)
            for x0, y0, x1, y1 in [rect, *gen_card_words.ERASE_RECTS.get(i + 1, []), (48, 128, 120, 144)]:
                assert 0 <= x0 < x1 <= 208 and 0 <= y0 < y1 <= 144
                draw.rectangle((x0, y0, x1 - 1, y1 - 1), fill=255)
            difference = ImageChops.difference(original.convert('RGB'), translated.convert('RGB'))
            difference.paste((0, 0, 0), (0, 0, *difference.size), allowed)
            assert difference.getbbox() is None, f'card {i + 1}: changed undeclared artwork'
            assert original.crop(rect).tobytes() != translated.crop(rect).tobytes()
            assert original.crop((0, 128, 48, 144)).tobytes() == translated.crop((0, 128, 48, 144)).tobytes()
            assert original.crop((48, 128, 120, 144)).tobytes() != translated.crop((48, 128, 120, 144)).tobytes()


def test_card_gate_rejects_old_japanese_dialect_caption():
    _, original = gen_gfx.original('HCARD00D.BIN:0')
    with Image.open(gfx.EN / 'HCARD00D_0.png') as translated:
        template = translated.crop((0, 0, 208, 128)).convert('RGBA')
    screen = Image.new('RGB', (320, 240))
    screen.paste(original.crop((0, 0, 208, 128)), (56, 56))
    assert not cards_qa.matches(screen, template, 56, 56)
    screen.paste(template, (56, 56))
    assert cards_qa.matches(screen, template, 56, 56)


def test_card_margin_edits_preserve_nearby_props():
    # Full-card review caught broad white clears cutting the bottle, tail,
    # club and blue hair. These are artwork, even inside a caption's bounds.
    for i, rect in ((9, (175, 94, 203, 128)), (48, (5, 90, 32, 128)),
                    (79, (176, 35, 186, 85)), (99, (180, 70, 186, 102))):
        _, original = gen_gfx.original(f'HCARD{i // 10}0D.BIN:{i % 10}')
        with Image.open(gfx.EN / f'HCARD{i // 10}0D_{i % 10}.png') as translated:
            assert original.crop(rect).tobytes() == translated.crop(rect).tobytes(), f'card {i + 1}'


def test_card_gate_rejects_old_caption_and_wrong_card():
    _, original = gen_gfx.original('HCARD00D.BIN:0')
    with Image.open(gfx.EN / 'HCARD00D_0.png') as translated:
        caption = translated.crop((0, 128, 120, 144)).convert('RGBA')
    screen = Image.new('RGB', (320, 240))
    screen.paste(original.crop((0, 128, 120, 144)), (88, 32))
    assert not cards_qa.matches(screen, caption, 88, 32)
    screen.paste(caption, (88, 32))
    assert cards_qa.matches(screen, caption, 88, 32)
    _, wrong = gen_gfx.original('HCARD00D.BIN:1')
    screen.paste(wrong.crop((0, 0, 208, 128)), (56, 56))
    assert not cards_qa.matches(screen, original.crop((0, 0, 208, 128)), 56, 56)
