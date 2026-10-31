"""Text lint over every merged English line (check.py runs it): the batch check (codes, ASCII, layout in every box
the JP is drawn in, glossary, honorifics) again on script/ `en`, so later glossary or budget changes fail old lines.
Hand-set rows (money templates, save titles) get their own checks.

    python -X utf8 tools/lint.py          exit 1 on any error
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import batches  # noqa: E402
import insert  # noqa: E402
import layout  # noqa: E402
import text  # noqa: E402
import windows  # noqa: E402


def errors():
    var, gl, ok = windows.variants(), batches.glossary(), batches.glossary_ok()
    errs = []
    for u in batches.units().values():
        en = {r.get('en', '') for r in u['rows']}
        if len(en) > 1:
            errs.append(f"{u['id']}: rows with the same JP differ in English")
        if u['en']:
            errs += [f"{u['id']}: {e}" for e in batches.problems(u, u['en'], var, gl, ok.get(u['id'], ()))]
        # an exception is keyed by the unit's first row: every twin needs its own reviewed line (or a by_id row)
        if u['id'] in ok:
            errs += [f"{r['id']}: shares a glossary exception with {u['id']}; list it in glossary_ok.txt or "
                     f"override it in by_id.tsv" for r in u['rows'] if r['id'] not in ok]
    menus = {}
    for rows in insert.rows_by_file().values():
        for r in rows:
            if var.get(r['id'], '').startswith('choice') and r.get('en'):
                menus.setdefault(r['id'].rsplit('.', 1)[0], []).append(r)
    for key, rs in menus.items():
        seen = {}
        for r in rs:
            if seen.setdefault(r['en'], r['jp']) != r['jp']:
                errs.append(f"{r['id']}: \"{r['en']}\" repeats another choice of {key} with different JP")
    for rows in insert.rows_by_file().values():
        for r in rows:
            if not r.get('en') or not batches.skip(r):
                continue
            if r['id'] in insert.SJIS_ONLY:
                if re.search(r'[\x20-\x7e]', r['en']) or len(text.encode_text(r['en'])) > insert.SJIS_ONLY[r['id']]:
                    errs.append(f"{r['id']}: save title must be full-width, <= {insert.SJIS_ONLY[r['id']]} bytes")
            elif '[20]' in r['jp']:
                slots = re.match(r'(?:\[20\])*', r['jp']).group()
                fits = len(text.encode_text(r['en'])) <= r['max'] - 1 or r['id'].startswith(layout.RELOC)  # RELOC: moved
                if not r['en'].startswith(slots) or not fits:
                    errs.append(f"{r['id']}: money template keeps its {len(slots) // 4} digit slots, fits max")
    return errs


if __name__ == '__main__':
    es = errors()
    for e in es:
        print('LINT', e)
    print(f'lint: {len(es)} errors')
    sys.exit(1 if es else 0)
