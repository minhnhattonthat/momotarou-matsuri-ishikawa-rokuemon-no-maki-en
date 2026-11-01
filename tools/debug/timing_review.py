"""Create native timing-game comparison sheets from complete disc coverage.

    python tools/debug/timing_review.py RUN --original ORIGINAL_RUN --out DIR

English left, original right. No verdicts are generated.
"""
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
    assert len(rows) == 10 and all(r['status'] == 'ok' for r in rows), 'incomplete coverage'
    return {(r['case'], r['label']): directory / r['case'] / r['frame'] for r in rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run', type=Path)
    parser.add_argument('--original', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    english, original = coverage(args.run), coverage(args.original)
    args.out.mkdir(parents=True, exist_ok=True)

    def sheet(name, en, jp, crop=None, zoom=2):
        command = [sys.executable, '-X', 'utf8', str(Path(SKILL) / 'scripts/sheet.py'),
                   str(en), '--compare', str(jp), '--zoom', str(zoom),
                   '--out', str(args.out / f'{name}_sheet.png')]
        if crop:
            command += ['--crop', crop]
        subprocess.run(command, check=True)

    for case in ('success', 'early'):
        sheet(case + '_start', english[case, 'Start'], original[case, 'Start'])
        sheet(case + '_cue', english[case, 'Start'], original[case, 'Start'], '124,108,72,40', 6)
        sheet(case + '_result', args.run / case / 'result.png', args.original / case / 'result.png')
    for item in range(6):
        case = 'success' if item < 4 else 'early'
        label = f'actor{item}'
        sheet(label, english[case, label], original[case, label], '104,56,112,104', 5)


if __name__ == '__main__':
    main()
