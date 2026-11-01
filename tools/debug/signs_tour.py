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
    'bath_board180': (180, 18, 16, 0, 'GV16000D.BIN:3'),
    'bath_board320a': (320, 16, 14, 0, 'GV36000D.BIN:0'),
    'bath_board320b': (320, 15, 47, 0, 'GV36000D.BIN:0'),
    'bath_board321a': (321, 16, 14, 0, 'GV36000D.BIN:0'),
    'bath_board321b': (321, 15, 47, 0, 'GV36000D.BIN:0'),
    'flowers99': (99, 20, 40, 0, 'GV06000D.BIN:0'),
    'flowers100': (100, 20, 40, 0, 'GV06000D.BIN:0'),
    'flowers237': (237, 70, 29, 0, 'GV22000D.BIN:0'),
    'flowers238': (238, 70, 29, 0, 'GV22000D.BIN:0'),
    'items143': (143, 24, 23, 0, 'GV12000D.BIN:0'),
    'items144': (144, 24, 23, 0, 'GV12002D.BIN:0'),
    'equipment45': (45, 34, 29, 0, 'GV01000D.BIN:0'),
    'produce45': (45, 38, 29, 0, 'GV01000D.BIN:0'),
    'produce80': (80, 21, 43, 0, 'GV04000D.BIN:0'),
    'produce81': (81, 21, 43, 0, 'GV04002D.BIN:0'),
    'produce99': (99, 20, 35, 0, 'GV06000D.BIN:0'),
    'produce100': (100, 20, 35, 0, 'GV06000D.BIN:0'),
    'produce143': (143, 32, 25, 0, 'GV12000D.BIN:0'),
    'produce144': (144, 32, 25, 0, 'GV12002D.BIN:0'),
    'produce163': (163, 20, 29, 0, 'GV13000D.BIN:0'),
    'produce285': (285, 29, 26, 0, 'GV30002D.BIN:0'),
    'produce286': (286, 29, 26, 0, 'GV30000D.BIN:0'),
    'fish126': (126, 30, 46, 0, 'GV09000D.BIN:0'),
    'fish237': (237, 32, 29, 0, 'GV22000D.BIN:0'),
    'fish238': (238, 32, 29, 0, 'GV22000D.BIN:0'),
    'fish207': (207, 28, 41, 0, 'GV20000D.BIN:0'),
    'games59a': (59, 22, 98, 0, 'GV02000D.BIN:2'),
    'games59b': (59, 38, 98, 0, 'GV02000D.BIN:2'),
    'games80': (80, 23, 27, 0, 'GV04000D.BIN:0'),
    'games81': (81, 23, 27, 0, 'GV04002D.BIN:0'),
    'games126': (126, 57, 28, 0, 'GV09000D.BIN:3'),
    'games223': (223, 21, 30, 0, 'GV21000D.BIN:0'),
    'games263a': (263, 27, 49, 0, 'GV23000D.BIN:2'),
    'games263b': (263, 60, 49, 0, 'GV23000D.BIN:2'),
    'games320': (320, 54, 27, 0, 'GV36000D.BIN:0'),
    'games321': (321, 54, 27, 0, 'GV36000D.BIN:0'),
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
    'inn45': (45, 20, 36, 0, 'GV01000D.BIN:0'),
    'inn59': (59, 37, 123, 0, 'GV02000D.BIN:0'),
    'inn99': (99, 48, 58, 0, 'GV06000D.BIN:0'),
    'inn100': (100, 48, 58, 0, 'GV06000D.BIN:0'),
    'inn114': (114, 32, 61, 0, 'GV08000D.BIN:0'),
    'inn80': (80, 47, 43, 0, 'GV04000D.BIN:0'),
    'inn81': (81, 47, 43, 0, 'GV04002D.BIN:0'),
    'inn126': (126, 39, 57, 0, 'GV09000D.BIN:0'),
    'inn143a': (143, 16, 33, 0, 'GV12000D.BIN:0'),
    'inn143b': (143, 116, 33, 0, 'GV12000D.BIN:0'),
    'inn144a': (144, 16, 33, 0, 'GV12002D.BIN:0'),
    'inn144b': (144, 116, 33, 0, 'GV12002D.BIN:0'),
    'inn163': (163, 45, 52, 0, 'GV13000D.BIN:0'),
    'inn180': (180, 80, 84, 0, 'GV16000D.BIN:0'),
    'inn223': (223, 31, 48, 0, 'GV21000D.BIN:0'),
    'inn237': (237, 20, 36, 0, 'GV22000D.BIN:0'),
    'inn238': (238, 20, 36, 0, 'GV22000D.BIN:0'),
    'inn263': (263, 48, 56, 0, 'GV23000D.BIN:0'),
    'inn285': (285, 40, 34, 0, 'GV30002D.BIN:0'),
    'inn286': (286, 40, 34, 0, 'GV30000D.BIN:0'),
    'inn295': (295, 34, 18, 0, 'GV32000D.BIN:0'),
    'inn306': (306, 46, 41, 0, 'GV34000D.BIN:0'),
    'inn320': (320, 33, 41, 0, 'GV36000D.BIN:0'),
    'inn321': (321, 33, 41, 0, 'GV36000D.BIN:0'),
    'inn207': (207, 16, 21, 0, 'GV20000D.BIN:0'),
    'inn335': (335, 25, 32, 0, 'GV38000D.BIN:0'),
    'tea45': (45, 45, 29, 0, 'GV01000D.BIN:0'),
    'tea59': (59, 35, 117, 0, 'GV02000D.BIN:0'),
    'tea80': (80, 30, 43, 0, 'GV04000D.BIN:0'),
    'tea81': (81, 30, 43, 0, 'GV04002D.BIN:0'),
    'tea99': (99, 63, 37, 0, 'GV06000D.BIN:0'),
    'tea100': (100, 63, 37, 0, 'GV06000D.BIN:0'),
    'tea114': (114, 13, 61, 0, 'GV08000D.BIN:0'),
    'tea126': (126, 53, 38, 0, 'GV09000D.BIN:0'),
    'tea143a': (143, 23, 33, 0, 'GV12000D.BIN:0'),
    'tea143b': (143, 96, 33, 0, 'GV12000D.BIN:0'),
    'tea144a': (144, 23, 33, 0, 'GV12002D.BIN:0'),
    'tea144b': (144, 96, 33, 0, 'GV12002D.BIN:0'),
    'tea163': (163, 26, 35, 0, 'GV13000D.BIN:0'),
    'tea180': (180, 93, 50, 0, 'GV16000D.BIN:0'),
    'tea207': (207, 23, 35, 0, 'GV20000D.BIN:0'),
    'tea223': (223, 51, 48, 0, 'GV21000D.BIN:0'),
    'tea237': (237, 20, 29, 0, 'GV22000D.BIN:0'),
    'tea238': (238, 20, 29, 0, 'GV22000D.BIN:0'),
    'tea263': (263, 43, 49, 0, 'GV23000D.BIN:0'),
    'tea285': (285, 28, 34, 0, 'GV30002D.BIN:0'),
    'tea286': (286, 28, 34, 0, 'GV30000D.BIN:0'),
    'tea295': (295, 26, 26, 0, 'GV32000D.BIN:0'),
    'tea306': (306, 57, 34, 0, 'GV34000D.BIN:0'),
    'tea320': (320, 14, 41, 0, 'GV36000D.BIN:0'),
    'tea321': (321, 14, 41, 0, 'GV36000D.BIN:0'),
    'tea335': (335, 36, 32, 0, 'GV38000D.BIN:0'),
    'bank45': (45, 19, 29, 0, 'GV01000D.BIN:0'),
    'bank59': (59, 22, 123, 0, 'GV02000D.BIN:0'),
    'bank80': (80, 20, 19, 0, 'GV04000D.BIN:0'),
    'bank81': (81, 20, 19, 0, 'GV04002D.BIN:0'),
    'bank99': (99, 17, 21, 0, 'GV06000D.BIN:0'),
    'bank100': (100, 17, 21, 0, 'GV06000D.BIN:0'),
    'bank114': (114, 20, 61, 0, 'GV08000D.BIN:0'),
    'bank126': (126, 38, 41, 0, 'GV09000D.BIN:0'),
    'bank143a': (143, 17, 25, 0, 'GV12000D.BIN:0'),
    'bank143b': (143, 106, 25, 0, 'GV12000D.BIN:0'),
    'bank144a': (144, 17, 25, 0, 'GV12002D.BIN:0'),
    'bank144b': (144, 106, 25, 0, 'GV12002D.BIN:0'),
    'bank163': (163, 30, 23, 0, 'GV13000D.BIN:0'),
    'bank180': (180, 80, 71, 0, 'GV16000D.BIN:0'),
    'bank207': (207, 18, 41, 0, 'GV20000D.BIN:0'),
    'bank223': (223, 16, 48, 0, 'GV21000D.BIN:0'),
    'bank237': (237, 23, 43, 0, 'GV22000D.BIN:0'),
    'bank238': (238, 23, 43, 0, 'GV22000D.BIN:0'),
    'bank263': (263, 18, 49, 0, 'GV23000D.BIN:0'),
    'bank306': (306, 19, 34, 0, 'GV34000D.BIN:0'),
    'bank320': (320, 22, 27, 0, 'GV36000D.BIN:0'),
    'bank321': (321, 22, 27, 0, 'GV36000D.BIN:0'),
}
# These atlases also retain another Inn tile beneath/outside the visible
# map layer. These routes approve only the displayed layer's complete label.
CASE_LABELS = {'inn80': ('inn2',), 'inn163': ('inn2',), 'inn99': ('inn',),
               **{name: ('bath',) for name in CASES if name.startswith('bath_board')},
               'inn100': ('inn',), 'inn295': ('inn',), 'inn335': ('inn2',),
               'equipment45': ('weapons', 'armor', 'shoes'),
               'flowers99': ('flowers',), 'flowers100': ('flowers',),
               'flowers237': ('flowers',), 'flowers238': ('flowers',),
               'items143': ('items',), 'items144': ('items',)}


