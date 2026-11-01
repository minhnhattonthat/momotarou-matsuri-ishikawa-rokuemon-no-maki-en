# Games, Produce and Fish Shop boards

This checkpoint translates seven more Games atlases, nine Produce atlases and
four Fish Shop atlases. The 20 sign placements occupy 18 atlases because two
atlases hold both a Games and a Produce board. Cold original/English runs prove
ten Games, ten Produce and four Fish Shop placements. The second Fish Shop
texture, GV20002D:0, is translated but remains unproved in map208, which still
lacks a known native initializer. Phase 8 remains incomplete.

## Sources and preservation

`tools/gfx_signs.py` contains the explicit sources in `ENGRAVED_GAMES`,
`PRODUCE_ATLASES` and `FISH_ATLASES`. Full index-12/13 mask searches locate the
otherwise different atlases; full-image duplicate expansion alone misses them.

```
python -X utf8 tools/gfxfind_rect.py GV04000D.BIN:0 185 193 229 206 --indices 12 13
python -X utf8 tools/gfxfind_rect.py GV01000D.BIN:0 194 177 235 190 --indices 12 13
python -X utf8 tools/gfxfind_rect.py GV09000D.BIN:0 121 65 152 78 --indices 12 13
python -X utf8 tools/gfxfind_rect.py GV20000D.BIN:0 152 81 184 95 --indices 12 13
```

The Games search finds 14 original texture occurrences: seven newly edited
sources, six already translated sources and the existing M220D:3 duplicate.
The other searches find nine Produce and two plus two Fish Shop sources.
This covers these exact glyph families, not every differently drawn shop sign.

The smaller Games boards are contiguous 64x16 source strips. Their 44x14
lettering band fits the complete word in doubled MIT credits7 glyphs. Produce
and Fish Shop use the seven-pixel font without abbreviation. Remove only the
engraved stroke/highlight colours, using nearby wood on the same row; preserve
the board, roofing, palette, tile records and sprite records. The existing
CLUT-1 override also applies to GV30002D's night Produce board.

`tests/test_signs.py` checks inserted indices, full English strokes, absence of
the old highlight, and every pixel outside all declared sign rectangles. The
older Games test in `test_gfx.py` now explicitly covers its original `wood`
method; the new `engraved` method has its own regression. No old coverage was
removed. The generated PNG consistency test still covers every redraw.

## Cold routes

All routes use `emu.py` headlessly and each map's native initializer. The
pixel oracle requires the complete lettering in a real screenshot and all
comparison sheets were inspected in a fresh read-only D10 pass.

| Word | Maps / cases | Atlas stems (entry) |
| --- | --- | --- |
| Games | 59a, 59b | GV02000D (2) |
| Games | 80, 81 | GV04000D, GV04002D (0) |
| Games | 126, 223 | GV09000D (3), GV21000D (0) |
| Games | 263a, 263b | GV23000D (2), two native palettes |
| Games | 320, 321 | GV36000D (0) |
| Produce | 45, 80, 81, 99, 100 | GV01000D, GV04000D, GV04002D, GV06000D (0) |
| Produce | 143, 144, 163, 285, 286 | GV12000D, GV12002D, GV13000D, GV30002D, GV30000D (0) |
| Fish Shop | 126, 207, 237, 238 | GV09000D, GV20000D, GV22000D (0) |

Reproduce with the literal case names below; `--only` does not expand wildcards.
Omit `--cue` to use the identical current main image. Repeat with `--original`
and the corresponding `_jp` output directory for the reference captures.

```
python -X utf8 tools/debug/signs_tour.py --cue build/shops8.cue --out work/qa/engraved_games8_en --only games59a games59b games80 games81 games126 games223 games263a games263b games320 games321
python -X utf8 tools/debug/signs_tour.py --cue build/shops8.cue --out work/qa/shops8_en --only produce45 produce80 produce81 produce99 produce100 produce143 produce144 produce163 produce285 produce286 fish126 fish237 fish238 fish207
python -X utf8 tools/debug/field_signs_review.py work/qa/engraved_games8_en work/qa/engraved_games8_jp --out work/qa/engraved_games8_review
python -X utf8 tools/debug/field_signs_review.py work/qa/shops8_en work/qa/shops8_jp --out work/qa/shops8_review
```

### Maps 99/100: explicit graphics fixture

Their initializer 0x104 resolves to GSV0600D:1 via the eight-byte
`{u32 file_id, u32 entry}` table at OVLGMAIN 0x800E480C. Its final branches at
0x3F6 onward dispatch script 0x477 or 0x478. Both events contain a native op1A
moving actor 0 to (39,59), explaining why early attempts moved away from the
Produce board even with valid arrival coordinates. A controller walk begun
600 frames after map load was already inside that event. This is original
game behavior, not an English-disc loading failure.

The two Produce routes use native pre-ops `2B 006F 0000; 2B 0090 0003` to
suppress those branches while retaining the complete map initializer. Opcode
2B at EXE 0x80034FE0 writes a single two-bit flag in 0x800BD930; 2C reads it.
The final routes at (20,35) show complete boards, actors and surrounding art
on both discs. These two captures are **graphics fixtures**, not evidence of
natural progression to the corresponding story state. No story flag or code
change is inserted in the build, and no memory card is written.

## Verdicts and validation

The final Games run was repeated on the combined `shops8.bin`, replacing its
earlier Games-only build evidence. All 24 original and English sign matches
pass. The fresh visual pass accepts every detail pair: Games **10/10**, shop
boards **14/14**, including snow, daylight, night and rain palettes. Complete
boards remain visible and their frames and surrounding artwork are preserved.

Games has **20/20 ok** context/detail sheets. Shop boards have **22 ok / 6
issues** across 28 sheets, with zero missing, stale or changed verdicts. The
shop gate correctly exits 1. The six issues are other signage: flower-shop
plaques in 99/100, item plaques in 143/144, footwear/weapon/armor plaques in 45,
and the unclassified purple banner at the edge of 163. Exact sheet hashes and
manual verdicts are committed in [engraved-games-verdicts.tsv](engraved-games-verdicts.tsv)
and [shop-boards-verdicts.tsv](shop-boards-verdicts.tsv).

```
python -X utf8 "$(python tools/skill.py)/scripts/qa_gate.py" check work/qa/engraved_games8_review/manifest.tsv work/qa/engraved_games8_review/verdicts
python -X utf8 "$(python tools/skill.py)/scripts/qa_gate.py" check work/qa/shops8_review/manifest.tsv work/qa/shops8_review/verdicts
```

Full validation: **111 tests passed / lint 0**, disc verifier **394 changed
files / 0 errors**, **0 Japanese lines in 24 English logs**, and cold smoke
passes at `work/qa/shops8_smoke` and `work/qa/shop_boards8_main_smoke`. Text logs
exclude graphics and dialogue not reached by these routes.

The verified combined image was copied byte-for-byte to the main build:
**182,451,696 bytes**, build timestamp **2026-11-01 13:39:20 UTC**, SHA-1
`1af379e36d3a23e8bc65b2ec8f131508afc16f9d`. No release was created. No shared
skill files were changed.

Still open: other shop/round-sprite variants, bath and costume marks, the
split contest board consumer, map208, full dialogue/story routes, HUD natural
outcomes and the phase-wide visual/graphics gate. Historical manifests retain
their original verdicts and hashes; this checkpoint does not retroactively
approve them. For `references/emulator-qa.md`: native map initialization can
launch a story event after the arrival shot, so a successful warp or delayed
controller route is not proof that the camera stayed at the requested sign.
