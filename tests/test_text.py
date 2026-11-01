"""Phase 4 extraction: roundtrip, jump relocation, coverage, script/ freshness (docs/re/script.md).

Disc-backed: skips without work/disc (dumpsxiso, tools/build.py)."""
import json
import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import arc  # noqa: E402
import codestr  # noqa: E402
import script  # noqa: E402
import text  # noqa: E402

disc = pytest.mark.skipif(not (ROOT / "work" / "disc" / "tree").exists(), reason="needs work/disc (dumpsxiso)")

# Japanese-looking runs no extracted string covers, all checked by eye as binary data (graphics, sound, code).
NOISE_ARCHIVE = {("CI0D", 0xD90C), ("ECTBG24D", 0x34D78), ("EVT020D", 0x1492), ("GCV0130D", 0x34C2C),
                 ("M100D", 0xCE92), ("TITLE0D", 0xD98C)}
NOISE_CODE = {("OVLM49", 0x938), ("OVLM56", 0x518)}


def all_script_entries():
    for f in text.archives():
        for i, e, its in text.script_entries(open(f, "rb").read()):
            yield f, i, e, its


def test_msg_codec_synthetic():
    t = "「あ{bb}い{ww}\n　う{KP}\nえ{KN}"
    b = text.encode_msg(t)
    assert b == ("「あbbいww".encode("cp932") + b"KG\0\0" + "　うKP".encode("cp932") + b"\0\0"
                 + "えKN".encode("cp932") + b"\0\0")
    assert text.msg_text(text.split_lines(b)) == t
    with pytest.raises(ValueError):
        text.encode_msg("あ{KP}")  # a message cannot end on a page break


@pytest.mark.parametrize('suffix', ['段', '時間', '分', '点', '個', '：', '両'])
def test_referenced_number_templates_include_short_units(suffix):
    raw = b'      ' + suffix.encode('cp932')
    data = b'\0' * 4 + raw + b'\0'
    assert codestr.strings(data, {0x80010004: [('ptr', 0)]}, 0x80010000) == [(4, 4 + len(raw))]
    if len(suffix) == 1 and suffix != '両':
        assert not codestr.is_jp(suffix.encode('cp932'))  # retain the instruction-noise filter


@disc
def test_every_script_entry_rebuilds_byte_identical():
    n = 0
    for f, i, e, its in all_script_entries():
        texts = {o: [s for _, s in strs] for o, op, _, strs in its}
        assert text.rebuild(e, texts) == e, (f, i)
        n += len(texts)
    assert n >= 5329  # text ops (4,894 msg + 408 menu + 27 caption)


@disc
def test_grown_text_keeps_jumps_on_their_ops():
    checked = 0
    for f, i, e, its in all_script_entries():
        old = list(script.ops(e))
        if not any(script.jumps(e, o, op) for o, op, _ in old):
            continue
        grow = {o: [s + "\n　" if op == 0x02 else s + "　" for _, s in strs] for o, op, _, strs in its}
        new = text.rebuild(e, grow)
        nops = list(script.ops(new))
        assert [op for _, op, _ in nops] == [op for _, op, _ in old], (f, i)
        idx_old = {o: k for k, (o, _, _) in enumerate(old)}
        idx_new = {o: k for k, (o, _, _) in enumerate(nops)}
        for (o, op, _), (no, _, _) in zip(old, nops):
            for (_, t), (_, nt) in zip(script.jumps(e, o, op), script.jumps(new, no, op)):
                if t in idx_old:
                    assert idx_new.get(nt) == idx_old[t], (f, i, hex(o))
        assert len(new) > len(e)
        checked += 1
    assert checked > 500


@disc
def test_archive_text_fully_covered():
    import re
    miss = set()
    for f in text.archives():
        d = open(f, "rb").read()
        rs = text.covered_ranges(d)
        for a, b, _ in text.jp_runs(d):
            if any(x <= a and b <= y for x, y in rs):
                continue
            if a % 2 == 0 and (d[b:b + 1] == b"\0" or re.match(rb"[A-Za-z]{2}", d[b:b + 2])):
                miss.add((text.stem(f), a))
    assert miss == NOISE_ARCHIVE


@disc
def test_code_strings_cover_and_roundtrip():
    miss = set()
    n = 0
    for p in codestr.code_files():
        rows, unref = codestr.table(p)
        miss |= {(os.path.basename(p).split(".")[0], a) for a, _ in unref}
        for r in rows:
            jp = text.table().decode(r["raw"], 0, len(r["raw"]))[0]
            assert "[" not in jp.replace("[20]", ""), (p, hex(r["addr"]), jp)  # [20] = money-template digit slots
            assert text.table().encode(jp) == r["raw"]
            assert r["refs"] and r["cap"] > len(r["raw"])
            n += 1
    assert miss == NOISE_CODE
    assert n > 1100


@disc
def test_script_json_matches_disc():
    """jp and ids in script/ equal a fresh extraction (a codec fix must regenerate jp: text.py dump --force,
    keeping en)."""
    seen = set()
    for f in text.text_files():
        path = ROOT / "script" / (os.path.basename(f).split(".")[0] + ".json")
        fresh = text.extract(f)
        if not fresh:
            assert not path.exists(), path
            continue
        rows = json.loads(path.read_text(encoding="utf-8"))
        assert [(r["id"], r["jp"]) for r in rows] == [(r["id"], r["jp"]) for r in fresh], path.name
        seen.add(path.name)
    assert {p.name for p in (ROOT / "script").glob("*.json")} == seen
