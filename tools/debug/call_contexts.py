"""Read-only MIPS direct-call contexts in the original EXE and overlays.

    python tools/debug/call_contexts.py 8001f3ac --contains '$a0, $zero, 8'
    python tools/debug/call_contexts.py 8001e224 --contains 0x15e --immediate 73

Filters apply to the preceding instruction window, NOT register dataflow.
A hit may contain a value overwritten before the call; inspect its delay slot.
No hits cannot rule out indirect calls, tail jumps, or computed addresses.
"""
import argparse
from pathlib import Path
import struct
import sys

import capstone

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import codestr  # noqa: E402


def contexts(target, before=20):
    needle = struct.pack('<I', 0x0c000000 | ((target >> 2) & 0x3ffffff))
    decoder = capstone.Cs(capstone.CS_ARCH_MIPS,
                          capstone.CS_MODE_MIPS32 | capstone.CS_MODE_LITTLE_ENDIAN)
    decoder.skipdata = True
    for path in codestr.code_files():
        data, base, _ = codestr.image(path)
        for offset in range(0, len(data) - 3, 4):
            if data[offset:offset + 4] != needle:
                continue
            if ((base + offset + 4) & 0xf0000000) != (target & 0xf0000000):
                continue
            start = max(0, offset - before * 4)
            block = list(decoder.disasm(data[start:offset + 8], base + start))
            yield Path(path).name, base + offset, block


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('target', type=lambda value: int(value, 16))
    parser.add_argument('--before', type=int, default=20)
    parser.add_argument('--contains', action='append', default=[])
    parser.add_argument('--immediate', type=lambda value: int(value, 0), action='append', default=[])
    args = parser.parse_args()
    if args.before < 0 or args.target % 4:
        parser.error('use a nonnegative window and word-aligned target')
    count = 0
    for name, address, block in contexts(args.target, args.before):
        if not all(any(value in ins.op_str for ins in block) for value in args.contains):
            continue
        immediates = {int(ins.op_str.split(', ')[-1], 0) for ins in block
                      if ins.mnemonic == 'addiu'}
        if args.immediate and not set(args.immediate) & immediates:
            continue
        count += 1
        print(f'{name} call {address:08X}')
        for ins in block:
            print(f'{ins.address:08X}  {ins.mnemonic:8} {ins.op_str}')
    print(f'{count} direct-call contexts; static leads only')


if __name__ == '__main__':
    main()
