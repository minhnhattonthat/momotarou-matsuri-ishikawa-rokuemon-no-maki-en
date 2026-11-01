"""Cold native op-26 renders of all 27 extracted location captions.

Uses warp.lua's existing OPS interface, not a replacement text renderer. The
caption is shown over the opening field before changing maps; this is caption
layout coverage, not proof of every destination's story state or entrance.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import csv
from pathlib import Path
import re
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
import insert  # noqa: E402
import layout  # noqa: E402
import text  # noqa: E402
import textlog  # noqa: E402
import windows  # noqa: E402
from skill import SKILL  # noqa: E402


def check_capture(log, value, width):
    """Require the intended complete line at the centred native coordinates."""
    match = re.search(r'^CAPTION x=(\d+) y=(\d+) glyphs=(\d+) f\d+$', log, re.M)
    if not match:
        return 'missing', '', '', ''
    x, y, glyphs = map(int, match.groups())
    lines = [textlog.LINE.match(line) for line in log.splitlines()]
    exact = any(m and int(m[2]) == x and int(m[3]) == y and textlog.decode(m[4]) == value
                for m in lines)
    status = 'ok' if exact and x == 160 - width // 2 and y == 60 and width <= 116 else 'wrong text/position'
    return status, x, y, glyphs


def run(row, variant, args):
    iid = row['id']
    out = args.out / iid.replace('/', '_')
    out.mkdir(parents=True, exist_ok=True)
    rendered, errors = layout.render(row, variant)
    assert not errors, errors
    value = row['jp'] if args.original else rendered
    data = struct.pack('<H', 0x26) + text.text_bytes(0x26, [value])
    ops = '{' + ','.join(str(w) for w in struct.unpack(f'<{len(data) // 2}H', data)) + '}'
    if not args.check_only:
        shot = out / 'caption.png'
        if shot.exists():
            shot.unlink()
        cue = ROOT / ('rom/Momotarou Matsuri - Ishikawa Rokuemon no Maki (Japan).cue' if args.original
                      else 'build/momotarou-matsuri_en.cue')
        command = [sys.executable, '-X', 'utf8', str(Path(SKILL) / 'scripts/emu.py'), str(cue),
                   '--out', str(out), '--script', str(ROOT / 'tools/debug/warp.lua'),
                   '--script', str(ROOT / 'tools/debug/caption_capture.lua'),
                   '--script', str(ROOT / 'tools/lua/textlog.lua'),
                   '--var', "SCENE='map_gv0000_037'", '--var', 'OPS=' + ops,
                   '--var', 'WARP_CLOSE_DELAY=60', '--var', 'HOLD=60', '--frames', '1', '--timeout', '150']
        result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
        (out / 'harness.log').write_text(result.stdout + result.stderr, encoding='utf-8')
        if result.returncode:
            return (iid, value, 'emulator failed', '', '', '')
    log = (out / 'log.txt').read_text(encoding='utf-8')
    if not (out / 'caption.png').exists():
        return (iid, value, 'missing', '', '', '')
    width = len(text.encode_text(value)) * 6 if args.original else layout.width(value)
    return (iid, value, *check_capture(log, value, width))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--original', action='store_true')
    ap.add_argument('--only', default='')
    ap.add_argument('--jobs', type=int, default=2)
    ap.add_argument('--check-only', action='store_true')
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    rows = [r for group in insert.rows_by_file().values() for r in group
            if r['kind'] == 'caption' and args.only in r['id']]
    variants = windows.variants()
    with ThreadPoolExecutor(args.jobs) as pool:
        results = list(pool.map(lambda row: run(row, variants[row['id']], args), rows))
    with (args.out / 'coverage.tsv').open('w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter='\t', lineterminator='\n')
        writer.writerow(('id', 'caption', 'status', 'x', 'y', 'glyphs'))
        writer.writerows(results)
    failed = [r for r in results if r[2] != 'ok']
    for row in failed:
        print(row)
    print(f'{len(rows) - len(failed)}/{len(rows)} cold native captions')
    return bool(failed)


if __name__ == '__main__':
    raise SystemExit(main())
