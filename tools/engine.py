"""English text engine (phase 5, docs/re/engine.md): digraph units, VWF drawer hook, English glyphs in FONT0D.

    python -X utf8 tools/engine.py sheet OUT.png     the English glyph cells as the game will draw them
    python -X utf8 tools/engine.py enc "text"        show the u16 units of an encoded line

Text units are u16 (docs/re/text.md). An English unit holds two ASCII bytes (a digraph, first char in the low
byte), so one 8-byte glyph record (32 per line object) carries two letters. The builder's append (0x80029AC4)
stores a digraph record {code, clut}; the drawer (0x8002A174), which skipped records with codes >= 0x20 not in
its control table, now draws both letters from FONT0D page 1 with per-glyph widths. PAD (0x7F, width 0) pads
odd runs and breaks a pair that would equal a control code (KG, bb, MM, two spaces ...).
"""
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import arc  # noqa: E402
import ecd  # noqa: E402

FONT_TXT = ROOT / 'fonts' / 'en12.txt'
ARMIPS = ROOT / 'tools' / 'armips' / 'armips.exe'
FIRST, LAST, PAD = 0x20, 0x7F, 0x7F
SPACE_W = 4
TOP = 2                       # en12.txt rows go to cell rows 2..11
# English cells: page 1 (FONT0D entry 0, nibble bits 0-1, odd CLUT), rows ROW0.., columns 0-15, char c at
# column (c - 0x20) & 15, row ROW0 + ((c - 0x20) >> 4). Those cells held kanji only Japanese text used.
PAGE_ENTRY, PAGE_SHIFT, ROW0, TPAGE = 0, 0, 0, 0x1E
# control codes of the builder/drawer table at 0x800829A8 (21 x {u16 code, u16 value}); no digraph may equal one
CONTROL = {0x4081, 0x2020, 0x474B, 0x504B, 0x4E4B, 0x3052, 0x3152, 0x3252, 0x3352, 0x3452, 0x4D4D, 0x5151,
           0x5555, 0x4949, 0x5A5A, 0x7777, 0x7272, 0x6767, 0x6262, 0x6F6F, 0x6464}
EXE_BASE = 0x80010000 - 0x800  # RAM address of EXE file offset 0
FREE, FREE_END = 0x80028A38, 0x80028DD4  # unreferenced debug/leaf functions (tools/deadcode.py, engine.md)
ORIG = {  # address: original word, checked before patching
    0x80029AC4: 0x3C078008,   # lui a3, 0x8008      (append: start)
    0x80029AC8: 0x24E81BE0,   # addiu t0, a3, 0x1be0
    0x8002A210: 0x1040003F,   # beqz v0, 0x8002a310 (drawer: code not in the control table -> skip)
}


def glyphs(path=FONT_TXT):
    """{char: rows ('#' ink)}."""
    out, cur = {}, None
    for line in path.read_text(encoding='utf-8').splitlines():
        if line.startswith('#') and cur is None or not line.strip():
            continue
        if line.startswith('= '):
            cur = out[line[2:]] = []
        else:
            cur.append(line)
    return out


def widths(g=None):
    """Advance in px for chars FIRST..LAST (space SPACE_W, PAD 0, others glyph width + 1)."""
    g = g or glyphs()
    w = []
    for c in range(FIRST, LAST + 1):
        if c == 0x20:
            w.append(SPACE_W)
        elif c == PAD or chr(c) not in g:
            w.append(0)
        else:
            w.append(max(len(r.rstrip('.')) for r in g[chr(c)]) + 1)
    return w


def cell(c):
    i = c - FIRST
    return (i & 15) * 12, (ROW0 + (i >> 4)) * 12


# ---- codec -------------------------------------------------------------------------------------------------

def encode_ascii(run):
    """ASCII run -> digraph bytes: pairs left to right, PAD before a char whose pair would be a control code,
    PAD at the end of an odd run."""
    out, i = bytearray(), 0
    b = run.encode('ascii')
    while i < len(b):
        a = b[i]
        nxt = b[i + 1] if i + 1 < len(b) else PAD
        if (nxt << 8 | a) in CONTROL:
            out += bytes([PAD, a])
            i += 1
            continue
        out += bytes([a, nxt])
        i += 2
    return bytes(out)


