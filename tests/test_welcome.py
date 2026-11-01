"""Guard the split banner's native geometry, rim and unchanged village art."""
import sys
from pathlib import Path

from PIL import Image, ImageDraw
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import anm
import arc
import gen_gfx
import gfx
import gfx_welcome

pytestmark = pytest.mark.skipif(not gfx.TREE.exists(), reason='needs original disc tree')


def test_welcome_assembly_matches_native_item():
    archive = arc.entries((gfx.TREE / 'EVT220D.BIN').read_bytes())
    records = anm.items(archive[3][1])[1]
    assert [(r[1], r[2], r[3], r[4], r[8] + 128, r[9] + 64) for r in records] == list(gfx_welcome.PIECES)
    assert all(r[5:8] == (0, 481, 7) and r[10:12] == (4096, 4096) for r in records)


def test_welcome_preserves_rim_tacks_and_every_other_pixel():
    _, before = gen_gfx.original(gfx_welcome.KEY)
    after = Image.open(gen_gfx.png_path(gfx_welcome.KEY)).convert('RGBA')
    assert before.getchannel('A').tobytes() == after.getchannel('A').tobytes()
    a, b = gfx_welcome.assemble(before), gfx_welcome.assemble(after)
    mask = Image.new('L', a.size)
    ImageDraw.Draw(mask).polygon(gfx_welcome.INTERIOR, fill=255)
    for p, q, allowed in zip(a.getdata(), b.getdata(), mask.getdata()):
        if not allowed:
            assert p == q
    # The only dark pixels left inside the cleared paper must be the new
    # lettering; pale old antialias fringes are not permitted there.
    assert {q for q, allowed in zip(b.getdata(), mask.getdata()) if allowed} == {
        (248, 248, 248, 255), (0, 0, 0, 255)}
    regenerated = before.copy()
    gfx_welcome.draw(regenerated, set(before.getdata()))
    assert regenerated.tobytes() == after.tobytes()
