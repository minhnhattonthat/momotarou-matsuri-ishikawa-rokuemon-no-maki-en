"""Summarise tools/lua/heapwatch.lua logs: the least free heap-A bytes per scene, tightest first.

    python -X utf8 tools/heaplog.py DIR [N]       DIR = a warp_all.py --probe tools/lua/heapwatch.lua output
"""
import re
import sys
from pathlib import Path

LINE = re.compile(r'peak=(\d+) top=\w+ start=(\w+) size=(\d+) free=(-?\d+)')


def tightest(log):
    """(free, peak, start, size) with the least free bytes; samples before the heap is set up are skipped."""
    best = None
    for m in LINE.finditer(log.read_text(encoding='utf-8', errors='replace')):
        peak, start, size, free = int(m[1]), int(m[2], 16), int(m[3]), int(m[4])
        if 0x80010000 <= start < 0x80200000 and 0 < size <= 0x200000 and 0 < peak <= size and (best is None or free < best[0]):
            best = (free, peak, start, size)
    return best


if __name__ == '__main__':
    d = Path(sys.argv[1])
    rows = sorted((t, p.parent.name) for p in d.glob('*/log.txt') if (t := tightest(p)))
    for (free, peak, start, size), name in rows[:int(sys.argv[2]) if len(sys.argv) > 2 else 10]:
        print(f'{name:28} free {free:7d}  peak {peak:7d}  heap {start:08X}+{size:#x}')
    print(f'{len(rows)} scenes with heap data')
