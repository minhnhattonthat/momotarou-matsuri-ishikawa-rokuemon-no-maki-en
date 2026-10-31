"""Field map table in OVLGMAIN (0x800E78E4, 364 x 40-byte records), indexed by the current map [0x8008C570].

usage: python -X utf8 tools/maps.py
Prints each record's u16 words and the names of its first two words (data file ids, tools/fileids.py).
"""
import os, struct, sys

sys.path.insert(0, os.path.dirname(__file__))
import fileids

OVL = os.path.join(os.path.dirname(__file__), '..', 'work', 'disc', 'tree', 'OUTBIN', 'OVLGMAIN.BIN')
BASE, TABLE, COUNT, SIZE = 0x800CB338, 0x800E78E4, 364, 40  # record 364 is not a map (word 17 != 0x800E)


def records():
    d = open(OVL, 'rb').read()
    return [d[TABLE - BASE + i * SIZE:TABLE - BASE + (i + 1) * SIZE] for i in range(COUNT)]


if __name__ == '__main__':
    names = fileids.names()
    for i, r in enumerate(records()):
        w = struct.unpack('<20H', r)
        print(f'{i:2d} ' + ' '.join(f'{x:04X}' for x in w) + '  ' +
              ' '.join(fileids.data_name(names, x) for x in w[:2]))
