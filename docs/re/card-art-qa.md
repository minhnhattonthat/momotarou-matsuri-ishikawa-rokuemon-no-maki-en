# Card illustration sound effects, 2026-11-01

Phase 8 remains incomplete. This checkpoint translates **56 sound-effect
placements on 36 cards**. It does not approve the remaining card signs,
clothing lettering, crown marks, or the fragmented red Card Album notice.

## Implementation

`gfx/card_art.tsv` lists the Japanese reading, English effect, selection
windows, drawing rectangle and rotation for every placement. The affected
cards are 001, 002, 005, 006, 009, 010, 013, 014, 019, 024, 027, 028, 033,
035, 042, 045, 046, 047, 048, 049, 051, 055, 056, 064, 071, 073, 074, 076,
080, 081, 084, 089, 090, 091, 093 and 099. Repeated fragments are explicitly
listed; 56 is a placement count, not a count of distinct words or whole cards.

`tools/gfx_card_art.py` runs after the marginal phrases in
`tools/gen_card_words.py`, including full `gen_gfx.py` regeneration. It starts
from the original image every time. Fredoka at a maximum 14 pixels is the
normal lettering; labels that would have fewer than nine visible pixel rows
use the existing MIT seven-pixel capitals. The ink matches the original dark
grey. No font, palette, ANM, code, archive membership or image size changes
are needed. The existing full-archive sweep identifies these card TIMs as
unique, with no second copy to patch.

The initial rectangular white clears were rejected: some cut Momotaro's
hair, the dog's outline or the chair. The final erasure selects whole isolated
dark-ink components and includes their two-pixel antialias fringe. Fixed
reviewed limits, independent of the selected components, gate every changed
decoded pixel and TIM pixel. Explicit protections retain the hand's motion
lines on card 033, the door corner on 042 and an underwater bubble on 091.
Card 091 fills the removed strokes from nearby pale water colours instead of
leaving white patches. Card 006's lower chair-shaking lines are retained;
they are not part of the written effect.

The first cold visual pass also rejected the crowded first Twang on 019 and
the tiny Scrub pair on 055. Twang now runs vertically between the sleeve and
the brown caption, above the preserved sweat drops; the small-letter fallback
fixes Scrub. A later fresh pass rejected cramped Hop lettering on 014 and a
retained long-vowel stroke on 024; a taller drawing region and a wider stroke
selection fix those two problems. All other existing
captions, numbers, emblems, props and illustrations retain their source data
outside the declared edit regions. Character and prop pixel regressions
specifically guard the previously damaged neighbours.

`test_card_assets_match_current_translation_sources` regenerates all 100
cards in memory and compares the committed PNGs. A suspected card 062
translation mismatch during review was a misreading of its rotated caption:
both the existing TSV and the existing PNG already say **Costs a fortune!**,
matching the native gloss **Expensive**. No translation was changed for that
card. All 100 source phrases were compared with the native gloss list; the
previously documented card 001 source inconsistency remains unchanged.

## Reproduce

```powershell
python -X utf8 tools/gen_card_words.py
python -X utf8 tools/build.py
python -X utf8 "$(python tools/skill.py)/scripts/emu.py" build/momotarou-matsuri_en.cue --out work/qa/card_art8_final3_cold --script tools/debug/warp.lua --script tools/debug/cards.lua --script tools/lua/textlog.lua --var "SCENE='card_album'" --var HOLD=-1 --frames 900 --timeout 300
python -X utf8 tools/debug/cards_qa.py work/qa/card_art8_final3_cold --out work/qa/card_art8_final3_coverage
python -X utf8 tools/debug/card_art_review.py --run work/qa/card_art8_final3_cold --out work/qa/card_art8_final3_review
python -X utf8 tools/textlog.py work/qa/card_art8_final3_cold
python -X utf8 "$(python tools/skill.py)/scripts/qa_gate.py" init work/qa/card_art8_final3_review/manifest.tsv work/qa/card_art8_final3_review
python -X utf8 "$(python tools/skill.py)/scripts/qa_gate.py" check work/qa/card_art8_final3_review/manifest.tsv work/qa/card_art8_final3_review/verdicts
```

