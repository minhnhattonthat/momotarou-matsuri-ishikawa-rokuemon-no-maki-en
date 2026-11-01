"""English redraws of graphics text -> gfx/en/*.png (tools/gfx.py writes them into the build).

    python -X utf8 tools/gen_gfx.py              regenerate every redraw in LABELS
    python -X utf8 tools/gen_gfx.py boxes FILE:E [--gap N]   bounding boxes of the image's opaque pieces

LABELS: {"FILE:ENTRY": [(x0, y0, x1, y1, "English", opts), ...]}. Each rect is cleared (to transparent, or with
bg='fill' to the rect's most common colour, for labels on a panel) and the English drawn centred in it with
fonts/ofl/Fredoka.ttf (OFL), no antialiasing. Colours come from the Japanese lettering in the rect: the fill per
row is that row's most common lettering colour (keeps vertical gradients), the outline is the darkest colour.
opts: size (px, default fits the rect), wdth 75-125, wght 300-700, outline 0/1, fill (RGBA tuple) to force one,
align 'left' (menu labels; default centred). bg='neutral' removes grey lettering by borrowing the nearest
coloured pixel on the same row, preserving coloured rank-plate artwork; edge overrides the outline colour.
pixel=True uses the native 7-pixel capitals in fonts/hud7.txt instead of the rounded font (small HUD words).
"""
import sys
from collections import Counter
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import arc  # noqa: E402
import engine  # noqa: E402
import gfx  # noqa: E402
import tim  # noqa: E402

FONT = ROOT / 'fonts' / 'ofl' / 'Fredoka.ttf'
CLEAR = (0, 0, 0, 0)
HUD = {'pixel': True, 'outline': 0, 'fill': (248, 248, 248, 255)}

LABELS = {
    # M990D ANM entry 2 references these as whole words (tools/anm.py), not shared characters.
    # Keep the original word rectangles so the HUD's fixed number positions remain valid.
    'M990D.BIN:0': [
        (176, 0, 208, 16, 'Score', HUD),
        (208, 0, 240, 16, 'Record', HUD),
        (80, 0, 112, 16, 'Time', HUD),
        (64, 16, 96, 32, 'Course', HUD),
        (96, 16, 136, 32, 'Stage', HUD),
        (176, 16, 192, 32, 'ryo', HUD),
        (88, 32, 152, 48, 'Bonus', HUD),
    ],
    'M110D.BIN:0': [
        (0, 184, 112, 208, 'Ready...', {}),
        (112, 184, 168, 208, 'Go!', {}),
        (0, 208, 56, 240, 'Win!', {}),
        (56, 208, 112, 240, 'Lose!', {}),
        (112, 208, 208, 240, 'Draw!', {}),
    ],
    'M560D.BIN:1': [
        (0, 0, 56, 32, 'Win!', {}),
        (56, 0, 112, 32, 'Lose!', {}),
        (112, 0, 208, 32, 'Draw!', {}),
    ],
    'M590D.BIN:6': [
        (0, 0, 56, 32, 'Win!', {}),
        (56, 0, 112, 32, 'Lose!', {}),
        (112, 0, 208, 32, 'Draw!', {}),
    ],
    'M590D.BIN:0': [
        (144, 80, 240, 112, 'Draw!', {}),
        (144, 112, 200, 144, 'Win!', {}),
        # The exclamation mark is a separate sprite; the word's source is only 40 px wide.
        (200, 112, 240, 144, 'Lose', {}),
    ],
    'M140D.BIN:0': [
        (184, 128, 240, 160, 'Win!', {}),
        (184, 160, 240, 192, 'Lose!', {}),
        (184, 192, 216, 208, 'Streak', {'size': 11, 'wdth': 75, 'outline': 0}),
    ],
    'M010D.BIN:4': [
        (0, 0, 152, 32, 'Perfect!', {}),
        (0, 32, 152, 64, 'Hit Award!', {}),
        (0, 64, 120, 96, 'Bonus Award', {}),
        (120, 64, 144, 96, '!', {}),
        (0, 96, 144, 128, 'Sharp Eye!', {}),
        (0, 128, 144, 160, 'Survivor!', {}),
    ],
    'M030D.BIN:3': [(0, 216, 176, 248, 'Perfect!', {})],
    # title: press-start prompt (the logo pieces are separate rows of docs/re/gfx_survey.tsv #6)
    # two sprites: line 1 is as wide as スタートボタンを, line 2 only as wide as おしてね! (x 49..122)
    'CI0D.BIN:3': [(49, 49, 175, 65, 'Press START', {'bg': 'fill', 'outline': 0}),
                   (49, 65, 122, 81, 'button!', {'bg': 'fill', 'outline': 0})],
    # Game Album menu: title + three mode labels (glossary; おためし対戦 as in the script, "Quick Match!")
    'NAME0D.BIN:0': [(81, 0, 241, 25, 'Game Album', {}),
                     (0, 145, 97, 168, 'Rank Details', {'wdth': 75, 'align': 'left'}),
                     (0, 168, 160, 191, 'Quick Match!', {'align': 'left'}),
                     (0, 192, 184, 216, 'Name Entry', {'align': 'left'})],
    'STATUS0D.BIN:0': [
        (0, 55, 111, 80, 'Status', {}),
        (0, 83, 66, 105, 'Rank', {'outline': 0, 'fill': (8, 8, 8, 255)}),
        (68, 83, 89, 105, ' ', {'outline': 0}),
        (90, 83, 111, 105, ' ', {'outline': 0}),
        (0, 110, 91, 129, 'Full Mastery', {'wdth': 75, 'outline': 0, 'fill': (8, 8, 8, 255)}),
        (1, 131, 112, 148, 'Total Cards', {'bg': 'fill', 'outline': 0, 'align': 'left', 'size': 14,
                                         'fill': (8, 8, 8, 255)}),
        (1, 153, 93, 169, 'Play Time', {'bg': 'fill', 'outline': 0, 'align': 'left', 'size': 14,
                                      'fill': (8, 8, 8, 255)}),
        (1, 174, 113, 191, 'Steps', {'bg': 'fill', 'outline': 0, 'align': 'left', 'size': 11,
                                   'fill': (8, 8, 8, 255)}),
        (1, 195, 112, 212, 'Money (ryo)', {'bg': 'fill', 'outline': 0, 'align': 'left', 'size': 14,
                                   'fill': (8, 8, 8, 255)}),
        # Counts already have an English label; Japanese counter suffixes are redundant.
        (224, 81, 239, 104, ' ', {'bg': 'fill', 'outline': 0}),
        (224, 114, 239, 139, ' ', {'bg': 'fill', 'outline': 0}),
        (224, 146, 239, 172, ' ', {'bg': 'fill', 'outline': 0}),
        (114, 82, 223, 106, 'Momotaro', {'bg': 'neutral', 'fill': (8, 8, 8, 255),
                                       'edge': (248, 248, 248, 255)}),
        (114, 114, 223, 139, 'Momotaro Master', {'bg': 'neutral', 'wdth': 75, 'fill': (8, 8, 8, 255),
                                              'edge': (248, 248, 248, 255)}),
        (114, 146, 223, 171, 'Momotaro Expert', {'bg': 'neutral', 'wdth': 75, 'fill': (8, 8, 8, 255),
                                              'edge': (248, 248, 248, 255)}),
        (114, 178, 223, 203, 'Momotaro Hermit', {'bg': 'neutral', 'wdth': 75, 'fill': (8, 8, 8, 255),
                                              'edge': (248, 248, 248, 255)}),
    ],
}


