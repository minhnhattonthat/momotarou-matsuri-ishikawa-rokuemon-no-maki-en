"""Write tools/debug/scenes.txt: every scene warp.lua can reach (docs/re/debug.md explains each kind).

usage: python -X utf8 tools/debug/gen_scenes.py        (needs work/disc/tree from dumpsxiso)

Kinds (one scene per line: name kind args...):
  menu  MODE PRESSES   cold boot, then the menu presses (c=circle, r=right) once the main menu (mode 0x49) is up
  event N              new game, OVLEVT event N (0-37) instead of the intro: [0x8008C4F9] = N at mode 0x4D
  game  MODE [CONTEXT]  trial match transition, optional native mode-context byte
  map   MAP X Y DIR INIT [PREOPS POSTOPS]  its own initializer, optional comma-separated u16 setup ops
  save  0              new game, invoke the shrine's save op; SAVE_CONFIRM=true selects slot 1 and Yes
  cards 0              new game, enable 100 collectible flags in RAM and enter the Card Album (mode 0x4C)
  mask  0              new game, invoke the mask shop's create-mask op (mode 0x3A)
Map arrival points are the commonest 0x1D destination for that map in the game's own scripts.
"""
import collections, glob, os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import arc, fileids, maps, script

TREE = os.path.join(HERE, '..', '..', 'work', 'disc', 'tree', 'OUTBIN')
MODES = {0x46: 'title', 0x49: 'main_menu'}
# map -> arrival point that works where the commonest one hangs the game; None = every point hangs
# (tools/debug/find_arrivals.py over warp_all.py's failures)
OVERRIDE = {
    59: (29, 127, 2), 61: (26, 18, 2), 71: (38, 10, 0), 80: (20, 18, 0), 81: (20, 18, 0), 99: (39, 14, 0),
    100: (39, 14, 0), 116: (26, 18, 2), 126: (11, 17, 2), 128: (26, 18, 2), 139: (21, 29, 0), 141: (32, 18, 0),
    142: (21, 52, 2), 155: (26, 18, 2), 163: (30, 22, 0), 180: (18, 16, 0), 200: (27, 35, 3), 202: (31, 33, 0),
    205: (18, 40, 2), 223: (16, 41, 0), 263: (19, 10, 0), 304: (29, 23, 2), 321: (31, 14, 0), 345: (17, 20, 2),
    284: (19, 11, 0),  # GSF0000D's own entry; dir 2 (GSD0000D) never loads in the en build (status.md, phase 7)
}
# Keep the normal GSF0000D:25 entry's setup around the map load. Without it,
# map 294 never completes loading even with the correct 0x32F initializer.
MAP_OPS = {294: ((0x59, 2, 0x56, 0x14), (0x57, 0, 0, 1))}


def arrivals():
    """map -> Counter of (x, y, dir) from every op 0x1D pattern in the script files."""
    c = collections.defaultdict(collections.Counter)
    for f in glob.glob(os.path.join(TREE, 'G*.BIN')):
        d = open(f, 'rb').read()
        for i in range(0, len(d) - 12, 2):
            op, m, x, y, dr, ex = struct.unpack_from('<6H', d, i)
            if op == 0x1D and m < maps.COUNT and 0 < x < 0x100 and 0 < y < 0x100 and dr < 8 and ex in (0xFFFF, 0xFFFE):
                c[m][(x, y, dr)] += 1
    return c


def initializers():
    """Map -> initializer used by original incoming scripts.

    Prefer an immediately adjacent 1E. For maps without one (e.g. bath 189),
    scan the intervening flag/if operations up to the next map change or end,
    and require one unique candidate. No guessed/default script is accepted.
    Maps 35/140 have conditional fallthroughs into another destination's init;
    both also have unambiguous adjacent calls, which take precedence.
    """
    direct, later = collections.defaultdict(set), collections.defaultdict(set)
    for f in glob.glob(os.path.join(TREE, 'GS*.BIN')):
        for _, d in arc.entries(open(f, 'rb').read()):
            try:
                ops = list(script.ops(d))
            except (ValueError, script.ParseError):
                continue
            for i, (o, op, _) in enumerate(ops):
                if op != 0x1D:
                    continue
                m = script.u16(d, o + 2)
                if m >= maps.COUNT:
                    continue
                for at, nextop, _ in ops[i + 1:]:
                    if nextop == 0x1E:
                        (direct if at == o + 12 else later)[m].add(script.u16(d, at + 2))
                        break
                    if nextop in (0, 0x1D):
                        break
    result = {}
    for m in direct.keys() | later.keys():
        candidates = direct.get(m) or later[m]
        if len(candidates) != 1:
            raise ValueError(f'map {m}: ambiguous initializers {candidates}')
        result[m] = next(iter(candidates))
    return result


def overlays():
    """mode -> overlay file name, from the EXE mode switch (0x80020F40, table 0x80018158)."""
    exe = open(os.path.join(TREE, '..', 'SLPM_868.88'), 'rb').read()[0x800:]
    w = lambda a: struct.unpack_from('<I', exe, a - 0x80010000)[0]
    names, out = fileids.names(), {}
    for m in range(2, 0x3E):
        t = w(0x80018158 + 4 * (m - 1))
        for a in range(t, t + 0x80, 4):
            i = w(a)
            if i >> 26 == 9 and (i >> 16) & 31 == 4 and (i >> 21) & 31 == 0 and i & 0xFFFF >= 0x2710:
                out[m] = names[(i & 0xFFFF) - 0x2710]
                break
    return out


def main():
    names = fileids.names()
    lines = ['# Scene list for tools/debug/warp.lua (generated by tools/debug/gen_scenes.py; kinds in its docstring).',
             '# name kind args',
             'title menu 0x46 -', 'main_menu menu 0x49 -', 'story_menu menu 0x49 c', 'trial_menu menu 0x50 c',
             'continue menu 0x4A r,c', 'save_menu save 0', 'card_album cards 0', 'mask_editor mask 0',
             'name_entry game 0x51 3  # Name Entry with return-to-Quick-Match context']
    for n in range(38):
        lines.append(f'event{n:02d} event {n}' + ('  # opening' if n == 19 else '  # ending + credits' if n == 20 else ''))
    seen = set()
    for m, ovl in sorted(overlays().items()):
        lines.append(f'game_{ovl[3:6].lower()}_{m:02x} game 0x{m:02X}' + ('  # same overlay as an earlier mode' if ovl in seen else ''))
        seen.add(ovl)
    arr, init = arrivals(), initializers()
    for m, r in enumerate(maps.records()):
        f = fileids.data_name(names, struct.unpack_from('<H', r)[0])  # GF/GV/GS + area + room
        if not arr[m]:
            lines.append(f'# map {m} {f}: no arrival point in the scripts')
            continue
        if m in OVERRIDE and OVERRIDE[m] is None:
            lines.append(f'# map {m} {f}: the game hangs after warping there (every arrival point tried)')
            continue
        (x, y, dr) = OVERRIDE.get(m) or arr[m].most_common(1)[0][0]
        extra = ''
        if m in MAP_OPS:
            extra = ' ' + ' '.join(','.join(f'0x{v:X}' for v in ops) for ops in MAP_OPS[m])
        lines.append(f'map_{f[:-6].lower()}_{m:03d} map {m} {x} {y} {dr} 0x{init[m]:03X}' + extra)
    open(os.path.join(HERE, 'scenes.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(lines) + '\n')
    print(len([l for l in lines if l and not l.startswith('#')]), 'scenes')


if __name__ == '__main__':
    main()
