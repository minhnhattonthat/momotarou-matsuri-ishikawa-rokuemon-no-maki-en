"""Cold captures and full-sprite coverage for minigame labels and race names.

    python -X utf8 tools/debug/minigame_labels.py --out work/qa/labels8
    ... --original --out work/qa/labels8_jp
    ... --check-only --out work/qa/labels8

The race title/distance label use their natural screen; runner names and small
race units cycle through the real runner list. Other cases substitute loaded
ANM pointers through sprite_fixture.lua or announcements.lua. These fixtures
prove assembly and palettes, not natural outcomes; they edit no disc data,
texture, palette or ANM geometry.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from skill import SKILL  # noqa: E402

# name, scene, mode, data file id, target ANM, source ANM, source items, texture
CASES = [
    ('m05', 'game_m05_07', 7, 298, 9, 18, [0], 2),
    ('m06', 'game_m06_08', 8, 299, -1, 8, list(range(32, 39)), 2),
    ('m08', 'game_m08_0a', 10, 301, -2, 14, [0], 6),
    ('m18', 'game_m18_14', 20, 311, 13, 9, [14], 3),
    ('m23', 'game_m23_19', 25, 317, None, 10, [7], 0),
    ('m50', 'game_m50_2e', 46, 339, 1, 2, [3], 0),
    ('racers', 'game_m23_19', 25, 317, 21, 21, list(range(30)), 3),
    ('race_hud', 'game_m23_19', 25, 350, None, 2, [43], 0),
    ('race_units', 'game_m23_19', 25, 317, 21, 20, list(range(5)), 3),
]


def run(case, args):
    name, scene, mode, file, target, source, items, texture = case
    out = args.out / name
    out.mkdir(parents=True, exist_ok=True)
    base = [sys.executable, '-X', 'utf8']
    if not args.check_only:
        cue = ROOT / ('rom/Momotarou Matsuri - Ishikawa Rokuemon no Maki (Japan).cue'
                      if args.original else 'build/momotarou-matsuri_en.cue')
        command = base + [str(Path(SKILL) / 'scripts/emu.py'), str(cue), '--out', str(out),
                          '--script', str(ROOT / 'tools/debug/warp.lua'),
                          '--script', str(ROOT / 'tools/lua/textlog.lua'),
                          '--var', f"SCENE='{scene}'", '--frames', '900', '--timeout', '180']
        if target is None:
            command += ['--var', 'HOLD=2000', '--var', 'CLICK=45']
        elif target < 0:
            config = f'ANNOUNCEMENT_SOURCE={{file={file},entry={source},items={{{",".join(map(str, items))}}}}}'
            command += ['--script', str(ROOT / 'tools/debug/announcements.lua'),
                        '--var', 'ANNOUNCEMENTS=true', '--var', f'ANNOUNCEMENT_MODE={mode}',
                        '--var', config]
            if target == -1:
                command += ['--var', 'HOLD=-1']
            else:
                command += ['--var', 'ANNOUNCEMENT_TRIGGER=13', '--var', 'HOLD=1600', '--shot-every', '15']
        else:
            config = (f'SPRITE_FIXTURE={{mode={mode},file={file},target={target},source={source},'
                      f'items={{{",".join(map(str, items))}}}}}')
            command += ['--script', str(ROOT / 'tools/debug/sprite_fixture.lua'),
                        '--var', config, '--var', 'HOLD=-1']
            if name in ('racers', 'race_units'):
                command += ['--var', 'CLICK=45']
        with (out / 'runner.txt').open('w', encoding='utf-8') as log:
            result = subprocess.run(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)
        if result.returncode:
            return name, f'emulator failed: {result.returncode}'
    command = base + [str(ROOT / 'tools/debug/announcements_qa.py'), str(out),
                      '--out', str(out / 'coverage'),
                      '--file', {'racers': 'M230D.BIN', 'race_hud': 'M990D.BIN', 'race_units': 'M230D.BIN'}
                      .get(name, name.upper() + '0D.BIN'),
                      '--entry', str(source), '--items', ','.join(map(str, items)),
                      '--textures', str(texture)]
    if args.original:
        command += ['--original']
    if name == 'race_units':
        # A one-pixel rank dot would otherwise match unrelated panel corners.
        # All five unit fixtures occupy the first runner row, after its digit.
        command += ['--region', '82,100,100,16']
    if target is None:
        command += ['--scan', '--glob', 'final.png']
    elif target == -2:
        command += ['--scan', '--glob', 'f003*.png']
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
    (out / 'coverage.txt').write_text(result.stdout + result.stderr, encoding='utf-8')
    return name, 'ok' if result.returncode == 0 else f'coverage failed: {result.returncode}'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--original', action='store_true')
    parser.add_argument('--check-only', action='store_true')
    parser.add_argument('--only', help='comma-separated case names')
    parser.add_argument('--jobs', type=int, choices=(1, 2, 3), default=3)
    args = parser.parse_args()
    cases = [case for case in CASES if not args.only or case[0] in args.only.split(',')]
    if not cases or (args.only and set(args.only.split(',')) - {c[0] for c in CASES}):
        parser.error('unknown or empty case selection')
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        results = list(pool.map(lambda case: run(case, args), cases))
    for name, status in results:
        print(name, status, sep='\t')
    (args.out / 'result.tsv').write_text(''.join(f'{n}\t{s}\n' for n, s in results), encoding='utf-8')
    return any(status != 'ok' for _, status in results)


if __name__ == '__main__':
    raise SystemExit(main())
