"""verify_build.py: phase 7 ROM-level check of a built disc against the original (pipeline §Checks).

    python -X utf8 tools/verify_build.py [CUE]      default build/momotarou-matsuri_en.cue; exit 1 on any error

Per disc file (read straight from both images through the ISO9660 records):
  - files insert.files() does not change are byte-identical;
  - changed files equal what insert.files() made (the EXE apart from its LBA/size tables, which follow the layout);
  - code files (EXE, OVL*): romdiff against the original, allowed = string slots (+ refs in layout.RELOC files),
    engine hook sites + hook area, money sites, the EXE LBA/size tables;
  - script archives: same entry count, non-script entries identical, and every script entry rebuilt with its
    original Japanese gives the original bytes (only text changed; jumps consistent);
  - FONT0D: only the English glyph page entry changed;
  - the EXE LBA table points at every file's new span, the size table holds its size.
"""
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import arc  # noqa: E402
import build  # noqa: E402
import codestr  # noqa: E402
import engine  # noqa: E402
import insert  # noqa: E402
import iso  # noqa: E402
import layout  # noqa: E402
import romdiff  # noqa: E402
import script  # noqa: E402
import text  # noqa: E402


def read_files(image):
    out = {}
    with open(image, 'rb') as f:
        for name, lba, size in iso.files(str(image)):
            out[name] = (lba, b''.join(iso.sector(f, lba + i) for i in range((size + 2047) // 2048))[:size])
    return out


def code_allowed(path, stem, rows):
    """Allowed file offsets in a code file: every string slot, refs of RELOC strings, hook and money sites."""
    d, base, hdr = codestr.image(path)
    ok = set()
    rf = codestr.refs(d, base) if stem.startswith(tuple(r.rstrip('@') for r in layout.RELOC)) else {}
    for r in rows:
        a = int(r['id'].split('@')[1], 16)
        o = a - base + hdr
        ok.update(range(o, o + r['max'] + 1))
        for k in rf.get(a, []):
            for x in k[1:]:
                ok.update(range(hdr + x, hdr + x + 4))
    sites = engine.MONEY_OVL.get(f'{stem}.BIN', [])
    if stem.startswith('SLPM'):
        sites = engine.MONEY_EXE + [tuple(engine.ORIG)]   # ORIG holds every patched site (money, choice, cursor)
        lo, hi = engine.FREE - engine.EXE_BASE, engine.FREE_END - engine.EXE_BASE
        ok.update(range(lo, hi))
        ok.update(range(build.TABLE, build.TABLE + 8 * build.COUNT))
        ok.update(range(build.SIZES, build.SIZES + 4 * (build.COUNT - build.DATA)))
    sbase = engine.EXE_BASE if stem.startswith('SLPM') else codestr.OVL_BASE
    for box in sites:
        for a in box:
            ok.update(range(a - sbase, a - sbase + 4))
    return ok


def check_archive(name, orig, new):
    errs = []
    oe, ne = arc.entries(orig), arc.entries(new)
    if len(oe) != len(ne):
        return [f'{name}: {len(ne)} entries, original has {len(oe)}']
    scripts = {i: its for i, _, its in text.script_entries(orig)}
    for i, ((_, a), (_, b)) in enumerate(zip(oe, ne)):
        # arc.pack pads entries to 16 bytes: compare without trailing zeros
        if i not in scripts:
            if a.rstrip(b'\0') != b.rstrip(b'\0'):
                errs.append(f'{name}/{i}: non-script entry changed')
            continue
        try:
            ops = [o for o, op, _ in script.ops(b) if op in text.TEXT_START]
        except (script.ParseError, ValueError) as ex:
            errs.append(f'{name}/{i}: built entry does not parse ({ex})')
            continue
        jp = [[s for _, s in strs] for _, _, _, strs in scripts[i]]
        if len(ops) != len(jp):
            errs.append(f'{name}/{i}: {len(ops)} text ops, original has {len(jp)}')
        elif text.rebuild(b, dict(zip(ops, jp))).rstrip(b'\0') != a.rstrip(b'\0'):
            errs.append(f'{name}/{i}: reverting the text does not give the original entry')
    return errs


def check_file(name, o, n, rows):
    """Range/structure errors for one changed disc file (o original, n new bytes)."""
    stem = Path(name).stem
    if name == build.EXE or stem.startswith('OVL'):
        key = 'SLPM_868' if name == build.EXE else stem
        e, _ = romdiff.check(o, n, code_allowed(build.TREE / name, stem, rows.get(key, [])), [])
        return [f'{name}: {x}' for x in e]
    if stem == 'FONT0D':
        oe, ne = arc.entries(o), arc.entries(n)
        if len(oe) != len(ne) or any(a != b for i, ((_, a), (_, b)) in enumerate(zip(oe, ne))
                                     if i != engine.PAGE_ENTRY):
            return [f'{name}: entries other than the glyph page changed']
        return []
    return check_archive(name, o, n)


def hook_branch_targets(exe):
    """Branches/jumps in the original EXE that land strictly inside an overwritten hook span (engine.ORIG)."""
    d, base = exe[codestr.EXE_HDR:], codestr.EXE_BASE
    sites = sorted(engine.ORIG)
    spans, cur = [], [sites[0], sites[0] + 4]
    for a in sites[1:]:
        if a == cur[1]:
            cur[1] += 4
        else:
            spans.append(cur)
            cur = [a, a + 4]
    spans.append(cur)
    bad = []
    for i in range(len(d) // 4):
        w = struct.unpack_from('<I', d, 4 * i)[0]
        pc, op = base + 4 * i, w >> 26
        if op in (2, 3):
            t = (pc & 0xF0000000) | ((w & 0x3FFFFFF) << 2)
        elif op in (1, 4, 5, 6, 7):
            t = pc + 4 + (((w & 0xFFFF) ^ 0x8000) - 0x8000) * 4
        else:
            continue
        bad += [(pc, t) for s, e in spans if s < t < e and not s <= pc < e]
    return bad


def verify(cue):
    errs = []
    orig = read_files(build.CUE.with_suffix('.bin'))
    new = read_files(Path(cue).with_suffix('.bin'))
    if set(orig) != set(new):
        errs.append(f'file set differs: {sorted(set(orig) ^ set(new))}')
    want = insert.files('en')
    rows = insert.rows_by_file()
    tables = set(range(build.TABLE, build.TABLE + 8 * build.COUNT)) | set(
        range(build.SIZES, build.SIZES + 4 * (build.COUNT - build.DATA)))
    for name, (_, o) in sorted(orig.items()):
        if name not in new:
            continue
        n = new[name][1]
        if name not in want and name != build.EXE:
            if n != o:
                errs.append(f'{name}: changed but insert.files() does not change it')
            continue
        w = want.get(name, o)
        if name == build.EXE:
            if len(n) != len(w) or any(x != y for i, (x, y) in enumerate(zip(n, w)) if i not in tables):
                errs.append(f'{name}: differs from insert.files() outside the LBA/size tables')
        elif n != w:
            errs.append(f'{name}: differs from insert.files() output')
        errs += check_file(name, o, n, rows)
    errs += [f'EXE {pc:#x} branches to {t:#x}, inside a hook span' for pc, t in hook_branch_targets(orig[build.EXE][1])]
    # LBA / size tables against the built image
    exe = new[build.EXE][1]
    span = {(lba, lba + (len(d) + 2047) // 2048): len(d) for lba, d in new.values()}
    for i in range(build.COUNT):
        s = struct.unpack_from('<II', exe, build.TABLE + 8 * i)
        if s not in span:
            errs.append(f'LBA table entry {i}: {s} is no file span')
        elif i >= build.DATA and struct.unpack_from('<I', exe, build.SIZES + 4 * (i - build.DATA))[0] != span[s]:
            errs.append(f'size table entry {i - build.DATA}: not the file size {span[s]}')
    return errs, sum(1 for k in orig if k in new and orig[k][1] != new[k][1])


if __name__ == '__main__':
    cue = sys.argv[1] if len(sys.argv) > 1 else ROOT / 'build' / 'momotarou-matsuri_en.cue'
    es, changed = verify(cue)
    for e in es[:80]:
        print('VERIFY', e)
    print(f'verify_build: {changed} files changed, {len(es)} errors')
    sys.exit(1 if es else 0)
