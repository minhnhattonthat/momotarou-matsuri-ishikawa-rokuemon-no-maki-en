# Field signs and map initializer correction (phase 8)

This checkpoint does **not** complete phase 8. The default map warps used the
wrong initializer; their earlier success count is not evidence that NPCs,
animated decorations or their dialogue were covered. See `map-initializers.md`.

## Redraws

`tools/gfx_signs.py` letters fixed signs in assembled tile space. The two Pun
Contest atlases use the complete glossary name, **World's Greatest Pun Contest**.
GV02000D:2 stores a 144x16 board as two 72x16 strips at (184,192) and (184,208).
GV13000D:2 stores it contiguously at (0,0). The outer frame is unchanged.

GV16090D:1's two 56x32 curtains read **Men's Bath** and **Women's Bath** on two
lines. Grey Japanese lettering is removed by borrowing coloured cloth from the
same row; transparent silhouettes, surrounding art and the texture palettes
remain unchanged. All three byte-identical atlases are patched: GV16090D:1,
GV36110D:1 and GV36120D:1. The generator's archive-wide duplicate scan and tests
guard this list. The font is the existing MIT `credits7.txt`.

## Cold routes and pixel checks

```
python -X utf8 tools/debug/signs_tour.py --out work/qa/signs8_final --jobs 1
python -X utf8 tools/debug/signs_tour.py --original --out work/qa/signs8_reference --jobs 1
python -X utf8 tools/debug/signs_tour.py --check-only --out work/qa/signs8_final
```

The contest route starts in map 163's courtyard at (40,33), direction 0, with
initializer 0x1C4. Bath routes start at (21,24), direction 2, on maps 189/332/333
with initializers 0x20C/0x39B/0x39D; `field_walk.lua` presses Up for 160 frames.
No texture, camera or actor memory is substituted by these routes.

Both original and English gates accept **7/7** complete sign interiors in four cold contexts.
It compares every pixel of the complete lettering area, including backgrounds,
against the patched TIM's palette variants. The contest uses palette 2; the
men's curtain uses palette 0 and the women's curtain palette 1. Testing only the
atlas's first palette incorrectly reported the red women's curtain missing.
Tile decorations can cover a board's outer edge, so the oracle checks its entire
lettering interior; visual review must separately inspect the frame and neighbours.

The pre-fix original route `work/qa/signs8_walk/map_gv1609_189` has **0/2**
curtains. With the right initializer and corrected Circle timing,
`work/qa/signs8_initwalk2_jp` has **2/2**. This is a runtime reproduction of the
warp bug, not a guessed source-code assertion.

## Limits

- GV02000D:2's split contest board is translated and regression-tested but has
  **no accepted runtime capture**. The default map 59's static layers show no
  contest board, and none of GV02001D:3's 27 ANM items uses its lettering strips.
  Do not count it as approved or classify it unused without
  checking alternate map/state consumers.
- Other signs in these town atlases remain Japanese. This is a scoped lettering
  checkpoint, not a whole-town visual approval.
- The restored bath-counter hanging placard at screen (144,80), about 32x16,
  needs classification. It is **GV16090D:1 at (128,0), 32x24, palette 2**;
  **GV16091D:3 ANM item 2** draws it with offset (-8,0). GSV1609D:1 creates
  actor 0x54B at (21,14). The tiny dark marks are visible now that the attendant
  and decorations actually load. It is outside the two curtain-label interiors
  approved here. The curtain items themselves are 64x32, with the lettering
  within the first 56 pixels as checked by the oracle.
- `tools/fieldmap.py GV1300 --out work/gfx/map.png` is a static navigation preview.
  It excludes actors, animation and story changes and is never a substitute for
  emulator evidence. Grid dimensions are bytes +4/+5 of a 0x23 entry; 16x16 tile
  cells are u16 indices after +8. The 0x0322 entry has count at +4 and 8-byte
  records after +8 (`u,v,CLUT,flags,page`). High page flags are ignored only by
  this preview; the runtime pixel gate verifies actual output.

## Validation and visual review

Fresh read-only self-review under D10 accepted **4/4** comparison sheets. Each
sheet places English on the left and its separate cold original run on the
right, at 2x size. Full contest lettering fits; both red and blue curtain labels
are legible with intact wooden frames and silhouettes. Nearby actors and art
match the original apart from ordinary NPC movement. The counter placard is
explicitly outside these scoped verdicts.

`qa_gate.py check work/qa/signs8_review/manifest.tsv work/qa/signs8_review/verdicts`
exits 0. Durable manifest hashes:

| Sheet | SHA-1 | Verdict |
|---|---|---|
| contest_sheet | d97d22b9808e11dfd39bae0348359dd18be02d70 | ok, complete title and intact frame |
| bath189_sheet | c6308ad89bd0891da8bc6a4b249fa902941adb3f | ok, both complete labels/palettes |
| bath332_sheet | 7d6b80bc180b02100f834d37fda603aad54acd5b | ok, separate cold map, same correct labels |
| bath333_sheet | 7d6b80bc180b02100f834d37fda603aad54acd5b | ok, third cold map, same correct labels |

Main disc: 182,498,736 bytes, 2026-11-01 06:27:20 UTC, SHA-1
`4493a392249171d9e12b467c1cfba74522e49a30`. `build/signs8.bin` is byte-identical.
The verifier reports **368 changed files / 0 errors**. Cold smoke
`work/qa/signs8_smoke` passes. Four targeted text logs contain **0 Japanese lines**
(graphics excluded). The full check passes **74 tests** and lint 0, including
the map-294 setup regression.
The destination initializer correction also passes **358/358 cold map loads**
with **0 Japanese lines in 358 logs**; those captures still need their broader
visual and interaction review (`map-initializers.md`).

Skill gotcha for `references/emulator-qa.md`: map-loader success does not prove
map initialization; retain the destination's following script call and verify
known actors/decorations, and stop queued confirm input during loading. Also,
`emu.py` clears numbered screenshots but leaves custom Lua names: `signs_tour.py`
clears only its own old captures and restricts the oracle to its expected names.
`sheet.py DIR` selects numbered `f<frame>.png` captures; pass an explicit file list
for custom names such as `walk_0120.png` (there is no `--glob` option).
No shared skill files were changed.
