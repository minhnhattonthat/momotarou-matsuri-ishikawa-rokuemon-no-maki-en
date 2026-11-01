"""A successful route must not certify missing or partly obscured lettering."""
import sys
from pathlib import Path

from PIL import Image
import pytest

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


def test_tiny_glyph_search_cannot_match_unrelated_panel_pixels():
    screen = Image.new('RGB', (40, 30))
    template = Image.new('RGBA', (1, 8))
    template.putpixel((0, 6), (248, 248, 248, 255))
    screen.putpixel((3, 9), (248, 248, 248))  # unrelated UI corner
    assert announcements_qa.match(screen, template) == (3, 3)
    assert announcements_qa.match(screen, template, (20, 12, 16, 16)) is None
    screen.putpixel((25, 22), (248, 248, 248))
    assert announcements_qa.match(screen, template, (20, 12, 16, 16)) == (25, 16)


@pytest.mark.skipif(not announcements_qa.gfx.TREE.exists(), reason='needs work/disc')
def test_bounded_cold_scan_skips_display_off_frames(tmp_path, monkeypatch):
    import tim
    archive = announcements_qa.arc.entries((announcements_qa.gfx.TREE / 'M990D.BIN').read_bytes())
    texture = announcements_qa.gfx.unpack(archive[0][1])[0]
    zero = tim.image(texture).crop((0, 0, 8, 16))
    Image.new('RGB', (1, 1)).save(tmp_path / 'f000001.png')
    screen = Image.new('RGB', (40, 30), (80, 100, 120))
    screen.paste(zero, (24, 12), zero)
    screen.save(tmp_path / 'f000002.png')
    monkeypatch.setattr(sys, 'argv', ['announcements_qa.py', str(tmp_path), '--out', str(tmp_path / 'coverage'),
                                    '--original', '--entry', '2', '--items', '0', '--scan',
                                    '--region', '20,12,16,16'])
    assert announcements_qa.main() == 0
    assert 'f000002.png' in (tmp_path / 'coverage/coverage.tsv').read_text(encoding='utf-8')
