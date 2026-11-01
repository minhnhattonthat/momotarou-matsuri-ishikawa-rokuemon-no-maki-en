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
def test_insert_rebuilds_an_archive_with_english_and_code_strings_in_place():
    import insert
    path = TREE / "OUTBIN" / "GDEF0D.BIN"
    new = insert.build_archive(path, {"GDEF0D/0/00DE": "Momotaro looked down.\nNothing there.{KN}"})
    e = arc.entries(new)[0][1]
    o, op, n = next(x for x in __import__("script").ops(e) if x[0] == 0xDE)
    lines = [engine.decode_units(x) for x in text.split_lines(e[o + text.TEXT_START[op]:o + n])]
    assert lines == ["Momotaro looked down.{KG}", "Nothing there.{KN}"]
    assert [x for _, x in arc.entries(new)[1:]] == [x for _, x in arc.entries(path.read_bytes())[1:]]
    rows = [{"id": "SLPM_868@8008C2D4", "max": 7}]
    exe = (TREE / "SLPM_868.88").read_bytes()
    out = insert.patch_code(exe, TREE / "SLPM_868.88", {"SLPM_868@8008C2D4": "Yes"}, rows)
    o = 0x8008C2D4 - engine.EXE_BASE
    assert out[o:o + 8] == b"Yes\x7f\0\0\0\0" and out[o + 8:] == exe[o + 8:] and out[:o] == exe[:o]
    with pytest.raises(ValueError):
        insert.patch_code(exe, TREE / "SLPM_868.88", {"SLPM_868@8008C2D4": "Too long"}, rows)


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


@disc
def test_every_item_has_a_box_budget_and_choices_use_fixed_layouts():
    import json
    import windows
    v = windows.variants()
    rows = [r for p in (ROOT / "script").glob("*.json") for r in json.loads(p.read_text(encoding="utf-8"))]
    assert {r["id"] for r in rows} <= set(v)
    assert sum(x in ("choice", "choice_top") for x in v.values()) == 1601
    assert all(windows.budget(r, v[r["id"]])[0] > 0 for r in rows)


@disc
def test_object_count_record_fits_four_digits_and_full_unit():
    import gfx_hud
    source = (TREE / 'SLPM_868.88').read_bytes()
    patched = engine.patch_exe(source)

    def imm(address):
        return struct.unpack_from('<I', patched, address - engine.EXE_BASE)[0] & 0xFFFF

    record_x = ((imm(0x80040B7C) << 16) | imm(0x80040B80)) >> 12
    unit_x = ((imm(0x80040C08) << 16) | imm(0x80040C0C)) >> 12
    number_x = imm(0x8003D8F8)
    placeholder_x = imm(0x8003D918)
    # Four 8px digits and the full 19px English unit must not meet the
    # Record heading or the panel's right inner edge at x296.
    assert record_x + 32 + 4 <= number_x
    assert number_x + 4 * 8 + 4 <= unit_x
    assert placeholder_x + 2 * 8 + 4 <= unit_x
    assert unit_x + gfx_hud.rect(78)[2] < 296
    floor_x = ((imm(0x80041880) << 16) | imm(0x80041884)) >> 12
    floor_number = imm(0x8003DAE8)
    assert floor_x + gfx_hud.rect(34)[2] + 4 <= floor_number
    assert floor_number + 2 * 8 < 88  # next timer icon begins at x88


@disc
def test_long_overlay_string_moves_into_slack_and_every_ref_follows():
    import codestr
    import insert
    p = TREE / "OUTBIN" / "OVLXTTL.BIN"
    rows = insert.rows_by_file()["OVLXTTL"]
    iid, addr = "OVLXTTL@800CB4E4", 0x800CB4E4
    row = next(r for r in rows if r["id"] == iid)
    long = "Relocated string " * 3
    others = {r["id"]: "x" for r in rows if r["id"] != iid}     # short English everywhere frees the slack
    out = insert.patch_code(p.read_bytes(), p, {**others, iid: long}, rows)
    d, base, _ = codestr.image(p)
    want = text.encode_text(long) + b"\0"
    refs = codestr.refs(d, base)[addr]
    assert refs and len(want) > row["max"] + 1
    for k in refs:
        if k[0] == "ptr":
            new = struct.unpack_from("<I", out, k[1])[0]
        else:
            hi, lw = struct.unpack_from("<I", out, k[1])[0] & 0xFFFF, struct.unpack_from("<I", out, k[2])[0]
            lo = lw & 0xFFFF
            new = (hi << 16) + (lo if lw >> 26 == 0x0D else lo - (lo & 0x8000) * 2)
        assert new != addr and new % 4 == 0 and out[new - base:new - base + len(want)] == want
    assert out[addr - base:addr - base + row["max"] + 1].endswith(b"\0")   # cut copy stays in place
