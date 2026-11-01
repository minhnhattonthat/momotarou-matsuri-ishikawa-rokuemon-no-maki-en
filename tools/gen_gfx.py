"""English redraws of graphics text -> gfx/en/*.png (tools/gfx.py writes them into the build).

    python -X utf8 tools/gen_gfx.py              regenerate every redraw in LABELS
    python -X utf8 tools/gen_gfx.py --only FILE:E ...  regenerate selected atlases and all identical copies
    python -X utf8 tools/gen_gfx.py boxes FILE:E [--gap N]   bounding boxes of the image's opaque pieces

LABELS: {"FILE:ENTRY": [(x0, y0, x1, y1, "English", opts), ...]}. Each rect is cleared (to transparent, or with
bg='fill' to the rect's most common colour, for labels on a panel) and the English drawn centred in it with
fonts/ofl/Fredoka.ttf (OFL), no antialiasing. Colours come from the Japanese lettering in the rect: the fill per
row is that row's most common lettering colour (keeps vertical gradients), the outline is the darkest colour.
opts: size (px, default fits the rect), wdth 75-125, wght 300-700, outline 0/1, fill (RGBA tuple) to force one,
align 'left' (menu labels; default centred). bg='neutral' removes grey lettering by borrowing the nearest
coloured pixel on the same row, preserving coloured rank-plate artwork; edge overrides the outline colour.
pixel=True uses the native 7-pixel capitals in fonts/hud7.txt instead of the rounded font (small HUD words).
For a named pixel font, tight=True trims blank mask margins. source=(x0,y0,x1,y1) borrows an original
rectangle's colours for a relocated label; list it before any redraw of that source rectangle.
COMPOSITES letters disjoint fragments in assembled screen space before scattering pixels back to the atlas.
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
import gfx_results  # noqa: E402
import gfx_racers  # noqa: E402
import gfx_hud  # noqa: E402
import gfx_signs  # noqa: E402
import gfx_intro  # noqa: E402
import gfx_event_props  # noqa: E402
import gfx_event_crowns  # noqa: E402
import gfx_welcome  # noqa: E402
import gfx_fortune  # noqa: E402
import gfx_tanuki  # noqa: E402
import gfx_tanuki_bibs  # noqa: E402
import gfx_status  # noqa: E402
import gfx_props  # noqa: E402
import name_entry  # noqa: E402

FONT = ROOT / 'fonts' / 'ofl' / 'Fredoka.ttf'
CLEAR = (0, 0, 0, 0)
# The dark town's CLUT 0 aliases wood index 11 and lettering index 12.
# CLUT 1 separates them, so the PNG can roundtrip their intended indices.
EDIT_PALETTES = {'GV30002D.BIN:0': 1}
HUD = {'pixel': True, 'outline': 0, 'fill': (248, 248, 248, 255)}
HUD_CONDENSED = {**HUD, 'pixel': 'credits7.txt', 'tight': True}
PANEL = {'bg': 'fill', 'outline': 0, 'align': 'left', 'size': 14, 'fill': (8, 8, 8, 255)}
MASK_BUTTON = {'bg': 'fill', 'outline': 0, 'size': 17, 'fill': (248, 248, 248, 255)}
MASK_DIM = {**MASK_BUTTON, 'fill': (128, 128, 128, 255)}

LABELS = {
    'NAME0D.BIN:1': [],  # Latin player-name font, also copied to PREM0D:1.
    # Attract-mode character introductions. Yashahime is assembled from three
    # fragments below; none of these name rectangles includes character art.
    'CHR0D.BIN:1': [(120, 208, 208, 240, 'Momotaro', {})],
    'CHR0D.BIN:2': [
        (0, 192, 88, 224, 'Kintaro', {}),
        (200, 184, 256, 216, 'Urashima', {'wdth': 75}),
        (88, 216, 256, 248, 'Ishikawa Rokuemon', {'wdth': 75}),
    ],
    **{key: [] for key in gfx_signs.SIGNS},
    **{key: [] for key in gfx_props.PROPS},
    **{key: [] for key in gfx_event_props.KEYS},
    **{key: [] for key in gfx_event_crowns.CROWNS},
    gfx_welcome.KEY: [],
    gfx_fortune.KEY: [],
    gfx_tanuki_bibs.KEY: [],
    'M340D.BIN:1': [],  # gfx_hud extends the counter panel for the full word "times".
    'M050D.BIN:2': [(0, 136, 64, 152, 'Jackpot!', {})],
    'M060D.BIN:2': [
        # Level 1 uses a whole 56px strip; levels 2/3 reuse only its first
        # 40px and append another number. Keep all three number cells intact.
        (170, 4, 208, 19, 'Level', {**PANEL, 'pixel': 'credits7.txt', 'align': 'center'}),
        (170, 28, 220, 43, 'Heave!', {**PANEL, 'pixel': 'credits7.txt', 'align': 'center'}),
        (170, 52, 220, 67, 'Ho!', {**PANEL, 'pixel': 'credits7.txt', 'align': 'center'}),
        (170, 76, 220, 91, 'Not yet!', {**PANEL, 'pixel': 'credits7.txt', 'align': 'center'}),
        (170, 100, 220, 115, 'Go for it!', {**PANEL, 'pixel': 'credits7.txt', 'align': 'center'}),
    ],
    'M080D.BIN:6': [(48, 32, 144, 56, 'One away!', {})],
    'M180D.BIN:3': [(128, 16, 160, 32, 'Miss', HUD)],
    'M230D.BIN:0': [
        # Reletter the sign interior while preserving its coloured frame.
        (3, 211, 53, 220, 'Rabbit', {**HUD_CONDENSED, 'bg': 'fill'}),
        (3, 220, 53, 229, 'Turtle', {**HUD_CONDENSED, 'bg': 'fill'}),
        (3, 229, 53, 237, 'Race', {**HUD_CONDENSED, 'bg': 'fill'}),
    ],
    'M230D.BIN:3': [],  # gfx_racers draws names into unused pixels below the font.
    'M500D.BIN:0': [
        (128, 128, 192, 144, 'Start', {}),
        # Poverty God's single-character bib emblem, as on the cards. These
        # four interiors share the complete kana mask; retain cloth edges.
        *[(x, y, x + 13, y + 8, 'P',
           {'bg': 'fill', 'pixel': True, 'tight': True, 'outline': 0, 'fill': (80, 80, 80, 255)})
          for x, y in ((26, 60), (90, 61), (154, 60), (26, 133))],
    ],
    'M250D.BIN:21': [(0, 32, 136, 56, 'Mask Album', {})],
    'M250D.BIN:22': [
        # Clear lettering only; preserve the beveled button edges and both states.
        (12, 60, 52, 100, 'Done', MASK_BUTTON),
        (68, 60, 108, 100, 'Redo', MASK_BUTTON),
        (12, 108, 52, 148, 'Done', MASK_DIM),
        (68, 108, 108, 148, 'Redo', MASK_DIM),
        (123, 58, 165, 70, 'L1', {**MASK_BUTTON, 'size': 14}),
        (123, 74, 165, 86, 'R1', {**MASK_BUTTON, 'size': 14}),
        (123, 106, 165, 118, 'L1', {**MASK_DIM, 'size': 14}),
        (123, 122, 165, 134, 'R1', {**MASK_DIM, 'size': 14}),
    ],
    'HOUGEN0D.BIN:0': [
        (0, 56, 160, 80, 'Card Album', {}),
        (160, 56, 184, 80, ' ', {}),
        (6, 109, 90, 126, 'Hokkaido', PANEL),
        (6, 129, 90, 146, 'Tohoku', PANEL),
        (6, 149, 90, 166, 'Kanto', PANEL),
        (6, 169, 90, 186, 'Chubu', PANEL),
        (6, 189, 90, 206, 'Kinki', PANEL),
        (6, 209, 90, 226, 'Chugoku-Shikoku', {**PANEL, 'pixel': 'credits7.txt'}),
        (6, 229, 90, 246, 'Kyushu-Okinawa', {**PANEL, 'pixel': 'credits7.txt'}),
        *[(149, y, 166, y + 17, ' ', {'bg': 'fill', 'outline': 0}) for y in range(109, 230, 20)],
    ],
    # Keep the rank announcements' shared exclamation at (200,40,16,40).
    # M990D:3 item 11 reads the complete 216px row; items 1-10 reuse its last 16px.
    'M990D.BIN:1': [
        (0, 40, 200, 80, 'New Record', {}),
        (0, 80, 192, 128, 'Level Up', {}),
        (216, 40, 256, 80, '1', {}),
        # The header already says Level; leave just the number and its shared ! below.
        (216, 80, 256, 120, ' ', {}),
        (0, 128, 160, 168, 'Full Mastery', {'wdth': 75}),
        (0, 168, 120, 200, 'Finish!', {}),
        (0, 200, 128, 232, 'Draw!', {}),
        # gfx_layout.py rejoins START and removes the Japanese borrowed dash.
        (160, 128, 248, 160, 'Game', {}),
        (128, 200, 216, 232, 'Start', {}),
    ],
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
        (192, 144, 208, 160, 'Race', HUD_CONDENSED),
        (208, 144, 240, 160, 'Weather', HUD_CONDENSED),
        (192, 160, 224, 176, 'Forecast', HUD_CONDENSED),
        (0, 176, 32, 192, 'Entry', HUD),
        (32, 176, 96, 192, 'Race Result', HUD_CONDENSED),
        (96, 176, 128, 192, 'Slow', HUD_CONDENSED),
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
        # The old second Lose sprite shares pixels with an actor. Give the
        # complete English banner its own unused rectangle (gfx_layout.py).
        (0, 208, 56, 240, 'Lose!', {'source': (200, 112, 240, 144)}),
        (144, 80, 240, 112, 'Draw!', {}),
        (144, 112, 200, 144, 'Win!', {}),
        # Keep the old 40px main-word region English too; its actor-shared tail
        # is no longer used by the relocated result sprite.
        (200, 112, 240, 144, 'Lose', {}),
    ],
    'M140D.BIN:0': [
        (184, 128, 240, 160, 'Win!', {}),
        (184, 160, 240, 192, 'Lose!', {}),
        (184, 192, 216, 208, 'Streak', {**HUD_CONDENSED, 'outline': 1}),
    ],
    'M010D.BIN:4': [
        # Item 4 adds the separately stored ! at (120,64,24,32).
        (0, 0, 152, 32, 'Perfect', {}),
        (0, 32, 152, 64, 'Hit Award!', {}),
        (0, 64, 120, 96, 'Bonus Award', {}),
        (120, 64, 144, 96, '!', {}),
        (0, 96, 144, 128, 'Sharp Eye!', {}),
        (0, 128, 144, 160, 'Survivor!', {}),
    ],
    'M030D.BIN:1': [(152, 176, 184, 184, 'Which?', HUD_CONDENSED)],
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
        (0, 56, 112, 80, 'Status', {}),
        (0, 83, 64, 104, 'Rank', {'outline': 0, 'fill': (8, 8, 8, 255)}),
        (64, 80, 88, 104, ' ', {'outline': 0}),
        (88, 80, 112, 104, ' ', {'outline': 0}),
        (0, 106, 88, 128, 'Full Mastery', {'wdth': 75, 'outline': 0, 'fill': (8, 8, 8, 255)}),
        (1, 131, 112, 148, 'Total Cards', {'bg': 'fill', 'outline': 0, 'align': 'left', 'size': 11,
                                         'fill': (8, 8, 8, 255)}),
        (1, 153, 93, 169, 'Play Time', {'bg': 'fill', 'outline': 0, 'align': 'left', 'size': 14,
                                      'fill': (8, 8, 8, 255)}),
        # Seven digits start at screen x=95; the left label starts at x=65.
        # Small pixel capitals leave a gap even for 9,999,999 steps/ryo.
        (1, 174, 112, 191, 'Steps', {**HUD_CONDENSED, 'bg': 'fill', 'align': 'left',
                                   'fill': (8, 8, 8, 255)}),
        (1, 195, 112, 204, 'Money', {**HUD_CONDENSED, 'bg': 'fill', 'align': 'left',
                                   'fill': (8, 8, 8, 255)}),
        (1, 204, 112, 212, 'ryo', {**HUD_CONDENSED, 'bg': 'fill', 'align': 'left',
                                   'fill': (8, 8, 8, 255)}),
        # gfx_status restores the counter suffix backgrounds without cutting
        # panel borders; the right-hand fragment is only 12 opaque pixels wide.
        (114, 82, 223, 106, 'Momotaro', {'bg': 'neutral', 'fill': (8, 8, 8, 255),
                                       'edge': (248, 248, 248, 255)}),
        (114, 114, 223, 139, 'Momotaro Master', {'bg': 'neutral', 'wdth': 75, 'fill': (8, 8, 8, 255),
                                              'edge': (248, 248, 248, 255)}),
        (114, 146, 223, 171, 'Momotaro Expert', {'bg': 'neutral', 'wdth': 75, 'fill': (8, 8, 8, 255),
                                              'edge': (248, 248, 248, 255)}),
        (114, 178, 223, 203, 'Momotaro Hermit', {'bg': 'neutral', 'wdth': 75, 'fill': (8, 8, 8, 255),
                                              'edge': (248, 248, 248, 255)}),
    ],
    'STATUS0D.BIN:1': [],  # gfx_status translates the split staff badge.
}

# Cards 25-27 (Tokyo), 54-56 (Osaka), 59-61 (Nara), 62-64 (Wakayama),
# 75-77 (Tokushima), and 80-82 (Ehime) have three entries; the other prefectures two.
# The name strip is a separate 120x16 sprite. Leave NO.### and the illustration intact.
PREFECTURES = [
    ('Hokkaido', 2), ('Aomori', 2), ('Iwate', 2), ('Miyagi', 2), ('Akita', 2),
    ('Yamagata', 2), ('Fukushima', 2), ('Ibaraki', 2), ('Tochigi', 2), ('Gunma', 2),
    ('Saitama', 2), ('Chiba', 2), ('Tokyo', 3), ('Kanagawa', 2), ('Niigata', 2),
    ('Toyama', 2), ('Ishikawa', 2), ('Fukui', 2), ('Yamanashi', 2), ('Nagano', 2),
    ('Gifu', 2), ('Shizuoka', 2), ('Aichi', 2), ('Mie', 2), ('Shiga', 2),
    ('Kyoto', 2), ('Osaka', 3), ('Hyogo', 2), ('Nara', 3), ('Wakayama', 3),
    ('Tottori', 2), ('Shimane', 2), ('Okayama', 2), ('Hiroshima', 2), ('Yamaguchi', 2),
    ('Tokushima', 3), ('Kagawa', 2), ('Ehime', 3), ('Kochi', 2), ('Fukuoka', 2),
    ('Saga', 2), ('Nagasaki', 2), ('Kumamoto', 2), ('Oita', 2), ('Miyazaki', 2),
    ('Kagoshima', 2), ('Okinawa', 2),
]
for _i, _name in enumerate(name for name, count in PREFECTURES for _ in range(count)):
    LABELS[f'HCARD{_i // 10}0D.BIN:{_i % 10}'] = [
        (48, 128, 120, 144, _name, {'bg': 'fill', 'outline': 0, 'size': 14, 'fill': (8, 8, 8, 255)}),
    ]

# (source x, source y, width, height, assembled x, assembled y).
# Good Work's last two kana are a separate sprite. Pause is split into top/bottom
# halves stored side-by-side. Letter the assembled image, then scatter it back.
COMPOSITES = {
    'CHR0D.BIN:2': [
        ('Yashahime', [(0, 224, 88, 16, 0, 0), (88, 200, 80, 16, 8, 16),
                       (0, 240, 8, 16, 0, 16)]),
    ],
    'M990D.BIN:1': [
        ('Good Work', [(120, 168, 136, 32, 0, 0), (216, 200, 32, 32, 136, 0)]),
        ('Pause', [(0, 232, 96, 16, 0, 0), (96, 232, 96, 16, 0, 16)]),
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
        filename = o['pixel'] if isinstance(o['pixel'], str) else 'hud7.txt'
        glyphs = engine.glyphs(ROOT / 'fonts' / filename)
        rows = [glyphs[c] if c != ' ' else ['..'] * 7 for c in text.upper()]
        widths = [max(map(len, g)) for g in rows]
        m = Image.new('L', (sum(widths) + len(rows) + 1, 9))
        x = 1
        for g, width in zip(rows, widths):
            for y, row in enumerate(g):
                for dx, pixel in enumerate(row):
                    if pixel == '#':
                        m.putpixel((x + dx, y + 1), 255)
            x += width + 1
        return m.crop(m.getbbox()) if o.get('tight') and m.getbbox() else m
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
    if o.get('source'):
        im.paste(im.crop(o['source']).resize((x1 - x0, y1 - y0), Image.Resampling.NEAREST), (x0, y0))
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


def original(key, p=None):
    name, _, e = key.partition(':')
    t, _ = gfx.unpack(arc.entries((gfx.TREE / name).read_bytes())[int(e)][1])
    return t, tim.image(t, EDIT_PALETTES.get(key, 0) if p is None else p)


def png_path(key, palette=None):
    name, entry = key.split(':')
    palette = EDIT_PALETTES.get(key, 0) if palette is None else palette
    return gfx.EN / f'{Path(name).stem}_{entry}{f"_p{palette}" if palette else ""}.png'


def redrawn(key):
    return gfx.redraw(original(key)[0], png_path(key), EDIT_PALETTES.get(key, 0))


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


def generate(keys=None):
    gfx.EN.mkdir(parents=True, exist_ok=True)
    same = copies()
    if keys and set(keys) - LABELS.keys():
        raise ValueError(f'unknown atlas keys: {set(keys) - LABELS.keys()}')
    for key, labels in LABELS.items():
        if keys and key not in keys:
            continue
        t, im = original(key)
        editing_palette = EDIT_PALETTES.get(key, 0)
        pal = {c if c[3] else CLEAR for c in gfx.palette(t, editing_palette)}
        im = Image.eval(im, lambda v: v)
        im.putdata([c if c[3] else CLEAR for c in im.getdata()])
        for x0, y0, x1, y1, text, o in labels:
            draw(im, x0, y0, x1, y1, text, o, pal)
        for text, pieces in COMPOSITES.get(key, []):
            width = max(x + w for _, _, w, _, x, _ in pieces)
            height = max(y + h for _, _, _, h, _, y in pieces)
            assembled = Image.new('RGBA', (width, height))
            for u, v, w, h, x, y in pieces:
                assembled.paste(im.crop((u, v, u + w, v + h)), (x, y))
            draw(assembled, 0, 0, width, height, text, {}, pal)
            for u, v, w, h, x, y in pieces:
                im.paste(assembled.crop((x, y, x + w, y + h)), (u, v))
        if key == 'M990D.BIN:0':
            gfx_results.draw(im, pal)
            gfx_hud.draw(im, pal)
        if key == 'M230D.BIN:3':
            gfx_racers.draw(im, pal)
        if key == 'M340D.BIN:1':
            gfx_hud.draw_panel(im)
        if key in gfx_signs.SIGNS:
            gfx_signs.draw(im, key, pal)
        if key in gfx_props.PROPS:
            gfx_props.draw(im, key, pal)
        if key.startswith('CHR0D.BIN:'):
            gfx_intro.draw(im, key, pal)
        if key in gfx_event_props.KEYS:
            gfx_event_props.draw(im, key, pal)
        if key in gfx_event_crowns.CROWNS:
            gfx_event_crowns.draw(im, key, pal)
        if key == gfx_welcome.KEY:
            gfx_welcome.draw(im, pal)
        if key == gfx_fortune.KEY:
            gfx_fortune.draw(im, pal)
        if key == gfx_tanuki.KEY:
            gfx_tanuki.draw(im, pal)
        if key == gfx_tanuki_bibs.KEY:
            gfx_tanuki_bibs.draw(im, pal)
        if key == 'STATUS0D.BIN:1':
            gfx_status.draw(im, pal)
        if key == 'STATUS0D.BIN:0':
            gfx_status.clear_units(im)
        if key == 'NAME0D.BIN:1':
            name_entry.draw(im)
        for k in same[t]:
            out = png_path(k, editing_palette)
            im.save(out)
            print(out.relative_to(ROOT), gfx.changed_box(t, out, editing_palette))
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
    elif sys.argv[1:2] == ['--only'] and len(sys.argv) > 2:
        generate(sys.argv[2:])
    else:
        same = generate()
        import gen_credits
        gen_credits.generate(same=same)
        import gen_card_words
        gen_card_words.generate()
