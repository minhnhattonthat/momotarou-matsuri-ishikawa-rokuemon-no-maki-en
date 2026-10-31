"""Warp to every scene of tools/debug/scenes.txt from a cold boot, in parallel; one proof shot per scene.

usage: python -X utf8 tools/debug/warp_all.py [CUE] [--out work/qa/warp_all] [--jobs 8] [--only REGEX]
                                              [--hold FRAMES --click N --every N]   (text tour: click through)
Writes OUT/<scene>/ (emu.py run), OUT/shots/<scene>.png (the arrival shot) and OUT/result.tsv
(scene, status, arrival frame); status is ok, flat (single-colour shot) or the emu.py failure. Exit 1 if any scene
is not ok. Then: sheet.py OUT/shots for a contact sheet.
"""
import argparse, concurrent.futures as cf, os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from skill import SKILL
from PIL import Image

ORIG = os.path.join(ROOT, 'rom', 'Momotarou Matsuri - Ishikawa Rokuemon no Maki (Japan).cue')


def scenes():
    out = []
    for line in open(os.path.join(HERE, 'scenes.txt'), encoding='utf-8'):
        w = line.split('#')[0].split()
        if len(w) >= 2:
            out.append(w[0])
    return out


def run(cue, out, name, hold=None, click=None, every=None, probes=()):
    d = os.path.join(out, name)
    shutil.rmtree(d, ignore_errors=True)
    extra = (['--var', f'HOLD={hold}'] if hold else []) + (['--var', f'CLICK={click}'] if click else []) + \
        (['--shot-every', str(every)] if every else []) + [x for p in probes for x in ('--script', os.path.abspath(p))]
    p = subprocess.run([sys.executable, '-X', 'utf8', os.path.join(SKILL, 'scripts', 'emu.py'), cue, '--out', d,
                        '--script', os.path.join(HERE, 'warp.lua'), '--var', f"SCENE='{name}'",
                        '--var', f"SCENES=[[{os.path.abspath(os.path.join(HERE, 'scenes.txt'))}]]",
                        '--frames', '1', '--timeout', str(240 + (hold or 0) // 20)] + extra,
                       capture_output=True, text=True)
    log = open(os.path.join(d, 'log.txt'), encoding='utf-8', errors='replace').read() if os.path.exists(
        os.path.join(d, 'log.txt')) else ''
    m = re.search(r'ARRIVED \S+ f(\d+)', log)
    shot = os.path.join(d, name + '.png')
    if p.returncode or not m or not os.path.exists(shot):
        err = os.path.join(d, 'lua_error.txt')
        why = open(err).read().strip() if os.path.exists(err) else f'exit {p.returncode}'
        return name, 'fail: ' + why.replace('\t', ' ').replace('\n', ' '), ''
    shutil.copy(shot, os.path.join(out, 'shots', name + '.png'))
    lo_hi = Image.open(shot).convert('L').getextrema()
    return name, 'ok' if lo_hi[1] - lo_hi[0] > 16 else 'flat', m.group(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cue', nargs='?', default=ORIG)
    ap.add_argument('--out', default=os.path.join(ROOT, 'work', 'qa', 'warp_all'))
    ap.add_argument('--jobs', type=int, default=8)
    ap.add_argument('--only', default='')
    ap.add_argument('--hold', type=int, help='frames to keep running after arrival (warp.lua HOLD)')
    ap.add_argument('--click', type=int, help='press circle every N frames after arrival (warp.lua CLICK)')
    ap.add_argument('--every', type=int, help='also shoot every N frames (OUT/<scene>/f*.png)')
    ap.add_argument('--probe', action='append', default=[], help='extra Lua script, e.g. tools/lua/textlog.lua')
    a = ap.parse_args()
    os.makedirs(os.path.join(a.out, 'shots'), exist_ok=True)
    todo = [s for s in scenes() if re.search(a.only, s)]
    with cf.ThreadPoolExecutor(a.jobs) as ex:
        res = list(ex.map(lambda s: run(a.cue, a.out, s, a.hold, a.click, a.every, a.probe), todo))
    with open(os.path.join(a.out, 'result.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        for r in res:
            f.write('\t'.join(r) + '\n')
    bad = [r for r in res if r[1] != 'ok']
    for r in bad:
        print(*r, sep='\t')
    print(f'{len(res) - len(bad)}/{len(res)} scenes ok')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
