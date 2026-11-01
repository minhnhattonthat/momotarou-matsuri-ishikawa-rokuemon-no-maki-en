"""Make original/English card comparisons using the shared sheet tool.

    python -X utf8 tools/debug/card_art_review.py --out DIR [--run COLD_RUN]
    python -X utf8 tools/debug/card_art_review.py --out DIR --grid 89 90

Grid output is a diagnostic overlay, never a game asset or QA screenshot.
"""
import argparse
import importlib.util
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import gen_gfx  # noqa: E402
import gfx  # noqa: E402
import gfx_card_art  # noqa: E402
import gfx_card_props  # noqa: E402
from skill import SKILL  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--run', type=Path)
    ap.add_argument('--grid', type=int, nargs='+')
    ap.add_argument('--cards', type=int, nargs='+', help='review these cards instead of sound-effect cards')
    ap.add_argument('--props', action='store_true', help='enlarge each sign or emblem, with its immediate border')
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    spec = importlib.util.spec_from_file_location('card_sheet', Path(SKILL) / 'scripts/sheet.py')
    sheet = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sheet)
    cards = args.grid or args.cards or sorted(gfx_card_props.PROPS if args.props else
                                             {row['card'] for row in gfx_card_art.rows()})
    pairs = []
    for card in cards:
        i = card - 1
        _, original = gen_gfx.original(f'HCARD{i // 10}0D.BIN:{i % 10}')
        source = args.out / f'original_{card:03d}.png'
        original.crop((0, 0, 208, 128)).save(source)
        if args.grid:
            # Grid coordinates are annotated at fourfold scale so numbers do
            # not obscure the source pixels needed for precise mask selection.
            grid = original.crop((0, 0, 208, 128)).resize((832, 512), Image.Resampling.NEAREST)
            draw = ImageDraw.Draw(grid)
            for x in range(0, 208, 10):
                draw.line((x * 4, 0, x * 4, 512), fill=(255, 0, 128, 100))
                draw.text((x * 4, 0), str(x), fill='black', stroke_width=1, stroke_fill='white')
            for y in range(10, 128, 10):
                draw.line((0, y * 4, 832, y * 4), fill=(255, 0, 128, 100))
                draw.text((0, y * 4), str(y), fill='black', stroke_width=1, stroke_fill='white')
            grid.save(args.out / f'grid_{card:03d}.png')
            continue
        translated = args.out / f'english_{card:03d}.png'
        if args.run:
            sheet.make([str(args.run / f'card_{card:03d}.png')], out=str(translated),
                       box=(56, 56, 208, 128), scale=1, div=1)
        else:
            with Image.open(gfx.EN / f'HCARD{i // 10}0D_{i % 10}.png') as image:
                image.crop((0, 0, 208, 128)).save(translated)
        if args.props:
            for name, _, polygon, _, _, _, rect, _, _ in gfx_card_props.PROPS.get(card, []):
                xs, ys = zip(*polygon)
                box = (max(0, min(min(xs), rect[0]) - 3), max(0, min(min(ys), rect[1]) - 3),
                       min(208, max(max(xs) + 1, rect[2]) + 3), min(128, max(max(ys) + 1, rect[3]) + 3))
                for label, path in [('jp', source), ('en', translated)]:
                    with Image.open(path) as im:
                        output = args.out / f'{card:03d}_{name}_{label}.png'
                        im.crop(box).save(output)
                        pairs.append(str(output))
        else:
            pairs.extend([str(source), str(translated)])
    if pairs:
        sheet.make(pairs, out=str(args.out / 'compare_sheet.png'), cols=2,
                   div=1, scale=6 if args.props else 3, limit=14 if args.props else 10)


if __name__ == '__main__':
    main()
