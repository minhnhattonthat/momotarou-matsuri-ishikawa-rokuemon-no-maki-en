"""Find which disc files (or parts) are resident in a PS1 RAM dump.

usage: python tools/ramfind.py RAM.bin [FILE_GLOB ...]
For each file, probe 256-byte windows every 2 KB (skipping low-entropy ones) and report where they sit in RAM,
as the load base (RAM address of file offset 0) that most windows agree on.
"""
import collections, glob, os, sys


def bases(ram, d, step=0x800, win=256):
    c = collections.Counter()
    for off in range(0, max(1, len(d) - win), step):
        k = d[off:off + win]
        if len(set(k)) < 24:
            continue
        i = ram.find(k)
        if i >= 0 and ram.find(k, i + 1) < 0:
            c[0x80000000 + i - off] += 1
    return c


def main():
    ram = open(sys.argv[1], 'rb').read()
    pats = sys.argv[2:] or ['work/disc/tree/OUTBIN/*.BIN', 'work/disc/tree/SLPM_868.88']
    for p in pats:
        for f in sorted(glob.glob(p)):
            d = open(f, 'rb').read()
            c = bases(ram, d)
            if c:
                b, n = c.most_common(1)[0]
                print(f'{os.path.basename(f):16} size {len(d):7x} base {b:08x} windows {n}/{len(d) // 0x800 + 1}')


if __name__ == '__main__':
    main()
