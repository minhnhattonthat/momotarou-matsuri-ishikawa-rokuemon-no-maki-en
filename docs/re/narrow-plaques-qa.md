# Flowers and Items: wider field plaques

Six cold original/English placements now show complete **Flowers** or **Items**
labels. A fresh read-only D10 pass accepts all **12/12** full-context/detail
comparison sheets. Phase 8 remains incomplete: this resolves the narrow-plaque
implementation gap, not the remaining graphics survey or story/NPC tour.

## Verified layout change

The original maps draw only a central 16-pixel glyph tile. Painting a wider
word in its existing atlas neighborhood would either clip it or alter another
consumer. `tools/gfx_field.py` instead copies the three front-layer tiles into
three unused 16x16 atlas cells. It removes the central Japanese strokes and
highlights, extends the wooden panel across x=8..39/y=3..11, and draws the full
word with the existing MIT credits7 font. All pixels outside that panel and
the old central glyph are copied from the native roof tiles.

The four plans are explicit, guarded by original entry SHA-1 hashes:

| Texture / companion | Maps | Grid entries, center cell | Native front records | New texture slots |
|---|---|---|---|---|
| GV06000D:0 / GV06001D | 99, 100 | 0, (20,39) | 197, 200, 199 | (128,64), (144,208), (144,240) |
| GV12000D:0 / GV12001D | 143 | 0, (24,20) | 99, 71, 101 | same as above |
| GV12002D:0 / GV12003D | 144 | 0, (24,20) | 99, 71, 101 | same as above |
| GV22000D:0 / GV22001D | 237, 238 | 0 and 2, (70,26) | 742, 75, 744 | (176,240), (192,240), (208,240) |

Each layout uses previously unreferenced records 1021-1023. The table keeps
its original count of 1024, size, header and padding. The three replacements
copy each native record's CLUT, flags and page; the trailing per-record byte
at `8200 + record` is copied too (its semantics remain unclassified, and all
selected values are zero). Only three named front-grid cells per grid change.
GV06001D has two table variants, both patched. Rear grids, source records,
original source pixels and all other entries remain unchanged.

The inserted archive verifier admits only these exact replacements through
`gfx_layout.patch`; a stray grid/record byte still fails. `insert.files` now
includes layout-only companion archives, and `fieldmap.py --english` applies
their layouts in its navigation preview. The preview is not QA evidence.

`tests/test_field_labels.py` checks every destination against all decoded
tile/ANM consumers of its texture and every reserved record against all grids,
including rear grids. It also checks preserved surrounding pixels, full word
strokes, copied attributes, untouched entries, bad original hashes and a
negative verifier case. All allocated texels are originally transparent.
Unknown native/story consumers are not disproved by the static scan; cold
proof covers the six explicit placements only.

## Mixed palettes and rain

Maps237/238 draw the center tile with CLUT 30784 and the sides with 31616.
Each relocated tile retains its native CLUT. The screenshot oracle assembles
the expected image per tile, rather than pretending the whole board uses one
palette. The minor original white-shade difference is retained in daylight;
the rain palette maps those whites to the same dark blue.

Rain also changes wood colors differently in the two CLUTs and overlays
streaks. A single global one-to-one color remap was therefore insufficient.
`field_walk.lua` can now capture a VRAM dump beside each screenshot using
`WALK_VRAM=true`; the Flowers rain route waits without controller input and
captures every six frames for 360 frames. This Redux build exports a 2 MiB
1024-row GPU backing store, whose first 512 rows contain hardware VRAM.
The parser also accepts a 1 MiB hardware-sized dump.

Only the palette rows are read from the dump. Expected texture indices still
come from the original or built disc, never from captured texture pixels.
The oracle rejects an invisible or indistinguishable ink/wood palette and
requires every opaque pixel of a complete 48x16 assembly to match, within the
existing 8-level screenshot color tolerance. It searches for an unoccluded
frame; rain-covered pixels are not ignored. Regression coverage proves that
captured texture/framebuffer pixels cannot supply the expected word.

Accepted rain captures: English `walk_0006.png`, original `walk_0000.png`.
All six labels occur at (136,76), except maps99/100 at (136,108). Original and
English routes each pass **6/6**. The native darkening remains visible and the
full word is readable in the enlarged comparison.

## Reproduction and verdicts

```
python -X utf8 tools/gen_gfx.py --only GV06000D.BIN:0 GV12000D.BIN:0 GV12002D.BIN:0 GV22000D.BIN:0
python -X utf8 tools/build.py --out build/narrow8_final.bin
python -X utf8 tools/debug/signs_tour.py --cue build/narrow8_final.cue --out work/qa/narrow8_final_en --only flowers99 flowers100 items143 items144 flowers237 flowers238
python -X utf8 tools/debug/signs_tour.py --original --out work/qa/narrow8_final_jp --only flowers99 flowers100 items143 items144 flowers237 flowers238
python -X utf8 tools/debug/field_signs_review.py work/qa/narrow8_final_en work/qa/narrow8_final_jp --out work/qa/narrow8_final_review
python -X utf8 "$(python tools/skill.py)/scripts/qa_gate.py" check work/qa/narrow8_final_review/manifest.tsv work/qa/narrow8_final_review/verdicts
```

Maps99/100 retain the prior graphics fixture's explicit op2B story flags
0x6F=0 and 0x90=3 to avoid Dog moving the player away. All routes still run
the map's full native initializer. Maps143/144/237/238 need no flag override.
The rain scene's English dialogue fits, but this is not a full event verdict.

The fresh read-only review accepts complete lettering, widened wood, retained
roof/snow/mounting posts and the surrounding scenes. Exact hashes and scoped
verdicts are committed in `narrow-plaques-verdicts.tsv`. The gate reports
**12 sheets, zero missing/stale/non-ok verdicts**. Historical issue sheets are
not rewritten; this evidence resolves the Flowers/Items findings in them.

Validation: **120 tests passed / lint 0**; disc verifier **398 changed files /
0 errors**; **0 Japanese lines in 6 logs** (graphics and unvisited dialogue are
excluded); cold smoke passes for `narrow8_final` and the byte-identical default
main image (`work/qa/narrow8_main_smoke`). Disc size **182,454,048 bytes**, build
**2026-11-01 14:28:34 UTC**, SHA-1
`3231d03e8188cf2631110dc4f4f8d2b5a3618c8f`.

The original unplaced/underlying Japanese tiles remain in the archives. These
six native front-layer uses are translated; unknown later story rewrites still
need tour coverage. Medicine at GV01000D:0 (128,80)-(160,96) has two static tile
records, 102/103, but no default grid placement in map45; its runtime consumer
remains unknown. Other equipment sprite forms, bath plaques, emblems, HUD
outcomes and the full corrected interaction tour remain in `docs/status.md`.
No release or visibility change was performed.
