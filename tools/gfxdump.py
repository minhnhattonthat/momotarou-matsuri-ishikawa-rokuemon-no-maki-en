"""Static graphics sweep (phase 1 survey): every TIM on the disc, deduplicated, rendered into numbered sheets.

usage: python -X utf8 tools/gfxdump.py [--out work/gfx]
Writes <out>/sheet_NNN.png (labelled cells) and <out>/index.tsv (id, sheet, file, entry offset, size, copies).
Prints every skipped entry with the reason.
"""
import argparse, glob, hashlib, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import arc, ecd, tim

TREE = os.path.join(os.path.dirname(__file__), '..', 'work', 'disc', 'tree', 'OUTBIN')


def collect():
    seen = {}
    for f in sorted(glob.glob(os.path.join(TREE, '*.BIN'))):
        d = open(f, 'rb').read()
        es = arc.entries(d)
        if es is None:
            continue
        for i, (o, e) in enumerate(es):
            if e[:4] == ecd.MAGIC:
                u = ecd.decompress(e)
            elif e[:4] == b'\x10\0\0\0':
                u = e
            else:
                continue
            if u[:4] != b'\x10\0\0\0':
                continue  # CLUT-only (0x11)
            h = hashlib.sha1(u).hexdigest()
            if h in seen:
                seen[h][2].append(f'{os.path.basename(f)}:{i}')
            else:
                seen[h] = [u, f'{os.path.basename(f)}:{i}@{o:x}', []]
    return list(seen.values())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default='work/gfx')
    ap.add_argument('--per', type=int, default=12)
    a = ap.parse_args()
    from PIL import Image, ImageDraw
    os.makedirs(a.out, exist_ok=True)
    items = collect()
    idx = open(os.path.join(a.out, 'index.tsv'), 'w', encoding='utf-8')
    idx.write('id\tsheet\tsource\tw\th\tcopies\n')
    for s in range(0, len(items), a.per):
        cells = []
        for n, (u, src, copies) in enumerate(items[s:s + a.per], s):
            try:
                im = tim.image(u)
            except Exception as ex:
                print('skip', src, ex)
                continue
            cells.append((n, src, im))
            idx.write(f'{n}\t{s // a.per:03d}\t{src}\t{im.width}\t{im.height}\t{" ".join(copies)}\n')
        W = 1024
        rows, x, y, rh = [], 0, 0, 0
        place = []
        for n, src, im in cells:
            w, h = min(im.width, W), im.height + 12
            if x + w > W:
                x, y, rh = 0, y + rh + 4, 0
            place.append((x, y, n, src, im))
            x += w + 4; rh = max(rh, h)
        sheet = Image.new('RGBA', (W, y + rh + 4), (255, 0, 255, 255))
        dr = ImageDraw.Draw(sheet)
        for x, y, n, src, im in place:
            dr.rectangle([x, y, x + min(im.width, W) - 1, y + 11], fill=(0, 0, 0, 255))
            dr.text((x + 1, y), f'#{n} {src}', fill=(255, 255, 0, 255))
            sheet.alpha_composite(im.crop((0, 0, min(im.width, W), im.height)), (x, y + 12))
        sheet.save(os.path.join(a.out, f'sheet_{s // a.per:03d}.png'))
    print(len(items), 'unique images ->', a.out)


if __name__ == '__main__':
    main()
