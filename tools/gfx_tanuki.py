"""Even Tanuki's upright/tilted 勝負 scrolls: MATCH, with mounts/stamps intact."""
from PIL import Image

KEY = 'M140D.BIN:0'
# Paper interiors, excluding the green binding, shaded paper edges and red seal.
TILTED_SPANS = (
    (165, 175), (164, 176), (164, 176), (165, 177), (165, 177),
    (165, 177), (165, 177), (166, 178), (166, 178), (166, 178),
    (166, 178), (167, 179), (167, 179), (167, 179), (168, 179),
    (168, 179), (168, 179), (169, 179), (169, 179), (169, 179), (169, 179),
)


def rectangles():
    return [(166, 133, 178, 154)] + [
        (left, 175 + row, right, 176 + row)
        for row, (left, right) in enumerate(TILTED_SPANS)]


def draw(image, palette):
    import gen_gfx
    paper, ink = (248, 248, 240, 255), (80, 80, 80, 255)
    assert paper in palette and ink in palette
    for left, top, right, bottom in rectangles():
        for y in range(top, bottom):
            for x in range(left, right):
                image.putpixel((x, y), paper)
    label = gen_gfx.mask('Match', 7, {'pixel': 'credits7.txt', 'tight': True})
    label = label.transpose(Image.Transpose.ROTATE_270)
    assert label.size == (7, 21)
    for y in range(label.height):
        for x in range(label.width):
            if label.getpixel((x, y)):
                image.putpixel((168 + x, 133 + y), ink)
                # The second drawing slopes right as it descends. Follow its
                # paper rather than rotating the whole sprite and its binding.
                image.putpixel((167 + x + y // 4, 175 + y), ink)
