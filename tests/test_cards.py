"""Card captions use only the name strip; runtime coverage must reject stale art."""
import sys
from pathlib import Path

import pytest
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(ROOT / 'tools' / 'debug'))
import cards_qa  # noqa: E402
import gen_gfx  # noqa: E402
import gfx  # noqa: E402

pytestmark = pytest.mark.skipif(not gfx.TREE.exists(), reason='needs work/disc')


def test_all_card_captions_preserve_numbers_and_art():
    names = [name for name, count in gen_gfx.PREFECTURES for _ in range(count)]
    assert len(names) == 100
    assert len(cards_qa.meanings()) == 100
    for i in range(100):
        key = f'HCARD{i // 10}0D.BIN:{i % 10}'
        _, original = gen_gfx.original(key)
        with Image.open(gfx.EN / f'HCARD{i // 10}0D_{i % 10}.png') as translated:
            assert original.crop((0, 0, 208, 128)).tobytes() == translated.crop((0, 0, 208, 128)).tobytes()
            assert original.crop((0, 128, 48, 144)).tobytes() == translated.crop((0, 128, 48, 144)).tobytes()
            assert original.crop((48, 128, 120, 144)).tobytes() != translated.crop((48, 128, 120, 144)).tobytes()


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