def luma(c):
    return c[0] * 3 + c[1] * 6 + c[2]


def font(size, o):
    f = ImageFont.truetype(str(FONT), size)
    f.set_variation_by_axes([o.get('wght', 600), o.get('wdth', 100)])
    return f


def mask(text, size, o):
    if o.get('pixel'):
        glyphs = engine.glyphs(ROOT / 'fonts' / 'hud7.txt')
        rows = [glyphs[c] for c in text.upper()]
        widths = [max(map(len, g)) for g in rows]
        m = Image.new('L', (sum(widths) + len(rows) + 1, 9))
        x = 1
        for g, width in zip(rows, widths):
            for y, row in enumerate(g):
                for dx, pixel in enumerate(row):
                    if pixel == '#':
                        m.putpixel((x + dx, y + 1), 255)
            x += width + 1
        return m
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
    dark = o.get('edge', min(set(ink), key=luma))
    rows = {}
    for y in range(y0, y1):
        cs = Counter(px[x, y] for x in range(x0, x1) if px[x, y][3] and px[x, y] not in (bgc, dark))
        if cs:
            rows[y] = cs.most_common(1)[0][0]
    fallback = Counter(c for c in ink if c != dark).most_common(1)[0][0] if len(set(ink)) > 1 else dark
    for y in range(y0, y1):
        if o.get('bg') == 'neutral':
            background = {x: px[x, y] for x in range(x0, x1)
                          if px[x, y][3] and max(px[x, y][:3]) - min(px[x, y][:3]) > 24}
            if not background:
                # The middle stripe of the Master plate is entirely white.
                background = {x0: max((px[x, y] for x in range(x0, x1)), key=luma)}
            for x in range(x0, x1):
                if max(px[x, y][:3]) - min(px[x, y][:3]) <= 24:
                    px[x, y] = background[min(background, key=lambda sx: abs(sx - x))]
        else:
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
    return same


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
        same = generate()
        import gen_credits
        gen_credits.generate(same=same)
