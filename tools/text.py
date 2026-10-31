"""Script text: find, decode, encode, rebuild (docs/re/script.md, docs/re/text.md).

usage:
  python -X utf8 tools/text.py dump [--force]    write script/<FILE>.json for archives without one
  python -X utf8 tools/text.py stats             items per file kind
  python -X utf8 tools/text.py gaps [--all]      Japanese runs on the disc no extracted item covers

Text items live in script entries (archive entries that parse as VM bytecode, tools/script.py):
  msg      op 02 `02 mode voice` + lines. Text form: lines joined by "\\n"; a line break is KG (implicit),
           "{KP}\\n" is a page break; the last line ends with {KN} (keep window) or nothing (close).
  caption  op 26: one line.
  menu     op 41 `41 n` + n lines: one item per line, id suffix ".k".
Codes: {KG} {KP} {KN} line/page/end, {bb} {rr} {oo} {dd} .. {ww} colour, {MM} name, {R0}-{R3} number.
Text is Shift-JIS (cp932); other bytes decode as [XX] and roundtrip.
"""
import glob
import json
import os
import re
import struct
import sys

sys.path.insert(0, os.path.dirname(__file__))
import arc  # noqa: E402
import script  # noqa: E402
from tbl import Table  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), '..')
TREE = os.path.join(ROOT, 'work', 'disc', 'tree')
OUT = os.path.join(ROOT, 'script')
CODES = ['KG', 'KP', 'KN', 'bb', 'rr', 'oo', 'dd', 'ww', 'MM', 'R0', 'R1', 'R2', 'R3',
         'KK', 'KE']  # KK/KE: line break / end in the EXE's memory-card messages
SKIP = (b'pQES', b'ANM\x00', b'ECD\x01', b'pBAV', b'end\x1a')
TEXT_START = {0x02: 6, 0x26: 2, 0x41: 4}
KIND = {0x02: 'msg', 0x26: 'caption', 0x41: 'menu'}


def jp_table():
    lines = [f'{c.encode().hex().upper()}={{{c}}}' for c in CODES]
    for hi in list(range(0x81, 0xA0)) + list(range(0xE0, 0xFD)):
        for lo in range(0x40, 0xFD):
            if lo == 0x7F:
                continue
            try:
                ch = bytes([hi, lo]).decode('cp932')
            except UnicodeDecodeError:
                continue
            if len(ch) == 1 and ch not in '={}[]':
                lines.append(f'{hi:02X}{lo:02X}={ch}')
    return Table(lines)


JP = None


def table():
    global JP
    JP = JP or jp_table()
    return JP


def split_lines(b):
    """Text bytes -> line contents (terminator units dropped). Raises if a terminator is not 0x0000."""
    out, o = [], 0
    while o < len(b):
        e = script.line_end(b, o)
        if b[e - 2:e] != b'\0\0':
            raise ValueError(f'line terminator {b[e - 2:e].hex()} is not 0000')
        out.append(b[o:e - 2])
        o = e
    return out


def decode_lines(lines):
    t = table()
    return [t.decode(x, 0, len(x))[0] for x in lines]


def msg_text(lines):
    s = decode_lines(lines)
    for i in range(len(s) - 1):
        if s[i].endswith('{KG}'):
            s[i] = s[i][:-4]
        elif not s[i].endswith('{KP}'):
            raise ValueError(f'inner line without KG/KP: {s[i]!r}')
    return '\n'.join(s)


PIECE = re.compile(r'(\{\w+\}|\[[0-9A-Fa-f]{2}\]|[^\x20-\x7e])')


def encode_text(text):
    """Codes, [XX] bytes and Japanese through the table; runs of printable ASCII as digraphs (tools/engine.py)."""
    import engine
    out = bytearray()
    for i, part in enumerate(PIECE.split(text)):
        if not part:
            continue
        out += table().encode(part) if i % 2 else engine.encode_ascii(part)
    return bytes(out)


