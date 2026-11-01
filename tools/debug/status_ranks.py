"""Cold saved Status: six naturally selected rank pictures and a counter stress case.

    python tools/debug/status_ranks.py --out work/qa/ranks8_final [--original]

Requires the game-written save from save_fixture.py. Fixture writes only RAM
after load; emu.py copies the memory card. Each case starts from a cold boot.
The expected complete rank plate AND character must match the same screenshot.
"""
import argparse
import csv
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import subprocess
import sys

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
import anm  # noqa: E402
import arc  # noqa: E402
import gfx  # noqa: E402
from skill import SKILL  # noqa: E402
from announcements_qa import match  # noqa: E402

CASES = ((0, 0), (20, 1), (50, 2), (100, 3), (150, 4), (250, 5), (610, 5))


def run(case, args):
    rank, tier = case
    out = args.out / f'rank{rank:03d}'
    out.mkdir(parents=True, exist_ok=True)
    if not args.check_only:
        (out / 'status.png').unlink(missing_ok=True)
        cue = ROOT / ('rom/Momotarou Matsuri - Ishikawa Rokuemon no Maki (Japan).cue' if args.original
                      else 'build/momotarou-matsuri_en.cue')
        cmd = [sys.executable, '-X', 'utf8', str(Path(SKILL) / 'scripts/emu.py'), str(cue),
               '--out', str(out), '--route', str(ROOT / 'tools/routes/status_saved.txt'),
               '--sav', str(args.save), '--script', str(ROOT / 'tools/debug/status_ranks.lua'),
               '--script', str(ROOT / 'tools/lua/textlog.lua'), '--var', f'STATUS_RANK={rank}',
               '--var', f'STATUS_STRESS={str(rank == 610).lower()}', '--timeout', '180']
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        (out / 'harness.log').write_text(result.stdout + result.stderr, encoding='utf-8')
        if result.returncode:
            return rank, tier, 'emulator_failed', '', ''
    raw = (gfx.TREE / 'STATUS0D.BIN').read_bytes()
    archive = arc.entries(raw if args.original else gfx.apply('STATUS0D.BIN', raw))
    template_dir = out / 'templates'
    # Runtime Status objects draw these blend-flagged source records opaque.
    records = [(r[0] & ~0x7000, *r[1:]) for r in anm.items(archive[4][1])[21 + tier]]
    anm.render(archive, [records], template_dir, strict=True)
    shot = out / 'status.png'
    position = None
    if shot.exists():
        with Image.open(shot) as screen, Image.open(template_dir / '000.png') as template:
            position = match(screen.convert('RGB'), template.convert('RGBA'))
    log = (out / 'log.txt').read_text(encoding='utf-8')
    expected = f'STATUS_RESULT rank={rank} tier={tier}'
    status = 'ok' if position is not None and expected in log else 'missing'
    return rank, tier, status, shot.as_posix(), position


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', required=True, type=Path)
    ap.add_argument('--save', type=Path, default=ROOT / 'work/qa/save_fixture_checked/memcard1.mcd')
    ap.add_argument('--original', action='store_true')
    ap.add_argument('--check-only', action='store_true')
    ap.add_argument('--jobs', type=int, default=3)
    args = ap.parse_args()
    before = args.save.read_bytes()
    args.out.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(args.jobs) as pool:
        rows = list(pool.map(lambda case: run(case, args), CASES))
    assert args.save.read_bytes() == before, 'source save changed'
    with (args.out / 'coverage.tsv').open('w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter='\t', lineterminator='\n')
        writer.writerow(('rank', 'tier', 'status', 'shot', 'position'))
        writer.writerows(rows)
    failed = [row for row in rows if row[2] != 'ok']
    print(f'{len(rows) - len(failed)}/{len(rows)} complete rank pictures')
    for row in failed:
        print(row)
    return bool(failed)


if __name__ == '__main__':
    raise SystemExit(main())
