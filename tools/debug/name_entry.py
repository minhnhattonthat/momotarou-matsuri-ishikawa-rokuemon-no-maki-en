"""Cold tour of every player-name glyph, editing and confirmation, then records."""
import argparse
from pathlib import Path
import re
import subprocess
import sys

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
import arc  # noqa: E402
import gfx  # noqa: E402
import name_entry as font  # noqa: E402
import tim  # noqa: E402
from skill import SKILL  # noqa: E402
from announcements_qa import match  # noqa: E402


def check_images(out, original):
    data = (gfx.TREE / 'NAME0D.BIN').read_bytes()
    archive = arc.entries(data if original else gfx.apply('NAME0D.BIN', data))
    atlas = tim.image(gfx.unpack(archive[1][1])[0], 0).convert('RGBA')
    rows = []
    for i, (x, y) in enumerate(font.cells()):
        with Image.open(out / f'glyph_{i:02d}.png') as shot:
            screen = shot.convert('RGB')
        expected = atlas.crop((x, y, x + 16, y + 16))
        position = match(screen, expected, (88, 94, 20, 20))
        if not original and font.ALPHABET[i] == ' ':
            # Space is intentionally blank; require no yellow glyph pixels in
            # the established cell. This does not accept another missing glyph.
            cell = screen.crop((90, 95, 106, 111))
            position = (90, 95) if not any(r > 200 and g > 160 and b < 40
                                         for r, g, b in cell.getdata()) else None
        rows.append((i, 'ok' if position else 'missing', position))
    (out / 'coverage.tsv').write_text('id\tstatus\tposition\n' + ''.join(
        f'{i}\t{status}\t{position}\n' for i, status, position in rows), encoding='utf-8')
    missing = [i for i, status, _ in rows if status != 'ok']
    print(f'{80 - len(missing)}/80 complete glyph images; missing={missing}')
    return not missing


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--original', action='store_true')
    ap.add_argument('--short', action='store_true', help='one-character name, finished with Start')
    ap.add_argument('--check-only', action='store_true')
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    if not args.check_only:
        cue = ROOT / ('rom/Momotarou Matsuri - Ishikawa Rokuemon no Maki (Japan).cue' if args.original
                      else 'build/momotarou-matsuri_en.cue')
        command = [sys.executable, '-X', 'utf8', str(Path(SKILL) / 'scripts/emu.py'), str(cue),
                   '--out', str(args.out), '--script', str(ROOT / 'tools/debug/warp.lua'),
                   '--script', str(ROOT / 'tools/debug/name_entry.lua'),
                   '--script', str(ROOT / 'tools/lua/textlog.lua'), '--var', "SCENE='name_entry'",
                   '--var', 'HOLD=-1', '--frames', '900', '--timeout', '360']
        if args.short:
            command += ['--var', 'NAME_SHORT=true']
        result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
        (args.out / 'harness.log').write_text(result.stdout + result.stderr, encoding='utf-8')
        if result.returncode:
            print(result.stdout + result.stderr)
            return result.returncode
    log = (args.out / 'log.txt').read_text(encoding='utf-8')
    if args.short:
        returned = 'NAME_RETURN record=0 ids=25 mode=80' in log
        print(f'one-character Start/confirm/return={returned}')
        return 0 if returned and (args.out / 'record_name.png').exists() else 1
    ids = [int(x) for x in re.findall(r'^NAME_GLYPH (\d+) f\d+$', log, re.M)]
    shots = [args.out / f'glyph_{i:02d}.png' for i in range(80)]
    complete = ids == list(range(80)) and all(p.exists() for p in shots)
    returned = 'NAME_RETURN record=0 ids=0,51,61,66' in log
    edited = 'NAME_BACK slots=' in log and 'NAME_DECLINED slots=' in log
    print(f'{len(ids)}/80 ordered glyphs; shots={complete}; editing={edited}; saved-name return={returned}')
    images = check_images(args.out, args.original) if complete else False
    return 0 if complete and edited and returned and images else 1


if __name__ == '__main__':
    raise SystemExit(main())
