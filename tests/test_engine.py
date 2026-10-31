"""English engine (tools/engine.py): digraph codec, widths, font cells, EXE hooks. Skips without work/disc."""
import struct
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import arc  # noqa: E402
import ecd  # noqa: E402
import engine  # noqa: E402
import text  # noqa: E402

TREE = ROOT / "work" / "disc" / "tree"
disc = pytest.mark.skipif(not (TREE / "SLPM_868.88").is_file(), reason="needs work/disc (tools/build.py)")


def units(b):
    return [struct.unpack_from("<H", b, i)[0] for i in range(0, len(b), 2)]


@pytest.mark.parametrize("s", ["Hello, good book", "bb", "  ", "KGKPKN MM R0 ww oo", "a", "", "aww dd", "~" * 63])
def test_digraphs_never_hit_a_control_code_and_keep_every_char(s):
    b = engine.encode_ascii(s)
    assert len(b) % 2 == 0
    assert not set(units(b)) & engine.CONTROL
    assert all(engine.FIRST <= c <= engine.LAST for c in b)
    assert b.replace(bytes([engine.PAD]), b"").decode("ascii") == s


def test_mixed_line_keeps_codes_and_japanese_aligned():
    b = text.encode_line("{bb}Momo{ww} got ○ x2!{KG}")
    assert len(b) % 2 == 0 and b.endswith(b"KG\0\0")
    assert b[:2] == b"bb" and b"\x81\x9b" in b  # ○ as one Shift-JIS unit
    # Japanese-only text encodes as before (no ASCII, so no digraphs)
    assert text.encode_line("桃太郎{KP}") == "桃太郎".encode("cp932") + b"KP\0\0"


def test_widths_fit_the_cell_and_pad_is_invisible():
    w = engine.widths()
    assert len(w) == engine.LAST - engine.FIRST + 1
    assert w[engine.PAD - engine.FIRST] == 0 and w[0] == engine.SPACE_W
    assert all(0 < x <= 12 for c, x in enumerate(w, engine.FIRST) if c not in (0x20, engine.PAD))
    assert engine.width_px("ab") == w[0x41] + w[0x42] and engine.width_px("桃{KG}") == 12


@disc
def test_font_cells_hold_the_glyphs_and_other_pages_are_untouched():
    orig = (TREE / "OUTBIN" / "FONT0D.BIN").read_bytes()
    new = engine.patch_font(orig)
    a = ecd.decompress(arc.entries(orig)[0][1])
    b = ecd.decompress(arc.entries(new)[0][1])
    pix, stride = engine.tim_pixels(b)
    assert a[:pix] == b[:pix] and len(a) == len(b)
    for i in range(pix, len(a)):  # page 0 (bits 2-3 of each nibble) unchanged
        assert a[i] & 0xCC == b[i] & 0xCC
    u, v = engine.cell(ord("A"))
    ink = sum((b[pix + (v + y) * stride + (u + x) // 2] >> 4 * ((u + x) & 1) & 3) == 3
              for y in range(12) for x in range(12))
    assert ink > 10
    assert arc.entries(new)[1][1] == arc.entries(orig)[1][1]


@disc
def test_exe_hooks_assemble_inside_the_free_area():
    exe = (TREE / "SLPM_868.88").read_bytes()
    new = engine.patch_exe(exe)
    lo, hi = engine.FREE - engine.EXE_BASE, engine.FREE_END - engine.EXE_BASE
    diff = [i for i in range(len(exe)) if exe[i] != new[i]]
    hooks = {a - engine.EXE_BASE + k for a in engine.ORIG for k in range(4)}
    assert all(lo <= i < hi or i in hooks for i in diff)
    assert struct.unpack_from("<I", new, 0x80029AC4 - engine.EXE_BASE)[0] >> 26 == 2  # j append_hook
    with pytest.raises(ValueError):
        engine.patch_exe(new)  # original words checked: no double patch
