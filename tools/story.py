"""Write story-pass chapter files (work/qa/story/chapters/*.txt) from script/*.json.

usage: python -X utf8 tools/story.py [OUT]

A chapter is a run of villages in play order (docs/synopsis.md): village NN = GSVNN*/GSFNN*/GSSNN* files,
in resource order; events and the ending overlay close the story. Minigame, menu and shop text had its
per-batch review in phase 6 and is not a story chapter.
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
CHAPTERS = {
    '01_tabidachi': range(0, 2), '02_villages_02_04': range(2, 5), '03_villages_05_07': range(5, 8),
    '04_villages_08_09': range(8, 10), '05_villages_10_12': range(10, 13), '06_village_13': range(13, 14),
    '07_village_16': range(14, 17), '08_villages_19_25': range(17, 30), '09_villages_30_40': range(30, 41),
}
EVENTS = 'EVT*.json', 'OVLEVT.json'  # appended to the last chapter


def files():
    """chapter -> script files, every GSV/GSF/GSS/EVT file assigned once."""
    out = {c: [] for c in CHAPTERS}
    for f in sorted(glob.glob(os.path.join(ROOT, 'script', 'GS[VFS]*.json'))):
        n = int(re.match(r'GS[VFS](\d\d)', os.path.basename(f)).group(1))
        out[next(c for c, r in CHAPTERS.items() if n in r)].append(f)
    for pat in EVENTS:
        out['09_villages_30_40'] += sorted(glob.glob(os.path.join(ROOT, 'script', pat)))
    return out


def generate(out):
    os.makedirs(out, exist_ok=True)
    for chapter, fs in files().items():
        lines = [f'# {chapter}', 'Read with docs/synopsis.md, docs/style-reference.md and glossary.md.',
                 'Resource order per file; conditional NPC responses are alternatives, not one conversation.',
                 'Speaker is not stored in the script: infer it from the JP.', '']
        for f in fs:
            lines.append(f'## {os.path.basename(f)[:-5]}')
            for s in json.load(open(f, encoding='utf-8')):
                if not s.get('en'):
                    continue
                lines += [f'>> {s["id"]} | - | {s["jp"]}'.replace('\n', ' / '), s['en'], '']
        with open(os.path.join(out, chapter + '.txt'), 'w', encoding='utf-8', newline='\n') as h:
            h.write('\n'.join(lines))


def diff(ref, out):
    """Per chapter: entries whose English changed since git REF (for a focused re-review)."""
    import subprocess
    os.makedirs(out, exist_ok=True)
    for chapter, fs in files().items():
        lines = []
        for f in fs:
            rel = os.path.relpath(f, ROOT).replace('\\', '/')
            got = subprocess.run(['git', 'show', f'{ref}:{rel}'], cwd=ROOT, capture_output=True)
            old = {s['id']: s.get('en') for s in json.loads(got.stdout.decode('utf-8'))} if got.returncode == 0 else {}
            for s in json.load(open(f, encoding='utf-8')):
                if old.get(s['id']) != s.get('en'):
                    lines += [f'>> {s["id"]} | {s["jp"]}'.replace('\n', ' / '), f'OLD: {old.get(s["id"])}',
                              f'NEW: {s.get("en")}', '']
        with open(os.path.join(out, chapter + '.txt'), 'w', encoding='utf-8', newline='\n') as h:
            h.write('\n'.join(lines))
        print(chapter, len(lines) // 4)


if __name__ == '__main__':
    every = [f for fs in files().values() for f in fs]
    assert len(every) == len(set(every)), 'file in two chapters'
    if sys.argv[1:2] == ['--diff']:  # story.py --diff REF [OUT]
        diff(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else os.path.join(ROOT, 'work', 'qa', 'story', 'diffs'))
    else:
        generate(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'work', 'qa', 'story', 'chapters'))
