"""Translation batches (docs/translator-brief.md): split untranslated script into work/tl/bNNN.tsv, check a
translator's work/tl/bNNN.out.tsv, merge checked batches into script/ `en`.

    python -X utf8 tools/batches.py split [--size 3500] [--only PREFIX ...]   batches for untranslated JP
    python -X utf8 tools/batches.py check bNNN ...                          ids, codes, ASCII, layout, glossary
    python -X utf8 tools/batches.py merge bNNN ...                          check, then write en to every row
    python -X utf8 tools/batches.py terms bNNN ...                          (re)write build/terms_bNNN.txt
    python -X utf8 tools/batches.py todo                                    untranslated units / chars left

Each unique JP text is translated once (id = its first row); merge writes the English to every row with the same
JP and check lays it out (tools/layout.py) in every box any of them is drawn in. Batch TSV: id, speaker (blank:
the script has no speaker field), form (box variant), limit, JP with in-page line breaks as ' / ', pages {KP}.
Not batched (set by hand): money templates ([20] digit slots + 両) and insert.SJIS_ONLY save titles.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import insert  # noqa: E402
import layout  # noqa: E402
import windows  # noqa: E402

TL = ROOT / 'work' / 'tl'
ORDER = ['OVLGMAIN', 'OVLXTTL', 'SLPM', 'OVLM', 'OVLEVT', 'NAME', 'YUGI', 'GDEF', 'PREM', 'EVT', 'GSV', 'GSF', 'GSS',
         'M']
JA = re.compile(r'[぀-ヿ㐀-鿿＀-￯〇～…・々]')
TOKEN = re.compile(r'\{\w+\}|\[[0-9A-F]{2}\]')
FREE = {'{KP}', '{n}', '{KN}', '{KK}', '{KE}'}   # placed by the English / checked by layout


def group(stem):
    return next((g for g in ORDER if stem.startswith(g)), stem)


def skip(r):
    return (r['id'] in insert.SJIS_ONLY or '[20]' in r['jp'] or not JA.search(TOKEN.sub('', r['jp'])))


def units():
    """{jp: {'id', 'jp', 'rows', 'stem', 'en'}} for every unique JP needing English, in batch order."""
    files = sorted(insert.rows_by_file().items(), key=lambda kv: (ORDER.index(group(kv[0])), kv[0]))
    out = {}
    for stem, rows in files:
        for r in rows:
            if skip(r):
                continue
            u = out.setdefault(r['jp'], {'id': r['id'], 'jp': r['jp'], 'rows': [], 'stem': stem, 'en': r.get('en', '')})
            u['rows'].append(r)
    return out


def boxes(u, var):
    """[(row, variant)] one per distinct box (variant, in-place max) the unit's rows are drawn in."""
    seen, out = set(), []
    for r in u['rows']:
        k = (var[r['id']], r.get('max'))
        if k not in seen:
            seen.add(k)
            out.append((r, var[r['id']]))
    return out


def show_jp(jp):
    pages = []
    for seg in jp.replace('{KN}', '').split('{KP}'):
        lines = [ln.strip('　 ') for ln in seg.strip('\n').split('\n')]
        pages.append(' / '.join(ln for ln in lines if ln))
    return ' {KP} '.join(pages) + ('{KN}' if jp.endswith('{KN}') else '')


def limit(u, var):
    bs = boxes(u, var)
    r, v = min(bs, key=lambda b: windows.budget(b[0], b[1])[0])
    px, _, tag = windows.budget(r, v)
    s = f'{"~" if tag == "guess" else ""}{px}px'      # ~ = soft (guessed) px; the byte cap B is hard
    s += ' x3/page' if r['kind'] == 'msg' else ''
    caps = [b[0]['max'] for b in bs if b[0].get('max')]
    return s + (f' {min(caps)}B' if caps else ''), v


def read_tsv(path):
    return [ln.split('\t') for ln in path.read_text(encoding='utf-8').splitlines() if ln.strip()]