def encode_line(text):
    b = encode_text(text)
    if len(b) % 2:
        raise ValueError(f'odd byte length: {text!r}')
    return b + b'\0\0'


def encode_msg(text):
    ls = text.split('\n')
    out = b''
    for i, line in enumerate(ls):
        if i < len(ls) - 1 and not line.endswith('{KP}'):
            line += '{KG}'
        if i == len(ls) - 1 and (line.endswith('{KG}') or line.endswith('{KP}')):
            raise ValueError(f'last line must not end in KG/KP: {text!r}')
        out += encode_line(line)
    return out


def items_of(e):
    """Text items of a parsed script entry: [(off, op, n, [(suffix, jp), ...])]."""
    res = []
    for o, op, n in script.ops(e):
        if op not in TEXT_START:
            continue
        lines = split_lines(e[o + TEXT_START[op]:o + n])
        if op == 0x02:
            strs = [('', msg_text(lines))]
        elif op == 0x26:
            strs = [('', decode_lines(lines)[0])]
        else:
            strs = [(f'.{k}', s) for k, s in enumerate(decode_lines(lines))]
        res.append((o, op, n, strs))
    return res


def script_entries(d):
    """[(index, entry bytes, items)] for entries of archive bytes d that parse as scripts with text."""
    out = []
    for i, (_, e) in enumerate(arc.entries(d) or []):
        if not e or e[:4] in SKIP:
            continue
        try:
            its = items_of(e)
        except (script.ParseError, ValueError):
            continue
        if its:
            out.append((i, e, its))
    return out


def archives():
    return sorted(glob.glob(os.path.join(TREE, 'OUTBIN', '*D.BIN')))


def stem(path):
    return os.path.basename(path)[:-4]


def item_id(name, i, o, suffix):
    return f'{name}/{i}/{o:04X}{suffix}'


def text_bytes(op, strs):
    if op == 0x02:
        return encode_msg(strs[0])
    return b''.join(encode_line(s) for s in strs)


def rebuild(e, texts):
    """Entry bytes with each text op's strings replaced: texts = {op offset: [str, ...]} (missing = keep).

    Jump offsets (script.jumps) are moved with the ops they point at; a jump whose target is not an op
    boundary in the original (one GSS0200 branch has offset 0xFFFF) keeps its raw value."""
    old = list(script.ops(e))
    bounds = {o for o, _, _ in old} | {len(e)}
    pieces, newpos, pos = [], {}, 0
    for o, op, n in old:
        newpos[o] = pos
        b = e[o:o + n]
        if o in texts:
            b = b[:TEXT_START[op]] + text_bytes(op, texts[o])
        pieces.append(bytearray(b))
        pos += len(b)
    newpos[len(e)] = pos
    for (o, op, n), b in zip(old, pieces):
        for at, target in script.jumps(e, o, op):
            if target not in bounds:
                continue
            k = at - o
            raw = struct.unpack_from('<H', e, at)[0]
            off = newpos[target] - newpos[o] - (2 if op in script.IF else 0)  # IF ops: target = op + off + 2
            if off < 0 or off > 0xFFFE:
                raise ValueError(f'jump at {o:#x} out of range after rebuild')
            struct.pack_into('<H', b, k, off | (raw & 1))
    return b''.join(pieces)


def code_rows(path):
    """Rows for the Japanese C strings of a code file (tools/codestr.py); max = bytes in place, NUL excluded."""
    import codestr
    rows, _ = codestr.table(path)
    name = os.path.basename(path).split('.')[0]
    return [{'id': f"{name}@{r['addr']:08X}", 'kind': 'code', 'jp': table().decode(r['raw'], 0, len(r['raw']))[0],
             'en': '', 'max': r['cap'] - 1} for r in rows]