def width_px(s, w=None):
    """Drawn width of a decoded-form line (codes and Japanese count as 12 px, the drawer's cell)."""
    import re
    w = w or widths()
    total = 0
    for tok in re.findall(r'\{\w+\}|\[[0-9A-F]{2}\]|.', s):
        if tok.startswith('{'):
            continue
        if len(tok) == 1 and FIRST <= ord(tok) <= LAST:
            total += w[ord(tok) - FIRST]
        else:
            total += 12
    return total


# ---- font --------------------------------------------------------------------------------------------------

def tim_pixels(t):
    """(offset of the pixel data, bytes per row) of a TIM with an optional CLUT block."""
    o = 8 + (struct.unpack_from('<I', t, 8)[0] if struct.unpack_from('<I', t, 4)[0] & 8 else 0)
    return o + 12, struct.unpack_from('<H', t, o + 8)[0] * 2


def patch_font(font0d):
    """FONT0D.BIN with the English glyphs drawn into page 1 (entry 0, bits 0-1 of each nibble)."""
    ents = arc.entries(font0d)
    hs = struct.unpack_from('<I', font0d)[0]
    blob = ents[PAGE_ENTRY][1]
    raw, _, _ = ecd.header(blob)
    t = bytearray(ecd.decompress(blob))
    pix, stride = tim_pixels(t)
    g, w = glyphs(), widths()
    for c in range(FIRST, LAST + 1):
        u, v = cell(c)
        rows = g.get(chr(c), []) if c not in (0x20, PAD) else []
        for y in range(12):
            for x in range(12):
                r = y - TOP
                ink = 0 <= r < len(rows) and x < len(rows[r]) and rows[r][x] == '#'
                o = pix + (v + y) * stride + (u + x) // 2
                sh = 4 * ((u + x) & 1) + PAGE_SHIFT
                t[o] = (t[o] & ~(3 << sh)) | ((3 << sh) if ink else 0)
    assert all(x <= 12 for x in w)
    new = ecd.compress(bytes(t), raw)
    out = [e for _, e in ents]
    out[PAGE_ENTRY] = new
    return arc.pack(out, hs)


# ---- EXE ---------------------------------------------------------------------------------------------------

