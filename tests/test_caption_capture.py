"""A successful warp must not approve an absent, wrong or off-centre caption."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools' / 'debug'))
from caption_tour import check_capture


def test_caption_requires_exact_text_and_centred_position():
    log = 'TEXT f100 140,60 Test\nCAPTION x=140 y=60 glyphs=2 f110\n'
    assert check_capture(log, 'Test', 40)[0] == 'ok'
    assert check_capture(log, 'Other', 40)[0] != 'ok'
    assert check_capture(log, 'Test', 42)[0] != 'ok'
    assert check_capture(log, 'Test', 200)[0] != 'ok'
    assert check_capture('ARRIVED map f200\n', 'Test', 40)[0] != 'ok'


def test_caption_decodes_original_glyphs_and_rejects_partial_lines():
    log = 'TEXT f100 154,60 {91BA}\nCAPTION x=154 y=60 glyphs=1 f110\n'
    assert check_capture(log, '村', 12)[0] == 'ok'
    assert check_capture(log, '村名', 12)[0] != 'ok'
