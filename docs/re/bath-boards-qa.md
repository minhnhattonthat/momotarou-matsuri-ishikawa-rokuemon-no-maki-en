# Bath roof boards

The large 湯 roof boards now read **Bath** in five cold original/English
placements: map180 and the northern/southern bathhouses in maps320/321.
A fresh read-only D10 pass accepts **10/10** context/detail sheets. This
resolves the large bath-plaque finding in the older Tea review, without
rewriting historical verdicts. Phase 8 remains incomplete.

## Sources and preservation

`tools/gfx_signs.py` describes two 48x32 assemblies:

| Atlas | Source pieces (x, y, width, height -> assembled x, y) | Native front-grid placements |
|---|---|---|
| GV36000D:0 | 96,64,48,32 -> 0,0 | maps320/321: (15..17,9..10), (14..16,42..43) |
| GV16000D:3 | 160,72,32,32 -> 0,0; 0,224,16,16 -> 32,0; 16,224,16,16 -> 32,16 | map180: (17..19,11..12) |

GV16001D table 2 records 1129-1131/1161-1163 assemble the latter board;
the right column is stored far below the main fragment. GV36001D tables
2/3 use records 74-76/106-108. Runtime palettes are recorded in each
tour's `coverage.tsv`. Whole-image duplicate generation also changes
M220D:3; its natural minigame placement remains unproved.

Only assembled rectangle (9,8)-(39,28) changes. The renderer removes both
engraved ink and highlights using nearby native wood, then draws the full
30x14 BATH mask with the existing MIT credits7 font at scale 2. No grid,
sprite-record, code, palette, board edge, mounting-post or roof changes.
The two boards' original outer pixels differ slightly and stay preserved.

The regression checks the inserted indices for every English stroke and
absence of old highlights, including the split final H. Existing whole-atlas
preservation checks protect every pixel outside all declared lettering
rectangles. An initial assertion that both complete boards were identical
failed because their original right-edge art differs; the final comparison
correctly covers their shared lettering panel, while the separate preservation
test still guards each native edge.

## Cold evidence and fresh read-only verdicts

```
python -X utf8 tools/gen_gfx.py --only GV36000D.BIN:0 GV16000D.BIN:3
python -X utf8 tools/build.py --out build/bath_boards8.bin
python -X utf8 tools/debug/signs_tour.py --cue build/bath_boards8.cue --out work/qa/bath_boards8_en --only bath_board180 bath_board320a bath_board320b bath_board321a bath_board321b
python -X utf8 tools/debug/signs_tour.py --original --out work/qa/bath_boards8_jp --only bath_board180 bath_board320a bath_board320b bath_board321a bath_board321b
python -X utf8 tools/debug/field_signs_review.py work/qa/bath_boards8_en work/qa/bath_boards8_jp --out work/qa/bath_boards8_review
python -X utf8 "$(python tools/skill.py)/scripts/qa_gate.py" check work/qa/bath_boards8_review/manifest.tsv work/qa/bath_boards8_review/verdicts
```

All five routes run the native map initializer, with no story-flag override.
Both discs pass **5/5** complete-lettering matches. Review inspected all ten
sheets after implementation, at full context and six-times lettering zoom.
The final H is intact across the split tile boundary, old engraving is gone,
and frames/posts/scenery are preserved. Maps320 and321 produce identical
accepted pixels but were separate cold runs. Exact hashes and scoped verdicts
are in `bath-boards-verdicts.tsv`; the gate has zero missing/stale/non-ok
verdicts. These are sign verdicts, not complete event or chapter verdicts.

The English textlog has **0 Japanese lines in 5 logs**; graphical symbols
and unvisited dialogue are outside that check. Cold smoke at
`work/qa/bath_boards8_smoke` passes. Build size **182,454,048 bytes**, build
time **2026-11-01 14:45:11 UTC**, SHA-1
`161e5adff5fae2c79cd691b2a86cc9cfbcd59b28`.

The repository check passes **121 tests / lint 0**; the built-disc verifier
reports **398 changed files / 0 errors**. A default main rebuild has the same
SHA-1 (built **2026-11-01 14:50:28 UTC**) and passes its own cold smoke at
`work/qa/bath_boards8_main_smoke`.

## Remaining field-sign leads

The complete large-glyph mask search at GV36000D:0 (109,72)-(130,93)
finds only that intact copy; the fragmented bath-town copy is explicitly
covered by the assembly above. The smaller ゆ glyph at GV16000D:0
(1,81)-(14,94) has eight exact occurrences: GF10000D:0/GF11000D:0/
GV00000D:0/GV31000D:0 at (209,81), GV04000D:0/GV04002D:0 at (1,153),
and GV16000D:0/M220D:0 at (1,81). Those small copies are unchanged.
Maps80/81's two matching static records have no grid uses; map180 has an
underlying rear-grid use at (18,12), behind the large board. These results
do not rule out native-code or later-story consumers.

Medicine has a concrete next seam. In both GV12001D and GV12003D table 2,
record 74 at atlas (64,80) occupies front grid cell (98,20); its neighbors
99 and101 match those used by the existing Items widening. All three use
CLUT31488/page5. The full word Medicine is 30 pixels with credits7, but the
native center is 16 pixels. After the existing Items allocation, the sunny
atlas has only two aligned unreferenced transparent 16x16 candidates:
(0,32) and (64,48). The snowy atlas additionally has (160,96). The current
widening needs three isolated cells, so it cannot simply be copied unchanged
to both variants; do not overwrite the Items slots. `field_label_plan.py`
now prints these remaining aligned slots as well as its older 48x16 search:

```
python -X utf8 tools/debug/field_label_plan.py GV12000D.BIN:0 64 80
python -X utf8 tools/debug/field_label_plan.py GV12002D.BIN:0 64 80
```

Possible next work is a verified two-tile layout or a broader atlas allocation
strategy. This is an implementation task, not an owner-only decision.
Other sign/emblem classification, remaining graphics/HUD outcomes and the
full interaction/story tour remain open in `docs/status.md`. No release or
repository visibility change was performed.
