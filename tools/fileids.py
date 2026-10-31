"""Game file ids -> disc file names, from the EXE LBA table (docs/re/disc.md: EXE 0x6F1B0, 1,606 {start, end} pairs).

The loader (EXE 0x8001C334) takes two id forms (verified: slot ids on the field match its map table's files):
  - 0x2710 + n: table index n (code overlays: the mode switch loads 0x2710 + 2 = OVLGMAIN);
  - data id d < 0x2710: table index d + 63 (loaded-file slots 0x800A3DE0, scripts, map tables use this form).

usage: python tools/fileids.py [--data] [ID|NAME ...]     no ids: the whole list (index, data id, name)
"""
import os, struct, sys

sys.path.insert(0, os.path.dirname(__file__))
import iso

ROOT = os.path.join(os.path.dirname(__file__), '..')
EXE = os.path.join(ROOT, 'work', 'disc', 'tree', 'SLPM_868.88')
TABLE, COUNT, DATA = 0x6F1B0, 1606, 63


def names(image=None):
    """Names by table index."""
    image = image or os.path.join(ROOT, 'rom', 'Momotarou Matsuri - Ishikawa Rokuemon no Maki (Japan).bin')
    by_lba = {lba: name.split('/')[-1] for name, lba, _ in iso.files(image)}
    exe = open(EXE, 'rb').read()
    return [by_lba[struct.unpack_from('<I', exe, TABLE + 8 * i)[0]] for i in range(COUNT)]


def data_name(n, d):
    """Name of data id d (as stored in slots and script tables), given names()."""
    return n[d + DATA] if 0 <= d + DATA < len(n) else f'?{d}'


if __name__ == '__main__':
    n = names()
    args = sys.argv[1:]
    data = '--data' in args
    args = [a for a in args if a != '--data']
    for i, nm in enumerate(n):
        d = i - DATA
        keys = {nm, str(d) if data else str(i)}
        if not args or keys & set(args):
            print(f'{i:5d} data {d:5d} {nm}')