def extract(path):
    """Fresh rows (without en) for one disc file: an archive's script text or a code file's strings."""
    if not path.endswith('D.BIN'):
        return code_rows(path)
    rows = []
    for i, e, its in script_entries(open(path, 'rb').read()):
        for o, op, n, strs in its:
            for suffix, jp in strs:
                rows.append({'id': item_id(stem(path), i, o, suffix), 'kind': KIND[op], 'jp': jp, 'en': ''})
    return rows


def text_files():
    import codestr
    return archives() + codestr.code_files()


def dump(force=False):
    os.makedirs(OUT, exist_ok=True)
    wrote = 0
    for f in text_files():
        path = os.path.join(OUT, os.path.basename(f).split('.')[0] + '.json')
        if os.path.exists(path) and not force:
            continue
        rows = extract(f)
        if not rows:
            continue
        if os.path.exists(path):  # --force: regenerate jp/ids, keep every en whose id survives
            old = {r['id']: r for r in json.load(open(path, encoding='utf-8'))}
            for r in rows:
                if r['id'] in old:
                    r['en'] = old[r['id']].get('en', '')
            lost = [i for i, r in old.items() if r.get('en') and i not in {x['id'] for x in rows}]
            if lost:
                raise SystemExit(f'{path}: ids with English would be dropped: {lost[:5]}')
        with open(path, 'w', encoding='utf-8', newline='\n') as fh:
            json.dump(rows, fh, ensure_ascii=False, indent=1)
            fh.write('\n')
        wrote += 1
    print(f'wrote {wrote} files to script/')


SJIS2 = re.compile(rb'(?:[\x81-\x9f\xe0-\xfc][\x40-\x7e\x80-\xfc])+')


def jp_runs(d, minchars=4):
    """(start, end, text) of Shift-JIS runs with >= minchars chars, at least a third kana."""
    for m in SJIS2.finditer(d):
        try:
            s = m.group().decode('cp932')
        except UnicodeDecodeError:
            continue
        kana = sum('ぁ' <= c <= 'ヿ' for c in s)
        if len(s) >= minchars and kana * 3 >= len(s):
            yield m.start(), m.end(), s


def covered_ranges(d):
    """File-relative byte ranges of extracted text in archive bytes d."""
    offs = arc.offsets(d) or []
    out = []
    for i, e, its in script_entries(d):
        for o, op, n, _ in its:
            out.append((offs[i] + o, offs[i] + o + n))
    return out


def gaps(show_all=False):
    files = archives() + sorted(glob.glob(os.path.join(TREE, 'OUTBIN', 'OVL*.BIN'))) + \
        [os.path.join(TREE, 'SLPM_868.88')]
    total = 0
    by = {}
    for f in files:
        d = open(f, 'rb').read()
        rs = sorted(covered_ranges(d)) if f.endswith('D.BIN') else []
        miss = [(a, b, s) for a, b, s in jp_runs(d) if not any(x <= a and b <= y for x, y in rs)]
        if miss:
            by[stem(f) if f.endswith('.BIN') else os.path.basename(f)] = miss
            total += sum(len(s) for _, _, s in miss)
    for k, miss in by.items():
        print(f'{k}: {len(miss)} runs, {sum(len(s) for *_, s in miss)} chars')
        for a, b, s in (miss if show_all else miss[:3]):
            print(f'   {a:06X} {s[:60]}')
    print('total uncovered chars', total)


def stats():
    from collections import Counter
    c = Counter()
    for f in archives():
        for i, e, its in script_entries(open(f, 'rb').read()):
            for o, op, n, strs in its:
                c[(re.sub(r'\d.*', '', stem(f)), KIND[op])] += len(strs)
    for k, v in sorted(c.items()):
        print(*k, v)


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    if cmd == 'dump':
        dump('--force' in sys.argv)
    elif cmd == 'gaps':
        gaps('--all' in sys.argv)
    elif cmd == 'stats':
        stats()
    else:
        print(__doc__)
