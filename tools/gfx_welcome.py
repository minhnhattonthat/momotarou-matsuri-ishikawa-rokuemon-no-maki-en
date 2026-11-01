"""EVT220's village welcome illustration, assembled from its native ANM.

Item 1 splits a 264x128 picture into three rectangles on TIM 1. The banner
crosses the first two rectangles; redraw in picture space, then scatter back.
"""
from PIL import Image, ImageDraw

KEY = 'EVT220D.BIN:1'
PIECES = ((0, 0, 184, 128, 0, 0), (0, 128, 80, 72, 184, 0),
          (80, 128, 80, 56, 184, 72))
# Excludes the banner's shaded rim and four tacks. The lower edge slopes
# down to the right, like the original cloth.
INTERIOR = ((168, 18), (219, 18), (219, 35), (179, 34), (168, 32))
RECTS = ((168, 18, 184, 35), (0, 146, 36, 164))


def assemble(texture):
    picture = Image.new('RGBA', (264, 128))
    for u, v, w, h, x, y in PIECES:
        picture.paste(texture.crop((u, v, u + w, v + h)), (x, y))
    return picture


def scatter(picture, texture):
    for u, v, w, h, x, y in PIECES:
        texture.paste(picture.crop((x, y, x + w, y + h)), (u, v))


def draw(texture, palette):
    import gen_gfx
    picture = assemble(texture)
    ImageDraw.Draw(picture).polygon(INTERIOR, fill=(248, 248, 248, 255))
    letters = gen_gfx.mask('Welcome!!', 7, {'pixel': 'credits7.txt', 'tight': True})
    assert letters.width <= 50 and letters.height == 7
    x0 = 169 + (50 - letters.width) // 2
    # Follow the slight slope without scaling or antialiasing the glyphs.
    for x in range(letters.width):
        y = 23 + x // 18
        picture.paste((0, 0, 0, 255), (x0 + x, y, x0 + x + 1, y + 7),
                      letters.crop((x, 0, x + 1, 7)))
    scatter(picture, texture)
    assert set(texture.getdata()) <= palette


if __name__ == '__main__':
    import gen_gfx
    target = gen_gfx.ROOT / 'work/gfx/welcome_assembled.png'
    assemble(gen_gfx.original(KEY)[1]).save(target)
    print(target)
