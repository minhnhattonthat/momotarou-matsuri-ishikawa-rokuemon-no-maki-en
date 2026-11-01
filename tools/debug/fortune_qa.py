"""Cold Fortune God reward route and complete actor checks from the named disc.

    python tools/debug/fortune_qa.py --out work/qa/fortune8_en [--original]

The ground shadow is translucent and excluded; every opaque actor/effect pixel
is required for poses 0-7, covering all four edited badge cells and the bow.
The alternate effect sequence (poses 9-13) is outside this route's scope;
pose 8 is omitted because its pixels are a subset of several other poses.
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
            if Path(path).name == 'M490D.BIN':
                return arc.entries(b''.join(iso.sector(disc, lba + i)
                                           for i in range((size + 2047) // 2048))[:size])
    raise ValueError('M490D missing from named disc')


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
        for pattern in ('actor_*.png', 'context_*.png', 'reward.png', 'return.png',
                        'coverage.tsv', 'log.txt', 'disc.sha1'):
            for old in out.glob(pattern):
                old.unlink()
        command = [sys.executable, '-X', 'utf8', str(Path(SKILL) / 'scripts/emu.py'), str(cue),
                   '--out', str(out), '--script', str(ROOT / 'tools/debug/warp.lua'),
                   '--script', str(ROOT / 'tools/debug/fortune.lua'),
                   '--script', str(ROOT / 'tools/lua/textlog.lua'),
                   '--var', "SCENE='game_m49_2d'", '--var', 'HOLD=-1',
                   '--frames', '900', '--timeout', '180']
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
        (out / 'runner.txt').write_text(result.stdout + result.stderr, encoding='utf-8')
        if result.returncode:
            print(result.stdout + result.stderr)
            return result.returncode
        assert hashlib.sha1(image.read_bytes()).hexdigest() == digest, 'disc changed during capture'
        (out / 'disc.sha1').write_text(digest + '\n', encoding='ascii')
    log = (out / 'log.txt').read_text(encoding='utf-8')
    for state in range(1, 5):
        assert re.search(rf'^FORTUNE state={state} sub=\d+ amount=\d+ f\d+$', log, re.M)
    assert re.search(r'^FORTUNE_RETURN mode=61 f\d+$', log, re.M), 'unexpected trial return'
    archive = source(image)
    actors = anm.items(archive[1][1])
    assert len(actors) == 14 and all(r[0][1:5] == (136, 128, 64, 16) for r in actors)
    templates = [[(r[0] & ~0x7000, *r[1:]) for r in records[1:]] for records in actors]
    anm.render(archive, templates, out / 'templates', strict=True)
    paths = sorted(out.glob('actor_*.png'))
    # Load once; all four badge variants appear in this native sequence.
    screens = [(path.name, Image.open(path).convert('RGB')) for path in paths]
    rows = []
    for index in range(8):
        found, position = '', None
        with Image.open(out / 'templates' / f'{index:03d}.png') as template:
            for name, screenshot in screens:
                position = match(screenshot, template, (116, 75, 125, 80))
                if position is not None:
                    found = name
                    break
        rows.append((index, 'ok' if found else 'missing', found, position, digest))
    with (out / 'coverage.tsv').open('w', encoding='utf-8', newline='') as stream:
        writer = csv.writer(stream, delimiter='\t', lineterminator='\n')
        writer.writerow(('pose', 'status', 'frame', 'position', 'disc_sha1'))
        writer.writerows(rows)
    for row in rows:
        print(*row, sep='\t')
    return int(any(row[1] != 'ok' for row in rows))


if __name__ == '__main__':
    raise SystemExit(main())