def split(argv):
    only = argv[argv.index('--only') + 1:] if '--only' in argv else None
    size = int(argv[argv.index('--size') + 1]) if '--size' in argv else 3500
    TL.mkdir(parents=True, exist_ok=True)
    taken = {r[0] for p in TL.glob('b[0-9][0-9][0-9].tsv') for r in read_tsv(p)}
    n = max([int(p.stem[1:4]) for p in TL.glob('b[0-9][0-9][0-9].tsv')] or [0])
    var = windows.variants()
    todo = [u for u in units().values() if not u['en'] and u['id'] not in taken
            and (only is None or group(u['stem']) in only)]
    batches, cur, chars, g = [], [], 0, None
    for u in todo:
        c = len(TOKEN.sub('', u['jp']))
        if cur and (chars + c > size or len(cur) >= 150 or group(u['stem']) != g):
            batches.append(cur)
            cur, chars = [], 0
        cur.append(u)
        chars += c
        g = group(u['stem'])
    if cur:
        batches.append(cur)
    for b in batches:
        n += 1
        name = f'b{n:03d}'
        path = TL / f'{name}.tsv'
        assert not path.exists(), path
        lines = []
        for u in b:
            lim, v = limit(u, var)
            lines.append(f"{u['id']}\t\t{v}\t{lim}\t{show_jp(u['jp'])}")
        path.write_text('\n'.join(lines) + '\n', encoding='utf-8', newline='\n')
        terms([name])
        print(name, len(b), 'entries', sum(len(TOKEN.sub('', u['jp'])) for u in b), 'chars', b[0]['stem'])


def glossary():
    """[(jp, en, avoid, person)] from glossary.md tables (person: a ## Characters row, honorifics kept: D1)."""
    rows, section = [], ''
    for line in (ROOT / 'glossary.md').read_text(encoding='utf-8').splitlines():
        section = line if line.startswith('## ') else section
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if line.startswith('|') and len(cells) >= 2 and JA.search(cells[0]) and cells[1]:
            avoid = [a.strip() for a in cells[4].split(',') if a.strip()] if len(cells) > 4 else []
            jps = [re.sub(r'\(.*?\)', '', j).strip() for j in cells[0].split('/')]
            ens = [e.strip() for e in cells[1].split('/')]
            for k, j in enumerate(jps):          # 'A / B' | 'a / b' pair up; else every JP form -> the first EN
                rows.append((j, ens[k] if len(ens) == len(jps) else ens[0], avoid, section == '## Characters'))
    return rows


def kind(c):
    if '぀' <= c <= 'ゟ':
        return 'h'
    if '゠' <= c <= 'ヿ':
        return 'k'
    if '一' <= c <= '鿿' or c == '々':
        return 'c'
    return 'o'


def has_term(jp, term):
    """term occurs in jp as a whole run (not inside a longer run of the same script)."""
    if len(term) < 2:
        return False
    for m in re.finditer(re.escape(term), jp):
        a, b = m.start(), m.end()
        if (a == 0 or kind(jp[a - 1]) != kind(term[0])) and (b == len(jp) or kind(jp[b]) != kind(term[-1])):
            return True
    return False


def terms(names):
    gl = glossary()
    (ROOT / 'build').mkdir(exist_ok=True)
    for name in names:
        jps = ' '.join(r[4] for r in read_tsv(TL / f'{name}.tsv'))
        rows = sorted({(j, e) for j, e, *_ in gl if has_term(jps, j)})
        (ROOT / f'build/terms_{name}.txt').write_text(
            ''.join(f'{j}\t{e}\n' for j, e in rows) or '(no glossary terms in this batch)\n', encoding='utf-8',
            newline='\n')


HONOR = {'さん': 'san', 'サン': 'san', 'さま': 'sama', 'サマ': 'sama', '様': 'sama', 'くん': 'kun', '君': 'kun',
         'ちゃん': 'chan', '殿': 'dono', 'どの': 'dono'}
GLOSS_OK = ROOT / 'script' / 'glossary_ok.txt'


def glossary_ok():
    """{id: {JP term}}: reviewed per-string exceptions to glossary/honorific errors (id<TAB>term<TAB>reason)."""
    ok = {}
    if GLOSS_OK.exists():
        for ln in GLOSS_OK.read_text(encoding='utf-8').splitlines():
            if ln.strip() and not ln.startswith('#'):
                i, term, reason = ln.split('\t')
                assert reason.strip(), ln
                ok.setdefault(i, set()).add(term)
    return ok


