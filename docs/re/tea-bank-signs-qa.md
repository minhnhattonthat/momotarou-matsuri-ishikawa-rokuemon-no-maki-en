# Tea and Bank roof plaques

Both engraved Tea patterns and both Bank patterns are translated. There are
**28 Tea placements and 23 Bank placements across 28 atlases**, including the
byte-identical M220D:0 copy. These are roof-mounted shop plaques; the separate
round sprite-strip signs are not covered by this change.

The glossary keeps 茶屋 as teahouse in prose and 茶 as Tea on these plaques.
The と plaque identifies といち屋, Bank. The condensed MIT credits7 font
fits Tea inside the original 13x13 ink rectangle. Bank uses the complete
16-pixel source span, with a seven-pixel-high word centered in
the same 13-pixel-high band. The extra columns were plain wood. This preserves
the full word without changing map records, sprite tables, palettes or roofs.

## Copy search and preservation

The four complete index-12/13 mask searches find 20 + 8 Tea placements and
17 + 6 Bank placements. They compare every row at the same aligned position,
not individual row hints:

```
python -X utf8 tools/gfxfind_rect.py GV12000D.BIN:0 49 81 62 94 --indices 12 13
python -X utf8 tools/gfxfind_rect.py GV20000D.BIN:0 33 81 46 94 --indices 12 13
python -X utf8 tools/gfxfind_rect.py GV22000D.BIN:0 49 81 62 94 --indices 12 13
python -X utf8 tools/gfxfind_rect.py GV20000D.BIN:0 65 81 78 94 --indices 12 13
python -X utf8 tools/debug/plaque_consumers.py tea
python -X utf8 tools/debug/plaque_consumers.py bank
```

`tools/gfx_signs.py` lists the sources, and `gen_gfx.py` regenerates their
exact full-image duplicates. `tests/test_signs.py` checks each English stroke
at the inserted palette-index level, rejects every remaining index-13 highlight
in the erase rectangles, and verifies every pixel outside the declared sign
rectangles is unchanged. The existing CLUT-1 editing override also applies to
the night Tea plaque, avoiding the CLUT-0 wood/ink alias documented in
`inn-signs-qa.md`.

## Cold routes

`tools/debug/signs_tour.py` contains 26 `tea*` and 22 `bank*` cases. Each uses
the map's own native initializer and a cold headless boot through `emu.py`.
The source texture's complete lettering must match a real screenshot. Rain
additionally uses the exact one-to-one palette-remapping matcher; visual
review must still judge its colours.

The first Tea routes for maps 99/100 used x=58. Their arrival captures placed
the plaque at the right edge: the narrower English lettering matched, while
the original glyph was clipped. Moving to x=63 shows the entire plaque in
both versions. The failed original coverage and the clipped English captures
are superseded; a lettering match alone does not approve a whole board.
The fresh visual pass caught the same framing problem in Bank maps 99/100:
the word matched but the left edge of the plaque was off-screen. Moving x=22
to x=17 and repeating both cold versions fixed it. All four replacement
context/detail pairs were inspected again before the final verdict file.

Use the explicit case lists in `signs_tour.py` with `--only`. The accepted
combined English run is `work/qa/tea_bank8_en`; the original run is
`work/qa/tea8_jp`. Original captures were collected in Tea and Bank batches,
then indexed together with `--check-only` (no mixed original-disc versions).

```
python -X utf8 tools/debug/field_signs_review.py work/qa/tea_bank8_en work/qa/tea8_jp --out work/qa/tea_bank8_review
python -X utf8 tools/textlog.py work/qa/tea_bank8_en
python -X utf8 "$(python tools/skill.py)/scripts/qa_gate.py" init work/qa/tea_bank8_review/manifest.tsv work/qa/tea_bank8_review --glob '*sheet*.png'
python -X utf8 "$(python tools/skill.py)/scripts/qa_gate.py" check work/qa/tea_bank8_review/manifest.tsv work/qa/tea_bank8_review/verdicts
```

## Visibility limits

GF10000D/GF11000D/GV00000D/GV31000D have no static map consumer of their Tea or
Bank glyph. GV24000D's Tea has no static consumer either. This does not prove
absence from native-code or later-story use. Map208 has static consumers for
both signs but still lacks a known native initializer. M220D's exact duplicate
is generated and checked statically, without a visible natural gameplay
placement. No guessed initializer or story-state claim was added.

## Validation

The final English and original coverage indices each pass **48/48 complete
signs** (26 Tea, 22 Bank). Textlog finds **0 Japanese lines in 48 English
logs**; this excludes graphics and unreached dialogue. The D10 fresh read-only
pass inspected all 48 whole-scene pairs and 48 enlarged detail pairs, English
at left and original at right. Every new word is readable, complete and inside
its plaque; snow, rain, night colours and board silhouettes are preserved.

The details are **48/48 ok**. Whole scenes are **30 ok / 18 issues**, making
the combined gate **78 ok / 18 issues**, with no missing/stale verdicts or
changed sheets. `qa_gate.py check` correctly exits 1. The manually authored
verdicts, their exact image SHA-1s and remaining findings are archived in
[tea-bank-signs-verdicts.tsv](tea-bank-signs-verdicts.tsv).

The remaining whole-scene findings are Fish Shop and produce boards,
item/medicine/equipment/bath plaques, Games boards in maps 80/81 and 263,
the purple-banner emblem and the tiny ground placard. The Games boards are
additional runtime copies uncovered by these camera positions, not approvals
of the previously translated Games atlases. The historical Inn and corrected
tour manifests retain their original hashes and verdicts.

The combined build passes **109 tests / lint 0**, **394 changed files / 0
verification errors**, and the cold smoke at `work/qa/tea_bank8_smoke`.
Main disc: **182,451,696 bytes**, **2026-11-01 13:11:23 UTC**, SHA-1
`5061f496f11a4fa0be71e1c4bf936bfb181e2b7d`.

Phase-wide graphics, dialogue/story interaction and visual gates remain open.
No release has been created. No shared skill files were changed.

Skill gotcha for `references/emulator-qa.md`: an exact match of the translated
glyph rectangle can pass while the larger sign frame is off-screen. Inspect
the complete board and use camera positions that show it on both discs.
