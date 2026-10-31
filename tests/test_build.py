"""Identity build (phase 3) and the EXE LBA-table rewrite. Skip without the dump in rom/."""
import hashlib
import struct
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import build  # noqa: E402
import iso  # noqa: E402

rom = pytest.mark.skipif(not build.CUE.with_suffix(".bin").is_file(), reason="needs the dump in rom/")


def sha1(p):
    with open(p, "rb") as f:
        return hashlib.file_digest(f, "sha1").hexdigest()


@rom
def test_identity_build_is_byte_identical(tmp_path):
    lines = (ROOT / "rom.sha1").read_text(encoding="utf-8").splitlines()
    want = next(l for l in lines if l.strip() and not l.startswith("#")).split()[0]
    assert sha1(build.build(tmp_path / "id.bin", changed={})) == want


@rom
def test_grown_file_moves_and_lba_table_follows(tmp_path):
    grown = "OUTBIN/CHR0D.BIN"  # an early file: everything after it shifts
    data = (build.TREE / grown).read_bytes() + bytes(5000)
    out = build.build(tmp_path / "grow.bin", changed={grown: data})
    disc = {name: (lba, size) for name, lba, size in iso.files(out)}
    orig = {name: lba for name, lba, _ in iso.files(build.CUE.with_suffix(".bin"))}
    assert disc["OUTBIN/CI0D.BIN"][0] > orig["OUTBIN/CI0D.BIN"]  # really moved
    exe = (tmp_path / "files" / build.EXE).read_bytes()
    spans = {(lba, lba + (size + 2047) // 2048) for name, (lba, size) in disc.items() if name.startswith("OUTBIN/")}
    table = {struct.unpack_from("<II", exe, build.TABLE + 8 * i) for i in range(build.COUNT)}
    assert len(table) == build.COUNT and table <= spans
    assert disc[grown][1] == len(data)
    sizes = {struct.unpack_from("<I", exe, build.SIZES + 4 * (i - build.DATA))[0]
             for i in range(build.DATA, build.COUNT)
             if struct.unpack_from("<I", exe, build.TABLE + 8 * i)[0] == disc[grown][0]}
    assert sizes == {len(data)}  # the loader allocates from this table
