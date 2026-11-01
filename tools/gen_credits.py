"""Redraw the 22 credit screens without changing their ANM or palette (EVT600D:2-4).

    python -X utf8 tools/gen_credits.py [--preview DIR]

gfx/credits.tsv identifies a logical line by ANM item and its screen-space x/y.
Adjacent sprite fragments are assembled BEFORE lettering and scattered back to
their original atlas rectangles afterwards. Some lines cross atlas rows/pages.
Every line must have a translation, fit at native pixel size, and own its pixels.
"""
import argparse
import csv
from pathlib import Path

from PIL import Image, ImageFilter

import anm
import arc
import engine
import gfx
import tim

ROOT = Path(__file__).resolve().parents[1]
FILE = 'EVT600D.BIN'
PAGES = {9: 2, 10: 3, 11: 4}
WHITE = (248, 248, 248, 255)
BLACK = (8, 8, 8, 255)
CLEAR = (0, 0, 0, 0)


def lines(records):
    """Yield each line's adjacent fragments, sorted top-to-bottom and left-to-right."""
    result = []
    for r in sorted(records, key=lambda r: (r[9], r[8])):
        if r[0] or r[4] != 16 or r[10:12] != (4096, 4096) or r[7] not in PAGES:
            raise ValueError(f'unsupported credit sprite {r}')
        if result and r[9] == result[-1][0][9] and r[8] == result[-1][-1][8] + result[-1][-1][3]:
            result[-1].append(r)
        else:
            result.append([r])
    return result


def translations():
    with (ROOT / 'gfx' / 'credits.tsv').open(encoding='utf-8') as f:
        rows = csv.DictReader((line for line in f if not line.startswith('#')), delimiter='\t')
        result = {}
        for row in rows:
            key = tuple(int(row[k]) for k in ('item', 'x', 'y'))
            if key in result or not row['jp'] or not row['en']:
                raise ValueError(f'duplicate or empty credit {row}')
            result[key] = row['en']
        return result


def lettering(text, width, glyphs):
    """Native 7px capitals, with a one-pixel dark outline; no resampling."""
    parts = text.upper().split('|')
    if len(parts) > 2:
        raise ValueError(f'too many lines: {text}')
    mask = Image.new('L', (width, 16))
    for i, part in enumerate(parts):
        cells = [glyphs[c] if c != ' ' else ['..'] * 7 for c in part]
        widths = [max(map(len, cell)) for cell in cells]
        w = sum(widths) + len(cells) - 1
        if w + 2 > width:
            raise ValueError(f'{text!r} needs {w + 2}px; sprite is {width}px')
        x, y = (width - w) // 2, (4 if len(parts) == 1 else i * 8)
        for cell, cw in zip(cells, widths):
            for dy, row in enumerate(cell):
                for dx, pixel in enumerate(row):
                    if pixel == '#':
                        mask.putpixel((x + dx, y + dy), 255)
            x += cw + 1
    image = Image.new('RGBA', mask.size, CLEAR)
    image.paste(BLACK, mask=mask.filter(ImageFilter.MaxFilter(3)))
    image.paste(WHITE, mask=mask)
    return image


def generate(preview=None, same=None):
    if same is None:
        from gen_gfx import copies
        same = copies()
    archive = arc.entries((gfx.TREE / FILE).read_bytes())
    frames = anm.items(archive[37][1])
    glyphs = engine.glyphs(ROOT / 'fonts' / 'credits7.txt')
    words = translations()
    images = {page: tim.image(gfx.unpack(archive[entry][1])[0]) for page, entry in PAGES.items()}
    owned, used = set(), set()
    for item, records in enumerate(frames):
        for fragments in lines(records):
            x, y = fragments[0][8:10]
            key = (item, x, y)
            used.add(key)
            word = lettering(words[key], sum(r[3] for r in fragments), glyphs)
            for r in fragments:
                u, v, w, h, page = r[1], r[2], r[3], r[4], r[7]
                pixels = {(page, sx, sy) for sy in range(v, v + h) for sx in range(u, u + w)}
                if owned & pixels:
                    raise ValueError(f'credit source pixels shared: {key}')
                owned.update(pixels)
                dx = r[8] - x
                images[page].paste(word.crop((dx, 0, dx + w, h)), (u, v))
    if used != words.keys():
        raise ValueError(f'unused translations: {words.keys() - used}')
    gfx.EN.mkdir(parents=True, exist_ok=True)
    for page, image in images.items():
        t = gfx.unpack(archive[PAGES[page]][1])[0]
        for copy in same[t]:
            name, entry = copy.split(':')
            out = gfx.EN / f'{Path(name).stem}_{entry}.png'
            image.save(out)
            gfx.redraw(t, out)  # validate palette/size before the build
            print(f'{out.relative_to(ROOT)}: {gfx.changed_box(t, out)}')
    if preview:
        # Use the same ANM renderer as the original preview, with only the TIM pixels replaced.
        patched = gfx.apply(FILE, (gfx.TREE / FILE).read_bytes())
        anm.render(arc.entries(patched), frames, preview)
    print(f'{len(used)} complete credit lines in {len(frames)} screens')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--preview', type=Path)
    generate(ap.parse_args().preview)
