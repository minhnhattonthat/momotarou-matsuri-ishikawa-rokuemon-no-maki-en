"""Cold native menu titles, verified against ANM/TIM pixels from the named disc.

python tools/debug/menu_titles.py --out work/qa/menu_titles8_en [--original]

The saved-Status Details route uses Game Album on the original too. This does
not claim a natural consumer for the separate Rank Details atlas label.
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

CASES = {
    'album': ('YUGI0D.BIN', 4, 1, 0x4F, None),
    'saved_details': ('YUGI0D.BIN', 4, 1, 0x4F, None),
    'quick': ('PREM0D.BIN', 10, 7, 0x50, 'trial_menu'),
    'name': ('NAME0D.BIN', 4, 8, 0x51, 'name_entry'),
}


def archives(image):
    result = {}
    wanted = {row[0] for row in CASES.values()}
    with image.open('rb') as disc:
        for path, lba, size in iso.files(str(image)):
            name = Path(path).name
            if name in wanted:
                data = b''.join(iso.sector(disc, lba + i) for i in range((size + 2047) // 2048))[:size]
                result[name] = arc.entries(data)
    assert set(result) == wanted, 'menu archives missing from named disc'
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--original', action='store_true')
    ap.add_argument('--cue', type=Path)
    ap.add_argument('--save', type=Path, default=ROOT / 'work/qa/save_fixture_checked/memcard1.mcd')
    ap.add_argument('--only', nargs='+', choices=CASES, default=list(CASES))
    ap.add_argument('--check-only', action='store_true')
    args = ap.parse_args()
    cue = (args.cue or ROOT / ('rom/Momotarou Matsuri - Ishikawa Rokuemon no Maki (Japan).cue'
                              if args.original else 'build/momotarou-matsuri_en.cue')).resolve()
    image = cue.with_suffix('.bin')
    sources = archives(image)
    digest = hashlib.sha1(image.read_bytes()).hexdigest()
    rows = []
    for name in args.only:
        archive_name, entry, item, mode, scene = CASES[name]
        out = args.out / name
        out.mkdir(parents=True, exist_ok=True)
        if not args.check_only:
            # Custom shots/logs survive emu.py's numbered-frame cleanup.
            for filename in ('title.png', 'status_before.png', 'log.txt', 'disc.sha1'):
                (out / filename).unlink(missing_ok=True)
            command = [sys.executable, '-X', 'utf8', str(Path(SKILL) / 'scripts/emu.py'), str(cue),
                       '--out', str(out), '--script', str(ROOT / 'tools/debug/menu_titles.lua'),
                       '--script', str(ROOT / 'tools/lua/textlog.lua'), '--var', f"TITLE_CASE='{name}'",
                       '--timeout', '180']
            before = args.save.read_bytes() if not scene else None
            if scene:
                command += ['--script', str(ROOT / 'tools/debug/warp.lua'), '--var', f"SCENE='{scene}'",
                            '--var', 'HOLD=-1', '--frames', '20000']
            else:
                command += ['--route', str(ROOT / 'tools/routes/status_saved.txt'), '--sav', str(args.save)]
            run = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
            (out / 'harness.log').write_text(run.stdout + run.stderr, encoding='utf-8')
            if before is not None:
                assert args.save.read_bytes() == before, 'source card changed'
            if run.returncode:
                print(run.stdout + run.stderr)
                return run.returncode
            (out / 'disc.sha1').write_text(digest + '\n', encoding='ascii')
        assert (out / 'disc.sha1').read_text().strip() == digest, 'captures belong to a different disc'
        archive = sources[archive_name]
        # The menu object draws these items opaque. Strip the ANM blend hint;
        # require every resulting colour to match the actual capture below.
        records = [(r[0] & ~0x7000, *r[1:]) for r in anm.items(archive[entry][1])[item]]
        textures = [(offset, data if i == 0 else b'') for i, (offset, data) in enumerate(archive)]
        anm.render(textures, [records], out / 'templates', strict=True)
        log = (out / 'log.txt').read_text(encoding='utf-8')
        event = re.search(rf'^MENU_TITLE {name} mode={mode} context=(\d+) state=1 f(\d+)$', log, re.M)
        position = None
        if event and (out / 'title.png').exists():
            with Image.open(out / 'title.png') as shot, Image.open(out / 'templates/000.png') as template:
                position = match(shot.convert('RGB'), template.convert('RGBA'), (0, 0, 320, 48))
        rows.append((name, 'ok' if position is not None else 'missing', archive_name, entry, item,
                     event.group(1) if event else '', position, digest))
    with (args.out / 'coverage.tsv').open('w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter='\t', lineterminator='\n')
        writer.writerow(('case', 'status', 'archive', 'entry', 'item', 'context', 'position', 'disc_sha1'))
        writer.writerows(rows)
    for row in rows:
        print(*row, sep='\t')
    return int(any(row[1] != 'ok' for row in rows))


if __name__ == '__main__':
    raise SystemExit(main())
