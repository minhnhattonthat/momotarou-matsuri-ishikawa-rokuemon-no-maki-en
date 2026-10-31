"""English redraws of graphics text -> gfx/en/*.png (tools/gfx.py writes them into the build).

    python -X utf8 tools/gen_gfx.py              regenerate every redraw in LABELS
    python -X utf8 tools/gen_gfx.py boxes FILE:E [--gap N]   bounding boxes of the image's opaque pieces

LABELS: {"FILE:ENTRY": [(x0, y0, x1, y1, "English", opts), ...]}. Each rect is cleared (to transparent, or with
bg='fill' to the rect's most common colour, for labels on a panel) and the English drawn centred in it with
fonts/ofl/Fredoka.ttf (OFL), no antialiasing. Colours come from the Japanese lettering in the rect: the fill per
row is that row's most common lettering colour (keeps vertical gradients), the outline is the darkest colour.
opts: size (px, default fits the rect), wdth 75-125, wght 300-700, outline 0/1, fill (RGBA tuple) to force one,
align 'left' (menu labels; default centred).
"""
import sys
from collections import Counter
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import arc  # noqa: E402
import gfx  # noqa: E402
import tim  # noqa: E402

FONT = ROOT / 'fonts' / 'ofl' / 'Fredoka.ttf'
CLEAR = (0, 0, 0, 0)

LABELS = {
    # title: press-start prompt (the logo pieces are separate rows of docs/re/gfx_survey.tsv #6)
    # two sprites: line 1 is as wide as スタートボタンを, line 2 only as wide as おしてね! (x 49..122)
    'CI0D.BIN:3': [(49, 49, 175, 65, 'Press START', {'bg': 'fill', 'outline': 0}),
                   (49, 65, 122, 81, 'button!', {'bg': 'fill', 'outline': 0})],
    # Game Album menu: title + three mode labels (glossary; おためし対戦 as in the script, "Quick Match!")
    'NAME0D.BIN:0': [(81, 0, 241, 25, 'Game Album', {}),
                     (0, 145, 97, 168, 'Rank Details', {'wdth': 75, 'align': 'left'}),
                     (0, 168, 160, 191, 'Quick Match!', {'align': 'left'}),
                     (0, 192, 184, 216, 'Name Entry', {'align': 'left'})],
}


def luma(c):
    return c[0] * 3 + c[1] * 6 + c[2]


def font(size, o):
    f = ImageFont.truetype(str(FONT), size)
    f.set_variation_by_axes([o.get('wght', 600), o.get('wdth', 100)])
    return f


def mask(text, size, o):
    f = font(size, o)
    l, t, r, b = f.getbbox(text)
    m = Image.new('L', (r - l + 2, b - t + 2))
    ImageDraw.Draw(m).text((1 - l, 1 - t), text, font=f, fill=255)
    return m.point(lambda v: 255 if v >= 128 else 0)


def fit(text, w, h, o):
    pad = 2 if o.get('outline', 1) else 0
    for size in range(o.get('size', 64), 5, -1):
        m = mask(text, size, o)
        if m.width + pad <= w and m.height + pad <= h:
            return m
    raise ValueError(f'{text!r} does not fit {w}x{h}')


