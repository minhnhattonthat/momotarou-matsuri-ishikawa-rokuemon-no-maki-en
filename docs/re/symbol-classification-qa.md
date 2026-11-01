# Shrine papers and round banners, 2026-11-02

Seven cold original/English routes were inspected against the Medicine build
(`d0552aced38bba6aed45e37620cf76e7ddff331d`). The nine-sheet fresh D10 pass
has **five ok / four issues**, with no missing or stale verdicts. The gate
correctly remains red. Exact sheet hashes are in
`symbol-classification-verdicts.tsv`; phase 8 remains open.

## Findings

- The shrine papers in maps42-44 contain repeated dots, short bars and
  torii-like pictograms. The enlarged map44 comparison shows the complete
  patterns; no readable kana/kanji is present. Preserve these as drawing.
  Maps42/43's arrival views cut off part of the room, so their verdicts cover
  the visible area only. GV00020D:0/1 and exact GV00030D/GV00040D copies are
  unchanged. This resolves the paper-mark classification question in the
  historical sheet024, not all shrine interactions or offscreen states.
- The historical sheet001 note wrongly calls event01 a snow-scene placard.
  Both that frozen sheet and new original/English captures show a bath
  illustration with a snowman, without a placard. The expected snow-sculpture
  image EVT110D:0 is absent from all three captures. This was a review-note
  error, not evidence of a broken event route. No warp/code fix was made.
  EVT110D:0/1's actual snow sculptures, placards and costume marks remain
  separate unresolved artwork; do not infer their approval from event01.
- Maps66/123/192 share a seal-like circle on the purple game-hall curtain.
  Its reading remains ambiguous after enlargement; it is **not** approved as
  decoration. The exact source is GV02070D:2, circle (128,180)-(144,196),
  **CLUT row13**. Default CLUT0 makes the curtain black and obscures its look.
  The full banner sprite is (104,176,64,24), ANM entry3 item0 sprite0,
  CLUT31555, offset(-8,-24). Item1 uses only its upper-left 8x8 corner.
  The three scene textures have identical complete TIMs. Other copies of
  the circle occur in different images and must be handled explicitly if
  the emblem is redrawn. Map192's arrival crops the banner's upper edge.

The exact indexed-rectangle search finds **30** sources: GV01090D:2,
GV02060D:2, GV02070D:2, GV02080D:2, GV02090D:2, GV04060D:2, GV06120D:2,
GV08060D:2, GV08070D:2, GV08080D:2, GV08090D:2, GV09070D:2, GV12150D:2,
GV13080D:2, GV16110D:2, GV16120D:2, GV16200D:3, GV16210D:3, GV16220D:3,
GV16230D:3, GV16240D:3, GV22080D:2, GV22240D:2, GV23060D:2, GV23070D:2,
GV32050D:2, GV34060D:2, GV34070D:2, GV36060D:2 and GV38090D:2. Every match is
at (128,180). Static matches are leads, not proof of runtime display.

## Reproduction

```text
python -X utf8 tools/debug/warp_all.py build/medicine8.cue --out work/qa/classification8_en --only '^(event01|map_gv0002_042|map_gv0003_043|map_gv0004_044|map_gv0207_066|map_gv0809_123|map_gv1612_192)$' --hold 900 --click 45 --every 120 --probe tools/lua/textlog.lua --jobs 2
python -X utf8 tools/debug/warp_all.py --out work/qa/classification8_jp --only '^(event01|map_gv0002_042|map_gv0003_043|map_gv0004_044|map_gv0207_066|map_gv0809_123|map_gv1612_192)$' --hold 900 --click 45 --every 120 --jobs 2
python -X utf8 tools/gfx.py export GV02070D.BIN:2 --pal 13
python -X utf8 tools/debug/field_consumers.py GV02070D.BIN:2 104 176 168 224 --out work/gfx/banner_consumers
python -X utf8 tools/gfxfind_rect.py GV02070D.BIN:2 128 180 144 196
```

Both tours report 7/7 arrivals. Textlog reports 0 Japanese lines in seven
English logs, without graphics coverage. Context sheets compare each
`shots/SCENE.png` to its original counterpart with `sheet.py --zoom 2`.
The shrine detail uses map44 `--crop 75,26,175,150 --zoom 4`; the banner
detail uses map66 `--crop 97,5,30,24 --zoom 10`. Create the output directory
before calling `sheet.py`; it does not create parent directories. Initialize
and check `work/qa/classification8_review/manifest.tsv` with `qa_gate.py`.

Historical verdict files remain untouched. This supplementary pass does not
turn the old 25 non-ok sheets green or approve all intermediate dialogue.
No shared skill files changed. Gotcha for `references/emulator-qa.md`: verify
a review note against its actual sheet before treating it as a route bug.
