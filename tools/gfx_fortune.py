"""Fortune God's four ふ badge cells, preserving hands and badge outlines."""
KEY = 'M490D.BIN:0'
# Half-open interior spans, one per row. The two throwing poses have a
# hand/cloth fold crossing the left edge; the third also covers the right.
BADGES = (
    (46, ((36, 48), (35, 50), (35, 50), (35, 50), (35, 50), (36, 49), (36, 49), (38, 47)), (40, 46)),
    (15, ((84, 96), (83, 98), (83, 98), (83, 98), (83, 98), (84, 97), (84, 97), (86, 95)), (88, 15)),
    (14, ((145, 148), (144, 148), (144, 148), (144, 149), (143, 150), (143, 151), (143, 150), (142, 146)), (144, 14)),
    (45, ((201, 208), (200, 210), (200, 210), (200, 210), (199, 210), (199, 209), (198, 209), (198, 207)), (200, 45)),
)


def pixels():
    return {(x, y0 + row) for y0, spans, _ in BADGES
            for row, (left, right) in enumerate(spans) for x in range(left, right)}


def rectangles():
    return [(left, y0 + row, right, y0 + row + 1) for y0, spans, _ in BADGES
            for row, (left, right) in enumerate(spans)]


def draw(image, palette):
    import gen_gfx
    ink = (48, 32, 0, 255)
    background = (232, 232, 0, 255)
    assert ink in palette and background in palette
    letter = gen_gfx.mask('F', 7, {'pixel': True, 'tight': True})
    assert letter.size == (4, 7)
    for y0, spans, (gx, gy) in BADGES:
        for row, (left, right) in enumerate(spans):
            y = y0 + row
            for x in range(left, right):
                on = 0 <= x - gx < letter.width and 0 <= y - gy < letter.height
                image.putpixel((x, y), ink if on and letter.getpixel((x - gx, y - gy)) else background)
