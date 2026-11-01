"""Cold HUD word assembly and natural counter captures, original or English.

    python -X utf8 tools/debug/hud_units.py --out work/qa/hudunits8
    ... --original --out work/qa/hudunits8_jp
    ... --check-only --out work/qa/hudunits8

The assembly fixture substitutes loaded ANM item pointers only. Natural
contexts use the warp's controller input and read-only HUD probe. A match
proves the complete word and palette; visual review checks the neighbours.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
import gfx_hud  # noqa: E402
from skill import SKILL  # noqa: E402

CONTEXTS = {
    'm05': ('game_m05_07', [20]),
    'm14': ('game_m14_10', [20]),
    'm15': ('game_m15_11', [78]),
    'm19': ('game_m19_15', [34]),
    'm20': ('game_m20_16', [79]),
    'm22': ('game_m22_18', [78]),
    'm28': ('game_m28_1e', [79]),
    'm34': ('game_m34_22', [77]),
    'record': ('game_m15_11', [78]),
}


def run(name, args):
    out = args.out / name
    out.mkdir(parents=True, exist_ok=True)
    fixture = name == 'fixture'
    scene, items = ('game_m11_0d', list(gfx_hud.WORDS)) if fixture else CONTEXTS[name]
    base = [sys.executable, '-X', 'utf8']
    if not args.check_only:
        cue = ROOT / ('rom/Momotarou Matsuri - Ishikawa Rokuemon no Maki (Japan).cue'
                      if args.original else 'build/momotarou-matsuri_en.cue')
        command = base + [str(Path(SKILL) / 'scripts/emu.py'), str(cue), '--out', str(out),
                          '--script', str(ROOT / 'tools/debug/warp.lua'),
                          '--script', str(ROOT / 'tools/lua/textlog.lua'),
                          '--var', f"SCENE='{scene}'", '--frames', '900', '--timeout', '180']
        if fixture:
            config = f'ANNOUNCEMENT_SOURCE={{file=350,entry=2,items={{{",".join(map(str, items))}}}}}'
            command += ['--script', str(ROOT / 'tools/debug/announcements.lua'),
                        '--var', 'ANNOUNCEMENTS=true', '--var', config, '--var', 'HOLD=-1']
        else:
            command += ['--script', str(ROOT / 'tools/debug/hud.lua'),
                        '--var', 'HOLD=6000' if name == 'm05' else 'HOLD=2400',
                        '--shot-every', '120']
            if name == 'm19':
                command += ['--script', str(ROOT / 'tools/debug/ice.lua')]
            else:
                command += ['--var', 'CLICK=45']
            if name == 'record':
                command += ['--script', str(ROOT / 'tools/debug/hud_record.lua'), '--var', 'HUD_RECORD=9999']
        with (out / 'runner.txt').open('w', encoding='utf-8') as log:
            result = subprocess.run(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)
        if result.returncode:
            return name, f'emulator failed: {result.returncode}'
    command = base + [str(ROOT / 'tools/debug/announcements_qa.py'), str(out),
                      '--out', str(out / 'coverage'), '--entry', '2',
                      '--items', ','.join(map(str, items))]
    if args.original:
        command += ['--original']
    if not fixture:
        command += ['--scan', '--glob', 'f*.png']
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
    (out / 'coverage.txt').write_text(result.stdout + result.stderr, encoding='utf-8')
    if result.returncode:
        return name, f'coverage failed: {result.returncode}'
    if name in ('m15', 'record'):
        # The same item is drawn twice. A match on the left must not conceal
        # a clipped right-hand unit, as the first enlarged review discovered.
        command[command.index('--out') + 1] = str(out / 'right_coverage')
        command += ['--region', '264,16,32,32']
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
        (out / 'right_coverage.txt').write_text(result.stdout + result.stderr, encoding='utf-8')
        if result.returncode:
            return name, f'right unit missing: {result.returncode}'
    return name, 'ok'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--original', action='store_true')
    parser.add_argument('--check-only', action='store_true')
    parser.add_argument('--only', help='comma-separated fixture/context names')
    parser.add_argument('--jobs', type=int, choices=(1, 2, 3), default=3)
    args = parser.parse_args()
    cases = ['fixture', *CONTEXTS]
    wanted = args.only.split(',') if args.only else cases
    if not wanted or set(wanted) - set(cases):
        parser.error('unknown or empty case selection')
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        results = list(pool.map(lambda case: run(case, args), wanted))
    for name, status in results:
        print(name, status, sep='\t')
    (args.out / 'result.tsv').write_text(''.join(f'{n}\t{s}\n' for n, s in results), encoding='utf-8')
    return any(status != 'ok' for _, status in results)


if __name__ == '__main__':
    raise SystemExit(main())
