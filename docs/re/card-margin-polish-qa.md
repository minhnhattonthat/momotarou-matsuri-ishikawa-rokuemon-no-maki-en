# Card caption cleanup, 2026-11-02

Six cards have corrected caption-erasure masks: **003, 011, 022, 045, 085
and 086**. Their English wording, placement, fonts and colours are unchanged.
The new menu-title coverage is recorded separately in `menu-titles-qa.md`.
**Phase 8 remains incomplete; these are scoped graphics checks.**

## Findings and repairs

| Card | Problem | Repair |
|---|---|---|
| 003 | Left stroke of ば survived at x179-180 | Clear the complete blank-paper caption area, keeping the dog's adjacent breath puff |
| 011 | Final っ extended below the old y86 erase bound | Extend erasure to y92; propagate the original cave colours, not white |
| 022 | Pale/grey stroke remnants beside Let me join in! | Two stepped paper rectangles clear the lettering and retain the ear edge at x179-181, y33-61 |
| 045 | Pale warm fringe survived the brown-ink threshold | Include pale warm pixels without dilating them into the shoreline; clear verified blank-paper subregions |
| 085 | Pale warm fringe survived beside Quit your griping! | Same bounded selection; a small paper region removes a propagated grey streak while retaining smoke |
| 086 | First kana began above y10; paper fill cut a pink heart | Begin at y7 and use colour propagation instead of a rectangular paper clear |

The first candidate expanded all pale pixels before erasing. It visibly cut
the grey shoreline and smoke, so it was rejected. Pale-pixel additions now
remain undilated. The cold enlarged review then caught grey antialias donors
propagating into vertical streaks at (13,91-98) on card 045 and (7,32-37) on
card 085. Explicit blank-paper subregions remove those; their boundaries stop
before the actual shoreline and smoke. Original-English comparisons preserve
these rejected sheets in `work/qa/card_polish8_rejected`:

| Rejected sheet | SHA-1 |
|---|---|
| cards_sheet.png | 958719923995823074f439a6a2609db131bea4b5 |
| card045_sheet.png | 8ab66b3e5f99b3146a499ed3d6866362b031ad38 |
| card085_sheet.png | 62a1dd6d73d453ac2e59fbfd3b82835c2345f629 |

Regeneration through `tools/gen_card_words.py` changes six card PNGs; the
other 94 remain byte-identical. Existing tests require every output to match
its source generator and every changed pixel/index to stay inside declared
bounds. New regressions cover the formerly retained kana, ear and breath
puff, heart pixels, pale fringe and the rejected grey streaks. Palette,
dimensions, sprite layout, scripts and engine code are unchanged.

## Reproduction

```powershell
python -X utf8 tools/gen_card_words.py
python -X utf8 tools/build.py
python -X utf8 <skill>/scripts/emu.py build/momotarou-matsuri_en.cue --out work/qa/card_polish8_accepted_cold --script tools/debug/warp.lua --script tools/debug/cards.lua --script tools/lua/textlog.lua --var "SCENE='card_album'" --var HOLD=-1 --frames 900 --timeout 360
python -X utf8 tools/debug/cards_qa.py work/qa/card_polish8_accepted_cold --out work/qa/card_polish8_accepted_coverage
python -X utf8 tools/debug/card_art_review.py --run work/qa/card_polish8_accepted_cold --out work/qa/card_polish8_final_review/cards --cards 3 11 22 45 85 86
```

`<skill>` is `python tools/skill.py`'s output. As in the earlier album tour,
collectible bits are seeded in RAM; native controller navigation loads every
card. This does not prove story acquisition. The complete-card oracle checks
all 100 illustrations and prefecture strips, not just the six repaired cards.
Original cold detail controls are `work/qa/cards8_jp_all3/card_NNN.png`.

The six detail sheets use `sheet.py` on cold English and original captures,
`--zoom 6`, with screen-space crops:

| Card | x,y,width,height |
|---|---|
| 003 | 230,62,34,98 |
| 011 | 234,56,30,100 |
| 022 | 231,63,30,60 |
| 045 | 56,56,35,125 |
| 085 | 56,56,34,125 |
| 086 | 234,60,30,68 |

Whole-card sheets show original left and cold English right; detail sheets
show cold English left and original right.

## Final validation and D10 review

The separate read-only pass inspected both complete-card sheets and all six
enlarged detail sheets. After rejecting the grey streaks, all three changed
sheets were regenerated and re-inspected; the other five hashes were
unchanged. **8/8 sheets are ok**, with no missing or stale verdicts, recorded
in `card-margin-polish-verdicts.tsv` and
`work/qa/card_polish8_final_review/verdicts/01_readonly.tsv`.

The final cold tour passes **100/100 complete illustration and caption
matches**; this is coverage, not visual approval of the other 94 cards.
`tools/check.py`: **126 tests passed, lint 0 errors**. Disc verifier:
**399 changed files, 0 errors**. Cold smoke at
`work/qa/card_polish8_accepted_smoke`: **passed**. The album textlog contains
**0 Japanese lines in one log**, excluding graphics.

Final main disc: `build/momotarou-matsuri_en.bin`, **182,454,048 bytes**,
built **2026-11-01 16:07:41 UTC**, SHA-1
**6ba02079bfa79409b99ce78d063942d6266eccdd**. The earlier
`card_polish8_cold` and `card_polish8_final_cold` runs predate the final
corrections; use `card_polish8_accepted_cold` for the accepted evidence.

## Remaining work

This review covers six cards, not every marginal caption in the album. The
red new-card notice, Rank Details title consumer, snow placards, ending gold
mark, round game-hall emblem, other field/minigame variants, full visual
manifest, NPC interactions and later story-state routes remain open. No owner
decision is needed for the remaining technical work, and no release was made.

No shared skill files changed. Gotcha for `references/graphics.md`: widening
a hue mask can erase adjacent grey linework, while a narrow mask can reuse
grey antialias pixels as fill donors; inspect enlarged cold captures and
limit paper clears to source-verified blank regions.
