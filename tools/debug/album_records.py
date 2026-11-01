"""Cold Game Album tour: 43 pages, populated/empty records, unchanged source card.

python tools/debug/album_records.py --out work/qa/records8_final [--original] [--empty] [--trial]
"""
import argparse
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
    ap.add_argument('--trial', action='store_true', help='six Quick Match record pages')
    ap.add_argument('--check-only', action='store_true')
    ap.add_argument('--save', type=Path, default=ROOT / 'work/qa/save_fixture_checked/memcard1.mcd')
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    before = args.save.read_bytes()
    if not args.check_only:
        for shot in args.out.glob('record_*.png'):
            shot.unlink()
        cue = ROOT / ('rom/Momotarou Matsuri - Ishikawa Rokuemon no Maki (Japan).cue' if args.original
                      else 'build/momotarou-matsuri_en.cue')
        cmd = [sys.executable, '-X', 'utf8', str(Path(SKILL) / 'scripts/emu.py'), str(cue),
               '--out', str(args.out), '--route', str(ROOT / 'tools/routes/status_saved.txt'),
               '--sav', str(args.save), '--script', str(ROOT / 'tools/debug/album_records.lua'),
               '--script', str(ROOT / 'tools/lua/textlog.lua'), '--var', f'ALBUM_EMPTY={str(args.empty).lower()}',
               '--var', f'ALBUM_TRIAL={str(args.trial).lower()}', '--timeout', '360']
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        (args.out / 'harness.log').write_text(result.stdout + result.stderr, encoding='utf-8')
        assert args.save.read_bytes() == before, 'source memory card changed'
        if result.returncode:
            print(result.stdout + result.stderr)
            return result.returncode
    log = (args.out / 'log.txt').read_text(encoding='utf-8')
    pages = [int(n) for n in re.findall(r'^ALBUM_PAGE (\d+) f\d+$', log, re.M)]
    count = 6 if args.trial else 43
    shots = [args.out / f'record_{i:02d}.png' for i in range(count)]
    ok = pages == list(range(count)) and all(p.exists() for p in shots)
    (args.out / 'coverage.tsv').write_text('page\tstatus\tshot\n' + ''.join(
        f'{i}\t{"ok" if i in pages and p.exists() else "missing"}\t{p.as_posix()}\n'
        for i, p in enumerate(shots)), encoding='utf-8')
    print(f'{len(pages)}/{count} ordered pages; all shots present={all(p.exists() for p in shots)}')
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
