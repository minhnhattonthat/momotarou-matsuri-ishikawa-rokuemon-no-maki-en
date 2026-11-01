"""Rain may recolour a whole sign; it may not remove or change any pixels."""
import sys
from pathlib import Path

from PIL import Image
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools' / 'debug'))
from field_signs import match_remapped  # noqa: E402


def test_weather_requires_complete_injective_pixel_pattern():
    template = Image.new('RGBA', (5, 3))
    colours = [(40, 20, 8, 255), (200, 200, 200, 255), (80, 48, 16, 255)]
    indices = [0, 1, 0, 1, 2, 1, 1, 2, 0, 1, 2, 0, 1, 2, 0]
    template.putdata([colours[i] for i in indices])
    dark = Image.new('RGB', template.size)
    palette = [(8, 4, 1), (32, 32, 56), (16, 8, 4)]
    dark.putdata([palette[i] for i in indices])
    screen = Image.new('RGB', (10, 8))
    screen.paste(dark, (3, 4))
    assert match_remapped(screen, template) == (3, 4)
    screen.putpixel((5, 5), palette[0])
    assert match_remapped(screen, template) is None
    assert match_remapped(Image.new('RGB', (10, 8), 'white'), template) is None
    assert match_remapped(dark.crop((0, 0, 4, 3)), template) is None
    template.putpixel((0, 0), (0, 0, 0, 0))
    with pytest.raises(ValueError, match='opaque'):
        match_remapped(screen, template)
