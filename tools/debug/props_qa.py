"""Find complete flag, sushi-price and private-bath lettering in cold captures.

    python tools/debug/props_qa.py RUN --key M440D.BIN:0 --out DIR [--original]

All palettes are searched. The report names the matched frame, position and
palette; visual review remains required, including the erased egg-label tail
across M440D's atlas seam. Original captures use the English layout's bounds
and establish a comparison, not coverage of the entire Japanese text.
"""
import argparse
import csv
from pathlib import Path
import sys

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import gen_gfx  # noqa: E402
import gfx  # noqa: E402
import gfx_props  # noqa: E402
import tim  # noqa: E402
from announcements_qa import match  # noqa: E402


def check(run, key, original=False, pattern='f[0-9]*.png'):
    texture, _ = gen_gfx.original(key)
    if not original:
        name, entry = key.split(':')
        texture = gfx.redraw(texture, gfx.EN / f'{Path(name).stem}_{entry}.png')
    count = tim.parse(texture)[2][3]
    templates = [[tim.image(texture, pal).crop(rect) for pal in range(count)]
                 for rect, _, _, _ in gfx_props.PROPS[key]]
    found = {}
    # Read each image once, and stop searching labels already proved complete.
    for path in sorted(run.glob(pattern)):
        with Image.open(path) as image:
            screen = image.convert('RGB')
        for index, variants in enumerate(templates):
            if index in found:
                continue
            for pal, template in enumerate(variants):
                if template.width > screen.width or template.height > screen.height:
                    continue
                position = match(screen, template)
                if position is not None:
                    found[index] = (str(path), position, pal)
                    break
        if len(found) == len(templates):
            break
    return [(key, '/'.join(lines) or 'erased egg seam',
             'ok' if i in found else 'missing', *found.get(i, ('', '', '')))
            for i, (_, lines, _, _) in enumerate(gfx_props.PROPS[key])]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run', type=Path)
    parser.add_argument('--key', choices=sorted(gfx_props.PROPS), required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--original', action='store_true')
    parser.add_argument('--glob', default='f[0-9]*.png')
    args = parser.parse_args()
    rows = check(args.run, args.key, args.original, args.glob)
    args.out.mkdir(parents=True, exist_ok=True)
    with (args.out / 'coverage.tsv').open('w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter='\t', lineterminator='\n')
        writer.writerow(('atlas', 'label', 'status', 'frame', 'position', 'palette'))
        writer.writerows(rows)
    missing = [row[1] for row in rows if row[2] != 'ok']
    print(f'{len(rows) - len(missing)}/{len(rows)} complete labels; missing {missing}')
    return bool(missing)


if __name__ == '__main__':
    raise SystemExit(main())
