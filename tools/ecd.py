"""ECD compression (docs/re/disc.md): the game's LZSS, decoder at EXE 0x80024834.

Header 16 bytes: b'ECD\\x01', then big-endian u32 raw (bytes stored uncompressed first, outside the ring),
u32 csize (stream bytes after the header, raw prefix included), u32 usize (decompressed size).
Stream: flag byte LSB-first, 1 = literal, 0 = 2-byte reference: ring position = b0 | (b1 & 0xC0) << 2,
length = (b1 & 0x3F) + 3. Ring 1024 bytes zero-filled, first write at 0x3BE.
"""
import struct

MAGIC = b'ECD\x01'
N, START, MAXLEN = 1024, 0x3BE, 0x3F + 3


def header(d, off=0):
    if d[off:off + 4] != MAGIC:
        raise ValueError('not ECD')
    return struct.unpack_from('>3I', d, off + 4)  # raw, csize, usize


def decompress(d, off=0):
    raw, csize, usize = header(d, off)
    src = d[off + 16:off + 16 + csize]
    out = bytearray(src[:raw])
    ring = bytearray(N)
    r = START
    i = raw
    while i < len(src) and len(out) < usize:
        flags = src[i]; i += 1
        for bit in range(8):
            if i >= len(src) or len(out) >= usize:
                break
            if flags >> bit & 1:
                c = src[i]; i += 1
                out.append(c); ring[r] = c; r = (r + 1) & (N - 1)
            else:
                b0, b1 = src[i], src[i + 1]; i += 2
                p = b0 | (b1 & 0xC0) << 2
                for k in range((b1 & 0x3F) + 3):
                    c = ring[(p + k) & (N - 1)]
                    out.append(c); ring[r] = c; r = (r + 1) & (N - 1)
    if len(out) != usize:
        raise ValueError(f'ECD size mismatch {len(out)} != {usize}')
    return bytes(out)


def compress(data, raw=0):
    """Greedy hash-chain encoder: decompress(compress(x)) == x, but not byte-identical to the original
    tool, so the build recompresses only entries it changed."""
    data = bytes(data)
    body = data[raw:]
    out = bytearray(data[:raw])
    chains = {}
    j, n = 0, len(body)

    def add(s):
        if s + 3 <= n:
            chains.setdefault(body[s:s + 3], []).append(s)

    while j < n:
        flags_at = len(out); out.append(0); flags = 0
        for bit in range(8):
            if j >= n:
                break
            best, pos = 0, 0
            for s in reversed(chains.get(body[j:j + 3], [])[-48:]):
                if j - s >= N:  # older than the ring
                    break
                L = 0
                while L < MAXLEN and j + L < n and body[s + L] == body[j + L]:
                    L += 1
                if L > best:
                    best, pos = L, (START + s) & (N - 1)
                    if L == MAXLEN:
                        break
            if best < MAXLEN and j + 3 < N and body[j] == 0:
                # never-written ring cells are zero: read just ahead of the write position
                L = 0
                while L < MAXLEN and j + L < n and body[j + L] == 0 and j + 1 + L < N:
                    L += 1
                if L > best:
                    best, pos = L, (START + j + 1) & (N - 1)
            if best >= 3:
                out += bytes([pos & 0xFF, (pos >> 2 & 0xC0) | (best - 3)])
            else:
                best = 1
                flags |= 1 << bit
                out.append(body[j])
            for t in range(best):
                add(j + t)
            j += best
        out[flags_at] = flags
    return MAGIC + struct.pack('>3I', raw, len(out), len(data)) + bytes(out)


if __name__ == '__main__':
    import sys
    d = open(sys.argv[1], 'rb').read()
    print(header(d, int(sys.argv[2], 0) if len(sys.argv) > 2 else 0))
