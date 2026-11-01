"""Cold native dice outcomes, checked against the named disc and rolled values.

    python tools/debug/dice_outcomes_qa.py --out work/qa/dice8_en [--original]

Each case varies controller timing until Win/Lose/Draw have all appeared.
M59's opponent is a declared encounter-entry parameter, never a result edit.
--check-only rejects changed discs and rechecks existing native captures.
Add --compare ORIGINAL_RUN to generate original/English review sheets.
--resume reuses hash-checked completed attempts when extending the search.
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

CASES = {'gussurin': (56, 0, 4, 1), 'oni': (59, 0, 9, 0), 'rokuemon': (59, 5, 16, 6)}
RESULT = re.compile(r'^DICE_RESULT round=(\d+) item=(\d+) entry=(\d+) player=(\d+) rival=(\d+) f(\d+)$', re.M)


def source(image, name):
    with image.open('rb') as disc:
        for path, lba, size in iso.files(str(image)):
            if Path(path).name == name:
                return arc.entries(b''.join(iso.sector(disc, lba + i)
                                           for i in range((size + 2047) // 2048))[:size])
    raise ValueError(f'{name} missing from named disc')


def check_run(out, game, opponent, entry, templates, digest):
    assert (out / 'disc.sha1').read_text().strip() == digest, 'stale disc captures'
    log = (out / 'log.txt').read_text(encoding='utf-8')
    assert f'DICE_ENTRY game={game} opponent={opponent} ' in log, 'wrong encounter'
    assert f'ARRIVED game_m{game}_{game - 4:02x} ' in log, 'missing cold arrival'
    assert f'DICE_RETURN game={game} ' in log, 'missing native return'
    rows = []
    for number, item, bank, player, rival, frame in RESULT.findall(log):
        item, bank, player, rival = map(int, (item, bank, player, rival))
        assert 1 <= player <= 6 and 1 <= rival <= 6, 'invalid native dice'
        assert bank == entry and item == (0 if player > rival else 1 if player < rival else 2)
        path = out / f'result_{int(number):02d}_{item}.png'
        with Image.open(path) as shot, Image.open(templates / f'{item:03d}.png') as template:
            position = match(shot.convert('RGB'), template, (96, 88, 128, 64))
        rows.append((item, 'ok' if position else 'missing', str(path), position, player, rival, frame))
    assert rows, 'no native result captures'
    return rows


def review_sheets(out, reference, cases):
    """Pair accepted complete sprites; sheet.py owns image scaling/composition."""
    sides = []
    for directory in (out, reference):
        digest = (directory / 'disc.sha1').read_text().strip()
        with (directory / 'coverage.tsv').open(encoding='utf-8', newline='') as stream:
            records = list(csv.DictReader(stream, delimiter='\t'))
        chosen = {}
        for row in records:
            assert row['disc_sha1'] == digest and row['status'] == 'ok', 'unaccepted reference run'
            chosen.setdefault((row['case'], row['item']), row['frame'])
        sides.append(chosen)
    destination = out / 'review'
    destination.mkdir(parents=True, exist_ok=True)
    for name in cases:
        for item, label in enumerate(('win', 'lose', 'draw')):
            key = name, str(item)
            for scope, options in (('context', ['--zoom', '2']),
                                   ('detail', ['--crop', '104,96,112,48', '--zoom', '6'])):
                command = [sys.executable, '-X', 'utf8', str(Path(SKILL) / 'scripts/sheet.py'),
                           sides[0][key], '--compare', sides[1][key], *options, '--out',
                           str(destination / f'{name}_{label}_{scope}_sheet.png')]
                subprocess.run(command, cwd=ROOT, check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--cue', type=Path)
    parser.add_argument('--original', action='store_true')
    parser.add_argument('--check-only', action='store_true')
    parser.add_argument('--only', choices=tuple(CASES))
    parser.add_argument('--attempts', type=int, default=24)
    parser.add_argument('--resume', action='store_true')
    parser.add_argument('--compare', type=Path, help='accepted original run; generate review sheets')
    args = parser.parse_args()
    if not 1 <= args.attempts <= 40:
        parser.error('--attempts must be 1..40')
    cue = (args.cue or ROOT / ('rom/Momotarou Matsuri - Ishikawa Rokuemon no Maki (Japan).cue'
                              if args.original else 'build/momotarou-matsuri_en.cue')).resolve()
    image = cue.with_suffix('.bin')
    digest = hashlib.sha1(image.read_bytes()).hexdigest()
    if args.check_only or (args.resume and (args.out / 'disc.sha1').exists()):
        assert (args.out / 'disc.sha1').read_text().strip() == digest, 'stale disc captures'
    args.out.mkdir(parents=True, exist_ok=True)
    rows = []
    failed = False
    for name, (game, opponent, entry, texture) in CASES.items():
        if args.only and name != args.only:
            continue
        directory = args.out / name
        archive = source(image, f'M{game}0D.BIN')
        records = anm.items(archive[entry][1])
        templates = directory / 'templates'
        anm.render([archive[texture]], [[(r[0] & ~0x7000, *r[1:]) for r in records[i]]
                                       for i in range(3)], templates, strict=True)
        seen = set()
        runs = sorted(directory.glob('attempt_*')) if args.check_only else [
            directory / f'attempt_{i:02d}' for i in range(args.attempts)]
        for index, out in enumerate(runs):
            if not args.check_only and not (args.resume and (out / 'disc.sha1').exists()):
                out.mkdir(parents=True, exist_ok=True)
                # Remove only known artifacts in this run, never another case.
                for pattern in ('result_*.png', 'dialogue_*.png', 'log.txt', 'disc.sha1'):
                    for old in out.glob(pattern):
                        old.unlink()
                command = [sys.executable, '-X', 'utf8', str(Path(SKILL) / 'scripts/emu.py'), str(cue),
                           '--out', str(out), '--script', str(ROOT / 'tools/debug/warp.lua'),
                           '--script', str(ROOT / 'tools/debug/dice_outcomes.lua'),
                           '--script', str(ROOT / 'tools/lua/textlog.lua'),
                           '--var', f"SCENE='game_m{game}_{game - 4:02x}'", '--var', f'DICE_GAME={game}',
                           '--var', f'DICE_OPPONENT={opponent}', '--var', f'DICE_OFFSET={index * 17}',
                           '--var', f'DICE_PERIOD={90 + index * 7}', '--var', 'HOLD=-1',
                           '--frames', '900', '--timeout', '180']
                result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
                (out / 'runner.txt').write_text(result.stdout + result.stderr, encoding='utf-8')
                if result.returncode:
                    print(result.stdout + result.stderr)
                    return result.returncode
                assert hashlib.sha1(image.read_bytes()).hexdigest() == digest, 'disc changed during capture'
                (out / 'disc.sha1').write_text(digest + '\n', encoding='ascii')
            checked = check_run(out, game, opponent, entry, templates, digest)
            rows.extend((name, *row, digest) for row in checked)
            seen.update(row[0] for row in checked if row[1] == 'ok')
            print(name, out.name, f'complete native outcomes {sorted(seen)}', flush=True)
            failed |= any(row[1] != 'ok' for row in checked)
            if not args.check_only and seen == {0, 1, 2}:
                break
        failed |= seen != {0, 1, 2}
    with (args.out / 'coverage.tsv').open('w', encoding='utf-8', newline='') as stream:
        writer = csv.writer(stream, delimiter='\t', lineterminator='\n')
        writer.writerow(('case', 'item', 'status', 'frame', 'position', 'player', 'rival', 'vsync', 'disc_sha1'))
        writer.writerows(rows)
    (args.out / 'disc.sha1').write_text(digest + '\n', encoding='ascii')
    if args.compare and not failed:
        review_sheets(args.out, args.compare, [args.only] if args.only else CASES)
    return int(failed)


if __name__ == '__main__':
    raise SystemExit(main())