def asm_source(exe_path):
    w = ', '.join(str(x) for x in widths())
    return f'''.psx
.open "{exe_path}", {EXE_BASE:#x}

; append(code a0, obj a1, colour a2): digraph -> record {{code, clut = colour * 2 + 1}}, else the original lookup
.org 0x80029AC4
    j       append_hook
    lui     a3, 0x8008

; drawer: a record code >= 0x20 that is not in the control table is a digraph
.org 0x8002A210
    beqz    v0, digraph_draw

.org {FREE:#x}
.area {FREE_END - FREE:#x}, 0
append_hook:
    andi    t1, a0, 0xff
    addiu   t1, t1, -{FIRST:#x}
    sltiu   t1, t1, {LAST - FIRST + 1:#x}
    srl     t2, a0, 8
    andi    t2, t2, 0xff
    addiu   t2, t2, -{FIRST:#x}
    sltiu   t2, t2, {LAST - FIRST + 1:#x}
    and     t1, t1, t2
    bnez    t1, @@digraph
    nop
    j       0x80029ACC
    addiu   t0, a3, 0x1be0
@@digraph:
    lhu     v0, 2(a1)
    andi    a2, a2, 0xffff
    sll     v0, v0, 3
    addu    v0, v0, a1
    sh      a0, 8(v0)
    sll     t1, a2, 1
    addiu   t1, t1, 1
    jr      ra
    sh      t1, 10(v0)

; in the drawer's frame: a2 = record, s1 = x, s4 = y << 16, s2 = record index, s3 = line object.
; sp+0x2C (free word of the frame) = chars left, sp+0x2E = clut. Exits to 0x8002A310 with a3 = s2 + 1.
digraph_draw:
    lhu     t0, 0(a2)
    lhu     t1, 2(a2)
    sh      t0, 0x2c(sp)
    sh      t1, 0x2e(sp)
@@next:
    lhu     t0, 0x2c(sp)
    nop
    andi    t2, t0, 0xff
    beqz    t2, @@done
    srl     t0, t0, 8
    sh      t0, 0x2c(sp)
    addiu   t2, t2, -{FIRST:#x}
    sltiu   t3, t2, {LAST - FIRST + 1:#x}
    beqz    t3, @@next
    la      t3, widths
    addu    t3, t3, t2
    lbu     a3, 0(t3)
    andi    t4, t2, 15
    sll     t5, t4, 3
    sll     t4, t4, 2
    addu    t4, t4, t5
    srl     t5, t2, 4
    addiu   t5, t5, {ROW0}
    sll     t6, t5, 3
    sll     t5, t5, 2
    addu    t5, t5, t6
    sll     a1, s1, 16
    sra     a1, a1, 16
    addu    s1, s1, a3
    beqz    t2, @@next          ; space: advance only
    nop
    beqz    a3, @@next          ; PAD / no glyph: nothing to draw
    addiu   t6, zero, 12
    sw      t6, 0x10(sp)
    addiu   t6, zero, {TPAGE:#x}
    sw      t6, 0x14(sp)
    sw      t4, 0x18(sp)
    sw      t5, 0x1c(sp)
    addiu   t6, zero, 0x100
    sw      t6, 0x20(sp)
    lhu     t6, 0x2e(sp)
    nop
    addiu   t6, t6, 0x1e0
    sw      t6, 0x24(sp)
    lw      t6, 0x108(s3)
    nop
    sw      t6, 0x28(sp)
    sra     a2, s4, 16
    jal     0x8001D14C
    move    a0, zero
    move    s0, v0
    move    a0, s0
    jal     0x8001D2F4
    addiu   a1, zero, 1
    jal     0x8001D210
    move    a0, s0
    j       @@next
    nop
@@done:
    j       0x8002A310
    addiu   a3, s2, 1
widths:
    .byte {w}
.endarea
.close
'''


def patch_exe(exe):
    """EXE bytes with the digraph/VWF hooks (armips), after checking the original words."""
    for a, word in ORIG.items():
        got = struct.unpack_from('<I', exe, a - EXE_BASE)[0]
        if got != word:
            raise ValueError(f'EXE {a:#x}: {got:#010x}, expected {word:#010x}')
    with tempfile.TemporaryDirectory() as d:
        p, s = Path(d) / 'exe.bin', Path(d) / 'engine.asm'
        p.write_bytes(exe)
        s.write_text(asm_source(p.as_posix()), encoding='utf-8')
        r = subprocess.run([str(ARMIPS), str(s)], capture_output=True, text=True)
        if r.returncode:
            raise RuntimeError(f'armips failed:\n{r.stdout}{r.stderr}')
        out = p.read_bytes()
    assert len(out) == len(exe)
    return out


def sheet(out):
    from PIL import Image
    import numpy as np
    t = ecd.decompress(arc.entries(patch_font((ROOT / 'work/disc/tree/OUTBIN/FONT0D.BIN').read_bytes()))[0][1])
    pix, stride = tim_pixels(t)
    w = widths()
    img = np.zeros((14 * 6, 16 * 14), np.uint8)
    for c in range(FIRST, LAST + 1):
        u, v = cell(c)
        i = c - FIRST
        for y in range(12):
            for x in range(12):
                b = t[pix + (v + y) * stride + (u + x) // 2] >> (4 * ((u + x) & 1) + PAGE_SHIFT) & 3
                img[i // 16 * 14 + y, i % 16 * 14 + x] = b * 85
        img[i // 16 * 14 + 12, i % 16 * 14:i % 16 * 14 + w[i]] = 96
    Image.fromarray(img).resize((img.shape[1] * 4, img.shape[0] * 4), Image.NEAREST).save(out)


if __name__ == '__main__':
    if sys.argv[1:2] == ['sheet']:
        sheet(sys.argv[2])
    elif sys.argv[1:2] == ['enc']:
        b = encode_ascii(sys.argv[2])
        print(' '.join(b[i:i + 2].decode('latin-1') for i in range(0, len(b), 2)))
    else:
        print(__doc__)
