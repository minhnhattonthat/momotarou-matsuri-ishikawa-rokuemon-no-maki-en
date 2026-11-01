"""Require the complete card art and name strip in each cold-boot fixture shot.

    python -X utf8 tools/debug/cards_qa.py RUN --out DIR [--original]

Checks all 100 unique cards against their own TIM, with the game's native ANM
positions. This is runtime coverage, not approval of untranslated illustrations.
"""
import argparse
import csv
import json
import struct
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import arc  # noqa: E402
import gen_gfx  # noqa: E402
import gfx  # noqa: E402
import tim  # noqa: E402


def matches(screen, template, x, y):
    if x + template.width > screen.width or y + template.height > screen.height:
        return False
    for dy in range(template.height):
        for dx in range(template.width):
            colour = template.getpixel((dx, dy))
            if colour[3] and max(abs(a - b) for a, b in zip(
                    colour[:3], screen.getpixel((x + dx, y + dy))[:3])) > 8:
                return False
    return True


def meanings():
    data = (gfx.TREE / 'OVLXTTL.BIN').read_bytes()
    pointers = struct.unpack_from('<100I', data, 0x800E05DC - 0x800CB338)
    rows = json.loads((gfx.ROOT / 'script' / 'OVLXTTL.json').read_text(encoding='utf-8'))
    by_address = {int(row['id'].split('@')[1], 16): row for row in rows}
    return [by_address[p] for p in pointers]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('run', type=Path)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--original', action='store_true')
    args = ap.parse_args()
    rows = []
    archives = {}
    args.out.mkdir(parents=True, exist_ok=True)
    pref = [name for name, count in gen_gfx.PREFECTURES for _ in range(count)]
    for i, meaning in enumerate(meanings()):
        name = f'HCARD{i // 10}0D.BIN'
        if name not in archives:
            raw = (gfx.TREE / name).read_bytes()
            archives[name] = arc.entries(raw)
        archive = archives[name]
        texture = gfx.unpack(archive[i % 10][1])[0]
        if not args.original:
            texture = gfx.redraw(texture, gfx.EN / f'HCARD{i // 10}0D_{i % 10}.png')
        source = tim.image(texture).convert('RGBA')
        shot = args.run / f'card_{i + 1:03d}.png'
        art = caption = False
        if shot.exists():
            with Image.open(shot) as screen:
                screen = screen.convert('RGB')
                art = matches(screen, source.crop((0, 0, 208, 128)), 56, 56)
                caption = matches(screen, source.crop((0, 128, 120, 144)), 88, 32)
        rows.append((i + 1, 'ok' if art and caption else 'missing', art, caption,
                     pref[i], meaning['id'], meaning['jp'].strip(), meaning['en'], shot.as_posix()))
    args.out.mkdir(parents=True, exist_ok=True)
    with (args.out / 'coverage.tsv').open('w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter='\t', lineterminator='\n')
        writer.writerow(('card', 'status', 'art', 'caption', 'prefecture', 'meaning_id', 'jp', 'en', 'shot'))
        writer.writerows(rows)
    missing = [row[0] for row in rows if row[1] != 'ok']
    print(f'{100 - len(missing)}/100 complete card captures; missing {missing}')
    return bool(missing)


if __name__ == '__main__':
    raise SystemExit(main())
