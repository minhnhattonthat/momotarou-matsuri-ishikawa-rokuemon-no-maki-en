"""Japanese C strings in code files (EXE, OVL*.BIN) and the references that reach them (docs/re/text.md).

usage: python -X utf8 tools/codestr.py [FILE ...]     summary per file (default: every code file with text)
       python -X utf8 tools/codestr.py --list FILE    every string with its refs

A string is a NUL-terminated byte run holding Japanese (tools/text.py jp_runs), widened to the bytes between
the previous NUL and its own NUL. Refs: 32-bit words equal to its address (pointer tables, data) and
`lui rX,hi` + `addiu/ori rY,rX,lo` pairs (also loads/stores with a lo offset) in code. `cap` = bytes from the
string start to the next string or non-zero byte (room for an in-place replacement, terminator included).
"""
import glob
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(__file__))
import text  # noqa: E402

TREE = text.TREE
EXE_BASE, EXE_HDR, OVL_BASE = 0x80010000, 0x800, 0x800CB338


def code_files():
    return [os.path.join(TREE, 'SLPM_868.88')] + sorted(glob.glob(os.path.join(TREE, 'OUTBIN', 'OVL*.BIN')))


def image(path):
    """(bytes as loaded, load address, file offset of byte 0)."""
    d = open(path, 'rb').read()
    if os.path.basename(path).startswith('SLPM'):
        return d[EXE_HDR:], EXE_BASE, EXE_HDR
    return d, OVL_BASE, 0


def is_jp(raw):
    """A whole string of printable Shift-JIS with at least two full-width characters (single ones were all
    instruction bytes that happen to decode, e.g. 拍)."""
    if not raw or min(raw) < 0x20 or max(raw) > 0xFC:
        return False
    try:
        s = raw.decode('cp932')
    except UnicodeDecodeError:
        return False
    if s.rstrip('両').strip(' －') == '' and s.endswith('両'):
        return True  # money templates: digit slots (two-space units or －) + 両, filled by put_number 0x8002A004
    wide = sum(ord(c) >= 0x3000 for c in s)
    return (wide - s.count('　') >= 2 and wide * 2 >= len(s)
            and not any(0xFF61 <= ord(c) <= 0xFF9F or 0xE000 <= ord(c) <= 0xF8FF for c in s))


def strings(d, rf, base):
    """[(start, end)] of referenced NUL-terminated Japanese strings (end = index of the NUL), sorted."""
    out = set()
    for addr in rf:
        s = addr - base
        if 0 <= s < len(d) and (s == 0 or d[s - 1] == 0 or s % 4 == 0):
            e = d.find(b'\0', s)
            if e > s and is_jp(d[s:e]):
                out.add((s, e))
    # a string that ends where another starts is a tail reference into it (both kept: both are reached)
    return sorted(out)


def unreferenced(d, ss):
    """Japanese runs (text.jp_runs) inside no referenced string: text this tool cannot reach."""
    return [(a, s) for a, b, s in text.jp_runs(d) if not any(x <= a and b <= y for x, y in ss)]


def refs(d, base):
    """{address: [(kind, offset of the word or the lui)]} for every word/lui-pair address in d."""
    r = {}
    n = len(d) // 4
    words = struct.unpack_from(f'<{n}I', d)
    for i, w in enumerate(words):
        if base <= w < base + len(d):
            r.setdefault(w, []).append(('ptr', i * 4))
    for i, w in enumerate(words):
        if w >> 26 != 0x0F:  # lui
            continue
        rt, hi = (w >> 16) & 31, w & 0xFFFF
        for j in range(i + 1, min(i + 12, n)):
            x = words[j]
            op, rs, rt2, lo = x >> 26, (x >> 21) & 31, (x >> 16) & 31, x & 0xFFFF
            if rs == rt and op in (0x09, 0x0D, 0x20, 0x21, 0x23, 0x24, 0x25, 0x28, 0x29, 0x2B):
                addr = (hi << 16) + (lo if op == 0x0D else (lo - 0x10000 if lo & 0x8000 else lo))
                r.setdefault(addr & 0xFFFFFFFF, []).append(('hilo', i * 4, j * 4))
            if (op == 0 and (x >> 11) & 31 == rt) or (op not in (0x2B, 0x29, 0x28, 0x04, 0x05) and op != 0
                                                       and rt2 == rt and rs != rt):
                break  # rt overwritten
    return r


def table(path):
    d, base, _ = image(path)
    rf = refs(d, base)
    rows = []
    ss = strings(d, rf, base)
    for k, (s, e) in enumerate(ss):
        nxt = ss[k + 1][0] if k + 1 < len(ss) else len(d)
        cap = e + 1
        while cap < nxt and d[cap] == 0:
            cap += 1
        rows.append({'addr': base + s, 'off': s, 'raw': d[s:e], 'cap': cap - s, 'refs': rf.get(base + s, [])})
    return rows, unreferenced(d, ss)


if __name__ == '__main__':
    args = sys.argv[1:]
    lst = '--list' in args
    args = [a for a in args if a != '--list']
    files = [p for p in code_files() if not args or os.path.basename(p) in args]
    for p in files:
        rows, miss = table(p)
        if not rows and not miss:
            continue
        print(f'{os.path.basename(p)}: {len(rows)} strings, {len(miss)} Japanese runs outside them')
        if lst:
            for r in rows:
                kinds = ','.join(sorted({k[0] for k in r['refs']}))
                print(f"  {r['addr']:08X} cap{r['cap']:3} {kinds:8} {r['raw'].decode('cp932', 'replace')[:50]}")
            for a, s in miss:
                print(f'  MISS {a:06X} {s[:50]}')
