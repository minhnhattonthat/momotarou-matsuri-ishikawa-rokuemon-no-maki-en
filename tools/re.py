"""MIPS recon helpers for this game's code files (EXE and overlays).

usage:
  python -X utf8 tools/re.py dis FILE ADDR [COUNT]      disassemble (FILE = exe or OVL*.BIN name)
  python -X utf8 tools/re.py imm FILE HEX [HEX ...]     instructions whose 16-bit immediate is one of the values
Code files and load addresses (verified from RAM dumps, docs/re/disc.md):
  SLPM_868.88 -> 0x80010000 (after the 0x800 header); every OUTBIN/OVL*.BIN -> 0x800CB338.
"""
import os, sys
import capstone

TREE = os.path.join(os.path.dirname(__file__), '..', 'work', 'disc', 'tree')
OVL_BASE = 0x800CB338


def load(name):
    if name.upper().startswith('SLPM'):
        d = open(os.path.join(TREE, 'SLPM_868.88'), 'rb').read()
        return d[0x800:], 0x80010000
    p = name if os.path.exists(name) else os.path.join(TREE, 'OUTBIN', name)
    return open(p, 'rb').read(), OVL_BASE


def md():
    m = capstone.Cs(capstone.CS_ARCH_MIPS, capstone.CS_MODE_MIPS32 + capstone.CS_MODE_LITTLE_ENDIAN)
    m.skipdata = True  # data words inside code files would otherwise stop disassembly
    return m


def dis(name, addr, count=40):
    d, base = load(name)
    off = addr - base
    for ins in md().disasm(d[off:off + count * 4], addr):
        print(f'{ins.address:08X}  {ins.mnemonic:8} {ins.op_str}')


def imm(name, vals):
    d, base = load(name)
    m = md()
    for i in range(0, len(d) - 3, 4):
        w = int.from_bytes(d[i:i + 4], 'little')
        op = w >> 26
        if op in (8, 9, 10, 11, 12, 13, 14, 4, 5, 0x20, 0x21, 0x23, 0x24, 0x25, 0x28, 0x29, 0x2B) and (w & 0xFFFF) in vals:
            for ins in m.disasm(d[i:i + 4], base + i):
                print(f'{ins.address:08X}  {ins.mnemonic:8} {ins.op_str}')


def switches(name):
    """Jump-table switches: sltiu rX, rY, N ... lui/addiu table ... jr. Prints site, case count, table address."""
    d, base = load(name)
    ins = list(md().disasm(d, base))
    for k, i in enumerate(ins):
        if i.mnemonic != 'jr' or i.op_str == '$ra':
            continue
        n = hi = tbl = None
        for j in ins[max(0, k - 12):k]:
            if j.mnemonic == 'sltiu':
                n = int(j.op_str.split(',')[-1], 0)
            elif j.mnemonic == 'lui':
                hi = int(j.op_str.split(',')[-1], 0)
            elif j.mnemonic == 'addiu' and hi is not None and tbl is None:
                lo = int(j.op_str.split(',')[-1], 0)
                tbl = ((hi << 16) + lo) & 0xFFFFFFFF
        if n and tbl:
            print(f'{i.address:08X}  cases {n:4}  table {tbl:08X}')


if __name__ == '__main__':
    a = sys.argv
    if a[1] == 'dis':
        dis(a[2], int(a[3], 16), int(a[4]) if len(a) > 4 else 40)
    elif a[1] == 'imm':
        imm(a[2], {int(x, 16) for x in a[3:]})
    elif a[1] == 'switches':
        switches(a[2])
