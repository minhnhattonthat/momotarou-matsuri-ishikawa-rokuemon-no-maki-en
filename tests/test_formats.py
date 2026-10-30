"""Disc formats (docs/re/disc.md): ECD codec, archives, the EXE LBA table. Disc-backed tests skip without work/disc."""
import struct
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import arc  # noqa: E402
import ecd  # noqa: E402

TREE = ROOT / "work" / "disc" / "tree"
BIN = next((ROOT / "rom").glob("*.bin"), None) if (ROOT / "rom").exists() else None
disc = pytest.mark.skipif(not TREE.exists(), reason="needs work/disc (dumpsxiso)")


def test_ecd_roundtrip_synthetic():
    data = b"\x10\0\0\0\x08\0\0\0" + bytes(300) + b"abcabcabcabc" * 40 + bytes(range(256)) * 3 + bytes(2000)
    c = ecd.compress(data, raw=8)
    assert ecd.decompress(c) == data
    assert len(c) < len(data)


@disc
def test_ecd_every_entry_decodes_and_roundtrips():
    n = 0
    for f in sorted((TREE / "OUTBIN").glob("*D.BIN"))[::7]:  # every 7th file keeps the test quick
        for _, e in arc.entries(f.read_bytes()) or []:
            if e[:4] == ecd.MAGIC:
                u = ecd.decompress(e)
                assert ecd.decompress(ecd.compress(u, ecd.header(e)[0])) == u
                n += 1
    assert n > 200


@disc
def test_archives_parse():
    files = sorted((TREE / "OUTBIN").glob("*D.BIN"))
    assert len(files) == 1543
    for f in files:
        assert arc.offsets(f.read_bytes()), f.name


@disc
@pytest.mark.skipif(BIN is None, reason="needs the disc image")
def test_exe_lba_table_matches_iso():
    import iso
    lb = {lba: size for _, lba, size in iso.files(str(BIN))}
    exe = (TREE / "SLPM_868.88").read_bytes()
    for i in range(1606):
        a, b = struct.unpack_from("<2I", exe, 0x6F1B0 + 8 * i)
        assert b - a == (lb[a] + 2047) // 2048
