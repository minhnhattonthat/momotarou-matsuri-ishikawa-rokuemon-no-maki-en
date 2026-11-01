"""Find complete event props in cold screenshots, using pixels from a disc.

    python tools/debug/event_props_qa.py IMAGE.bin --snow RUN --ending RUN --out DIR

Requires all three ending fans and both pieces of the snow initial, including
nearby paper/snow. It does not classify the tiny snow placards or approve
other event artwork. Screenshot generation uses warp.lua event07 and event20.
"""
import argparse
import csv
from pathlib import Path
import shutil
import sys

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import arc  # noqa: E402
import gfx  # noqa: E402
import iso  # noqa: E402
import tim  # noqa: E402
from announcements_qa import match  # noqa: E402

PROPS = [('snow_upper', 'EVT110D.BIN', (228, 104, 255, 128)),
         ('snow_lower', 'EVT110D.BIN', (227, 128, 249, 137)),
         ('fan_top', 'EVT620D.BIN', (96, 0, 156, 30)),
         ('fan_left', 'EVT620D.BIN', (0, 58, 38, 91)),
         ('fan_right', 'EVT620D.BIN', (268, 120, 320, 174))]


def pictures(image):
    pictures = {}
    with image.open('rb') as disc:
        for path, lba, size in iso.files(str(image)):
            name = Path(path).name
            if name not in {row[1] for row in PROPS}:
                continue
            raw = b''.join(iso.sector(disc, lba + n) for n in range((size + 2047) // 2048))[:size]
            entries = arc.entries(raw)
            textures = [gfx.unpack(entries[entry][1])[0] for entry in (0, 1)]
            picture = Image.new('RGBA', (320, 240))
            for entry, width, x in ((0, 240, 0), (1, 80, 240)):
                texture = tim.image(textures[entry])
                # EVT620's second TIM uploads to the SAME CLUT address as
                # its first. Both halves therefore draw with the later CLUT.
                if entry == 0 and tim.parse(textures[0])[2][:4] == tim.parse(textures[1])[2][:4]:
                    palette = gfx.palette(textures[1], 0)
                    texture.putdata([palette[i] for i in gfx.indices(textures[0])])
                picture.paste(texture.crop((0, 0, width, 240)), (x, 0))
            pictures[name] = picture
    assert len(pictures) == 2, pictures.keys()
    return pictures


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('image', type=Path)
    ap.add_argument('--snow', type=Path, required=True)
    ap.add_argument('--ending', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    sources = pictures(args.image)
    rows = []
    for label, name, rect in PROPS:
        run = args.snow if name == 'EVT110D.BIN' else args.ending
        template = sources[name].crop(rect)
        template.save(args.out / f'{label}_template.png')
        found, position = '', None
        paths = sorted(run.glob('f[0-9]*.png')) + sorted(run.glob('event*.png'))
        for path in paths:
            with Image.open(path) as screenshot:
                position = match(screenshot.convert('RGB'), template)
            if position is not None:
                found = path.as_posix()
                shutil.copyfile(path, args.out / f'{label}.png')
                break
        rows.append((label, 'ok' if found else 'missing', name, str(rect), found, position))
    with (args.out / 'coverage.tsv').open('w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter='\t', lineterminator='\n')
        writer.writerow(('prop', 'status', 'archive', 'source_rect', 'shot', 'position'))
        writer.writerows(rows)
    for row in rows:
        print(*row, sep='\t')
    print(f'{sum(row[1] == "ok" for row in rows)}/{len(rows)} complete event prop regions')
    return int(any(row[1] != 'ok' for row in rows))


if __name__ == '__main__':
    raise SystemExit(main())
