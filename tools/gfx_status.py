"""Full Hermit label on the Status staff, assembled across two atlas fragments.

The original 仙 sits on the wooden staff badge, not on the character's hat.
Keep the wood silhouette, staff grain, cloud, beard and animation unchanged.
"""
from PIL import Image, ImageFilter

PIECES = ((120, 88, 32, 16, 0, 0), (216, 0, 32, 16, 0, 16))
ERASE = ((5, 10, 25, 23), (3, 15, 5, 18))
UNIT_ROWS = (80, 122, 143)


def clear_units(im):
    # The second row contains no unit. Its exact background and shaded border
    # repeat at 21px intervals. The final bottom border at y=164 stays intact.
    blank = im.crop((224, 101, 240, 122))
    for y in UNIT_ROWS:
        im.paste(blank, (224, y))


def draw(im, pal):
    import gen_gfx

    badge = Image.new('RGBA', (32, 32))
    for u, v, w, h, x, y in PIECES:
        badge.paste(im.crop((u, v, u + w, v + h)), (x, y))
    wood, gold, shadow = (152, 136, 112, 255), (224, 144, 0, 255), (56, 48, 32, 255)
    assert {wood, gold, shadow} <= pal
    for rect in ERASE:
        badge.paste(wood, rect)
    letters = Image.new('L', badge.size)
    for row, word in enumerate(('HER', 'MIT')):
        mask = gen_gfx.mask(word, 7, {'pixel': 'credits7.txt', 'tight': True})
        letters.paste(mask, ((32 - mask.width) // 2, 8 + row * 8))
    border = letters.filter(ImageFilter.MaxFilter(3))
    badge.paste(shadow, (0, 0), border)
    badge.paste(gold, (0, 0), letters)
    for u, v, w, h, x, y in PIECES:
        im.paste(badge.crop((x, y, x + w, y + h)), (u, v))
