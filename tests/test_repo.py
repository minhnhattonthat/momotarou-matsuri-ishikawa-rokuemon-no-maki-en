"""Repo invariants that hold without the ROM (a fresh clone runs these too)."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_rom_sha1_pins_the_dump():
    lines = [l for l in (ROOT / "rom.sha1").read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]
    assert lines, "rom.sha1 lists no file"
    for line in lines:
        assert re.fullmatch(r"[0-9a-f]{40}  rom/.+", line), line
