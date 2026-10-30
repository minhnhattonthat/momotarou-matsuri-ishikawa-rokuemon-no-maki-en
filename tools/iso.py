"""List files of a MODE2/2352 PS1 disc image: name, LBA, size (ISO9660 directory records).

usage: python tools/iso.py IMAGE.bin
"""
import struct, sys

SECTOR, DATA = 2352, 24  # MODE2 form 1: user data at +24


def sector(f, lba):
    f.seek(lba * SECTOR + DATA)
    return f.read(2048)


def walk(f, lba, size, path=''):
    out = []
    data = b''.join(sector(f, lba + i) for i in range((size + 2047) // 2048))
    i = 0
    while i < len(data):
        n = data[i]
        if n == 0:
            i = (i // 2048 + 1) * 2048
            continue
        ext = struct.unpack_from('<I', data, i + 2)[0]
        ln = struct.unpack_from('<I', data, i + 10)[0]
        flags = data[i + 25]
        nl = data[i + 32]
        name = data[i + 33:i + 33 + nl]
        if name not in (b'\0', b'\1'):
            nm = name.decode('ascii').split(';')[0]
            if flags & 2:
                out += walk(f, ext, ln, path + nm + '/')
            else:
                out.append((path + nm, ext, ln))
        i += n
    return out


def files(image):
    with open(image, 'rb') as f:
        pvd = sector(f, 16)
        root = pvd[156:156 + 34]
        return walk(f, struct.unpack_from('<I', root, 2)[0], struct.unpack_from('<I', root, 10)[0])


if __name__ == '__main__':
    for name, lba, size in sorted(files(sys.argv[1]), key=lambda x: x[1]):
        print(f'{lba:6d} {size:9d} {name}')
