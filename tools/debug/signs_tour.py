"""Cold original/English map-sign routes and complete-lettering coverage.

    python tools/debug/signs_tour.py --out work/qa/signs8_final
    python tools/debug/signs_tour.py --original --out work/qa/signs8_jp
    python tools/debug/signs_tour.py --check-only --out work/qa/signs8_final

Bath routes use controller input after each map's own initializer. The contest
route starts in the courtyard with its real NPCs. GV02000D's retained contest
atlas is NOT covered: its default map contains no displayed contest board.
"""
import argparse
import csv
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from skill import SKILL  # noqa: E402
import gen_scenes  # noqa: E402
from field_signs import check  # noqa: E402

CASES = {
    'contest': (163, 40, 33, 0, 'GV13000D.BIN:2'),
    'bath189': (189, 21, 24, 2, 'GV16090D.BIN:1'),
    'bath332': (332, 21, 24, 2, 'GV16090D.BIN:1'),
    'bath333': (333, 21, 24, 2, 'GV16090D.BIN:1'),
    'games143': (143, 120, 26, 0, 'GV12000D.BIN:1'),
    'games144': (144, 120, 26, 0, 'GV12002D.BIN:1'),
    'games163': (163, 57, 32, 0, 'GV13000D.BIN:1'),
    'games295': (295, 19, 27, 0, 'GV32000D.BIN:1'),
    'games306a': (306, 21, 26, 0, 'GV34000D.BIN:1'),
    'games306b': (306, 60, 42, 0, 'GV34000D.BIN:1'),
    'games180': (180, 27, 79, 0, 'GV16000D.BIN:3'),
    'games237a': (237, 17, 16, 0, 'GV22000D.BIN:1'),
    'games237b': (237, 87, 40, 0, 'GV22000D.BIN:1'),
    'games238a': (238, 17, 16, 0, 'GV22000D.BIN:1'),
    'games238b': (238, 87, 40, 0, 'GV22000D.BIN:1'),
}


def run(name, args, initializers):
    m, x, y, direction, key = CASES[name]
    out = args.out / name
    out.mkdir(parents=True, exist_ok=True)
    if not args.check_only:
        # emu.py clears numbered frames but keeps custom Lua screenshot names.
        # Delete only this harness's captures, so an old successful walk cannot
        # supply a missing label on a later run.
        for pattern in ('walk_*.png', 'walk_*.psx', f'{name}.png', f'{name}.psx'):
            for old in out.glob(pattern):
                old.unlink()
        scenes = out / 'scene.txt'
        scenes.write_text(f'{name} map {m} {x} {y} {direction} 0x{initializers[m]:03X}\n', encoding='utf-8')
        cue = args.cue or ROOT / ('rom/Momotarou Matsuri - Ishikawa Rokuemon no Maki (Japan).cue' if args.original
                                  else 'build/momotarou-matsuri_en.cue')
        command = [sys.executable, '-X', 'utf8', str(Path(SKILL) / 'scripts/emu.py'), str(cue),
                   '--out', str(out), '--script', str(ROOT / 'tools/debug/warp.lua'),
                   '--script', str(ROOT / 'tools/lua/textlog.lua'), '--var', f"SCENE='{name}'",
                   '--var', f'SCENES=[[{scenes.resolve().as_posix()}]]', '--frames', '1', '--timeout', '120']
        if name.startswith('bath'):
            command += ['--script', str(ROOT / 'tools/debug/field_walk.lua'), '--var', 'HOLD=-1',
                        '--var', f'WALK_MAP={m}', '--var', "WALK={{'up',160}}"]
        else:
            command += ['--var', 'HOLD=300']
        result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
        (out / 'harness.log').write_text(result.stdout + result.stderr, encoding='utf-8')
        if result.returncode:
            return name, [('emulator', name, 'failed', '', '', '')]
    return name, check(out, key, args.original, ('walk_*.png', f'{name}.png', 'final.png'), weather=m == 237)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--original', action='store_true')
    ap.add_argument('--cue', type=Path, help='alternate built disc; --original still selects reference pixels')
    ap.add_argument('--check-only', action='store_true')
    ap.add_argument('--jobs', type=int, default=3)
    ap.add_argument('--only', nargs='+', choices=sorted(CASES), help='limit to these named routes')
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    initializers = gen_scenes.initializers()
    with ThreadPoolExecutor(args.jobs) as pool:
        results = list(pool.map(lambda name: run(name, args, initializers), args.only or CASES))
    rows = [(name, *r) for name, group in results for r in group]
    with (args.out / 'coverage.tsv').open('w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter='\t', lineterminator='\n')
        writer.writerow(('case', 'atlas', 'sign', 'status', 'screenshot', 'position', 'palette'))
        writer.writerows(rows)
    failed = [r for r in rows if r[3] != 'ok']
    print(f'{len(rows) - len(failed)}/{len(rows)} complete signs in {len(results)} cold map contexts')
    for row in failed:
        print(row)
    return bool(failed)


if __name__ == '__main__':
    raise SystemExit(main())
