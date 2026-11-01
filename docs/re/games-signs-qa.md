# Games shop boards, 2026-11-01

Five more field atlases now say **Games** for ゆうぎ. Six cold map contexts
on each disc contain the complete lettering, and a fresh read-only D10 pass
accepts all twelve scoped context/detail sheets. Other Games variants, shop
signs and the phase-wide graphics/interaction work remain open.

## Additional bath-town and island signs

Later checkpoint: **GV16000D:3 and GV22000D:1** now say Games as well. The
byte-identical M220D:3 copy is regenerated automatically. Five more cold
original/English map pairs pass the complete-lettering oracle, and a fresh
read-only D10 pass accepts all ten context/detail sheets. This brings the
accepted field routes in this document to eleven, across seven source atlases.

| Atlas | Pieces `(u,v,w,h,x,y)` | Lettering in assembled space | Map/player position | Palette |
| --- | --- | --- | --- | --- |
| GV16000D:3 | `(0,40,96,48,0,0)` | `(23,16)-(73,31)` | 180:27,79 | 3 |
| GV22000D:1 | `(128,48,64,32,0,0)` + `(176,96,32,32,64,0)` | `(23,16)-(69,31)` | 237/238:17,16 and 87,40 | rain remap / sunny CLUT 14 |

The island board's right edge is stored on a separate atlas row. The first
attempt omitted that fragment; visual review rejected the residual kana and
the generator now clears/draws in the complete assembled board. Preservation
tests now map every declared piece, including that tail. All pixels outside
the lettering remain unchanged. The original uncorrected captures under
`games_more8_en` and their review are rejected, not release evidence.

Rain changes the whole sign palette. Map237 explicitly opts into an exact
one-to-one colour-remapping check: every opaque pixel, including the wood
between letters, must match its template's pattern. A flat panel, missing edge
or altered glyph fails. The coverage row says `weather-remapped`, not a guessed
CLUT number. This checks geometry only; the fresh visual pass separately
confirms that the English darkness matches the original rain palette.

```
python -X utf8 tools/gen_gfx.py --only GV16000D.BIN:3 GV22000D.BIN:1
python -X utf8 tools/build.py
python -X utf8 tools/debug/signs_tour.py --out work/qa/games_more8_fixed --jobs 2 --only games180 games237a games237b games238a games238b
python -X utf8 tools/debug/signs_tour.py --original --out work/qa/games_more8_jp --jobs 2 --only games180 games237a games237b games238a games238b
python -X utf8 tools/debug/field_signs_review.py work/qa/games_more8_fixed work/qa/games_more8_jp --out work/qa/games_more8_fixed_review
```

The scoped manifest gate is **10/10 ok**, textlog **0 Japanese lines in 5 logs**,
full check **105 tests / lint 0**, verifier **375 changed files / 0 errors**, cold
smoke `games_more8_smoke` passed. Disc: **182454048 bytes**, **2026-11-01
12:10:14 UTC**, SHA-1 `a55a142561d6bb35cd67b479a08e9692f57434c3`.

| Case | Context SHA-1 | Detail SHA-1 | D10 verdict |
| --- | --- | --- | --- |
| games180 | 028f3da574229d25bba7fbd0fae528ec7ce6037d | 29589b3484a64ff7d3c68a802b369217749c7282 | ok |
| games237a | e3b5d989a4cc08c83a877d01d281d6dfcdfa1e50 | af30bca7b762e3a92311298ce223b2235fd60896 | ok |
| games237b | d4ab335f5899e9f8e54f761141d3543fa7432203 | af30bca7b762e3a92311298ce223b2235fd60896 | ok |
| games238a | 4323764bcc571eeb7009a27169558a3ea733925f | d232287ccec2a3d3933c6fbd88189c9b7472c09e | ok |
| games238b | 8fe8ae97542960cf4fda8e39d4e540f0bc077632 | d232287ccec2a3d3933c6fbd88189c9b7472c09e | ok |

M22's natural cold route reaches gameplay but does not show this board in the
captured view; the duplicate has static preservation proof only. GV36000D:1
still needs classification: the inspected brown strip has knobs/wood grain
and no legible Games word, so it was not changed on a guessed transcription.
Other roof signs in GV16000D:3 remain Japanese. Phase 8 remains incomplete.

## Placement and palette

`tools/gfx_signs.py` reletters only a 46x15 rectangle inside each original
wooden board. Credits7 is scaled exactly 2x with nearest-neighbour sampling.
Every pixel outside the lettering rectangle is preserved, including the roof,
board silhouette, other signs and surrounding tiles.

