"""Find a complete cold-boot screenshot for each of the 22 redrawn credit items.

    python -X utf8 tools/debug/credits_qa.py work/qa/credits8_final --out work/qa/credits8_review

Read-only image oracle: the original ANM anchors determine x; y scrolls. Every
white glyph pixel of a whole item must be visible, with its dark outline. The
script copies matching frames and writes coverage.tsv, then returns nonzero if
any item is absent. This supplements, and never substitutes for, visual review.
"""
import argparse
import csv
import shutil
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import anm  # noqa: E402
import arc  # noqa: E402
import gen_credits  # noqa: E402
import gfx  # noqa: E402


def templates():
    records = anm.items(arc.entries((gfx.TREE / 'EVT600D.BIN').read_bytes())[37][1])
    atlases = {page: Image.open(gfx.EN / f'EVT600D_{entry}.png').convert('RGBA')
               for page, entry in gen_credits.PAGES.items()}
    result = {}
    for item, sprites in enumerate(records):
        x0, y0 = min(r[8] for r in sprites), min(r[9] for r in sprites)
        x1, y1 = max(r[8] + r[3] for r in sprites), max(r[9] + r[4] for r in sprites)
        im = Image.new('RGBA', (x1 - x0, y1 - y0))
        for r in sprites:
            u, v, w, h, page = r[1], r[2], r[3], r[4], r[7]
            im.paste(atlases[page].crop((u, v, u + w, v + h)), (r[8] - x0, r[9] - y0))
        ink, shadow = [], []
        for y in range(im.height):
            for x in range(im.width):
                c = im.getpixel((x, y))
                if c[3]:
                    (ink if c[0] > 200 else shadow).append((160 + x0 + x, y))
        result[item] = im.height, ink, shadow
    return result


def find(px, height, template):
    th, ink, shadow = template
    # A few glyph pixels reject most positions cheaply before checking the whole item.
    probes = ink[::max(1, len(ink) // 12)]
    for dy in range(height - th + 1):
        if not all(min(px[x, y + dy][:3]) >= 230 for x, y in probes):
            continue
        if not all(min(px[x, y + dy][:3]) >= 230 for x, y in ink):
            continue
        if not all(max(px[x, y + dy][:3]) <= 24 for x, y in shadow):
            continue
        return dy
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('run', type=Path)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    pending = templates()
    found = {}
    args.out.mkdir(parents=True, exist_ok=True)
    for path in sorted(args.run.glob('f[0-9]*.png')):
        im = Image.open(path).convert('RGB')
        if im.size != (320, 240):
            continue
        for item in list(pending):
            dy = find(im.load(), im.height, pending[item])
            if dy is not None:
                out = args.out / f'credit_{item:02d}.png'
                shutil.copyfile(path, out)
                found[item] = (item, 'ok', path.as_posix(), dy)
                del pending[item]
        if not pending:
            break
    with (args.out / 'coverage.tsv').open('w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter='\t', lineterminator='\n')
        writer.writerow(('item', 'status', 'frame', 'y'))
        for item in range(22):
            writer.writerow(found.get(item, (item, 'missing', '', '')))
    print(f'{len(found)}/22 complete credit items; missing {sorted(pending)}')
    return bool(pending)


if __name__ == '__main__':
    sys.exit(main())
