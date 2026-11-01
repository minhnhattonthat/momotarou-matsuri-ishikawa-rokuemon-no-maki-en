"""Make arrival/final contact sheets for a cold scene sweep.

    python tools/debug/tour_review.py RUN --out DIR

Each row pairs a scene's arrival and final capture. These sheets cover those
two moments only: they do not replace dialogue-frame or interactive QA. Groups
with unfinished runs are skipped, so this can inspect a tour still running.
--fallback RUN uses a separately recorded retry only for missing pairs and
records its source directory in scenes.tsv; original failure logs stay intact.
"""
import argparse
import csv
import importlib.util
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from skill import SKILL  # noqa: E402
from warp_all import scenes  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--fallback', type=Path)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    spec = importlib.util.spec_from_file_location('tour_sheet', Path(SKILL) / 'scripts/sheet.py')
    sheet = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sheet)
    names = scenes()
    rows = []
    sources, missing = {}, []
    for name in names:
        for run in (args.run, args.fallback):
            if run and all((run / name / image).exists() for image in (f'{name}.png', 'final.png')):
                sources[name] = run
                break
        else:
            missing.append(name)
    for start in range(0, len(names), 6):
        group = names[start:start + 6]
        if any(name not in sources for name in group):
            continue
        paths = [sources[name] / name / image for name in group for image in (f'{name}.png', 'final.png')]
        output = args.out / f'arrival_final_sheet_{start // 6:03d}.png'
        if not output.exists() or any(path.stat().st_mtime > output.stat().st_mtime for path in paths):
            sheet.make(list(map(str, paths)), out=str(output), cols=2, div=1, scale=1, limit=12)
        rows.extend((output.name, row + 1, name, str(sources[name])) for row, name in enumerate(group))
    with (args.out / 'scenes.tsv').open('w', encoding='utf-8', newline='') as stream:
        writer = csv.writer(stream, delimiter='\t', lineterminator='\n')
        writer.writerow(('sheet', 'row', 'scene', 'run'))
        writer.writerows(rows)
    print(f'{len(rows)}/{len(names)} complete arrival/final pairs')
    print(f'Missing pairs: {missing}')


if __name__ == '__main__':
    main()
