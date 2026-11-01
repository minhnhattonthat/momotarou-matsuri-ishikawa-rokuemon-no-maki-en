"""Kintaro's eight gold bib initials in Even Tanuki, preserving hands and rims."""
from PIL import Image

KEY = 'M140D.BIN:2'
# Each row is a half-open span inside the yellow badge. Side and eating poses
# have narrower spans where a hand or cloth fold covers the badge.
SHAPES = (
    ((-2, 4), (-2, 5), (-2, 5), (-2, 6), (-2, 5), (-2, 5), (-2, 5)),
    ((-1, 4), (-2, 5), (-2, 5), (-1, 6), (-1, 5), (0, 5), (0, 5)),
    ((-1, 3), (-2, 5), (-1, 5), (-1, 6), (-1, 5), (-1, 5), (-1, 5)),
    ((-1, 3), (-2, 5), (-2, 5), (-2, 6), (-2, 5), (-2, 5), (-2, 5)),
)
# (first ink x/y, shape). The native letter is replaced with the same K used
# on the snow statue/card costumes, drawn as a small unambiguous pixel initial.
BADGES = ((62, 143, 0), (110, 144, 0), (20, 200, 0),
          (56, 194, 1), (92, 193, 2), (140, 194, 3),
          (180, 193, 0), (222, 214, 0))


def rectangles():
    return [(x + left, y + row, x + right, y + row + 1)
            for x, y, shape in BADGES
            for row, (left, right) in enumerate(SHAPES[shape])]


def draw(image, palette):
    ink, gold = (80, 72, 16, 255), (240, 240, 0, 255)
    assert ink in palette and gold in palette
    # A three-pixel K collapses into two bars at native size. The five-pixel
    # tall initial keeps both diagonal arms connected, below the eating hands.
    letter = Image.new('L', (4, 5))
    for y, row in enumerate(('#..#', '#.#.', '##..', '#.#.', '#..#')):
        for x, pixel in enumerate(row):
            if pixel == '#':
                letter.putpixel((x, y), 255)
    for x, y, shape in BADGES:
        for row, (left, right) in enumerate(SHAPES[shape]):
            for dx in range(left, right):
                image.putpixel((x + dx, y + row),
                               ink if 0 <= dx < letter.width and 1 <= row < 6
                               and letter.getpixel((dx, row - 1)) else gold)
