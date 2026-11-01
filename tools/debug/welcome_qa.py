"""Verify the complete EVT220 welcome banner in a natural cold event15 run.

    python tools/debug/welcome_qa.py IMAGE.bin RUN --out DIR

Generate RUN with warp_all.py --only '^event15$' --hold 4800 --every 60,
without --click: Circle skips the scrolling illustrations. This oracle reads
the named disc, including ANM geometry, rather than the generator's PNG.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import anm
import arc
import gfx
import gfx_welcome
import iso
import tim
from announcements_qa import match

RECT = (162, 11, 224, 41)  # complete banner, rim and tacks; both texture pieces


def template(image):
    with image.open('rb') as disc:
        for path, lba, size in iso.files(str(image)):
            if Path(path).name == 'EVT220D.BIN':
                raw = b''.join(iso.sector(disc, lba + n)
                               for n in range((size + 2047) // 2048))[:size]
                entries = arc.entries(raw)
                records = anm.items(entries[3][1])[1]
                assert [(r[1], r[2], r[3], r[4], r[8] + 128, r[9] + 64)
                        for r in records] == list(gfx_welcome.PIECES)
                assert all(r[5:8] == (0, 481, 7) and r[10:12] == (4096, 4096)
                           for r in records)
                texture = gfx.unpack(entries[1][1])[0]
                _, depth, clut, pixels = tim.parse(texture)
                assert depth == 1 and clut[:2] == (0, 481) and pixels[:2] == (448, 0)
                return gfx_welcome.assemble(tim.image(texture)).crop(RECT)
    raise ValueError('EVT220D.BIN not found on disc')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('image', type=Path)
    parser.add_argument('run', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    expected = template(args.image)
    expected.save(args.out / 'banner_template.png')
    hits = []
    for path in sorted(args.run.glob('f[0-9]*.png')):
        with Image.open(path) as shot:
            position = match(shot.convert('RGB'), expected)
        if position is not None:
            hits.append({'shot': path.as_posix(), 'position': position})
    if hits:
        shutil.copyfile(hits[0]['shot'], args.out / 'banner.png')
    with args.image.open('rb') as disc:
        sha1 = hashlib.file_digest(disc, 'sha1').hexdigest()
    report = {'disc': args.image.as_posix(), 'sha1': sha1,
              'source': 'EVT220D.BIN:1, ANM 3 item 1', 'rectangle': RECT,
              'status': 'ok' if hits else 'missing', 'matches': hits}
    (args.out / 'coverage.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(f'{report["status"]}: {len(hits)} frames with the complete banner')
    return int(not hits)


if __name__ == '__main__':
    raise SystemExit(main())