def run(name, args, initializers):
    m, x, y, direction, key = CASES[name]
    out = args.out / name
    out.mkdir(parents=True, exist_ok=True)
    if not args.check_only:
        # emu.py clears numbered frames but keeps custom Lua screenshot names.
        # Delete only this harness's captures, so an old successful walk cannot
        # supply a missing label on a later run.
        for pattern in ('walk_*.png', 'walk_*.psx', 'walk_*.vram.bin', f'{name}.png', f'{name}.psx'):
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
        if name in ('produce99', 'produce100', 'flowers99', 'flowers100'):
            # GSV0600D:1 +0x3F6 checks flags 0x6F/0x90 before dispatching
            # Dog's forced-entry event. Native 2B writes exactly these two
            # two-bit flags; the full initializer still loads all map actors.
            # This is a graphics fixture, not proof of natural story progress.
            command += ['--var', 'OPS={0x2B,0x6F,0,0x2B,0x90,3}']
        if name == 'flowers237':
            command += ['--script', str(ROOT / 'tools/debug/field_walk.lua'), '--var', 'HOLD=-1',
                        '--var', f'WALK_MAP={m}', '--var', "WALK={{'-',360}}",
                        '--var', 'WALK_VRAM=true', '--var', 'WALK_EVERY=6']
        elif name in ('bath189', 'bath332', 'bath333'):
            command += ['--script', str(ROOT / 'tools/debug/field_walk.lua'), '--var', 'HOLD=-1',
                        '--var', f'WALK_MAP={m}', '--var', "WALK={{'up',160}}"]
        else:
            command += ['--var', 'HOLD=300']
        result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
        (out / 'harness.log').write_text(result.stdout + result.stderr, encoding='utf-8')
        if result.returncode:
            return name, [('emulator', name, 'failed', '', '', '')]
    return name, check(out, key, args.original, ('walk_*.png', f'{name}.png', 'final.png'),
                       weather=m == 237, labels=CASE_LABELS.get(
                           name, ('inn',) if name.startswith('inn') else
                           ('tea',) if name.startswith('tea') else
                           ('bank',) if name.startswith('bank') else
                           ('produce',) if name.startswith('produce') else
                           ('fish',) if name.startswith('fish') else
                           ('games',) if name.startswith('games') else None))


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
