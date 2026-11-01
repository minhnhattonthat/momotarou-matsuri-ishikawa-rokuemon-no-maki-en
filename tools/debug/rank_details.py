"""Cold Rank Details tour: every page, ranks 0-10, native return to Status.

python tools/debug/rank_details.py --out work/qa/details8_final [--original] [--empty]
"""
import argparse
import csv
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from skill import SKILL  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--original', action='store_true')
    ap.add_argument('--empty', action='store_true')
    ap.add_argument('--check-only', action='store_true')
    ap.add_argument('--save', type=Path, default=ROOT / 'work/qa/save_fixture_checked/memcard1.mcd')
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    before = args.save.read_bytes()
    if not args.check_only:
        for pattern in ('detail_*.png', 'status_before.png', 'status_return.png'):
            for shot in args.out.glob(pattern):
                shot.unlink()
        cue = ROOT / ('rom/Momotarou Matsuri - Ishikawa Rokuemon no Maki (Japan).cue' if args.original
                      else 'build/momotarou-matsuri_en.cue')
        cmd = [sys.executable, '-X', 'utf8', str(Path(SKILL) / 'scripts/emu.py'), str(cue),
               '--out', str(args.out), '--route', str(ROOT / 'tools/routes/status_saved.txt'),
               '--sav', str(args.save), '--script', str(ROOT / 'tools/debug/rank_details.lua'),
               '--script', str(ROOT / 'tools/lua/textlog.lua'),
               '--var', f'DETAIL_EMPTY={str(args.empty).lower()}', '--timeout', '360']
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        (args.out / 'harness.log').write_text(result.stdout + result.stderr, encoding='utf-8')
        assert args.save.read_bytes() == before, 'source memory card changed'
        if result.returncode:
            print(result.stdout + result.stderr)
            return result.returncode
    log = (args.out / 'log.txt').read_text(encoding='utf-8')
    pages = [tuple(map(int, row)) for row in re.findall(
        r'^DETAIL_PAGE (\d+) record=(\d+) rank=(\d+) context=4 f\d+$', log, re.M)]
    complete = [p for p, _, _ in pages] == list(range(43))
    ranks = {rank for _, _, rank in pages}
    complete &= ranks == ({0} if args.empty else set(range(11)))
    returned = 'DETAIL_RETURN status cursor=0' in log
    shots = [args.out / f'detail_{i:02d}.png' for i in range(43)]
    shots += [args.out / name for name in ('status_before.png', 'status_return.png')]
    complete &= all(p.exists() for p in shots)
    with (args.out / 'coverage.tsv').open('w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter='\t', lineterminator='\n')
        writer.writerow(('page', 'record', 'rank', 'screenshot'))
        writer.writerows((page, record, rank, f'detail_{page:02d}.png') for page, record, rank in pages)
    print(f'{len(pages)}/43 ordered Rank Details pages; ranks={sorted(ranks)}; return={returned}; shots={complete}')
    return 0 if complete and returned else 1


if __name__ == '__main__':
    raise SystemExit(main())
