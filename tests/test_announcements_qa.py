"""A successful route must not certify missing or partly obscured lettering."""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools' / 'debug'))
import announcements_qa  # noqa: E402


def test_coverage_requires_every_glyph_and_outline_pixel():
    template = Image.new('RGBA', (8, 8))
    for y in range(1, 7):
        for x in range(1, 7):
            template.putpixel((x, y), (216, 152 if x % 2 else 40, 96, 255))
    screen = Image.new('RGB', (24, 24), (80, 100, 120))
    assert announcements_qa.match(screen, template) is None
    screen.paste(template, (5, 9), template)
    assert announcements_qa.match(screen, template) == (5, 9)
    screen.putpixel((8, 13), (8, 8, 8))  # one covered letter pixel invalidates coverage
    assert announcements_qa.match(screen, template) is None
