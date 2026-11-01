# Games shop boards, 2026-11-01

Five more field atlases now say **Games** for ゆうぎ. Six cold map contexts
on each disc contain the complete lettering, and a fresh read-only D10 pass
accepts all twelve scoped context/detail sheets. Other Games variants, shop
signs and the phase-wide graphics/interaction work remain open.

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
