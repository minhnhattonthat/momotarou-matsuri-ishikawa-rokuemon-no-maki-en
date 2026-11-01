"""A linear pixel match must not cross a texture row or drop later rows."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from gfxfind_rect import locations  # noqa: E402


def test_complete_rectangle_rejects_wrap_partial_and_bottom_overrun():
    pixels = b'abcXabcYabcZ'
    assert list(locations(pixels, 4, 3, [b'bc', b'bc'])) == [(1, 0), (1, 1)]
    assert list(locations(pixels, 4, 3, [b'Xa'])) == []
    assert list(locations(pixels, 4, 3, [b'bc', b'bZ'])) == []
