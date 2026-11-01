"""Cold native event crown coverage, matched to complete named-disc regions.

    python tools/debug/event_crowns_qa.py --out work/qa/crowns8_en [--original]

Only event entry is warped. Native animation, scrolling and palettes run
unchanged. --check-only rejects stale discs; --compare creates paired sheets.
"""
import argparse
import concurrent.futures as cf
import csv
import hashlib
from pathlib import Path
import subprocess
import sys

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
import gfx  # noqa: E402
import tim  # noqa: E402
from skill import SKILL  # noqa: E402
from announcements_qa import match  # noqa: E402
from dice_outcomes_qa import source  # noqa: E402
from warp_all import run  # noqa: E402

CASES = {
    'event03': ('EVT030D.BIN', 1, (154, 148, 204, 177)),
    'event11': ('EVT170D.BIN', 0, (185, 70, 227, 100)),
    'event12': ('EVT180D.BIN', 1, (115, 0, 152, 22)),
    'event13': ('EVT190D.BIN', 1, (130, 88, 171, 117)),
    'event23': ('EVT180D.BIN', 1, (115, 0, 152, 22)),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--cue', type=Path)
    parser.add_argument('--original', action='store_true')
    parser.add_argument('--check-only', action='store_true')
    parser.add_argument('--compare', type=Path)
    args = parser.parse_args()
    cue = (args.cue or ROOT / ('rom/Momotarou Matsuri - Ishikawa Rokuemon no Maki (Japan).cue'
                              if args.original else 'build/momotarou-matsuri_en.cue')).resolve()
    image = cue.with_suffix('.bin')
    digest = hashlib.sha1(image.read_bytes()).hexdigest()
    out = args.out.resolve()
    (out / 'shots').mkdir(parents=True, exist_ok=True)
    if args.check_only:
        assert (out / 'disc.sha1').read_text().strip() == digest, 'stale disc captures'
    else:
        with cf.ThreadPoolExecutor(2) as executor:
            results = list(executor.map(lambda name: run(str(cue), str(out), name,
                           hold=1800, every=60, probes=[str(ROOT / 'tools/lua/textlog.lua')]), CASES))
        for result in results:
            print(*result, sep='\t', flush=True)
        assert all(row[1] == 'ok' for row in results), results
        assert hashlib.sha1(image.read_bytes()).hexdigest() == digest, 'disc changed during capture'
        (out / 'disc.sha1').write_text(digest + '\n', encoding='ascii')
    rows = []
    for name, (archive, entry, rect) in CASES.items():
        texture = gfx.unpack(source(image, archive)[entry][1])[0]
        template = tim.image(texture).crop(rect)
        template.save(out / f'{name}_template.png')
        found, position = '', None
        for shot in sorted((out / name).glob('f[0-9]*.png')):
            with Image.open(shot) as screen:
                position = match(screen.convert('RGB'), template)
            if position is not None:
                found = str(shot)
                break
        rows.append((name, 'ok' if found else 'missing', found, position, digest))
    with (out / 'coverage.tsv').open('w', encoding='utf-8', newline='') as stream:
        writer = csv.writer(stream, delimiter='\t', lineterminator='\n')
        writer.writerow(('scene', 'status', 'frame', 'position', 'disc_sha1'))
        writer.writerows(rows)
    for row in rows:
        print(*row, sep='\t', flush=True)
    failed = any(row[1] != 'ok' for row in rows)
    if args.compare and not failed:
        reference = args.compare.resolve()
        with (reference / 'coverage.tsv').open(encoding='utf-8', newline='') as stream:
            originals = {row['scene']: row for row in csv.DictReader(stream, delimiter='\t')}
        reference_digest = (reference / 'disc.sha1').read_text().strip()
        (out / 'review').mkdir(exist_ok=True)
        for scene, _, frame, position, _ in rows:
            original = originals[scene]
            assert original['status'] == 'ok' and original['disc_sha1'] == reference_digest
            # Position is allowed to differ between asynchronous event stages.
            # Context comparisons use each oracle's first complete capture;
            # detail comparisons isolate the full source-matched crown region.
            from ast import literal_eval
            x, y = position
            ox, oy = literal_eval(original['position'])
            a, b, c, d = CASES[scene][2]
            for target, path, px, py in (('en', frame, x, y), ('jp', original['frame'], ox, oy)):
                subprocess.run([sys.executable, '-X', 'utf8', str(Path(SKILL) / 'scripts/sheet.py'),
                                path, '--crop', f'{px},{py},{c-a},{d-b}', '--zoom', '1',
                                '--out', str(out / f'{scene}_{target}_detail.png')], check=True)
            for scope, left, right, zoom in (
                    ('context', frame, original['frame'], '2'),
                    ('detail', out / f'{scene}_en_detail.png', out / f'{scene}_jp_detail.png', '10')):
                subprocess.run([sys.executable, '-X', 'utf8', str(Path(SKILL) / 'scripts/sheet.py'),
                                str(left), '--compare', str(right), '--zoom', zoom, '--out',
                                str(out / 'review' / f'{scene}_{scope}_sheet.png')], check=True)
    return int(failed)


if __name__ == '__main__':
    raise SystemExit(main())
