# Inn plaques, 2026-11-01

Both engraved forms of **宿** now read **Inn**: **34 placements in 28 atlases**,
including the identical M220D copy. The generated pixel-font lettering fits
inside the original 13x13 glyph rectangle. Board silhouettes, wood outside
that rectangle, roofs, palette data and map tile records are unchanged.

This is a scoped phase-8 checkpoint. Other shop signs, the separate sprite-strip
plaques, later story states and the phase-wide visual gate remain unfinished.

## Sources and copy audit

`tools/gfx_signs.py` lists 33 source rectangles in 27 atlases; the full-archive
duplicate sweep additionally generates M220D:0 from GV16000D:0. Two original
glyph patterns differ in their engraved strokes. Search every decompressed
archive texture, retaining their exact index-12/index-13 masks:

```
python -X utf8 tools/gfxfind_rect.py GV01000D.BIN:0 201 81 214 94 --indices 12 13
python -X utf8 tools/gfxfind_rect.py GV00000D.BIN:0 225 49 238 62 --indices 12 13
python -X utf8 tools/debug/inn_consumers.py
```

The searches return **22 + 12 placements**. The new rectangle finder requires
every row at the same aligned position, unlike the older row-search hints.
Its regression test rejects row wrapping, partial matches and bottom overrun.
The consumer audit follows each map's paired archive and reports tile-grid
positions; those positions are navigation leads, not visibility verdicts.

The roof sign in map45 is the strip at GV01000D:0 `(192,80)`, confirmed against
the cold screenshot under CLUT 1. A similar standalone plaque elsewhere in
the town atlases is often unused. Selecting it solely by its appearance would
leave the actual displayed sign Japanese.

## Palette failure and correction

The first GV30002D redraw lost parts of its letters. CLUT 0 assigns both wood
index 11 and lettering index 12 the RGB value `(16,8,0)`. PNG insertion chose
wood for newly drawn pixels; an exact screenshot-template match alone accepted
that damaged result because it used the same incorrect built pixels.

The new engraving regression requires every English stroke to use index 12
and no original index-13 highlight to remain in the glyph rectangle. It caught
the failure. `gen_gfx.EDIT_PALETTES` now selects CLUT 1 for GV30002D, yielding
`gfx/en/GV30002D_0_p1.png`; that palette distinguishes the indices. The old
CLUT-0 PNG is removed. The game keeps its original palettes, including the
dark blue lettering in this night scene. The earlier `inn_all8_en/inn285`
capture and its review are rejected, not release evidence.

## Cold routes

All routes use the map's own initializer and the existing headless warp.
They show the complete sign rather than relying on the emulator exit code.

| Maps | Atlas stem(s), entry 0 | Player position(s) |
| --- | --- | --- |
| 45 | GV01000D | 20,36 |
| 59 | GV02000D | 37,123 |
| 80 / 81 | GV04000D / GV04002D | 47,43 |
| 99 / 100 | GV06000D | 48,58 |
| 114 | GV08000D | 32,61 |
| 126 | GV09000D | 39,57 |
| 143 / 144 | GV12000D / GV12002D | 16,33 and 116,33 on each |
| 163 | GV13000D | 45,52 |
| 180 | GV16000D | 80,84 |
| 207 | GV20000D | 16,21 |
| 223 | GV21000D | 31,48 |
| 237 / 238 | GV22000D | 20,36 on rainy and sunny maps |
| 263 | GV23000D | 48,56 |
| 285 / 286 | GV30002D / GV30000D | 40,34 |
| 295 | GV32000D | 34,18 |
| 306 | GV34000D | 46,41 |
| 320 / 321 | GV36000D | 33,41 |
| 335 | GV38000D | 25,32 |

Reproduce the 26 placements on either disc:

