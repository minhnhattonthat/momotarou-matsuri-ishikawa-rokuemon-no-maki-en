"""Script VM bytecode: op lengths, message text, branch offsets (docs/re/script.md).

An op is u16 words: the opcode, then operands. Op 0x02 (message) is followed by text lines: u16 units ended by
a u16 0; the message ends after a line whose last unit is not KG or KP (KN, or an empty line). Ops 0x0D-0x13 are
conditional jumps whose last operand is a byte offset from the op's own start (`& 0xFFFE`, forward only).

usage: python -X utf8 tools/script.py FILE ENTRY        disassemble one archive entry
"""
import struct
import sys

KG, KP, KN = 0x474B, 0x504B, 0x4E4B

# fixed op lengths in bytes (EXE handler table 0x800830D0; tools/ophandlers.py summaries)
LEN = {
    0x00: 2, 0x01: 4, 0x03: 4, 0x04: 6, 0x14: 2, 0x16: 2, 0x17: 4, 0x18: 8, 0x19: 4,
    0x1A: 12, 0x1B: 8, 0x1C: 2, 0x1D: 12, 0x1E: 4, 0x1F: 16, 0x20: 2, 0x30: 6, 0x32: 2, 0x3B: 2, 0x43: 4, 0x21: 12, 0x22: 2, 0x23: 4, 0x24: 4,
    0x25: 12, 0x27: 6, 0x28: 2, 0x29: 2, 0x2A: 2, 0x2B: 6, 0x2C: 6, 0x2D: 10, 0x2E: 2, 0x2F: 6,
    0x31: 6, 0x34: 2, 0x35: 2, 0x37: 4, 0x38: 8, 0x39: 4, 0x3A: 6, 0x3C: 4, 0x3D: 6, 0x3E: 6,
    0x40: 4, 0x42: 6, 0x44: 4, 0x45: 4, 0x46: 6, 0x47: 6, 0x48: 6, 0x49: 4, 0x4A: 4, 0x4B: 6,
    0x4C: 6, 0x4D: 8, 0x4E: 4, 0x4F: 4, 0x50: 6, 0x51: 4, 0x52: 4, 0x53: 4, 0x54: 4, 0x55: 8,
    0x56: 4, 0x57: 8, 0x58: 4, 0x59: 4, 0x5A: 2, 0x5B: 6, 0x5C: 6, 0x5D: 6, 0x5E: 2, 0x5F: 2,
    0x60: 8, 0x61: 4, 0x62: 4, 0x63: 2, 0x64: 2, 0x65: 2, 0x66: 10, 0x67: 4, 0x68: 4,
}
for _op in range(0x05, 0x0B):
    LEN[_op] = 10
LEN[0x0B] = LEN[0x0C] = 2
for _op in range(0x0D, 0x14):
    LEN[_op] = 8
BRANCH = range(0x0D, 0x14)
IF = range(0x05, 0x0B)


def jumps(d, o, op):
    """[(byte position of the offset word, target offset)] for op at o.

    0D-13 `op var val off`: if the test holds, go to o + off (handler 0x8002D2C0).
    05-0A `op var val else end` (if-block, tested a frame later by 0x8002CFD8): when the test fails, go to
    o + else + 2 (else != 0xFFFF) or o + end + 2: else/end point at the 0B / 0C marker word ending each part.
    0B (else marker) goes to the enclosing 05-0A op's end + 2; 0C (end marker) falls through.
    """
    if op in BRANCH:
        return [(o + 6, o + (u16(d, o + 6) & 0xFFFE))]
    if op in IF:
        return [(o + k, o + (u16(d, o + k) & 0xFFFE) + 2) for k in (6, 8) if u16(d, o + k) != 0xFFFF]
    return []
# no fall-through: 00 end, 1E/30/32/43 switch to another script, 3B restart this one
END = {0x00, 0x1E, 0x30, 0x32, 0x3B, 0x43}


class ParseError(Exception):
    pass


def u16(d, o):
    if o + 2 > len(d):
        raise ParseError(f'read past end at {o:#x}')
    return struct.unpack_from('<H', d, o)[0]


def line_end(d, o):
    """End of one text line at o: u16 units through the first unit whose low byte is 0 (0x80029DF4, op 41)."""
    while True:
        w = u16(d, o)
        o += 2
        if w & 0xFF == 0:
            return o


def text_end(d, o):
    """End offset of the message text starting at o (after op 0x02's operands)."""
    while True:
        e = line_end(d, o)
        last = u16(d, e - 4) if e - o >= 4 else None
        o = e
        if last not in (KG, KP):
            return o


def op_len(d, o):
    op = u16(d, o)
    if op == 0x02:
        return text_end(d, o + 6) - o
    if op == 0x26:  # one caption line
        return line_end(d, o + 2) - o
    if op == 0x41:  # menu: n item lines
        e = o + 4
        for _ in range(u16(d, o + 2)):
            e = line_end(d, e)
        return e - o
    if op == 0x15:
        return 4 + 6 * u16(d, o + 2)
    if op == 0x33:
        return 4 + 12 * u16(d, o + 2)
    if op == 0x3F:
        return 4 + 10 * u16(d, o + 2)
    if op == 0x36:  # records {type, a, ...}: 8 words when type is 3, else 4
        e = o + 4
        for _ in range(u16(d, o + 2)):
            e += 16 if u16(d, e) == 3 else 8
        return e - o
    if op in LEN:
        return LEN[op]
    raise ParseError(f'op {op:#04x} at {o:#x}: length unknown')


def ops(d, start=0, stop=None):
    """Yield (offset, opcode, length) walking linearly from start until stop (or end of d)."""
    stop = len(d) if stop is None else stop
    o = start
    while o < stop:
        n = op_len(d, o)
        yield o, u16(d, o), n
        o += n
    if o != stop:
        raise ParseError(f'walk overran the end: {o:#x} > {stop:#x}')


def show(d):
    for o, op, n in ops(d):
        words = [u16(d, o + k) for k in range(0, n, 2)]
        if op == 0x02:
            args = ' '.join(f'{w:04X}' for w in words[1:3])
            text = d[o + 6:o + n].replace(b'\x00\x00', b'|').replace(b'\x00', b'').decode('cp932', 'replace')
            print(f'{o:05X}  02 {args}  {text}')
        else:
            extra = ''.join(f'  -> {t:05X}' for _, t in jumps(d, o, op))
            print(f'{o:05X}  ' + ' '.join(f'{w:04X}' for w in words) + extra)


if __name__ == '__main__':
    import arc
    d = open(sys.argv[1], 'rb').read()
    show(arc.entries(d)[int(sys.argv[2])][1])
