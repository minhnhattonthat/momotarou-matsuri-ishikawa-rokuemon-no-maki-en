"""A monochrome word must not pass visual coverage on a featureless panel."""
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools' / 'debug'))
from announcements_qa import match  # noqa: E402


def test_match_requires_contrast_at_transparent_glyph_edges():
    glyph = Image.new('RGBA', (5, 7))
    for x, y in [(2, y) for y in range(1, 6)] + [(x, 3) for x in range(1, 4)]:
        glyph.putpixel((x, y), (248, 248, 248, 255))
    assert match(Image.new('RGB', (20, 20), (248, 248, 248)), glyph) is None
    screen = Image.new('RGB', (20, 20), (60, 40, 20))
    screen.paste(glyph, (8, 9), glyph)
    assert match(screen, glyph) == (8, 9)
    screen.putpixel((10, 12), (60, 40, 20))
    assert match(screen, glyph) is None
    # A dark outline may disappear into a black background; complete coloured
    # ink must still match without demanding contrast at the outermost edge.
    outlined = Image.new('RGBA', (8, 8))
    for y in range(1, 7):
        for x in range(1, 7):
            outlined.putpixel((x, y), (0, 0, 0, 255))
    outlined.putpixel((3, 3), (248, 248, 248, 255))
    screen = Image.new('RGB', (20, 20))
    screen.paste(outlined, (5, 6), outlined)
    assert match(screen, outlined) == (5, 6)
