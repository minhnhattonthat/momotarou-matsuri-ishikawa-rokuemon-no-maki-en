"""Make scoped full-screen save/name comparisons with the skill's sheet tool."""
import argparse
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from skill import SKILL  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--en', type=Path, default=ROOT / 'work/qa/np_en')
    ap.add_argument('--jp', type=Path, default=ROOT / 'work/qa/np_jp')
    ap.add_argument('--short', type=Path, default=ROOT / 'work/qa/np_short')
    ap.add_argument('--short-jp', type=Path, default=ROOT / 'work/qa/np_sjp')
    ap.add_argument('--out', type=Path, default=ROOT / 'work/qa/np_review')
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    groups = [
        ('save', args.en / 'write', args.jp / 'write',
         ['record_name', 'save_prompt', 'save_advice', 'save_slot', 'use_file', 'overwrite', 'save_complete',
          'saved_return']),
        ('reload', args.en / 'reload', args.jp / 'reload', ['loaded_menu', 'reloaded_name']),
        ('short_write', args.short / 'write', args.short_jp / 'write', ['record_name', 'overwrite']),
        ('short_reload', args.short / 'reload', args.short_jp / 'reload', ['reloaded_name']),
    ]
    for label, english, japanese, names in groups:
        paths = [english / f'{n}.png' for n in names]
        assert all(p.exists() and (japanese / p.name).exists() for p in paths), label
        subprocess.run([sys.executable, '-X', 'utf8', str(Path(SKILL) / 'scripts/sheet.py'),
                        *map(str, paths), '--compare', str(japanese), '--zoom', '2', '--cols', '1',
                        '--max', '3', '--out', str(args.out / f'{label}_sheet.png')], check=True)


if __name__ == '__main__':
    main()
