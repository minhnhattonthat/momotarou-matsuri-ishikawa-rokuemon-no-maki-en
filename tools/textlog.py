"""Summarise tools/lua/textlog.lua logs: Japanese still drawn, and which marker numbers showed up.

    python -X utf8 tools/textlog.py DIR [--all]     DIR = a warp_all/emu.py output (log.txt files below it)

Prints, per scene, every drawn line that still holds Japanese glyphs (decoded), then marker coverage against
work/markers.tsv (`<n>` prefixes, phase 5 marker build). Exit 1 if any Japanese line was drawn.
Glyphs that are fine in English text (digits, ○×△□ and arrows, punctuation) don't count as Japanese.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINE = re.compile(r'TEXT f(\d+) (\d+),(\d+) (.*)')
GLYPH = re.compile(r'\{([0-9A-F]{4})\}')
OK = set('０１２３４５６７８９　○×□△◎▽↑→↓←！？・…～ー－＋：（）「」')


def decode(t):
    return GLYPH.sub(lambda m: bytes.fromhex(m.group(1)).decode('cp932', 'replace'), t)


def scan(root):
    root = Path(root)
    out = {}
    for log in sorted(root.rglob('log.txt')):
        rows = []
        for line in log.read_text(encoding='utf-8', errors='replace').splitlines():
            m = LINE.match(line)
            if m:
                rows.append((int(m.group(1)), int(m.group(2)), int(m.group(3)), m.group(4)))
        if rows:
            # Nested case/attempt directories often reuse the same leaf name.
            # A leaf-only key silently lost earlier logs, including JP findings.
            out[log.parent.relative_to(root).as_posix()] = rows
    return out


def japanese(t):
    s = decode(t)
    return any(c not in OK and ord(c) >= 0x3000 for c in s)


def main(root, show_all=False):
    logs = scan(root)
    seen, bad = set(), 0
    for scene, rows in logs.items():
        jp = [(f, x, y, decode(t)) for f, x, y, t in rows if japanese(t)]
        seen |= {int(n) for *_, t in rows for n in re.findall(r'<(\d+)>', t)}
        if jp:
            bad += len(jp)
            print(f'{scene}: {len(jp)} Japanese lines')
            for f, x, y, t in jp if show_all else jp[:8]:
                print(f'   f{f} {x},{y} {t}')
    mk = ROOT / 'work' / 'markers.tsv'
    if mk.exists():
        total = sum(1 for _ in mk.open(encoding='utf-8')) - 1
        print(f'markers seen: {len(seen)} of {total}')
    print(f'{bad} Japanese lines in {len(logs)} logs')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1], '--all' in sys.argv))
