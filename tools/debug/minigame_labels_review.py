"""Make scoped zoomed sheets from complete-sprite coverage, never from exit codes.

    python -X utf8 tools/debug/minigame_labels_review.py RUN --out REVIEW

The sheets are review inputs. This tool never creates visual verdicts.
"""
import argparse
import ast
import csv
from pathlib import Path
import subprocess
import sys

from PIL import Image

from minigame_labels import CASES, ROOT
from skill import SKILL


def sheet(paths, out, *options):
    subprocess.run([sys.executable, '-X', 'utf8', str(Path(SKILL) / 'scripts/sheet.py'),
                    *map(str, paths), '--out', str(out), *options], cwd=ROOT, check=True,
                   stdout=subprocess.DEVNULL)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    crops = args.out / 'crops'
    crops.mkdir(parents=True, exist_ok=True)
    groups, context = {'labels': [], 'racers': []}, []
    for name, _, _, _, _, _, items, _ in CASES:
        run = args.run / name
        with (run / 'coverage/coverage.tsv').open(encoding='utf-8', newline='') as source:
            coverage = list(csv.DictReader(source, delimiter='\t'))
        if [int(row['item']) for row in coverage] != items or any(row['status'] != 'ok' for row in coverage):
            raise ValueError(f'{name}: incomplete sprite coverage')
        for index, row in enumerate(coverage):
            x, y = ast.literal_eval(row['position'])
            with Image.open(run / 'coverage/templates' / f'{index:03d}.png') as template:
                w, h = template.size
            crop = crops / f'{name}_{int(row["item"]):02d}.png'
            sheet([row['frame']], crop, '--crop', f'{max(0, x-2)},{max(0, y-2)},{w+4},{h+4}', '--zoom', '4')
            groups['racers' if name == 'racers' else 'labels'].append(crop)
        context.append(coverage[0]['frame'])
    for group, paths in groups.items():
        sheet(paths, args.out / f'{group}_sheet.png', '--div', '1', '--cols', '4', '--max', '12')
    sheet(context, args.out / 'context_sheet.png', '--zoom', '2', '--cols', '2', '--max', '4')
    print('18 label states and 30 runner names; zoomed sheets plus nine context frames')


if __name__ == '__main__':
    main()
