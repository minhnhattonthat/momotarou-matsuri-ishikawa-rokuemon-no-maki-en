"""Record columns preserve full units and the native 12px numeric cells."""
import json
import struct
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import engine  # noqa: E402


def test_maximal_records_fit_after_rank_and_heading():
    heading = engine.RECORD_LAYOUT[0x800DAC88][1] & 0xFFFF
    value = engine.RECORD_LAYOUT[0x800DAD24][1] & 0xFFFF
    assert 48 + engine.width_px('Rank: Full Mastery') + 8 <= heading
    assert heading + engine.width_px('Record') + 8 <= value
    rows = json.loads((ROOT / 'script/OVLXTTL.json').read_text(encoding='utf-8'))
    for addr, digits, suffix in ((0x800CD14C, 4, ' points'), (0x800CD164, 4, ' items'),
                                 (0x800CD1A4, 6, ' ryo'), (0x800CD1C4, 5, ' points'),
                                 (0x800CD3F8, 4, ' points'), (0x800CD410, 4, ' items'),
                                 (0x800CD450, 6, ' ryo'), (0x800CD470, 5, ' points')):
        row = next(r for r in rows if r['id'] == f'OVLXTTL@{addr:08X}')
        assert row['en'] == '[20]' * (digits * 2) + suffix
        assert 184 + digits * 12 + engine.width_px(suffix) <= 280
    assert 184 + 24 + engine.width_px(':') < 214
    assert 214 + 24 + engine.width_px(':') < 244
    assert 244 + 24 <= 280


def test_record_patch_checks_revision_and_changes_only_declared_instructions():
    path = ROOT / 'work/disc/tree/OUTBIN/OVLXTTL.BIN'
    if not path.exists():
        pytest.skip('needs original disc extraction')
    original = path.read_bytes()
    patched = engine.patch_records(original)
    allowed = {a - 0x800CB338 + k for a in engine.RECORD_LAYOUT for k in range(4)}
    assert all(i in allowed for i, (a, b) in enumerate(zip(original, patched)) if a != b)
    assert len(patched) == len(original)
    for address, (_, new) in engine.RECORD_LAYOUT.items():
        assert struct.unpack_from('<I', patched, address - 0x800CB338)[0] == new
    with pytest.raises(ValueError):
        engine.patch_records(patched)