def draw(im, x0, y0, x1, y1, text, o, pal):
    px = im.load()
    rect = [px[x, y] for y in range(y0, y1) for x in range(x0, x1)]
    bgc = Counter(rect).most_common(1)[0][0] if o.get('bg') == 'fill' else CLEAR
    ink = [c for c in rect if c[3] and c != bgc]
    if not ink:
        raise ValueError(f'{text!r}: no lettering in {(x0, y0, x1, y1)}')
    dark = min(set(ink), key=luma)
    rows = {}
    for y in range(y0, y1):
        cs = Counter(px[x, y] for x in range(x0, x1) if px[x, y][3] and px[x, y] not in (bgc, dark))
        if cs:
            rows[y] = cs.most_common(1)[0][0]
    fallback = Counter(c for c in ink if c != dark).most_common(1)[0][0] if len(set(ink)) > 1 else dark
    for y in range(y0, y1):
        for x in range(x0, x1):
            px[x, y] = bgc
    m = fit(text, x1 - x0, y1 - y0, o)
    ox = x0 + 1 if o.get('align') == 'left' else x0 + (x1 - x0 - m.width) // 2
    oy = y0 + (y1 - y0 - m.height) // 2
    full = Image.new('L', im.size)
    full.paste(m, (ox, oy))
    edge = full.filter(ImageFilter.MaxFilter(3)) if o.get('outline', 1) else full
    fm, em = full.load(), edge.load()
    lettered = [y for y in range(y0, y1) if any(fm[x, y] for x in range(x0, x1))]
    span = [y for y in sorted(rows)] or [y0]
    for y in range(y0, y1):
        # map the new lettering's rows onto the old lettering's rows, so a gradient keeps its order
        if lettered:
            k = (y - lettered[0]) * len(span) // max(1, len(lettered))
            fill = o.get('fill') or rows.get(span[min(max(k, 0), len(span) - 1)], fallback)
        else:
            fill = fallback
        for x in range(x0, x1):
            if fm[x, y]:
                px[x, y] = fill
            elif em[x, y]:
                px[x, y] = dark
    assert all(px[x, y] in pal for y in range(y0, y1) for x in range(x0, x1))


def original(key, p=0):
    name, _, e = key.partition(':')
    t, _ = gfx.unpack(arc.entries((gfx.TREE / name).read_bytes())[int(e)][1])
    return t, tim.image(t, p)


def copies():
    """{TIM bytes: [FILE:ENTRY, ...]} over every archive: the same image often ships in several files."""
    out = {}
    for f in sorted(gfx.TREE.glob('*.BIN')):
        for i, (_, ent) in enumerate(arc.entries(f.read_bytes()) or []):
            if ent[:4] in (b'ECD\x01', b'\x10\0\0\0'):
                try:
                    out.setdefault(gfx.unpack(ent)[0], []).append(f'{f.name}:{i}')
                except ValueError:
                    pass
    return out


def generate():
    gfx.EN.mkdir(parents=True, exist_ok=True)
    same = copies()
    for key, labels in LABELS.items():
        t, im = original(key)
        pal = {c if c[3] else CLEAR for c in gfx.palette(t, 0)}
        im = Image.eval(im, lambda v: v)
        im.putdata([c if c[3] else CLEAR for c in im.getdata()])
        for x0, y0, x1, y1, text, o in labels:
            draw(im, x0, y0, x1, y1, text, o, pal)
        for k in same[t]:
            name, _, e = k.partition(':')
            out = gfx.EN / f'{Path(name).stem}_{e}.png'
            im.save(out)
            print(out.relative_to(ROOT), gfx.changed_box(t, out))


def boxes(key, gap=2):
    _, im = original(key)
    a = im.getchannel('A').point(lambda v: 255 if v else 0).filter(ImageFilter.MaxFilter(2 * gap + 1))
    w, h = im.size
    px, seen = a.load(), set()
    for y in range(h):
        for x in range(w):
            if px[x, y] and (x, y) not in seen:
                st, bb = [(x, y)], [x, y, x, y]
                seen.add((x, y))
                while st:
                    cx, cy = st.pop()
                    bb = [min(bb[0], cx), min(bb[1], cy), max(bb[2], cx), max(bb[3], cy)]
                    for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                        if 0 <= nx < w and 0 <= ny < h and px[nx, ny] and (nx, ny) not in seen:
                            seen.add((nx, ny))
                            st.append((nx, ny))
                if (bb[2] - bb[0]) * (bb[3] - bb[1]) > 16:
                    print(bb[0] + gap, bb[1] + gap, bb[2] - gap + 1, bb[3] - gap + 1)


if __name__ == '__main__':
    if sys.argv[1:2] == ['boxes']:
        boxes(sys.argv[2], int(sys.argv[sys.argv.index('--gap') + 1]) if '--gap' in sys.argv else 2)
    else:
        generate()
