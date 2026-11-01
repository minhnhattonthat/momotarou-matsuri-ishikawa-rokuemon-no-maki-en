# Status rank pictures and counter stress QA

This pass covers all six Status rank illustrations, four English rank plates,
and a fully populated counter panel. It fixes label overlap that the earlier
zero-value save fixture concealed. Phase 8 remains open outside this scope.

## Fixtures and actual game selection

```
python -X utf8 tools/debug/save_fixture.py --out work/qa/save_fixture_checked
python -X utf8 tools/gen_gfx.py --only STATUS0D.BIN:0 STATUS0D.BIN:1
python -X utf8 tools/build.py
python -X utf8 tools/debug/status_ranks.py --out work/qa/ranks8_final2
python -X utf8 tools/debug/status_ranks.py --original --out work/qa/ranks8_original_final
```

The harness boots cold for each case, copies the game-written memory card,
and follows `status_saved.txt`. After the file-selector mode 4A returns to
menu mode 49, it seeds RAM record values. It then opens Status normally (mode
4E). No sprite selector, ANM record, coordinate, code or save file is changed.
The source card is checked byte-identical after the tour.

Rank records begin at **0x800BDBF0**, stride **0x1C**, 70 records; Story rank is
the u32 at +4. EXE **0x80042374** sums those values. Status **0x800D933C** uses
that sum to choose six tiers at thresholds **20, 50, 100, 150 and 250**; it also
counts Full Mastery for rank 10 in the first 61 entries. The seven fixtures
are 0, 20, 50, 100, 150, 250 and 610, distributed as legal per-record ranks
0-10. Their Status items are ANM entry 4, items **21-26**. The first three
illustrations all share the Momotaro plate.

The 610 fixture additionally seeds:

| Value | RAM / interpretation |
|---|---|
| 100 cards | first 100 collectible bits at 0x800BD9F8; adjacent bits preserved |
| 9,999,999 ryo | u32 0x8008C504 |
| 9,999,999 steps | u32 0x8008C50C |
| 99:59 play time | u32 0x8008C560 = 21,596,400 frames |
| Pedometer | item 8 in the first free key-item slot at 0x800BDAE0 |

The pedometer check is EXE **0x800431D0**, which calls the inventory scan
`0x800328F4(category=1,item=8)`. Without it the original shows seven question
marks. The fixture asserts the loaded Status counter values at capture time;
the screenshot oracle requires every opaque pixel of the complete rank plate
**and** illustration to match their own ANM item in the same screenshot.
Rank and tier are also checked from the log. These are RAM fixtures, not proof
that a player has earned those ranks or played each minigame.

## Fixes

The previous `Money (ryo)` label overlaps seven-digit balances; `Total Cards`
crowds a three-digit total. Steps and Money now use the condensed seven-pixel
font and leave the original number columns clear. Money and the full `ryo`
unit occupy two short lines to the left of the balance. Total Cards uses a
smaller rounded font. Tests reserve the actual counter columns at x=95 and
x=136, including a separation margin.

Fresh enlarged comparisons rejected the earlier panel erasure: its rectangles
cut through separators/right bevels, filled transparent pixels, and left the
bottom of the Steps suffix. The right fragment is **12 opaque pixels plus
four transparent columns**, not a full 16-pixel panel. `gfx_status.clear_units`
copies its blank Play Time row to the three unit rows, preserving geometry.
The label rectangles now respect actual ANM bounds: Full Mastery stops before
the panel's top edge, Steps before the adjacent rank plate, and Status starts
below the large digit sprites. Regression tests preserve every digit/question
mark, all panel separators, the outer bevel and transparency.

The Hermit illustration contains a previously unlisted **仙** on its wooden
staff. `gfx_status.py` assembles two source fragments, letters **HER / MIT**
in the original gold colour, and scatters them back. The full word is kept;
the staff silhouette, grain outside the lettering, beard, cloud and other
five illustrations are preserved. The fragments are (120,88,32,16) and
(216,0,32,16) in STATUS0D entry 1. All animation data and palettes are unchanged.
The graphics survey now includes this additional row.

## Review and remaining scope

Final English tour `work/qa/ranks8_final2`: **7/7 complete rank pictures**.
Independent original tour `work/qa/ranks8_original_final`: **7/7**. The earlier
`ranks8_final` and `ranks8_fixed` captures are superseded; the first lacks the
staff redraw and the second was rejected for panel-border defects.

Fresh read-only D10 review inspected every complete 2x side-by-side comparison
(English left, original right), including all panel edges and the staff badge.
The original picture/number positions are preserved, English labels fit, and
the stress digits have clear gaps. Money/ryo uses two smaller native-pixel
lines, both readable and inside the panel. The hidden-step question marks in
non-stress cases match the original. All seven sheets have **fixed** verdicts
in `work/qa/ranks8_review/verdicts/review_02.tsv`, superseding the seven explicit
issue verdicts from the rejected redraw. The scoped gate passes **7/7**:

```
python -X utf8 "$(python tools/skill.py)/scripts/qa_gate.py" check work/qa/ranks8_review/manifest.tsv work/qa/ranks8_review/verdicts
```

| Sheet | SHA-1 | Verdict |
|---|---|---|
| rank000_sheet | 6ab2fcc65ea96af50af4c071c6db91d86aca69d7 | fixed: base peach, labels, borders |
| rank020_sheet | bd1aefade448be9a9ba960c9d918103cf1bc9c55 | fixed: baby, rank 20, mastery 2 |
| rank050_sheet | 6f7824081f64a3bfea6e2711c20d54aa90e3bab2 | fixed: child, rank 50, mastery 5 |
| rank100_sheet | 948cb831fa2aff3e0d1a95f3818f216df07c278e | fixed: Master and full illustration |
| rank150_sheet | 87cd325c80c7c4d8d7266e57a1ae3cf37e069324 | fixed: Expert and full illustration |
| rank250_sheet | cd4202ec3679061bb408010aa73196d399e80dc2 | fixed: Hermit and staff lettering |
| rank610_sheet | 0b053b79364d8c7cff80415bb8f2301b6d58e2e1 | fixed: all maximum-width counters |

Recreate each comparison with `sheet.py EN/status.png --compare JP/status.png
--zoom 2 --out work/qa/ranks8_review/rankNNN_sheet.png` after creating the output
folder. Re-run `qa_gate.py init` before reviewing changed sheets.

Validation: **80 tests passed**, lint 0; disc verifier **369 changed files,
0 errors**; cold smoke `work/qa/ranks8_final_smoke` passes. Runtime textlog:
**0 Japanese lines in 7 logs** (graphics are covered separately by images).
Main disc: **182,491,680 bytes**, built **2026-11-01 07:39:16 UTC**, SHA-1
`fcca7fe2b700c03a8be3012b24a24f71d02d87ce`.

This closes the higher Status rank-picture gap only. Saved-record categories
with nonzero scores, Game Album mode menus, Name Entry, broader graphics and
the corrected dialogue/story tour remain separate phase-8 work.

No shared skill files changed. Gotcha for `references/emulator-qa.md`: a
zero-value counter fixture can approve a label that overlaps longer numbers;
seed real input fields before UI construction and review their largest widths.
