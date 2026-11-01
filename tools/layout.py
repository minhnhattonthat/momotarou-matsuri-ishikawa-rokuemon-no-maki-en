"""English layout: a translator's English -> the game's line format for its box (budgets: tools/windows.py).

    python -X utf8 tools/layout.py "English text" [--box msg|msg_portrait|choice|caption|...] [--jp ID]

English form (script/<FILE>.json `en`, translator batches): no line breaks; pages separated by {KP} (at least as
many as the Japanese has), {KN} at the end where the Japanese ends with it, {n} = forced line break (rare: a quote
followed by narration, verse). Other codes exactly as in the Japanese: {MM} name, {R0}-{R3} number, {bb}{rr}{oo}
{dd}..{ww} colour, [XX] bytes. Code strings (kind code): one line, no {n}/{KP}; memory-card lines keep {KK}/{KE}.
render() wraps each page greedily to the px budget (a page starting with a quote hangs its later lines by one
space, like the Japanese 「 indent), max 3 lines per page, and pads each page with full-width-space lines to the
Japanese page's line count so the box clears the same way.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import engine  # noqa: E402
import text  # noqa: E402
import windows  # noqa: E402

CODE = re.compile(r'\{\w+\}|\[[0-9A-F]{2}\]')
# shortcut: inserted name/number widths are guesses (item names <= ~16 chars, numbers <= 4 full-width digits);
# measure the longest in phase 8 and raise these if a line overruns.
VAR_W = {'{MM}': 84, '{R0}': 52, '{R1}': 52, '{R2}': 52, '{R3}': 52}
PAD = '　'
PAGE_LINES = 3
# code files whose strings may outgrow `max`: insert.patch_code relocates them into slack (EXE, OVLM*, OVLGMAIN:
# English fills their Japanese bytes, holes <= 6 bytes)
RELOC = ('OVLXTTL@',)
_W = []


def width(s):
    if not _W:
        _W.extend(engine.widths())
    return engine.width_px(s, _W) + sum(VAR_W.get(t, 0) for t in CODE.findall(s))


def units(line):
    return len(text.encode_text(line)) // 2 + 1


def jp_page_lines(jp):
    return [seg.lstrip('\n').count('\n') + 1 for seg in jp.replace('{KN}', '').split('{KP}')]


def wrap(page, px, indent=''):
    lines = []
    for seg in page.split('{n}'):
        seg = seg.strip()
        hang = ' ' if seg.startswith('"') else ''
        cur = indent
        for w in seg.split():
            trial = cur + ' ' + w if cur.strip() else cur + w
            if cur.strip() and (width(trial) > px or units(trial) > windows.LINE_UNITS):
                lines.append(cur)
                cur = indent + hang + w
            else:
                cur = trial
        lines.append(cur)
    return lines


def render_msg(en, jp, px, indent=''):
    errs = []
    kn = en.rstrip().endswith('{KN}')
    body = re.sub(r'\{KN\}\s*$', '', en.rstrip())
    pages = [p.strip() for p in body.split('{KP}')]
    want = jp_page_lines(jp)
    out = []
    for i, p in enumerate(pages):
        if not p:
            errs.append(f'page {i + 1} is empty')
        lines = wrap(p, px, indent)
        for ln in lines:
            if width(ln) > px:
                errs.append(f'page {i + 1}: {width(ln)} px > {px}: {ln!r}')
            if units(ln) > windows.LINE_UNITS:
                errs.append(f'page {i + 1}: {units(ln)} units > {windows.LINE_UNITS}: {ln!r}')
        if len(lines) > PAGE_LINES:
            errs.append(f'page {i + 1}: {len(lines)} lines > {PAGE_LINES} (split it with {{KP}})')
        last = i == len(pages) - 1
        target = want[i] if len(pages) == len(want) else (want[-1] if last else PAGE_LINES)
        lines += [PAD] * (target - len(lines))
        out.append('\n'.join(lines) + ('{KN}' if last and kn else '' if last else '{KP}'))
    if len(pages) < len(want):
        errs.append(f'{len(pages)} pages < Japanese {len(want)} (keep every {{KP}})')
    if kn != jp.endswith('{KN}'):
        errs.append('{KN} at the end must match the Japanese')
    return '\n'.join(out), errs


def render_line(en, row, px, soft=False):
    """soft: px budget is a guess (code strings: JP design width), so only the in-place byte cap is an error."""
    errs = []
    if re.search(r'\{(n|KP|KN)\}', en):
        errs.append('one-line text: no {n}/{KP}/{KN}')
    lines = en.replace('{KE}', '').split('{KK}')
    if row.get('jp', '').endswith('{KE}'):          # memory-card message: lines split on the KK/KE bytes
        if len(lines) > 3:
            errs.append(f'{len(lines)} lines > 3')
        for ln in lines:
            b = text.encode_text(ln)
            if b'KK' in b or b'KE' in b or len(b) > 64:
                errs.append(f'memory-card line: no "KK"/"KE" letter pairs, <= 64 bytes: {ln!r}')
    for ln in lines:
        if width(ln) > px and not soft:
            errs.append(f'{width(ln)} px > {px}: {ln!r}')
    if row.get('max') is not None and len(text.encode_text(en)) > row['max'] and not row['id'].startswith(RELOC):
        errs.append(f'{len(text.encode_text(en))} bytes > in-place max {row["max"]} (shorten, or report LONG)')
    return en, errs


def render(row, variant, en=None):
    """(game-format text, [error]) for row's English (en or row['en']) in its box."""
    en = row['en'] if en is None else en
    px, _, tag = windows.budget(row, variant)
    if row['kind'] == 'msg':
        return render_msg(en, row['jp'], px, indent=PAD * 4 if variant == 'msg_mask' else '')
    return render_line(en, row, px, soft=tag == 'guess')


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a or a[0].startswith('-'):
        sys.exit(__doc__)
    box = a[a.index('--box') + 1] if '--box' in a else 'msg'
    if '--jp' in a:
        import json
        rid = a[a.index('--jp') + 1]
        row = next(r for p in (ROOT / 'script').glob('*.json') for r in json.loads(p.read_text(encoding='utf-8'))
                   if r['id'] == rid)
        box = windows.variants()[rid]
    else:
        row = {'kind': 'msg' if box.startswith('msg') else 'menu', 'jp': a[0], 'id': ''}
    out, errs = render(row, box, a[0])
    print(f'box {box}, {windows.budget(row, box)[0]} px')
    for ln in out.split('\n'):
        print(f'{width(ln):4d} px | {ln}')
    for e in errs:
        print('ERROR', e)
    sys.exit(1 if errs else 0)
