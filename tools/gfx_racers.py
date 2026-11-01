"""Thirty Rabbit-Turtle Race names, originally assembled from kana sprites.

Store whole English names below the old font, where the original ANMs have no
users. Keep each item's original record count, left anchor, palette and flags;
the first record draws the name and the others sample a transparent texel.
"""
import csv
import hashlib
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[1]
ANM_SHA1 = '27810d3328f186e8ba9fa4b0baf1a29b60a7d16f'
UNITS_SHA1 = 'f68f1b0842ad7453a6861ebcc66a61e96eedc270'
RECT = (0, 136, 256, 216)
# 位 is a rank suffix after a number: English uses list punctuation (1., 2.,
# etc.), avoiding an ordinal suffix that would be wrong for some positions.
UNITS = ['.', 'Lane', 'Time', 'Hit', 'ryo']
KANA = ['ヲアイウエオカキクケコサシスセソ', 'タチツテトナニヌネノハヒフヘホマ',
        'ミムメモヤユヨラリルレロワンガギ', 'グゲゴザジズゼゾダヂヅデドバビブ',
        'ベボパピプペポァィゥェォャュョッ']


def original_names(data):
    import anm
    alphabet = {0xB0 + y * 16 + x: c for y, row in enumerate(KANA) for x, c in enumerate(row)}
    alphabet[0x2D] = 'ー'
    return [''.join(alphabet[r[2] // 8 * 16 + r[1] // 8] for r in sorted(item, key=lambda r: r[8]))
            for item in anm.items(data)]


def rows():
    with (ROOT / 'gfx/racers.tsv').open(encoding='utf-8', newline='') as source:
        result = list(csv.DictReader(source, delimiter='\t'))
    if [int(row['item']) for row in result] != list(range(30)):
        raise ValueError('race names must cover items 0 through 29 in order')
    return result


def mask(name):
    import gen_gfx
    return gen_gfx.fit(name, 50, 8, {'pixel': 'credits7.txt', 'outline': 0, 'tight': True})


def rect(item, name):
    return (item % 4 * 64, 136 + item // 4 * 8, mask(name).width, 8)


def unit_rect(item):
    return (item % 4 * 64, 200 + item // 4 * 8, mask(UNITS[item]).width, 8)


def draw(image, palette):
    clear, white = (0, 0, 0, 0), (248, 248, 248, 255)
    if clear not in palette or white not in palette:
        raise ValueError('unexpected race font palette')
    if image.crop(RECT).getchannel('A').getbbox():
        raise ValueError('race name destination is not transparent')
    for item, row in enumerate(rows()):
        u, v, _, _ = rect(item, row['en'])
        image.paste(white, (u, v), mask(row['en']))
    for item, text in enumerate(UNITS):
        u, v, _, _ = unit_rect(item)
        glyphs = mask(text)
        image.paste(white, (u, v + 7 - glyphs.height), glyphs)


def patch(data):
    if hashlib.sha1(data).hexdigest() != ANM_SHA1:
        raise ValueError('unexpected original M230D race-name ANM')
    if original_names(data) != [row['jp'] for row in rows()]:
        raise ValueError('race-name transcription differs from the source sprites')
    out = bytearray(data)
    table, = struct.unpack_from('<I', data, 8)
    for item, row in enumerate(rows()):
        start, = struct.unpack_from('<I', data, table + item * 4)
        count, = struct.unpack_from('<I', data, start)
        anchors = [struct.unpack_from('<hh', data, start + 4 + sprite * 28 + 16) for sprite in range(count)]
        left, top = min(x for x, _ in anchors), min(y for _, y in anchors)
        for sprite in range(count):
            geometry = (*rect(item, row['en']), left, top) if sprite == 0 else (255, 255, 1, 1, 0, 0)
            for field, value in zip((1, 2, 3, 4, 8, 9), geometry):
                struct.pack_into('<H', out, start + 4 + sprite * 28 + field * 2, value & 0xFFFF)
    return bytes(out)


def patch_units(data):
    if hashlib.sha1(data).hexdigest() != UNITS_SHA1:
        raise ValueError('unexpected original M230D race-label ANM')
    out = bytearray(data)
    table, = struct.unpack_from('<I', data, 8)
    for item in range(len(UNITS)):
        start, = struct.unpack_from('<I', data, table + item * 4)
        count, = struct.unpack_from('<I', data, start)
        left, top = struct.unpack_from('<hh', data, start + 4 + 16)
        for sprite in range(count):
            geometry = (*unit_rect(item), left, top) if sprite == 0 else (255, 255, 1, 1, 0, 0)
            for field, value in zip((1, 2, 3, 4, 8, 9), geometry):
                struct.pack_into('<H', out, start + 4 + sprite * 28 + field * 2, value & 0xFFFF)
    return bytes(out)
