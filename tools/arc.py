"""OUTBIN offset-table archives (docs/re/disc.md).

Header: u32 LE offsets, the first equals the header size; zero words pad the header. Entry i runs from offs[i]
to the next offset (or end of file). Many archives end on a 16-byte b'end\\x1a' entry.
"""
import struct


def offsets(d):
    """Entry offsets, or None if d does not look like an archive."""
    if len(d) < 8:
        return None
    hs = struct.unpack_from('<I', d)[0]
    if hs < 4 or hs % 4 or hs > len(d) or hs > 0x10000:
        return None
    offs = []
    for i in range(0, hs, 4):
        o = struct.unpack_from('<I', d, i)[0]
        if o == 0:
            if any(struct.unpack_from('<I', d, k)[0] for k in range(i, hs, 4)):
                return None  # zero inside the table: not this format
            break
        if o > len(d) or (offs and o < offs[-1]):
            return None
        offs.append(o)
    return offs


def entries(d):
    offs = offsets(d)
    if offs is None:
        return None
    ends = offs[1:] + [len(d)]
    return [(o, d[o:e]) for o, e in zip(offs, ends)]
