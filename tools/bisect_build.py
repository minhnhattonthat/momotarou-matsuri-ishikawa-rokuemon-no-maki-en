"""Build the marker disc with only some changed files, to find which one breaks a boot.

    python -X utf8 tools/bisect_build.py OUT.bin [--mode marker] PATTERN [PATTERN ...]

Keeps the engine files (EXE hooks, FONT0D) and every other changed file whose disc path matches a glob
PATTERN; '!PATTERN' excludes. Code strings in the EXE stay only if SLPM* matches (else the engine-only EXE).
"""
import argparse
import fnmatch
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import build  # noqa: E402
import engine  # noqa: E402
import insert  # noqa: E402

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('out', type=Path)
    ap.add_argument('--mode', default='marker')
    ap.add_argument('patterns', nargs='+')
    a = ap.parse_args()
    files = insert.files(a.mode)
    inc = [p for p in a.patterns if not p.startswith('!')]
    exc = [p[1:] for p in a.patterns if p.startswith('!')]
    keep = {k: v for k, v in files.items()
            if any(fnmatch.fnmatch(k, p) for p in inc) and not any(fnmatch.fnmatch(k, p) for p in exc)}
    keep.setdefault('SLPM_868.88', engine.patch_exe((insert.TREE / 'SLPM_868.88').read_bytes()))
    keep['OUTBIN/FONT0D.BIN'] = files['OUTBIN/FONT0D.BIN']
    print(sorted(keep)[:10], len(keep))
    a.out.parent.mkdir(parents=True, exist_ok=True)
    print(build.build(a.out.resolve(), keep))
