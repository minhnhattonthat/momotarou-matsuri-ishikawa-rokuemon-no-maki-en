"""Compare the exact original/English captures that passed the field-sign oracle.

    python tools/debug/field_signs_review.py EN_RUN JP_RUN --out DIR

Produces full context and lettering close-ups. Never writes visual verdicts.
"""
import argparse
import ast
import csv
import importlib.util
from pathlib import Path
import sys

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import gfx_signs  # noqa: E402
from skill import SKILL  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('english', type=Path)
    parser.add_argument('original', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    spec = importlib.util.spec_from_file_location('sign_sheet', Path(SKILL) / 'scripts/sheet.py')
    sheet = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sheet)
    runs = []
    for run in (args.english, args.original):
        with (run / 'coverage.tsv').open(encoding='utf-8', newline='') as stream:
            rows = list(csv.DictReader(stream, delimiter='\t'))
        assert rows and all(row['status'] == 'ok' for row in rows), run
        runs.append({(row['case'], row['atlas'], row['sign']): row for row in rows})
    assert runs[0].keys() == runs[1].keys(), 'coverage sets differ'
    for key in runs[0]:
        name, atlas, label = key
        pair = [run[key] for run in runs]
        sheet.make([row['screenshot'] for row in pair], out=str(args.out / f'{name}_{label}_context_sheet.png'),
                   cols=2, div=1, scale=2)
        rect = next(sign[2] for sign in gfx_signs.SIGNS[atlas] if sign[0] == label)
        width, height = rect[2] - rect[0], rect[3] - rect[1]
        crops = []
        for language, row in zip(('en', 'jp'), pair):
            x, y = ast.literal_eval(row['position'])
            crop = args.out / f'{name}_{label}_{language}_crop.png'
            with Image.open(row['screenshot']) as im:
                im.crop((max(0, x - 8), max(0, y - 8), min(im.width, x + width + 8),
                         min(im.height, y + height + 8))).save(crop)
            crops.append(str(crop))
        sheet.make(crops, out=str(args.out / f'{name}_{label}_detail_sheet.png'), cols=2, div=1, scale=6)


if __name__ == '__main__':
    main()
