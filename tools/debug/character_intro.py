"""Cold, input-free attract sequence: all five full character pictures and names.

    python tools/debug/character_intro.py --out work/qa/names8_final
    python tools/debug/character_intro.py --original --out work/qa/names8_original

The game itself transitions from the title to the introductions. No mode,
sprite, palette, position or story flag is substituted. A name and its complete
character must match in the SAME screenshot. The whole picture remains subject
to visual review (including Japanese emblems outside the name-label scope).
"""
import argparse
import csv
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

CHARACTERS = ('Momotaro', 'Kintaro', 'Urashima', 'Yashahime', 'Ishikawa Rokuemon')


def check(out, original=False):
    raw = (gfx.TREE / 'CHR0D.BIN').read_bytes()
    archive = arc.entries(raw if original else gfx.apply('CHR0D.BIN', raw))
    rows = []
    shots = sorted(out.glob('f[0-9]*.png'))
    for entry, name in enumerate(CHARACTERS, 5):
        templates = out / 'templates' / str(entry)
        anm.render(archive, anm.items(archive[entry][1]), templates, strict=True)
        art = Image.open(templates / '000.png').convert('RGBA')
        label = Image.open(templates / '001.png').convert('RGBA')
        found, art_at, label_at = '', None, None
        for path in shots:
            with Image.open(path) as image:
                screen = image.convert('RGB')
            label_at = match(screen, label)
            if label_at is not None:
                art_at = match(screen, art)
                if art_at is not None:
                    found = path.as_posix()
                    break
        rows.append((name, 'ok' if found else 'missing', found, art_at, label_at))
    with (out / 'coverage.tsv').open('w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter='\t', lineterminator='\n')
        writer.writerow(('character', 'status', 'shot', 'art_position', 'name_position'))
        writer.writerows(rows)
    print(f'{sum(row[1] == "ok" for row in rows)}/5 complete character/name pairs')
    for row in rows:
        print(*row, sep='\t')
    return all(row[1] == 'ok' for row in rows)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--original', action='store_true')
    ap.add_argument('--cue', type=Path)
    ap.add_argument('--check-only', action='store_true')
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    if not args.check_only:
        cue = args.cue or ROOT / ('rom/Momotarou Matsuri - Ishikawa Rokuemon no Maki (Japan).cue'
                                  if args.original else 'build/momotarou-matsuri_en.cue')
        result = subprocess.run([
            sys.executable, '-X', 'utf8', str(Path(SKILL) / 'scripts/emu.py'), str(cue),
            '--out', str(args.out), '--frames', '9600', '--shot-every', '60', '--timeout', '180',
            '--script', str(ROOT / 'tools/lua/textlog.lua'),
        ])
        if result.returncode:
            return result.returncode
    return 0 if check(args.out, args.original) else 1


if __name__ == '__main__':
    raise SystemExit(main())
