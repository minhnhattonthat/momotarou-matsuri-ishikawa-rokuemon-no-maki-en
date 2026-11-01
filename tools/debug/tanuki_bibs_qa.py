"""Cold native two-player Even Tanuki and disc-sourced Kintaro sprite coverage.

    python tools/debug/tanuki_bibs_qa.py --out work/qa/bibs8_en [--original]

No outcomes, RNG, sprite selections or positions are injected. Shadow pixels
are translucent and excluded; every opaque pixel of the complete actor is
checked. ANM6 items 9/10 share identical assembled actor pixels, so one match
proves the cell, not both vertical positions in the jump animation.
"""
import argparse
import csv
import hashlib
from pathlib import Path
import re
import subprocess
import sys

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
import anm  # noqa: E402
from skill import SKILL  # noqa: E402
from announcements_qa import match  # noqa: E402
from tanuki_qa import source  # noqa: E402

ITEMS = (0, 1, 5, 6, 7, 8, 9, 11, 12)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--cue', type=Path)
    parser.add_argument('--original', action='store_true')
    parser.add_argument('--check-only', action='store_true')
    parser.add_argument('--offset', type=int, default=45)
    parser.add_argument('--hold', type=int, default=6000)
    args = parser.parse_args()
    cue = (args.cue or ROOT / ('rom/Momotarou Matsuri - Ishikawa Rokuemon no Maki (Japan).cue'
                              if args.original else 'build/momotarou-matsuri_en.cue')).resolve()
    image = cue.with_suffix('.bin')
    digest = hashlib.sha1(image.read_bytes()).hexdigest()
    out = args.out
    out.mkdir(parents=True, exist_ok=True)
    if args.check_only:
        assert (out / 'disc.sha1').read_text().strip() == digest, 'stale disc captures'
    else:
        for pattern in ('f[0-9]*.png', 'game_m14_10.png', 'final.png',
                        'coverage.tsv', 'log.txt', 'disc.sha1'):
            for old in out.glob(pattern):
                old.unlink()
        command = [sys.executable, '-X', 'utf8', str(Path(SKILL) / 'scripts/emu.py'), str(cue),
                   '--out', str(out), '--script', str(ROOT / 'tools/debug/warp.lua'),
                   '--script', str(ROOT / 'tools/debug/two_player.lua'),
                   '--script', str(ROOT / 'tools/debug/tanuki.lua'),
                   '--script', str(ROOT / 'tools/lua/textlog.lua'),
                   '--var', "SCENE='game_m14_10'", '--var', f'HOLD={args.hold}',
                   '--var', f'TANUKI_OFFSET={args.offset}',
                   '--frames', '900', '--shot-every', '6', '--timeout', '240']
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
        (out / 'runner.txt').write_text(result.stdout + result.stderr, encoding='utf-8')
        if result.returncode:
            print(result.stdout + result.stderr)
            return result.returncode
        assert hashlib.sha1(image.read_bytes()).hexdigest() == digest, 'disc changed during capture'
        (out / 'disc.sha1').write_text(digest + '\n', encoding='ascii')
    log = (out / 'log.txt').read_text(encoding='utf-8')
    arrival = re.search(r'^ARRIVED game_m14_10 f(\d+)$', log, re.M)
    assert arrival, 'missing scene arrival'
    assert 'TWO_PLAYER verified mode=10 selector=1' in log
    archive = source(image)
    actors = anm.items(archive[6][1])
    assert len(actors) == 13
    templates = [[(r[0] & ~0x7000, *r[1:]) for r in actors[i][1:]] for i in ITEMS]
    anm.render(archive[2:3], templates, out / 'templates', strict=True)
    # Crop once to keep a long native run's memory bounded. All Kintaro sprites
    # stay on the right half; the offset is restored in the coverage output.
    region = (224, 96, 320, 208)
    screens = []
    for path in sorted(out.glob('f[0-9]*.png')):
        if int(path.stem[1:]) < int(arrival.group(1)) - 600:
            continue
        with Image.open(path) as screenshot:
            if screenshot.size == (320, 240):
                screens.append((path.name, screenshot.crop(region).convert('RGB')))
    rows = []
    for index, item in enumerate(ITEMS):
        found, position = '', None
        with Image.open(out / 'templates' / f'{index:03d}.png') as template:
            for name, screenshot in screens:
                position = match(screenshot, template)
                if position is not None:
                    position = (position[0] + region[0], position[1] + region[1])
                    found = name
                    break
        rows.append((item, 'ok' if found else 'missing', found, position, digest))
    with (out / 'coverage.tsv').open('w', encoding='utf-8', newline='') as stream:
        writer = csv.writer(stream, delimiter='\t', lineterminator='\n')
        writer.writerow(('item', 'status', 'frame', 'position', 'disc_sha1'))
        writer.writerows(rows)
    for row in rows:
        print(*row, sep='\t')
    return int(any(row[1] != 'ok' for row in rows))


if __name__ == '__main__':
    raise SystemExit(main())
