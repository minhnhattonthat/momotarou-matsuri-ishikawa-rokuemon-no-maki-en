"""Cold native M50 Start, successful timing and early failure, with disc pixel checks.

    python tools/debug/timing_qa.py --out work/qa/timing8_en [--original]

Only controller input follows the established cold game warp. Captures must
match the named disc SHA-1 and native state logs. Actor checks omit the separate
translucent ground shadow, retaining every body and anger-puff sprite pixel.
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
            if Path(path).name == 'M500D.BIN':
                return arc.entries(b''.join(iso.sector(disc, lba + i)
                                           for i in range((size + 2047) // 2048))[:size])
    raise ValueError('M500D missing from named disc')


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
    if args.check_only:
        # Reject a wrong disc before replacing templates or coverage artifacts.
        for case in ('success', 'early'):
            assert (args.out / case / 'disc.sha1').read_text().strip() == digest, 'stale disc captures'
    else:
        (args.out / 'coverage.tsv').unlink(missing_ok=True)
    archive = source(image)
    actors = anm.items(archive[1][1])
    # First actor record is the translucent ground shadow, not costume art.
    assert all(r[0][1:5] == (64, 128, 64, 16) for r in actors)
    templates = [anm.items(archive[2][1])[3], *[r[1:] for r in actors]]
    templates = [[(r[0] & ~0x7000, *r[1:]) for r in records] for records in templates]
    anm.render(archive, templates, args.out / 'templates', strict=True)
    rows = []
    for case, result_code in (('success', 1), ('early', 2)):
        out = args.out / case
        out.mkdir(parents=True, exist_ok=True)
        if not args.check_only:
            for pattern in ('actor_*.png', 'countdown_*.png', 'result.png', 'log.txt', 'disc.sha1'):
                for old in out.glob(pattern):
                    old.unlink()
            command = [sys.executable, '-X', 'utf8', str(Path(SKILL) / 'scripts/emu.py'), str(cue),
                       '--out', str(out), '--script', str(ROOT / 'tools/debug/warp.lua'),
                       '--script', str(ROOT / 'tools/debug/timing_start.lua'),
                       '--script', str(ROOT / 'tools/lua/textlog.lua'),
                       '--var', "SCENE='game_m50_2e'", '--var', f"TIMING_OUTCOME='{case}'",
                       '--var', 'HOLD=-1', '--frames', '900', '--timeout', '180']
            result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
            (out / 'runner.txt').write_text(result.stdout + result.stderr, encoding='utf-8')
            if result.returncode:
                print(result.stdout + result.stderr)
                return result.returncode
            assert hashlib.sha1(image.read_bytes()).hexdigest() == digest, 'disc changed during capture'
            (out / 'disc.sha1').write_text(digest + '\n', encoding='ascii')
        assert (out / 'disc.sha1').read_text().strip() == digest, 'stale disc captures'
        log = (out / 'log.txt').read_text(encoding='utf-8')
        for number in range(1, 5):
            assert re.search(rf'^TIMING_CAPTURE cue={number} item={number - 1} state=\d+ f\d+$', log, re.M)
        assert re.search(rf'^TIMING_RESULT {case} result={result_code} f\d+$', log, re.M)
        wanted = [0, 1, 2, 3, 4] if case == 'success' else [0, 1, 2, 5, 6]
        for index in wanted:
            paths = [out / 'countdown_4.png'] if index == 0 else sorted(out.glob('actor_*.png'))
            position, found = None, ''
            with Image.open(args.out / 'templates' / f'{index:03d}.png') as template:
                for path in paths:
                    with Image.open(path) as screenshot:
                        position = match(screenshot.convert('RGB'), template, (96, 40, 128, 120))
                    if position is not None:
                        found = path.name
                        break
            rows.append((case, 'Start' if index == 0 else f'actor{index - 1}',
                         'ok' if found else 'missing', found, position, digest))
    with (args.out / 'coverage.tsv').open('w', encoding='utf-8', newline='') as stream:
        writer = csv.writer(stream, delimiter='\t', lineterminator='\n')
        writer.writerow(('case', 'label', 'status', 'frame', 'position', 'disc_sha1'))
        writer.writerows(rows)
    for row in rows:
        print(*row, sep='\t')
    return int(any(row[2] != 'ok' for row in rows))


if __name__ == '__main__':
    raise SystemExit(main())