```
python -X utf8 tools/build.py
python -X utf8 tools/debug/signs_tour.py --out work/qa/inn_final8_en --jobs 2 --only inn45 inn59 inn80 inn81 inn99 inn100 inn114 inn126 inn143a inn143b inn144a inn144b inn163 inn180 inn223 inn237 inn238 inn263 inn285 inn286 inn295 inn306 inn320 inn321 inn207 inn335
# Same arguments with --original and a different --out for the reference disc.
python -X utf8 tools/debug/field_signs_review.py work/qa/inn_final8_en work/qa/inn_final8_jp --out work/qa/inn_final8_review
python -X utf8 tools/textlog.py work/qa/inn_final8_en
```

The original reference index at `inn_final8_jp/coverage.tsv` combines the 24
captures in `inn_all8_jp` and the two in `inn_extra8_jp`; every row retains its
actual screenshot path. All are cold captures of the same original disc.
`CASE_LABELS` explicitly limits multi-plaque atlases to the displayed copy.
Rain uses the existing exact one-to-one colour-remapping oracle and a separate
visual colour check. Neither mechanism approves an undisplayed variant.

## Remaining visibility limits

- GF10000D/GF11000D/GV31000D's identical standalone plaque and GV00000D's
  variant have no matched static consumer. They are redrawn, not runtime-approved.
- The standalone copies in GV06000D, GV13000D and GV38000D, and both GV24000D
  copies, have no matched static consumer. This is not proof of universal
  native-code or story unreachability.
- GV04000D and GV32000D have a second plaque on the underlying map layer.
  The approved routes show the foreground variant; they do not prove the
  underlying copy is ever independently visible.
- GV20002D's map208 has a static Inn tile but no initializer in the known
  native transition scripts. It remains outside the cold coverage; no guessed
  initializer was added. The failed exploratory run recorded a KeyError before
  emulation for that case.
- M220D's duplicate is regenerated and covered by the pixel-preservation
  checks, but this checkpoint has no visible natural minigame placement.

These limits and the other Japanese shop labels remain phase-8 work. The old
corrected-tour manifest keeps its historical verdicts and build hashes.

## Fresh read-only verdicts and validation

The D10 pass inspected all **26 context pairs and 26 enlarged detail pairs**.
Each pair places English at left and a separate cold original capture at right.
All complete Inn words fit and remain readable; board boundaries, adjacent
roof tiles and the original snow/rain/night colours are preserved. The corrected
night lettering was also inspected separately at full detail resolution.
The Inn lettering passes all 26 details. The full-scene review also records
seven unresolved contexts: Tea plaques in inn143a/inn144a/inn295, the と shop
sign in inn237/inn238, the white purple-banner emblem in inn163, and the tiny
ground placard in inn180. The latter two need classification; they have not
been guessed to be non-text decoration.

The gate at `work/qa/inn_final8_review/manifest.tsv` with its sibling verdicts
directory reports **45 ok / 7 issues**, no stale or missing verdicts, and
correctly exits 1. `02_context_followup.tsv` records the seven whole-scene
findings after the initial lettering-only pass. The detail sheets are **26/26
ok**; the context sheets are **19/26 ok**. This gate cannot clear phase 8.
[inn-signs-verdicts.tsv](inn-signs-verdicts.tsv) preserves all 52 sheet SHA-1s
and authored verdicts. The contact overviews `details*.png` and `contexts*.png`
are review aids; the manifest hashes each underlying pair separately.

Final English and original coverage: **26/26 complete plaques each**. Textlog:
**0 Japanese lines in 26 English logs** (graphics excluded). Full check:
**107 tests passed / lint 0**. Disc verifier: **394 changed files / 0 errors**.
Cold smoke: `work/qa/inn_final8_smoke`, passed.

Final main disc: **182,451,696 bytes**, **2026-11-01 12:46:24 UTC**, SHA-1
`7e5908a7bc3a4b2d6b85346a18da1cb050d1c3b1`. No release was created.

Skill gotcha for `references/graphics.md`: an editing CLUT can alias wood and
ink even when the runtime CLUT distinguishes them; use an unambiguous editing
palette and assert the inserted indices, not just PNG colours. No shared
skill files were modified.
