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


def pack(ents, header_size):
    """Archive bytes from entry bytes: header of header_size bytes (offsets, zero padded), each entry padded
    with zeros to 16 bytes, so the last entry (usually end\\x1a) keeps its alignment."""
    if 4 * len(ents) > header_size:
        raise ValueError('header too small')
    out, offs = bytearray(header_size), []
    for e in ents:
        offs.append(len(out))
        out += e + bytes(-len(e) % 16)
    struct.pack_into(f'<{len(offs)}I', out, 0, *offs)
    return bytes(out)


def entries(d):
    offs = offsets(d)
    if offs is None:
        return None
    ends = offs[1:] + [len(d)]
    return [(o, d[o:e]) for o, e in zip(offs, ends)]
