"""Pair English/original Fortune God cold captures; never generate verdicts."""
import argparse
import csv
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from skill import SKILL  # noqa: E402


def coverage(directory):
    with (directory / 'coverage.tsv').open(encoding='utf-8', newline='') as stream:
        rows = list(csv.DictReader(stream, delimiter='\t'))
    digest = (directory / 'disc.sha1').read_text().strip()
    assert len(rows) == 8 and {int(row['pose']) for row in rows} == set(range(8))
    assert all(r['status'] == 'ok' and r['disc_sha1'] == digest for r in rows), 'incomplete/stale coverage'
    return {int(r['pose']): directory / r['frame'] for r in rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run', type=Path)
    parser.add_argument('--original', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    english, original = coverage(args.run), coverage(args.original)
    args.out.mkdir(parents=True, exist_ok=True)

    def sheet(name, en, jp, crop=None):
        command = [sys.executable, '-X', 'utf8', str(Path(SKILL) / 'scripts/sheet.py'),
                   str(en), '--compare', str(jp), '--zoom', '5' if crop else '2',
                   '--out', str(args.out / f'{name}_sheet.png')]
        if crop:
            command += ['--crop', crop]
        subprocess.run(command, check=True)

    for pose in range(8):
        sheet(f'pose_{pose}', english[pose], original[pose], '112,72,128,88')
    for name in ('context_1', 'context_2', 'reward'):
        sheet(name, args.run / f'{name}.png', args.original / f'{name}.png')


if __name__ == '__main__':
    main()
