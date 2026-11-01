"""Cold solo/versus Duel cues, matched against the named disc's ANM and TIM.

    python tools/debug/duel_qa.py --out work/qa/duel8_en
    python tools/debug/duel_qa.py --original --out work/qa/duel8_jp

No inputs after the warp: the game naturally counts to five and shows the cue.
The versus route uses two_player.lua and requires two connected emulator pads.
"""
import argparse
import csv
import hashlib
from pathlib import Path
import re
import shutil
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
            if Path(path).name == 'M990D.BIN':
                raw = b''.join(iso.sector(disc, lba + i)
                               for i in range((size + 2047) // 2048))[:size]
                return arc.entries(raw)
    raise ValueError('M990D missing from named disc')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--original', action='store_true')
    parser.add_argument('--cue', type=Path)
    parser.add_argument('--check-only', action='store_true')
    parser.add_argument('--only', nargs='+', choices=('solo', 'versus'), default=['solo', 'versus'])
    args = parser.parse_args()
    cue = (args.cue or ROOT / ('rom/Momotarou Matsuri - Ishikawa Rokuemon no Maki (Japan).cue'
                              if args.original else 'build/momotarou-matsuri_en.cue')).resolve()
    image = cue.with_suffix('.bin')
    digest = hashlib.sha1(image.read_bytes()).hexdigest()
    archive = source(image)
    records = [(r[0] & ~0x7000, *r[1:]) for r in anm.items(archive[2][1])[73]]
    args.out.mkdir(parents=True, exist_ok=True)
    anm.render(archive, [records], args.out / 'template', strict=True)
    rows = []
    for case in args.only:
        out = args.out / case
        out.mkdir(parents=True, exist_ok=True)
        players = 1 if case == 'solo' else 2
        if not args.check_only:
            for name in ('log.txt', 'disc.sha1', 'cue.png', 'two_player_menu.png'):
                (out / name).unlink(missing_ok=True)
            command = [sys.executable, '-X', 'utf8', str(Path(SKILL) / 'scripts/emu.py'), str(cue),
                       '--out', str(out), '--script', str(ROOT / 'tools/debug/warp.lua'),
                       '--script', str(ROOT / 'tools/debug/duel.lua'),
                       '--script', str(ROOT / 'tools/lua/textlog.lua'),
                       '--var', "SCENE='game_m16_12'", '--var', f'DUEL_PLAYERS={players}',
                       '--var', 'HOLD=1800', '--frames', '900', '--shot-every', '30', '--timeout', '180']
            if case == 'versus':
                command += ['--script', str(ROOT / 'tools/debug/two_player.lua')]
            result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
            (out / 'runner.txt').write_text(result.stdout + result.stderr, encoding='utf-8')
            if result.returncode:
                print(result.stdout + result.stderr)
                return result.returncode
            (out / 'disc.sha1').write_text(digest + '\n', encoding='ascii')
        assert (out / 'disc.sha1').read_text().strip() == digest, 'stale disc captures'
        log = (out / 'log.txt').read_text(encoding='utf-8')
        proof = re.search(rf'^DUEL players={players} selector={players - 1} f(\d+)$', log, re.M)
        assert proof, f'{case}: missing native player-count verification'
        if case == 'versus':
            assert 'TWO_PLAYER verified mode=12 selector=1' in log
        found, position = '', None
        with Image.open(args.out / 'template/000.png') as template:
            for path in sorted(out.glob('f[0-9]*.png')):
                if int(path.stem[1:]) < int(proof.group(1)):
                    continue
                with Image.open(path) as screenshot:
                    if screenshot.size != (320, 240):
                        continue
                    position = match(screenshot.convert('RGB'), template, (128, 48, 64, 40))
                if position is not None:
                    found = path.name
                    shutil.copyfile(path, out / 'cue.png')
                    break
        rows.append((case, 'ok' if found else 'missing', found, position, digest))
    with (args.out / 'coverage.tsv').open('w', encoding='utf-8', newline='') as stream:
        writer = csv.writer(stream, delimiter='\t', lineterminator='\n')
        writer.writerow(('case', 'status', 'frame', 'position', 'disc_sha1'))
        writer.writerows(rows)
    for row in rows:
        print(*row, sep='\t')
    return int(any(row[1] != 'ok' for row in rows))


if __name__ == '__main__':
    raise SystemExit(main())
