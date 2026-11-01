"""Cold Even Tanuki scroll coverage from controller-only dice play.

    python tools/debug/tanuki_qa.py --out work/qa/tanuki8_en [--original]

Checks both complete scroll sprites and the natural Streak label from the
named disc. No result, RNG, animation or placement RAM edits.
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
import arc  # noqa: E402
import iso  # noqa: E402
from skill import SKILL  # noqa: E402
from announcements_qa import match  # noqa: E402


def source(image):
    with image.open('rb') as disc:
        for path, lba, size in iso.files(str(image)):
            if Path(path).name == 'M140D.BIN':
                return arc.entries(b''.join(iso.sector(disc, lba + i)
                                           for i in range((size + 2047) // 2048))[:size])
    raise ValueError('M140D missing from named disc')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--cue', type=Path)
    parser.add_argument('--original', action='store_true')
    parser.add_argument('--check-only', action='store_true')
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
        for pattern in ('f[0-9]*.png', 'scroll_*.png', 'game_m14_10.png', 'final.png',
                        'coverage.tsv', 'log.txt', 'disc.sha1'):
            for old in out.glob(pattern):
                old.unlink()
        command = [sys.executable, '-X', 'utf8', str(Path(SKILL) / 'scripts/emu.py'), str(cue),
                   '--out', str(out), '--script', str(ROOT / 'tools/debug/warp.lua'),
                   '--script', str(ROOT / 'tools/lua/textlog.lua'),
                   '--var', "SCENE='game_m14_10'", '--var', 'HOLD=6500', '--var', 'CLICK=90',
                   '--frames', '900', '--shot-every', '12', '--timeout', '180']
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
    archive = source(image)
    # Only texture 0 is used by these sprites; other entries share VRAM pages.
    records = anm.items(archive[11][1])
    assert [r[0][1:5] for r in records[:2]] == [(160, 128, 24, 32), (160, 168, 24, 40)]
    templates = [[(r[0] & ~0x7000, *r[1:]) for r in records[i]] for i in (0, 1, 2)]
    anm.render(archive[:1], templates, out / 'templates', strict=True)
    rows = []
    for index, label in enumerate(('upright', 'tilted', 'streak')):
        found, position = '', None
        with Image.open(out / 'templates' / f'{index:03d}.png') as template:
            for path in sorted(out.glob('f[0-9]*.png')):
                if int(path.stem[1:]) < int(arrival.group(1)):
                    continue
                with Image.open(path) as screenshot:
                    if screenshot.size != (320, 240):
                        continue
                    region = (145, 48, 40, 60) if index < 2 else (144, 96, 60, 32)
                    position = match(screenshot.convert('RGB'), template, region)
                if position is not None:
                    found = path.name
                    break
        rows.append((label, index, 'ok' if found else 'missing', found, position, digest))
    with (out / 'coverage.tsv').open('w', encoding='utf-8', newline='') as stream:
        writer = csv.writer(stream, delimiter='\t', lineterminator='\n')
        writer.writerow(('label', 'item', 'status', 'frame', 'position', 'disc_sha1'))
        writer.writerows(rows)
    for row in rows:
        print(*row, sep='\t')
    return int(any(row[2] != 'ok' for row in rows))


if __name__ == '__main__':
    raise SystemExit(main())
