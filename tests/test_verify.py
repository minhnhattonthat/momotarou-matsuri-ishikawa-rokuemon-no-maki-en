"""Phase 7 ROM-level checks (tools/verify_build.py): every file insert changes stays inside its allowed ranges
(code files) or changes only text (archives), and the checks catch a stray byte."""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import arc  # noqa: E402
import build  # noqa: E402
import insert  # noqa: E402
import text  # noqa: E402
import verify_build as v  # noqa: E402

disc = pytest.mark.skipif(not build.TREE.exists(), reason="needs work/disc (dumpsxiso)")


@pytest.fixture(scope="module")
def want():
    return insert.files("en")


@disc
def test_every_changed_file_passes_its_range_or_structure_check(want):
    rows = insert.rows_by_file()
    errs = [e for name, n in want.items() for e in v.check_file(name, (build.TREE / name).read_bytes(), n, rows)]
    assert errs == []
    assert len(want) > 300


@disc
def test_checks_catch_a_changed_op_byte_and_a_code_byte(want):
    rows = insert.rows_by_file()
    name = next(k for k in want if not Path(k).stem.startswith(("OVL", "FONT", "SLPM")))
    o, n = (build.TREE / name).read_bytes(), bytearray(want[name])
    n[arc.entries(bytes(n))[text.script_entries(o)[0][0]][0] + 1] ^= 1   # an op header byte, not text
    assert v.check_file(name, o, bytes(n), rows)
    for name in ("OUTBIN/OVLGMAIN.BIN", "OUTBIN/OVLXTTL.BIN", build.EXE):
        stem = Path(name).stem
        ok = v.code_allowed(build.TREE / name, stem, rows["SLPM_868" if name == build.EXE else stem])
        n = bytearray(want[name])
        n[next(i for i in range(0x900, len(n)) if i not in ok)] ^= 1      # no string, hook or table there
        assert v.check_file(name, (build.TREE / name).read_bytes(), bytes(n), rows), name


@disc
def test_no_branch_lands_inside_a_hook_span():
    assert v.hook_branch_targets((build.TREE / build.EXE).read_bytes()) == []