| Atlas | Lettering rectangle | Cold map/player position | Active CLUT |
| --- | --- | --- | --- |
| GV12000D:1 | 151,16 to 197,31 | 143: 120,26 | 9 |
| GV12002D:1 | 151,16 to 197,31 | 144: 120,26 | 9 |
| GV13000D:1 | 119,192 to 165,207 | 163: 57,32 | 10 |
| GV32000D:1 | 87,144 to 133,159 | 295: 19,27 | 10 |
| GV34000D:1 | 55,224 to 101,239 | 306: 21,26 and 60,42 | 11 |

Two failures were caught and corrected by cold visual review. CLUT-0 index 1
looks cream in the editing atlas but becomes dark blue/purple at runtime;
the original lettering uses index 12, which becomes cream in CLUTs 9-11.
The first wood repair also borrowed roof pixels at the narrow board's edge
in maps 163 and 295. It now admits only wood indices 7-11. Regression checks
require cream-index lettering, exclude roof indices from the repaired area,
and preserve every pixel outside the declared lettering rectangle.

The complete-pixel oracle correctly matched the initial bad-colour build:
matching built pixels proves assembly, not readability or correct art.
Visual review remains necessary. Review sheets now use the exact successful
coverage frame, not an arrival shot that can precede the completed warp.

## Reproduction

```
python -X utf8 tools/gen_gfx.py --only GV12000D.BIN:1 GV12002D.BIN:1 GV13000D.BIN:1 GV32000D.BIN:1 GV34000D.BIN:1
python -X utf8 tools/build.py
python -X utf8 tools/debug/signs_tour.py --out work/qa/games_signs8_fixed --jobs 1 --only games143 games144 games163 games295 games306a games306b
python -X utf8 tools/debug/signs_tour.py --original --out work/qa/games_signs8_jp --jobs 1 --only games143 games144 games163 games295 games306a games306b
python -X utf8 tools/debug/field_signs_review.py work/qa/games_signs8_fixed work/qa/games_signs8_jp --out work/qa/games_signs8_fixed_review
```

Each route uses its own native map initializer and a cold boot. Map 306's two
separate placements are checked separately. All six original and six English
rows in `coverage.tsv` are `ok`; English textlog has **0 Japanese lines in 6
logs** (graphics excluded). Cold smoke `games_signs8_fixed_smoke` passes.
The final full check passes **103 tests / lint 0**, including the wood-only
repair regression. The verifier reports **373 changed files / 0 errors**.

Main disc: **182,454,048 bytes**, **2026-11-01 11:40:47 UTC**, SHA-1
`606ce85331274eff4e3e495021c391f1f2e29112`.

## Scoped visual verdicts

Manifest: `work/qa/games_signs8_fixed_review/manifest.tsv`; verdicts beside it
in `verdicts/01_readonly.tsv`. All twelve sheets were read whole and enlarged.
English is left, a separate original cold capture is right. These verdicts
cover the Games boards only; visible adjacent Inn/Tea/shop labels remain open.

| Case | Context SHA-1 | Detail SHA-1 | Verdict |
| --- | --- | --- | --- |
| games143 | 02b92f39c7b7d3b134b5de516064dc68eac8ab8e | 6c6e17006f75f456ee5152551864be2dcbf1cd45 | ok |
| games144 | 760b05f506c56e30771fc5a83112c66b006ec9d7 | a3cc1d04c6c99452d9521e501825fefcc1007d52 | ok |
| games163 | 82ee6c501a0a7ee39a5d2f6be67adb9e6857a945 | c16b5b0cadd3643e403ef5df640449717c666458 | ok |
| games295 | 1ab4754a9449194067b1d8f5cad43f1cdae2614f | e47685e7318b3655629129cfc21f2af69727d0a9 | ok |
| games306a | e9fd3a1979d91bf62472298dbd3cd971e022bc8c | 118337d692398bf612802bb78c6d486cb9c8b63b | ok |
| games306b | d10ea1c2283f9b2a689012ae4a2b0f12a90623a1 | 118337d692398bf612802bb78c6d486cb9c8b63b | ok |

## Static consumer audit

`tools/debug/field_consumers.py KEY X0 Y0 X1 Y1 --out DIR` follows the actual
map table's texture/companion pair, then matches texture-page/CLUT identity
against tile records and ANM sprites. Its grid coordinates provide navigation
leads; they are not runtime evidence. The known displayed GV13000D:2 contest
board is a positive control: nine contiguous tiles in map 163, matching the
existing cold route. The Games records led to the six routes above.

GV02000D:2's split contest rectangle (184,192)-(256,224) has map-table owner
59 / GV02001D and **zero matching static tile or ANM records** in that paired
archive. This narrows the search; it does not prove absence from native-code
or story-controlled consumers. Its runtime coverage remains unresolved.

Skill gotchas for graphics/emulator QA: choose indices using the active CLUT,
filter repair samples by actual material, and compare the oracle's successful
frame. No shared skill files were changed.
