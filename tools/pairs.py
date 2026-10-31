"""Reviewer pairs files (docs/reviewer-brief.md): `>> id | JP` / `EN` for every unit of the named batches, with
the +-2 neighbouring rows of its script file as context.

    python -X utf8 tools/pairs.py OUT_DIR --group N      one file per N consecutive batches: OUT_DIR/gNN.txt
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TL = ROOT / 'work' / 'tl'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out')
    ap.add_argument('--group', type=int, default=6)
    a = ap.parse_args()
    rows, where = {}, {}
    for p in sorted((ROOT / 'script').glob('*.json')):
        rs = json.loads(p.read_text(encoding='utf-8'))
        for k, r in enumerate(rs):
            rows[r['id']] = r
            where[r['id']] = (rs, k)
    names = sorted(p.name[:4] for p in TL.glob('b[0-9][0-9][0-9].tsv'))
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for g in range(0, len(names), a.group):
        lines = []
        for b in names[g:g + a.group]:
            lines.append(f'### batch {b}')
            for ln in (TL / f'{b}.tsv').read_text(encoding='utf-8').splitlines():
                i = ln.split('\t')[0]
                if i not in where:
                    continue
                rs, k = where[i]
                ctx = [x for x in rs[max(0, k - 2):k + 3]]
                for x in ctx:
                    mark = '>>' if x['id'] == i else '  '
                    lines.append(f"{mark} {x['id']} | {x['jp']}")
                    if mark == '>>':
                        lines.append(f"   EN: {x.get('en', '')}")
                lines.append('')
        (out / f'g{g // a.group + 1:02d}.txt').write_text('\n'.join(lines), encoding='utf-8')
    print(len(names), 'batches ->', (len(names) + a.group - 1) // a.group, 'files in', out)


if __name__ == '__main__':
    sys.exit(main())
