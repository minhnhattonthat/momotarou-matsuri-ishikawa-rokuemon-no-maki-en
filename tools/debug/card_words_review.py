"""Make scoped marginal-caption review sheets from the 100-card cold tour.

    python -X utf8 tools/debug/card_words_review.py RUN --out DIR

Uses the skill's sheet.py for all cropping/rotation/zoom. These sheets cover
only the marginal English phrases, never the unlocalized illustration SFX.
Run cards_qa.py separately to verify each complete card against the built TIM.
"""
import argparse
import importlib.util
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import gen_card_words  # noqa: E402
from skill import SKILL  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('run', type=Path)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    spec = importlib.util.spec_from_file_location('card_review_sheet', Path(SKILL) / 'scripts' / 'sheet.py')
    sheet = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sheet)
    crops = args.out / 'crops'
    crops.mkdir(parents=True, exist_ok=True)
    for row in gen_card_words.rows():
        card = row['card']
        source = args.run / f'card_{card:03d}.png'
        if not source.exists():
            raise FileNotFoundError(source)
        rect = (56 + row['x0'], 56 + row['y0'], row['x1'] - row['x0'], row['y1'] - row['y0'])
        sheet.make([str(source)], out=str(crops / f'card_{card:03d}.png'), box=rect, scale=3, turn=270)
    sheet.make([str(crops / 'card_*.png')], out=str(args.out / 'phrases_sheet.png'),
               cols=4, div=1, limit=20)


if __name__ == '__main__':
    main()
