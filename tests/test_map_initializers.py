"""Warps must run the real map initializer, including actors and decorations."""
import struct
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools' / 'debug'))
import gen_scenes  # noqa: E402
import fileids  # noqa: E402
import arc  # noqa: E402

pytestmark = pytest.mark.skipif(not Path(gen_scenes.TREE).exists(), reason='needs work/disc')


def test_every_arrival_has_a_real_initializer():
    initializers = gen_scenes.initializers()
    assert set(gen_scenes.arrivals()) <= initializers.keys()
    table = (Path(gen_scenes.TREE) / 'OVLGMAIN.BIN').read_bytes()
    names = fileids.names()
    expected = {9: ('GSF0401D.BIN', 1), 29: ('GSF1200D.BIN', 2),
                35: ('GSF1206D.BIN', 1), 140: ('GSV1001D.BIN', 1),
                163: ('GSV1300D.BIN', 1), 189: ('GSV1609D.BIN', 1),
                332: ('GSV3611D.BIN', 1), 333: ('GSV3612D.BIN', 1)}
    for m, target in expected.items():
        fid, entry = struct.unpack_from('<II', table, 0x800E480C - 0x800CB338 + 8 * initializers[m])
        assert (fileids.data_name(names, fid), entry) == target


def test_scene_list_never_falls_back_to_world_map_initialization():
    initializers = gen_scenes.initializers()
    for line in (ROOT / 'tools/debug/scenes.txt').read_text().splitlines():
        fields = line.split('#')[0].split()
        if len(fields) > 1 and fields[1] == 'map':
            assert len(fields) == (9 if int(fields[2]) in gen_scenes.MAP_OPS else 7)
            assert int(fields[6], 0) == initializers[int(fields[2])]
    # These nine maps were previously excluded after using the wrong initializer.
    maps = {int(line.split()[2]) for line in (ROOT / 'tools/debug/scenes.txt').read_text().splitlines()
            if line.startswith('map_')}
    assert {9, 29, 30, 31, 34, 187, 201, 204, 294} <= maps


def test_map_294_setup_matches_its_normal_entry_script():
    data = arc.entries((Path(gen_scenes.TREE) / 'GSF0000D.BIN').read_bytes())[25][1]
    before, after = gen_scenes.MAP_OPS[294]
    assert struct.pack('<4H', *before) == data[0x10:0x18]
    assert struct.pack('<4H', *after) == data[0x24:0x2C]