The tour uses the existing collectible-bit fixture and controller navigation,
then the game loads every card normally. It checks all 100 complete 208x128
illustrations and their caption strips, not only the modified lettering.
`card_art_review.py` makes original TIM / English cold-capture comparisons;
its optional `--grid 89 90` produces coordinate diagnostics, never QA evidence.
The original cold tour remains `work/qa/cards8_jp_all3` and passes the same
whole-card oracle with `--original`.

## Remaining card work

- Card 035's helper wears a sake label; card 062 has a price tag; card 068
  has a dumpling-shop banner; card 073 has a pufferfish-shop curtain. These
  have not been redrawn or approved by this sound-effect pass.
- Kintaro's kana badge and Poverty God's kana loincloth, plus small crown
  marks in several cards, need their own masks and legible English treatment.
  They are not covered by the product-logo exception.
- Small brown remnants below the existing marginal captions on 028, 045,
  046, 081 and 099 need another polish pass. This sound-effect review does
  not approve those older caption masks.
- The 64 cards without new sound effects were captured by the coverage tour,
  but this comparison manifest reviews only the 36 changed illustrations.
- HOUGEN0D's red notice still lacks a proven native renderer. Do not declare
  it absent solely because neither local ANM table references its fragments.

## Final validation and read-only verdicts

The main disc is **182,458,752 bytes**, built **2026-11-01 10:46:26 UTC**,
SHA-1 **d6c06dcc9a39d45fd49692aae423407608e33366**.

- `tools/check.py`: **101 passed**, lint **0 errors**. This includes all 100
  generated PNG comparisons and both decoded-pixel and TIM-index bounds.
- `tools/verify_build.py`: **369 files changed, 0 errors**; log in
  `work/qa/card_art_inventory/verify_main3.log`.
- Cold smoke `work/qa/card_art8_main3_smoke`: exit **0**, smoke passed.
- Cold album `work/qa/card_art8_final3_cold`: exit **0**; **100/100** complete
  card captures, none missing. `textlog.py`: **0 Japanese lines in 1 log**;
  that text hook does not inspect graphical lettering.
- Fresh read-only D10 review accepts **8/8 sound-effect comparison sheets**.
  The final2 pass rejected sheet 2, then the final3 cold re-review accepted
  its Hop and Pshh corrections. The other seven final3 sheets have identical
  SHA-1 hashes to the seven just inspected in the final2 read-only pass.
  Verdicts: `work/qa/card_art8_final3_review/verdicts/01_readonly.tsv`.
  `qa_gate.py check` reports no missing, rejected or changed sheets.

The manifest covers only the 36 changed cards' sound effects. It is not a
phase-wide verdict, nor approval of the remaining signs, emblems or caption
remnants listed above. The accepted sheet hashes are recorded here so the
review remains identifiable if the rebuildable work folder is cleaned:

| Sheet | SHA-1 |
| --- | --- |
| compare_sheet | `7515abf1985cc3b3a9bee3c93b8c296cf775af66` |
| compare_sheet_2 | `eb3ddc08af0bb0cb5dc9d4476f87904ca537e794` |
| compare_sheet_3 | `f3567e9f315f79756d40721be851f811d6521122` |
| compare_sheet_4 | `4bc8a61061069803e6aaa6e1a5c6c488794e11fa` |
| compare_sheet_5 | `9ddca04f8c4dcaa5ec2a65a1a6f96b6d27d40a2e` |
| compare_sheet_6 | `a1bfa3709747ef5b111730e633d53a602544c0d9` |
| compare_sheet_7 | `dbb3688320a1e59dfab420cc2b332b300716522a` |
| compare_sheet_8 | `0f0e041d66e87c1f481dc44a742eb3b18ec32c08` |