def problems(u, en, var, gl, ok=()):
    if not en.strip():
        return ['empty English']
    errs = []
    bad = sorted({c for c in TOKEN.sub('', en) if not ' ' <= c <= '~' or c in '{}[]'})
    if bad:
        errs.append(f'characters outside printable ASCII, or stray braces/brackets: {bad}')
    if '\\u' in en or '\\n' in en:
        errs.append('escape sequence in the English (write the character; {n} for a forced break)')
    a = Counter(t for t in TOKEN.findall(u['jp']) if t not in FREE)
    b = Counter(t for t in TOKEN.findall(en) if t not in FREE)
    if a != b:
        errs.append(f'codes differ: JP {dict(a)} EN {dict(b)}')
    if re.search(r'\{(MM|R\d)\}(st|nd|rd|th)\b', en):
        errs.append('ordinal suffix glued to a variable (write "No. {R0}")')
    for r, v in boxes(u, var):
        errs += [f'[{v}] {e}' for e in layout.render(r, v, en)[1]]
    plain = TOKEN.sub('', u['jp'])
    for j, e, avoid, person in gl:
        for a_ in avoid:
            if re.search(rf'\b{re.escape(a_)}\b', en):
                errs.append(f'glossary: "{a_}" is an avoided spelling of {j} -> {e}')
        if not has_term(plain, j):
            continue
        stem = e.lower()[:-1] + 'i' if e.endswith('y') else e.lower()    # trophy -> trophies
        if e.lower() not in en.lower() and stem not in en.lower() and j not in ok:
            errs.append(f'glossary: {j} -> {e} not in the English (fix, or report GLOSSARY: id term reason)')
        for m in re.finditer(re.escape(j) + '(' + '|'.join(HONOR) + ')', plain) if person else ():
            want = f'{e.split()[-1]}-{HONOR[m.group(1)]}'          # D1: honorifics kept, hyphenated
            if (m.start() == 0 or kind(plain[m.start() - 1]) != kind(j[0])) and want.lower() not in en.lower() \
                    and m.group(0) not in ok:
                errs.append(f'honorific: {m.group(0)} -> {want} not in the English')
    return errs


def check(name, us=None, var=None, gl=None):
    rows = read_tsv(TL / f'{name}.tsv')
    out_path = TL / f'{name}.out.tsv'
    if not out_path.exists():
        print(f'{name}: no {out_path.name}')
        return None
    us = us or {u['id']: u for u in units().values()}
    var = var or windows.variants()
    gl = gl if gl is not None else glossary()
    got, errs = {}, []
    for k, line in enumerate(out_path.read_text(encoding='utf-8').splitlines(), 1):
        if not line.strip():
            continue
        if line.count('\t') != 1:
            errs.append(f'line {k}: need exactly one tab (id<TAB>English)')
            continue
        i, en = line.split('\t')
        if i in got:
            errs.append(f'{i}: duplicate id')
        got[i] = en
    want = [r[0] for r in rows]
    errs += [f'{i}: missing' for i in want if i not in got]
    errs += [f'{i}: not in this batch' for i in got if i not in set(want)]
    ok = glossary_ok()
    for i in want:
        if i in got and i in us:
            errs += [f'{i}: {x}' for x in problems(us[i], got[i], var, gl, ok.get(i, ()))]
    for e in errs:
        print('ERROR', e)
    print(f'{name}: {"OK" if not errs else f"{len(errs)} errors"} ({len(got)} entries)')
    return got if not errs else None


def merge(names):
    us = {u['id']: u for u in units().values()}
    var, gl = windows.variants(), glossary()
    trans = {}
    for name in names:
        got = check(name, us, var, gl)
        if got is None:
            sys.exit(f'{name} failed its check; nothing merged')
        trans.update(got)
    by_jp = {us[i]['jp']: en for i, en in trans.items() if i in us}
    nfiles = 0
    for p in sorted((ROOT / 'script').glob('*.json')):
        rows = json.loads(p.read_text(encoding='utf-8'))
        changed = False
        for r in rows:
            en = by_jp.get(r['jp'])
            if en is not None and not skip(r) and r.get('en') != en:
                r['en'] = en
                changed = True
        if changed:
            p.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding='utf-8', newline='\n')
            nfiles += 1
    print(f'merged {len(trans)} entries into {nfiles} files')


def main(argv):
    cmd, rest = (argv[0], argv[1:]) if argv else ('', [])
    if cmd == 'split':
        split(rest)
    elif cmd == 'check':
        us, var, gl = {u['id']: u for u in units().values()}, windows.variants(), glossary()
        sys.exit(0 if all([check(n, us, var, gl) is not None for n in rest]) else 1)
    elif cmd == 'merge':
        merge(rest)
    elif cmd == 'terms':
        terms(rest)
    elif cmd == 'todo':
        left = [u for u in units().values() if not u['en']]
        print(len(left), 'units,', sum(len(TOKEN.sub('', u['jp'])) for u in left), 'JP chars untranslated')
    else:
        sys.exit(__doc__)


if __name__ == '__main__':
    main(sys.argv[1:])
