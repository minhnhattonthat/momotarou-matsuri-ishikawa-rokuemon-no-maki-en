"""Summarise the script VM op handlers (EXE table 0x800830D0, docs/re/script.md).

usage: python -X utf8 tools/ophandlers.py [OP ...]

For each handler, walks every path (bounded) tracking registers that hold `pc + k` (pc = the word the
handler's a0 points to) and prints, per path end: the pc stores (`sw r,(a0)` as +k or ?), the operand words read
(lhu/lh at pc+k) and the calls made. A guide for reading the handlers, not a source of truth.
"""
import importlib.util
import os
import sys

_spec = importlib.util.spec_from_file_location('re_tools', os.path.join(os.path.dirname(__file__), 're.py'))
_re = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_re)  # tools/re.py (its name clashes with the stdlib re)
load, md = _re.load, _re.md

TABLE, NOPS = 0x800830D0, 0x69


def handler_addrs():
    d, base = load('SLPM')
    o = TABLE - base
    return [int.from_bytes(d[o + 4 * i:o + 4 * i + 4], 'little') for i in range(NOPS)]


def analyse(addr, limit=400):
    d, base = load('SLPM')
    m = md()
    m.detail = False
    cache = {}

    def ins_at(a):
        if a not in cache:
            off = a - base
            cache[a] = next(m.disasm(d[off:off + 4], a), None)
        return cache[a]

    results = []
    # state: regs dict name -> ('pc',k) | ('a0',) | ('reg',name) ; stores list ; reads set ; calls list
    start = {'$a0': ('ptr',)}
    stack = [(addr, start, (), frozenset(), (), 0)]
    seen = set()
    while stack:
        a, regs, stores, reads, calls, n = stack.pop()
        key = (a, tuple(sorted(regs.items())), stores)
        if key in seen or n > limit:
            continue
        seen.add(key)
        i = ins_at(a)
        if i is None:
            continue
        mn, ops = i.mnemonic, [x.strip() for x in i.op_str.split(',')]
        regs = dict(regs)
        nxt = [a + 4]

        def val(r):
            return regs.get(r)

        def setr(r, v):
            if v is None:
                regs.pop(r, None)
            else:
                regs[r] = v

        delay = None
        if mn in ('beq', 'bne', 'beqz', 'bnez', 'bltz', 'bgez', 'blez', 'bgtz', 'b', 'j', 'jal', 'jr', 'jalr'):
            delay = ins_at(a + 4)
        def step(ins, regs):
            # capstone prints a zero offset as "($a0)"
            mn, ops = ins.mnemonic, [x.strip() for x in ins.op_str.replace(', (', ', 0(').split(',')]
            r = regs
            if mn == 'move':
                v = r.get(ops[1])
                if ops[1] == '$zero':
                    v = None
                r.pop(ops[0], None)
                if v is not None:
                    r[ops[0]] = v
            elif mn == 'lw' and '(' in ops[1]:
                off, b = ops[1].split('(')
                b = b[:-1]
                if r.get(b) == ('ptr',) and int(off, 0) == 0:
                    r[ops[0]] = ('pc', 0)
                else:
                    r.pop(ops[0], None)
            elif mn in ('lhu', 'lh', 'lbu', 'lb') and '(' in ops[1]:
                off, b = ops[1].split('(')
                b = b[:-1]
                v = r.get(b)
                r.pop(ops[0], None)
                if v and v[0] == 'pc':
                    return ('read', v[1] + int(off, 0), mn)
            elif mn in ('addiu', 'addi') and len(ops) == 3:
                v = r.get(ops[1])
                r.pop(ops[0], None)
                if v and v[0] == 'pc':
                    r[ops[0]] = ('pc', v[1] + int(ops[2], 0))
            elif mn in ('addu',) and len(ops) == 3:
                v1, v2 = r.get(ops[1]), r.get(ops[2])
                r.pop(ops[0], None)
                if v1 and v1[0] == 'pc' and ops[2] == '$zero':
                    r[ops[0]] = v1
                elif (v1 and v1[0] == 'pc') or (v2 and v2[0] == 'pc'):
                    r[ops[0]] = ('pcvar',)
            elif mn == 'sw' and '(' in ops[1]:
                off, b = ops[1].split('(')
                b = b[:-1]
                if r.get(b) == ('ptr',) and int(off, 0) == 0:
                    v = r.get(ops[0])
                    return ('store', v)
            elif mn in ('jal', 'jalr'):
                for k in list(r):
                    if k[1] in 'avt' or k in ('$ra',):
                        r.pop(k, None)
                return ('call', ops[0])
            elif ops and ops[0].startswith('$') and mn not in ('sw', 'sh', 'sb', 'beq', 'bne', 'beqz', 'bnez',
                                                                'bltz', 'bgez', 'blez', 'bgtz', 'jr', 'j', 'b'):
                r.pop(ops[0], None)
            return None

        def apply(ins):
            nonlocal stores, reads, calls
            ev = step(ins, regs)
            if ev:
                if ev[0] == 'read':
                    reads = reads | {(ev[1], ev[2])}
                elif ev[0] == 'store':
                    v = ev[1]
                    stores = stores + ((('+%d' % v[1]) if v and v[0] == 'pc' else ('var' if v else '?')),)
                elif ev[0] == 'call':
                    calls = calls + (ev[1],)

        if delay is None:
            apply(i)
            stack.append((a + 4, regs, stores, reads, calls, n + 1))
            continue
        # branch: delay slot executes first for our purposes (operands read before; fine for summaries)
        if mn in ('jal', 'jalr'):
            apply(delay)
            apply(i)
            stack.append((a + 8, regs, stores, reads, calls, n + 2))
            continue
        apply(delay)
        if mn == 'jr':
            if ops[0] == '$ra':
                results.append((stores, tuple(sorted(reads)), calls))
            else:
                results.append((stores + ('JR-switch',), tuple(sorted(reads)), calls))
            continue
        tgt = int(ops[-1], 0)
        if mn in ('j', 'b'):
            stack.append((tgt, regs, stores, reads, calls, n + 2))
        else:
            stack.append((tgt, regs, stores, reads, calls, n + 2))
            stack.append((a + 8, regs, stores, reads, calls, n + 2))
    return results


def summary(op, addr):
    res = analyse(addr)
    st = sorted({r[0] for r in res})
    rd = sorted({x for r in res for x in r[1]})
    cl = sorted({c for r in res for c in r[2]})
    rds = ' '.join(f'{k}{"" if t == "lhu" else t[1:]}' for k, t in rd)
    print(f'{op:02X} {addr:08X} stores={st} reads=[{rds}] calls={cl}')


if __name__ == '__main__':
    hs = handler_addrs()
    ops = [int(x, 16) for x in sys.argv[1:]] or range(NOPS)
    for op in ops:
        summary(op, hs[op])
