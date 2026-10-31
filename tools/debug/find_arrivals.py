"""Find a working arrival point for map scenes that hang or never load (warp_all result.tsv 'fail' rows).

usage: python -X utf8 tools/debug/find_arrivals.py [--result work/qa/warp_all/result.tsv] [--jobs 8]
Tries every 0x1D destination the scripts use for that map (commonest first), then the failed point shifted by
+-1..2 tiles, each from a cold boot, and prints `M: (x, y, dir)` lines to paste into OVERRIDE in gen_scenes.py.
"""
import argparse, concurrent.futures as cf, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
sys.path.insert(0, os.path.join(ROOT, 'tools'))
sys.path.insert(0, HERE)
from skill import SKILL
import gen_scenes
from warp_all import ORIG

OUT = os.path.join(ROOT, 'work', 'qa', 'arrivals')


def attempt(m, pos):
    name = f'm{m}_{pos[0]}_{pos[1]}_{pos[2]}'
    lst = os.path.join(OUT, name + '.txt')
    open(lst, 'w').write(f'{name} map {m} {pos[0]} {pos[1]} {pos[2]}\n')
    d = os.path.join(OUT, name)
    p = subprocess.run([sys.executable, '-X', 'utf8', os.path.join(SKILL, 'scripts', 'emu.py'), ORIG, '--out', d,
                        '--script', os.path.join(HERE, 'warp.lua'), '--var', f"SCENE='{name}'",
                        '--var', f'SCENES=[[{os.path.abspath(lst)}]]', '--var', 'HOLD=300',
                        '--frames', '1', '--timeout', '90'], capture_output=True, text=True)
    return p.returncode == 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--result', default=os.path.join(ROOT, 'work', 'qa', 'warp_all', 'result.tsv'))
    ap.add_argument('--jobs', type=int, default=8)
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    failed = [int(re.search(r'_(\d+)$', l.split('\t')[0]).group(1)) for l in open(a.result, encoding='utf-8')
              if l.startswith('map_') and '\tfail' in l]
    arr = gen_scenes.arrivals()
    found = {}
    for m in failed:
        cands = [p for p, _ in arr[m].most_common()]
        x, y, dr = cands[0]
        cands += [(x + dx, y + dy, dr) for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0), (0, 2), (0, -2), (2, 0),
                                                     (-2, 0), (1, 1), (-1, -1))]
        for i in range(1, len(cands), a.jobs):  # cands[0] is the one that failed
            batch = cands[i:i + a.jobs]
            with cf.ThreadPoolExecutor(a.jobs) as ex:
                ok = list(ex.map(lambda p: attempt(m, p), batch))
            if any(ok):
                found[m] = batch[ok.index(True)]
                break
        print(f'    {m}: {found.get(m)},', flush=True)
    return 0 if len(found) == len(failed) else 1


if __name__ == '__main__':
    sys.exit(main())
