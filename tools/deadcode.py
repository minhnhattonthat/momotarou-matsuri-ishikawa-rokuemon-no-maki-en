"""EXE functions nothing calls: candidates for hook space (docs/re/engine.md).

usage: python -X utf8 tools/deadcode.py [MIN_BYTES]

A function start = the word after a `jr $ra` + delay slot that begins with `addiu $sp, $sp, -N` (or any word
after jr ra + nop padding). Reached = a jal/j target in the EXE or any overlay, a 32-bit word equal to its address
anywhere in a code file, or a lui/addiu pair building it (codestr.refs). Prints unreached starts with their size
(to the next start). A guess list: confirm with an exec watch before writing over one.
"""
import struct
import sys

sys.path.insert(0, __file__.rsplit('\\', 1)[0].rsplit('/', 1)[0])
import codestr  # noqa: E402

EXE_TEXT_END = 0x80080000  # code ends before the data tables (glyph table 0x80081BE0)


def main(minb=64):
    files = codestr.code_files()
    d, base, _ = codestr.image(files[0])
    n = (EXE_TEXT_END - base) // 4
    w = struct.unpack_from(f'<{n}I', d)
    starts = []
    for i in range(2, n):
        if w[i - 2] == 0x03E00008 and (w[i] >> 16) == 0x27BD and w[i] & 0x8000:
            starts.append(base + 4 * i)
    reached = set()
    for p in files:
        dd, bb, _ = codestr.image(p)
        ww = struct.unpack_from(f'<{len(dd) // 4}I', dd)
        for i, x in enumerate(ww):
            if x >> 26 in (2, 3):
                reached.add((bb + 4 * i) & 0xF0000000 | (x & 0x3FFFFFF) << 2)
            reached.add(x)
        reached.update(codestr.refs(dd, bb))
    total = 0
    for k, s in enumerate(starts):
        e = starts[k + 1] if k + 1 < len(starts) else EXE_TEXT_END
        if s not in reached and e - s >= minb:
            print(f'{s:08X} {e - s:5}')
            total += e - s
    print('total', total)


if __name__ == '__main__':
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 64)
