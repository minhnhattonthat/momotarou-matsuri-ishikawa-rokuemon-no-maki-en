"""Enlarged review sheets for the scoped HUD counter checks (no verdicts).

    python -X utf8 tools/debug/hud_units_review.py RUN --original ORIGINAL_RUN --out DIR

ORIGINAL_RUN supplies the twelve fixture screenshots. Context frames come
from successful coverage rows; the record stress case also shows 9999 at a
stable gameplay frame. Use qa_gate.py only after reading every output sheet.
"""
import argparse
import csv
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from skill import SKILL  # noqa: E402
from hud_units import CONTEXTS  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run', type=Path)
    parser.add_argument('--original', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    base = [sys.executable, '-X', 'utf8', str(Path(SKILL) / 'scripts/sheet.py')]
    subprocess.run(base + [str(args.run / 'fixture/announcement_*.png'),
                          '--compare', str(args.original / 'fixture'), '--crop', '152,124,48,24',
                          '--zoom', '5', '--cols', '2', '--max', '12',
                          '--out', str(args.out / 'fixture_sheet.png')], check=True, cwd=ROOT)
    frames = []
    for name in CONTEXTS:
        with (args.run / name / 'coverage/coverage.tsv').open(encoding='utf-8', newline='') as f:
            rows = list(csv.DictReader(f, delimiter='\t'))
        if any(row['status'] != 'ok' for row in rows):
            raise ValueError(f'{name}: incomplete coverage')
        frame = Path(rows[0]['frame'])
        if name == 'record':
            frame = args.run / name / 'f004800.png'
        frames.append(str(frame))
    for i in range(0, len(frames), 4):
        subprocess.run(base + frames[i:i + 4] + ['--zoom', '2', '--cols', '2', '--max', '4',
                       '--out', str(args.out / f'contexts{i // 4 + 1}_sheet.png')], check=True, cwd=ROOT)
    subprocess.run(base + [str(args.run / 'record/f004800.png'), '--crop', '16,16,288,32',
                          '--zoom', '4', '--out', str(args.out / 'record_sheet.png')], check=True, cwd=ROOT)


if __name__ == '__main__':
    main()
