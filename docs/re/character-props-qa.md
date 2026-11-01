# Character portrait lettering (phase 8)

The remaining lettering in the five title-attract portraits is translated:
Kintaro and Urashima's fans say **Festival**, and Ishikawa Rokuemon's ten coat
badges use **6** for their stylized 六 marks. This closes the portrait lettering
in survey rows #1/#2, including the earlier name-label work. It does not close
phase 8, the four separate GCV0310 name tags, or other occurrences of festival
marks in ending/card artwork.

## Source and preservation

`tools/gfx_intro.py` redraws only bounded regions of CHR0D:1/2. Both fans use
the complete word, split FEST / IVAL in the existing seven-pixel condensed
font. Their colours come from the original palette. The coat uses a hand-drawn
5x7 numeral, scaled/rotated to match the badges; two badges show the complete
numeral and eight are naturally clipped by the coat edges or folds.

All palettes, ANM records, timings and sprite positions are unchanged. The
archive-wide exact-TIM duplicate search finds only these two affected images.
The pixel-range test allows the named regions only; the portrait test renders
every character to ensure the name-label redraws do not damage other artwork.
A separate preservation test checks alpha silhouettes, all coloured coat
pixels, and both bamboo fan handles. The first redraw failed that last test at
two rib pixels, which are now explicitly excluded. The narrow left badge also
needed its numeral moved left one pixel to preserve its closed lower loop.

## Cold reproduction

```text
python -X utf8 tools/gen_gfx.py --only CHR0D.BIN:1 CHR0D.BIN:2
python -X utf8 tools/build.py
python -X utf8 tools/debug/character_intro.py --out work/qa/props8_final
python -X utf8 tools/debug/character_intro.py --original --out work/qa/props8_original
```

The existing harness waits through the natural title sequence for 9,600 frames,
without controller input, save data, warps or RAM substitutions. Both runs pass
**5/5 complete character/name pairs**, matched in the same screenshot. The
complete portrait match includes all edited prop pixels, not just the name.

| Character | Frame on both discs | Portrait position |
|---|---|---|
| Momotaro | 6540 | 24,48 |
| Kintaro | 7080 | 168,66 |
| Urashima | 7560 | 176,40 |
| Yashahime | 8040 | 32,24 |
| Ishikawa Rokuemon | 8520 | 40,16 |

The intro produces no textlog output: **0 Japanese lines in 0 logs** supplies
no text coverage. Approval rests on the full-portrait oracle and visual pass.

## Fresh read-only review (D10)

After the final build and cold runs, the worker inspected all three full-screen
comparison sheets at 2x, with English left and original right. The verdicts in
`work/qa/props8_review/verdicts/fresh.tsv` accept all three: both full fan words
are readable, the two complete numerals have their closed lower loops, partial
badges follow the original folds, and the characters/full names remain intact.
The fans have subtle original colour variation around the lettering; this is
not remaining Japanese text. No changes were made after this review.

| Sheet | SHA-1 | Verdict |
|---|---|---|
| kintaro_sheet | de8d340e221103a2c8b1a416b518e9cf4fcbf559 | ok |
| urashima_sheet | 56c7db85a751a13f62d9d36970fae19b93b0bdc7 | ok |
| rokuemon_sheet | 5971ebc8e5edf75670ed0ce731cff2ef20a584a5 | ok |

Regenerate each sheet with the skill's `sheet.py`, passing the English frame,
`--compare` the same original frame, `--zoom 2`, and the corresponding
`--out work/qa/props8_review/<name>_sheet.png`. Then run:

```text
python -X utf8 <skill>/scripts/qa_gate.py init work/qa/props8_review/manifest.tsv work/qa/props8_review
python -X utf8 <skill>/scripts/qa_gate.py check work/qa/props8_review/manifest.tsv work/qa/props8_review/verdicts
```

The scoped gate passes **3/3 sheets**. This is a fresh self-review explicitly
permitted by D10, not an independent agent review or a phase-wide verdict.

## Build and remaining work

`build/momotarou-matsuri_en.bin`: **182,491,680 bytes**, **2026-11-01 07:11:40 UTC**,
SHA-1 **6fd935950a81755dcc5a37796150790508af9c6c**. Validation: **76 tests passed**,
lint 0; verifier **369 changed files / 0 errors**; cold smoke
`work/qa/props8_smoke` passes.

Phase 8 remains incomplete. Other card/ending/town graphics, the full visual
manifest, caption routes, saved-record categories, natural minigame outcomes
and corrected map-interaction/story-state coverage are still open. These three
sheets do not authorize phase 9 or a release.

Gotcha for `references/graphics.md`: a bounding rectangle around lettering on a
prop may include the prop's ribs or handle; preserve those with an explicit
pixel exclusion and regression comparison. No shared skill files were changed.
