"""Create a disposable memory-card fixture through the game's shrine save routine.

    python -X utf8 tools/debug/save_fixture.py [CUE] [--out work/qa/save_fixture]

The seed must be a formatted, empty PS1 card; emu.py copies it before use. The game writes slot 1 and its
checksum. No memory-card format editing, saved-game editing, or user playthrough is needed.
"""
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from skill import SKILL  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('cue', nargs='?', default=str(ROOT / 'build/momotarou-matsuri_en.cue'))
    ap.add_argument('--out', type=Path, default=ROOT / 'work/qa/save_fixture')
    ap.add_argument('--seed', type=Path, default=ROOT / 'tools/pcsx/memcard1.mcd')
    args = ap.parse_args()
    seed = args.seed.read_bytes()
    if len(seed) != 131072 or seed[:2] != b'MC' or any(seed[i * 128] != 0xA0 for i in range(1, 16)):
        ap.error('--seed must be a formatted empty 128 KiB memory card')
    cmd = [sys.executable, '-X', 'utf8', str(Path(SKILL) / 'scripts/emu.py'), args.cue,
           '--out', str(args.out), '--script', str(ROOT / 'tools/debug/warp.lua'),
           '--var', "SCENE='save_menu'", '--var', 'HOLD=6000', '--var', 'SAVE_CONFIRM=true',
           '--sav', str(args.seed), '--frames', '900', '--shot-every', '300', '--timeout', '120']
    result = subprocess.run(cmd, cwd=ROOT)
    if result.returncode:
        return result.returncode
    card = args.out / 'memcard1.mcd'
    saved = card.read_bytes()
    entries = [saved[i * 128:(i + 1) * 128] for i in range(1, 16)]
    if not any(e[0] == 0x51 and e[10:].startswith(b'BISLPM-86888-A\0') for e in entries):
        print('FAIL: the game did not create save slot 1', file=sys.stderr)
        return 1
    if args.seed.read_bytes() != seed:
        print('FAIL: the seed card changed', file=sys.stderr)
        return 1
    print(f'Game-written save fixture: {card.resolve()}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
